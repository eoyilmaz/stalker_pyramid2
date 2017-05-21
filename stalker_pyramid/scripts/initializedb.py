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
import os
import sys


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def create_statuses_and_status_lists():
    """Creates the statuses needed for Project, Task, Asset, Shot and Sequence
    entities
    """
    # Also create basic Status and status lists for
    # Project, Asset, Shot, Sequence

    # Project
    from stalker import Status, StatusList
    project_status_list = StatusList.query\
        .filter_by(target_entity_type='Project').first()
    if not project_status_list:
        project_status_list = StatusList(name='Project Statuses',
                                         target_entity_type='Project')

    new = Status.query.filter_by(code='NEW').first()
    wip = Status.query.filter_by(code='WIP').first()
    cmpl = Status.query.filter_by(code='CMPL').first()

    # now use them in status lists
    project_status_list.statuses = [new, wip, cmpl]

    # Warning! Not using scoped_session here, it is the plain old session
    from stalker.db.session import DBSession
    DBSession.add_all([
        project_status_list,
    ])
    DBSession.commit()


def create_ticket_types():
    """Creates the extra ticket types
    """
    # create Review ticket type
    from stalker import Type
    review = Type.query.filter_by(name='Review').first()
    if not review:
        # create the review type for Tickets
        review = Type(
            target_entity_type='Ticket',
            name='Review',
            code='Review'
        )

    # Warning! Not using scoped_session here, it is the plain old session
    from stalker.db.session import DBSession
    DBSession.add(review)
    DBSession.commit()


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)

    from pyramid.paster import get_appsettings, setup_logging
    from stalker import db

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    db.setup(settings)
    db.init()

    # create statuses
    create_statuses_and_status_lists()
    create_ticket_types()


if __name__ == '__main__':
    main()
