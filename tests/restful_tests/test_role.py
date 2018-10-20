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
from stalker_pyramid2.views import role


class RoleViewsUnitTestCase(UnitTestBase):
    """unit tests for RoleViews class
    """

    def setUp(self):
        """create test data
        """
        super(RoleViewsUnitTestCase, self).setUp()

        from stalker import db, Role
        self.test_role1 = Role(
            name='Test Role 1',
            created_by=self.admin
        )
        db.DBSession.add(self.test_role1)

        self.test_role2 = Role(
            name='Test Role 2',
            created_by=self.admin
        )
        db.DBSession.add(self.test_role2)

        self.test_role3 = Role(
            name='Test Role 3',
            created_by=self.admin
        )
        db.DBSession.add(self.test_role3)
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_role1.id
        role_view = role.RoleViews(request)

        response = role_view.get_entity()

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'name': 'admin',
                    'id': 3,
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_role1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_role1.date_updated
                    ),
                'description': '',
                'entity_type': 'Role',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_role1.id,
                    'length': 0
                },
                'id': self.test_role1.id,
                'name': 'Test Role 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_role1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_role1.id,
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
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        role_view = role.RoleViews(request)

        response = role_view.get_entities()

        from stalker import Role
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Role',
                    '$ref': '/api/roles/%s' % r.id
                } for r in Role.query.all()
            ]
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict

        request = DummyRequest()
        request.matchdict['id'] = self.test_role1.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Role Name'
        request.params['description'] = 'New description'

        role_view = role.RoleViews(request)

        self.patch_logged_in_user(request)
        response = role_view.update_entity()

        from stalker import Role
        role_db = Role.query.get(self.test_role1.id)

        self.assertEqual(role_db.name, 'New Role Name')
        self.assertEqual(role_db.description, 'New description')

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Role'
        request.params['description'] = 'this is a new test role'
        request.params['created_by_id'] = 3

        role_view = role.RoleViews(request)

        self.patch_logged_in_user(request)
        response = role_view.create_entity()

        from stalker import Role
        role_db = Role.query\
            .filter(Role.name == 'New Role')\
            .first()

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'name': 'admin',
                    'id': 3,
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        role_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        role_db.date_updated
                    ),
                'description': 'this is a new test role',
                'entity_type': 'Role',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            role_db.id,
                    'length': 0
                },
                'id': role_db.id,
                'name': 'New Role',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % role_db.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % role_db.id,
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
        )

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_role1.id

        role_view = role.RoleViews(request)

        self.patch_logged_in_user(request)
        response = role_view.delete_entity()

        from stalker import Role
        self.assertIsNone(
            Role.query.filter(
                Role.id == self.test_role1.id
            ).first()
        )


class RoleViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for RoleViews class
    """

    def setUp(self):
        """create test data
        """
        super(RoleViewsFunctionalTestCase, self).setUp()

        from stalker import db, Role
        self.test_role1 = Role(
            name='Test Role 1',
            created_by=self.admin
        )
        db.DBSession.add(self.test_role1)

        self.test_role2 = Role(
            name='Test Role 2',
            created_by=self.admin
        )
        db.DBSession.add(self.test_role2)

        self.test_role3 = Role(
            name='Test Role 3',
            created_by=self.admin
        )
        db.DBSession.add(self.test_role3)
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/entities/{id} view is working properly
        """
        response = self.test_app.get(
            '/api/roles/%s' % self.test_role1.id,
            status=200
        )

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'name': 'admin',
                    'id': 3,
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_role1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_role1.date_updated
                    ),
                'description': '',
                'entity_type': 'Role',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_role1.id,
                    'length': 0
                },
                'id': self.test_role1.id,
                'name': 'Test Role 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_role1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_role1.id,
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
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET: /api/roles view is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        role_view = role.RoleViews(request)

        response = self.test_app.get(
            '/api/roles',
            status=200
        )

        from stalker import Role
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Role',
                    '$ref': '/api/roles/%s' % r.id
                } for r in Role.query.all()
            ]
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/roles/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.patch(
            '/api/roles/%s' % self.test_role1.id,
            status=200,
            params={
                'name': 'New Role Name',
                'description': 'New description',
            }
        )

        from stalker import Role
        role_db = Role.query.get(self.test_role1.id)

        self.assertEqual(role_db.name, 'New Role Name')
        self.assertEqual(role_db.description, 'New description')

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/roles/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.post(
            '/api/roles/%s' % self.test_role1.id,
            status=200,
            params={
                'name': 'New Role Name',
                'description': 'New description',
            }
        )

        from stalker import Role
        role_db = Role.query.get(self.test_role1.id)

        self.assertEqual(role_db.name, 'New Role Name')
        self.assertEqual(role_db.description, 'New description')

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/roles view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/roles',
            params={
                'name': 'New Role',
                'description': 'this is a new test role',
                'created_by_id': 3,
            },
            status=201
        )

        from stalker import Role
        role_db = Role.query\
            .filter(Role.name == 'New Role')\
            .first()

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'name': 'admin',
                    'id': 3,
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        role_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        role_db.date_updated
                    ),
                'description': 'this is a new test role',
                'entity_type': 'Role',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            role_db.id,
                    'length': 0
                },
                'id': role_db.id,
                'name': 'New Role',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % role_db.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % role_db.id,
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
        )

    def test_delete_entity_is_working_properly(self):
        """testing if DELETE: /api/roles/{id} view is working properly
        """
        response = self.test_app.delete(
            '/api/roles/%s' % self.test_role1.id,
            status=200
        )

        from stalker import Role
        self.assertIsNone(
            Role.query.filter(
                Role.id == self.test_role1.id
            ).first()
        )
