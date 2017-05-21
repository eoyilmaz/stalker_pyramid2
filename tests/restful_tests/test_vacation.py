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
from stalker_pyramid.views import vacation


class VacationViewsUnitTestCase(UnitTestBase):
    """unit tests for Vacation views
    """

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22)
        end = datetime.datetime(2016, 4, 23)

        # get admin
        admin = User.query.filter(User.login == 'admin').first()

        vac1 = Vacation(
            user=user1,
            start=start,
            end=end,
            created_by=admin,
        )
        db.DBSession.add(vac1)
        db.DBSession.commit()

        # get the id
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = vac1.id

        vacation_views = vacation.VacationViews(request)
        response = vacation_views.get_entity()

        from stalker_pyramid.views import EntityViewBase
        import stalker
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': vac1.created_by.id,
                    '$ref': '/api/users/%s' % vac1.created_by.id,
                    'name': vac1.created_by.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(vac1.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(vac1.date_updated),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(vac1.end),
                'entity_type': 'Vacation',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % vac1.id,
                    'length': 0
                },
                'id': vac1.id,
                'name': vac1.name,
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(vac1.start),
                'thumbnail': None,
                'type': None,
                'user': {
                    'id': vac1.user.id,
                    '$ref': '/api/users/%s' % vac1.user.id,
                    'name': vac1.user.name,
                    'entity_type': 'User'
                },
                'updated_by': {
                    'id': vac1.updated_by.id,
                    '$ref': '/api/users/%s' % vac1.updated_by.id,
                    'name': vac1.updated_by.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(user2)

        admin = User.query.filter(User.login == 'admin').first()

        import datetime
        vac1 = Vacation(
            user=user1,
            start=datetime.datetime(2016, 4, 22),
            end=datetime.datetime(2016, 4, 23),
            created_by=admin
        )
        db.DBSession.add(vac1)

        vac2 = Vacation(
            user=user1,
            start=datetime.datetime(2016, 4, 24),
            end=datetime.datetime(2016, 4, 25),
            created_by=admin
        )
        db.DBSession.add(vac2)

        vac3 = Vacation(
            user=user2,
            start=datetime.datetime(2016, 4, 10),
            end=datetime.datetime(2016, 4, 12),
            created_by=admin
        )
        db.DBSession.add(vac3)

        vac4 = Vacation(
            user=user2,
            start=datetime.datetime(2016, 4, 13),
            end=datetime.datetime(2016, 4, 20),
            created_by=admin
        )
        db.DBSession.add(vac4)

        db.DBSession.commit()

        # get the id
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()
        vac2 = Vacation.query.filter(Vacation.name == vac2.name).first()
        vac3 = Vacation.query.filter(Vacation.name == vac3.name).first()
        vac4 = Vacation.query.filter(Vacation.name == vac4.name).first()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()

        vacation_views = vacation.VacationViews(request)
        response = vacation_views.get_entities()

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': v.id,
                    '$ref': '/api/vacations/%s' % v.id,
                    'name': v.name,
                    'entity_type': 'Vacation'
                } for v in [vac1, vac2, vac3, vac4]
            ]
        )

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.flush()

        import transaction
        transaction.commit()

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        user1 = User.query.filter(User.login == user1.login).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        from stalker_pyramid.views import EntityViewBase
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['user_id'] = user1.id
        request.params['start'] = \
            EntityViewBase.milliseconds_since_epoch(start)
        request.params['end'] = EntityViewBase.milliseconds_since_epoch(end)

        self.patch_logged_in_user(request)
        vacation_views = vacation.VacationViews(request)
        response = vacation_views.create_entity()

        vac = Vacation.query.filter(Vacation.user == user1).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user1)

        import stalker
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
                    EntityViewBase.milliseconds_since_epoch(vac.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(vac.date_created),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(vac.end),
                'entity_type': 'Vacation',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % vac.id,
                    'length': 0
                },
                'generic_text': '',
                'id': vac.id,
                'name': vac.name,
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(vac.start),
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'user': {
                    'id': vac.user_id,
                    '$ref': '/api/users/%s' % vac.user_id,
                    'name': vac.user.name,
                    'entity_type': 'User'
                }
            }
        )

    def test_create_entity_with_missing_user_id(self):
        """testing if create_entity() method is working properly with missing
        user_id parameter
        """
        from stalker import db, User
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        from stalker_pyramid.views import EntityViewBase
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['start'] = \
            EntityViewBase.milliseconds_since_epoch(start)
        request.params['end'] = EntityViewBase.milliseconds_since_epoch(end)

        vacation_views = vacation.VacationViews(request)
        from pyramid.httpexceptions import HTTPServerError
        with self.assertRaises(HTTPServerError) as cm:
            vacation_views.create_entity()

        self.assertEqual(
            str(cm.exception),
            'Missing "user_id" parameter'
        )

    def test_create_entity_with_invalid_user_id(self):
        """testing if create_entity() method is working properly with invalid
        user_id parameter
        """
        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        from stalker_pyramid.views import EntityViewBase
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['user_id'] = -1
        request.params['start'] = \
            EntityViewBase.milliseconds_since_epoch(start)
        request.params['end'] = EntityViewBase.milliseconds_since_epoch(end)

        vacation_views = vacation.VacationViews(request)
        from pyramid.httpexceptions import HTTPServerError
        with self.assertRaises(HTTPServerError) as cm:
            vacation_views.create_entity()

        self.assertEqual(
            str(cm.exception),
            'Missing "user_id" parameter'
        )

    def test_create_entity_with_missing_start(self):
        """testing if create_entity() method is working properly with missing
        start parameter
        """
        from stalker import db, User
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        import datetime
        end = datetime.datetime(2016, 4, 22, 16)
        user1 = User.query.filter(User.login == user1.login).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        from stalker_pyramid.views import EntityViewBase
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['user_id'] = user1.id
        request.params['end'] = EntityViewBase.milliseconds_since_epoch(end)

        vacation_views = vacation.VacationViews(request)

        from pyramid.httpexceptions import HTTPServerError
        with self.assertRaises(HTTPServerError) as cm:
            vacation_views.create_entity()

        self.assertEqual(
            str(cm.exception),
            'Missing "start" parameter'
        )

    def test_create_entity_with_missing_end(self):
        """testing if create_entity() method is working properly with missing
        end parameter
        """
        from stalker import db, User
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        user1 = User.query.filter(User.login == user1.login).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        from stalker_pyramid.views import EntityViewBase
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['user_id'] = user1.id
        request.params['start'] = \
            EntityViewBase.milliseconds_since_epoch(start)

        vacation_views = vacation.VacationViews(request)

        from pyramid.httpexceptions import HTTPServerError
        with self.assertRaises(HTTPServerError) as cm:
            vacation_views.create_entity()

        self.assertEqual(
            str(cm.exception),
            'Missing "end" parameter'
        )

    def test_update_entity_change_user(self):
        """testing if update_entity() method is working properly for changing
        user attribute
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(user2)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        user2 = User.query.filter(User.login == user2.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()
        # also update updated_by_id attribute

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = vac1.id

        request.params = DummyMultiDict()

        # change user
        request.params['user_id'] = user2.id
        request.params['updated_by_id'] = user2.id

        self.patch_logged_in_user(request)
        vacation_views = vacation.VacationViews(request)
        vacation_views.update_entity()

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user2)
        self.assertEqual(vac.updated_by, user2)

    def test_update_entity_change_start(self):
        """testing if update_entity() method is working properly for changing
        the start attribute
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        new_start = datetime.datetime(2016, 4, 22, 11)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        user1 = User.query.filter(User.login == user1.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = vac1.id

        request.params = DummyMultiDict()

        # change start
        from stalker_pyramid.views import EntityViewBase
        request.params['start'] = \
            EntityViewBase.milliseconds_since_epoch(new_start)

        self.patch_logged_in_user(request)
        vacation_views = vacation.VacationViews(request)
        vacation_views.update_entity()

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, new_start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user1)

    def test_update_entity_change_end(self):
        """testing if update_entity() method is working properly for changing
        end attribute
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        new_end = datetime.datetime(2016, 4, 22, 17)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        user1 = User.query.filter(User.login == user1.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = vac1.id

        request.params = DummyMultiDict()

        # change start
        from stalker_pyramid.views import EntityViewBase
        request.params['end'] = \
            EntityViewBase.milliseconds_since_epoch(new_end)

        self.patch_logged_in_user(request)
        vacation_views = vacation.VacationViews(request)
        vacation_views.update_entity()

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, new_end)
        self.assertEqual(vac.user, user1)

    def test_delete_entity(self):
        """testing if delete_entity() method is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = vac1.id

        vacation_views = vacation.VacationViews(request)
        vacation_views.delete_entity()

        vac = Vacation.query.filter(Vacation.name == vac1.name).all()
        self.assertEqual(vac, [])


