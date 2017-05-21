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

from pyramid.view import view_defaults, view_config
from stalker import Ticket

from stalker_pyramid.views import simple_entity_interpreter
from stalker_pyramid.views.entity import EntityViews
from stalker_pyramid.views.mixins import StatusMixinViews

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class TicketViews(EntityViews, StatusMixinViews):
    """views for Ticket class
    """

    som_class = Ticket
    local_params = [
        {
            'param_name': 'link_id',
            'arg_name': 'links',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'project_id',
            'arg_name': 'project',
            'is_list': False,
            'interpreter': simple_entity_interpreter,
            'nullable': False
        },
        {
            'param_name': 'priority',
        },
        {
            'param_name': 'summary',
        }
    ]

    @view_config(
        route_name='ticket',
        request_method='GET'
    )
    def get_entity(self):
        """return one Ticket instance data as JSON
        """

        # get link count
        sql_query = """
        select
            count(1)
        from "Ticket_SimpleEntities"
        where "Ticket_SimpleEntities".ticket_id = :id
        """

        from stalker.db.session import DBSession
        from sqlalchemy import text
        conn = DBSession.connection()
        result = conn.execute(text(sql_query), id=self.entity_id)
        link_count = result.fetchone()

        # get log count
        sql_query = """
        select
            count(1)
        from "TicketLogs"
        where "TicketLogs".ticket_id = :id
        """
        result = conn.execute(text(sql_query), id=self.entity_id)
        log_count = result.fetchone()
        logger.debug('log_count: %s' % log_count[0])

        # get related_ticket_count
        sql_query = """
        select
            count(1)
        from "Ticket_Related_Tickets" as trt
        where trt.ticket_id = :id
        """
        result = conn.execute(text(sql_query), id=self.entity_id)
        related_ticket_count = result.fetchone()

        entity_response = EntityViews.get_entity(self)

        from stalker_pyramid import entity_type_to_url
        data = {
            'links': {
                '$ref': '%s/%s/links' % (
                    entity_type_to_url[self.entity.entity_type],
                    self.entity_id
                ),
                'length': link_count[0]
            },
            'logs': {
                '$ref': '%s/%s/logs' %(
                    entity_type_to_url[self.entity.entity_type],
                    self.entity_id
                ),
                'length': log_count[0]
            },
            'number': self.entity.number,
            'owner': {
                'id': self.entity.owner.id,
                'name': self.entity.owner.name,
                'entity_type': self.entity.owner.entity_type,
                '$ref': '%s/%s' % (
                    entity_type_to_url[self.entity.owner.entity_type],
                    self.entity.owner.id
                )
            } if self.entity.owner else None,
            'priority': self.entity.priority,
            'project': {
                'id': self.entity.project.id,
                'name': self.entity.project.name,
                'entity_type': self.entity.project.entity_type,
                '$ref': '%s/%s' % (
                    entity_type_to_url[self.entity.project.entity_type],
                    self.entity.project.id
                ),
            },
            'related_tickets': {
                '$ref': '%s/%s/related_tickets' % (
                    entity_type_to_url[self.entity.entity_type],
                    self.entity_id
                ),
                'length': related_ticket_count[0]
            },
            'reported_by': entity_response.json_body['created_by'],
            'summary': self.entity.summary,
        }

        data.update(StatusMixinViews.get_entity(self))
        return self.update_response_data(entity_response, data)

    @view_config(
        route_name='tickets',
        request_method='GET'
    )
    def get_entities(self):
        """returns all Ticket instances
        """
        return super(TicketViews, self).get_entities()

    @view_config(
        route_name='ticket',
        request_method=['PATCH', 'POST']
    )
    def update_entity(self):
        """updates the entity
        """
        return super(TicketViews, self).update_entity()

    @view_config(
        route_name='tickets',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a new ticket
        """
        return super(TicketViews, self).create_entity()

    @view_config(
        route_name='ticket',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes a ticket
        """
        return super(TicketViews, self).delete_entity()

    @view_config(
        route_name='ticket_resolutions',
        request_method='GET'
    )
    def get_ticket_resolutions(self):
        """returns the available ticket resolutions
        """
        from stalker import defaults
        from pyramid.response import Response
        return Response(
            json_body=defaults['ticket_resolutions']
        )

    @view_config(
        route_name='ticket_workflow',
        request_method='GET'
    )
    def get_ticket_workflow(self):
        """returns the available ticket workflow
        """
        from stalker import defaults
        from pyramid.response import Response
        return Response(
            json_body=defaults['ticket_workflow']
        )

    # ACTIONS
    def resolve(self):
        """resolves the ticket with the given resolution
        """
        created_by_id = self.request.params['created_by_id']
        resolution = self.request.params['resolution']

        from stalker import User
        created_by = User.query.get(created_by_id)
        self.entity.resolve(created_by, resolution)

        return self.get_entity()

    def accept(self):
        """sets the owner of the ticket
        """
        created_by_id = self.request.params['created_by_id']

        from stalker import User
        created_by = User.query.get(created_by_id)
        self.entity.accept(created_by)

        return self.get_entity()

    def reassign(self):
        """assigns the ticket to a new owner
        """
        created_by_id = self.request.params['created_by_id']
        assign_to_id = self.request.params['assign_to_id']

        from stalker import User
        created_by = User.query.get(created_by_id)
        assign_to = User.query.get(assign_to_id)
        self.entity.reassign(created_by, assign_to)

        return self.get_entity()

    def reopen(self):
        """reopens the ticket
        """
        created_by_id = self.request.params['created_by_id']

        from stalker import User
        created_by = User.query.get(created_by_id)
        self.entity.reopen(created_by)

        return self.get_entity()

    # COLLECTIONS
    @view_config(
        route_name='ticket_links',
        request_method='GET'
    )
    def get_links(self):
        """returns ticket.links
        """
        from stalker import SimpleEntity
        from stalker.models.ticket import Ticket_SimpleEntities
        join = Ticket_SimpleEntities
        filters = [Ticket_SimpleEntities.c.ticket_id == self.entity_id]
        filters.extend(self.filter_generator(SimpleEntity))
        return self.collection_query(
            SimpleEntity,
            join=join,
            filters=filters
        )

    @view_config(
        route_name='ticket_links',
        request_method=['PATCH', 'POST']
    )
    def update_links(self):
        """updates the ticket.links attribute
        """
        link_ids = self.get_multi_integer(self.request, 'link_id')

        from stalker import SimpleEntity
        links = SimpleEntity.query.filter(SimpleEntity.id.in_(link_ids)).all()

        if self.request.method == 'PATCH':
            for link in links:
                if link not in self.entity.links:
                    self.entity.links.append(link)
        elif self.request.method == 'POST':
            self.entity.links = links

        import transaction
        transaction.commit()

        from pyramid.response import Response
        return Response('Updated links of ticket %s' % self.entity_id)

    @view_config(
        route_name='ticket_links',
        request_method='DELETE'
    )
    def delete_links(self):
        """removes items from the ticket.links attribute
        """
        link_ids = self.get_multi_integer(self.request, 'link_id')

        from stalker import SimpleEntity
        links = SimpleEntity.query.filter(SimpleEntity.id.in_(link_ids)).all()

        successfully_deleted_item_ids = []
        for link in links:
            if link in self.entity.links:
                self.entity.links.remove(link)
                successfully_deleted_item_ids.append(link.id)

        import transaction
        transaction.commit()

        from pyramid.response import Response
        return Response(
            'Deleted links [%s] from ticket %s' % (
                ', '.join(map(str, successfully_deleted_item_ids)),
                self.entity_id
            )
        )

    @view_config(
        route_name='ticket_related_tickets',
        request_method='GET'
    )
    def get_related_tickets(self):
        """returns ticket.related_tickets
        """
        from stalker.models.ticket import Ticket_Related_Tickets
        join = (Ticket_Related_Tickets,
                 Ticket.id == Ticket_Related_Tickets.c.related_ticket_id)
        filters = [Ticket_Related_Tickets.c.ticket_id == self.entity_id]
        filters.extend(self.filter_generator(Ticket))
        return self.collection_query(Ticket, join=join, filters=filters)

    @view_config(
        route_name='ticket_related_tickets',
        request_method=['PATCH', 'POST']
    )
    def update_related_tickets(self):
        """updates the ticket.related_tickets attribute
        """
        related_ticket_ids = \
            self.get_multi_integer(self.request, 'related_ticket_id')
        related_tickets = \
            Ticket.query.filter(Ticket.id.in_(related_ticket_ids)).all()

        if self.request.method == 'PATCH':
            for rt in related_tickets:
                if rt not in self.entity.related_tickets:
                    self.entity.related_tickets.append(rt)
        elif self.request.method == 'POST':
            self.entity.related_tickets = related_tickets

        import transaction
        transaction.commit()

    @view_config(
        route_name='ticket_related_tickets',
        request_method='DELETE'
    )
    def delete_related_tickets(self):
        """removes other tickets from the ticket.related_tickets attribute
        """
        related_ticket_ids = \
            self.get_multi_integer(self.request, 'related_ticket_id')
        related_tickets = \
            Ticket.query.filter(Ticket.id.in_(related_ticket_ids)).all()

        for rt in related_tickets:
            if rt in self.entity.related_tickets:
                self.entity.related_tickets.remove(rt)

        import transaction
        transaction.commit()

    @view_config(
        route_name='ticket_logs',
        request_method='GET'
    )
    def get_logs(self):
        """returns ticket.logs
        """
        from stalker.models.ticket import TicketLog
        filters = [TicketLog.ticket_id == self.entity_id]
        filters.extend(self.filter_generator(TicketLog))
        return self.collection_query(
            TicketLog,
            filters=filters
        )


# @view_config(
#     route_name='create_ticket'
# )
# def create_ticket(request):
#     """runs when creating a ticket
#     """
#     logged_in_user = get_logged_in_user(request)
#
#     #**************************************************************************
#     # collect data
#
#     description = request.params.get('description')
#     summary = request.params.get('summary')
#
#     project_id = request.params.get('project_id', None)
#     project = Project.query.filter(Project.id == project_id).first()
#
#     owner_id = request.params.get('owner_id', None)
#     owner = User.query.filter(User.id == owner_id).first()
#
#     priority = request.params.get('priority', "TRIVIAL")
#     type_name = request.params.get('type')
#
#     send_email = request.params.get('send_email', 1)  # for testing purposes
#
#     logger.debug('*******************************')
#
#     logger.debug('create_ticket is running')
#
#     logger.debug('project_id : %s' % project_id)
#     logger.debug('owner_id : %s' % owner_id)
#     logger.debug('owner: %s' % owner)
#
#     if not summary:
#         return Response('Please supply a summary', 500)
#
#     if not description:
#         return Response('Please supply a description', 500)
#
#     if not type_name:
#         return Response('Please supply a type for this ticket', 500)
#
#     type_ = Type.query.filter_by(name=type_name).first()
#
#     if not project:
#         return Response('There is no project with id: %s' % project_id, 500)
#
#     if owner_id:
#         if not owner:
#             # there is an owner id but no resource found
#             return Response('There is no user with id: %s' % owner_id, 500)
#     else:
#         return Response('Please supply an owner for this ticket', 500)
#
#     link_ids = get_multi_integer(request, 'link_ids')
#     links = Task.query.filter(Task.id.in_(link_ids)).all()
#
#     # we are ready to create the time log
#     # Ticket should handle the extension of the effort
#     utc_now = local_to_utc(datetime.datetime.now())
#     ticket = Ticket(
#         project=project,
#         summary=summary,
#         description=description,
#         priority=priority,
#         type=type_,
#         created_by=logged_in_user,
#         date_created=utc_now,
#         date_updated=utc_now
#     )
#     ticket.links = links
#     ticket.set_owner(owner)
#
#     # email the ticket to the owner and to the created by
#     if send_email:
#         # send email to responsible and resources of the task
#         mailer = get_mailer(request)
#
#         recipients = [logged_in_user.email, owner.email]
#
#         # append link resources
#         for link in links:
#             for resource in link.resources:
#                 recipients.append(resource.email)
#
#             for watcher in link.watchers:
#                 recipients.append(watcher.email)
#
#         # make recipients unique
#         recipients = list(set(recipients))
#
#         description_text = \
#             'A New Ticket for project "%s" has been created by %s with the ' \
#             'following description:\n\n%s' % (
#                 project.name, logged_in_user.name, description
#             )
#
#         # TODO: add project link, after the server can be reached outside
#         description_html = \
#             'A <strong>New Ticket</strong> for project <strong>%s</strong> ' \
#             'has been created by <strong>%s</strong> and assigned to ' \
#             '<strong>%s</strong> with the following description:<br><br>%s' % (
#                 project.name, logged_in_user.name, owner.name,
#                 description.replace('\n', '<br>')
#             )
#
#         message = Message(
#             subject='New Ticket: %s' % summary,
#             sender=dummy_email_address,
#             recipients=recipients,
#             body=description_text,
#             html=description_html
#         )
#         mailer.send_to_queue(message)
#
#     DBSession.add(ticket)
#
#     return Response('Ticket Created successfully')


# @view_config(
#     route_name='update_ticket',
# )
# def update_ticket(request):
#     """runs when updating a ticket
#     """
#     logged_in_user = get_logged_in_user(request)
#
#     ticket_id = request.matchdict.get('id', -1)
#     ticket = Ticket.query.filter_by(id=ticket_id).first()
#
#     # *************************************************************************
#     # collect data
#     comment = request.params.get('comment')
#     comment_as_text = request.params.get('comment_as_text')
#     action = request.params.get('action')
#
#     logger.debug('updating ticket')
#     if not ticket:
#         transaction.abort()
#         return Response('No ticket with id : %s' % ticket_id, 500)
#
#     utc_now = local_to_utc(datetime.datetime.now())
#     ticket_log = None
#
#     if not action.startswith('leave_as'):
#         if logged_in_user == ticket.owner or \
#            logged_in_user == ticket.created_by:
#             if action.startswith('resolve_as'):
#                 resolution = action.split(':')[1]
#                 ticket_log = ticket.resolve(logged_in_user, resolution)
#             elif action.startswith('set_owner'):
#                 user_id = int(action.split(':')[1])
#                 assign_to = User.query.get(user_id)
#                 ticket_log = ticket.reassign(logged_in_user, assign_to)
#             elif action.startswith('delete_resolution'):
#                 ticket_log = ticket.reopen(logged_in_user)
#             ticket.date_updated = utc_now
#             if ticket_log:
#                 ticket_log.date_created = utc_now
#                 ticket_log.date_updated = utc_now
#         else:
#             transaction.abort()
#             return Response(
#                 'Error: You are not the owner nor the creator of this ticket'
#                 '\n\nSo, you do not have permission to update the ticket', 500
#             )
#
#     # mail
#     recipients = [
#         logged_in_user.email,
#         ticket.created_by.email,
#         ticket.owner.email
#     ]
#
#     # append watchers of ticket.links to recipients
#     for link in ticket.links:
#         for watcher in link.watchers:
#             recipients.append(watcher.email)
#
#     # mail the comment to anybody related to the ticket
#     if comment:
#         # convert images to Links
#         attachments = []
#         comment, links = replace_img_data_with_links(comment)
#         if links:
#             # update created_by attributes of links
#             for link in links:
#                 link.created_by = logged_in_user
#
#                 # manage attachments
#                 link_full_path = \
#                     MediaManager.convert_file_link_to_full_path(link.full_path)
#                 link_data = open(link_full_path, "rb").read()
#
#                 link_extension = os.path.splitext(link.filename)[1].lower()
#                 mime_type = ''
#                 if link_extension in ['.jpeg', '.jpg']:
#                     mime_type = 'image/jpg'
#                 elif link_extension in ['.png']:
#                     mime_type = 'image/png'
#
#                 attachment = Attachment(
#                     link.filename,
#                     mime_type,
#                     link_data
#                 )
#                 attachments.append(attachment)
#             DBSession.add_all(links)
#
#         note_type = query_type('Note', 'Ticket Comment')
#         note_type.html_class = 'yellow'
#         note = Note(
#             content=comment,
#             created_by=logged_in_user,
#             date_created=utc_now,
#             type=note_type
#         )
#         ticket.comments.append(note)
#         DBSession.add(note)
#
#         # send email to the owner about the new comment
#         mailer = get_mailer(request)
#
#         # also inform ticket commenter
#         for t_comment in ticket.comments:
#             recipients.append(t_comment.created_by.email)
#
#         message_body_text = "%(who)s has added a the following comment to " \
#                             "%(ticket)s:\n\n%(comment)s"
#
#         message_body_html = "<div>%(who)s has added a the following comment " \
#                             "to %(ticket)s:<br><br>%(comment)s</div>"
#
#         message_body_text = message_body_text % {
#             'who': logged_in_user.name,
#             'ticket': "Ticket #%s" % ticket.number,
#             'comment': comment_as_text
#         }
#
#         message_body_html = message_body_html % {
#             'who': '<a href="%(link)s">%(name)s</a>' % {
#                 'link': request.route_url('view_user', id=logged_in_user.id),
#                 'name': logged_in_user.name
#             },
#             'ticket': '<a href="%(link)s">%(name)s</a>' % {
#                 'link': request.route_url('view_ticket', id=ticket.id),
#                 'name': "Ticket #%(number)s - %(summary)s" % {
#                     'number': ticket.number,
#                     'summary': ticket.summary
#                 }
#             },
#             'comment': re.sub(
#                 r'/SPL/[a-z0-9]+/[a-z0-9]+/',
#                 'cid:',
#                 comment
#             )
#         }
#
#         # make recipients unique
#         recipients = list(set(recipients))
#         message = Message(
#             subject="New Comment: Ticket #%s" % ticket.number,
#             sender=dummy_email_address,
#             recipients=recipients,
#             body=message_body_text,
#             html=message_body_html,
#             attachments=attachments
#         )
#         mailer.send_to_queue(message)
#
#     # mail about changes in ticket status
#     if ticket_log:
#         from stalker import TicketLog
#
#         assert isinstance(ticket_log, TicketLog)
#         mailer = get_mailer(request)
#
#         # just inform anybody in the previously created recipients list
#
#         message_body_text = \
#             '%(user)s has changed the status of %(ticket)s\n\n' \
#             'from "%(from)s" to "%(to)s"'
#
#         message_body_html = \
#             '<div>%(user)s has changed the status of ' \
#             '%(ticket)s:<br><br>from %(from)s to %(to)s</div>'
#
#         message_body_text = message_body_text % {
#             'user': ticket_log.created_by.name,
#             'ticket': "Ticket #%s" % ticket.number,
#             'from': ticket_log.from_status.name,
#             'to': ticket_log.to_status.name
#         }
#
#         message_body_html = message_body_html % {
#             'user': '<strong>%(name)s</strong>' % {
#                 'name': ticket_log.created_by.name
#             },
#             'ticket': "<strong>Ticket #%(number)s - %(summary)s</strong>" % {
#                 'number': ticket.number,
#                 'summary': ticket.summary
#             },
#             'from': '<strong>%s</strong>' % ticket_log.from_status.name,
#             'to': '<strong>%s</strong>' % ticket_log.to_status.name
#         }
#
#         message = Message(
#             subject="Status Updated:"
#                     "Ticket #%(ticket_number)s - %(ticket_summary)s" % {
#                         'ticket_number': ticket.number,
#                         'ticket_summary': ticket.summary
#                     },
#             sender=dummy_email_address,
#             recipients=recipients,
#             body=message_body_text,
#             html=message_body_html
#         )
#         mailer.send_to_queue(message)
#
#     logger.debug('successfully updated ticket')
#
#     request.session.flash('Success: Successfully updated ticket')
#     return Response('Successfully updated ticket')