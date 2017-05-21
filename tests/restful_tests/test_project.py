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
from stalker_pyramid.views import project


class ProjectViewsUnitTestCase(UnitTestBase):
    """unit tests for ProjectViews class
    """

    def setUp(self):
        """create test data
        """
        super(ProjectViewsUnitTestCase, self).setUp()

        from stalker import User
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        from stalker import db
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

        self.test_user4 = User(
            name='Test User 4',
            login='tuser4',
            email='tuser4@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user4)

        self.test_user5 = User(
            name='Test User 5',
            login='tuser5',
            email='tuser5@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user5)

        from stalker import Repository
        self.test_repo1 = Repository(
            name='Test Repository 1',
            windows_path='T:/some_path1',
            linux_path='/mnt/T/some_path1',
            osx_path='/volumes/T/some_path1'
        )
        db.DBSession.add(self.test_repo1)
        db.DBSession.commit()

        self.test_repo2 = Repository(
            name='Test Repository 2',
            windows_path='T:/some_path2',
            linux_path='/mnt/T/some_path2',
            osx_path='/volumes/T/some_path2'
        )
        db.DBSession.add(self.test_repo2)
        db.DBSession.commit()

        self.test_repo3 = Repository(
            name='Test Repository 3',
            windows_path='T:/some_path3',
            linux_path='/mnt/T/some_path3',
            osx_path='/volumes/T/some_path3'
        )
        db.DBSession.add(self.test_repo3)
        db.DBSession.commit()

        self.test_repo4 = Repository(
            name='Test Repository 4',
            windows_path='T:/some_path4',
            linux_path='/mnt/T/some_path4',
            osx_path='/volumes/T/some_path4'
        )
        db.DBSession.add(self.test_repo4)
        db.DBSession.commit()

        from stalker import Status
        self.status_new = Status.query.filter(Status.code == 'NEW').first()
        self.status_wip = Status.query.filter(Status.code == 'WIP').first()
        self.status_cmpl = Status.query.filter(Status.code == 'CMPL').first()

        from stalker import StatusList
        self.test_project_status_list = StatusList(
            name='Project Statuses',
            statuses=[self.status_new, self.status_wip, self.status_cmpl],
            target_entity_type='Project'
        )
        db.DBSession.add(self.test_project_status_list)
        db.DBSession.commit()

        from stalker import ImageFormat
        self.test_image_format1 = ImageFormat(
            name='VR',
            width=4096,
            height=2048
        )
        db.DBSession.add(self.test_image_format1)

        self.test_image_format2 = ImageFormat(
            name='VR - Half',
            width=2048,
            height=1024
        )
        db.DBSession.add(self.test_image_format2)

        from stalker import Client
        self.test_client1 = Client(
            name='Test Client 1'
        )
        db.DBSession.add(self.test_client1)

        self.test_client2 = Client(
            name='Test Client 2'
        )
        db.DBSession.add(self.test_client2)

        self.test_client3 = Client(
            name='Test Client 3'
        )
        db.DBSession.add(self.test_client3)

        self.test_client4 = Client(
            name='Test Client 4'
        )
        db.DBSession.add(self.test_client4)

        # project1
        from stalker import Project
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            repositories=[self.test_repo1, self.test_repo2],
            created_by=self.admin,
            image_format=self.test_image_format1,
            clients=[self.test_client1, self.test_client2],
            users=[self.test_user1, self.test_user2, self.test_user3]
        )
        db.DBSession.add(self.test_project1)
        db.DBSession.commit()

        # project 2
        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            repositories=[self.test_repo1],
            created_by=self.admin
        )
        db.DBSession.add(self.test_project2)
        db.DBSession.commit()

        # create some tasks
        from stalker import Task
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task2)
        db.DBSession.commit()

        # some assets
        from stalker import Type
        self.test_asset_type = Type(
            name='Asset Type 1',
            code='AT1',
            target_entity_type='Asset'
        )
        db.DBSession.add(self.test_asset_type)
        db.DBSession.commit()

        from stalker import Asset
        self.test_asset1 = Asset(
            name='Test Asset 1',
            code='TA1',
            type=self.test_asset_type,
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_asset1)

        # and a shot
        from stalker import Shot
        self.test_shot1 = Shot(
            name='Test Shot',
            code='ts',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_shot1)
        db.DBSession.commit()

        # and some test tasks for the other project, so we'll be sure that it
        # is returning the tasks of the correct project
        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task3)
        db.DBSession.commit()

        from stalker import Link
        self.test_link1 = Link()
        self.test_link2 = Link()
        self.test_link3 = Link()
        self.test_project1.references = \
            [self.test_link1, self.test_link2, self.test_link3]

        self.test_link4 = Link()
        self.test_link5 = Link()
        self.test_task1.references = [self.test_link4, self.test_link5]
        self.test_task2.references = [self.test_link5]

        self.test_link6 = Link()
        self.test_link7 = Link()
        self.test_project2.references = [self.test_link6]
        self.test_task3.references = [self.test_link7]

        db.DBSession.add_all([
            self.test_link1, self.test_link2, self.test_link3, self.test_link4,
            self.test_link5, self.test_link6, self.test_link7
        ])
        db.DBSession.commit()

        from stalker import Daily
        self.test_daily1 = Daily(name='Daily1', project=self.test_project1)
        self.test_daily2 = Daily(name='Daily2', project=self.test_project1)
        self.test_daily3 = Daily(name='Daily3', project=self.test_project1)
        db.DBSession.add_all(
            [self.test_daily1, self.test_daily2, self.test_daily3]
        )

        self.test_daily4 = Daily(name='Daily4', project=self.test_project2)
        self.test_daily5 = Daily(name='Daily5', project=self.test_project2)
        self.test_daily6 = Daily(name='Daily6', project=self.test_project2)
        db.DBSession.add_all(
            [self.test_daily4, self.test_daily5, self.test_daily6]
        )
        db.DBSession.commit()

        from stalker import Ticket

        # for test_project1
        self.test_ticket1 = \
            Ticket(project=self.test_project1, summary='this is ticket 1')
        db.DBSession.add(self.test_ticket1)
        self.test_ticket2 = \
            Ticket(project=self.test_project1, summary='this is ticket 2')
        db.DBSession.add(self.test_ticket2)
        self.test_ticket3 = \
            Ticket(project=self.test_project1, summary='this is ticket 3')
        db.DBSession.add(self.test_ticket3)

        # for test_project2
        self.test_ticket4 = \
            Ticket(project=self.test_project2, summary='this is ticket 4')
        db.DBSession.add(self.test_ticket4)
        self.test_ticket5 = \
            Ticket(project=self.test_project2, summary='this is ticket 5')
        db.DBSession.add(self.test_ticket5)
        self.test_ticket6 = \
            Ticket(project=self.test_project2, summary='this is ticket 6')
        db.DBSession.add(self.test_ticket6)

        # create a couple of Budgets
        self.test_budget_status_list = StatusList(
            name='Budget Statuses',
            statuses=[self.status_new, self.status_cmpl],
            target_entity_type='Budget'
        )
        db.DBSession.add(self.test_budget_status_list)
        db.DBSession.commit()

        from stalker import Budget
        self.test_budget1 = Budget(
            name='Test Budget 1',
            project=self.test_project1
        )
        db.DBSession.add(self.test_budget1)

        self.test_budget2 = Budget(
            name='Test Budget 2',
            project=self.test_project1
        )
        db.DBSession.add(self.test_budget2)

        self.test_budget3 = Budget(
            name='Test Budget 3',
            project=self.test_project2
        )
        db.DBSession.add(self.test_budget3)
        db.DBSession.commit()

    def test_get_entity_method_is_working_properly(self):
        """testing if the get_entity() method is working properly
        """
        from pyramid_tm.tests import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        response = project_view.get_entity()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'clients': {
                '$ref': '/api/projects/%s/clients' % self.test_project1.id,
                'length': 2
            },
            'code': self.test_project1.code,
            'created_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'dailies': {
                '$ref': '/api/projects/%s/dailies' % self.test_project1.id,
                'length': 3
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_project1.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_project1.date_updated
                ),
            'description': '',
            'end': EntityViewBase.milliseconds_since_epoch(
                self.test_project1.end
            ),
            'entity_type': 'Project',
            'fps': 25,
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        self.test_project1.id,
                'length': 0
            },
            'generic_text': '',
            'id': self.test_project1.id,
            'image_format': {
                'id': self.test_image_format1.id,
                'name': self.test_image_format1.name,
                'entity_type': self.test_image_format1.entity_type,
                '$ref': '/api/image_formats/%s' % self.test_image_format1.id
            },
            'name': 'Test Project 1',
            'notes': {
                '$ref': '/api/entities/%s/notes' % self.test_project1.id,
                'length': 0
            },
            'references': {
                '$ref': '/api/projects/%s/references' % self.test_project1.id,
                'length': 5
            },
            'repositories': {
                '$ref':
                    '/api/projects/%s/repositories' % self.test_project1.id,
                'length': 2,
            },
            'stalker_version': stalker.__version__,
            'start': EntityViewBase.milliseconds_since_epoch(
                self.test_project1.start
            ),
            'status': {
                'id': self.test_project1.status.id,
                'name': self.test_project1.status.name,
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.test_project1.status.id
            },
            'status_list': {
                'id': self.test_project_status_list.id,
                'name': self.test_project_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' %
                        self.test_project_status_list.id
            },
            'structure': None,
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_project1.id,
                'length': 0
            },
            'tasks': {
                '$ref': '/api/projects/%s/tasks' % self.test_project1.id,
                'length': 4
            },
            'tickets': {
                '$ref': '/api/projects/%s/tickets' % self.test_project1.id,
                'length': 3,
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'users': {
                '$ref': '/api/projects/%s/users' % self.test_project1.id,
                'length': 3
            }
        }

        # import pprint
        # pprint.pprint(response.json_body)
        # print('------')
        # pprint.pprint(expected_result)

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_entities_method_is_working_properly(self):
        """testing if the get_entities() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()

        params = DummyMultiDict()

        from stalker_pyramid.views.project import ProjectViews
        project_view = ProjectViews(request)

        response = project_view.get_entities()

        expected_result = [
            {
                'id': p.id,
                'entity_type': 'Project',
                'name': p.name,
                '$ref': '/api/projects/%s' % p.id,
            } for p in [self.test_project1, self.test_project2]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_update_entity_method_is_working_properly_with_patch(self):
        """testing if the update_entity() method is working properly with the
        request method is set to PATCH
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.method = 'PATCH'

        params = DummyMultiDict()
        params['name'] = 'New Project Name'
        params['code'] = 'NPN'
        params['fps'] = 24
        params['image_format_id'] = self.test_image_format2.id

        request.params = params

        self.patch_logged_in_user(request)
        project_view = project.ProjectViews(request)
        response = project_view.update_entity()

        # get the project from database
        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(test_project1_db.name, 'New Project Name')
        self.assertEqual(test_project1_db.code, 'NPN')
        self.assertEqual(test_project1_db.fps, 24)
        self.assertEqual(
            test_project1_db.image_format,
            self.test_image_format2
        )

    def test_update_entity_method_is_working_properly_with_post(self):
        """testing if the update_entity() method is working properly with the
        request method is set to POST
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.method = 'POST'

        params = DummyMultiDict()
        params['name'] = 'New Project Name'
        params['code'] = 'NPN'
        params['fps'] = 24
        params['image_format_id'] = self.test_image_format2.id

        request.params = params

        self.patch_logged_in_user(request)
        project_view = project.ProjectViews(request)
        response = project_view.update_entity()

        # get the project from database
        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(test_project1_db.name, 'New Project Name')
        self.assertEqual(test_project1_db.code, 'NPN')
        self.assertEqual(test_project1_db.fps, 24)
        self.assertEqual(
            test_project1_db.image_format,
            self.test_image_format2
        )

    def test_create_entity_method_is_working_properly(self):
        """testing if the create_entity() method is working properly
        """
        import datetime
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        from stalker_pyramid.views import EntityViewBase
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Project 1'
        request.params['code'] = 'NP1'
        request.params['client_id'] = [self.test_client1.id]
        request.params['repository_id'] = [self.test_repo1.id]
        request.params['fps'] = 33
        request.params['description'] = 'Test Description'
        request.params['user_id'] = [self.test_user1.id, self.test_user2.id]
        request.params['image_format_id'] = self.test_image_format2.id
        request.params['start'] = EntityViewBase.milliseconds_since_epoch(
            datetime.datetime(2016, 12, 23, 1, 30)
        )
        request.params['end'] = EntityViewBase.milliseconds_since_epoch(
            datetime.datetime(2016, 12, 23, 1, 35)
        )

        self.patch_logged_in_user(request)
        project_view = project.ProjectViews(request)
        response = project_view.create_entity()

        # get the project instance from DB
        from stalker import Project
        new_project1_db = \
            Project.query.filter(Project.name=='New Project 1').first()

        import stalker
        expected_result = {
            'clients': {
                '$ref': '/api/projects/%s/clients' % new_project1_db.id,
                'length': 1
            },
            'code': 'NP1',
            'created_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'dailies': {
                '$ref': '/api/projects/%s/dailies' % new_project1_db.id,
                'length': 0
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    new_project1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    new_project1_db.date_updated
                ),
            'description': 'Test Description',
            'end':
                EntityViewBase.milliseconds_since_epoch(new_project1_db.end),
            'entity_type': 'Project',
            'fps': 33,
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        new_project1_db.id,
                'length': 0
            },
            'generic_text': '',
            'id': new_project1_db.id,
            'image_format': {
                'id': self.test_image_format2.id,
                'name': self.test_image_format2.name,
                'entity_type': self.test_image_format2.entity_type,
                '$ref': '/api/image_formats/%s' % self.test_image_format2.id
            },
            'name': 'New Project 1',
            'notes': {
                '$ref': '/api/entities/%s/notes' % new_project1_db.id,
                'length': 0
            },
            'references': {
                '$ref': '/api/projects/%s/references' % new_project1_db.id,
                'length': 0
            },
            'repositories': {
                '$ref':
                    '/api/projects/%s/repositories' % new_project1_db.id,
                'length': 1,
            },
            'stalker_version': stalker.__version__,
            'start':
                EntityViewBase.milliseconds_since_epoch(new_project1_db.start),
            'status': {
                'id': new_project1_db.status.id,
                'name': new_project1_db.status.name,
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % new_project1_db.status.id
            },
            'status_list': {
                'id': self.test_project_status_list.id,
                'name': self.test_project_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' %
                        self.test_project_status_list.id
            },
            'structure': None,
            'tags': {
                '$ref': '/api/entities/%s/tags' % new_project1_db.id,
                'length': 0
            },
            'tasks': {
                '$ref': '/api/projects/%s/tasks' % new_project1_db.id,
                'length': 0
            },
            'tickets': {
                '$ref': '/api/projects/%s/tickets' % new_project1_db.id,
                'length': 0,
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'users': {
                '$ref': '/api/projects/%s/users' % new_project1_db.id,
                'length': 2
            }
        }

        import pprint
        pprint.pprint(response.json_body)
        print('--------')
        pprint.pprint(expected_result)

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_delete_entity_method_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        project_view.delete_entity()

        from stalker import Project
        self.assertIsNone(
            Project.query.filter_by(id=self.test_project1.id).first()
        )

    def test_get_clients_method_is_working_properly(self):
        """testing if the get_clients() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        response = project_view.get_clients()

        expected_result = [
            {
                'id': c.id,
                'entity_type': 'Client',
                'name': c.name,
                '$ref': '/api/clients/%s' % c.id,
            } for c in [self.test_client1, self.test_client2]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_update_clients_method_is_working_properly_with_patch(self):
        """testing if the update_clients() method is working properly with the
        request method is set to PATCH
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        # now do it!
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.method = 'PATCH'

        request.params = DummyMultiDict()
        request.params['client_id'] = \
            [self.test_client3.id, self.test_client4.id]

        project_view = project.ProjectViews(request)
        response = project_view.update_clients()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client1, self.test_client2,
             self.test_client3, self.test_client4]
        )

    def test_update_clients_method_is_working_properly_with_post(self):
        """testing if the update_clients() method is working properly with the
        request method is set to POST
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        # now do it!
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.method = 'POST'

        request.params = DummyMultiDict()
        request.params['client_id'] = \
            [self.test_client3.id, self.test_client4.id]

        project_view = project.ProjectViews(request)
        response = project_view.update_clients()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client3, self.test_client4]
        )

    def test_delete_clients_method_is_working_properly(self):
        """testing if the delete_clients() method is working properly
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        # now do it!
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        request.params = DummyMultiDict()
        request.params['client_id'] = \
            [self.test_client1.id]

        project_view = project.ProjectViews(request)
        response = project_view.delete_clients()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client2]
        )

    def test_delete_clients_method_is_working_properly_with_non_members(self):
        """testing if the delete_clients() method is working properly with
        clients that are not present in the current Project.clients list
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        # now do it!
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        request.params = DummyMultiDict()
        request.params['client_id'] = \
            [self.test_client1.id, self.test_client3.id]

        project_view = project.ProjectViews(request)
        response = project_view.delete_clients()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client2]
        )

    def test_get_repositories_method_is_working_properly(self):
        """testing if the get_repositories() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        project_view = project.ProjectViews(request)

        response = project_view.get_repositories()

        expected_result = [
            {
                'id': r.id,
                'name': r.name,
                'entity_type': 'Repository',
                '$ref': '/api/repositories/%s' % r.id
            } for r in [self.test_repo1, self.test_repo2]
        ]

        self.assertEqual(response.json_body, expected_result)

    def test_update_repositories_method_is_working_properly_with_patch(self):
        """testing if the update_repositories() method is working properly with
        the request method is set to PATCH
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['repo_id'] = [self.test_repo2.id, self.test_repo3.id]
        request.method = 'PATCH'

        project_view = project.ProjectViews(request)
        response = project_view.update_repositories()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo1, self.test_repo2, self.test_repo3]
        )

    def test_update_repositories_method_is_working_properly_with_post(self):
        """testing if the update_repositories() method is working properly with
        the request method is set to POST
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['repo_id'] = [self.test_repo2.id, self.test_repo3.id]
        request.method = 'POST'

        project_view = project.ProjectViews(request)
        response = project_view.update_repositories()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo2, self.test_repo3]
        )

    def test_delete_repositories_method_is_working_properly(self):
        """testing if the delete_repositories() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['repo_id'] = [self.test_repo2.id]

        project_view = project.ProjectViews(request)
        response = project_view.delete_repositories()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo1]
        )

    def test_delete_repositories_method_is_working_properly_with_non_related_data(self):
        """testing if the delete_repositories() method is working properly with
        non related data
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['repo_id'] = [self.test_repo2.id, self.test_repo3.id]

        project_view = project.ProjectViews(request)
        response = project_view.delete_repositories()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo1]
        )

    def test_get_tasks_method_is_working_properly(self):
        """testing if the get_tasks() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        response = project_view.get_tasks()

        from stalker_pyramid import entity_type_to_url
        expected_result = [
            {
                'id': t.id,
                'name': t.name,
                'entity_type': t.entity_type,
                '$ref': '%s/%s' % (entity_type_to_url[t.entity_type], t.id)
            } for t in [self.test_task1, self.test_task2,
                        self.test_asset1, self.test_shot1]
        ]

    def test_get_tickets_method_is_working_properly(self):
        """testing if the get_tickets() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        project_view = project.ProjectViews(request)
        response = project_view.get_tickets()

        expected_result = [
            {
                'id': t.id,
                'name': t.name,
                'entity_type': 'Ticket',
                '$ref': '/api/tickets/%s' % t.id
            } for t in [self.test_ticket1, self.test_ticket2,
                        self.test_ticket3]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_users_method_is_working_properly(self):
        """testing if the get_users() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        response = project_view.get_users()

        expected_result = [
            {
                'id': u.id,
                'name': u.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % u.id
            } for u in [self.test_user1, self.test_user2, self.test_user3]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_update_users_method_is_working_properly_with_patch(self):
        """testing if the update_users() method is working properly with
        the request method is set to PATCH
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user4.id]
        request.method = 'PATCH'

        project_view = project.ProjectViews(request)
        response = project_view.update_users()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user1, self.test_user2, self.test_user3,
                           self.test_user4]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_update_users_method_is_working_properly_with_post(self):
        """testing if the update_users() method is working properly with
        the request method is set to POST
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user4.id]
        request.method = 'POST'

        project_view = project.ProjectViews(request)
        response = project_view.update_users()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user4]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_delete_users_method_is_working_properly(self):
        """testing if the delete_users() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user3.id]

        project_view = project.ProjectViews(request)
        response = project_view.delete_users()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user1, self.test_user2]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_delete_users_method_is_working_properly_with_non_related_data(self):
        """testing if the delete_users() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id
        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user3.id, self.test_user4.id]

        project_view = project.ProjectViews(request)
        response = project_view.delete_users()

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user1, self.test_user2]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_get_dailies_method_is_working_properly(self):
        """testing if get_dailies() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        response = project_view.get_dailies()

        expected_result = [
            {
                'id': d.id,
                'name': d.name,
                'entity_type': 'Daily',
                '$ref': '/api/dailies/%s' % d.id
            } for d in [self.test_daily1, self.test_daily2, self.test_daily3]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_references_method_is_working_properly(self):
        """testing if get_references() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        response = project_view.get_references()

        expected_result = [
            {
                'id': l.id,
                'name': l.name,
                'entity_type': 'Link',
                '$ref': '/api/links/%s' % l.id
            } for l in [self.test_link1, self.test_link2, self.test_link3,
                        self.test_link4, self.test_link5]
        ]

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(expected_result)
        )

    def test_get_budgets_method_is_working_properly(self):
        """testing if get_budgets() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_project1.id

        project_view = project.ProjectViews(request)
        response = project_view.get_budgets()

        expected_result = [
            {
                'id': b.id,
                'name': b.name,
                'entity_type': 'Budget',
                '$ref': '/api/budgets/%s' % b.id
            } for b in [self.test_budget1, self.test_budget2]
        ]

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(expected_result)
        )


class ProjectViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for ProjectViews class
    """

    def setUp(self):
        """create test data
        """
        super(ProjectViewsFunctionalTestCase, self).setUp()

        from stalker import User
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        from stalker import db
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

        self.test_user4 = User(
            name='Test User 4',
            login='tuser4',
            email='tuser4@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user4)

        self.test_user5 = User(
            name='Test User 5',
            login='tuser5',
            email='tuser5@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user5)

        from stalker import Repository
        self.test_repo1 = Repository(
            name='Test Repository 1',
            windows_path='T:/some_path',
            linux_path='/mnt/T/some_path',
            osx_path='/volumes/T/some_path'
        )
        db.DBSession.add(self.test_repo1)
        db.DBSession.commit()

        self.test_repo2 = Repository(
            name='Test Repository 2',
            windows_path='T:/some_path',
            linux_path='/mnt/T/some_path',
            osx_path='/volumes/T/some_path'
        )
        db.DBSession.add(self.test_repo2)
        db.DBSession.commit()

        self.test_repo3 = Repository(
            name='Test Repository 3',
            windows_path='T:/some_path',
            linux_path='/mnt/T/some_path',
            osx_path='/volumes/T/some_path'
        )
        db.DBSession.add(self.test_repo3)
        db.DBSession.commit()

        self.test_repo4 = Repository(
            name='Test Repository 4',
            windows_path='T:/some_path',
            linux_path='/mnt/T/some_path',
            osx_path='/volumes/T/some_path'
        )
        db.DBSession.add(self.test_repo4)
        db.DBSession.commit()

        from stalker import Status
        self.status_new = Status.query.filter(Status.code == 'NEW').first()
        self.status_wip = Status.query.filter(Status.code == 'WIP').first()
        self.status_cmpl = Status.query.filter(Status.code == 'CMPL').first()

        from stalker import StatusList
        self.test_project_status_list = StatusList(
            name='Project Statuses',
            statuses=[self.status_new, self.status_wip, self.status_cmpl],
            target_entity_type='Project'
        )
        db.DBSession.add(self.test_project_status_list)
        db.DBSession.commit()

        from stalker import ImageFormat
        self.test_image_format1 = ImageFormat(
            name='VR',
            width=4096,
            height=2048
        )
        db.DBSession.add(self.test_image_format1)

        self.test_image_format2 = ImageFormat(
            name='VR - Half',
            width=2048,
            height=1024
        )
        db.DBSession.add(self.test_image_format2)

        from stalker import Client
        self.test_client1 = Client(
            name='Test Client 1'
        )
        db.DBSession.add(self.test_client1)

        self.test_client2 = Client(
            name='Test Client 2'
        )
        db.DBSession.add(self.test_client2)

        self.test_client3 = Client(
            name='Test Client 3'
        )
        db.DBSession.add(self.test_client3)

        self.test_client4 = Client(
            name='Test Client 4'
        )
        db.DBSession.add(self.test_client4)

        # project1
        from stalker import Project
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            repositories=[self.test_repo1, self.test_repo2],
            created_by=self.admin,
            image_format=self.test_image_format1,
            clients=[self.test_client1, self.test_client2],
            users=[self.test_user1, self.test_user2, self.test_user3]
        )
        db.DBSession.add(self.test_project1)
        db.DBSession.commit()

        # project 2
        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            repositories=[self.test_repo1],
            created_by=self.admin
        )
        db.DBSession.add(self.test_project2)
        db.DBSession.commit()

        # create some tasks
        from stalker import Task
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task2)
        db.DBSession.commit()

        # some assets
        from stalker import Type
        self.test_asset_type = Type(
            name='Asset Type 1',
            code='AT1',
            target_entity_type='Asset'
        )
        db.DBSession.add(self.test_asset_type)
        db.DBSession.commit()

        from stalker import Asset
        self.test_asset1 = Asset(
            name='Test Asset 1',
            code='TA1',
            type=self.test_asset_type,
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_asset1)

        # and a shot
        from stalker import Shot
        self.test_shot1 = Shot(
            name='Test Shot',
            code='ts',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_shot1)
        db.DBSession.commit()

        # and some test tasks for the other project, so we'll be sure that it
        # is returning the tasks of the correct project
        self.test_task3 = Task(
            name='Test Task 3',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task3)
        db.DBSession.commit()

        from stalker import Link
        self.test_link1 = Link()
        self.test_link2 = Link()
        self.test_link3 = Link()
        self.test_project1.references = \
            [self.test_link1, self.test_link2, self.test_link3]

        self.test_link4 = Link()
        self.test_link5 = Link()
        self.test_task1.references = [self.test_link4, self.test_link5]
        self.test_task2.references = [self.test_link5]

        self.test_link6 = Link()
        self.test_link7 = Link()
        self.test_project2.references = [self.test_link6]
        self.test_task3.references = [self.test_link7]

        db.DBSession.add_all([
            self.test_link1, self.test_link2, self.test_link3, self.test_link4,
            self.test_link5, self.test_link6, self.test_link7
        ])
        db.DBSession.commit()

        from stalker import Daily
        self.test_daily1 = Daily(name='Daily1', project=self.test_project1)
        self.test_daily2 = Daily(name='Daily2', project=self.test_project1)
        self.test_daily3 = Daily(name='Daily3', project=self.test_project1)
        db.DBSession.add_all(
            [self.test_daily1, self.test_daily2, self.test_daily3]
        )

        self.test_daily4 = Daily(name='Daily4', project=self.test_project2)
        self.test_daily5 = Daily(name='Daily5', project=self.test_project2)
        self.test_daily6 = Daily(name='Daily6', project=self.test_project2)
        db.DBSession.add_all(
            [self.test_daily4, self.test_daily5, self.test_daily6]
        )
        db.DBSession.commit()

        from stalker import Ticket

        # for test_project1
        self.test_ticket1 = \
            Ticket(project=self.test_project1, summary='this is ticket 1')
        db.DBSession.add(self.test_ticket1)
        self.test_ticket2 = \
            Ticket(project=self.test_project1, summary='this is ticket 2')
        db.DBSession.add(self.test_ticket2)
        self.test_ticket3 = \
            Ticket(project=self.test_project1, summary='this is ticket 3')
        db.DBSession.add(self.test_ticket3)

        # for test_project2
        self.test_ticket4 = \
            Ticket(project=self.test_project2, summary='this is ticket 4')
        db.DBSession.add(self.test_ticket4)
        self.test_ticket5 = \
            Ticket(project=self.test_project2, summary='this is ticket 5')
        db.DBSession.add(self.test_ticket5)
        self.test_ticket6 = \
            Ticket(project=self.test_project2, summary='this is ticket 6')
        db.DBSession.add(self.test_ticket6)

        # create a couple of Budgets
        self.test_budget_status_list = StatusList(
            name='Budget Statuses',
            statuses=[self.status_new, self.status_cmpl],
            target_entity_type='Budget'
        )
        db.DBSession.add(self.test_budget_status_list)
        db.DBSession.commit()

        from stalker import Budget
        self.test_budget1 = Budget(
            name='Test Budget 1',
            project=self.test_project1
        )
        db.DBSession.add(self.test_budget1)

        self.test_budget2 = Budget(
            name='Test Budget 2',
            project=self.test_project1
        )
        db.DBSession.add(self.test_budget2)

        self.test_budget3 = Budget(
            name='Test Budget 3',
            project=self.test_project2
        )
        db.DBSession.add(self.test_budget3)
        db.DBSession.commit()

    def test_get_entity_view_is_working_properly(self):
        """testing if the GET: /api/projects/{id} view is working properly
        """
        response = self.test_app.get(
            '/api/projects/%s' % self.test_project1.id,
            status=200
        )

        import stalker
        from stalker_pyramid.views import EntityViewBase
        expected_result = {
            'clients': {
                '$ref': '/api/projects/%s/clients' % self.test_project1.id,
                'length': 2
            },
            'code': self.test_project1.code,
            'created_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'dailies': {
                '$ref': '/api/projects/%s/dailies' % self.test_project1.id,
                'length': 3
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_project1.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    self.test_project1.date_updated
                ),
            'description': '',
            'end': EntityViewBase.milliseconds_since_epoch(
                self.test_project1.end
            ),
            'entity_type': 'Project',
            'fps': 25,
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        self.test_project1.id,
                'length': 0
            },
            'generic_text': '',
            'id': self.test_project1.id,
            'image_format': {
                'id': self.test_image_format1.id,
                'name': self.test_image_format1.name,
                'entity_type': self.test_image_format1.entity_type,
                '$ref': '/api/image_formats/%s' % self.test_image_format1.id
            },
            'name': 'Test Project 1',
            'notes': {
                '$ref': '/api/entities/%s/notes' % self.test_project1.id,
                'length': 0
            },
            'references': {
                '$ref': '/api/projects/%s/references' % self.test_project1.id,
                'length': 5
            },
            'repositories': {
                '$ref':
                    '/api/projects/%s/repositories' % self.test_project1.id,
                'length': 2,
            },
            'stalker_version': stalker.__version__,
            'start': EntityViewBase.milliseconds_since_epoch(
                self.test_project1.start
            ),
            'status': {
                'id': self.test_project1.status.id,
                'name': self.test_project1.status.name,
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.test_project1.status.id
            },
            'status_list': {
                'id': self.test_project_status_list.id,
                'name': self.test_project_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' %
                        self.test_project_status_list.id
            },
            'structure': None,
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_project1.id,
                'length': 0
            },
            'tasks': {
                '$ref': '/api/projects/%s/tasks' % self.test_project1.id,
                'length': 4
            },
            'tickets': {
                '$ref': '/api/projects/%s/tickets' % self.test_project1.id,
                'length': 3,
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'users': {
                '$ref': '/api/projects/%s/users' % self.test_project1.id,
                'length': 3
            }
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_entities_view_is_working_properly(self):
        """testing if the GET:/api/projects view is working properly
        """
        response = self.test_app.get(
            '/api/projects',
            status=200
        )

        expected_result = [
            {
                'id': p.id,
                'entity_type': 'Project',
                'name': p.name,
                '$ref': '/api/projects/%s' % p.id,
            } for p in [self.test_project1, self.test_project2]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_update_entity_view_is_working_properly_with_patch(self):
        """testing if the PATCH: /api/projects/{id} view is working properly
        """
        # login ass admin
        self.admin_login()

        response = self.test_app.patch(
            '/api/projects/%s' % self.test_project1.id,
            params={
                'name': 'New Project Name',
                'code': 'NPN',
                'fps': 24,
                'image_format_id': self.test_image_format2.id,
            }
        )

        # get the project from database
        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(test_project1_db.name, 'New Project Name')
        self.assertEqual(test_project1_db.code, 'NPN')
        self.assertEqual(test_project1_db.fps, 24)
        self.assertEqual(
            test_project1_db.image_format,
            self.test_image_format2
        )

    def test_update_entity_view_is_working_properly_with_post(self):
        """testing if the POST:/api/projects/{id} view is working properly
        """
        # login ass admin
        self.admin_login()

        response = self.test_app.post(
            '/api/projects/%s' % self.test_project1.id,
            params={
                'name': 'New Project Name',
                'code': 'NPN',
                'fps': 24,
                'image_format_id': self.test_image_format2.id,
            }
        )

        # get the project from database
        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(test_project1_db.name, 'New Project Name')
        self.assertEqual(test_project1_db.code, 'NPN')
        self.assertEqual(test_project1_db.fps, 24)
        self.assertEqual(
            test_project1_db.image_format,
            self.test_image_format2
        )

    def test_create_entity_view_is_working_properly(self):
        """testing if the PUT:/api/projects view is working properly
        """
        import datetime
        from stalker_pyramid.views import EntityViewBase
        self.admin_login()
        response = self.test_app.put(
            '/api/projects',
            params={
                'name': 'New Project 1',
                'code': 'NP1',
                'client_id': [self.test_client1.id],
                'repository_id': [self.test_repo1.id],
                'fps': 33,
                'description': 'Test Description',
                'user_id': [self.test_user1.id, self.test_user2.id],
                'image_format_id': self.test_image_format2.id,
                'start': EntityViewBase.milliseconds_since_epoch(
                    datetime.datetime(2016, 12, 23, 1, 30)
                ),
                'end': EntityViewBase.milliseconds_since_epoch(
                    datetime.datetime(2016, 12, 23, 1, 35)
                )
            },
            status=201
        )

        # get the project instance from DB
        from stalker import Project
        new_project1_db = \
            Project.query.filter(Project.name=='New Project 1').first()

        import stalker
        expected_result = {
            'clients': {
                '$ref': '/api/projects/%s/clients' % new_project1_db.id,
                'length': 1
            },
            'code': 'NP1',
            'created_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'dailies': {
                '$ref': '/api/projects/%s/dailies' % new_project1_db.id,
                'length': 0,
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    new_project1_db.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    new_project1_db.date_updated
                ),
            'description': 'Test Description',
            'end':
                EntityViewBase.milliseconds_since_epoch(new_project1_db.end),
            'entity_type': 'Project',
            'fps': 33,
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        new_project1_db.id,
                'length': 0
            },
            'generic_text': '',
            'id': new_project1_db.id,
            'image_format': {
                'id': self.test_image_format2.id,
                'name': self.test_image_format2.name,
                'entity_type': self.test_image_format2.entity_type,
                '$ref': '/api/image_formats/%s' % self.test_image_format2.id
            },
            'name': 'New Project 1',
            'notes': {
                '$ref': '/api/entities/%s/notes' % new_project1_db.id,
                'length': 0
            },
            'references': {
                '$ref': '/api/projects/%s/references' % new_project1_db.id,
                'length': 0
            },
            'repositories': {
                '$ref':
                    '/api/projects/%s/repositories' % new_project1_db.id,
                'length': 1,
            },
            'stalker_version': stalker.__version__,
            'start':
                EntityViewBase.milliseconds_since_epoch(new_project1_db.start),
            'status': {
                'id': new_project1_db.status.id,
                'name': new_project1_db.status.name,
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % new_project1_db.status.id
            },
            'status_list': {
                'id': self.test_project_status_list.id,
                'name': self.test_project_status_list.name,
                'entity_type': 'StatusList',
                '$ref': '/api/status_lists/%s' %
                        self.test_project_status_list.id
            },
            'structure': None,
            'tags': {
                '$ref': '/api/entities/%s/tags' % new_project1_db.id,
                'length': 0
            },
            'tasks': {
                '$ref': '/api/projects/%s/tasks' % new_project1_db.id,
                'length': 0
            },
            'thumbnail': None,
            'tickets': {
                '$ref': '/api/projects/%s/tickets' % new_project1_db.id,
                'length': 0
            },
            'type': None,
            'updated_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'users': {
                '$ref': '/api/projects/%s/users' % new_project1_db.id,
                'length': 2
            }
        }

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_delete_entity_view_is_working_properly(self):
        """testing if the DELETE:/api/projects/{id} view is working properly
        """
        self.admin_login()
        self.test_app.delete(
            '/api/projects/%s' % self.test_project1.id,
            status=200
        )

        from stalker import Project
        self.assertIsNone(
            Project.query.filter_by(id=self.test_project1.id).first()
        )

    def test_get_clients_view_is_working_properly(self):
        """testing if the GET:/api/projects/{id}/clients view is working
        properly
        """
        response = self.test_app.get(
            '/api/projects/%s/clients' % self.test_project1.id,
            status=200
        )

        expected_result = [
            {
                'id': c.id,
                'entity_type': 'Client',
                'name': c.name,
                '$ref': '/api/clients/%s' % c.id,
            } for c in [self.test_client1, self.test_client2]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_update_clients_view_is_working_properly_with_patch(self):
        """testing if the PATCH:/api/projects/{id}/clients view is working
        properly
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        response = self.test_app.patch(
            '/api/projects/%s/clients' % self.test_project1.id,
            params={
                'client_id': [self.test_client3.id, self.test_client4.id],
            },
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client1, self.test_client2,
             self.test_client3, self.test_client4]
        )

    def test_update_clients_view_is_working_properly_with_post(self):
        """testing if the POST:/api/projects/{id}/clients view is working
        properly
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        # now do it!
        response = self.test_app.post(
            '/api/projects/%s/clients' % self.test_project1.id,
            params={
                'client_id': [self.test_client3.id, self.test_client4.id]
            },
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client3, self.test_client4]
        )

    def test_delete_clients_view_is_working_properly(self):
        """testing if the delete_clients() view is working properly
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        # now do it!
        response = self.test_app.delete(
            '/api/projects/%s/clients?client_id=%s' % (
                self.test_project1.id, self.test_client1.id
            ),
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client2]
        )

    def test_delete_clients_view_is_working_properly_with_non_members(self):
        """testing if the DELETE:/api/projects/{id}/clients view is working
        properly with clients that are not present in the current
        Project.clients list
        """
        # before doing anything make sure that the client is as expected
        self.assertEqual(
            self.test_project1.clients,
            [self.test_client1, self.test_client2]
        )

        # now do it!
        response = self.test_app.delete(
            '/api/projects/%s/clients?client_id=%s&clint_id=%s' %
            (
                self.test_project1.id,
                self.test_client1.id,
                self.test_client3.id
            ),
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.clients,
            [self.test_client2]
        )

    def test_get_repositories_view_is_working_properly(self):
        """testing if the GET:/api/projects/{id}/repositories view is working
        properly
        """
        response = self.test_app.get(
            '/api/projects/%s/repositories' % self.test_project1.id,
            status=200
        )

        expected_result = [
            {
                'id': r.id,
                'name': r.name,
                'entity_type': 'Repository',
                '$ref': '/api/repositories/%s' % r.id
            } for r in [self.test_repo1, self.test_repo2]
        ]

        self.assertEqual(response.json_body, expected_result)

    def test_update_repositories_view_is_working_properly_with_patch(self):
        """testing if the PATCH:/api/projects/{id}/repositories view is working
        properly
        """
        response = self.test_app.patch(
            '/api/projects/%s/repositories' % self.test_project1.id,
            params={
                'repo_id': [self.test_repo2.id, self.test_repo3.id],
            },
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo1, self.test_repo2, self.test_repo3]
        )

    def test_update_repositories_view_is_working_properly_with_post(self):
        """testing if the POST:/api/projects/{id}/repositories view is working
        properly
        """
        response = self.test_app.post(
            '/api/projects/%s/repositories' % self.test_project1.id,
            params={
                'repo_id': [self.test_repo2.id, self.test_repo3.id]
            },
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo2, self.test_repo3]
        )

    def test_delete_repositories_view_is_working_properly(self):
        """testing if the DELETE:/api/projects/{id}/repositories view is
        working
        """
        response = self.test_app.delete(
            '/api/projects/%s/repositories?repo_id=%s' % (
                self.test_project1.id, self.test_repo2.id
            ),
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo1]
        )

    def test_delete_repositories_view_is_working_properly_with_non_related_data(self):
        """testing if the DELETE:/api/projects/{id}/repositories view is
        working properly with non related data
        """
        response = self.test_app.delete(
            '/api/projects/%s/repositories?repo_id=%s&repo_id=%s' % (
                self.test_project1.id, self.test_repo2.id, self.test_repo3.id
            ),
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        self.assertEqual(
            test_project1_db.repositories,
            [self.test_repo1]
        )

    def test_get_tasks_view_is_working_properly(self):
        """testing if the GET:/api/projects/{id}/tasks view is working properly
        """
        response = self.test_app.get(
            '/api/projects/%s/tasks' % self.test_project1.id,
            status=200
        )

        from stalker_pyramid import entity_type_to_url
        expected_result = [
            {
                'id': t.id,
                'name': t.name,
                'entity_type': t.entity_type,
                '$ref': '%s/%s' % (entity_type_to_url[t.entity_type], t.id)
            } for t in [self.test_task1, self.test_task2,
                        self.test_asset1, self.test_shot1]
        ]

    def test_get_tickets_view_is_working_properly(self):
        """testing if the GET:/api/projects/{id}/tickets view is working
        properly
        """
        response = self.test_app.get(
            '/api/projects/%s/tickets' % self.test_project1.id,
            status=200
        )
        expected_result = [
            {
                'id': t.id,
                'name': t.name,
                'entity_type': 'Ticket',
                '$ref': '/api/tickets/%s' % t.id
            } for t in [self.test_ticket1, self.test_ticket2,
                        self.test_ticket3]
        ]

        import pprint
        pprint.pprint(response.json_body)
        print('--------')
        pprint.pprint(expected_result)


        self.maxDiff = 0
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_users_view_is_working_properly(self):
        """testing if the GET:/api/projects/{id}/users view is working properly
        """
        response = self.test_app.get(
            '/api/projects/%s/users' % self.test_project1.id,
            status=200
        )

        expected_result = [
            {
                'id': u.id,
                'name': u.name,
                'entity_type': 'User',
                '$ref': '/api/users/%s' % u.id
            } for u in [self.test_user1, self.test_user2, self.test_user3]
        ]

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_update_users_view_is_working_properly_with_patch(self):
        """testing if the PATCH:/api/projects/{id}/users view is working
        properly
        """
        response = self.test_app.patch(
            '/api/projects/%s/users' % self.test_project1.id,
            params={
                'user_id': [self.test_user4.id],
            },
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user1, self.test_user2, self.test_user3,
                           self.test_user4]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_update_users_view_is_working_properly_with_post(self):
        """testing if the POST:/api/projects/{id}/users view is working
        properly
        """
        response = self.test_app.post(
            '/api/projects/%s/users' % self.test_project1.id,
            params={
                'user_id': [self.test_user4.id]
            },
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user4]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_delete_users_view_is_working_properly(self):
        """testing if the DELETE:/api/projects/{id}/users view is working
        properly
        """
        response = self.test_app.delete(
            '/api/projects/%s/users?user_id=%s' % (
                self.test_project1.id, self.test_user3.id
            ),
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user1, self.test_user2]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_delete_users_view_is_working_properly_with_non_related_data(self):
        """testing if the DELETE:/api/projects/%s/users view is working
        properly
        """
        response = self.test_app.delete(
            '/api/projects/%s/users?user_id=%s&user_id=%s' % (
                self.test_project1.id, self.test_user3.id, self.test_user4.id
            ),
            status=200
        )

        from stalker import Project
        test_project1_db = Project.query.get(self.test_project1.id)

        expected_result = [self.test_user1, self.test_user2]

        self.assertEqual(
            test_project1_db.users,
            expected_result
        )

    def test_get_dailies_method_is_working_properly(self):
        """testing if GET:/api/projects/{id}/dailies method is working properly
        """
        response = self.test_app.get(
            '/api/projects/%s/dailies' % self.test_project1.id,
            status=200
        )

        expected_result = [
            {
                'id': d.id,
                'name': d.name,
                'entity_type': 'Daily',
                '$ref': '/api/dailies/%s' % d.id
            } for d in [self.test_daily1, self.test_daily2, self.test_daily3]
        ]

        self.assertEqual(
            response.json_body,
            expected_result
        )

    def test_get_references_method_is_working_properly(self):
        """testing if GET:/api/projects/{id}/references method is working
        properly
        """
        response = self.test_app.get(
            '/api/projects/%s/references' % self.test_project1.id,
            status=200
        )

        expected_result = [
            {
                'id': l.id,
                'name': l.name,
                'entity_type': 'Link',
                '$ref': '/api/links/%s' % l.id
            } for l in [self.test_link1, self.test_link2, self.test_link3,
                        self.test_link4, self.test_link5]
        ]

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(expected_result)
        )

    def test_get_budgets_view_is_working_properly(self):
        """testing if GET:/api/projects/{id}/budgets view is working properly
        """
        response = self.test_app.get(
            '/api/projects/%s/budgets' % self.test_project1.id,
            status=200
        )

        expected_result = [
            {
                'id': b.id,
                'name': b.name,
                'entity_type': 'Budget',
                '$ref': '/api/budgets/%s' % b.id
            } for b in [self.test_budget1, self.test_budget2]
        ]

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(expected_result)
        )
