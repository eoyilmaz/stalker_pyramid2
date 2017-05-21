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
from stalker_pyramid.views import time_log


class TimeLogViewsUnitTestCase(UnitTestBase):
    """unit tests for the TimeLogViews class
    """

    def setUp(self):
        """setting the test up
        """
        super(TimeLogViewsUnitTestCase, self).setUp()

        # get the admin
        import datetime
        from stalker import User
        self.admin = User.query.filter(User.login == 'admin').first()
        # update the date_created to a known value
        self.admin.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.admin.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        # create test users
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@test.com',
            password='secret',
            created_by=self.admin,
        )

        # update the date_created to a known value
        self.test_user1.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.test_user1.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@test.com',
            password='secret',
            created_by=self.admin,
        )
        # update the date_created to a known value
        self.test_user2.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.test_user2.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@test.com',
            password='secret',
            created_by=self.admin,
        )
        # update the date_created to a known value
        self.test_user3.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.test_user3.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        # create Projects
        from stalker import Status, StatusList, Project, Repository
        self.test_status1 = Status(name='Work In Progress', code='WIP')
        self.test_status2 = Status(name='Completed', code='CMPL')
        self.test_status_list = StatusList(
            name='Project Status List',
            target_entity_type='Project',
            statuses=[self.test_status1, self.test_status2]
        )
        self.test_repo = Repository(
            name='Test Repository',
        )
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            status_list=self.test_status_list,
            repositories=[self.test_repo]
        )

        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            status_list=self.test_status_list,
            repositories=[self.test_repo]
        )

        # set user projects
        self.test_user1.projects = [self.test_project1]
        self.test_user2.projects = [self.test_project2]
        self.test_user3.projects = [self.test_project1, self.test_project2]

        from stalker import db
        db.DBSession.add_all([
            self.test_user1, self.test_user2, self.test_user3,
            self.test_status1, self.test_status2, self.test_status_list,
            self.test_repo, self.test_project1, self.test_project2
        ])
        db.DBSession.flush()
        db.DBSession.commit()

        # create tasks
        # tasks
        # as resource
        from stalker import Task
        self.test_task1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2],
            schedule_timing=10,
            schedule_unit='h',
            schedule_model='effort'
        )
        db.DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_task3)

        # as responsible
        self.test_task4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task4)

        self.test_task5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task5)

        self.test_task6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task6)

        # non related
        self.test_task7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task7)

        self.test_task8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task8)

        self.test_task9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task9)

        self.test_task10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task10)

        db.DBSession.flush()
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        # create a time log
        import datetime
        start = datetime.datetime(2016, 7, 26, 16)
        end = datetime.datetime(2016, 7, 26, 17)

        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=start,
            end=end,
            created_by=self.test_user2
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = t1.id
        time_log_view = time_log.TimeLogViews(request)

        from stalker_pyramid.views import EntityViewBase
        import stalker
        response = time_log_view.get_entity()
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(t1.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(t1.date_updated),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(t1.end),
                'entity_type': 'TimeLog',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % t1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': t1.id,
                'name': t1.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % t1.id,
                    'length': 0
                },
                'resource': {
                    'id': t1.resource_id,
                    '$ref': '/api/users/%s' % t1.resource_id,
                    'name': self.test_user1.name,
                    'entity_type': 'User'
                },
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(t1.start),
                'tags': {
                    '$ref': '/api/entities/%s/tags' % t1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        # create a time log
        import datetime
        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=datetime.datetime(2016, 7, 26, 16),
            end=datetime.datetime(2016, 7, 26, 17),
            created_by=self.test_user2
        )
        db.DBSession.add(t1)

        t2 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=datetime.datetime(2016, 7, 26, 17),
            end=datetime.datetime(2016, 7, 26, 18),
            created_by=self.test_user2
        )
        db.DBSession.add(t2)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        time_log_view = time_log.TimeLogViews(request)

        response = time_log_view.get_entities()
        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'entity_type': 'TimeLog',
                    'id': t.id,
                    'name': t.name,
                    '$ref': '/api/time_logs/%s' % t.id
                } for t in [t1, t2]
            ])
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        # create a time log
        import datetime
        start = datetime.datetime(2016, 7, 26, 16)
        end = datetime.datetime(2016, 7, 26, 17)
        new_end = datetime.datetime(2016, 7, 26, 18)

        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=start,
            end=end,
            created_by=self.test_user2
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = t1.id
        request.params = DummyMultiDict()

        from stalker_pyramid.views import EntityViewBase
        request.params['end'] = \
            EntityViewBase.milliseconds_since_epoch(new_end)

        self.patch_logged_in_user(request)
        time_log_view = time_log.TimeLogViews(request)

        response = time_log_view.update_entity()

        t1_db = TimeLog.query.filter(TimeLog.name == t1.name).first()
        self.assertEqual(t1_db.end, new_end)

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()

        import datetime
        from stalker_pyramid.views import EntityViewBase

        start = datetime.datetime(2016, 7, 27, 19)
        end = datetime.datetime(2016, 7, 27, 20)
        request.params['start'] = \
            EntityViewBase.milliseconds_since_epoch(start)
        request.params['end'] = EntityViewBase.milliseconds_since_epoch(end)
        request.params['task_id'] = self.test_task1.id
        request.params['resource_id'] = self.test_user1.id
        request.params['created_by_id'] = self.test_user2.id

        time_log_view = time_log.TimeLogViews(request)

        response = time_log_view.create_entity()

        from stalker import TimeLog
        t1 = TimeLog.query\
            .filter(TimeLog.resource == self.test_user1)\
            .filter(TimeLog.task == self.test_task1)\
            .first()

        import stalker
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(t1.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(t1.date_updated),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(end),
                'entity_type': 'TimeLog',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % t1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': t1.id,
                'name': t1.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % t1.id,
                    'length': 0
                },
                'resource': {
                    'id': t1.resource_id,
                    '$ref': '/api/users/%s' % t1.resource_id,
                    'name': self.test_user1.name,
                    'entity_type': 'User'
                },
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(start),
                'tags': {
                    '$ref': '/api/entities/%s/tags' % t1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        # create a time log
        import datetime
        start = datetime.datetime(2016, 7, 26, 16)
        end = datetime.datetime(2016, 7, 26, 17)

        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=start,
            end=end,
            created_by=self.test_user2
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = t1.id
        time_log_view = time_log.TimeLogViews(request)

        response = time_log_view.delete_entity()

        self.assertIsNone(
            TimeLog.query
            .filter(TimeLog.task == self.test_task1)
            .filter(TimeLog.resource == self.test_user1)
            .first()
        )


class TimeLogViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for the TimeLogViews class
    """

    def setUp(self):
        """setting the test up
        """
        super(TimeLogViewsFunctionalTestCase, self).setUp()

        # get the admin
        import datetime
        from stalker import User
        self.admin = User.query.filter(User.login == 'admin').first()
        # update the date_created to a known value
        self.admin.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.admin.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        # create test users
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@test.com',
            password='secret',
            created_by=self.admin,
        )

        # update the date_created to a known value
        self.test_user1.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.test_user1.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@test.com',
            password='secret',
            created_by=self.admin,
        )
        # update the date_created to a known value
        self.test_user2.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.test_user2.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@test.com',
            password='secret',
            created_by=self.admin,
        )
        # update the date_created to a known value
        self.test_user3.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.test_user3.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        # create Projects
        from stalker import Status, StatusList, Project, Repository
        self.test_status1 = Status(name='Work In Progress', code='WIP')
        self.test_status2 = Status(name='Completed', code='CMPL')
        self.test_status_list = StatusList(
            name='Project Status List',
            target_entity_type='Project',
            statuses=[self.test_status1, self.test_status2]
        )
        self.test_repo = Repository(
            name='Test Repository',
        )
        self.test_project1 = Project(
            name='Test Project 1',
            code='TP1',
            status_list=self.test_status_list,
            repositories=[self.test_repo]
        )

        self.test_project2 = Project(
            name='Test Project 2',
            code='TP2',
            status_list=self.test_status_list,
            repositories=[self.test_repo]
        )

        # set user projects
        self.test_user1.projects = [self.test_project1]
        self.test_user2.projects = [self.test_project2]
        self.test_user3.projects = [self.test_project1, self.test_project2]

        from stalker import db
        db.DBSession.add_all([
            self.test_user1, self.test_user2, self.test_user3,
            self.test_status1, self.test_status2, self.test_status_list,
            self.test_repo, self.test_project1, self.test_project2
        ])
        db.DBSession.flush()
        db.DBSession.commit()

        # create tasks
        # tasks
        # as resource
        from stalker import Task
        self.test_task1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2],
            schedule_timing=10,
            schedule_unit='h',
            schedule_model='effort'
        )
        db.DBSession.add(self.test_task1)

        self.test_task2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_task2)

        self.test_task3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(self.test_task3)

        # as responsible
        self.test_task4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task4)

        self.test_task5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task5)

        self.test_task6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(self.test_task6)

        # non related
        self.test_task7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task7)

        self.test_task8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task8)

        self.test_task9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task9)

        self.test_task10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(self.test_task10)

        db.DBSession.flush()
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/time_logs/{id} view is working properly
        """
        # create a time log
        import datetime
        start = datetime.datetime(2016, 7, 26, 16)
        end = datetime.datetime(2016, 7, 26, 17)

        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=start,
            end=end,
            created_by=self.test_user2
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/time_logs/%s' % t1.id,
            status=200
        )

        from stalker_pyramid.views import EntityViewBase
        import stalker
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(t1.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(t1.date_updated),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(t1.end),
                'entity_type': 'TimeLog',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % t1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': t1.id,
                'name': t1.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % t1.id,
                    'length': 0
                },
                'resource': {
                    'id': t1.resource_id,
                    '$ref': '/api/users/%s' % t1.resource_id,
                    'name': self.test_user1.name,
                    'entity_type': 'User'
                },
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(t1.start),
                'tags': {
                    '$ref': '/api/entities/%s/tags' % t1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET: /api/time_logs view is working properly
        """
        # create a time log
        import datetime
        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=datetime.datetime(2016, 7, 26, 16),
            end=datetime.datetime(2016, 7, 26, 17),
            created_by=self.test_user2
        )
        db.DBSession.add(t1)

        t2 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=datetime.datetime(2016, 7, 26, 17),
            end=datetime.datetime(2016, 7, 26, 18),
            created_by=self.test_user2
        )
        db.DBSession.add(t2)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/time_logs',
            status=200
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'entity_type': 'TimeLog',
                    'id': t.id,
                    'name': t.name,
                    '$ref': '/api/time_logs/%s' % t.id
                } for t in [t1, t2]
            ])
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/time_logs/{id} view is working properly
        """
        # create a time log
        import datetime
        start = datetime.datetime(2016, 7, 26, 16)
        end = datetime.datetime(2016, 7, 26, 17)
        new_end = datetime.datetime(2016, 7, 26, 18)

        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=start,
            end=end,
            created_by=self.test_user2
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        from stalker_pyramid.views import EntityViewBase

        self.admin_login()
        response = self.test_app.patch(
            '/api/time_logs/%s' % t1.id,
            params={
                'end': EntityViewBase.milliseconds_since_epoch(new_end)
            },
            status=200
        )

        t1_db = TimeLog.query.filter(TimeLog.name == t1.name).first()
        self.assertEqual(t1_db.end, new_end)

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/time_logs/{id} view is working properly
        """
        # create a time log
        import datetime
        start = datetime.datetime(2016, 7, 26, 16)
        end = datetime.datetime(2016, 7, 26, 17)
        new_end = datetime.datetime(2016, 7, 26, 18)

        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=start,
            end=end,
            created_by=self.test_user2
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        from stalker_pyramid.views import EntityViewBase

        self.admin_login()
        response = self.test_app.post(
            '/api/time_logs/%s' % t1.id,
            params={
                'end': EntityViewBase.milliseconds_since_epoch(new_end)
            },
            status=200
        )

        t1_db = TimeLog.query.filter(TimeLog.name == t1.name).first()
        self.assertEqual(t1_db.end, new_end)

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/time_logs view is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()

        import datetime
        from stalker_pyramid.views import EntityViewBase

        start = datetime.datetime(2016, 7, 27, 19)
        end = datetime.datetime(2016, 7, 27, 20)

        self.admin_login()
        response = self.test_app.put(
            '/api/time_logs',
            params={
                'start': EntityViewBase.milliseconds_since_epoch(start),
                'end': EntityViewBase.milliseconds_since_epoch(end),
                'task_id': self.test_task1.id,
                'resource_id': self.test_user1.id,
                'created_by_id': self.test_user2.id,
            },
            status=201
        )

        from stalker import TimeLog
        t1 = TimeLog.query\
            .filter(TimeLog.resource == self.test_user1)\
            .filter(TimeLog.task == self.test_task1)\
            .first()

        import stalker
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(t1.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(t1.date_updated),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(end),
                'entity_type': 'TimeLog',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % t1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': t1.id,
                'name': t1.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % t1.id,
                    'length': 0
                },
                'resource': {
                    'id': t1.resource_id,
                    '$ref': '/api/users/%s' % t1.resource_id,
                    'name': self.test_user1.name,
                    'entity_type': 'User'
                },
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(start),
                'tags': {
                    '$ref': '/api/entities/%s/tags' % t1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.test_user2.id,
                    '$ref': '/api/users/%s' % self.test_user2.id,
                    'name': self.test_user2.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if DELETE: /api/time_logs/{id} view is working properly
        """
        # create a time log
        import datetime
        start = datetime.datetime(2016, 7, 26, 16)
        end = datetime.datetime(2016, 7, 26, 17)

        from stalker import db, TimeLog

        db.DBSession.flush()
        db.DBSession.commit()

        t1 = TimeLog(
            task=self.test_task1,
            resource=self.test_user1,
            start=start,
            end=end,
            created_by=self.test_user2
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/time_logs/%s' % t1.id,
            status=200
        )

        self.assertIsNone(
            TimeLog.query
            .filter(TimeLog.task == self.test_task1)
            .filter(TimeLog.resource == self.test_user1)
            .first()
        )
