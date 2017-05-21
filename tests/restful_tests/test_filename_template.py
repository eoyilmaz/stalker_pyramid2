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
from stalker_pyramid.views import template


class FilenameTemplateViewsUnitTestCase(UnitTestBase):
    """unit tests for FilenameTemplateViews class
    """

    def setUp(self):
        """create test data
        """
        super(FilenameTemplateViewsUnitTestCase, self).setUp()

        from stalker import db, FilenameTemplate
        self.test_filename_template1 = FilenameTemplate(
            name='Asset Filename Template',
            target_entity_type='Asset',
            path='$REPO{{project.repository.id}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{version.nice_name}}'
                     '_v{{"%03d"|format(version.version_number)}}',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_filename_template1)

        self.test_filename_template2 = FilenameTemplate(
            name='Shot Filename Template',
            target_entity_type='Shot',
            path='$REPO{{project.repository.id}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{version.nice_name}}'
                     '_v{{"%03d"|format(version.version_number)}}',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_filename_template2)

        self.test_filename_template3 = FilenameTemplate(
            name='Shot Filename Template',
            target_entity_type='Shot',
            path='$REPO{{project.repository.id}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{version.nice_name}}'
                     '_v{{"%03d"|format(version.version_number)}}',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_filename_template3)
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_filename_template1.id
        filename_template_view = template.FilenameTemplateViews(request)
        response = filename_template_view.get_entity()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    self.test_filename_template1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    self.test_filename_template1.date_updated
                ),
                'description': '',
                'entity_type': 'FilenameTemplate',
                'filename': '{{version.nice_name}}'
                            '_v{{"%03d"|format(version.version_number)}}',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_filename_template1.id,
                    'length': 0,
                },
                'generic_text': '',
                'id': self.test_filename_template1.id,
                'name': 'Asset Filename Template',
                'notes': {
                    '$ref': '/api/entities/%s/notes' %
                            self.test_filename_template1.id,
                    'length': 0
                },
                'path': '$REPO{{project.repository.id}}/{{project.code}}/'
                        '{%- for parent_task in parent_tasks -%}'
                        '{{parent_task.nice_name}}/'
                        '{%- endfor -%}',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' %
                            self.test_filename_template1.id,
                    'length': 0
                },
                'target_entity_type': 'Asset',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        filename_template_view = template.FilenameTemplateViews(request)
        response = filename_template_view.get_entities()

        from stalker import FilenameTemplate
        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'name': ft.name,
                    'id': ft.id,
                    'entity_type': ft.entity_type,
                    '$ref': '/api/filename_templates/%s' % ft.id
                } for ft in FilenameTemplate.query.all()
            ])
        )

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Filename Template'
        request.params['target_entity_type'] = 'Task'
        request.params['filename'] = 'some_template_text'
        request.params['path'] = 'some_other_template_text'
        request.params['created_by_id'] = self.admin.id
        request.params['description'] = 'This is a new filename template'

        filename_template_view = template.FilenameTemplateViews(request)
        response = filename_template_view.create_entity()

        from stalker import FilenameTemplate
        new_ft_db = FilenameTemplate.query\
            .filter(FilenameTemplate.name == 'New Filename Template')\
            .first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    new_ft_db.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    new_ft_db.date_updated
                ),
                'description': 'This is a new filename template',
                'entity_type': 'FilenameTemplate',
                'filename': 'some_template_text',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_ft_db.id,
                    'length': 0,
                },
                'generic_text': '',
                'id': new_ft_db.id,
                'name': 'New Filename Template',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_ft_db.id,
                    'length': 0
                },
                'path': 'some_other_template_text',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' %
                            new_ft_db.id,
                    'length': 0
                },
                'target_entity_type': 'Task',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
            }
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        name = 'New Filename Template'
        filename = 'some_template_text'
        description = 'This is a new filename template'
        path = 'some_other_template_text'

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_filename_template1.id

        request.params = DummyMultiDict()
        request.params['name'] = name
        # request.params['target_entity_type'] = target_entity_type
        request.params['filename'] = filename
        request.params['path'] = path
        request.params['updated_by_id'] = self.admin.id
        request.params['description'] = description

        self.patch_logged_in_user(request)
        filename_template_view = template.FilenameTemplateViews(request)
        response = filename_template_view.update_entity()

        from stalker import FilenameTemplate
        ft_db = FilenameTemplate.query\
            .filter(FilenameTemplate.name == name)\
            .first()

        self.assertEqual(ft_db.name, name)
        self.assertEqual(ft_db.filename, filename)
        self.assertEqual(ft_db.description, description)
        self.assertEqual(ft_db.path, path)
        self.assertEqual(ft_db.updated_by, self.admin)

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_filename_template1.id

        self.patch_logged_in_user(request)
        filename_template_view = template.FilenameTemplateViews(request)
        response = filename_template_view.delete_entity()

        from stalker import FilenameTemplate
        self.assertIsNone(
            FilenameTemplate.query.get(self.test_filename_template1.id)
        )


class FilenameTemplateViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for FilenameTemplateViews class
    """

    def setUp(self):
        """create test data
        """
        super(FilenameTemplateViewsFunctionalTestCase, self).setUp()

        from stalker import db, FilenameTemplate
        self.test_filename_template1 = FilenameTemplate(
            name='Asset Filename Template',
            target_entity_type='Asset',
            path='$REPO{{project.repository.id}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{version.nice_name}}'
                     '_v{{"%03d"|format(version.version_number)}}',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_filename_template1)

        self.test_filename_template2 = FilenameTemplate(
            name='Shot Filename Template',
            target_entity_type='Shot',
            path='$REPO{{project.repository.id}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{version.nice_name}}'
                     '_v{{"%03d"|format(version.version_number)}}',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_filename_template2)

        self.test_filename_template3 = FilenameTemplate(
            name='Shot Filename Template',
            target_entity_type='Shot',
            path='$REPO{{project.repository.id}}/{{project.code}}/'
                 '{%- for parent_task in parent_tasks -%}'
                 '{{parent_task.nice_name}}/'
                 '{%- endfor -%}',
            filename='{{version.nice_name}}'
                     '_v{{"%03d"|format(version.version_number)}}',
            created_by=self.admin,
        )
        db.DBSession.add(self.test_filename_template3)
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/filename_templates/{id} view is working
        properly
        """
        response = self.test_app.get(
            '/api/filename_templates/%s' % self.test_filename_template1.id,
            status=200
        )

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    self.test_filename_template1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    self.test_filename_template1.date_updated
                ),
                'description': '',
                'entity_type': 'FilenameTemplate',
                'filename': '{{version.nice_name}}'
                            '_v{{"%03d"|format(version.version_number)}}',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_filename_template1.id,
                    'length': 0,
                },
                'generic_text': '',
                'id': self.test_filename_template1.id,
                'name': 'Asset Filename Template',
                'notes': {
                    '$ref': '/api/entities/%s/notes' %
                            self.test_filename_template1.id,
                    'length': 0
                },
                'path': '$REPO{{project.repository.id}}/{{project.code}}/'
                        '{%- for parent_task in parent_tasks -%}'
                        '{{parent_task.nice_name}}/'
                        '{%- endfor -%}',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' %
                            self.test_filename_template1.id,
                    'length': 0
                },
                'target_entity_type': 'Asset',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET: /api/filename_templates view is working properly
        """
        response = self.test_app.get(
            '/api/filename_templates',
            status=200
        )

        from stalker import FilenameTemplate
        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'name': ft.name,
                    'id': ft.id,
                    'entity_type': ft.entity_type,
                    '$ref': '/api/filename_templates/%s' % ft.id
                } for ft in FilenameTemplate.query.all()
            ])
        )

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/filename_templates view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/filename_templates',
            params={
                'name': 'New Filename Template',
                'target_entity_type': 'Task',
                'filename': 'some_template_text',
                'path': 'some_other_template_text',
                'created_by_id': self.admin.id,
                'description': 'This is a new filename template',
            },
            status=201
        )

        from stalker import FilenameTemplate
        new_ft_db = FilenameTemplate.query\
            .filter(FilenameTemplate.name == 'New Filename Template')\
            .first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    new_ft_db.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    new_ft_db.date_updated
                ),
                'description': 'This is a new filename template',
                'entity_type': 'FilenameTemplate',
                'filename': 'some_template_text',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            new_ft_db.id,
                    'length': 0,
                },
                'generic_text': '',
                'id': new_ft_db.id,
                'name': 'New Filename Template',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % new_ft_db.id,
                    'length': 0
                },
                'path': 'some_other_template_text',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' %
                            new_ft_db.id,
                    'length': 0
                },
                'target_entity_type': 'Task',
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': 3,
                    'name': 'admin',
                    'entity_type': 'User',
                    '$ref': '/api/users/3'
                },
            }
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/filename_templates/{id} view is working
        properly
        """
        name = 'New Filename Template'
        filename = 'some_template_text'
        description = 'This is a new filename template'
        path = 'some_other_template_text'

        response = self.test_app.patch(
            '/api/filename_templates/%s' % self.test_filename_template1.id,
            params={
                'name': name,
                'filename': filename,
                'path': path,
                'updated_by_id': self.admin.id,
                'description': description,
            },
            status=200
        )

        from stalker import FilenameTemplate
        ft_db = FilenameTemplate.query\
            .filter(FilenameTemplate.name == name)\
            .first()

        self.assertEqual(ft_db.name, name)
        self.assertEqual(ft_db.filename, filename)
        self.assertEqual(ft_db.description, description)
        self.assertEqual(ft_db.path, path)
        self.assertEqual(ft_db.updated_by, self.admin)

    def test_update_entity_is_working_properly_with_post(self):
        """testing if PATCH: /api/filename_templates/{id} view is working
        properly
        """
        name = 'New Filename Template'
        filename = 'some_template_text'
        description = 'This is a new filename template'
        path = 'some_other_template_text'

        response = self.test_app.patch(
            '/api/filename_templates/%s' % self.test_filename_template1.id,
            params={
                'name': name,
                'filename': filename,
                'path': path,
                'updated_by_id': self.admin.id,
                'description': description,
            },
            status=200
        )

        from stalker import FilenameTemplate
        ft_db = FilenameTemplate.query\
            .filter(FilenameTemplate.name == name)\
            .first()

        self.assertEqual(ft_db.name, name)
        self.assertEqual(ft_db.filename, filename)
        self.assertEqual(ft_db.description, description)
        self.assertEqual(ft_db.path, path)
        self.assertEqual(ft_db.updated_by, self.admin)

    def test_delete_entity_is_working_properly(self):
        """testing if DELETE: /api/filename_templates/{id} view is working
        properly
        """
        response = self.test_app.delete(
            '/api/filename_templates/%s' % self.test_filename_template1.id,
            status=200
        )

        from stalker import FilenameTemplate
        self.assertIsNone(
            FilenameTemplate.query.get(self.test_filename_template1.id)
        )
