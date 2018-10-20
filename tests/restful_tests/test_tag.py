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
from stalker_pyramid2.views import tag


class TagViewsUnitTestCase(UnitTestBase):
    """unit tests for the Tag views
    """

    def test_get_entity(self):
        """testing if get_entity() method is working properly
        """
        from stalker import db, Tag
        tag1 = Tag(
            name='Test Tag 1'
        )
        db.DBSession.add(tag1)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = tag1.id

        tag_view = tag.TagViews(request)
        response = tag_view.get_entity()

        from stalker_pyramid2.views import EntityViewBase
        import stalker

        self.assertEqual(
            response.json_body,
            {
                'created_by': None,
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    tag1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    tag1.date_updated
                ),
                'description': '',
                'entity_type': 'Tag',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % tag1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': tag1.id,
                'name': 'Test Tag 1',
                'stalker_version': stalker.__version__,
                'thumbnail': None,
                'type': None,
                'updated_by': None
            }
        )

    def test_get_entities_view_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker import db, Tag
        test_tag1 = Tag(name='Test Tag 1')
        test_tag2 = Tag(name='Test Tag 2')
        test_tag3 = Tag(name='Test Tag 3')
        db.DBSession.add_all([test_tag1, test_tag2, test_tag3])
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()

        tag_view = tag.TagViews(request)
        response = tag_view.get_entities()

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': t.id,
                    '$ref': '/api/tags/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in [test_tag1, test_tag2, test_tag3]
            ]
        )

    def test_create_entity_is_working_properly(self):
        """testing if the create_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()

        request.params['name'] = 'Test Tag 1'
        request.method = 'PUT'

        # patch get_logged_in_user
        self.patch_logged_in_user(request)

        tag_view = tag.TagViews(request)
        response = tag_view.create_entity()

        from stalker_pyramid2.views import EntityViewBase
        from stalker import Tag
        new_tag = Tag.query.filter(Tag.name == 'Test Tag 1').first()

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
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    new_tag.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    new_tag.date_updated
                ),
                'description': '',
                'entity_type': 'Tag',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % new_tag.id,
                    'length': 0
                },
                'generic_text': '',
                'id': new_tag.id,
                'name': 'Test Tag 1',
                'stalker_version': stalker.__version__,
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

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if update_entity() method is working properly with PATCH
        """
        from stalker import db, Tag
        new_tag = Tag(name='Test Tag 1')
        db.DBSession.add(new_tag)
        db.DBSession.flush()
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = new_tag.id
        self.patch_logged_in_user(request)

        request.params = DummyMultiDict()
        request.params['name'] = 'New Tag Name'
        request.params['description'] = 'This also should be updated'
        request.method = 'PATCH'

        tag_view = tag.TagViews(request)
        tag_view.update_entity()

        new_tag_db = Tag.query.get(new_tag.id)
        self.assertEqual(new_tag_db.name, 'New Tag Name')
        self.assertEqual(new_tag_db.description, 'This also should be updated')
        self.assertEqual(new_tag_db.updated_by, self.admin)

    def test_update_entity_is_working_properly_with_post(self):
        """testing if update_entity() method is working properly with POST
        """
        from stalker import db, Tag
        new_tag = Tag(name='Test Tag 1')
        db.DBSession.add(new_tag)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = new_tag.id
        self.patch_logged_in_user(request)

        request.params = DummyMultiDict()
        request.params['name'] = 'New Tag Name'
        request.params['description'] = 'This also should be updated'
        request.method = 'POST'

        tag_view = tag.TagViews(request)
        tag_view.update_entity()

        new_tag_db = Tag.query.get(new_tag.id)
        self.assertEqual(new_tag_db.name, 'New Tag Name')
        self.assertEqual(new_tag_db.description, 'This also should be updated')

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker import db, Tag
        test_tag1 = Tag(name='Test Tag 1')
        test_tag2 = Tag(name='Test Tag 2')
        test_tag3 = Tag(name='Test Tag 3')

        db.DBSession.add_all([test_tag1, test_tag2, test_tag3])
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_tag1.id

        tag_view = tag.TagViews(request)
        tag_view.delete_entity()

        tags = Tag.query.all()
        self.assertEqual(
            sorted(tags),
            sorted([test_tag2, test_tag3])
        )


