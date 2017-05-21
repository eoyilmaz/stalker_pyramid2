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

from stalker_pyramid.testing import UnitTestBase, FunctionalTestBase
from stalker_pyramid.views import ticket


class TicketViewsUnitTestCase(UnitTestBase):
    """unit tests for TicketViews class
    """

    def setUp(self):
        """create test data
        """
        super(TicketViewsUnitTestCase, self).setUp()

        from stalker import db, User, Project, Repository, Status, StatusList

        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user3)

        self.test_repo = Repository(
            name='Test Repository',
            windows_path='T:/some_path',
            linux_path='/mnt/T/some_path',
            osx_path='/volumes/T/some_path'
        )
        db.DBSession.add(self.test_repo)
        db.DBSession.commit()

        self.status_new = Status.query.filter(Status.code == 'NEW').first()
        self.status_wip = Status.query.filter(Status.code == 'WIP').first()
        self.status_cmpl = Status.query.filter(Status.code == 'CMPL').first()
        self.status_assigned = \
            Status.query.filter(Status.code == 'ASG').first()
        self.status_accepted = \
            Status.query.filter(Status.code == 'ACP').first()
        self.status_closed = \
            Status.query.filter(Status.code == 'CLS').first()
        self.status_reopened = \
            Status.query.filter(Status.code == 'ROP').first()

        # get ticket statuses
        # self.status_

        self.ticket_status_list = \
            StatusList.query\
                .filter(StatusList.target_entity_type == 'Ticket')\
                .first()

        self.test_project_status_list = StatusList(
            name='Project Statuses',
            statuses=[self.status_new, self.status_wip, self.status_cmpl],
            target_entity_type='Project'
        )
        db.DBSession.add(self.test_project_status_list)
        db.DBSession.commit()

        # project1
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            repositories=[self.test_repo],
        )
        db.DBSession.add(self.test_project1)
        db.DBSession.commit()

        # project 2
        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            repositories=[self.test_repo],
        )
        db.DBSession.add(self.test_project2)
        db.DBSession.commit()

        from stalker import SimpleEntity
        self.test_link1 = SimpleEntity(
            name='Dummy Link 1'
        )
        db.DBSession.add(self.test_link1)
        self.test_link2 = SimpleEntity(
            name='Dummy Link 2'
        )
        db.DBSession.add(self.test_link1)
        self.test_link3 = SimpleEntity(
            name='Dummy Link 3'
        )
        db.DBSession.add(self.test_link1)
        db.DBSession.commit()

        # create tickets for project1
        from stalker import Ticket
        self.test_ticket1 = Ticket(
            description='This is a test ticket 1',
            project=self.test_project1,
            created_by=self.admin,
            links=[self.test_link1, self.test_link2],
            summary='This is the summary of ticket 1'
        )
        db.DBSession.add(self.test_ticket1)
        db.DBSession.commit()

        # assign an owner for this ticket
        self.test_ticket1.reassign(self.admin, self.test_user1)
        db.DBSession.commit()

        self.test_ticket2 = Ticket(
            description='This is a test ticket 2',
            project=self.test_project1,
            created_by=self.admin,
            links=[self.test_link1, self.test_link3],
            summary='This is the summary of ticket 2'
        )
        db.DBSession.add(self.test_ticket2)
        db.DBSession.commit()

        self.test_ticket3 = Ticket(
            description='This is a test ticket 3',
            project=self.test_project1,
            created_by=self.admin,
            links=[self.test_link2, self.test_link3],
            summary='This is the summary of ticket 3'
        )
        db.DBSession.add(self.test_ticket3)
        db.DBSession.commit()

        self.test_ticket3a = Ticket(
            description='This is a test ticket 3A',
            project=self.test_project1,
            created_by=self.admin,
            links=[],
            summary='This is the summary of ticket 3A'
        )
        db.DBSession.add(self.test_ticket3a)
        db.DBSession.commit()

        # create tickets for project2
        from stalker import Ticket
        self.test_ticket4 = Ticket(
            description='This is a test ticket 4',
            project=self.test_project2,
            created_by=self.admin,
            links=[self.test_link1, self.test_link2],
            summary='This is the summary of ticket 4'
        )
        db.DBSession.add(self.test_ticket4)
        db.DBSession.commit()

        self.test_ticket5 = Ticket(
            description='This is a test ticket 5',
            project=self.test_project2,
            created_by=self.admin,
            links=[self.test_link1, self.test_link3],
            summary='This is the summary of ticket 5'
        )
        db.DBSession.add(self.test_ticket5)
        db.DBSession.commit()

        self.test_ticket6 = Ticket(
            description='This is a test ticket 6',
            project=self.test_project2,
            created_by=self.admin,
            links=[self.test_link2, self.test_link3],
            summary='This is the summary of ticket 6'
        )
        db.DBSession.add(self.test_ticket6)
        db.DBSession.commit()

        # relate tickets to each other
        self.test_ticket1.related_tickets.append(self.test_ticket2)
        self.test_ticket1.related_tickets.append(self.test_ticket3)
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id
        ticket_view = ticket.TicketViews(request)

        response = ticket_view.get_entity()

        import stalker
        from stalker_pyramid.views import EntityViewBase

        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_ticket1.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_ticket1.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        self.test_ticket1.id,
                'length': 0
            },
            'id': self.test_ticket1.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % self.test_ticket1.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % self.test_ticket1.id,
                'length': 1
            },
            'name': self.test_ticket1.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % self.test_ticket1.id,
                'length': 0
            },
            'number': self.test_ticket1.number,
            'owner': {
                'id': self.test_ticket1.owner.id,
                'name': self.test_ticket1.owner.name,
                'entity_type': self.test_ticket1.owner.entity_type,
                '$ref': '/api/users/%s' % self.test_ticket1.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        self.test_ticket1.id,
                'length': 2
            },
            'reported_by': {
                'id': self.test_ticket1.reported_by.id,
                'name': self.test_ticket1.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % self.test_ticket1.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_assigned.id,
                'name': 'Assigned',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_assigned.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_entities_method_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        ticket_view = ticket.TicketViews(request)

        response = ticket_view.get_entities()
        expected_result = [
            {
                 'id': t.id,
                 'name': t.name,
                 'entity_type': 'Ticket',
                 '$ref': '/api/tickets/%s' % t.id
            } for t in [
                self.test_ticket1, self.test_ticket2, self.test_ticket3,
                self.test_ticket3a, self.test_ticket4, self.test_ticket5,
                self.test_ticket6
            ]
        ]

        self.assertEqual(
            sorted(response.json_body),
            sorted(expected_result)
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        ticket_view = ticket.TicketViews(request)

        request.params = DummyMultiDict()

        test_description = 'This is the new description'
        test_summary = 'This is the new summary'
        test_priority = 'MAJOR'

        request.params['description'] = test_description
        request.params['summary'] = test_summary
        request.params['priority'] = test_priority

        self.patch_logged_in_user(request)
        response = ticket_view.update_entity()

        from stalker import Ticket
        ticket_from_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(ticket_from_db.description, test_description)
        self.assertEqual(ticket_from_db.summary, test_summary)
        self.assertEqual(ticket_from_db.priority, test_priority)

    def test_create_entity_is_working_properly(self):
        """testing if the create_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()

        request.params = DummyMultiDict()
        request.params['project_id'] = self.test_project1.id
        request.params['summary'] = 'This is a new ticket'
        request.params['link_id'] = [
            self.test_link1.id, self.test_link2.id, self.test_link3.id
        ]
        request.params['description'] = \
            'This is a new ticket, and this is the description.'
        request.params['priority'] = 'MAJOR'

        ticket_view = ticket.TicketViews(request)

        self.patch_logged_in_user(request)
        response = ticket_view.create_entity()

        from stalker import Ticket
        new_ticket = Ticket.query\
            .filter(Ticket.summary == 'This is a new ticket')\
            .filter(Ticket.project_id == self.test_project1.id)\
            .first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    new_ticket.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    new_ticket.date_updated
                ),
            'description':
                'This is a new ticket, and this is the description.',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        new_ticket.id,
                'length': 0
            },
            'id': new_ticket.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % new_ticket.id,
                'length': 3
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % new_ticket.id,
                'length': 0
            },
            'name': new_ticket.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % new_ticket.id,
                'length': 0
            },
            'number': new_ticket.number,
            'owner': None,
            'priority': 'MAJOR',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        new_ticket.id,
                'length': 0
            },
            'reported_by': {
                'id': new_ticket.reported_by.id,
                'name': new_ticket.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % new_ticket.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_new.id,
                'name': 'New',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_new.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is a new ticket',
            'tags': {
                '$ref': '/api/entities/%s/tags' % new_ticket.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_delete_entity_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        ticket_view = ticket.TicketViews(request)
        ticket_view.delete_entity()

        from stalker import Ticket
        self.assertIsNone(Ticket.query.get(self.test_ticket1.id))

    # test actions
    def test_resolve_action_method_is_working_properly(self):
        """testing if the resolve action method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.admin.id
        request.params['resolution'] = 'fixed'

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.resolve()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 2
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_closed.id,
                'name': 'Closed',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_closed.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_accept_action_method_is_working_properly(self):
        """testing if the accept action method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.test_user1.id

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.accept()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                 ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 2
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_accepted.id,
                'name': 'Accepted',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_accepted.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_reassign_action_method_is_working_properly(self):
        """testing if the reassign action method is working properly
        """
        # first accept the ticket
        self.test_ticket1.accept(created_by=self.test_user1)

        # and now reassign it
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.admin.id
        request.params['assign_to_id'] = self.test_user2.id

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.reassign()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 3
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_assigned.id,
                'name': 'Assigned',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_assigned.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_reopen_action_method_is_working_properly(self):
        """testing if the reopen action method is working properly
        """
        # first close the ticket
        self.test_ticket1.resolve(self.admin, 'fixed')

        # now reopen
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.admin.id

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.reopen()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 3
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_reopened.id,
                'name': 'Reopened',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_reopened.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_ticket_resolutions_method_is_working_properly(self):
        """testing if get_ticket_resolutions() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        ticket_view = ticket.TicketViews(request)
        response = ticket_view.get_ticket_resolutions()
        self.assertEqual(
            response.json_body,
            [
                'fixed', 'invalid', 'wontfix', 'duplicate', 'worksforme',
                'cantfix'
            ]
        )

    def test_get_ticket_workflow_method_is_working_properly(self):
        """testing if get_ticket_workflow() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        ticket_view = ticket.TicketViews(request)
        response = ticket_view.get_ticket_workflow()
        self.assertEqual(
            response.json_body,
            {
                'resolve': {
                    'New': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                    'Accepted': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                    'Assigned': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                    'Reopened': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                },
                'accept': {
                    'New': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                    'Accepted': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                    'Assigned': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                    'Reopened': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                },
                'reassign': {
                    'New': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                    'Accepted': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                    'Assigned': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                    'Reopened': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                },
                'reopen': {
                    'Closed': {
                        'new_status': 'Reopened',
                        'action': 'del_resolution'
                    }
                }
            }
        )

    def test_get_links_method_is_working_properly(self):
        """testing if get_links() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        self.patch_logged_in_user(request)
        ticket_view = ticket.TicketViews(request)

        from stalker_pyramid import entity_type_to_url

        response = ticket_view.get_links()
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': l.id,
                    'name': l.name,
                    'entity_type': l.entity_type,
                    '$ref': '%s/%s' % (entity_type_to_url[l.entity_type], l.id)
                } for l in self.test_ticket1.links
            ]
        )

    def test_update_links_method_is_working_properly_with_patch(self):
        """testing if update_links() method is working properly with patch
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['link_id'] = [self.test_link3.id]
        request.method = 'PATCH'

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.update_links()

        from stalker import Ticket
        id_ = self.test_ticket1.id
        del self.test_ticket1
        test_ticket1_db = Ticket.query.get(id_)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link1, self.test_link2, self.test_link3]
        )

    def test_update_links_method_is_working_properly_with_post(self):
        """testing if update_links() method is working properly with post
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['link_id'] = [self.test_link3.id]
        request.method = 'POST'

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.update_links()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link3]
        )

    def test_delete_links_method_is_working_properly(self):
        """testing if delete_links()( method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['link_id'] = [self.test_link2.id]

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.delete_links()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link1]
        )

    def test_delete_links_method_is_working_properly_with_non_related_items(self):
        """testing if delete_links()( method is working properly with non
        related items
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['link_id'] = [self.test_link2.id, self.test_link3.id]

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.delete_links()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link1]
        )

    def test_get_related_tickets_method_is_working_properly(self):
        """testing if get_related_tickets() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id
        ticket_view = ticket.TicketViews(request)

        response = ticket_view.get_related_tickets()

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': t.id,
                    'name': t.name,
                    'entity_type': t.entity_type,
                    '$ref': '/api/tickets/%s' % t.id
                } for t in self.test_ticket1.related_tickets
            ]
        )

    def test_update_related_tickets_method_is_working_properly_with_patch(self):
        """testing if update_related_tickets() method is working properly with
        request.method is PATCH
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['related_ticket_id'] = [self.test_ticket3a.id]
        request.method = 'PATCH'

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.update_related_tickets()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket2, self.test_ticket3, self.test_ticket3a]
        )

    def test_update_related_tickets_method_is_working_properly_with_post(self):
        """testing if update_related_tickets() method is working properly with
        request.method is POST
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['related_ticket_id'] = [self.test_ticket3a.id]
        request.method = 'POST'

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.update_related_tickets()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket3a]
        )

    def test_delete_related_tickets_method_is_working_properly(self):
        """testing if delete_related_tickets()( method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['related_ticket_id'] = [self.test_ticket3.id]

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.delete_related_tickets()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket2]
        )

    def test_delete_related_tickets_method_is_working_properly_with_non_related_tickets(self):
        """testing if delete_related_tickets()( method is working properly
        with non-related tickets
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params = DummyMultiDict()
        request.params['related_ticket_id'] = [
            self.test_ticket3.id,
            self.test_ticket3a.id,
            self.test_ticket4.id
        ]

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.delete_related_tickets()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket2]
        )

    def test_get_logs_method_is_working_properly(self):
        """testing if get_logs() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.get_logs()

        from stalker_pyramid import entity_type_to_url
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': tl.id,
                    'name': tl.name,
                    'entity_type': tl.entity_type,
                    '$ref': '%s/%s' % (
                        entity_type_to_url[tl.entity_type], tl.id
                    )
                } for tl in self.test_ticket1.logs
            ]
        )


class TicketViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for TicketViews class
    """

    def setUp(self):
        """create test data
        """
        super(TicketViewsFunctionalTestCase, self).setUp()

        from stalker import db, User, Project, Repository, Status, StatusList

        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user3)

        self.test_repo = Repository(
            name='Test Repository',
            windows_path='T:/some_path',
            linux_path='/mnt/T/some_path',
            osx_path='/volumes/T/some_path'
        )
        db.DBSession.add(self.test_repo)
        db.DBSession.commit()

        self.status_new = Status.query.filter(Status.code == 'NEW').first()
        self.status_wip = Status.query.filter(Status.code == 'WIP').first()
        self.status_cmpl = Status.query.filter(Status.code == 'CMPL').first()
        self.status_assigned = \
            Status.query.filter(Status.code == 'ASG').first()
        self.status_accepted = \
            Status.query.filter(Status.code == 'ACP').first()
        self.status_closed = \
            Status.query.filter(Status.code == 'CLS').first()
        self.status_reopened = \
            Status.query.filter(Status.code == 'ROP').first()

        # get ticket statuses
        # self.status_

        self.ticket_status_list = \
            StatusList.query\
                .filter(StatusList.target_entity_type == 'Ticket')\
                .first()

        self.test_project_status_list = StatusList(
            name='Project Statuses',
            statuses=[self.status_new, self.status_wip, self.status_cmpl],
            target_entity_type='Project'
        )
        db.DBSession.add(self.test_project_status_list)
        db.DBSession.commit()

        # project1
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            repositories=[self.test_repo],
        )
        db.DBSession.add(self.test_project1)
        db.DBSession.commit()

        # project 2
        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            repositories=[self.test_repo],
        )
        db.DBSession.add(self.test_project2)
        db.DBSession.commit()

        from stalker import SimpleEntity
        self.test_link1 = SimpleEntity(
            name='Dummy Link 1'
        )
        db.DBSession.add(self.test_link1)
        self.test_link2 = SimpleEntity(
            name='Dummy Link 2'
        )
        db.DBSession.add(self.test_link1)
        self.test_link3 = SimpleEntity(
            name='Dummy Link 3'
        )
        db.DBSession.add(self.test_link1)
        db.DBSession.commit()

        # create tickets for project1
        from stalker import Ticket
        self.test_ticket1 = Ticket(
            description='This is a test ticket 1',
            project=self.test_project1,
            created_by=self.admin,
            links=[self.test_link1, self.test_link2],
            summary='This is the summary of ticket 1'
        )
        db.DBSession.add(self.test_ticket1)
        db.DBSession.commit()

        # assign an owner for this ticket
        self.test_ticket1.reassign(self.admin, self.test_user1)
        db.DBSession.commit()

        self.test_ticket2 = Ticket(
            description='This is a test ticket 2',
            project=self.test_project1,
            created_by=self.admin,
            links=[self.test_link1, self.test_link3],
            summary='This is the summary of ticket 2'
        )
        db.DBSession.add(self.test_ticket2)
        db.DBSession.commit()

        self.test_ticket3 = Ticket(
            description='This is a test ticket 3',
            project=self.test_project1,
            created_by=self.admin,
            links=[self.test_link2, self.test_link3],
            summary='This is the summary of ticket 3'
        )
        db.DBSession.add(self.test_ticket3)
        db.DBSession.commit()

        self.test_ticket3a = Ticket(
            description='This is a test ticket 3A',
            project=self.test_project1,
            created_by=self.admin,
            links=[],
            summary='This is the summary of ticket 3A'
        )
        db.DBSession.add(self.test_ticket3a)
        db.DBSession.commit()

        # create tickets for project2
        from stalker import Ticket
        self.test_ticket4 = Ticket(
            description='This is a test ticket 4',
            project=self.test_project2,
            created_by=self.admin,
            links=[self.test_link1, self.test_link2],
            summary='This is the summary of ticket 4'
        )
        db.DBSession.add(self.test_ticket4)
        db.DBSession.commit()

        self.test_ticket5 = Ticket(
            description='This is a test ticket 5',
            project=self.test_project2,
            created_by=self.admin,
            links=[self.test_link1, self.test_link3],
            summary='This is the summary of ticket 5'
        )
        db.DBSession.add(self.test_ticket5)
        db.DBSession.commit()

        self.test_ticket6 = Ticket(
            description='This is a test ticket 6',
            project=self.test_project2,
            created_by=self.admin,
            links=[self.test_link2, self.test_link3],
            summary='This is the summary of ticket 6'
        )
        db.DBSession.add(self.test_ticket6)
        db.DBSession.commit()

        # relate tickets to each other
        self.test_ticket1.related_tickets.append(self.test_ticket2)
        self.test_ticket1.related_tickets.append(self.test_ticket3)
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/tickets/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.get('/api/tickets/%s' % self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase

        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_ticket1.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_ticket1.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        self.test_ticket1.id,
                'length': 0
            },
            'id': self.test_ticket1.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % self.test_ticket1.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % self.test_ticket1.id,
                'length': 1
            },
            'name': self.test_ticket1.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % self.test_ticket1.id,
                'length': 0
            },
            'number': self.test_ticket1.number,
            'owner': {
                'id': self.test_ticket1.owner.id,
                'name': self.test_ticket1.owner.name,
                'entity_type': self.test_ticket1.owner.entity_type,
                '$ref': '/api/users/%s' % self.test_ticket1.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        self.test_ticket1.id,
                'length': 2
            },
            'reported_by': {
                'id': self.test_ticket1.reported_by.id,
                'name': self.test_ticket1.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % self.test_ticket1.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_assigned.id,
                'name': 'Assigned',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_assigned.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_entities_method_is_working_properly(self):
        """testing if GET: /api/tickets view is working properly
        """
        self.admin_login()
        response = self.test_app.get('/api/tickets')

        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [
                    {
                        'id': t.id,
                        'name': t.name,
                        'entity_type': 'Ticket',
                        '$ref': '/api/tickets/%s' % t.id
                    } for t in [self.test_ticket1, self.test_ticket2,
                                self.test_ticket3, self.test_ticket3a,
                                self.test_ticket4, self.test_ticket5,
                                self.test_ticket6]
                ]
            )
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/tickets/{id} method is working properly
        """

        test_description = 'This is the new description'
        test_summary = 'This is the new summary'
        test_priority = 'MAJOR'

        self.admin_login()
        response = self.test_app.patch(
            '/api/tickets/%s' % self.test_ticket1.id,
            params={
                'description': test_description,
                'summary': test_summary,
                'priority': test_priority
            }
        )

        from stalker import Ticket
        ticket_from_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(ticket_from_db.description, test_description)
        self.assertEqual(ticket_from_db.summary, test_summary)
        self.assertEqual(ticket_from_db.priority, test_priority)

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/tickets/{id} method is working properly
        """

        test_description = 'This is the new description'
        test_summary = 'This is the new summary'
        test_priority = 'MAJOR'

        self.admin_login()
        response = self.test_app.post(
            '/api/tickets/%s' % self.test_ticket1.id,
            params={
                'description': test_description,
                'summary': test_summary,
                'priority': test_priority
            }
        )

        from stalker import Ticket
        ticket_from_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(ticket_from_db.description, test_description)
        self.assertEqual(ticket_from_db.summary, test_summary)
        self.assertEqual(ticket_from_db.priority, test_priority)

    def test_create_entity_is_working_properly(self):
        """testing if the PUT: /api/tickets method is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/tickets',
            params={
                'project_id': self.test_project1.id,
                'summary': 'This is a new ticket',
                'link_id': [
                    self.test_link1.id, self.test_link2.id, self.test_link3.id
                ],
                'description':
                    'This is a new ticket, and this is the description.',
                'priority': 'MAJOR'
            },
            status=201
        )

        from stalker import Ticket
        new_ticket = Ticket.query\
            .filter(Ticket.summary == 'This is a new ticket')\
            .filter(Ticket.project_id == self.test_project1.id)\
            .first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    new_ticket.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    new_ticket.date_updated
                ),
            'description':
                'This is a new ticket, and this is the description.',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        new_ticket.id,
                'length': 0
            },
            'id': new_ticket.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % new_ticket.id,
                'length': 3
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % new_ticket.id,
                'length': 0
            },
            'name': new_ticket.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % new_ticket.id,
                'length': 0
            },
            'number': new_ticket.number,
            'owner': None,
            'priority': 'MAJOR',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        new_ticket.id,
                'length': 0
            },
            'reported_by': {
                'id': new_ticket.reported_by.id,
                'name': new_ticket.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % new_ticket.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_new.id,
                'name': 'New',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_new.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is a new ticket',
            'tags': {
                '$ref': '/api/entities/%s/tags' % new_ticket.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_delete_entity_is_working_properly(self):
        """testing if the DELETE: /api/tickets/{id} is working properly
        """
        self.admin_login()
        self.test_app.delete(
            '/api/tickets/%s' % self.test_ticket1.id
        )

        from stalker import Ticket
        self.assertIsNone(Ticket.query.get(self.test_ticket1.id))

    # test actions
    def test_resolve_action_method_is_working_properly(self):
        """testing if the resolve action method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.admin.id
        request.params['resolution'] = 'fixed'

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.resolve()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 2
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_closed.id,
                'name': 'Closed',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_closed.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_accept_action_method_is_working_properly(self):
        """testing if the accept action method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.test_user1.id

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.accept()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 2
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_accepted.id,
                'name': 'Accepted',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_accepted.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_reassign_action_method_is_working_properly(self):
        """testing if the reassign action method is working properly
        """
        # first accept the ticket
        self.test_ticket1.accept(created_by=self.test_user1)

        # and now reassign it
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.admin.id
        request.params['assign_to_id'] = self.test_user2.id

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.reassign()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 3
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_assigned.id,
                'name': 'Assigned',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_assigned.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_reopen_action_method_is_working_properly(self):
        """testing if the reopen action method is working properly
        """
        # first close the ticket
        self.test_ticket1.resolve(self.admin, 'fixed')

        # now reopen
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_ticket1.id

        request.params['created_by_id'] = self.admin.id

        ticket_view = ticket.TicketViews(request)
        response = ticket_view.reopen()

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'created_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    test_ticket1_db.date_updated
                ),
            'description': 'This is a test ticket 1',
            'entity_type': 'Ticket',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_ticket1_db.id,
                'length': 0
            },
            'id': test_ticket1_db.id,
            'links': {
                '$ref': '/api/tickets/%s/links' % test_ticket1_db.id,
                'length': 2
            },
            'logs': {
                '$ref': '/api/tickets/%s/logs' % test_ticket1_db.id,
                'length': 3
            },
            'name': test_ticket1_db.name,
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_ticket1_db.id,
                'length': 0
            },
            'number': test_ticket1_db.number,
            'owner': {
                'id': test_ticket1_db.owner.id,
                'name': test_ticket1_db.owner.name,
                'entity_type': test_ticket1_db.owner.entity_type,
                '$ref': '/api/users/%s' % test_ticket1_db.owner_id
            },
            'priority': 'TRIVIAL',
            'project': {
                'id': self.test_project1.id,
                'name': self.test_project1.name,
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'related_tickets': {
                '$ref': '/api/tickets/%s/related_tickets' %
                        test_ticket1_db.id,
                'length': 2
            },
            'reported_by': {
                'id': test_ticket1_db.reported_by.id,
                'name': test_ticket1_db.reported_by.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % test_ticket1_db.reported_by.id
            },
            'stalker_version': stalker.__version__,
            'status': {
                'id': self.status_reopened.id,
                'name': 'Reopened',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_reopened.id
            },
            'status_list': {
                'id': self.ticket_status_list.id,
                'name': self.ticket_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' % self.ticket_status_list.id
            },
            'summary': 'This is the summary of ticket 1',
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_ticket1.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'name': 'admin',
                'id': 3,
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_ticket_resolutions_method_is_working_properly(self):
        """testing if GET: /api/tickets/resolutions view is working properly
        """
        response = self.test_app.get(
            '/api/ticket_resolutions'
        )
        self.assertEqual(
            response.json_body,
            [
                'fixed', 'invalid', 'wontfix', 'duplicate', 'worksforme',
                'cantfix'
            ]
        )

    def test_get_ticket_workflow_method_is_working_properly(self):
        """testing if GET: /api/ticket_workflow view is working properly
        """
        response = self.test_app.get(
            '/api/ticket_workflow'
        )
        self.assertEqual(
            response.json_body,
            {
                'resolve': {
                    'New': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                    'Accepted': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                    'Assigned': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                    'Reopened': {
                        'new_status': 'Closed',
                        'action': 'set_resolution'
                    },
                },
                'accept': {
                    'New': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                    'Accepted': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                    'Assigned': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                    'Reopened': {
                        'new_status': 'Accepted',
                        'action': 'set_owner'
                    },
                },
                'reassign': {
                    'New': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                    'Accepted': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                    'Assigned': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                    'Reopened': {
                        'new_status': 'Assigned',
                        'action': 'set_owner'
                    },
                },
                'reopen': {
                    'Closed': {
                        'new_status': 'Reopened',
                        'action': 'del_resolution'
                    }
                }
            }
        )

    def test_get_links_method_is_working_properly(self):
        """testing if GET: /api/ticket/%s/links view is working properly
        """
        self.admin_login()
        response = self.test_app.get(
            '/api/tickets/%s/links' % self.test_ticket1.id,
            status=200
        )
        from stalker_pyramid import entity_type_to_url
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': l.id,
                    'name': l.name,
                    'entity_type': l.entity_type,
                    '$ref': '%s/%s' % (entity_type_to_url[l.entity_type], l.id)
                } for l in [self.test_link1, self.test_link2]
            ]
        )

    def test_update_links_method_is_working_properly_with_patch(self):
        """testing if PATCH: /api/tickets/{id}/links view is working properly
        """
        response = self.test_app.patch(
            '/api/tickets/%s/links' % self.test_ticket1.id,
            params={
                'link_id': [self.test_link3.id]
            },
            status=200
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link1, self.test_link2, self.test_link3]
        )

    def test_update_links_method_is_working_properly_with_post(self):
        """testing if POST: /api/tickets/{id}/links view is working properly
        """
        response = self.test_app.post(
            '/api/tickets/%s/links' % self.test_ticket1.id,
            params={
                'link_id': [self.test_link3.id],
            }
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link3]
        )

    def test_delete_links_method_is_working_properly(self):
        """testing if DELETE: /api/ticket/{id}/links view is working properly
        """
        self.test_app.delete(
            '/api/tickets/%s/links?link_id=%s' % (
                self.test_ticket1.id, self.test_link2.id
            ),
            status=200
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link1]
        )

    def test_delete_links_method_is_working_properly_with_non_related_items(self):
        """testing if DELETE: /api/ticket/{id}/links view is working properly
        with non related items
        """
        response = self.test_app.delete(
            '/api/tickets/%s/links?link_id=%s&link_id=%s' % (
                self.test_ticket1.id,
                self.test_link2.id,
                self.test_link3.id
            ),
            status=200
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.links,
            [self.test_link1]
        )

    def test_get_related_tickets_method_is_working_properly(self):
        """testing if GET: /api/tickets/{id}/related_tickets view is working
        properly
        """
        response = self.test_app.get(
            '/api/tickets/%s/related_tickets' % self.test_ticket1.id,
            status=200
        )
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': t.id,
                    'name': t.name,
                    'entity_type': t.entity_type,
                    '$ref': '/api/tickets/%s' % t.id
                } for t in self.test_ticket1.related_tickets
            ]
        )

    def test_update_related_tickets_method_is_working_properly_with_patch(self):
        """testing if PATCH: /api/tickets/{id}/related_tickets view is working
        properly
        """
        response = self.test_app.patch(
            '/api/tickets/%s/related_tickets' % self.test_ticket1.id,
            params={
                'related_ticket_id': [self.test_ticket3a.id]
            }
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket2, self.test_ticket3, self.test_ticket3a]
        )

    def test_update_related_tickets_method_is_working_properly_with_post(self):
        """testing if POST: /api/tickets/{id}/related_tickets view is working
        properly
        """
        response = self.test_app.post(
            '/api/tickets/%s/related_tickets' % self.test_ticket1.id,
            params={
                'related_ticket_id': [self.test_ticket3a.id]
            }
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket3a]
        )

    def test_delete_related_tickets_method_is_working_properly(self):
        """testing if DELETE: /api/tickets/{id}/related_tickets view is working
        properly
        """
        response = self.test_app.delete(
            '/api/tickets/%s/related_tickets?related_ticket_id=%s' %(
                self.test_ticket1.id, self.test_ticket3.id
            ),
            status=200
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket2]
        )

    def test_delete_related_tickets_method_is_working_properly_with_non_related_tickets(self):
        """testing if DELETE: /api/tickets/{id}/related_tickets view is working
        properly with non-related tickets
        """
        response = self.test_app.delete(
            '/api/tickets/%s/related_tickets?related_ticket_id=%s'
            '&related_ticket_id=%s&related_ticket_id=%s' % (
                self.test_ticket1.id,
                self.test_ticket3.id,
                self.test_ticket3a.id,
                self.test_ticket4.id
            ),
            status=200
        )

        from stalker import Ticket
        test_ticket1_db = Ticket.query.get(self.test_ticket1.id)

        self.assertEqual(
            test_ticket1_db.related_tickets,
            [self.test_ticket2]
        )

    def test_get_logs_method_is_working_properly(self):
        """testing if GET: /api/tickets/{id}/logs view is working properly
        """
        response = self.test_app.get(
            '/api/tickets/%s/logs' % self.test_ticket1.id,
            status=200
        )

        from stalker_pyramid import entity_type_to_url
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': tl.id,
                    'name': tl.name,
                    'entity_type': tl.entity_type,
                    '$ref': '%s/%s' % (
                        entity_type_to_url[tl.entity_type], tl.id
                    )
                } for tl in self.test_ticket1.logs
            ]
        )
