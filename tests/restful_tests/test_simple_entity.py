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

from stalker_pyramid2.testing import UnitTestBase, FunctionalTestBase
from stalker_pyramid2.views import entity


class SimpleEntityViewsUnitTestCase(UnitTestBase):
    """unit tests for the SimpleEntity views
    """

    def test_get_simple_entity(self):
        """testing GET a SimpleEntity instance
        """
        # create a test simple entity
        from stalker import db, SimpleEntity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        test_simple_entity_type = Type(
            name='Test Simple Entity',
            code='TSE',
            target_entity_type='SimpleEntity'
        )
        db.DBSession.add(test_simple_entity_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)
        test_simple_entity = SimpleEntity(
            name='Test Entity',
            description='This is a test description',
            created_by=self.admin,
            type=test_simple_entity_type,
            date_created=date_created,
            thumbnail=test_thumbnail,
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity.id

        simple_entity_view = entity.SimpleEntityViews(request)
        response = simple_entity_view.get_entity()

        from stalker_pyramid2.views import EntityViewBase
        import stalker

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(date_created),
                'description': 'This is a test description',
                'entity_type': 'SimpleEntity',
                'id': test_simple_entity.id,
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_simple_entity.id,
                    'length': 0
                },
                'name': 'Test Entity',
                'stalker_version': stalker.__version__,
                'thumbnail': {
                    'id': test_thumbnail.id,
                    '$ref': '/api/links/%s' % test_thumbnail.id,
                    'name': test_thumbnail.name,
                    'entity_type': test_thumbnail.entity_type
                },
                'type': {
                    'id': test_simple_entity_type.id,
                    '$ref': '/api/types/%s' % test_simple_entity_type.id,
                    'name': test_simple_entity_type.name,
                    'entity_type': test_simple_entity_type.entity_type
                },
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
            }
        )

    def test_get_simple_entities(self):
        """testing GET multiple SimpleEntity instances
        """
        # create a couple of test simple entities
        from stalker import db, SimpleEntity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)

        # Test Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Entity 1',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_simple_entity1)

        # Test Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Entity 2',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_simple_entity2)

        # Test Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Entity 3',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_simple_entity3)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()

        simple_entity_view = entity.SimpleEntityViews(request)
        response = simple_entity_view.get_entities()

        # admins department
        admins_department = SimpleEntity.query\
            .filter(SimpleEntity.name == 'admins')\
            .filter(SimpleEntity.entity_type == 'Department')\
            .first()

        # admins group
        admins_group = SimpleEntity.query\
            .filter(SimpleEntity.name == 'admins')\
            .filter(SimpleEntity.entity_type == 'Group')\
            .first()

        # Statuses
        status_new = SimpleEntity.query\
            .filter(SimpleEntity.name == 'New').first()
        status_accepted = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Accepted').first()
        status_assigned = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Assigned').first()
        status_reopened = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Reopened').first()
        status_closed = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Closed').first()
        status_open = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Open').first()
        status_wfd = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Waiting For Dependency').first()
        status_rts = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Ready To Start').first()
        status_wip = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Work In Progress').first()
        status_prev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Pending Review').first()
        status_hrev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Has Revision').first()
        status_drev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Dependency Has Revision').first()
        status_oh = SimpleEntity.query\
            .filter(SimpleEntity.name == 'On Hold').first()
        status_stop = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Stopped').first()
        status_cmpl = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Completed').first()
        status_rrev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Requested Revision').first()
        status_app = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Approved').first()

        # Status Lists
        ticket_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Ticket Statuses').first()
        daily_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Daily Statuses').first()
        task_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Task Statuses').first()
        asset_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Asset Statuses').first()
        shot_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Shot Statuses').first()
        sequence_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Sequence Statuses').first()
        review_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Review Statuses').first()

        # Types
        type_defect = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Defect').first()
        type_enhancement = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Enhancement').first()

        all_data = [
            test_simple_entity1, test_simple_entity2, test_simple_entity3,
            admins_department, admins_group, self.admin,
            status_new, status_accepted, status_assigned, status_reopened,
            status_closed, status_open, status_wfd, status_rts, status_wip,
            status_prev, status_hrev, status_drev, status_oh, status_stop,
            status_cmpl, status_rrev, status_app,
            ticket_statuses, daily_statuses, task_statuses, asset_statuses,
            shot_statuses, sequence_statuses, review_statuses,
            type_defect, type_enhancement, test_type, test_thumbnail,
        ]

        from stalker_pyramid2 import entity_type_to_url
        self.maxDiff = None
        expected_result = [
            {
                'id': r.id,
                '$ref': '%s/%s' % (entity_type_to_url[r.entity_type], r.id),
                'name': r.name,
                'entity_type': r.entity_type
            } for r in all_data
        ]

        self.assertEqual(
            sorted(response.json_body, key=lambda x: x['id']),
            sorted(expected_result, key=lambda x: x['id'])
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if the update_entity() method is working properly with the
        patch method
        """
        from stalker import db, SimpleEntity, User
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(test_user2)

        from stalker import Type
        test_type1 = Type(
            name='Test Type 1',
            code='ttype1',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type1)

        test_type2 = Type(
            name='Test Type 2',
            code='ttype2',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type2)

        test_simple_entity = SimpleEntity(
            name='Test Simple Entity',
            created_by=test_user1,
            type=test_type1
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Name'
        request.method = 'PATCH'

        self.patch_logged_in_user(request)
        simple_entity_views = entity.SimpleEntityViews(request)
        simple_entity_views.update_entity()

        # check if the name is updated
        test_simple_entity_db = SimpleEntity.query.get(test_simple_entity.id)

        self.assertEqual(
            test_simple_entity_db.name,
            'New Name'
        )

    def test_update_entity_is_working_properly_with_patch_multiple_params(self):
        """testing if the update_entity() method is working properly with the
        patch method and multiple parameters
        """
        from stalker import db, SimpleEntity, User
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(test_user2)

        from stalker import Type
        test_type1 = Type(
            name='Test Type 1',
            code='ttype1',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type1)

        test_type2 = Type(
            name='Test Type 2',
            code='ttype2',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type2)

        test_simple_entity = SimpleEntity(
            name='Test Simple Entity',
            created_by=test_user1,
            type=test_type1
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Name'
        request.params['description'] = 'New description'
        request.params['created_by_id'] = test_user2.id
        request.method = 'PATCH'

        self.patch_logged_in_user(request)
        simple_entity_views = entity.SimpleEntityViews(request)
        simple_entity_views.update_entity()

        # check if the name is updated
        test_simple_entity_db = SimpleEntity.query.get(test_simple_entity.id)

        self.assertEqual(
            test_simple_entity_db.name,
            'New Name'
        )
        self.assertEqual(
            test_simple_entity_db.description,
            'New description'
        )
        self.assertEqual(
            test_simple_entity_db.created_by,
            test_user2
        )

    def test_update_entity_is_working_properly_with_post(self):
        """testing if the update_entity() method is working properly with the
        post method
        """
        from stalker import db, SimpleEntity, User
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(test_user2)

        from stalker import Type
        test_type1 = Type(
            name='Test Type 1',
            code='ttype1',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type1)

        test_type2 = Type(
            name='Test Type 2',
            code='ttype2',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type2)

        test_simple_entity = SimpleEntity(
            name='Test Simple Entity',
            created_by=test_user1,
            type=test_type1
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Name'
        request.params['description'] = 'New description'
        request.params['created_by_id'] = test_user2.id
        request.method = 'POST'

        self.patch_logged_in_user(request)
        simple_entity_views = entity.SimpleEntityViews(request)
        simple_entity_views.update_entity()

        # check if the name is updated
        test_simple_entity_db = SimpleEntity.query.get(test_simple_entity.id)

        self.assertEqual(
            test_simple_entity_db.name,
            'New Name'
        )
        self.assertEqual(
            test_simple_entity_db.description,
            'New description'
        )
        self.assertEqual(
            test_simple_entity_db.created_by,
            test_user2
        )

    def test_get_generic_data(self):
        """testing GET generic data of a SimpleEntity instance
        """
        # create a test simple entity
        from stalker import db, SimpleEntity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)

        # create different types of generic data
        # SimpleEntity
        generic_data1 = SimpleEntity(
            name='Generic Data 1'
        )
        # User
        from stalker import User
        generic_data2 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret'
        )
        # Department
        from stalker import Department
        generic_data3 = Department(
            name='Generic Data 3',
        )
        db.DBSession.add_all([generic_data1, generic_data2, generic_data3])

        test_simple_entity1 = SimpleEntity(
            name='Test Entity 1',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail,
        )
        test_simple_entity1.generic_data = \
            [generic_data1, generic_data2, generic_data3]

        db.DBSession.add(test_simple_entity1)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity1.id

        simple_entity_view = entity.SimpleEntityViews(request)
        result = simple_entity_view.get_generic_data()

        self.maxDiff = None
        self.assertEqual(
            sorted(result.json_body),
            sorted([
                {
                    'id': generic_data1.id,
                    '$ref': '/api/simple_entities/%s' % generic_data1.id,
                    'name': generic_data1.name,
                    'entity_type': generic_data1.entity_type
                },
                {
                    'id': generic_data2.id,
                    '$ref': '/api/users/%s' % generic_data2.id,
                    'name': generic_data2.name,
                    'entity_type': generic_data2.entity_type
                },
                {
                    'id': generic_data3.id,
                    '$ref': '/api/departments/%s' % generic_data3.id,
                    'name': generic_data3.name,
                    'entity_type': generic_data3.entity_type
                },
            ])
        )

    def test_update_generic_data_is_working_properly_with_patch(self):
        """testing if the update_generic_data() method is working properly with
        the request method is PATCH
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity1.id
        request.method = 'PATCH'
        request.params = DummyMultiDict()
        request.params['entity_id'] = \
            [test_simple_entity4.id, test_simple_entity5.id]
        request.POST = request.params

        from stalker_pyramid2.views.entity import SimpleEntityViews
        simple_entity_view = SimpleEntityViews(request)
        simple_entity_view.update_generic_data()

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity2, test_simple_entity3,
                    test_simple_entity4, test_simple_entity5]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_update_generic_data_is_working_properly_with_put(self):
        """testing if the update_generic_data() method is working properly with
        the request method is PUT
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity1.id
        request.method = 'PUT'
        request.params = DummyMultiDict()
        request.params['entity_id'] = \
            [test_simple_entity4.id, test_simple_entity5.id]
        request.POST = request.params

        from stalker_pyramid2.views.entity import SimpleEntityViews
        simple_entity_view = SimpleEntityViews(request)
        simple_entity_view.update_generic_data()

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity4, test_simple_entity5]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_update_generic_data_is_working_properly_with_post(self):
        """testing if the update_generic_data() method is working properly with
        the request method is POST
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity1.id
        request.method = 'POST'
        request.params = DummyMultiDict()
        request.params['entity_id'] = \
            [test_simple_entity4.id, test_simple_entity5.id]
        request.POST = request.params

        from stalker_pyramid2.views.entity import SimpleEntityViews
        simple_entity_view = SimpleEntityViews(request)
        simple_entity_view.update_generic_data()

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity4, test_simple_entity5]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_delete_generic_data_is_working_properly(self):
        """testing if the delete_generic_data() method is working properly
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3, test_simple_entity4,
            test_simple_entity5
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity1.id
        request.method = 'DELETE'
        request.params = DummyMultiDict()
        request.params['entity_id'] = \
            [test_simple_entity4.id, test_simple_entity5.id]
        request.POST = request.params

        from stalker_pyramid2.views.entity import SimpleEntityViews
        simple_entity_view = SimpleEntityViews(request)
        simple_entity_view.delete_generic_data()

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity2, test_simple_entity3]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_delete_generic_data_is_working_properly_with_non_related_data(self):
        """testing if the delete_generic_data() method is working properly when
        the given entity is not related with the simple entity
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity1.id
        request.method = 'DELETE'
        request.params = DummyMultiDict()
        request.params['entity_id'] = [
            test_simple_entity3.id,
            test_simple_entity4.id,
            test_simple_entity5.id
        ]
        request.POST = request.params

        from stalker_pyramid2.views.entity import SimpleEntityViews
        simple_entity_view = SimpleEntityViews(request)
        simple_entity_view.delete_generic_data()

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity2]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker import db, SimpleEntity
        test_simple_entity = SimpleEntity(
            name='Test SimpleEntity'
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        test_simple_entity_db = SimpleEntity.query\
            .filter(SimpleEntity.name == test_simple_entity.name)\
            .first()

        self.assertIsNotNone(test_simple_entity_db)

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_simple_entity_db.id

        simple_entity_view = entity.SimpleEntityViews(request)
        simple_entity_view.delete_entity()

        test_simple_entity_db = SimpleEntity.query\
            .filter(SimpleEntity.name == test_simple_entity.name)\
            .first()

        self.assertIsNone(test_simple_entity_db)


class SimpleEntityViewFunctionalTestCase(FunctionalTestBase):
    """functional tests for the SimpleEntity views
    """

    def test_get_simple_entity(self):
        """testing GET a SimpleEntity instance
        """
        # create a test simple entity
        from stalker import db, SimpleEntity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)
        test_simple_entity = SimpleEntity(
            name='Test Entity',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        self.admin_login()

        response = self.test_app.get(
            '/api/simple_entities/%s' % test_simple_entity.id,
            status=200
        )

        from stalker_pyramid2.views import EntityViewBase
        import stalker

        self.maxDiff = None
        self.assertEqual(
            response.json,
            {
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(date_created),
                'description': 'This is a test description',
                'entity_type': 'SimpleEntity',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_simple_entity.id,
                    'length': 0
                },
                'id': test_simple_entity.id,
                'name': 'Test Entity',
                'stalker_version': stalker.__version__,
                'thumbnail': {
                    'id': test_thumbnail.id,
                    '$ref': '/api/links/%s' % test_thumbnail.id,
                    'name': test_thumbnail.name,
                    'entity_type': test_thumbnail.entity_type
                },
                'type': {
                    'id': test_type.id,
                    '$ref': '/api/types/%s' % test_type.id,
                    'name': test_type.name,
                    'entity_type': test_type.entity_type
                },
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
            }
        )

    def test_get_simple_entities(self):
        """testing GET multiple SimpleEntity instances
        """
        # create a couple of test simple entities
        from stalker import db, SimpleEntity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)

        # Test Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Entity 1',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_simple_entity1)

        # Test Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Entity 2',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_simple_entity2)

        # Test Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Entity 3',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_simple_entity3)

        # commit data
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/simple_entities',
            status=200
        )

        # admins department
        admins_department = SimpleEntity.query\
            .filter(SimpleEntity.name == 'admins')\
            .filter(SimpleEntity.entity_type == 'Department')\
            .first()

        # admins group
        admins_group = SimpleEntity.query\
            .filter(SimpleEntity.name == 'admins')\
            .filter(SimpleEntity.entity_type == 'Group')\
            .first()

        # Statuses
        status_new = SimpleEntity.query\
            .filter(SimpleEntity.name == 'New').first()
        status_accepted = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Accepted').first()
        status_assigned = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Assigned').first()
        status_reopened = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Reopened').first()
        status_closed = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Closed').first()
        status_open = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Open').first()
        status_wfd = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Waiting For Dependency').first()
        status_rts = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Ready To Start').first()
        status_wip = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Work In Progress').first()
        status_prev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Pending Review').first()
        status_hrev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Has Revision').first()
        status_drev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Dependency Has Revision').first()
        status_oh = SimpleEntity.query\
            .filter(SimpleEntity.name == 'On Hold').first()
        status_stop = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Stopped').first()
        status_cmpl = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Completed').first()
        status_rrev = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Requested Revision').first()
        status_app = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Approved').first()

        # Status Lists
        ticket_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Ticket Statuses').first()
        daily_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Daily Statuses').first()
        task_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Task Statuses').first()
        asset_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Asset Statuses').first()
        shot_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Shot Statuses').first()
        sequence_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Sequence Statuses').first()
        review_statuses = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Review Statuses').first()

        # Types
        type_defect = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Defect').first()
        type_enhancement = SimpleEntity.query\
            .filter(SimpleEntity.name == 'Enhancement').first()

        all_data = [
            test_simple_entity1, test_simple_entity2, test_simple_entity3,
            admins_department, admins_group, self.admin,
            status_new, status_accepted, status_assigned, status_reopened,
            status_closed, status_open, status_wfd, status_rts, status_wip,
            status_prev, status_hrev, status_drev, status_oh, status_stop,
            status_cmpl, status_rrev, status_app,
            ticket_statuses, daily_statuses, task_statuses, asset_statuses,
            shot_statuses, sequence_statuses, review_statuses,
            type_defect, type_enhancement, test_type, test_thumbnail,
        ]

        from stalker_pyramid2 import entity_type_to_url
        self.maxDiff = None
        expected_result = [
            {
                'id': r.id,
                '$ref': '%s/%s' % (entity_type_to_url[r.entity_type], r.id),
                'name': r.name,
                'entity_type': r.entity_type
            } for r in all_data
        ]

        self.assertEqual(
            sorted(response.json, key=lambda x: x['id']),
            sorted(expected_result, key=lambda x: x['id'])
        )

    def test_update_entity_is_working_properly_with_patch_multiple_params(self):
        """testing if the update_entity() method is working properly with the
        patch method and multiple parameters
        """
        from stalker import db, SimpleEntity, User
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(test_user2)

        from stalker import Type
        test_type1 = Type(
            name='Test Type 1',
            code='ttype1',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type1)

        test_type2 = Type(
            name='Test Type 2',
            code='ttype2',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type2)

        test_simple_entity = SimpleEntity(
            name='Test Simple Entity',
            created_by=test_user1,
            type=test_type1
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.patch(
            '/api/simple_entities/%s' % test_simple_entity.id,
            params={
                'name': 'New Name',
                'description': 'New description',
                'created_by_id': test_user2.id,
            },
            status=200
        )

        # check if the name is updated
        test_simple_entity_db = SimpleEntity.query.get(test_simple_entity.id)

        self.assertEqual(
            test_simple_entity_db.name,
            'New Name'
        )
        self.assertEqual(
            test_simple_entity_db.description,
            'New description'
        )
        self.assertEqual(
            test_simple_entity_db.created_by,
            test_user2
        )

    def test_update_entity_is_working_properly_with_post(self):
        """testing if the update_entity() method is working properly with the
        post method
        """
        from stalker import db, SimpleEntity, User
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(test_user2)

        from stalker import Type
        test_type1 = Type(
            name='Test Type 1',
            code='ttype1',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type1)

        test_type2 = Type(
            name='Test Type 2',
            code='ttype2',
            target_entity_type='SimpleEntity',
        )
        db.DBSession.add(test_type2)

        test_simple_entity = SimpleEntity(
            name='Test Simple Entity',
            created_by=test_user1,
            type=test_type1
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.post(
            '/api/simple_entities/%s' % test_simple_entity.id,
            params={
                'name': 'New Name',
                'description': 'New description',
                'created_by_id': test_user2.id,
            },
            status=200
        )

        # check if the name is updated
        test_simple_entity_db = SimpleEntity.query.get(test_simple_entity.id)

        self.assertEqual(
            test_simple_entity_db.name,
            'New Name'
        )
        self.assertEqual(
            test_simple_entity_db.description,
            'New description'
        )
        self.assertEqual(
            test_simple_entity_db.created_by,
            test_user2
        )

    def test_get_generic_data(self):
        """testing GET generic data of a SimpleEntity instance
        """
        # create a test simple entity
        from stalker import db, SimpleEntity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)

        # create different types of generic data
        # SimpleEntity
        generic_data1 = SimpleEntity(
            name='Generic Data 1'
        )
        # User
        from stalker import User
        generic_data2 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret'
        )
        # Department
        from stalker import Department
        generic_data3 = Department(
            name='Generic Data 3',
        )
        db.DBSession.add_all([generic_data1, generic_data2, generic_data3])

        test_simple_entity1 = SimpleEntity(
            name='Test Entity 1',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail,
        )
        test_simple_entity1.generic_data = \
            [generic_data1, generic_data2, generic_data3]

        db.DBSession.add(test_simple_entity1)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/simple_entities/%s/generic_data' % test_simple_entity1.id,
            status=200
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json),
            sorted([
                {
                    'id': generic_data1.id,
                    '$ref': '/api/simple_entities/%s' % generic_data1.id,
                    'name': generic_data1.name,
                    'entity_type': generic_data1.entity_type
                },
                {
                    'id': generic_data2.id,
                    '$ref': '/api/users/%s' % generic_data2.id,
                    'name': generic_data2.name,
                    'entity_type': generic_data2.entity_type
                },
                {
                    'id': generic_data3.id,
                    '$ref': '/api/departments/%s' % generic_data3.id,
                    'name': generic_data3.name,
                    'entity_type': generic_data3.entity_type
                },
            ])
        )

    def test_update_generic_data_is_working_properly_with_patch(self):
        """testing if the update_generic_data() method is working properly with
        the request method is PATCH
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        self.test_app.patch(
            '/api/simple_entities/%s/generic_data'
            '?entity_id=%s&entity_id=%s' % (test_simple_entity1.id,
                                            test_simple_entity4.id,
                                            test_simple_entity5.id),
            status=200
        )

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity2, test_simple_entity3,
                    test_simple_entity4, test_simple_entity5]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_update_generic_data_is_working_properly_with_put(self):
        """testing if the update_generic_data() method is working properly with
        the request method is PUT
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        self.test_app.put(
            '/api/simple_entities/%s/generic_data'
            '?entity_id=%s&entity_id=%s' % (test_simple_entity1.id,
                                            test_simple_entity4.id,
                                            test_simple_entity5.id),
            status=200
        )

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity4, test_simple_entity5]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_update_generic_data_is_working_properly_with_post(self):
        """testing if the update_generic_data() method is working properly with
        the request method is POST
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        self.test_app.post(
            '/api/simple_entities/%s/generic_data'
            '?entity_id=%s&entity_id=%s' % (test_simple_entity1.id,
                                            test_simple_entity4.id,
                                            test_simple_entity5.id),
            status=200
        )

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity4, test_simple_entity5]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_delete_generic_data_is_working_properly(self):
        """testing if the delete_generic_data() method is working properly
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3, test_simple_entity4,
            test_simple_entity5
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        self.test_app.delete(
            '/api/simple_entities/%s/generic_data'
            '?entity_id=%s&entity_id=%s' % (test_simple_entity1.id,
                                            test_simple_entity4.id,
                                            test_simple_entity5.id),
            status=200
        )

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity2, test_simple_entity3]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_delete_generic_data_is_working_properly_with_non_related_data(self):
        """testing if the delete_generic_data() method is working properly when
        the given entity is not related with the simple entity
        """
        from stalker import db, SimpleEntity

        # Simple Entity 1
        test_simple_entity1 = SimpleEntity(
            name='Test Simple Entity 1'
        )
        db.DBSession.add(test_simple_entity1)

        # Simple Entity 2
        test_simple_entity2 = SimpleEntity(
            name='Test Simple Entity 2'
        )
        db.DBSession.add(test_simple_entity2)

        # Simple Entity 3
        test_simple_entity3 = SimpleEntity(
            name='Test Simple Entity 3'
        )
        db.DBSession.add(test_simple_entity3)

        # Simple Entity 4
        test_simple_entity4 = SimpleEntity(
            name='Test Simple Entity 4'
        )
        db.DBSession.add(test_simple_entity4)

        # Simple Entity 5
        test_simple_entity5 = SimpleEntity(
            name='Test Simple Entity 5'
        )
        db.DBSession.add(test_simple_entity5)

        test_simple_entity1.generic_data = [
            test_simple_entity2, test_simple_entity3
        ]

        db.DBSession.commit()

        # now add test_simple_entity4 and 5 to the
        self.test_app.delete(
            '/api/simple_entities/%s/generic_data'
            '?entity_id=%s&entity_id=%s&entity_id=%s' % (
                test_simple_entity1.id,
                test_simple_entity3.id,
                test_simple_entity4.id,
                test_simple_entity5.id
            ),
            status=200
        )

        test_simple_entity1 = SimpleEntity.query\
            .filter(SimpleEntity.id == test_simple_entity1.id).first()

        self.assertEqual(
            sorted([test_simple_entity2]),
            sorted(test_simple_entity1.generic_data)
        )

    def test_delete_entity_is_working_properly(self):
        """testing DELETE /api/simple_entities/{id} is working properly
        """
        from stalker import db, SimpleEntity
        test_simple_entity = SimpleEntity(
            name='Test SimpleEntity'
        )
        db.DBSession.add(test_simple_entity)
        db.DBSession.commit()

        test_simple_entity_db = SimpleEntity.query\
            .filter(SimpleEntity.name == test_simple_entity.name)\
            .first()

        self.assertIsNotNone(test_simple_entity_db)

        self.test_app.delete(
            '/api/simple_entities/%s' % test_simple_entity_db.id,
            status=200
        )

        test_simple_entity_db = SimpleEntity.query\
            .filter(SimpleEntity.name == test_simple_entity.name)\
            .first()

        self.assertIsNone(test_simple_entity_db)
