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
from stalker_pyramid2.views import format


class ImageFormatViewsUnitTestCase(UnitTestBase):
    """unit tests for the ImageFormatViews class
    """

    def test_get_entity_method_is_working_properly(self):
        """testing if the get_entity() method is working properly
        """
        from stalker import db, ImageFormat
        test_image_format = ImageFormat(
            name='HD 1080',
            width=1920,
            height=1080,
            pixel_aspect=1.0,
            print_resolution=300.0,
            description='A test image format',
            created_by=self.admin
        )
        db.DBSession.add(test_image_format)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_image_format.id

        image_format_view = format.ImageFormatViews(request)
        response = image_format_view.get_entity()

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
                    'entity_type': self.admin.entity_type
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_updated
                    ),
                'description': 'A test image format',
                'entity_type': 'ImageFormat',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_image_format.id,
                    'length': 0
                },
                'height': 1080,
                'id': test_image_format.id,
                'name': 'HD 1080',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_image_format.id,
                    'length': 0
                },
                'pixel_aspect': 1.0,
                'print_resolution': 300.0,
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_image_format.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'width': 1920,
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
        # create a couple of image formats
        from stalker import db, ImageFormat
        im1 = ImageFormat(
            name='HD 720',
            width=1280,
            height=720
        )
        db.DBSession.add(im1)

        im2 = ImageFormat(
            name='HD 1080',
            width=1920,
            height=1080
        )
        db.DBSession.add(im2)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()

        image_format_view = format.ImageFormatViews(request)
        response = image_format_view.get_entities()

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': im.id,
                    '$ref': '/api/image_formats/%s' % im.id,
                    'name': im.name,
                    'entity_type': im.entity_type
                } for im in [im1, im2]
            ])
        )

    def test_create_entity_method_is_working_properly(self):
        """testing if the create_entity() method is working properly
        """
        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict

        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'HD 1080'
        request.params['width'] = 1920
        request.params['height'] = 1080
        request.params['description'] = 'A test image format'
        request.params['created_by_id'] = self.admin.id

        image_format_view = format.ImageFormatViews(request)
        response = image_format_view.create_entity()

        from stalker import ImageFormat
        test_image_format = \
            ImageFormat.query\
                .filter(ImageFormat.name == 'HD 1080')\
                .first()

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
                    'entity_type': self.admin.entity_type
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_updated
                    ),
                'description': 'A test image format',
                'entity_type': 'ImageFormat',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_image_format.id,
                    'length': 0
                },
                'height': 1080,
                'id': test_image_format.id,
                'name': 'HD 1080',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_image_format.id,
                    'length': 0
                },
                'pixel_aspect': 1.0,
                'print_resolution': 300.0,
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_image_format.id,
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
                'width': 1920
            }
        )

    def test_update_entity_method_is_working_properly(self):
        """testing if the update_entity() method is working properly
        """
        from stalker import db, ImageFormat
        test_image_format = ImageFormat(
            name='HD 1080',
            description='A test image format',
            width=1920,
            height=1080,
            pixel_aspect=1.0,
            print_resolution=300.0,
            created_by=self.admin
        )
        db.DBSession.add(test_image_format)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_image_format.id

        request.params = DummyMultiDict()
        request.params['description'] = 'New description'
        request.params['name'] = 'HD 720'
        request.params['width'] = 1280
        request.params['height'] = 720

        self.patch_logged_in_user(request)
        image_format_view = format.ImageFormatViews(request)
        response = image_format_view.update_entity()

        test_image_format_db = ImageFormat.query.get(test_image_format.id)
        self.assertEqual(test_image_format_db.name, 'HD 720')
        self.assertEqual(test_image_format_db.description, 'New description')
        self.assertEqual(test_image_format_db.width, 1280)
        self.assertEqual(test_image_format_db.height, 720)

    def test_delete_entity_method_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        from stalker import db, ImageFormat
        test_image_format = ImageFormat(
            name='HD 1080',
            description='A test image format',
            created_by=self.admin,
            width=1920,
            height=1080
        )
        db.DBSession.add(test_image_format)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_image_format.id

        image_format_view = format.ImageFormatViews(request)
        image_format_view.delete_entity()

        self.assertIsNotNone(test_image_format.id)
        self.assertIsNone(
            ImageFormat.query
                .filter(ImageFormat.id == test_image_format.id)
                .first()
        )


class TypeViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for the TypeViews class
    """

    def test_get_entity_method_is_working_properly(self):
        """testing if the GET: /api/image_formats/{id} view is working properly
        """
        from stalker import db, ImageFormat
        test_image_format = ImageFormat(
            name='HD 1080',
            width=1920,
            height=1080,
            pixel_aspect=1.0,
            print_resolution=300.0,
            description='A test image format',
            created_by=self.admin
        )
        db.DBSession.add(test_image_format)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/image_formats/%s' % test_image_format.id,
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
                    'entity_type': self.admin.entity_type
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_updated
                    ),
                'description': 'A test image format',
                'entity_type': 'ImageFormat',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_image_format.id,
                    'length': 0
                },
                'height': 1080,
                'id': test_image_format.id,
                'name': 'HD 1080',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_image_format.id,
                    'length': 0
                },
                'pixel_aspect': 1.0,
                'print_resolution': 300.0,
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_image_format.id,
                    'length': 0
                },
                'thumbnail': None,
                'type': None,
                'width': 1920,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
            }
        )

    def test_get_entities_method_is_working_properly(self):
        """testing if the GET: /api/image_formats view is working properly
        """
        # create a couple of image formats
        from stalker import db, ImageFormat
        im1 = ImageFormat(
            name='HD 720',
            width=1280,
            height=720
        )
        db.DBSession.add(im1)

        im2 = ImageFormat(
            name='HD 1080',
            width=1920,
            height=1080
        )
        db.DBSession.add(im2)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/image_formats',
            status=200
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': im.id,
                    '$ref': '/api/image_formats/%s' % im.id,
                    'name': im.name,
                    'entity_type': im.entity_type
                } for im in [im1, im2]
            ])
        )

    def test_create_entity_method_is_working_properly(self):
        """testing if the PUT: /api/image_formats view is working properly
        """
        response = self.test_app.put(
            '/api/image_formats',
            params={
                'name': 'HD 1080',
                'width': 1920,
                'height': 1080,
                'description': 'A test image format',
                'created_by_id': self.admin.id,
            },
            status=201,
        )

        from stalker import ImageFormat
        test_image_format = \
            ImageFormat.query\
            .filter(ImageFormat.name == 'HD 1080')\
            .first()

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
                    'entity_type': self.admin.entity_type
                },
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_image_format.date_updated
                    ),
                'description': 'A test image format',
                'entity_type': 'ImageFormat',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_image_format.id,
                    'length': 0
                },
                'height': 1080,
                'id': test_image_format.id,
                'name': 'HD 1080',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_image_format.id,
                    'length': 0
                },
                'pixel_aspect': 1.0,
                'print_resolution': 300.0,
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_image_format.id,
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
                'width': 1920
            }
        )

    def test_update_entity_method_is_working_properly_with_patch(self):
        """testing if the PATCH: /api/image_formats/{id} view is working
        properly
        """
        from stalker import db, ImageFormat
        test_image_format = ImageFormat(
            name='HD 1080',
            description='A test image format',
            width=1920,
            height=1080,
            pixel_aspect=1.0,
            print_resolution=300.0,
            created_by=self.admin
        )
        db.DBSession.add(test_image_format)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.patch(
            '/api/image_formats/%s' % test_image_format.id,
            params={
                'description': 'New description',
                'name': 'HD 720',
                'width': 1280,
                'height': 720,
            },
            status=200
        )

        test_image_format_db = ImageFormat.query.get(test_image_format.id)
        self.assertEqual(test_image_format_db.name, 'HD 720')
        self.assertEqual(test_image_format_db.description, 'New description')
        self.assertEqual(test_image_format_db.width, 1280)
        self.assertEqual(test_image_format_db.height, 720)

    def test_update_entity_method_is_working_properly_with_post(self):
        """testing if the POST: /api/image_formats/{id} view is working
        properly
        """
        from stalker import db, ImageFormat
        test_image_format = ImageFormat(
            name='HD 1080',
            description='A test image format',
            width=1920,
            height=1080,
            pixel_aspect=1.0,
            print_resolution=300.0,
            created_by=self.admin
        )
        db.DBSession.add(test_image_format)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.post(
            '/api/image_formats/%s' % test_image_format.id,
            params={
                'description': 'New description',
                'name': 'HD 720',
                'width': 1280,
                'height': 720,
            },
            status=200
        )

        test_image_format_db = ImageFormat.query.get(test_image_format.id)
        self.assertEqual(test_image_format_db.name, 'HD 720')
        self.assertEqual(test_image_format_db.description, 'New description')
        self.assertEqual(test_image_format_db.width, 1280)
        self.assertEqual(test_image_format_db.height, 720)

    def test_delete_entity_method_is_working_properly(self):
        """testing if the DELETE: /api/image_formats/{id} view is working
        properly
        """
        from stalker import db, ImageFormat
        test_image_format = ImageFormat(
            name='HD 1080',
            description='A test image format',
            created_by=self.admin,
            width=1920,
            height=1080
        )
        db.DBSession.add(test_image_format)
        db.DBSession.commit()

        self.test_app.delete(
            '/api/image_formats/%s' % test_image_format.id,
            status=200
        )

        self.assertIsNotNone(test_image_format.id)
        self.assertIsNone(
            ImageFormat.query
            .filter(ImageFormat.id == test_image_format.id)
            .first()
        )
