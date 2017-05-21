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
from stalker_pyramid.views import user
from stalker_pyramid.testing import UnitTestBase, FunctionalTestBase


# TODO: User testing_securitypolicy() to isolate the authentication process.


class UserViewsUnitTestCase(UnitTestBase):
    """unit tests for the User views
    """

    def setUp(self):
        """setup test
        """
        super(UserViewsUnitTestCase, self).setUp()

        # get the admin
        import datetime
        from stalker import User
        self.admin = User.query.filter(User.login == 'admin').first()
        # update the date_created to a known value
        self.admin.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.admin.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        # create departments
        from stalker import Department
        self.test_dep1 = Department(
            name='Test Department 1',
            created_by=self.admin,
        )

        self.test_dep2 = Department(
            name='Test Department 2',
            created_by=self.admin,
        )

        self.test_dep3 = Department(
            name='Test Department 3',
            created_by=self.admin,
        )

        # create groups
        from stalker import Group
        self.test_group1 = Group(
            name='Test Group 1',
            created_by=self.admin,
        )

        self.test_group2 = Group(
            name='Test Group 2',
            created_by=self.admin,
        )

        # create test users
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@test.com',
            password='secret',
            departments=[self.test_dep1],
            groups=[self.test_group1],
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
            departments=[self.test_dep1],
            groups=[self.test_group1],
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
            departments=[self.test_dep2, self.test_dep3],
            groups=[self.test_group1, self.test_group2],
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
            self.test_dep1, self.test_dep2, self.test_dep3,
            self.test_user1, self.test_user2, self.test_user3,
            self.test_status1, self.test_status2, self.test_status_list,
            self.test_repo, self.test_project1, self.test_project2
        ])

        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing get_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        user_view = user.UserViews(request)
        response = user_view.get_entity()

        import stalker
        expected_result = {
            'created_by': {
                'id': self.admin.id,
                '$ref': '/api/users/%s' % self.admin.id,
                'name': self.admin.name,
                'entity_type': 'User'
            },
            'date_created': 1459252800000L,
            'date_updated': 1459252800000L,
            'departments': {
                '$ref': '/api/users/%s/departments' % self.test_user1.id,
                'length': 1
            },
            'description': '',
            'email': 'tuser1@test.com',
            'entity_type': 'User',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        self.test_user1.id,
                'length': 0
            },
            'generic_text': '',
            'groups': {
                '$ref': '/api/users/%s/groups' % self.test_user1.id,
                'length': 1
            },
            'id': self.test_user1.id,
            'login': 'tuser1',
            'name': 'Test User 1',
            'notes': {
                '$ref': '/api/entities/%s/notes' % self.test_user1.id,
                'length': 0
            },
            'open_tickets': {
                '$ref': '/api/users/%s/tickets?status=open' %
                        self.test_user1.id,
                'length': 0
            },
            'pending_reviews': {
                '$ref': '/api/users/%s/reviews?status=new' %
                        self.test_user1.id,
                'length': 0
            },
            'projects': {
                '$ref': '/api/users/%s/projects' % self.test_user1.id,
                'length': 1
            },
            'rate': self.test_user1.rate,
            'reviews': {
                '$ref': '/api/users/%s/reviews' % self.test_user1.id,
                'length': 0
            },
            'stalker_version': stalker.__version__,
            'tags': {
                '$ref': '/api/entities/%s/tags' % self.test_user1.id,
                'length': 0
            },
            'tasks': {
                '$ref': '/api/users/%s/tasks' % self.test_user1.id,
                'length': 0
            },
            'thumbnail': None,
            'tickets': {
                '$ref': '/api/users/%s/tickets' % self.test_user1.id,
                'length': 0
            },
            'type': None,
            'updated_by': {
                'id': self.admin.id,
                '$ref': '/api/users/%s' % self.admin.id,
                'name': self.admin.name,
                'entity_type': 'User'
            },
            'vacations': {
                '$ref': '/api/users/%s/vacations' % self.test_user1.id,
                'length': 0
            },
        }

        self.maxDiff = None
        self.assertEqual(response.json_body, expected_result)

    def test_get_entities_is_working_properly(self):
        """testing if UserViews.get_entities() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        user_view = user.UserViews(request)
        response = user_view.get_entities()

        expected_result = [
            {
                'id': 3,
                '$ref': '/api/users/3',
                'name': 'admin',
                'entity_type': 'User'
            },
            {
                'id': self.test_user1.id,
                '$ref': '/api/users/%s' % self.test_user1.id,
                'name': self.test_user1.name,
                'entity_type': 'User'
            },
            {
                'id': self.test_user2.id,
                '$ref': '/api/users/%s' % self.test_user2.id,
                'name': self.test_user2.name,
                'entity_type': 'User'
            },
            {
                'id': self.test_user3.id,
                '$ref': '/api/users/%s' % self.test_user3.id,
                'name': self.test_user3.name,
                'entity_type': 'User'
            },
        ]

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(expected_result)
        )

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()

        request.params['login'] = 'testuser4'
        request.params['name'] = 'Test User 4'
        request.params['password'] = '12345'
        request.params['email'] = 'testuser4@test.com'

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.create_entity()

        import stalker
        from stalker import User
        created_user = User.query.filter(User.login == 'testuser4').first()
        from stalker_pyramid.views import EntityViewBase

        expected_result = {
            'created_by': {
                'id': self.admin.id,
                '$ref': '/api/users/%s' % self.admin.id,
                'name': self.admin.name,
                'entity_type': 'User'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(
                    created_user.date_created
                ),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(
                    created_user.date_updated
                ),
            'departments': {
                '$ref': '/api/users/%s/departments' % created_user.id,
                'length': 0
            },
            'description': '',
            'email': 'testuser4@test.com',
            'entity_type': 'User',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        created_user.id,
                'length': 0
            },
            'groups': {
                '$ref': '/api/users/%s/groups' % created_user.id,
                'length': 0
            },
            'id': created_user.id,
            'login': 'testuser4',
            'name': 'Test User 4',
            'notes': {
                '$ref': '/api/entities/%s/notes' % created_user.id,
                'length': 0
            },
            'open_tickets': {
                '$ref': '/api/users/%s/tickets?status=open' % created_user.id,
                'length': 0
            },
            'pending_reviews': {
                '$ref': '/api/users/%s/reviews?status=new' % created_user.id,
                'length': 0
            },
            'projects': {
                '$ref': '/api/users/%s/projects' % created_user.id,
                'length': 0
            },
            'rate': created_user.rate,
            'reviews': {
                '$ref': '/api/users/%s/reviews' % created_user.id,
                'length': 0
            },
            'stalker_version': stalker.__version__,
            'tags': {
                '$ref': '/api/entities/%s/tags' % created_user.id,
                'length': 0
            },
            'tasks': {
                '$ref': '/api/users/%s/tasks' % created_user.id,
                'length': 0
            },
            'thumbnail': None,
            'tickets': {
                '$ref': '/api/users/%s/tickets' % created_user.id,
                'length': 0
            },
            'type': None,
            'updated_by': {
                'id': self.admin.id,
                '$ref': '/api/users/%s' % self.admin.id,
                'name': self.admin.name,
                'entity_type': 'User'
            },
            'vacations': {
                '$ref': '/api/users/%s/vacations' % created_user.id,
                'length': 0
            },
        }

        self.maxDiff = None
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json_body, expected_result)

    def test_create_entity_with_non_available_login(self):
        """testing create_entity() method with non available login
        """

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()

        request.params['login'] = self.test_user3.login
        request.params['name'] = 'Test User 4'
        request.params['password'] = '12345'
        request.params['email'] = 'testuser4@test.com'

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.create_entity()
        self.assertEqual(
            response.body,
            'Login not available: %s' % self.test_user3.login
        )
        self.assertEqual(
            response.status_code,
            500
        )

    def test_create_entity_with_non_available_email(self):
        """testing create_entity() method with non available login
        """

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()

        request.params['login'] = 'tuser4'
        request.params['name'] = 'Test User 4'
        request.params['password'] = '12345'
        request.params['email'] = self.test_user3.email

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.create_entity()
        self.assertEqual(
            response.body,
            'Email not available: %s' % self.test_user3.email
        )
        self.assertEqual(
            response.status_code,
            500
        )

    def test_update_entity_name_is_working_properly(self):
        """testing if UserViews.update_entity() method is working properly
        with only updating the ``name`` parameter
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()
        test_value = 'Test User 1 new Name'
        request.params['name'] = test_value

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)
        user_view.update_entity()

        # get the user back from database
        # and check the name
        from stalker import User
        test_user = User.query.filter(User.id == self.test_user1.id).first()
        self.assertEqual(test_user.name, test_value)

    def test_update_entity_with_login_parameter(self):
        """testing if UserViews.update_entity() method is working properly for
        updating login parameter
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()

        test_value = 'testuser1newlogin'
        request.params['login'] = test_value

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)
        user_view.update_entity()

        # get the user back from database
        # and check the login
        from stalker import User
        test_user = User.query.filter(User.id == self.test_user1.id).first()
        self.assertEqual(test_user.login, test_value)

    def test_update_user_login_with_not_available_login_name(self):
        """testing if update_user view is working properly for updating login
        with an already present one
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()

        test_value = self.test_user2.login
        request.params['login'] = test_value

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        # with self.assertRaises(HTTPServerError) as cm:
        response = user_view.update_entity()
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 500)

        # get the user back from database
        # and check the login is intact
        from stalker import User
        test_user = User.query.filter(User.id == self.test_user1.id).first()
        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.login, self.test_user1.login)

    def test_update_entity_with_email_param_is_working_properly(self):
        """testing if UserViews.update_entity() method is working properly for
        updating email
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()

        test_value = 'testuser1_new_email@users.com'
        request.params['email'] = test_value

        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.update_entity()
        self.assertIsNone(response)

        # get the user back from database
        # and check the email
        from stalker import User
        test_user = User.query.filter(User.id == self.test_user1.id).first()
        self.assertEqual(test_user.email, test_value)

    def test_update_entity_with_email_with_bad_format(self):
        """testing if UserViews.update_entity() method is working properly for
        updating email with a malformed email address
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()

        test_value = 'testuser1_new_email'
        request.params['email'] = test_value

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)
        response = user_view.update_entity()

        self.assertEqual(
            response.status_code,
            500
        )

        self.assertEqual(
            str(response.body),
            'check the formatting of User.email, there is no @ sign'
        )

        # get the user back from database
        # and check the email is intact
        from stalker import User
        test_user = User.query.filter(User.id == self.test_user1.id).first()
        self.assertEqual(test_user.email, self.test_user1.email)

    def test_update_entity_with_password_parameter(self):
        """testing if UserViews.update_entity() method is working properly for
        updating password
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()

        test_value = 'newpassword'
        request.params['password'] = test_value

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.update_entity()
        self.assertIsNone(response)

        # get the user back from database
        # and check the email
        from stalker import User
        test_user = User.query.filter(User.id == self.test_user1.id).first()
        self.assertTrue(test_user.check_password(test_value))

    def test_update_entity_with_multiple_parameters(self):
        """testing if UserViews.update_entity() view is working properly for
        updating multiple parameters at once
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()

        test_login = 'testuser1newlogin'
        test_email = 'test_user1_new_email@users.com'
        test_password = 'testusernewpassword'
        test_name = 'Test User1 New Name'

        request.params['login'] = test_login
        request.params['email'] = test_email
        request.params['name'] = test_name
        request.params['password'] = test_password
        request.params['updated_by_id'] = self.test_user3.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.update_entity()
        self.assertIsNone(response)

        # get the user back from database
        # and check the email
        from stalker import User
        test_user = User.query.filter(User.id == self.test_user1.id).first()
        self.assertEqual(test_user.name, test_name)
        self.assertEqual(test_user.login, test_login)
        self.assertEqual(test_user.email, test_email)
        self.assertTrue(test_user.check_password(test_password))
        self.assertEqual(test_user.updated_by, self.test_user3)

    def test_delete_enity_is_working_properly(self):
        """testing if UserViews.delete_entity() view is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()

        deleted_user_id = self.test_user1.id
        request.matchdict['id'] = deleted_user_id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.delete_entity()
        self.assertIsNone(response)

        # and check the database if test user1 is deleted
        from stalker import User
        self.assertIsNone(
            User.query.filter(User.id == deleted_user_id).first()
        )

    # DEPARTMENTS
    def test_get_departments(self):
        """testing getting user departments
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()

        request.matchdict['id'] = self.test_user1.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        user_view = user.UserViews(request)

        response = user_view.get_departments()

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': self.test_user1.departments[0].id,
                    '$ref': '/api/departments/%s' %
                            self.test_user1.departments[0].id,
                    'name': self.test_user1.departments[0].name,
                    'entity_type': 'Department'
                }
            ]
        )

    def test_get_departments_with_a_user_with_no_departments(self):
        """testing getting user departments for a user with no department
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # create a new user with no departments
        from stalker import User
        new_user = User(
            name='New User',
            login='newuser',
            password='1234',
            email='newuser@users.com'
        )
        import transaction
        from stalker import db
        db.DBSession.add(new_user)
        transaction.commit()

        # get the user id
        new_user = User.query.filter(User.login == 'newuser').first()

        request.matchdict['id'] = new_user.id
        self.assertIsNotNone(new_user.id)

        user_view = user.UserViews(request)

        response = user_view.get_departments()

        self.assertEqual(response.json_body, [])

    def test_update_departments_with_request_method_is_post(self):
        """testing update_departments() method with request method is POST
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # create a new department (with Python)
        from stalker import db, Department
        new_dep = Department(
            name='New Department'
        )
        db.DBSession.add(new_dep)
        # get the new_dep id
        new_dep = Department.query\
            .filter(Department.name == 'New Department').first()

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # and assign it to the new user (with RESTFull API)
        from stalker_pyramid.testing import DummyMultiDict
        request.method = 'POST'
        request.params = DummyMultiDict()
        request.params['dep_id[]'] = [self.test_dep1.id, new_dep.id]
        request.POST = request.params

        user_view = user.UserViews(request)

        response = user_view.update_departments()

        from stalker import User
        test_user1_db = \
            User.query.filter(User.id == self.test_user1.id).first()

        self.assertEqual(
            sorted(test_user1_db.departments),
            sorted([self.test_dep1, new_dep])
        )

    def test_remove_departments(self):
        """testing removing a department from the user
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # and assign it to the new user (with RESTFull API)
        request.method = 'DELETE'
        request.params = DummyMultiDict()
        request.params['dep_id[]'] = [self.test_dep1.id]
        request.POST = request.params

        user_view = user.UserViews(request)

        user_view.remove_departments()

        # get the user from database
        from stalker import User
        test_user1 = User.query.filter(User.id == self.test_user1.id).first()
        # check the departments
        self.assertEqual(test_user1.departments, [])

    def test_remove_departments_with_invalid_department(self):
        """testing remove_departments() will work silently when the given
        department is not in user.departments
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # and assign it to the new user (with RESTFull API)
        request.method = 'DELETE'
        request.params = DummyMultiDict()
        self.assertTrue(self.test_dep2 not in self.test_user1.departments)
        request.params['dep_id[]'] = [self.test_dep2.id]
        request.POST = request.params

        user_view = user.UserViews(request)

        user_view.remove_departments()

        # get the user from database
        from stalker import User
        test_user1 = User.query.filter(User.id == self.test_user2.id).first()
        # check the departments
        self.assertEqual(test_user1.departments, [self.test_dep1])

    # GROUPS
    def test_get_groups(self):
        """testing getting user groups
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user3.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # and assign it to the new user (with RESTFull API)
        request.method = 'GET'
        request.params = DummyMultiDict()

        user_view = user.UserViews(request)

        response = user_view.get_groups()

        self.assertTrue(
            sorted(response.json_body) == sorted([
                {
                    'id': self.test_group1.id,
                    '$ref': '/api/groups/%s' % self.test_group1.id,
                    'name': self.test_group1.name,
                    'entity_type': 'Group'
                },
                {
                    'id': self.test_group2.id,
                    '$ref': '/api/groups/%s' % self.test_group2.id,
                    'name': self.test_group2.name,
                    'entity_type': 'Group'
                }
            ])
        )

    def test_update_groups(self):
        """testing update_groups() is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()

        request.matchdict['id'] = self.test_user1.id

        # create a new group (with Python)
        from stalker import db, Group
        new_group = Group(
            name='New Group'
        )
        db.DBSession.add(new_group)
        # get the new_group id
        new_group = Group.query \
            .filter(Group.name == 'New Group').first()

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # and assign it to the new user (with RESTFull API)
        from stalker_pyramid.testing import DummyMultiDict
        request.method = 'POST'
        request.params = DummyMultiDict()
        request.params['group_id[]'] = [self.test_group1.id, new_group.id]
        request.POST = request.params

        user_view = user.UserViews(request)
        response = user_view.update_groups()

        # check user groups
        from stalker import User
        test_user1_db = User.query.get(self.test_user1.id)

        self.assertEqual(
            sorted(test_user1_db.groups),
            sorted([self.test_group1, new_group])
        )

    def test_remove_groups(self):
        """testing if remove_groups() is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        request.method = 'DELETE'
        request.params = DummyMultiDict()
        request.params['group_id[]'] = [self.test_group1.id]
        request.POST = request.params

        user_view = user.UserViews(request)

        user_view.remove_groups()

        # get the user from database
        from stalker import User
        test_user1 = User.query.filter(User.id == self.test_user1.id).first()
        # check the groups
        self.assertEqual(test_user1.groups, [])

    def test_remove_groups_with_invalid_group(self):
        """testing if remove_groups() will silently remove the group when
        the given group is not related to the user
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        request.method = 'DELETE'
        request.params = DummyMultiDict()
        self.assertTrue(self.test_group2 not in self.test_user1.groups)
        request.params['group_id[]'] = [self.test_group2.id]
        request.POST = request.params

        user_view = user.UserViews(request)

        user_view.remove_groups()

        # get the user from database
        from stalker import User
        test_user1 = User.query.filter(User.id == self.test_user1.id).first()
        # check the groups
        self.assertEqual(test_user1.groups, [self.test_group1])

    # PROJECTS
    def test_get_projects(self):
        """testing getting user projects
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user3.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # and assign it to the new user (with RESTFull API)
        request.method = 'GET'
        request.params = DummyMultiDict()

        user_view = user.UserViews(request)

        response = user_view.get_projects()

        self.assertTrue(
            sorted(response.json_body) == sorted([
                {
                    'id': self.test_project1.id,
                    '$ref': '/api/projects/%s' % self.test_project1.id,
                    'name': self.test_project1.name,
                    'entity_type': 'Project'
                },
                {
                    'id': self.test_project2.id,
                    '$ref': '/api/projects/%s' % self.test_project2.id,
                    'name': self.test_project2.name,
                    'entity_type': 'Project'
                }
            ])
        )

    def test_update_projects(self):
        """testing update_projects() is working properly
        """
        # create a new Project (with Python)
        from stalker import db, Project
        new_project = Project(
            name='New Project',
            code='NP',
            repositories=[self.test_repo]
        )
        db.DBSession.add(new_project)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        # and assign it to the new user (with RESTFull API)
        request.method = 'POST'
        request.params = DummyMultiDict()
        request.params['project_id[]'] = [self.test_project1.id,
                                          new_project.id]
        request.POST = request.params

        user_view = user.UserViews(request)
        response = user_view.update_projects()

        # check the user projects
        from stalker import User
        test_user1_db = User.query.get(self.test_user1.id)

        self.assertEqual(
            sorted(test_user1_db.projects),
            sorted([self.test_project1, new_project])
        )

    def test_remove_projects(self):
        """testing if remove_projects() is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user3.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        request.method = 'DELETE'
        request.params = DummyMultiDict()
        request.params['project_id[]'] = [self.test_project1.id]
        request.POST = request.params

        user_view = user.UserViews(request)

        user_view.remove_projects()

        # get the user from database
        from stalker import User
        test_user3 = User.query.filter(User.id == self.test_user3.id).first()
        # check the groups
        self.assertEqual(test_user3.projects, [self.test_project2])

    def test_remove_projects_with_invalid_project(self):
        """testing if remove_projects() will silently remove the projects
        even when the given user is not in the given project
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        request.method = 'DELETE'
        request.params = DummyMultiDict()
        # try to remove test_project2 which the user is not related to
        self.assertTrue(self.test_project2 not in self.test_user1.projects)
        request.params['project_id[]'] = [self.test_project2.id]
        request.POST = request.params

        user_view = user.UserViews(request)

        user_view.remove_projects()

        # get the user from database
        from stalker import User
        test_user1 = User.query.filter(User.id == self.test_user1.id).first()
        # check the groups
        self.assertEqual(test_user1.projects, [self.test_project1])

    # VACATIONS
    def test_get_vacations(self):
        """testing if get_vacations() is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        # create a couple of vacations for the self.test_user1
        from stalker import db, Vacation
        import datetime
        v1 = Vacation(
            user=self.test_user1,
            start=datetime.datetime(2016, 4, 3, 12, 0),
            end=datetime.datetime(2016, 4, 4, 12, 0)
        )
        v2 = Vacation(
            user=self.test_user1,
            start=datetime.datetime(2016, 4, 4, 12, 0),
            end=datetime.datetime(2016, 4, 5, 12, 0)
        )
        v3 = Vacation(
            user=self.test_user1,
            start=datetime.datetime(2016, 4, 5, 12, 0),
            end=datetime.datetime(2016, 4, 6, 12, 0)
        )

        # and a couple for other users
        v4 = Vacation(
            user=self.test_user2,
            start=datetime.datetime(2016, 4, 3, 12, 0),
            end=datetime.datetime(2016, 4, 4, 12, 0)
        )
        v5 = Vacation(
            user=self.test_user2,
            start=datetime.datetime(2016, 4, 4, 12, 0),
            end=datetime.datetime(2016, 4, 5, 12, 0)
        )
        v6 = Vacation(
            user=self.test_user2,
            start=datetime.datetime(2016, 4, 5, 12, 0),
            end=datetime.datetime(2016, 4, 6, 12, 0)
        )
        db.DBSession.add_all([v1, v2, v3, v4, v5, v6])
        db.DBSession.commit()

        # now request the data
        user_views = user.UserViews(request)
        response = user_views.get_vacations()

        v1 = Vacation.query.filter(Vacation.name == v1.name).first()
        v2 = Vacation.query.filter(Vacation.name == v2.name).first()
        v3 = Vacation.query.filter(Vacation.name == v3.name).first()

        expected = [
            {
                'id': v1.id,
                '$ref': '/api/vacations/%s' % v1.id,
                'name': v1.name,
                'entity_type': 'Vacation'
            },
            {
                'id': v2.id,
                '$ref': '/api/vacations/%s' % v2.id,
                'name': v2.name,
                'entity_type': 'Vacation'
            },
            {
                'id': v3.id,
                '$ref': '/api/vacations/%s' % v3.id,
                'name': v3.name,
                'entity_type': 'Vacation'
            },
        ]
        self.assertTrue(sorted(response.json_body) == sorted(expected))

    # TASKS
    def test_get_tasks_is_working_properly(self):
        """testing if the get_tasks() view is working properly
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        user_views = user.UserViews(request)
        response = user_views.get_tasks()

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t1, t2, t3]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_get_tasks_with_as_parameter_is_resource_is_working_properly(self):
        """testing if the get_tasks() will return the tasks that the user
        is a resource of when the "as" parameter is set to "resource"
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.method = 'GET'
        request.params['as'] = 'resource'

        user_views = user.UserViews(request)
        response = user_views.get_tasks()

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t1, t2, t3]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_get_tasks_responsible_is_working_properly(self):
        """testing if the get_tasks_responsible() will return the tasks that
        the user is a responsible of
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.method = 'GET'

        user_views = user.UserViews(request)
        response = user_views.get_tasks_responsible()

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t4, t5, t6]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_get_tasks_watched_is_working_properly(self):
        """testing if the get_tasks_watched() will return the tasks that the
        user is a watcher of
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.method = 'GET'

        user_views = user.UserViews(request)
        response = user_views.get_tasks_watched()

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t11, t12, t13, t14]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_remove_tasks_is_working_properly(self):
        """testing if the remove_tasks() will remove the user from the tasks
        that the user is a resource of when the "as" parameter is not given
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.method = 'DELETE'

        t1 = Task.query.filter(Task.name == t1.name).first()
        request.params = DummyMultiDict()
        request.params['task_id'] = [t1.id]
        request.POST = request.params

        user_views = user.UserViews(request)
        response = user_views.remove_tasks()

        expected = [t2, t3]

        from stalker import Task
        result = Task.query\
            .filter(Task.resources.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_silently_work_when_non_related_task_is_given(self):
        """testing if the remove_tasks() will silently continue its job when
        the user is not a resource to the given task when the "as" parameter is
        not given
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.method = 'DELETE'

        t1 = Task.query.filter(Task.name == t1.name).first()
        t4 = Task.query.filter(Task.name == t4.name).first()

        request.params = DummyMultiDict()
        request.params['task_id'] = [t1.id, t4.id]
        request.POST = request.params

        user_views = user.UserViews(request)
        response = user_views.remove_tasks()

        expected = [t2, t3]

        from stalker import Task
        result = Task.query\
            .filter(Task.resources.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_remove_with_the_as_parameter_is_resource(self):
        """testing if the remove_tasks() will remove the user from the
        resources list of the task when the "as" parameter is resource
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        t = Task.query.filter(Task.name == t1.name).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.method = 'DELETE'
        request.params['as'] = 'resource'
        request.params = DummyMultiDict()
        request.params['task_id'] = [t.id]
        request.POST = request.params

        user_views = user.UserViews(request)
        response = user_views.remove_tasks()

        expected = [t2, t3]

        from stalker import Task
        result = Task.query \
            .filter(Task.resources.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_remove_with_the_as_parameter_is_responsible(self):
        """testing if the remove_tasks() will remove the user from the
        responsible list of the task when the "as" parameter is responsible
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        t = Task.query.filter(Task.name == t4.name).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()
        request.params['as'] = 'responsible'
        request.params['task_id'] = [t.id]
        request.method = 'DELETE'
        request.POST = request.params

        user_views = user.UserViews(request)
        response = user_views.remove_tasks()

        expected = [t5, t6]

        from stalker import Task
        result = Task.query \
            .filter(Task.responsible.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_remove_with_the_as_parameter_is_watcher(self):
        """testing if the remove_tasks() will remove the user from the
        watchers list of the task when the "as" parameter is watcher
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        t = Task.query.filter(Task.name == t13.name).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params = DummyMultiDict()
        request.params['as'] = 'watcher'
        request.params['task_id'] = [t.id]
        request.method = 'DELETE'
        request.POST = request.params

        user_views = user.UserViews(request)
        response = user_views.remove_tasks()

        expected = [t11, t12, t14]

        from stalker import Task
        result = Task.query \
            .filter(Task.watchers.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    # REVIEWS
    def test_get_reviews_is_working_properly(self):
        """testing if get_reviews() is working properly
        """
        import datetime
        from stalker import db, Task, TimeLog
        t1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user2],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t1)

        # create a time log for this task
        tlog1 = TimeLog(
            task=t1,
            resource=self.test_user2,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog1)

        t2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user3],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t2)

        # create a time log for this task
        tlog2 = TimeLog(
            task=t2,
            resource=self.test_user3,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog2)
        db.DBSession.commit()

        r1 = t1.request_review()
        r2 = t2.request_review()

        db.DBSession.commit()

        # get user reviews
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        user_views = user.UserViews(request)
        response = user_views.get_reviews()

        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [
                    {
                        'id': r.id,
                        '$ref': '/api/reviews/%s' % r.id,
                        'name': r.name,
                        'entity_type': r.entity_type
                    } for r in [r1[0], r2[0]]
                ]
            )
        )

    def test_get_reviews_for_pending_reviews_is_working_properly(self):
        """testing if get_reviews() will return only Pending reviews when the
        `status` parameter value is Pending
        """
        import datetime
        from stalker import db, Task, TimeLog
        t1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user2],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t1)

        # create a time log for this task
        tlog1 = TimeLog(
            task=t1,
            resource=self.test_user2,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog1)

        t2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user3],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t2)

        # create a time log for this task
        tlog2 = TimeLog(
            task=t2,
            resource=self.test_user3,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog2)
        db.DBSession.commit()

        r1 = t1.request_review()
        r2 = t2.request_review()

        # close r2
        r2[0].approve()
        db.DBSession.commit()

        # get user reviews
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id
        request.params['status'] = 'NEW'

        user_views = user.UserViews(request)
        response = user_views.get_reviews()

        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [
                    {
                        'id': r1[0].id,
                        '$ref': '/api/reviews/%s' % r1[0].id,
                        'name': r1[0].name,
                        'entity_type': r1[0].entity_type
                    }
                ]
            )
        )

    # TICKETS
    def test_get_tickets_is_working_properly(self):
        """testing if get_tickets() is working properly
        """
        # create a couple of tickets for test_user1
        from stalker import db, Ticket
        from stalker.models.ticket import FIXED

        # Ticket#1
        t1 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t1.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t1)

        # Ticket#2
        t2 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t2.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t2)

        # Ticket#3
        t3 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t3.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t3)

        # Ticket#4 to some other Projects
        t4 = Ticket(
            project=self.test_project2,
            created_by=self.admin
        )
        t4.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t4)

        # Ticket#5 to another user
        t5 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t5.reassign(created_by=self.admin, assign_to=self.test_user2)
        db.DBSession.add(t5)

        # and some closed tickets
        t6 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t6.reassign(created_by=self.admin, assign_to=self.test_user1)
        t6.resolve(created_by=self.test_user1, resolution=FIXED)
        db.DBSession.add(t6)

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        user_views = user.UserViews(request)
        response = user_views.get_tickets()

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    '$ref': '/api/tickets/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in [t1, t2, t3, t4, t6]
            ])
        )

    def test_get_tickets_for_open_tickets_is_working_properly(self):
        """testing if get_tickets() will return only Open tickets when the
        `status` parameter value is Open
        """
        # create a couple of tickets for test_user1
        from stalker import db, Ticket
        from stalker.models.ticket import FIXED

        # Ticket#1
        t1 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t1.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t1)

        # Ticket#2
        t2 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t2.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t2)

        # Ticket#3
        t3 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t3.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t3)

        # Ticket#4 to some other Projects
        t4 = Ticket(
            project=self.test_project2,
            created_by=self.admin
        )
        t4.reassign(created_by=self.admin, assign_to=self.test_user1)
        db.DBSession.add(t4)

        # Ticket#5 to another user
        t5 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t5.reassign(created_by=self.admin, assign_to=self.test_user2)
        db.DBSession.add(t5)

        # and some closed tickets
        t6 = Ticket(
            project=self.test_project1,
            created_by=self.admin
        )
        t6.reassign(created_by=self.admin, assign_to=self.test_user1)
        t6.resolve(created_by=self.test_user1, resolution=FIXED)
        db.DBSession.add(t6)

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        from stalker import Status
        status_closed = Status.query.filter(Status.code == 'CLS').first()
        request.params['status_id'] = '!%s' % status_closed.id

        user_views = user.UserViews(request)
        response = user_views.get_tickets()

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    '$ref': '/api/tickets/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in [t1, t2, t3, t4]
            ])
        )

    def test_check_availability_for_available_login(self):
        """testing check_availability() method for login parameter
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.params['login'] = 'new_login'
        user_view = user.UserViews(request)
        response = user_view.check_availability()
        self.assertTrue(response['login_available'])

    def test_check_availability_for_non_available_login(self):
        """testing check_availability() method for login parameter
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.params['login'] = self.test_user1.login
        user_view = user.UserViews(request)
        response = user_view.check_availability()
        self.assertFalse(response['login_available'])

    def test_check_availability_for_available_email(self):
        """testing check_availability() method for email parameter
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.params['email'] = 'available@users.com'
        user_view = user.UserViews(request)
        response = user_view.check_availability()
        self.assertTrue(response['email_available'])

    def test_check_availability_for_non_available_email(self):
        """testing check_availability() method for email parameter
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.params['email'] = self.test_user1.email
        user_view = user.UserViews(request)
        response = user_view.check_availability()
        self.assertFalse(response['email_available'])

    # TimeLogs
    def test_get_time_logs_is_working_properly(self):
        """testing if the get_time_logs() method is working properly
        """
        # create a Task
        from stalker import db, Task

        # task1
        test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            resources=[self.test_user1],
            schedule_timing=10,
            schedule_unit='h'
        )
        db.DBSession.add(test_task1)

        # task2
        test_task2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            resources=[self.test_user1],
            schedule_timing=10,
            schedule_unit='h'
        )
        db.DBSession.add(test_task2)
        db.DBSession.commit()

        # create time logs
        import datetime
        from stalker import TimeLog

        # time log 1
        t1 = TimeLog(
            resource=self.test_user1,
            task=test_task1,
            start=datetime.datetime(2016, 7, 27, 15),
            end=datetime.datetime(2016, 7, 27, 16)
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        # time log 2
        t2 = TimeLog(
            resource=self.test_user1,
            task=test_task1,
            start=datetime.datetime(2016, 7, 27, 16),
            end=datetime.datetime(2016, 7, 27, 17)
        )
        db.DBSession.add(t2)
        db.DBSession.commit()

        # now get the time logs
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_user1.id

        user_view = user.UserViews(request)
        response = user_view.get_time_logs()

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    'name': t.name,
                    '$ref': '/api/time_logs/%s' % t.id,
                    'entity_type': 'TimeLog'
                } for t in [t1, t2]
            ])
        )


class UserViewFunctionalTestCase(FunctionalTestBase):
    """functional tests for User views
    """

    def setUp(self):
        """set the test up
        """
        # run super setup
        super(UserViewFunctionalTestCase, self).setUp()

        # get the admin
        import datetime
        from stalker import User
        self.admin = User.query.filter(User.login == 'admin').first()
        # update the date_created to a known value
        self.admin.date_created = datetime.datetime(2016, 3, 29, 12, 0)
        self.admin.date_updated = datetime.datetime(2016, 3, 29, 12, 0)

        # create departments
        from stalker import Department
        self.test_dep1 = Department(
            name='Test Department 1',
            created_by=self.admin,
        )

        self.test_dep2 = Department(
            name='Test Department 2',
            created_by=self.admin,
        )

        self.test_dep3 = Department(
            name='Test Department 3',
            created_by=self.admin,
        )

        # create groups
        from stalker import Group
        self.test_group1 = Group(
            name='Test Group 1',
            created_by=self.admin,
        )

        self.test_group2 = Group(
            name='Test Group 2',
            created_by=self.admin,
        )

        # create test users
        self.test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@test.com',
            password='secret',
            departments=[self.test_dep1],
            groups=[self.test_group1],
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
            departments=[self.test_dep1],
            groups=[self.test_group1],
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
            departments=[self.test_dep2, self.test_dep3],
            groups=[self.test_group1, self.test_group2],
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
            self.test_dep1, self.test_dep2, self.test_dep3,
            self.test_user1, self.test_user2, self.test_user3,
            self.test_status1, self.test_status2, self.test_status_list,
            self.test_repo, self.test_project1, self.test_project2
        ])

        db.DBSession.flush()
        db.DBSession.commit()

    def test_user_login(self):
        """testing if login is successful
        """
        response = self.test_app.post(
            '/api/login',
            params={
                'login': 'admin',
                'password': 'admin'
            },
            status=200
        )

        import stalker
        from stalker_pyramid.views import EntityViewBase
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
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    self.admin.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    self.admin.date_updated
                ),
                'departments': {
                    '$ref': '/api/users/%s/departments' % self.admin.id,
                    'length': 1
                },
                'description': '',
                'email': self.admin.email,
                'entity_type': 'User',
                'id': self.admin.id,
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % self.admin.id,
                    'length': 0
                },
                'generic_text': '',
                'groups': {
                    '$ref': '/api/users/%s/groups' % self.admin.id,
                    'length': 1
                },
                'login': self.admin.login,
                'name': self.admin.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.admin.id,
                    'length': 0
                },
                'open_tickets': {
                    '$ref': '/api/users/%s/tickets?status=open' %
                            self.admin.id,
                    'length': 0
                },
                'pending_reviews': {
                    '$ref': '/api/users/%s/reviews?status=new' % self.admin.id,
                    'length': 0
                },
                'projects': {
                    '$ref': '/api/users/%s/projects' % self.admin.id,
                    'length': 0
                },
                'rate': self.admin.rate,
                'reviews': {
                    '$ref': '/api/users/%s/reviews' % self.admin.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.admin.id,
                    'length': 0
                },
                'tasks': {
                    '$ref': '/api/users/%s/tasks' % self.admin.id,
                    'length': 0
                },
                'tickets': {
                    '$ref': '/api/users/%s/tickets' % self.admin.id,
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
                'vacations': {
                    '$ref': '/api/users/%s/vacations' % self.admin.id,
                    'length': 0
                }
            }
        )

    def test_get_entity_is_working_properly(self):
        """testing GET: /api/users/{id} is working properly
        """
        # login as admin first
        self.admin_login()

        # get the admin from db
        import stalker
        from stalker import User
        admin = User.query.filter(User.login == 'admin').first()
        from stalker_pyramid.views import EntityViewBase

        res = self.test_app.get(
            '/api/users/3',
            status=200,
        )
        self.maxDiff = None
        self.assertEqual(
            res.json_body,
            {
                'id': 3,
                'created_by': {
                    'id': admin.id,
                    '$ref': '/api/users/%s' % admin.id,
                    'name': admin.name,
                    'entity_type': 'User'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    admin.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    admin.date_updated
                ),
                'departments': {
                    '$ref': '/api/users/3/departments',
                    'length': 1
                },
                'description': '',
                'email': 'admin@admin.com',
                'entity_type': 'User',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % admin.id,
                    'length': 0
                },
                'groups': {
                    '$ref': '/api/users/3/groups',
                    'length': 1
                },
                'login': 'admin',
                'name': 'admin',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % admin.id,
                    'length': 0
                },
                'open_tickets': {
                    '$ref': '/api/users/3/tickets?status=open',
                    'length': 0
                },
                'pending_reviews': {
                    '$ref': '/api/users/3/reviews?status=new',
                    'length': 0
                },
                'projects': {
                    '$ref': '/api/users/3/projects',
                    'length': 0
                },
                'rate': admin.rate,
                'reviews': {
                    '$ref': '/api/users/3/reviews',
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/3/tags',
                    'length': 0
                },
                'tasks': {
                    '$ref': '/api/users/3/tasks',
                    'length': 0
                },
                'tickets': {
                    '$ref': '/api/users/3/tickets',
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': admin.id,
                    '$ref': '/api/users/%s' % admin.id,
                    'name': admin.name,
                    'entity_type': 'User'
                },
                'vacations': {
                    '$ref': '/api/users/3/vacations',
                    'length': 0
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET:/api/users is working properly
        """
        # login as admin
        self.admin_login()
        # get admin user
        from stalker import User
        admin = User.query.filter(User.login == 'admin').first()

        response = self.test_app.get(
            '/api/users',
            status=200,
        )
        expected_result = [
            {
                'id': u.id,
                '$ref': '/api/users/%s' % u.id,
                'name': u.name,
                'entity_type': u.entity_type
            } for u in [self.admin, self.test_user1, self.test_user2,
                        self.test_user3]
        ]

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(expected_result)
        )

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/users is working properly
        """
        # login as admin first
        self.admin_login()
        res = self.test_app.put(
            '/api/users',
            params={
                'login': 'newuser1',
                'name': 'New User 1',
                'email': 'new_user@users.com',
                'password': 'secret'
            },
            status=201
        )
        # get newly created user from database
        import stalker
        from stalker import User
        new_user = User.query.filter(User.login == 'newuser1').first()
        admin = User.query.filter(User.login == 'admin').first()

        from stalker_pyramid.views import EntityViewBase

        self.maxDiff = None
        self.assertEqual(
            res.json_body,
            {
                'created_by': {
                    'id': admin.id,
                    '$ref': '/api/users/%s' % admin.id,
                    'name': admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        new_user.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        new_user.date_updated
                    ),
                'departments': {
                    '$ref': '/api/users/%s/departments' % new_user.id,
                    'length': 0
                },
                'description': '',
                'email': 'new_user@users.com',
                'entity_type': 'User',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_user.id,
                    'length': 0
                },
                'groups': {
                    '$ref': '/api/users/%s/groups' % new_user.id,
                    'length': 0
                },
                'id': new_user.id,
                'login': 'newuser1',
                'name': 'New User 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_user.id,
                    'length': 0
                },
                'open_tickets': {
                    '$ref': '/api/users/%s/tickets?status=open' % new_user.id,
                    'length': 0
                },
                'pending_reviews': {
                    '$ref': '/api/users/%s/reviews?status=new' % new_user.id,
                    'length': 0
                },
                'projects': {
                    '$ref': '/api/users/%s/projects' % new_user.id,
                    'length': 0
                },
                'rate': admin.rate,
                'reviews': {
                    '$ref': '/api/users/%s/reviews' % new_user.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % new_user.id,
                    'length': 0
                },
                'tasks': {
                    '$ref': '/api/users/%s/tasks' % new_user.id,
                    'length': 0
                },
                'thumbnail': None,
                'tickets': {
                    '$ref': '/api/users/%s/tickets' % new_user.id,
                    'length': 0
                },
                'type': None,
                'updated_by': {
                    'id': admin.id,
                    '$ref': '/api/users/%s' % admin.id,
                    'name': admin.name,
                    'entity_type': 'User'
                },
                'vacations': {
                    '$ref': '/api/users/%s/vacations' % new_user.id,
                    'length': 0
                },
            }
        )

    def test_create_entity_with_non_available_login(self):
        """testing PUT: /api/users view with non available login
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/users',
            params={
                'login': self.test_user1.login,
                'name': 'Test User 4',
                'password': '12345',
                'email': 'testuser4@test.com',
            },
            status=500,
        )

        self.assertEqual(
            response.body,
            'Login not available: %s' % self.test_user1.login
        )

    def test_create_entity_with_non_available_email(self):
        """testing PUT: /api/users view with non available email
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/users',
            params={
                'login': 'tuser4',
                'name': 'Test User 4',
                'password': '12345',
                'email': self.test_user1.email,
            },
            status=500,
        )

        self.assertEqual(
            response.body,
            'Email not available: %s' % self.test_user1.email
        )

    def test_update_entity_information_with_patch(self):
        """testing if PATCH:/api/users/{id} is working properly
        """
        # login as admin first
        self.admin_login()

        # now update user information
        test_value = 'New User new name'
        self.test_app.patch(
            '/api/users/%s' % self.test_user1.id,
            params={
                'name': test_value
            }
        )

        # check the database and see if the user is updated
        from stalker import User
        new_user_from_db = \
            User.query.filter(User.name == test_value).first()
        self.assertEqual(new_user_from_db.name, test_value)

    def test_update_entity_multiple_information_at_once_with_patch(self):
        """testing if PATCH:/api/users/{id} is working properly with multiple
        parameters at once
        """
        # login as admin first
        self.admin_login()

        # now update user information
        test_name = 'New User new name'
        test_pass = '12345'
        test_login = 'newusernewlogin'
        test_email = 'new_user_new_email@users.com'
        self.test_app.patch(
            '/api/users/%s' % self.test_user1.id,
            params={
                'name': test_name,
                'password': test_pass,
                'login': test_login,
                'email': test_email,
                'updated_by_id': self.test_user2.id
            },
            status=200
        )

        # check the database and see if the user is updated
        from stalker import User
        test_user1_db = \
            User.query.filter(User.name == test_name).first()

        self.assertEqual(test_user1_db.name, test_name)
        self.assertEqual(test_user1_db.login, test_login)
        self.assertEqual(test_user1_db.email, test_email)
        self.assertTrue(test_user1_db.check_password(test_pass))
        self.assertEqual(test_user1_db.updated_by, self.test_user2)

    def test_update_entity_with_patch_with_bad_formatted_email(self):
        """testing if PATCH: /api/users/{id} is working properly when the email
        formatting is not correct
        """
        # login as admin first
        self.admin_login()

        # now update user information
        test_name = 'New User new name'
        test_pass = '12345'
        test_login = 'newusernewlogin'
        test_email = 'new_user_new_email_users.com'
        response = self.test_app.patch(
            '/api/users/%s' % self.test_user1.id,
            params={
                'name': test_name,
                'password': test_pass,
                'login': test_login,
                'email': test_email,
                'updated_by_id': self.test_user2.id
            },
            status=500
        )
        self.assertEqual(
            response.body,
            'check the formatting of User.email, there is no @ sign'
        )

    def test_delete_user(self):
        """testing if delete user is working properly
        """
        # login as admin first
        self.admin_login()

        # create a new user in the database
        from stalker import db, User
        new_user = User(
            name='New User',
            login='newuser',
            email='newuser@userrs.com',
            password='secret'
        )
        db.DBSession.add(new_user)
        import transaction
        transaction.commit()

        # check if the user is created in the database
        new_user_from_db = \
            User.query.filter(User.name == new_user.name).first()
        self.assertIsNotNone(new_user_from_db)
        self.assertIsInstance(new_user_from_db, User)

        # now delete the user
        self.test_app.delete(
            '/api/users/%s' % new_user.id,
            status=200
        )

        # check the database
        new_user_from_db = \
            User.query.filter(User.name == new_user.name).first()
        self.assertIsNone(new_user_from_db)

    # DEPARTMENTS
    def test_get_departments_view_is_working_properly(self):
        """testing if GET /api/user/{id}departments view is working properly
        """
        # login as admin first
        self.admin_login()

        # get user departments
        # user1
        response = self.test_app.get(
            '/api/users/%s/departments' % self.test_user1.id,
            status=200
        )
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': self.test_dep1.id,
                    '$ref': '/api/departments/%s' % self.test_dep1.id,
                    'name': self.test_dep1.name,
                    'entity_type': 'Department'
                }
            ]
        )

        # user3
        response = self.test_app.get(
            '/api/users/%s/departments' % self.test_user3.id,
            status=200
        )
        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [
                    {
                        'id': d.id,
                        '$ref': '/api/departments/%s' % d.id,
                        'name': d.name,
                        'entity_type': 'Department'
                    } for d in [self.test_dep2, self.test_dep3]
                ]
            )
        )

    def test_patch_departments_view_is_working_properly(self):
        """testing if PATCH /api/user/{id}departments view is working properly
        """
        # login as admin first
        self.admin_login()

        # now get user departments
        self.test_app.patch(
            '/api/users/%s/departments?dep_id[]=%s' %
            (self.test_user1.id, self.test_dep2.id),
            status=200
        )

        # check if new_user1's department includes new_department2 also
        from stalker import User
        test_user1_db = \
            User.query.filter(User.login == self.test_user1.login).first()

        self.assertEqual(
            sorted([d.name for d in test_user1_db.departments]),
            sorted([self.test_dep1.name, self.test_dep2.name])
        )

    def test_put_departments_view_is_working_properly(self):
        """testing if PUT: /api/user/{id}departments view returns 404
        """
        # login as admin first
        self.admin_login()

        # now get user departments
        # user1
        self.test_app.put(
            '/api/users/%s/departments?dep_id[]=%s' %
            (self.test_user1.id, self.test_dep2.id),
            status=404
        )

    def test_post_departments_view_is_working_properly(self):
        """testing if POST: /api/user/{id}departments view is working properly
        """
        # login as admin first
        self.admin_login()

        # now get user departments
        # user1
        response = self.test_app.post(
            '/api/users/%s/departments?dep_id[]=%s' %
            (self.test_user1.id, self.test_dep2.id),
            status=200
        )

        # check if new_user1's department includes new_department2 also
        from stalker import User
        test_user1_db = \
            User.query.filter(User.login == self.test_user1.login).first()
        self.assertEqual(
            sorted([d.name for d in test_user1_db.departments]),
            sorted([self.test_dep2.name])
        )

    def test_delete_departments_view_is_working_properly(self):
        """testing if DELETE: /api/user/{id}departments view is working properly
        """
        # login as admin first
        self.admin_login()

        # now delete dep2 from user2
        # user1
        self.test_app.delete(
            '/api/users/%s/departments?dep_id[]=%s' % (
                self.test_user2.id,
                self.test_dep2.id
            ),
            status=200
        )

        # check if new_user2's departments doesn't include new_department2
        from stalker import User
        test_user2_db = \
            User.query.filter(User.login == self.test_user2.login).first()
        self.assertEqual(
            sorted([d.name for d in test_user2_db.departments]),
            sorted([self.test_dep1.name])
        )

    # GROUPS
    def test_get_groups_view_is_working_properly(self):
        """testing if the GET: /api/users/{id}/groups view is working properly
        """
        # login as admin
        self.admin_login()

        response = self.test_app.get(
            '/api/users/%s/groups' % self.test_user3.id,
            status=200
        )
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': g.id,
                    '$ref': '/api/groups/%s' % g.id,
                    'name': g.name,
                    'entity_type': 'Group'
                } for g in [self.test_group1, self.test_group2]
            ])
        )

    def test_patch_groups_view_is_working_properly(self):
        """testing if the PATCH: /api/user/{id}/groups view is working properly
        """
        # login as admin
        self.admin_login()

        self.test_app.patch(
            '/api/users/%s/groups?group_id[]=%s' %
                (self.test_user1.id, self.test_group2.id),
            status=200
        )

        # get user groups
        from stalker import User
        test_user1_db = \
            User.query.filter(User.login == self.test_user1.login).first()
        self.assertEqual(
            sorted(test_user1_db.groups),
            sorted([self.test_group1, self.test_group2])
        )

    def test_put_groups_view_is_working_properly(self):
        """testing if the PUT: /api/users/{id}/groups view returns 404
        """
        # login as admin
        self.admin_login()

        self.test_app.put(
            '/api/users/%s/groups?group_id[]=%s' %
            (self.test_user1.id, self.test_group2.id),
            status=404
        )

    def test_post_groups_view_is_working_properly(self):
        """testing if the POST: /api/users/{id}/groups view is working properly
        """
        # login as admin
        self.admin_login()

        response = self.test_app.post(
            '/api/users/%s/groups?group_id[]=%s' %
            (self.test_user1.id, self.test_group2.id),
            status=200
        )

        # get user groups
        from stalker import User
        test_user1_db = \
            User.query.filter(User.login == self.test_user1.login).first()
        self.assertEqual(
            sorted(test_user1_db.groups),
            sorted([self.test_group2])
        )

    def test_delete_groups_view_is_working_properly(self):
        """testing if the DELETE: /api/users/{id}/groups view is working
        properly
        """
        # login as admin
        self.admin_login()

        self.test_app.delete(
            '/api/users/%s/groups?group_id[]=%s' %
            (self.test_user1.id, self.test_group2.id),
            status=200
        )

        # get user groups
        from stalker import User
        test_user1_db = \
            User.query.filter(User.login == self.test_user1.login).first()
        self.assertEqual(
            sorted(test_user1_db.groups),
            sorted([self.test_group1])
        )

    # PROJECTS
    def test_get_projects_view_is_working_properly(self):
        """testing if the GET: /api/users/{id}/projects view is working
        properly
        """
        response = self.test_app.get(
            '/api/users/%s/projects' % self.test_user3.id,
            status=200
        )
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                    {
                        'id': p.id,
                        '$ref': '/api/projects/%s' % p.id,
                        'name': p.name,
                        'entity_type': 'Project'
                    } for p in [self.test_project1, self.test_project2]
                ]
            )
        )

    def test_patch_projects_view_is_working_properly(self):
        """testing if the PATCH: /api/users/{id}/projects view is working
        properly
        """
        self.test_app.patch(
            '/api/users/%s/projects?project_id[]=%s' %
            (self.test_user1.id, self.test_project2.id),
            status=200
        )

        from stalker import User
        user1 = User.query.filter(User.login == self.test_user1.login).first()
        self.assertEqual(
            sorted(user1.projects),
            sorted([self.test_project1, self.test_project2])
        )

    def test_put_projects_view_is_working_properly(self):
        """testing if the PUT: /api/users/{id}/projects view returns 404
        """
        self.test_app.put(
            '/api/users/%s/projects?project_id[]=%s' %
            (self.test_user1.id, self.test_project2.id),
            status=404
        )

        # and user.projects is intact
        from stalker import User
        user1 = User.query.filter(User.login == self.test_user1.login).first()
        self.assertEqual(
            sorted(user1.projects),
            sorted([self.test_project1])
        )

    def test_post_projects_view_is_working_properly(self):
        """testing if the POST: /api/users/{id}/projects view is working
        properly
        """
        response = self.test_app.post(
            '/api/users/%s/projects?project_id[]=%s&project_id[]=%s' %
            (self.test_user1.id, self.test_project1.id, self.test_project2.id),
            status=200
        )

        from stalker import User
        user1 = User.query.filter(User.login == self.test_user1.login).first()
        self.assertEqual(
            sorted(user1.projects),
            sorted([self.test_project1, self.test_project2])
        )

    def test_delete_projects_view_is_working_properly(self):
        """testing if the DELETE: /api/users/{id}/projects view is working
        properly
        """
        self.test_app.delete(
            '/api/users/%s/projects?project_id[]=%s' %
            (self.test_user3.id, self.test_project1.id),
            status=200
        )

        from stalker import User
        user3 = User.query.filter(User.login == self.test_user3.login).first()
        self.assertEqual(
            sorted(user3.projects),
            sorted([self.test_project2])
        )

    # VACATIONS
    def test_get_vacations_view_is_working_properly(self):
        """testing if GET: /api/users/{id}/vacations view is working properly
        """
        from stalker import db, Vacation
        import datetime
        vac1 = Vacation(
            user=self.test_user1,
            start=datetime.datetime(2016, 4, 24, 0, 0),
            end=datetime.datetime(2016, 4, 28, 0, 0)
        )

        vac2 = Vacation(
            user=self.test_user1,
            start=datetime.datetime(2016, 7, 1, 0, 0),
            end=datetime.datetime(2016, 7, 8, 0, 0)
        )
        db.DBSession.add_all([vac1, vac2])

        db.DBSession.flush()
        import transaction
        transaction.commit()

        from stalker import User
        user1 = User.query.filter(User.login == self.test_user1.login).first()
        response = self.test_app.get(
            '/api/users/%s/vacations' % self.test_user1.id
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': v.id,
                    '$ref': '/api/vacations/%s' % v.id,
                    'name': v.name,
                    'entity_type': v.entity_type
                } for v in [user1.vacations[0], user1.vacations[1]]
            ])
        )

    # TASKS
    def test_get_tasks_is_working_properly(self):
        """testing if the get_tasks() view is working properly
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # commit data
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/users/%s/tasks' % self.test_user1.id,
            status=200
        )

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t1, t2, t3]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_get_tasks_with_as_parameter_is_resource_is_working_properly(self):
        """testing if the GET: /api/users/{id}/tasks view will return the tasks
        that the user is a resource of when the "as" parameter is set to
        "resource"
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # commit data
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/users/%s/tasks' % self.test_user1.id,
            params={
                'as': 'resource'
            },
            status=200
        )

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t1, t2, t3]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_get_tasks_responsible_is_working_properly(self):
        """testing if the GET: /api/users/{id}/tasks view will return the tasks
        that the user is a responsible of when the "as" parameter is set to
        "responsible"
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # commit data
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/users/%s/tasks_responsible' % self.test_user1.id,
            status=200
        )

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t4, t5, t6]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_get_tasks_watcher_is_working_properly(self):
        """testing if the GET: /api/users/{id}/tasks_watched view will return
        the tasks that the user is a watcher of
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/users/%s/tasks_watched' % self.test_user1.id,
            status=200,
        )

        expected = [
            {
                'id': t.id,
                '$ref': '/api/tasks/%s' % t.id,
                'name': t.name,
                'entity_type': t.entity_type
            } for t in [t11, t12, t13, t14]
        ]

        self.assertEqual(sorted(response.json_body), sorted(expected))

    def test_remove_tasks_is_working_properly(self):
        """testing if the DELETE: /api/users/{id}/tasks view will remove the
        user from the tasks that the user is a resource of when the "as"
        parameter is not given
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/users/%s/tasks?task_id=%s' % (self.test_user1.id, t1.id),
            status=200
        )

        expected = [t2, t3]
        result = Task.query\
            .filter(Task.resources.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_silently_work_when_non_related_task_is_given(self):
        """testing if the DELETE: /api/users/{id}/tasks view will silently
        continue its job when the user is not a resource to the given task when
        the "as" parameter is not given
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/users/%s/tasks?task_id=%s&task_id=%s' % (
                self.test_user1.id, t1.id, t4.id
            ),
            status=200
        )

        expected = [t2, t3]

        from stalker import Task
        result = Task.query\
            .filter(Task.resources.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_remove_with_the_as_parameter_is_resource(self):
        """testing if the DELETE: /api/users/{id}/tasks view will remove the
        user from the resources list of the task when the "as" parameter is
        "resource"
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/users/%s/tasks?as=resource&task_id=%s' % (
                self.test_user1.id, t1.id
            ),
            status=200
        )
        expected = [t2, t3]

        from stalker import Task
        result = Task.query \
            .filter(Task.resources.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_remove_with_the_as_parameter_is_responsible(self):
        """testing if the DElETE: /api/users/{id}/tasks will remove the user
        from the responsible list of the task when the "as" parameter is
        "responsible"
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        response = self.test_app.delete(
            '/api/users/%s/tasks?as=responsible&task_id=%s' %
            (self.test_user1.id, t4.id),
            status=200
        )
        expected = [t5, t6]

        from stalker import Task
        result = Task.query \
            .filter(Task.responsible.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    def test_remove_tasks_will_remove_with_the_as_parameter_is_watcher(self):
        """testing if the DELETE: /api/users/{id}/tasks view will remove the
        user from the watchers list of the task when the "as" parameter is
        "watcher"
        """
        # create a couple of tasks
        from stalker import db, Task

        # tasks
        # as resource
        t1 = Task(
            name='T1',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t1)

        t2 = Task(
            name='T2',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t2)

        t3 = Task(
            name='T3',
            project=self.test_project1,
            resources=[self.test_user1],
            responsible=[self.test_user2]
        )
        db.DBSession.add(t3)

        # as responsible
        t4 = Task(
            name='T4',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t4)

        t5 = Task(
            name='T5',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t5)

        t6 = Task(
            name='T6',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user1]
        )
        db.DBSession.add(t6)

        # non related
        t7 = Task(
            name='T7',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t7)

        t8 = Task(
            name='T8',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t8)

        t9 = Task(
            name='T9',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t9)

        t10 = Task(
            name='T10',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3]
        )
        db.DBSession.add(t10)

        # as watcher
        t11 = Task(
            name='T11',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t11)

        t12 = Task(
            name='T12',
            project=self.test_project1,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1],
        )
        db.DBSession.add(t12)

        t13 = Task(
            name='T13',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user3],
        )
        db.DBSession.add(t13)

        t14 = Task(
            name='T14',
            project=self.test_project2,
            resources=[self.test_user2],
            responsible=[self.test_user3],
            watchers=[self.test_user1, self.test_user2],
        )
        db.DBSession.add(t14)

        # commit data
        db.DBSession.commit()

        # t = Task.query.filter(Task.name == t13.name).first()

        response = self.test_app.delete(
            '/api/users/%s/tasks?as=watcher&task_id=%s' %
            (self.test_user1.id, t13.id),
            status=200
        )
        expected = [t11, t12, t14]

        from stalker import Task
        result = Task.query \
            .filter(Task.watchers.contains(self.test_user1)).all()

        self.assertEqual(sorted(result), sorted(expected))

    # REVIEWS
    def test_get_reviews_view_is_working_properly(self):
        """testing if GET: /api/users/{id}/reviews view is working properly
        """
        import datetime
        from stalker import db, Task, TimeLog
        t1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user2],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t1)

        # create a time log for this task
        tlog1 = TimeLog(
            task=t1,
            resource=self.test_user2,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog1)

        t2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user3],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t2)

        # create a time log for this task
        tlog2 = TimeLog(
            task=t2,
            resource=self.test_user3,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog2)

        import transaction
        transaction.commit()

        r1 = t1.request_review()
        r2 = t2.request_review()

        transaction.commit()

        # get user reviews
        response = self.test_app.get(
            '/api/users/%s/reviews' % self.test_user1.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [
                    {
                        'id': r.id,
                        '$ref': '/api/reviews/%s' % r.id,
                        'name': r.name,
                        'entity_type': r.entity_type
                    } for r in [r1[0], r2[0]]
                ]
            )
        )

    def test_get_reviews_for_pending_reviews_is_working_properly(self):
        """testing if GET: /api/users/{id}/reviews will return only Pending
        reviews when the "status" parameter value is "NEW"
        """
        from stalker import db, Task
        t1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user2],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t1)

        # create a time log for this task
        import datetime
        from stalker import TimeLog
        tlog1 = TimeLog(
            task=t1,
            resource=self.test_user2,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog1)

        t2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            responsible=[self.test_user1],
            resources=[self.test_user3],
            schedule_timing=3,
            schedule_unit='h',
        )
        db.DBSession.add(t2)

        # create a time log for this task
        tlog2 = TimeLog(
            task=t2,
            resource=self.test_user3,
            start=datetime.datetime(2016, 5, 13, 10),
            end=datetime.datetime(2016, 5, 13, 11)
        )
        db.DBSession.add(tlog2)
        db.DBSession.commit()

        r1 = t1.request_review()
        r2 = t2.request_review()

        # close r2
        r2[0].approve()
        db.DBSession.commit()

        # get user reviews
        response = self.test_app.get(
            '/api/users/%s/reviews?status=new' % self.test_user1.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [
                    {
                        'id': r1[0].id,
                        '$ref': '/api/reviews/%s' % r1[0].id,
                        'name': r1[0].name,
                        'entity_type': r1[0].entity_type
                    }
                ]
            )
        )

    # TICKETS
    def test_get_tickets_is_working_properly(self):
        """testing if GET: /api/users/{id}/tickets view is working properly
        """
        # create a couple of tickets for test_user1
        from stalker import db, Ticket
        from stalker.models.ticket import FIXED

        # Ticket#1
        t1 = Ticket(
            project=self.test_project1,
            created_by=self.test_user2
        )
        t1.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t1)

        # Ticket#2
        t2 = Ticket(
            project=self.test_project1,
            created_by=self.test_user2
        )
        t2.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t2)

        # Ticket#3
        t3 = Ticket(
            project=self.test_project1,
            created_by=self.test_user2
        )
        t3.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t3)

        # Ticket#4 to some other Projects
        t4 = Ticket(
            project=self.test_project2,
            created_by=self.test_user2
        )
        t4.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t4)

        # Ticket#5 to another user
        t5 = Ticket(
            project=self.test_project1,
            created_by=self.test_user3
        )
        t5.reassign(created_by=self.test_user3, assign_to=self.test_user2)
        db.DBSession.add(t5)

        # and some closed tickets
        t6 = Ticket(
            project=self.test_project1,
            created_by=self.test_user3
        )
        t6.reassign(created_by=self.test_user3, assign_to=self.test_user1)
        t6.resolve(created_by=self.test_user1, resolution=FIXED)
        db.DBSession.add(t6)

        response = self.test_app.get(
            '/api/users/%s/tickets' % self.test_user1.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    '$ref': '/api/tickets/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in [t1, t2, t3, t4, t6]
            ])
        )

    def test_get_tickets_for_open_tickets_is_working_properly(self):
        """testing if GET: /api/users/{id}/tickets will return only Open
        tickets when the "status" parameter value is "Open"
        """
        # create a couple of tickets for test_user1
        from stalker import db, Ticket
        from stalker.models.ticket import FIXED

        # Ticket#1
        t1 = Ticket(
            project=self.test_project1,
            created_by=self.test_user2
        )
        t1.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t1)

        # Ticket#2
        t2 = Ticket(
            project=self.test_project1,
            created_by=self.test_user2
        )
        t2.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t2)

        # Ticket#3
        t3 = Ticket(
            project=self.test_project1,
            created_by=self.test_user2
        )
        t3.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t3)

        # Ticket#4 to some other Projects
        t4 = Ticket(
            project=self.test_project2,
            created_by=self.test_user2
        )
        t4.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        db.DBSession.add(t4)

        # Ticket#5 to another user
        t5 = Ticket(
            project=self.test_project1,
            created_by=self.test_user3
        )
        t5.reassign(created_by=self.test_user3, assign_to=self.test_user2)
        db.DBSession.add(t5)

        # and some closed tickets
        t6 = Ticket(
            project=self.test_project1,
            created_by=self.test_user2
        )
        t6.reassign(created_by=self.test_user2, assign_to=self.test_user1)
        t6.resolve(created_by=self.test_user1, resolution=FIXED)
        db.DBSession.add(t6)

        from stalker import Status
        status_closed = Status.query.filter(Status.code == 'CLS').first()
        response = self.test_app.get(
            '/api/users/%s/tickets?status_id=!%s' % (
                self.test_user1.id, status_closed.id
            ),
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    '$ref': '/api/tickets/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in [t1, t2, t3, t4]
            ])
        )

    def test_check_availability_for_available_login(self):
        """testing GET: /api/check_availability view is working properly with
        login parameter
        """
        response = self.test_app.get(
            '/api/check_availability',
            params={
                'login': 'new_login'
            },
            status=200
        )
        self.assertTrue(response.json_body['login_available'])

    def test_check_availability_for_non_available_login(self):
        """testing GET: /api/check_availability view is working properly with
        login parameter
        """
        response = self.test_app.get(
            '/api/check_availability',
            params={
                'login': self.test_user1.login
            },
            status=200
        )
        self.assertFalse(response.json_body['login_available'])

    def test_check_availability_for_available_email(self):
        """testing check_availability() method for email parameter
        """
        response = self.test_app.get(
            '/api/check_availability',
            params={
                'email': 'available@users.com'
            },
            status=200
        )
        self.assertTrue(response.json_body['email_available'])

    def test_check_availability_for_non_available_email(self):
        """testing check_availability() method for email parameter
        """
        response = self.test_app.get(
            '/api/check_availability',
            params={
                'email': self.test_user1.email,
            },
            status=200,
        )
        self.assertFalse(response.json_body['email_available'])

    # TimeLogs
    def test_get_time_logs_is_working_properly(self):
        """testing if the get_time_logs() method is working properly
        """
        # create a Task
        from stalker import db, Task

        # task1
        test_task1 = Task(
            name='Test Task 1',
            project=self.test_project1,
            resources=[self.test_user1],
            schedule_timing=10,
            schedule_unit='h'
        )
        db.DBSession.add(test_task1)

        # task2
        test_task2 = Task(
            name='Test Task 2',
            project=self.test_project1,
            resources=[self.test_user1],
            schedule_timing=10,
            schedule_unit='h'
        )
        db.DBSession.add(test_task2)
        db.DBSession.commit()

        # create time logs
        import datetime
        from stalker import TimeLog

        # time log 1
        t1 = TimeLog(
            resource=self.test_user1,
            task=test_task1,
            start=datetime.datetime(2016, 7, 27, 15),
            end=datetime.datetime(2016, 7, 27, 16)
        )
        db.DBSession.add(t1)
        db.DBSession.commit()

        # time log 2
        t2 = TimeLog(
            resource=self.test_user1,
            task=test_task1,
            start=datetime.datetime(2016, 7, 27, 16),
            end=datetime.datetime(2016, 7, 27, 17)
        )
        db.DBSession.add(t2)
        db.DBSession.commit()

        # now get the time logs
        response = self.test_app.get(
            '/api/users/%s/time_logs' % self.test_user1.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': t.id,
                    'name': t.name,
                    '$ref': '/api/time_logs/%s' % t.id,
                    'entity_type': 'TimeLog'
                } for t in [t1, t2]
            ])
        )