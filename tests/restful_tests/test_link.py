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
from stalker_pyramid2.views import link


class LinkViewsUnitTestCase(UnitTestBase):
    """unit tests for LinkViews class
    """

    def setUp(self):
        """create test data
        """
        super(LinkViewsUnitTestCase, self).setUp()

        from stalker import db, Link
        self.test_link1 = Link(
            name='Test Link 1',
            full_path='/some/full/path/to/a/file.txt',
            original_filename='the_original_file_name.txt',
            created_by=self.admin
        )
        db.DBSession.add(self.test_link1)

        self.test_link2 = Link(
            name='Test Link 2',
            full_path='/some/full/path/to/a/file.txt',
            original_filename='the_original_file_name.txt',
            created_by=self.admin
        )
        db.DBSession.add(self.test_link2)

        self.test_link3 = Link(
            name='Test Link 3',
            full_path='/some/full/path/to/a/file.txt',
            original_filename='the_original_file_name.txt',
            created_by=self.admin
        )
        db.DBSession.add(self.test_link3)

        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_link1.id
        link_view = link.LinkViews(request)

        response = link_view.get_entity()

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
                        self.test_link1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_link1.date_updated
                    ),
                'description': '',
                'entity_type': 'Link',
                'full_path': '/some/full/path/to/a/file.txt',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_link1.id,
                    'length': 0
                },
                'id': self.test_link1.id,
                'name': 'Test Link 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_link1.id,
                    'length': 0
                },
                'original_filename': 'the_original_file_name.txt',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_link1.id,
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
        link_view = link.LinkViews(request)

        response = link_view.get_entities()

        from stalker import Link
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Link',
                    '$ref': '/api/links/%s' % r.id
                } for r in Link.query.all()
            ]
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict

        request = DummyRequest()
        request.matchdict['id'] = self.test_link1.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Link Name'
        request.params['description'] = 'New description'
        request.params['full_path'] = '/new/path/to/a/file'
        request.params['original_filename'] = 'new_original_file_name'

        link_view = link.LinkViews(request)

        self.patch_logged_in_user(request)
        response = link_view.update_entity()

        from stalker import Link
        link_db = Link.query.get(self.test_link1.id)

        self.assertEqual(link_db.name, 'New Link Name')
        self.assertEqual(link_db.description, 'New description')
        self.assertEqual(link_db.full_path, '/new/path/to/a/file')
        self.assertEqual(link_db.original_filename, 'new_original_file_name')

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Link'
        request.params['description'] = 'this is a new test link'
        request.params['created_by_id'] = 3
        request.params['full_path'] = '/full/path/to/a/new/file'
        request.params['original_filename'] = 'original_file_name'

        link_view = link.LinkViews(request)

        self.patch_logged_in_user(request)
        response = link_view.create_entity()

        from stalker import Link
        link_db = Link.query\
            .filter(Link.name == 'New Link')\
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
                        link_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        link_db.date_updated
                    ),
                'description': 'this is a new test link',
                'entity_type': 'Link',
                'full_path': '/full/path/to/a/new/file',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            link_db.id,
                    'length': 0
                },
                'id': link_db.id,
                'name': 'New Link',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % link_db.id,
                    'length': 0
                },
                'original_filename': 'original_file_name',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % link_db.id,
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
        request.matchdict['id'] = self.test_link1.id

        link_view = link.LinkViews(request)

        self.patch_logged_in_user(request)
        response = link_view.delete_entity()

        from stalker import Link
        self.assertIsNone(
            Link.query.filter(
                Link.id == self.test_link1.id
            ).first()
        )


class LinkViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for LinkViews class
    """

    def setUp(self):
        """create test data
        """
        super(LinkViewsFunctionalTestCase, self).setUp()

        from stalker import db, Link
        self.test_link1 = Link(
            name='Test Link 1',
            full_path='/some/full/path/to/a/file.txt',
            original_filename='the_original_file_name.txt',
            created_by=self.admin
        )
        db.DBSession.add(self.test_link1)

        self.test_link2 = Link(
            name='Test Link 2',
            full_path='/some/full/path/to/a/file.txt',
            original_filename='the_original_file_name.txt',
            created_by=self.admin
        )
        db.DBSession.add(self.test_link2)

        self.test_link3 = Link(
            name='Test Link 3',
            full_path='/some/full/path/to/a/file.txt',
            original_filename='the_original_file_name.txt',
            created_by=self.admin
        )
        db.DBSession.add(self.test_link3)

        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/entities/{id} view is working properly
        """
        response = self.test_app.get(
            '/api/links/%s' % self.test_link1.id,
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
                        self.test_link1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_link1.date_updated
                    ),
                'description': '',
                'entity_type': 'Link',
                'full_path': '/some/full/path/to/a/file.txt',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_link1.id,
                    'length': 0
                },
                'id': self.test_link1.id,
                'name': 'Test Link 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_link1.id,
                    'length': 0
                },
                'original_filename': 'the_original_file_name.txt',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_link1.id,
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
        """testing if GET: /api/links view is working properly
        """
        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        link_view = link.LinkViews(request)

        response = self.test_app.get(
            '/api/links',
            status=200
        )

        from stalker import Link
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Link',
                    '$ref': '/api/links/%s' % r.id
                } for r in Link.query.all()
            ]
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/links/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.patch(
            '/api/links/%s' % self.test_link1.id,
            status=200,
            params={
                'name': 'New Link Name',
                'description': 'New description',
                'full_path': '/new/path/to/a/file',
                'original_filename': 'new_original_file_name',
            }
        )

        from stalker import Link
        link_db = Link.query.get(self.test_link1.id)

        self.assertEqual(link_db.name, 'New Link Name')
        self.assertEqual(link_db.description, 'New description')
        self.assertEqual(link_db.full_path, '/new/path/to/a/file')
        self.assertEqual(link_db.original_filename, 'new_original_file_name')

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/links/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.post(
            '/api/links/%s' % self.test_link1.id,
            status=200,
            params={
                'name': 'New Link Name',
                'description': 'New description',
                'full_path': '/new/path/to/a/file',
                'original_filename': 'new_original_file_name',
            }
        )

        from stalker import Link
        link_db = Link.query.get(self.test_link1.id)

        self.assertEqual(link_db.name, 'New Link Name')
        self.assertEqual(link_db.description, 'New description')
        self.assertEqual(link_db.full_path, '/new/path/to/a/file')
        self.assertEqual(link_db.original_filename, 'new_original_file_name')

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/links view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/links',
            params={
                'name': 'New Link',
                'description': 'this is a new test link',
                'created_by_id': 3,
                'full_path': '/full/path/to/a/new/file',
                'original_filename': 'original_file_name',
            },
            status=201
        )

        from stalker import Link
        link_db = Link.query\
            .filter(Link.name == 'New Link')\
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
                        link_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        link_db.date_updated
                    ),
                'description': 'this is a new test link',
                'entity_type': 'Link',
                'full_path': '/full/path/to/a/new/file',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            link_db.id,
                    'length': 0
                },
                'id': link_db.id,
                'name': 'New Link',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % link_db.id,
                    'length': 0
                },
                'original_filename': 'original_file_name',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % link_db.id,
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
        """testing if DELETE: /api/links/{id} view is working properly
        """
        response = self.test_app.delete(
            '/api/links/%s' % self.test_link1.id,
            status=200
        )

        from stalker import Link
        self.assertIsNone(
            Link.query.filter(
                Link.id == self.test_link1.id
            ).first()
        )
