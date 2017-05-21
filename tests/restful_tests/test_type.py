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
from stalker_pyramid.views import type


class TypeViewsUnitTestCase(UnitTestBase):
    """unit tests for the TypeViews class
    """

    def test_get_entity_method_is_working_properly(self):
        """testing if the get_entity() method is working properly
        """
        from stalker import db, Type
        test_type = Type(
            name='Test Type',
            code='TT',
            description='A test type',
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add(test_type)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_type.id

        type_view = type.TypeViews(request)
        response = type_view.get_entity()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'code': 'TT',
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_updated
                    ),
                'description': 'A test type',
                'entity_type': 'Type',
                'generic_text': '',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % test_type.id,
                    'length': 0
                },
                'id': test_type.id,
                'name': 'Test Type',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_type.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_type.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
            }
        )

    def test_get_entities_method_is_working_properly(self):
        """testing if the get_entities() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()

        type_view = type.TypeViews(request)
        response = type_view.get_entities()

        from stalker import Type
        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    '$ref': '/api/types/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in Type.query.all()
            ])
        )

    def test_create_entity_method_is_working_properly(self):
        """testing if the create_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict

        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'Test Type'
        request.params['code'] = 'TT'
        request.params['target_entity_type'] = 'Project'
        request.params['description'] = 'A test type'
        request.params['created_by_id'] = self.admin.id

        type_view = type.TypeViews(request)
        response = type_view.create_entity()

        from stalker import Type
        test_type = Type.query.filter(Type.name == 'Test Type').first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'code': 'TT',
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_updated
                    ),
                'description': 'A test type',
                'entity_type': 'Type',
                'generic_text': '',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % test_type.id,
                    'length': 0
                },
                'id': test_type.id,
                'name': 'Test Type',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_type.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_type.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_update_entity_method_is_working_properly(self):
        """testing if the update_entity() method is working properly
        """
        from stalker import db, Type
        test_type = Type(
            name='Test Type',
            code='TT',
            description='A test type',
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add(test_type)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_type.id
        request.params = DummyMultiDict()
        request.params['description'] = 'New description'
        request.params['name'] = 'New Name'
        request.params['code'] = 'New Code'

        self.patch_logged_in_user(request)
        type_view = type.TypeViews(request)
        response = type_view.update_entity()

        test_type_db = Type.query.get(test_type.id)
        self.assertEqual(test_type_db.name, 'New Name')
        self.assertEqual(test_type_db.code, 'New Code')
        self.assertEqual(test_type_db.description, 'New description')

    def test_delete_entity_method_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        from stalker import db, Type
        test_type = Type(
            name='Test Type',
            code='TT',
            description='A test type',
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add(test_type)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_type.id

        type_view = type.TypeViews(request)
        type_view.delete_entity()

        self.assertIsNotNone(test_type.id)
        self.assertIsNone(
            Type.query.filter(Type.id == test_type.id).first()
        )


class TypeViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for the TypeViews class
    """

    def test_get_entity_method_is_working_properly(self):
        """testing if the GET: /api/types/{id} view is working properly
        """
        from stalker import db, Type
        test_type = Type(
            name='Test Type',
            code='TT',
            description='A test type',
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add(test_type)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/types/%s' % test_type.id,
            status=200
        )

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'code': 'TT',
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_updated
                    ),
                'description': 'A test type',
                'entity_type': 'Type',
                'generic_text': '',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % test_type.id,
                    'length': 0
                },
                'id': test_type.id,
                'name': 'Test Type',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_type.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_type.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_get_entities_method_is_working_properly(self):
        """testing if the GET: /api/types view is working properly
        """
        response = self.test_app.get(
            '/api/types',
            status=200
        )

        from stalker import Type
        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    '$ref': '/api/types/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in Type.query.all()
            ])
        )

    def test_create_entity_method_is_working_properly(self):
        """testing if the PUT: /api/types is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/types',
            params={
                'name': 'Test Type',
                'code': 'TT',
                'target_entity_type': 'Project',
                'description': 'A test type',
            },
            status=201,
        )

        from stalker import Type
        test_type = Type.query.filter(Type.name == 'Test Type').first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'code': 'TT',
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_type.date_updated
                    ),
                'description': 'A test type',
                'entity_type': 'Type',
                'generic_text': '',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % test_type.id,
                    'length': 0
                },
                'id': test_type.id,
                'name': 'Test Type',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_type.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_type.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_update_entity_method_is_working_properly_with_patch(self):
        """testing if the PATCH: /api/types/{id} view is working properly
        """
        from stalker import db, Type
        test_type = Type(
            name='Test Type',
            code='TT',
            description='A test type',
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add(test_type)
        db.DBSession.commit()

        self.admin_login()
        response = self.test_app.patch(
            '/api/types/%s' % test_type.id,
            params={
                'description': 'New description',
                'name': 'New Name',
                'code': 'New Code'
            },
            status=200
        )

        test_type_db = Type.query.get(test_type.id)
        self.assertEqual(test_type_db.name, 'New Name')
        self.assertEqual(test_type_db.code, 'New Code')
        self.assertEqual(test_type_db.description, 'New description')

    def test_update_entity_method_is_working_properly_with_post(self):
        """testing if the POST: /api/types/{id} view is working properly
        """
        from stalker import db, Type
        test_type = Type(
            name='Test Type',
            code='TT',
            description='A test type',
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add(test_type)
        db.DBSession.commit()

        self.admin_login()
        response = self.test_app.post(
            '/api/types/%s' % test_type.id,
            params={
                'description': 'New description',
                'name': 'New Name',
                'code': 'New Code'
            },
            status=200
        )

        test_type_db = Type.query.get(test_type.id)
        self.assertEqual(test_type_db.name, 'New Name')
        self.assertEqual(test_type_db.code, 'New Code')
        self.assertEqual(test_type_db.description, 'New description')

    def test_delete_entity_method_is_working_properly(self):
        """testing if the DELETE: /api/types/{id} view is working properly
        """
        from stalker import db, Type
        test_type = Type(
            name='Test Type',
            code='TT',
            description='A test type',
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add(test_type)
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/types/%s' % test_type.id,
            status=200
        )

        self.assertIsNotNone(test_type.id)
        self.assertIsNone(
            Type.query.filter(Type.id == test_type.id).first()
        )