class TagViewFunctionalTestCase(FunctionalTestBase):
    """functional tests for the Tag views
    """

    def test_get_entity(self):
        """testing if GET: /api/tags/{id} view is working properly
        """
        from stalker import db, Tag
        tag1 = Tag(name='Test Tag 1')
        db.DBSession.add(tag1)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/tags/%s' % tag1.id,
            status=200
        )

        from stalker_pyramid2.views import EntityViewBase
        import stalker

        self.assertEqual(
            response.json_body,
            {
                'created_by': None,
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    tag1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    tag1.date_updated
                ),
                'description': '',
                'entity_type': 'Tag',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' % tag1.id,
                    'length': 0
                },
                'generic_text': '',
                'id': tag1.id,
                'name': 'Test Tag 1',
                'stalker_version': stalker.__version__,
                'thumbnail': None,
                'type': None,
                'updated_by': None
            }
        )

    def test_get_entities_view_is_working_properly(self):
        """testing if GET: /api/tags view is working properly
        """
        from stalker import db, Tag
        test_tag1 = Tag(name='Test Tag 1')
        test_tag2 = Tag(name='Test Tag 2')
        test_tag3 = Tag(name='Test Tag 3')
        db.DBSession.add_all([test_tag1, test_tag2, test_tag3])
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/tags',
            status=200
        )

        self.assertEqual(
            response.json_body,
            [
                {
                    'id': t.id,
                    '$ref': '/api/tags/%s' % t.id,
                    'name': t.name,
                    'entity_type': t.entity_type
                } for t in [test_tag1, test_tag2, test_tag3]
            ]
        )

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/tags view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/tags',
            params={
                'name': 'Test Tag 1'
            },
            status=201
        )

        from stalker_pyramid2.views import EntityViewBase
        from stalker import Tag
        new_tag = Tag.query.filter(Tag.name == 'Test Tag 1').first()

        import stalker
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': 3,
                    '$ref': '/api/users/3',
                    'name': 'admin',
                    'entity_type': 'User'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    new_tag.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    new_tag.date_updated
                ),
                'description': '',
                'entity_type': 'Tag',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % new_tag.id,
                    'length': 0
                },
                'generic_text': '',
                'id': new_tag.id,
                'name': 'Test Tag 1',
                'stalker_version': stalker.__version__,
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

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/tags/{id} view is working properly
        """
        from stalker import db, Tag
        new_tag = Tag(name='Test Tag 1')
        db.DBSession.add(new_tag)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.patch(
            '/api/tags/%s' % new_tag.id,
            params={
                'name': 'New Tag Name',
                'description': 'This also should be updated'
            },
            status=200
        )

        new_tag_db = Tag.query.get(new_tag.id)
        self.assertEqual(new_tag_db.name, 'New Tag Name')
        self.assertEqual(new_tag_db.description, 'This also should be updated')

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/tags/{id} view is working properly
        """
        from stalker import db, Tag
        new_tag = Tag(name='Test Tag 1')
        db.DBSession.add(new_tag)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.post(
            '/api/tags/%s' % new_tag.id,
            params={
                'name': 'New Tag Name',
                'description': 'This also should be updated'
            },
            status=200
        )

        new_tag_db = Tag.query.get(new_tag.id)
        self.assertEqual(new_tag_db.name, 'New Tag Name')
        self.assertEqual(new_tag_db.description, 'This also should be updated')

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker import db, Tag
        test_tag1 = Tag(name='Test Tag 1')
        test_tag2 = Tag(name='Test Tag 2')
        test_tag3 = Tag(name='Test Tag 3')

        db.DBSession.add_all([test_tag1, test_tag2, test_tag3])
        db.DBSession.commit()

        self.test_app.delete(
            '/api/tags/%s' % test_tag1.id,
            status=200
        )

        tags = Tag.query.all()
        self.assertEqual(
            sorted(tags),
            sorted([test_tag2, test_tag3])
        )
