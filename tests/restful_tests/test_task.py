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
from stalker_pyramid.views import task


class TaskViewUnitTestCase(UnitTestBase):
    """tests for the TaskViews class
    """

    def setUp(self):
        """create the test data
        """
        super(TaskViewUnitTestCase, self).setUp()
        from stalker import db

        from stalker import User
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@test.com',
            password='secret'
        )
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@test.com',
            password='secret'
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@test.com',
            password='secret'
        )
        db.DBSession.add(self.test_user3)
        db.DBSession.commit()

        from stalker import Status
        self.status_rts = Status.query.filter(Status.code == 'RTS').first()
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

        from stalker import Repository
        self.test_repo1 = Repository(
            name='Test Repository',
            linux_path='/mnt/T/',
            windows_path='T:/',
            osx_path='/Volumes/T'
        )
        db.DBSession.add(self.test_repo1)

        from stalker import Project
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            status_list=self.test_project_status_list,
            repositories=[self.test_repo1]
        )
        db.DBSession.add(self.test_project1)
        db.DBSession.commit()

        from stalker import Task
        self.test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            responsible=[self.test_user3],
            created_by=self.admin,
        )
        db.DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='Test Task 2',
            parent=self.test_task1,
            resources=[self.test_user1, self.test_user2],
            schedule_timing=10,
            schedule_unit='h',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='Test Task 3',
            parent=self.test_task1,
            resources=[self.test_user2],
            schedule_timing=10,
            schedule_unit='h',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_task3)
        db.DBSession.commit()

    def test_get_entity_method_is_working_properly(self):
        """testing if the get_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_task2.id
        task_view = task.TaskViews(request)
        response = task_view.get_entity()

        import stalker
        expected_result = {
            'allocation_strategy': 'minallocated',
            'alternative_resources': {
                '$ref': '/api/tasks/%s/alternative_resources' %
                        self.test_task2.id,
                'length': 0
            },
            'bid_timing': 10,
            'bid_unit': 'h',
            'created_by': {
                'id': 3,
                'name': 'admin',
                'entity_type': 'User',
                '$ref': '/api/users/3'
            },
            'children': {
                '$ref': '/api/tasks/%s/children' % self.test_task2.id,
                'length': 0
            },
            'date_created': task_view.milliseconds_since_epoch(
                self.test_task2.date_created
            ),
            'date_updated': task_view.milliseconds_since_epoch(
                self.test_task2.date_created
            ),
            'depends': {
                '$ref': '/api/tasks/%s/depends' % self.test_task2.id,
                'length': 0
            },
            'description': '',
            'end': task_view.milliseconds_since_epoch(self.test_task2.end),
            'entity_type': 'Task',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        self.test_task2.id,
                'length': 0
            },
            'good': None,
            'id': self.test_task2.id,
            'is_milestone': False,
            'name': 'Test Task 2',
            'notes': {
                '$ref': '/api/entities/%s/notes' % self.test_task2.id,
                'length': 0
            },
            'parent': {
                'id': self.test_task1.id,
                'name': 'Test Task 1',
                'entity_type': 'Task',
                '$ref': '/api/tasks/%s' % self.test_task1.id
            },
            'persistent_allocation': True,
            'priority': 500,
            'project': {
                'id': self.test_project1.id,
                'name': 'Test Project 1',
                'entity_type': 'Project',
                '$ref': '/api/projects/%s' % self.test_project1.id
            },
            'resources': {
                '$ref': '/api/tasks/%s/resources' % self.test_task2.id,
                'length': 2
            },
            'responsible': {
                '$ref': '/api/tasks/%s/responsible' % self.test_task2.id,
                'length': 1
            },
            'schedule_constraint': 0,
            'schedule_model': 'effort',
            'schedule_timing': 10,
            'schedule_unit': 'h',
            'stalker_version': stalker.__version__,
            'start': task_view.milliseconds_since_epoch(self.test_task2.start),
            'status': {
                'id': self.status_rts.id,
                'name': 'Ready To Start',
                'entity_type': 'Status',
                '$ref': '/api/statuses/%s' % self.status_rts.id
            },
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_task2.id,
                'length': 0
            },
            'thumbnail': None,
            'type': None,
            'updated_by': {
                'id': 3,
                'name': 'admin',
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
        """testing if the get_entities() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_create_entity_method_is_working_properly(self):
        """testing if the create_entity() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_update_entity_method_is_working_properly(self):
        """testing if the update_entity() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_delete_entity_method_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        self.fail('test is not implemented yet')

    # === COLLECTIONS ===
    def test_get_children_method_is_working_properly(self):
        """testing if the get_children() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_computed_resources_method_is_working_properly(self):
        """testing if the get_computed_resources() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_depends_method_is_working_properly(self):
        """testing if the get_depends() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_dependent_of_method_is_working_properly(self):
        """testing if the get_dependent() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_references_method_is_working_properly(self):
        """testing if the get_references() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_update_references_method_is_working_properly_with_patch(self):
        """testing if the update_references() method is working properly with
        patch
        """
        self.fail('test is not implemented yet')

    def test_update_references_method_is_working_properly_with_post(self):
        """testing if the update_references() method is working properly with
        post
        """
        self.fail('test is not implemented yet')

    def test_delete_references_method_is_working_properly(self):
        """testing if the delete_references() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_resources_method_is_working_properly(self):
        """testing if the get_resources() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_update_resources_method_is_working_properly_with_patch(self):
        """testing if the update_resources() method is working properly with
        patch
        """
        self.fail('test is not implemented yet')

    def test_update_resources_method_is_working_properly_with_post(self):
        """testing if the update_resources() method is working properly with
        post
        """
        self.fail('test is not implemented yet')

    def test_delete_resources_method_is_working_properly(self):
        """testing if the delete_resources() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_reviews_method_is_working_properly(self):
        """testing if the get_reviews() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_time_logs_method_is_working_properly(self):
        """testing if the get_time_logs() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_get_versions_method_is_working_properly(self):
        """testing if the get_versions() method is working properly
        """
        self.fail('test is not implemented yet')

    # ==== METHODS ====
    def test_request_review_method_is_working_properly(self):
        """testing if the request_review() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_request_revision_method_is_working_properly(self):
        """testing if the request_revision() method is working properly
        """
        self.fail('test is not implemented yet')

    def test_fix_status_is_working_properly_for_fixing_with_dependent_statuses(self):
        """testing if the fix_status(() method is working properly for fixing
        status with dependent statuses
        """
        self.fail('test is not implemented yet')

    def test_fix_status_is_working_properly_for_fixing_with_children_statuses(self):
        """testing if the fix_status() method is working properly for fixing
        status with children statuses
        """
        self.fail('test is not implemented yet')
