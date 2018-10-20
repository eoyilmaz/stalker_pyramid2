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
from stalker_pyramid2.views import group


class GroupViewsUnitTestCase(UnitTestBase):
    """unit tests for GroupViews class
    """

    def setUp(self):
        """create test data
        """
        super(GroupViewsUnitTestCase, self).setUp()
        admin = self.admin  # just to prevent autoflush

        from stalker import db, User
        # user1
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user1)

        # user2
        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user2)

        # user3
        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user3)

        from stalker import Permission

        # create a couple of groups
        from stalker import Group
        self.test_group1 = Group(
            name='Test Group',
            users=[self.test_user1, self.test_user2],
            created_by=self.admin
        )

        db.DBSession.add(self.test_group1)
        db.DBSession.commit()

        self.perm_allow_create_user = \
            Permission.query.filter(Permission.access == 'Allow')\
                .filter(Permission.action == 'Create')\
                .filter(Permission.class_name == 'User')\
                .first()
        self.perm_allow_read_user = \
            Permission.query.filter(Permission.access == 'Allow')\
                .filter(Permission.action == 'Read')\
                .filter(Permission.class_name == 'User')\
                .first()
        self.perm_allow_update_user = \
            Permission.query.filter(Permission.access == 'Allow')\
                .filter(Permission.action == 'Update')\
                .filter(Permission.class_name == 'User')\
                .first()
        self.perm_deny_delete_user = \
            Permission.query.filter(Permission.access == 'Deny')\
                .filter(Permission.action == 'Delete')\
                .filter(Permission.class_name == 'User')\
                .first()

        self.test_group1.permissions = [
            self.perm_allow_create_user,
            self.perm_allow_read_user,
            self.perm_allow_update_user,
            self.perm_deny_delete_user,
        ]
        db.DBSession.commit()

        # get permissions
        self.all_permissions = Permission.query.all()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id

        group_view = group.GroupViews(request)
        response = group_view.get_entity()

        import stalker
        from stalker_pyramid2.views import EntityViewBase

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_group1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_group1.date_updated
                    ),
                'description': '',
                'entity_type': 'Group',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_group1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': self.test_group1.id,
                'name': 'Test Group',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_group1.id,
                    'length': 0
                },
                'permissions': [
                    'Allow_Create_User',
                    'Allow_Read_User',
                    'Allow_Update_User',
                    'Deny_Delete_User'
                ],
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_group1.id,
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
                'users': {
                    '$ref': '/api/groups/%s/users' % self.test_group1.id,
                    'length': 2
                }
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        group_view = group.GroupViews(request)
        response = group_view.get_entities()

        from stalker import Group
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': g.id,
                    'name': g.name,
                    'entity_type': 'Group',
                    '$ref': '/api/groups/%s' % g.id
                } for g in Group.query.all()
            ])
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id
        request.params = DummyMultiDict()
        request.params['name'] = 'New Group Name'
        request.params['user_id'] = [self.test_user1.id, self.test_user2.id]
        request.params['description'] = 'New description'

        request.params['permission'] = \
            ['%s_%s_%s' % (p.access, p.action, p.class_name)
             for p in self.all_permissions[0:5]]

        group_view = group.GroupViews(request)

        self.patch_logged_in_user(request)
        response = group_view.update_entity()

        # get group1 from db
        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(test_group1_db.name, 'New Group Name')
        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1, self.test_user2])
        )
        self.assertEqual(test_group1_db.description, 'New description')
        self.assertEqual(
            sorted(test_group1_db.permissions),
            sorted(self.all_permissions[0:5])
        )

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Group'
        request.params['description'] = 'This is a new test group'
        request.params['user_id'] = [self.test_user1.id, self.test_user3.id]
        request.params['permission'] = \
            ['%s_%s_%s' % (p.access, p.action, p.class_name)
             for p in self.all_permissions[4:10]]
        request.params['created_by_id'] = self.test_user2.id

        group_view = group.GroupViews(request)
        response = group_view.create_entity()

        # get the new group from db
        import stalker
        from stalker import Group
        from stalker_pyramid2.views import EntityViewBase
        new_group = Group.query.filter(Group.name == 'New Group').first()

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
                    EntityViewBase.milliseconds_since_epoch(new_group.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(new_group.date_updated),
                'description': 'This is a new test group',
                'entity_type': 'Group',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_group.id,
                    'length': 0
                },
                'generic_text': '',
                'id': new_group.id,
                'name': 'New Group',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_group.id,
                    'length': 0
                },
                'permissions': [
                    '%s_%s_%s' % (p.access, p.action, p.class_name)
                    for p in self.all_permissions[4:10]
                ],
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % new_group.id,
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
                'users': {
                    '$ref': '/api/groups/%s/users' % new_group.id,
                    'length': 2
                }
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id
        group_view = group.GroupViews(request)
        response = group_view.delete_entity()

        from stalker import Group
        self.assertIsNone(
            Group.query.filter(Group.name == self.test_group1.name).first()
        )

    def test_get_users_is_working_properly(self):
        """testing if get_users() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id
        group_view = group.GroupViews(request)
        response = group_view.get_users()

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': u.id,
                    'name': u.name,
                    'entity_type': 'User',
                    '$ref': '/api/users/%s' % u.id
                } for u in [self.test_user1, self.test_user2]
            ])
        )

    def test_update_users_is_working_properly_with_patch(self):
        """testing if update_users() method is working properly with request
        method is patch
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id
        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user3.id]
        request.method = 'PATCH'

        group_view = group.GroupViews(request)
        response = group_view.update_users()

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1, self.test_user2, self.test_user3])
        )

    def test_update_users_is_working_properly_with_post(self):
        """testing if update_users() method is working properly with request
        method is post
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id
        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user2.id, self.test_user3.id]
        request.method = 'POST'

        group_view = group.GroupViews(request)
        response = group_view.update_users()

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user2, self.test_user3])
        )

    def test_remove_users_is_working_properly(self):
        """testing if remove_users() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id
        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user2.id]

        group_view = group.GroupViews(request)
        response = group_view.remove_users()

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1])
        )

    def test_remove_users_is_working_properly_with_non_related_user_instances(self):
        """testing if remove_users() method is working properly with non
        related user instances
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_group1.id
        request.params = DummyMultiDict()

        # self.test_user3 is not in this group
        request.params['user_id'] = [self.test_user2.id, self.test_user3.id]

        group_view = group.GroupViews(request)
        response = group_view.remove_users()

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1])
        )


class GroupViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for GroupViews class
    """

    def setUp(self):
        """create test data
        """
        super(GroupViewsFunctionalTestCase, self).setUp()

        from stalker import db, User
        # user1
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user1)

        # user2
        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user2)

        # user3
        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret'
        )
        db.DBSession.add(self.test_user3)

        from stalker import Permission

        # create a couple of groups
        from stalker import Group
        self.test_group1 = Group(
            name='Test Group',
            users=[self.test_user1, self.test_user2],
            created_by=self.admin
        )

        db.DBSession.add(self.test_group1)
        db.DBSession.commit()

        self.perm_allow_create_user = \
            Permission.query.filter(Permission.access == 'Allow')\
                .filter(Permission.action == 'Create')\
                .filter(Permission.class_name == 'User')\
                .first()
        self.perm_allow_read_user = \
            Permission.query.filter(Permission.access == 'Allow')\
                .filter(Permission.action == 'Read')\
                .filter(Permission.class_name == 'User')\
                .first()
        self.perm_allow_update_user = \
            Permission.query.filter(Permission.access == 'Allow')\
                .filter(Permission.action == 'Update')\
                .filter(Permission.class_name == 'User')\
                .first()
        self.perm_deny_delete_user = \
            Permission.query.filter(Permission.access == 'Deny')\
                .filter(Permission.action == 'Delete')\
                .filter(Permission.class_name == 'User')\
                .first()

        self.test_group1.permissions = [
            self.perm_allow_create_user,
            self.perm_allow_read_user,
            self.perm_allow_update_user,
            self.perm_deny_delete_user,
        ]
        db.DBSession.commit()

        # get permissions
        self.all_permissions = Permission.query.all()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/groups/{id} view is working properly
        """
        response = self.test_app.get(
            '/api/groups/%s' % self.test_group1.id,
            status=200
        )

        import stalker
        from stalker_pyramid2.views import EntityViewBase

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_group1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_group1.date_updated
                    ),
                'description': '',
                'entity_type': 'Group',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_group1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': self.test_group1.id,
                'name': 'Test Group',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_group1.id,
                    'length': 0
                },
                'permissions': [
                    'Allow_Create_User',
                    'Allow_Read_User',
                    'Allow_Update_User',
                    'Deny_Delete_User'
                ],
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_group1.id,
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
                'users': {
                    '$ref': '/api/groups/%s/users' % self.test_group1.id,
                    'length': 2
                }
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET: /api/groups view is working properly
        """
        response = self.test_app.get(
            '/api/groups',
            status=200
        )

        from stalker import Group
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': g.id,
                    'name': g.name,
                    'entity_type': 'Group',
                    '$ref': '/api/groups/%s' % g.id
                } for g in Group.query.all()
            ])
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/groups/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.patch(
            '/api/groups/%s' % self.test_group1.id,
            params={
                'name': 'New Group Name',
                'user_id': [self.test_user1.id, self.test_user2.id],
                'description': 'New description',
                'permission': [
                    '%s_%s_%s' % (p.access, p.action, p.class_name)
                    for p in self.all_permissions[0:5]
                ]
            }
        )

        # get group1 from db
        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(test_group1_db.name, 'New Group Name')
        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1, self.test_user2])
        )
        self.assertEqual(test_group1_db.description, 'New description')
        self.assertEqual(
            sorted(test_group1_db.permissions),
            sorted(self.all_permissions[0:5])
        )

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/groups/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.post(
            '/api/groups/%s' % self.test_group1.id,
            params={
                'name': 'New Group Name',
                'user_id': [self.test_user1.id, self.test_user2.id],
                'description': 'New description',
                'permission': [
                    '%s_%s_%s' % (p.access, p.action, p.class_name)
                    for p in self.all_permissions[0:5]
                ]
            }
        )

        # get group1 from db
        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(test_group1_db.name, 'New Group Name')
        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1, self.test_user2])
        )
        self.assertEqual(test_group1_db.description, 'New description')
        self.assertEqual(
            sorted(test_group1_db.permissions),
            sorted(self.all_permissions[0:5])
        )

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/groups view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/groups',
            params={
                'name': 'New Group',
                'description': 'This is a new test group',
                'user_id': [self.test_user1.id, self.test_user3.id],
                'permission':[
                    '%s_%s_%s' % (p.access, p.action, p.class_name)
                    for p in self.all_permissions[4:10]
                ],
                'created_by_id': self.test_user2.id
            },
            status=201
        )

        # get the new group from db
        import stalker
        from stalker import Group
        from stalker_pyramid2.views import EntityViewBase
        new_group = Group.query.filter(Group.name == 'New Group').first()

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
                    EntityViewBase.milliseconds_since_epoch(
                        new_group.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        new_group.date_updated
                    ),
                'description': 'This is a new test group',
                'entity_type': 'Group',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_group.id,
                    'length': 0
                },
                'generic_text': '',
                'id': new_group.id,
                'name': 'New Group',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_group.id,
                    'length': 0
                },
                'permissions': [
                    '%s_%s_%s' % (p.access, p.action, p.class_name)
                    for p in self.all_permissions[4:10]
                ],
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % new_group.id,
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
                'users': {
                    '$ref': '/api/groups/%s/users' % new_group.id,
                    'length': 2
                }
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if DELETE: /api/groups/{id} view is working properly
        """
        response = self.test_app.delete(
            '/api/groups/%s' % self.test_group1.id,
            status=200
        )

        from stalker import Group
        self.assertIsNone(
            Group.query.filter(Group.name == self.test_group1.name).first()
        )

    def test_get_users_is_working_properly(self):
        """testing if GET: /api/groups/{id}/users view is working properly
        """
        response = self.test_app.get(
            '/api/groups/%s/users' % self.test_group1.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': u.id,
                    'name': u.name,
                    'entity_type': 'User',
                    '$ref': '/api/users/%s' % u.id
                } for u in [self.test_user1, self.test_user2]
            ])
        )

    def test_update_users_is_working_properly_with_patch(self):
        """testing if PATCH: /api/groups/{id}/users view is working properly
        """
        self.admin_login()
        response = self.test_app.patch(
            '/api/groups/%s/users' % self.test_group1.id,
            params={
                'user_id': [self.test_user3.id]
            },
            status=200
        )

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1, self.test_user2, self.test_user3])
        )

    def test_update_users_is_working_properly_with_post(self):
        """testing if POST: /api/groups/{id}/users view is working properly
        """
        self.admin_login()
        response = self.test_app.post(
            '/api/groups/%s/users' % self.test_group1.id,
            params={
                'user_id': [self.test_user2.id, self.test_user3.id],
            },
            status=200
        )

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user2, self.test_user3])
        )

    def test_remove_users_is_working_properly(self):
        """testing if DELETE: /api/groups/{id}/users view is working properly
        """
        self.admin_login()
        response = self.test_app.delete(
            '/api/groups/%s/users?user_id=%s' % (
                self.test_group1.id, self.test_user2.id
            ),
            status=200
        )

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1])
        )

    def test_remove_users_is_working_properly_with_non_related_user_instances(self):
        """testing if DELETE: /api/groups/{id}/users view is working properly
        with non related user instances
        """
        response = self.test_app.delete(
            '/api/groups/%s/users?user_id=%s&user_id=%s' % (
                self.test_group1.id, self.test_user2.id, self.test_user3.id
            ),
            status=200
        )

        from stalker import Group
        test_group1_db = Group.query.get(self.test_group1.id)

        self.assertEqual(
            sorted(test_group1_db.users),
            sorted([self.test_user1])
        )
