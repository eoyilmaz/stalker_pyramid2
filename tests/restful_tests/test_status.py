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
from stalker_pyramid2.views import status


class StatusViewsUnitTestCase(UnitTestBase):
    """unit tests for the Status views
    """

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker import db, Status
        test_status1 = Status(
            name='Test Status 1',
            code='TST1',
            created_by=self.admin
        )
        db.DBSession.add(test_status1)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_status1.id

        status_view = status.StatusViews(request)
        response = status_view.get_entity()

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
                'code': 'TST1',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status1.date_updated
                    ),
                'description': '',
                'entity_type': 'Status',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_status1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': test_status1.id,
                'name': 'Test Status 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_status1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_status1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker import db, Status
        test_status1 = Status(name='Test Entity 1', code='TST1')
        test_status2 = Status(name='Test Entity 2', code='TST2')
        test_status3 = Status(name='Test Entity 3', code='TST3')
        db.DBSession.add_all([test_status1, test_status2, test_status3])
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()

        status_view = status.StatusViews(request)
        response = status_view.get_entities()

        all_statuses = Status.query.all()

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': s.id,
                    '$ref': '/api/statuses/%s' % s.id,
                    'name': s.name,
                    'entity_type': s.entity_type
                } for s in all_statuses])
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() is working properly
        """
        from stalker import db, Status
        test_status1 = Status(name='Test Status 1', code='TST1')
        db.DBSession.add(test_status1)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.matchdict['id'] = test_status1.id
        self.patch_logged_in_user(request)

        new_name = 'New Status Name'
        new_code = 'NSN'
        new_description = 'This should also be present'

        request.params['name'] = new_name
        request.params['code'] = new_code
        request.params['description'] = new_description

        status_view = status.StatusViews(request)
        response = status_view.update_entity()

        test_status1_db = Status.query.get(test_status1.id)
        self.assertEqual(test_status1_db.name, new_name)
        self.assertEqual(test_status1_db.code, new_code)
        self.assertEqual(test_status1_db.description, new_description)

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()

        name = 'New Status Name'
        code = 'NSN'
        description = 'This should also be present'
        created_by_id = 3

        request.params['name'] = name
        request.params['code'] = code
        request.params['description'] = description
        request.params['created_by_id'] = created_by_id

        status_view = status.StatusViews(request)
        response = status_view.create_entity()

        from stalker import Status
        new_status = Status.query.filter(Status.code == code).first()

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'code': code,
                'created_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        new_status.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        new_status.date_updated
                    ),
                'description': description,
                'entity_type': 'Status',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_status.id,
                    'length': 0
                },
                'generic_text': '',
                'id': new_status.id,
                'name': name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_status.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % new_status.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker import db, Status
        test_status = Status(name='Test Status', code='TST')
        db.DBSession.add(test_status)
        db.DBSession.commit()

        self.assertIsNotNone(Status.query.filter(Status.code == 'TST').first())

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_status.id

        status_view = status.StatusViews(request)
        status_view.delete_entity()

        self.assertIsNone(Status.query.filter(Status.code == 'TST').first())


class StatusViewsFunctionalTestCase(FunctionalTestBase):
    """unit tests for the Status views
    """

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/status/{id} view is working properly
        """
        from stalker import db, Status
        test_status1 = Status(
            name='Test Status 1',
            code='TST1',
            created_by=self.admin
        )
        db.DBSession.add(test_status1)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/statuses/%s' % test_status1.id,
            status=200
        )

        import stalker
        from stalker_pyramid2.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
                'code': 'TST1',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status1.date_updated
                    ),
                'description': '',
                'entity_type': 'Status',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_status1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': test_status1.id,
                'name': 'Test Status 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_status1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_status1.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET: /api/statuses view is working properly
        """
        from stalker import db, Status
        test_status1 = Status(name='Test Entity 1', code='TST1')
        test_status2 = Status(name='Test Entity 2', code='TST2')
        test_status3 = Status(name='Test Entity 3', code='TST3')
        db.DBSession.add_all([test_status1, test_status2, test_status3])
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/statuses',
            status=200
        )

        all_statuses = Status.query.all()

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': s.id,
                    '$ref': '/api/statuses/%s' % s.id,
                    'name': s.name,
                    'entity_type': s.entity_type
                } for s in all_statuses])
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/statuses/{id} view is working properly
        """
        from stalker import db, Status
        test_status1 = Status(name='Test Status 1', code='TST1')
        db.DBSession.add(test_status1)
        db.DBSession.commit()

        new_name = 'New Status Name'
        new_code = 'NSN'
        new_description = 'This should also be present'

        self.admin_login()
        self.test_app.patch(
            '/api/statuses/%s' % test_status1.id,
            params={
                'name': new_name,
                'code': new_code,
                'description': new_description
            },
            status=200
        )

        test_status1_db = Status.query.get(test_status1.id)
        self.assertEqual(test_status1_db.name, new_name)
        self.assertEqual(test_status1_db.code, new_code)
        self.assertEqual(test_status1_db.description, new_description)

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/statuses/{id} view is working properly
        """
        from stalker import db, Status
        test_status1 = Status(name='Test Status 1', code='TST1')
        db.DBSession.add(test_status1)
        db.DBSession.commit()

        new_name = 'New Status Name'
        new_code = 'NSN'
        new_description = 'This should also be present'

        self.admin_login()
        self.test_app.post(
            '/api/statuses/%s' % test_status1.id,
            params={
                'name': new_name,
                'code': new_code,
                'description': new_description
            },
            status=200
        )

        test_status1_db = Status.query.get(test_status1.id)
        self.assertEqual(test_status1_db.name, new_name)
        self.assertEqual(test_status1_db.code, new_code)
        self.assertEqual(test_status1_db.description, new_description)

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/statuses is working properly
        """
        name = 'New Status Name'
        code = 'NSN'
        description = 'This should also be present'
        created_by_id = 3

        response = self.test_app.put(
            '/api/statuses',
            params={
                'name': name,
                'code': code,
                'description': description,
                'created_by_id': created_by_id
            },
            status=201
        )

        from stalker import Status
        new_status = Status.query.filter(Status.code == code).first()

        from stalker_pyramid2.views import EntityViewBase
        import stalker
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'code': code,
                'created_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        new_status.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        new_status.date_updated
                    ),
                'description': description,
                'entity_type': 'Status',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_status.id,
                    'length': 0
                },
                'generic_text': '',
                'id': new_status.id,
                'name': name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_status.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % new_status.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker import db, Status
        test_status = Status(name='Test Status', code='TST')
        db.DBSession.add(test_status)
        db.DBSession.commit()

        self.assertIsNotNone(Status.query.filter(Status.code == 'TST').first())

        self.test_app.delete(
            '/api/statuses/%s' % test_status.id,
            status=200
        )

        self.assertIsNone(Status.query.filter(Status.code == 'TST').first())
