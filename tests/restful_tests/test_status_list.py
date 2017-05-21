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
from stalker_pyramid.views import status


class StatusListViewsUnitTestCase(UnitTestBase):
    """unit tests for the StatusList views
    """

    def test_get_entity_is_working_properly(self):
        """testing if the get_entity() method is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Status List',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id
        status_list_view = status.StatusListViews(request)

        response = status_list_view.get_entity()

        from stalker_pyramid.views import EntityViewBase
        import stalker
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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_updated
                    ),
                'description': '',
                'entity_type': 'StatusList',
                'id': test_status_list.id,
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_status_list.id,
                    'length': 0
                },
                'generic_text': '',
                'name': test_status_list.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_status_list.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'statuses': {
                    '$ref': '/api/status_lists/%s/statuses' %
                            test_status_list.id,
                    'length': 4
                },
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_status_list.id,
                    'length': 0
                },
                'target_entity_type': 'Project',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                }
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list_1 = StatusList(
            name='Status List 1',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list_1
        ])
        db.DBSession.commit()

        # get the default status lists
        s_lists = StatusList.query.all()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        status_list_view = status.StatusListViews(request)
        response = status_list_view.get_entities()

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': sl.id,
                    '$ref': '/api/status_lists/%s' % sl.id,
                    'name': sl.name,
                    'entity_type': sl.entity_type
                } for sl in s_lists
            ]
        )

    def test_get_entities_is_working_properly_with_filters(self):
        """testing if get_entities() method is working properly with filters
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list_1 = StatusList(
            name='Status List 1',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list_1
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['target_entity_type'] = 'Project'
        status_list_view = status.StatusListViews(request)
        response = status_list_view.get_entities()

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': sl.id,
                    '$ref': '/api/status_lists/%s' % sl.id,
                    'name': sl.name,
                    'entity_type': sl.entity_type
                } for sl in [test_status_list_1]
            ]
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Status List',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id
        self.patch_logged_in_user(request)

        request.params = DummyMultiDict()

        name = 'New Status List Name'
        description = 'This is a new description'

        request.params['name'] = name
        request.params['description'] = description
        status_list_view = status.StatusListViews(request)
        status_list_view.update_entity()

        test_status_list_db = StatusList.query.get(test_status_list.id)
        self.assertEqual(test_status_list_db.name, name)
        self.assertEqual(test_status_list_db.description, description)

    def test_delete_entity_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Status List',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id

        status_list_view = status.StatusListViews(request)
        status_list_view.delete_entity()

        # normally we shouldn't need a commit
        # but this is a unit test and the data is not committed to the db
        # and that's why it is not deleted (I guess)
        db.DBSession.commit()

        test_status_list_db = StatusList.query.get(test_status_list.id)
        self.assertIsNone(test_status_list_db)

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker import db, Status
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')
        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'Project Status List'
        request.params['description'] = 'Test description'
        request.params['status_id'] = \
            [test_status1.id, test_status2.id, test_status3.id]
        request.params['target_entity_type'] = 'Project'
        request.params['created_by_id'] = 3

        status_list_view = status.StatusListViews(request)
        response = status_list_view.create_entity()

        from stalker import StatusList
        test_status_list = StatusList.query\
            .filter(StatusList.name == 'Project Status List')\
            .first()

        from stalker_pyramid.views import EntityViewBase
        import stalker
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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_updated
                    ),
                'description': 'Test description',
                'entity_type': 'StatusList',
                'id': test_status_list.id,
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_status_list.id,
                    'length': 0
                },
                'generic_text': '',
                'name': test_status_list.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_status_list.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'statuses': {
                    '$ref':
                        '/api/status_lists/%s/statuses' % test_status_list.id,
                    'length': 3
                },
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_status_list.id,
                    'length': 0
                },
                'target_entity_type': 'Project',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                }
            }
        )

    def test_get_statuses_is_working_properly(self):
        """testing if get_statuses() method is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id

        status_list_view = status.StatusListViews(request)
        response = status_list_view.get_statuses()

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': s.id,
                    '$ref': '/api/statuses/%s' % s.id,
                    'name': s.name,
                    'entity_type': s.entity_type
                } for s in [test_status1, test_status2, test_status3,
                            test_status4]
            ])
        )

    def test_update_statuses_is_working_properly_with_patch(self):
        """testing if update_statuses() method is working properly when the
        request method is PATCH
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id
        self.patch_logged_in_user(request)

        request.params = DummyMultiDict()
        request.params['status_id'] = [test_status5.id]
        request.method = 'PATCH'

        status_list_view = status.StatusListViews(request)
        response = status_list_view.update_statuses()

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list.statuses),
            sorted([
                test_status1, test_status2, test_status3,
                test_status4, test_status5
            ])
        )

    def test_update_statuses_is_working_properly_with_post(self):
        """testing if update_statuses() method is working properly when the
        request method is POST
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id
        self.patch_logged_in_user(request)

        request.params = DummyMultiDict()
        request.params['status_id'] = [test_status1.id, test_status5.id]
        request.method = 'POST'

        status_list_view = status.StatusListViews(request)
        status_list_view.update_statuses()

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list.statuses),
            sorted([test_status1, test_status5])
        )

    def test_delete_statuses_is_working_properly(self):
        """testing if delete_statuses() method is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id

        request.params = DummyMultiDict()
        request.params['status_id'] = [test_status4.id]

        status_list_view = status.StatusListViews(request)
        status_list_view.delete_statuses()

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list.statuses),
            sorted([test_status1, test_status2, test_status3])
        )

    def test_delete_statuses_is_working_properly_with_non_related_statuses(self):
        """testing if delete_statuses() method is working properly with
        statuses that is not in the statuses list
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_status_list.id

        request.params = DummyMultiDict()
        request.params['status_id'] = [test_status4.id, test_status5.id]

        status_list_view = status.StatusListViews(request)
        status_list_view.delete_statuses()

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list.statuses),
            sorted([test_status1, test_status2, test_status3])
        )


class StatusListViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for the StatusList views
    """

    def test_get_entity_is_working_properly(self):
        """testing if the GET: /api/status_lists/{id} view is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Status List',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/status_lists/%s' % test_status_list.id,
            status=200
        )

        from stalker_pyramid.views import EntityViewBase
        import stalker
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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_updated
                    ),
                'description': '',
                'entity_type': 'StatusList',
                'id': test_status_list.id,
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_status_list.id,
                    'length': 0
                },
                'generic_text': '',
                'name': test_status_list.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_status_list.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'statuses': {
                    '$ref': '/api/status_lists/%s/statuses' %
                            test_status_list.id,
                    'length': 4
                },
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_status_list.id,
                    'length': 0
                },
                'target_entity_type': 'Project',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                }
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET: /api/status_lists view is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list_1 = StatusList(
            name='Status List 1',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list_1
        ])
        db.DBSession.commit()

        # get the default status lists
        s_lists = StatusList.query.all()

        response = self.test_app.get(
            '/api/status_lists',
            status=200
        )

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': sl.id,
                    '$ref': '/api/status_lists/%s' % sl.id,
                    'name': sl.name,
                    'entity_type': sl.entity_type
                } for sl in s_lists
            ]
        )

    def test_get_entities_is_working_properly_with_filters(self):
        """testing if GET: /api/status_lists view is working properly with
        filters
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list_1 = StatusList(
            name='Status List 1',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )
        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list_1
        ])
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/status_lists',
            params={
                'target_entity_type': 'Project'
            },
            status=200
        )

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': sl.id,
                    '$ref': '/api/status_lists/%s' % sl.id,
                    'name': sl.name,
                    'entity_type': sl.entity_type
                } for sl in [test_status_list_1]
            ]
        )

        response = self.test_app.get(
            '/api/status_lists',
            params={
                'name': 'Status List 1'
            },
            status=200
        )

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': sl.id,
                    '$ref': '/api/status_lists/%s' % sl.id,
                    'name': sl.name,
                    'entity_type': sl.entity_type
                } for sl in [test_status_list_1]
            ]
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/status_lists/{id} is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Status List',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        name = 'New Status List Name'
        description = 'This is a new description'
        self.admin_login()
        self.test_app.patch(
            '/api/status_lists/%s' % test_status_list.id,
            params={
                'name': name,
                'description': description,
                'status_id': [
                    test_status1.id, test_status2.id, test_status3.id
                ]
            },
            status=200
        )

        test_status_list_db = StatusList.query.get(test_status_list.id)
        self.assertEqual(test_status_list_db.name, name)
        self.assertEqual(test_status_list_db.description, description)
        self.assertEqual(
            sorted(test_status_list_db.statuses),
            sorted([test_status1, test_status2, test_status3])
        )

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/status_lists/{id} is working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Status List',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        name = 'New Status List Name'
        description = 'This is a new description'
        self.admin_login()
        self.test_app.post(
            '/api/status_lists/%s' % test_status_list.id,
            params={
                'name': name,
                'description': description,
                'status_id': [
                    test_status1.id, test_status2.id, test_status3.id
                ]
            },
            status=200
        )

        test_status_list_db = StatusList.query.get(test_status_list.id)
        self.assertEqual(test_status_list_db.name, name)
        self.assertEqual(test_status_list_db.description, description)
        self.assertEqual(
            sorted(test_status_list_db.statuses),
            sorted([test_status1, test_status2, test_status3])
        )

    def test_delete_entity_is_working_properly(self):
        """testing if the DELETE: /api/status_list/{id} view is working
        properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Status List',
            statuses=[test_status1, test_status2, test_status3, test_status4],
            target_entity_type='Project',
            created_by=self.admin
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        self.test_app.delete('/api/status_lists/%s' % test_status_list.id)
        # normally we shouldn't need a commit
        db.DBSession.commit()

        test_status_list_db = StatusList.query.get(test_status_list.id)
        self.assertIsNone(test_status_list_db)

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/status_lists view is working properly
        """
        from stalker import db, Status
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')
        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5
        ])
        db.DBSession.commit()

        response = self.test_app.put(
            '/api/status_lists',
            params={
                'name': 'Project Status List',
                'description': 'Test description',
                'status_id': [test_status1.id, test_status2.id,
                              test_status3.id],
                'target_entity_type': 'Project',
                'created_by_id': 3
            },
            status=201
        )

        from stalker import StatusList
        test_status_list = StatusList.query\
            .filter(StatusList.name == 'Project Status List')\
            .first()

        from stalker_pyramid.views import EntityViewBase
        import stalker
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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_status_list.date_updated
                    ),
                'description': 'Test description',
                'entity_type': 'StatusList',
                'id': test_status_list.id,
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_status_list.id,
                    'length': 0
                },
                'generic_text': '',
                'name': test_status_list.name,
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_status_list.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'statuses': {
                    '$ref':
                        '/api/status_lists/%s/statuses' % test_status_list.id,
                    'length': 3
                },
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_status_list.id,
                    'length': 0
                },
                'target_entity_type': 'Project',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                }
            }
        )

    def test_get_statuses_is_working_properly(self):
        """testing if GET: /api/status_lists/{id}/statuses view is
        working properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/status_lists/%s/statuses' % test_status_list.id,
            status=200
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': s.id,
                    '$ref': '/api/statuses/%s' % s.id,
                    'name': s.name,
                    'entity_type': s.entity_type
                } for s in [test_status1, test_status2, test_status3,
                            test_status4]
            ])
        )

    def test_update_statuses_is_working_properly_with_patch(self):
        """testing if PATCH: /api/status_lists/{id}/statuses view is working
        properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        response = self.test_app.patch(
            '/api/status_lists/%s/statuses' % test_status_list.id,
            params={
                'status_id': [test_status5.id]
            },
            status=200
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list.statuses),
            sorted([
                test_status1, test_status2, test_status3,
                test_status4, test_status5
            ])
        )

    def test_update_statuses_is_working_properly_with_post(self):
        """testing if POST: /api/status_lists/{id}/statuses view is working
        properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        response = self.test_app.post(
            '/api/status_lists/%s/statuses' % test_status_list.id,
            params={
                'status_id': [test_status4.id, test_status5.id]
            },
            status=200
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list.statuses),
            sorted([test_status4, test_status5])
        )

    def test_delete_statuses_is_working_properly(self):
        """testing if DELETE: /api/status_lists/{id}/statuses view is working
        properly
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        self.test_app.delete(
            '/api/status_lists/%s/statuses?status_id=%s' % (
                test_status_list.id, test_status4.id)
        )

        test_status_list_db = StatusList.query\
            .filter(StatusList.name == test_status_list.name).first()

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list_db.statuses),
            sorted([test_status1, test_status2, test_status3])
        )

    def test_delete_statuses_is_working_properly_with_non_related_statuses(self):
        """testing if delete_statuses() method is working properly with
        statuses that is not in the statuses list
        """
        from stalker import db, Status, StatusList
        test_status1 = Status(name='Test Status 1', code='TST1')
        test_status2 = Status(name='Test Status 2', code='TST2')
        test_status3 = Status(name='Test Status 3', code='TST3')
        test_status4 = Status(name='Test Status 4', code='TST4')
        test_status5 = Status(name='Test Status 5', code='TST5')

        test_status_list = StatusList(
            name='Test Status List',
            target_entity_type='Project',
            statuses=[test_status1, test_status2, test_status3, test_status4]
        )

        db.DBSession.add_all([
            test_status1, test_status2, test_status3, test_status4,
            test_status5, test_status_list
        ])
        db.DBSession.commit()

        self.test_app.delete(
            '/api/status_lists/%s/statuses?status_id=%s&status_id=%s' % (
                test_status_list.id, test_status4.id, test_status5.id
            )
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(test_status_list.statuses),
            sorted([test_status1, test_status2, test_status3])
        )
