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
from stalker_pyramid.views import structure


class StructureViewsUnitTestCase(UnitTestBase):
    """unit tests for StructureViews class
    """

    def setUp(self):
        """create test data
        """
        super(StructureViewsUnitTestCase, self).setUp()

        from stalker import db, FilenameTemplate, Structure
        self.test_filename_template1 = FilenameTemplate(
            name='Asset Filename Template 1',
            target_entity_type='Asset',
            path='/some/path/template/code',
            filename='file_name_template_code'
        )
        db.DBSession.add(self.test_filename_template1)

        self.test_filename_template2 = FilenameTemplate(
            name='Asset Filename Template 2',
            target_entity_type='Asset',
            path='/some/path/template/code',
            filename='file_name_template_code'
        )
        db.DBSession.add(self.test_filename_template2)

        self.test_filename_template3 = FilenameTemplate(
            name='Asset Filename Template 3',
            target_entity_type='Asset',
            path='/some/path/template/code',
            filename='file_name_template_code'
        )
        db.DBSession.add(self.test_filename_template3)

        self.test_structure1 = Structure(
            name='Test Structure 1',
            created_by=self.admin,
            templates=[
                self.test_filename_template1,
                self.test_filename_template2
            ],
            custom_template='custom template code here',
        )
        db.DBSession.add(self.test_structure1)

        self.test_structure2 = Structure(
            name='Test Structure 2',
            created_by=self.admin,
            templates=[
                self.test_filename_template1,
                self.test_filename_template2
            ],
            custom_template='custom template code here',
        )
        db.DBSession.add(self.test_structure2)

        self.test_structure3 = Structure(
            name='Test Structure 3',
            created_by=self.admin,
            templates=[
                self.test_filename_template1,
                self.test_filename_template2
            ],
            custom_template='custom template code here',
        )
        db.DBSession.add(self.test_structure3)

        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id
        structure_view = structure.StructureViews(request)

        response = structure_view.get_entity()

        import stalker
        from stalker_pyramid.views import EntityViewBase
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
                'custom_template': 'custom template code here',
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    self.test_structure1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    self.test_structure1.date_updated
                ),
                'description': '',
                'entity_type': 'Structure',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_structure1.id,
                    'length': 0
                },
                'id': self.test_structure1.id,
                'name': 'Test Structure 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_structure1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_structure1.id,
                    'length': 0
                },
                'templates': {
                    '$ref': '/api/structures/%s/templates' %
                            self.test_structure1.id,
                    'length': 2
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
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        structure_view = structure.StructureViews(request)

        response = structure_view.get_entities()

        from stalker import Structure
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Structure',
                    '$ref': '/api/structures/%s' % r.id
                } for r in Structure.query.all()
            ]
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict

        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id
        request.method = 'POST'

        request.params = DummyMultiDict()
        request.params['name'] = 'New Structure Name'
        request.params['description'] = 'New description'
        request.params['custom_template'] = 'New custom template code'
        request.params['template_id'] = [
            self.test_filename_template2.id,
            self.test_filename_template3.id
        ]

        structure_view = structure.StructureViews(request)

        self.patch_logged_in_user(request)
        response = structure_view.update_entity()

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(structure_db.name, 'New Structure Name')
        self.assertEqual(structure_db.description, 'New description')
        self.assertEqual(
            structure_db.custom_template, 'New custom template code'
        )
        self.assertEqual(
            sorted(structure_db.templates),
            sorted([
                self.test_filename_template2,
                self.test_filename_template3
            ])
        )

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Structure'
        request.params['description'] = 'this is a new test structure'
        request.params['custom_template'] = 'custom template code here'
        request.params['template_id'] = [self.test_filename_template1.id,
                                         self.test_filename_template2.id,
                                         self.test_filename_template3.id]
        request.params['created_by_id'] = 3

        structure_view = structure.StructureViews(request)

        self.patch_logged_in_user(request)
        response = structure_view.create_entity()

        from stalker import Structure
        structure_db = Structure.query\
            .filter(Structure.name == 'New Structure')\
            .first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
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
                'custom_template': 'custom template code here',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        structure_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        structure_db.date_updated
                    ),
                'description': 'this is a new test structure',
                'entity_type': 'Structure',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            structure_db.id,
                    'length': 0
                },
                'id': structure_db.id,
                'name': 'New Structure',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % structure_db.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % structure_db.id,
                    'length': 0
                },
                'templates': {
                    '$ref': '/api/structures/%s/templates' % structure_db.id,
                    'length': 3
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
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id

        structure_view = structure.StructureViews(request)

        self.patch_logged_in_user(request)
        response = structure_view.delete_entity()

        from stalker import Structure
        self.assertIsNone(
            Structure.query.filter(
                Structure.id == self.test_structure1.id
            ).first()
        )

    def test_get_templates_is_working_properly(self):
        """testing if get_templates() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id

        structure_view = structure.StructureViews(request)
        response = structure_view.get_templates()

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [{
                    'id': ft.id,
                    'name': ft.name,
                    'entity_type': ft.entity_type,
                    '$ref': '/api/filename_templates/%s' % ft.id
                } for ft in [self.test_filename_template1,
                             self.test_filename_template2]]
            )
        )

    def test_update_templates_is_working_properly_with_patch(self):
        """testing if update_templates() method is working properly with patch
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id

        request.params = DummyMultiDict()
        request.params['template_id'] = \
            [self.test_filename_template3.id]
        request.method = 'PATCH'

        structure_view = structure.StructureViews(request)
        response = structure_view.update_templates()

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([
                self.test_filename_template1, self.test_filename_template2,
                self.test_filename_template3
            ])
        )

    def test_update_templates_is_working_properly_with_post(self):
        """testing if update_templates() method is working properly with post
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id

        request.params = DummyMultiDict()
        request.params['template_id'] = \
            [self.test_filename_template3.id]
        request.method = 'POST'

        structure_view = structure.StructureViews(request)
        response = structure_view.update_templates()

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([self.test_filename_template3])
        )

    def test_remove_templates_is_working_properly(self):
        """testing if remove_templates() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id

        request.params = DummyMultiDict()
        request.params['template_id'] = \
            [self.test_filename_template1.id]

        structure_view = structure.StructureViews(request)
        response = structure_view.remove_templates()

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([self.test_filename_template2])
        )

    def test_remove_templates_is_working_properly_with_non_related_templates(self):
        """testing if remove_templates() method is working properly with non
        related filename templates
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = self.test_structure1.id

        request.params = DummyMultiDict()
        request.params['template_id'] = \
            [self.test_filename_template1.id, self.test_filename_template3.id]

        structure_view = structure.StructureViews(request)
        response = structure_view.remove_templates()

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([self.test_filename_template2])
        )


class StructureViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for StructureViews class
    """

    def setUp(self):
        """create test data
        """
        super(StructureViewsFunctionalTestCase, self).setUp()

        from stalker import db, FilenameTemplate, Structure
        self.test_filename_template1 = FilenameTemplate(
            name='Asset Filename Template 1',
            target_entity_type='Asset',
            path='/some/path/template/code',
            filename='file_name_template_code'
        )
        db.DBSession.add(self.test_filename_template1)

        self.test_filename_template2 = FilenameTemplate(
            name='Asset Filename Template 2',
            target_entity_type='Asset',
            path='/some/path/template/code',
            filename='file_name_template_code'
        )
        db.DBSession.add(self.test_filename_template2)

        self.test_filename_template3 = FilenameTemplate(
            name='Asset Filename Template 3',
            target_entity_type='Asset',
            path='/some/path/template/code',
            filename='file_name_template_code'
        )
        db.DBSession.add(self.test_filename_template3)

        self.test_structure1 = Structure(
            name='Test Structure 1',
            created_by=self.admin,
            templates=[
                self.test_filename_template1,
                self.test_filename_template2
            ],
            custom_template='custom template code here',
        )
        db.DBSession.add(self.test_structure1)

        self.test_structure2 = Structure(
            name='Test Structure 2',
            created_by=self.admin,
            templates=[
                self.test_filename_template1,
                self.test_filename_template2
            ],
            custom_template='custom template code here',
        )
        db.DBSession.add(self.test_structure2)

        self.test_structure3 = Structure(
            name='Test Structure 3',
            created_by=self.admin,
            templates=[
                self.test_filename_template1,
                self.test_filename_template2
            ],
            custom_template='custom template code here',
        )
        db.DBSession.add(self.test_structure3)
        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/entities/{id} view is working properly
        """
        response = self.test_app.get(
            '/api/structures/%s' % self.test_structure1.id,
            status=200
        )

        import stalker
        from stalker_pyramid.views import EntityViewBase
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
                'custom_template': 'custom template code here',
                'date_created': EntityViewBase.milliseconds_since_epoch(
                    self.test_structure1.date_created
                ),
                'date_updated': EntityViewBase.milliseconds_since_epoch(
                    self.test_structure1.date_updated
                ),
                'description': '',
                'entity_type': 'Structure',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_structure1.id,
                    'length': 0
                },
                'id': self.test_structure1.id,
                'name': 'Test Structure 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_structure1.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_structure1.id,
                    'length': 0
                },
                'templates': {
                    '$ref': '/api/structures/%s/templates' %
                            self.test_structure1.id,
                    'length': 2
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
        """testing if GET: /api/structures view is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        structure_view = structure.StructureViews(request)

        response = self.test_app.get(
            '/api/structures',
            status=200
        )

        from stalker import Structure
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Structure',
                    '$ref': '/api/structures/%s' % r.id
                } for r in Structure.query.all()
            ]
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/structures/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.patch(
            '/api/structures/%s' % self.test_structure1.id,
            status=200,
            params={
                'name': 'New Structure Name',
                'description': 'New description',
            }
        )

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(structure_db.name, 'New Structure Name')
        self.assertEqual(structure_db.description, 'New description')

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/structures/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.post(
            '/api/structures/%s' % self.test_structure1.id,
            status=200,
            params={
                'name': 'New Structure Name',
                'description': 'New description',
            }
        )

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(structure_db.name, 'New Structure Name')
        self.assertEqual(structure_db.description, 'New description')

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/structures view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/structures',
            params={
                'name': 'New Structure',
                'description': 'this is a new test structure',
                'created_by_id': 3,
                'custom_template': 'custom template code',
                'template_id': [self.test_filename_template1.id,
                                self.test_filename_template2.id]
            },
            status=201
        )

        from stalker import Structure
        structure_db = Structure.query\
            .filter(Structure.name == 'New Structure')\
            .first()

        import stalker
        from stalker_pyramid.views import EntityViewBase
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
                'custom_template': 'custom template code',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        structure_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        structure_db.date_updated
                    ),
                'description': 'this is a new test structure',
                'entity_type': 'Structure',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            structure_db.id,
                    'length': 0
                },
                'id': structure_db.id,
                'name': 'New Structure',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % structure_db.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % structure_db.id,
                    'length': 0
                },
                'templates': {
                    '$ref': '/api/structures/%s/templates' % structure_db.id,
                    'length': 2
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
        """testing if DELETE: /api/structures/{id} view is working properly
        """
        response = self.test_app.delete(
            '/api/structures/%s' % self.test_structure1.id,
            status=200
        )

        from stalker import Structure
        self.assertIsNone(
            Structure.query.filter(
                Structure.id == self.test_structure1.id
            ).first()
        )

    def test_get_templates_is_working_properly(self):
        """testing if GET: /api/structures/{id}/templates view is working
        properly
        """
        response = self.test_app.get(
            '/api/structures/%s/templates' % self.test_structure1.id,
            status=200
        )

        self.maxDiff = None
        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [{
                    'id': ft.id,
                    'name': ft.name,
                    'entity_type': ft.entity_type,
                    '$ref': '/api/filename_templates/%s' % ft.id
                } for ft in [self.test_filename_template1,
                             self.test_filename_template2]]
            )
        )

    def test_update_templates_is_working_properly_with_patch(self):
        """testing if PATCH: /api/structure/{id}/templates view is working
        properly with patch
        """
        response = self.test_app.patch(
            '/api/structures/%s/templates' % self.test_structure1.id,
            params={
                'template_id': [self.test_filename_template3.id]
            }
        )

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([
                self.test_filename_template1, self.test_filename_template2,
                self.test_filename_template3
            ])
        )

    def test_update_templates_is_working_properly_with_post(self):
        """testing if POST: /api/structures/{id}/templates view is working
        properly with post
        """
        response = self.test_app.post(
            '/api/structures/%s/templates' % self.test_structure1.id,
            params={
                'template_id': [self.test_filename_template3.id]
            }
        )

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([self.test_filename_template3])
        )

    def test_remove_templates_is_working_properly(self):
        """testing if DELETE: /api/structures/{id}/templates view is working
        properly
        """
        response = self.test_app.delete(
            '/api/structures/%s/templates?template_id=%s' % (
                self.test_structure1.id, self.test_filename_template1.id
            ),
            status=200
        )

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([self.test_filename_template2])
        )

    def test_remove_templates_is_working_properly_with_non_related_templates(self):
        """testing if remove_templates() method is working properly with non
        related filename templates
        """
        response = self.test_app.delete(
            '/api/structures/%s/templates?template_id=%s&template_id=%s' % (
                self.test_structure1.id, self.test_filename_template1.id,
                self.test_filename_template3.id
            ),
            status=200
        )

        from stalker import Structure
        structure_db = Structure.query.get(self.test_structure1.id)

        self.assertEqual(
            sorted(structure_db.templates),
            sorted([self.test_filename_template2])
        )
