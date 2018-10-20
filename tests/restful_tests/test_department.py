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
from stalker_pyramid2.views import department


class DepartmentViewsUnitTestCase(UnitTestBase):
    """unit tests for DepartmentViews class
    """

    def setUp(self):
        """create the test data
        """
        super(DepartmentViewsUnitTestCase, self).setUp()

        from stalker import db, User
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret',
            created_by=self.admin
        )
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret',
            created_by=self.admin
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret',
            created_by=self.admin
        )
        db.DBSession.add(self.test_user3)

        from stalker import Department
        self.test_department1 = Department(
            name='Test Department 1',
            created_by=self.admin
        )
        db.DBSession.add(self.test_department1)

        self.test_department2 = Department(
            name='Test Department 2',
            created_by=self.admin
        )
        db.DBSession.add(self.test_department2)

        # create a couple of roles
        from stalker import Role
        self.test_role1 = Role(name='Test Role 1', created_by=self.admin)
        self.test_role2 = Role(name='Test Role 2', created_by=self.admin)
        self.test_role3 = Role(name='Test Role 3', created_by=self.admin)
        db.DBSession.add_all([
            self.test_role1, self.test_role2, self.test_role3
        ])
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if the get_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id

        department_view = department.DepartmentViews(request)
        response = department_view.get_entity()

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    self.test_department1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    self.test_department1.date_updated
                ),
                'description': '',
                'entity_type': 'Department',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_department1.id,
                    'length': 0
                },
                'id': self.test_department1.id,
                'name': 'Test Department 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' %
                            self.test_department1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_department1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'user_roles': {
                    '$ref': '/api/departments/%s/user_roles' %
                            self.test_department1.id,
                    'length': 0
                },
                'users': {
                    '$ref': '/api/departments/%s/users' %
                            self.test_department1.id,
                    'length': 0
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if the get_entities() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        department_view = department.DepartmentViews(request)
        response = department_view.get_entities()

        from stalker import Department
        all_deps = Department.query.all()
        self.assertEqual(
            sorted(response.json_body),
            [{
                'id': d.id,
                'name': d.name,
                '$ref': '/api/departments/%s' % d.id,
                'entity_type': d.entity_type
            } for d in all_deps]
        )

    def test_update_entity_is_working_properly(self):
        """testing if the update_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        request.params = DummyMultiDict()
        new_name = 'New Department Name'
        new_description = 'New Description'
        request.params['name'] = new_name
        request.params['description'] = new_description
        request.params['user_id'] = [self.test_user1.id, self.test_user2.id]

        department_view = department.DepartmentViews(request)

        self.patch_logged_in_user(request)
        response = department_view.update_entity()

        from stalker import Department
        test_department1_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(test_department1_db.name, new_name)
        self.assertEqual(test_department1_db.description, new_description)
        self.assertEqual(
            sorted(test_department1_db.users),
            sorted([self.test_user1, self.test_user2])
        )

    def test_create_entity_is_working_properly(self):
        """testing if the create_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Department'
        request.params['description'] = 'New department description'
        request.params['user_id'] = [self.test_user1.id, self.test_user2.id]

        department_view = department.DepartmentViews(request)
        print('code is here 1')
        self.patch_logged_in_user(request)
        print('code is here 2')
        response = department_view.create_entity()
        print('code is here 3')

        from stalker import Department
        new_dep = Department.query\
            .filter(Department.name == 'New Department')\
            .first()

        from stalker_pyramid2.views import EntityViewBase
        import stalker

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        new_dep.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        new_dep.date_updated
                    ),
                'description': 'New department description',
                'entity_type': 'Department',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_dep.id,
                    'length': 0
                },
                'id': new_dep.id,
                'name': 'New Department',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_dep.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % new_dep.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'user_roles': {
                    '$ref': '/api/departments/%s/user_roles' % new_dep.id,
                    'length': 2
                },
                'users': {
                    '$ref': '/api/departments/%s/users' % new_dep.id,
                    'length': 2
                },
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id

        department_view = department.DepartmentViews(request)
        department_view.delete_entity()

        from stalker import Department
        dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()
        self.assertIsNone(dep_db)

    def test_get_users_is_working_properly(self):
        """testing if the get_users() method is working properly
        """
        self.test_department1.users = [self.test_user1, self.test_user2]
        from stalker import db
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        department_view = department.DepartmentViews(request)
        response = department_view.get_users()

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': u.id,
                    'name': u.name,
                    '$ref': '/api/users/%s' % u.id,
                    'entity_type': 'User'
                } for u in [self.test_user1, self.test_user2]
            ])
        )

    def test_update_users_is_working_properly_with_patch(self):
        """testing if update_users() method is working properly with PATCH
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = [self.test_user1]
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id

        request.params = DummyMultiDict()
        request.method = 'PATCH'
        request.params['user_id'] = [self.test_user2.id, self.test_user3.id]

        department_view = department.DepartmentViews(request)
        response = department_view.update_users()

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user1, self.test_user2, self.test_user3])
        )

    def test_update_users_is_working_properly_with_post(self):
        """testing if update_users() method is working properly with POST
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = [self.test_user1]
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id

        request.params = DummyMultiDict()
        request.method = 'POST'
        request.params['user_id'] = [self.test_user2.id, self.test_user3.id]

        department_view = department.DepartmentViews(request)
        response = department_view.update_users()

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user2, self.test_user3])
        )

    def test_remove_users_is_working_properly(self):
        """testing if remove_users() method is working properly
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = \
            [self.test_user1, self.test_user2, self.test_user3]
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id

        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user2.id, self.test_user3.id]

        department_view = department.DepartmentViews(request)
        response = department_view.remove_users()

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user1])
        )

    def test_remove_users_is_working_properly_with_non_related_user(self):
        """testing if remove_users() method is working properly with users that
        is not related to the department
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = \
            [self.test_user1, self.test_user2]
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id

        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user2.id, self.test_user3.id]

        department_view = department.DepartmentViews(request)
        response = department_view.remove_users()

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user1])
        )

    def test_get_department_user_roles_is_working_properly(self):
        """testing if the get_department_user_roles() method is working
         properly
        """
        self.test_department1.users = [self.test_user1, self.test_user2]
        from stalker import db
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        department_view = department.DepartmentViews(request)
        response = department_view.get_user_roles()

        from stalker import DepartmentUser
        all_dep_users = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .all()

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'user': {
                        'id': du.user.id,
                        'name': du.user.name,
                        'entity_type': du.user.entity_type,
                        '$ref': '/api/users/%s' % du.user.id
                    },
                    'role': {
                        'id': du.role.id,
                        'name': du.role.name,
                        'entity_type': du.role.entity_type,
                        '$ref': '/api/roles/%s' % du.role.id
                    } if du.role else None
                } for du in all_dep_users
            ])
        )

    def test_update_user_roles_is_working_properly_with_patch(self):
        """testing if update_user_roles() method is working properly with PATCH
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        request.method = 'PATCH'

        request.params = DummyMultiDict()
        request.params['user_role'] = [
            '%s,%s' % (self.test_user1.id, self.test_role2.id),
            '%s,%s' % (self.test_user2.id, self.test_role3.id),
        ]

        department_view = department.DepartmentViews(request)
        department_view.update_user_role()

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertEqual(du1_db.role, self.test_role2)
        self.assertEqual(du2_db.role, self.test_role3)

    def test_update_user_roles_is_working_properly_with_post(self):
        """testing if update_user_roles() method is working properly with POST
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        request.method = 'POST'

        request.params = DummyMultiDict()
        request.params['user_role'] = [
            '%s,%s' % (self.test_user1.id, self.test_role2.id),
            '%s,%s' % (self.test_user2.id, self.test_role3.id),
        ]

        department_view = department.DepartmentViews(request)
        department_view.update_user_role()

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertEqual(du1_db.role, self.test_role2)
        self.assertEqual(du2_db.role, self.test_role3)

    def test_update_user_roles_is_working_properly_with_non_related_user(self):
        """testing if update_user_roles() method is working properly with non
        related user
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        request.method = 'POST'

        request.params = DummyMultiDict()
        request.params['user_role'] = [
            '%s,%s' % (self.test_user1.id, self.test_role2.id),
            '%s,%s' % (self.test_user2.id, self.test_role3.id),
            '%s,%s' % (self.test_user3.id, self.test_role1.id)
        ]

        department_view = department.DepartmentViews(request)
        department_view.update_user_role()

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertEqual(du1_db.role, self.test_role2)
        self.assertEqual(du2_db.role, self.test_role3)

    def test_remove_user_roles_is_working_properly(self):
        """testing if remove_user_roles() method is working properly
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        request.method = 'POST'

        request.params = DummyMultiDict()
        request.params['user_id'] = [self.test_user1.id, self.test_user2.id]

        department_view = department.DepartmentViews(request)
        department_view.remove_user_role()

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertIsNone(du1_db.role)
        self.assertIsNone(du2_db.role)

    def test_remove_user_roles_is_working_properly_with_non_related_user(self):
        """testing if remove_user_roles() method is working properly with non
        related user
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_department1.id
        request.method = 'POST'

        request.params = DummyMultiDict()
        request.params['user_id'] = \
            [self.test_user1.id, self.test_user2.id, self.test_user3.id]

        department_view = department.DepartmentViews(request)
        department_view.remove_user_role()

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertIsNone(du1_db.role)
        self.assertIsNone(du2_db.role)


class DepartmentViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for DepartmentViews class
    """

    def setUp(self):
        """create the test data
        """
        super(DepartmentViewsFunctionalTestCase, self).setUp()

        from stalker import db, User
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret',
            created_by=self.admin
        )
        db.DBSession.add(self.test_user1)

        self.test_user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret',
            created_by=self.admin
        )
        db.DBSession.add(self.test_user2)

        self.test_user3 = User(
            name='Test User 3',
            login='tuser3',
            email='tuser3@users.com',
            password='secret',
            created_by=self.admin
        )
        db.DBSession.add(self.test_user3)

        from stalker import Department
        self.test_department1 = Department(
            name='Test Department 1',
            created_by=self.admin
        )
        db.DBSession.add(self.test_department1)

        self.test_department2 = Department(
            name='Test Department 2',
            created_by=self.admin
        )
        db.DBSession.add(self.test_department2)

        # create a couple of roles
        from stalker import Role
        self.test_role1 = Role(name='Test Role 1', created_by=self.admin)
        self.test_role2 = Role(name='Test Role 2', created_by=self.admin)
        self.test_role3 = Role(name='Test Role 3', created_by=self.admin)
        db.DBSession.add_all([
            self.test_role1, self.test_role2, self.test_role3
        ])
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if the GET: /api/departments/{id} view is working properly
        """
        response = self.test_app.get(
            '/api/departments/%s' % self.test_department1.id,
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
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    self.test_department1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    self.test_department1.date_updated
                ),
                'description': '',
                'entity_type': 'Department',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_department1.id,
                    'length': 0
                },
                'id': self.test_department1.id,
                'name': 'Test Department 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' %
                            self.test_department1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_department1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'user_roles': {
                    '$ref': '/api/departments/%s/user_roles' %
                            self.test_department1.id,
                    'length': 0
                },
                'users': {
                    '$ref': '/api/departments/%s/users' %
                            self.test_department1.id,
                    'length': 0
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if the GET: /api/departments is working properly
        """
        response = self.test_app.get(
            '/api/departments',
            status=200
        )

        from stalker import Department
        all_deps = Department.query.all()
        self.assertEqual(
            sorted(response.json_body),
            [{
                'id': d.id,
                'name': d.name,
                '$ref': '/api/departments/%s' % d.id,
                'entity_type': d.entity_type
            } for d in all_deps]
        )

    def test_update_entity_is_working_properly_witch_patch(self):
        """testing if the PATCH: /api/departments/{id} view is working properly
        """
        self.admin_login()
        new_name = 'New Department Name'
        new_description = 'New Description'
        response = self.test_app.patch(
            '/api/departments/%s' % self.test_department1.id,
            params={
                'name': new_name,
                'description': new_description,
                'user_id': [self.test_user1.id, self.test_user2.id]
            },
            status=200
        )

        from stalker import Department
        test_department1_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(test_department1_db.name, new_name)
        self.assertEqual(test_department1_db.description, new_description)
        self.assertEqual(
            sorted(test_department1_db.users),
            sorted([self.test_user1, self.test_user2])
        )

    def test_update_entity_is_working_properly_witch_post(self):
        """testing if the POST: /api/departments/{id} view is working properly
        """
        self.admin_login()
        new_name = 'New Department Name'
        new_description = 'New Description'
        response = self.test_app.post(
            '/api/departments/%s' % self.test_department1.id,
            params={
                'name': new_name,
                'description': new_description,
                'user_id': [self.test_user1.id, self.test_user2.id]
            },
            status=200
        )

        from stalker import Department
        test_department1_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(test_department1_db.name, new_name)
        self.assertEqual(test_department1_db.description, new_description)
        self.assertEqual(
            sorted(test_department1_db.users),
            sorted([self.test_user1, self.test_user2])
        )

    def test_create_entity_is_working_properly(self):
        """testing if the PUT: /api/departments view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/departments',
            params={
                'name': 'New Department',
                'description': 'New department description',
                'user_id': [self.test_user1.id, self.test_user2.id],
            },
            status=201
        )

        from stalker import Department
        new_dep = Department.query\
            .filter(Department.name == 'New Department')\
            .first()

        from stalker_pyramid2.views import EntityViewBase
        import stalker

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        new_dep.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        new_dep.date_updated
                    ),
                'description': 'New department description',
                'entity_type': 'Department',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_dep.id,
                    'length': 0
                },
                'id': new_dep.id,
                'name': 'New Department',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_dep.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % new_dep.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    'name': 'admin',
                    '$ref': '/api/users/%s' % self.admin.id,
                    'entity_type': 'User'
                },
                'user_roles': {
                    '$ref': '/api/departments/%s/user_roles' % new_dep.id,
                    'length': 2
                },
                'users': {
                    '$ref': '/api/departments/%s/users' % new_dep.id,
                    'length': 2
                },
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if the DELETE: /api/departments/{id} view is working
        properly
        """
        response = self.test_app.delete(
            '/api/departments/%s' % self.test_department1.id,
            status=200
        )

        from stalker import Department
        dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()
        self.assertIsNone(dep_db)

    def test_get_users_is_working_properly(self):
        """testing if the GET: /api/departments/{id}/users view is working
        properly
        """
        self.test_department1.users = [self.test_user1, self.test_user2]
        from stalker import db
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/departments/%s/users' % self.test_department1.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': u.id,
                    'name': u.name,
                    '$ref': '/api/users/%s' % u.id,
                    'entity_type': 'User'
                } for u in [self.test_user1, self.test_user2]
            ])
        )

    def test_update_users_is_working_properly_with_patch(self):
        """testing if PATCH: /api/departments/{id}/users view is working
        properly with PATCH
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = [self.test_user1]
        db.DBSession.commit()

        response = self.test_app.patch(
            '/api/departments/%s/users' % self.test_department1.id,
            params={
                'user_id': [self.test_user2.id, self.test_user3.id]
            },
            status=200
        )

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user1, self.test_user2, self.test_user3])
        )

    def test_update_users_is_working_properly_with_post(self):
        """testing if POST: /api/departments/{id}/users view is working
        properly with POST
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = [self.test_user1]
        db.DBSession.commit()

        response = self.test_app.post(
            '/api/departments/%s/users' % self.test_department1.id,
            params={
                'user_id': [self.test_user2.id, self.test_user3.id]
            },
            status=200
        )

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user2, self.test_user3])
        )

    def test_remove_users_is_working_properly(self):
        """testing if DELETE: /api/departments/{id}/users view is working
        properly
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = \
            [self.test_user1, self.test_user2, self.test_user3]
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/departments/%s/users?user_id=%s&user_id=%s' % (
                self.test_department1.id,
                self.test_user2.id,
                self.test_user3.id
            ),
            status=200
        )

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user1])
        )

    def test_remove_users_is_working_properly_with_non_related_user(self):
        """testing if DELETE: /api/departments/{id}/users is working properly
        with users that is not related to the department
        """
        from stalker import db
        # add some users first to see if patching works
        self.test_department1.users = \
            [self.test_user1, self.test_user2]
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/departments/%s/users?user_id=%s&user_id=%s' % (
                self.test_department1.id,
                self.test_user2.id,
                self.test_user3.id
            ),
            status=200
        )

        from stalker import Department
        test_dep_db = Department.query\
            .filter(Department.id == self.test_department1.id)\
            .first()

        self.assertEqual(
            sorted(test_dep_db.users),
            sorted([self.test_user1])
        )

    def test_get_department_user_roles_is_working_properly(self):
        """testing if the GEt: /api/departments/{id}/user_roles view is working
        properly
        """
        self.test_department1.users = [self.test_user1, self.test_user2]
        from stalker import db
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/departments/%s/user_roles' % self.test_department1.id,
            status=200
        )

        from stalker import DepartmentUser
        all_dep_users = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .all()

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'user': {
                        'id': du.user.id,
                        'name': du.user.name,
                        'entity_type': du.user.entity_type,
                        '$ref': '/api/users/%s' % du.user.id
                    },
                    'role': {
                        'id': du.role.id,
                        'name': du.role.name,
                        'entity_type': du.role.entity_type,
                        '$ref': '/api/roles/%s' % du.role.id
                    } if du.role else None
                } for du in all_dep_users
            ])
        )

    def test_update_user_roles_is_working_properly_with_patch(self):
        """testing if PATCH: /api/departments/{id}/user_roles view is working
        properly with PATCH
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        response = self.test_app.patch(
            '/api/departments/%s/user_roles' % self.test_department1.id,
            params={
                'user_role': [
                    '%s,%s' % (self.test_user1.id, self.test_role2.id),
                    '%s,%s' % (self.test_user2.id, self.test_role3.id),
                ]
            },
            status=200
        )

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertEqual(du1_db.role, self.test_role2)
        self.assertEqual(du2_db.role, self.test_role3)

    def test_update_user_roles_is_working_properly_with_post(self):
        """testing if POST: /api/departments/{id}/user_roles view is working
        properly with POST
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        response = self.test_app.post(
            '/api/departments/%s/user_roles' % self.test_department1.id,
            params={
                'user_role': [
                    '%s,%s' % (self.test_user1.id, self.test_role2.id),
                    '%s,%s' % (self.test_user2.id, self.test_role3.id),
                ]
            },
            status=200
        )

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertEqual(du1_db.role, self.test_role2)
        self.assertEqual(du2_db.role, self.test_role3)

    def test_update_user_roles_is_working_properly_with_non_related_user(self):
        """testing if POST: /api/departments/{id}/user_roles view is working
        properly with non related user
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        response = self.test_app.post(
            '/api/departments/%s/user_roles' % self.test_department1.id,
            params={
                'user_role': [
                    '%s,%s' % (self.test_user1.id, self.test_role2.id),
                    '%s,%s' % (self.test_user2.id, self.test_role3.id),
                    '%s,%s' % (self.test_user3.id, self.test_role1.id)
                ]
            },
            status=200
        )

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertEqual(du1_db.role, self.test_role2)
        self.assertEqual(du2_db.role, self.test_role3)

    def test_remove_user_roles_is_working_properly(self):
        """testing if DELETE: /api/departments/{id}/user_roles view is working
        properly
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        response = self.test_app.delete(
            '/api/departments/%s/user_roles?user_id=%s&user_id=%s' % (
                self.test_department1.id, self.test_user1.id,
                self.test_user2.id),
            status=200
        )

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertIsNone(du1_db.role)
        self.assertIsNone(du2_db.role)

    def test_remove_user_roles_is_working_properly_with_non_related_user(self):
        """testing if DELETE: /api/departments/%s/user_roles view is working
        properly with non related user
        """
        from stalker import db, DepartmentUser
        # create a role for the user
        du1 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user1,
            role=self.test_role1
        )
        db.DBSession.add(du1)
        db.DBSession.commit()

        du2 = DepartmentUser(
            department=self.test_department1,
            user=self.test_user2,
            role=self.test_role1
        )
        db.DBSession.add(du2)
        db.DBSession.commit()

        # now update the user role to something new
        response = self.test_app.delete(
            '/api/departments/%s/user_roles?user_id=%s&user_id=%s'
            '&user_id=%s' % (
                self.test_department1.id, self.test_user1.id,
                self.test_user2.id, self.test_user3.id),
            status=200
        )

        du1_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user1)\
            .first()

        du2_db = DepartmentUser.query\
            .filter(DepartmentUser.department == self.test_department1)\
            .filter(DepartmentUser.user == self.test_user2)\
            .first()

        self.assertIsNone(du1_db.role)
        self.assertIsNone(du2_db.role)
