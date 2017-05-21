# -*- coding: utf-8 -*-
# Stalker Pyramid a Web Based Production Asset Management System
# Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
#
# This file is part of Stalker Pyramid.
#
# Stalker Pyramid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Stalker Pyramid is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stalker Pyramid.  If not, see <http://www.gnu.org/licenses/>.
"""This is a helper script that you can run as a cron job per weekly
"""
import os
import sys
import datetime

import transaction

from jinja2 import Template

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message

from stalker import db, Task, User
from stalker_pyramid.views import dummy_email_address, utc_to_local

mailer = None
stalker_server_external_url = None
here = os.path.dirname(os.path.realpath(sys.argv[0]))
templates_path = os.path.join(here, 'templates')

resource_mail_html_template_path = os.path.join(
    templates_path,
    'weekly_digest_resource_template.jinja2'
)

responsible_mail_html_template_path = os.path.join(
    templates_path,
    'weekly_digest_responsible_template.jinja2'
)

resource_mail_html_template_content = None
resource_mail_html_template = None

responsible_mail_html_template_content = None
responsible_mail_html_template = None


def usage(argv):
    """shows usage
    """
    cmd = os.path.basename(argv[0])
    print(
        'usage: %s ,config_uri>\n'
        '(example: "%s development.ini")' % (cmd, cmd)
    )
    sys.exit(1)


def get_week_dates(date):
    """returns the start and end of week days of now
    """
    day_of_week = date.isoweekday()
    start_of_week = date - datetime.timedelta(days=day_of_week - 1)
    end_of_week = start_of_week + datetime.timedelta(days=6, hours=23,
                                                     minutes=59, seconds=59)
    return start_of_week, end_of_week


def get_this_week_dates():
    """returns the start and end date of this week
    """
    now = datetime.datetime.utcnow()\
        .replace(hour=0, minute=0, second=0, microsecond=0)

    return get_week_dates(now)


def convert_seconds_to_text(seconds):
    """returns a meaningful text out of the given seconds
    """

    return


def send_resource_remainder(resource):
    """sends the reminder mail to the resource
    """
    recipients = [resource.email]

    start_of_week, end_of_week = get_this_week_dates()

    tasks_ending_this_week = Task.query.join(Task.resources, User.tasks)\
        .filter(Task.computed_start < end_of_week)\
        .filter(Task.computed_end > start_of_week)\
        .filter(Task.computed_end < end_of_week)\
        .filter(User.id == resource.id)\
        .order_by(Task.end)\
        .all()

    tasks_continues = Task.query.join(Task.resources, User.tasks)\
        .filter(Task.computed_start < end_of_week)\
        .filter(Task.computed_end > end_of_week)\
        .filter(User.id == resource.id)\
        .order_by(Task.end)\
        .all()

    # skip if he/she doesn't have any tasks
    if len(tasks_ending_this_week) == 0 and len(tasks_continues) == 0:
        return

    rendered_template = resource_mail_html_template.render(
        user=resource,
        tasks_ending_this_week=tasks_ending_this_week,
        tasks_continues=tasks_continues,
        start_of_week=start_of_week,
        end_of_week=end_of_week,
        utc_to_local=utc_to_local,
        stalker_url=stalker_server_external_url
    )

    # with open(
    #     os.path.expanduser(
    #         '~/tmp/rendered_html_template_%s.html' % resource.id, 'w+'
    #     )
    # ) as f:
    #     f.write(rendered_template)

    message = Message(
        subject='Stalker Weekly Digest',
        sender=dummy_email_address,
        recipients=recipients,
        body='This is an HTMl email',
        html=rendered_template
    )

    mailer.send_to_queue(message)


def send_responsible_remainder(responsible):
    """sends the reminder mail to the responsible
    """
    recipients = [responsible.email]

    start_of_week, end_of_week = get_this_week_dates()

    tasks_ending_this_week = Task.query.join(Task.responsible, User.responsible_of)\
        .filter(Task.computed_start < end_of_week)\
        .filter(Task.computed_end > start_of_week)\
        .filter(Task.computed_end < end_of_week)\
        .filter(User.id == responsible.id)\
        .order_by(User.name)\
        .order_by(Task.end)\
        .all()

    tasks_continues = Task.query.join(Task.responsible, User.responsible_of)\
        .filter(Task.computed_start < end_of_week)\
        .filter(Task.computed_end > end_of_week)\
        .filter(User.id == responsible.id)\
        .filter(~Task.children.any())\
        .order_by(User.name)\
        .order_by(Task.end)\
        .all()

    # skip if he/she doesn't have any tasks
    if len(tasks_ending_this_week) == 0 and len(tasks_continues) == 0:
        return

    rendered_template = responsible_mail_html_template.render(
        user=responsible,
        tasks_ending_this_week=tasks_ending_this_week,
        tasks_continues=tasks_continues,
        start_of_week=start_of_week,
        end_of_week=end_of_week,
        utc_to_local=utc_to_local,
        stalker_url=stalker_server_external_url
    )

    # with open(
    #     os.path.expanduser(
    #         '~/tmp/rendered_html_template_%s.html' % responsible.id
    #     ), 'w+'
    # ) as f:
    #     f.write(rendered_template)

    message = Message(
        subject='Stalker Weekly Responsible Digest',
        sender=dummy_email_address,
        recipients=recipients,
        body='This is an HTMl email',
        html=rendered_template
    )

    mailer.send_to_queue(message)


def main(argv=sys.argv):
    """main function
    """
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    # global here
    global stalker_server_external_url
    global mailer
    global resource_mail_html_template
    global responsible_mail_html_template
    global resource_mail_html_template_content
    global responsible_mail_html_template_content

    # here = os.path.dirname(os.path.realpath(sys.argv[0]))
    stalker_server_external_url = settings.get('stalker.external_url')
    mailer = Mailer.from_settings(settings)

    with open(resource_mail_html_template_path) as f:
        resource_mail_html_template_content = f.read()

    with open(responsible_mail_html_template_path) as f:
        responsible_mail_html_template_content = f.read()

    resource_mail_html_template = Template(resource_mail_html_template_content)
    responsible_mail_html_template = Template(responsible_mail_html_template_content)

    db.setup(settings)

    for user in User.query.all():
        send_resource_remainder(user)
        send_responsible_remainder(user)

    transaction.commit()


if __name__ == '__main__':
    main()