class VacationViewFunctionalTestCase(FunctionalTestBase):
    """functional tests for Vacation views
    """

    def test_get_entity_is_working_properly(self):
        """test if GET: /api/vacation/{id} view is working properly
        """
        # login as admin
        self.admin_login()

        # create a vacation instance
        from stalker import db, User, Vacation
        user = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user)

        admin = User.query.filter(User.login == 'admin').first()

        import datetime
        vac = Vacation(
            user=user,
            start=datetime.datetime(2016, 4, 22, 10, 0),
            end=datetime.datetime(2016, 4, 24, 10, 0),
            created_by=admin
        )
        db.DBSession.add(vac)
        db.DBSession.commit()

        response = self.test_app.get('/api/vacations/%s' % vac.id)
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        import stalker
        self.assertEqual(
            response.json,
            {
                'created_by': {
                    'id': admin.id,
                    '$ref': '/api/users/%s' % admin.id,
                    'name': admin.name,
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(vac.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(vac.date_created),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(vac.end),
                'entity_type': 'Vacation',
                'id': vac.id,
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % vac.id,
                    'length': 0
                },
                'name': vac.name,
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(vac.start),
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': admin.id,
                    '$ref': '/api/users/%s' % admin.id,
                    'name': admin.name,
                    'entity_type': 'User'
                },
                'user': {
                    'id': vac.user_id,
                    '$ref': '/api/users/%s' % vac.user_id,
                    'name': vac.user.name,
                    'entity_type': 'User'
                }
            }
        )

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/vacations view is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        user1 = User.query.filter(User.login == user1.login).first()

        from stalker_pyramid.views import EntityViewBase

        self.admin_login()
        response = self.test_app.put(
            '/api/vacations',
            params={
                'user_id': user1.id,
                'start': EntityViewBase.milliseconds_since_epoch(start),
                'end': EntityViewBase.milliseconds_since_epoch(end),
            },
            status=201
        )

        vac = Vacation.query.filter(Vacation.user == user1).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user1)

        import stalker
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
                    EntityViewBase.milliseconds_since_epoch(vac.date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(vac.date_created),
                'description': '',
                'end': EntityViewBase.milliseconds_since_epoch(vac.end),
                'entity_type': 'Vacation',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % vac.id,
                    'length': 0
                },
                'generic_text': '',
                'id': vac.id,
                'name': vac.name,
                'stalker_version': stalker.__version__,
                'start': EntityViewBase.milliseconds_since_epoch(vac.start),
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
                'user': {
                    'id': vac.user_id,
                    '$ref': '/api/users/%s' % vac.user_id,
                    'name': vac.user.name,
                    'entity_type': 'User'
                }
            }
        )

    def test_create_entity_missing_user_id(self):
        """testing if PUT: /api/vacations view with missing user_id parameter
        """
        from stalker import db, User
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)

        from stalker_pyramid.views import EntityViewBase
        response = self.test_app.put(
            '/api/vacations',
            params={
                'start': EntityViewBase.milliseconds_since_epoch(start),
                'end': EntityViewBase.milliseconds_since_epoch(end),
            },
            status=500
        )

        self.assertEqual(
            response.body,
            'Server Error: Missing "user_id" parameter'
        )

    def test_create_entity_invalid_user_id(self):
        """testing if PUT: /api/vacations view with invalid user_id parameter
        """
        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)

        from stalker_pyramid.views import EntityViewBase
        response = self.test_app.put(
            '/api/vacations',
            params={
                'user_id': -1,
                'start': EntityViewBase.milliseconds_since_epoch(start),
                'end': EntityViewBase.milliseconds_since_epoch(end)
            },
            status=500
        )
        self.assertEqual(
            response.body,
            'Server Error: Missing "user_id" parameter'
        )

    def test_create_entity_missing_start(self):
        """testing if PUT: /api/vacations view with missing start parameter
        """
        from stalker import db, User
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        import datetime
        end = datetime.datetime(2016, 4, 22, 16)
        user1 = User.query.filter(User.login == user1.login).first()

        from stalker_pyramid.views import EntityViewBase
        self.admin_login()
        response = self.test_app.put(
            '/api/vacations',
            params={
                'user_id': user1.id,
                'end': EntityViewBase.milliseconds_since_epoch(end)
            },
            status=500
        )

        self.assertEqual(
            str(response.body),
            'Server Error: Missing "start" parameter'
        )

    def test_create_entity_missing_end(self):
        """testing if PUT: /api/vacations view with missing end parameter
        """
        from stalker import db, User
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)
        db.DBSession.commit()

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        user1 = User.query.filter(User.login == user1.login).first()

        from stalker_pyramid.views import EntityViewBase
        self.admin_login()
        response = self.test_app.put(
            '/api/vacations',
            params={
                'user_id': user1.id,
                'start': EntityViewBase.milliseconds_since_epoch(start)
            },
            status=500
        )

        self.assertEqual(
            str(response.body),
            'Server Error: Missing "end" parameter'
        )

    def test_update_entity_change_user_with_patch(self):
        """testing if PATCH: /api/vacations/{id}?user_id={value} is working
        properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(user2)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        user2 = User.query.filter(User.login == user2.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()
        # also update updated_by_id attribute

        resposne = self.test_app.patch(
            '/api/vacations/%s' % vac1.id,
            params={
                'user_id': user2.id,
                'updated_by_id': user2.id
            }
        )

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user2)
        self.assertEqual(vac.updated_by, user2)

    def test_update_entity_change_user_with_post(self):
        """testing if POST: /api/vacations/{id}?user_id={value} is working
        properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        user2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@users.com',
            password='secret'
        )
        db.DBSession.add(user2)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        user2 = User.query.filter(User.login == user2.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()
        # also update updated_by_id attribute

        response = self.test_app.post(
            '/api/vacations/%s' % vac1.id,
            params={
                'user_id': user2.id,
                'updated_by_id': user2.id
            }
        )

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user2)
        self.assertEqual(vac.updated_by, user2)

    def test_update_entity_change_start_with_patch(self):
        """testing if PATCH: /api/vacations/{id}?start={value}
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        new_start = datetime.datetime(2016, 4, 22, 11)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        user1 = User.query.filter(User.login == user1.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.views import EntityViewBase
        self.admin_login()
        self.test_app.patch(
            '/api/vacations/%s' % vac1.id,
            params={
                'start': EntityViewBase.milliseconds_since_epoch(new_start)
            },
            status=200
        )

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, new_start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user1)

    def test_update_entity_change_start_with_post(self):
        """testing POSt: /api/vacations/{id}?start={value}
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        new_start = datetime.datetime(2016, 4, 22, 11)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        user1 = User.query.filter(User.login == user1.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.views import EntityViewBase
        self.admin_login()
        self.test_app.post(
            '/api/vacations/%s' % vac1.id,
            params={
                'start': EntityViewBase.milliseconds_since_epoch(new_start)
            },
            status=200
        )

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, new_start)
        self.assertEqual(vac.end, end)
        self.assertEqual(vac.user, user1)

    def test_update_entity_change_end_with_patch(self):
        """testing PATCH: /api/vacations/{id}?end={value} is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        new_end = datetime.datetime(2016, 4, 22, 17)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )
        db.DBSession.commit()

        user1 = User.query.filter(User.login == user1.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.views import EntityViewBase
        self.admin_login()
        self.test_app.patch(
            '/api/vacations/%s' % vac1.id,
            params={
                'end': EntityViewBase.milliseconds_since_epoch(new_end)
            },
            status=200
        )

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, new_end)
        self.assertEqual(vac.user, user1)

    def test_update_entity_change_end_with_post(self):
        """testing POST: /api/vacations/{id}?end={value} is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        new_end = datetime.datetime(2016, 4, 22, 17)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )
        db.DBSession.commit()

        user1 = User.query.filter(User.login == user1.login).first()
        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        from stalker_pyramid.views import EntityViewBase
        self.admin_login()
        self.test_app.patch(
            '/api/vacations/%s' % vac1.id,
            params={
                'end': EntityViewBase.milliseconds_since_epoch(new_end)
            },
            status=200
        )

        vac = Vacation.query.filter(Vacation.name == vac1.name).first()
        self.assertEqual(vac.start, start)
        self.assertEqual(vac.end, new_end)
        self.assertEqual(vac.user, user1)

    def test_delete_entity_is_working_properly(self):
        """testing if DELETE: /api/vacations/{id} view is working properly
        """
        from stalker import db, User, Vacation
        user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(user1)

        import datetime
        start = datetime.datetime(2016, 4, 22, 10)
        end = datetime.datetime(2016, 4, 22, 16)
        vac1 = Vacation(
            user=user1,
            start=start,
            end=end
        )

        db.DBSession.commit()

        vac1 = Vacation.query.filter(Vacation.name == vac1.name).first()

        self.test_app.delete(
            '/api/vacations/%s' % vac1.id,
            status=200
        )

        vac = Vacation.query.filter(Vacation.name == vac1.name).all()
        self.assertEqual(vac, [])
