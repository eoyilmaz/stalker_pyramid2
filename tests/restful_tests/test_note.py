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
from stalker_pyramid.views import note


class NoteViewsUnitTestCase(UnitTestBase):
    """unit tests for the Note views
    """

    def test_get_entity_is_working_properly(self):
        """testing if get_entity method is working properly
        """
        from stalker import db, Note
        test_note1 = Note(
            content='This is a test note',
            created_by=self.admin
        )
        db.DBSession.add(test_note1)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_note1.id

        note_view = note.NoteViews(request)
        response = note_view.get_entity()

        import stalker
        from stalker_pyramid.views import EntityViewBase

        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
                'content': 'This is a test note',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_updated
                    ),
                'description': 'This is a test note',
                'entity_type': 'Note',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_note1.id,
                    'length': 0
                },
                'id': test_note1.id,
                'name': test_note1.name,
                'stalker_version': stalker.__version__,
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                }
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities is working properly
        """
        from stalker import db, Note
        note1 = Note(content='test content 1')
        note2 = Note(content='test content 2')
        note3 = Note(content='test content 3')
        note4 = Note(content='test content 4')
        db.DBSession.add_all([note1, note2, note3, note4])
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()

        note_views = note.NoteViews(request)
        response = note_views.get_entities()

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': note1.id,
                    '$ref': '/api/notes/%s' % note1.id,
                    'name': note1.name,
                    'entity_type': note1.entity_type
                },
                {
                    'id': note2.id,
                    '$ref': '/api/notes/%s' % note2.id,
                    'name': note2.name,
                    'entity_type': note2.entity_type
                },
                {
                    'id': note3.id,
                    '$ref': '/api/notes/%s' % note3.id,
                    'name': note3.name,
                    'entity_type': note3.entity_type
                },
                {
                    'id': note4.id,
                    '$ref': '/api/notes/%s' % note4.id,
                    'name': note4.name,
                    'entity_type': note4.entity_type
                },
            ])
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_note is working properly
        """
        from stalker import db, Note, User
        test_user = User(
            name='Test User',
            login='tuser',
            email='tuser@users.com',
            password='secret'
        )
        db.DBSession.add(test_user)

        note1 = Note(
            content='This is a test note'
        )
        db.DBSession.add(note1)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = note1.id
        request.params = DummyMultiDict()
        request.params['content'] = 'this is the new content'
        request.params['updated_by_id'] = test_user.id

        note_view = note.NoteViews(request)
        note_view.update_entity()

        note1 = Note.query.first()
        self.assertEqual(
            note1.content,
            'this is the new content'
        )
        self.assertEqual(
            note1.updated_by,
            test_user
        )

    def test_create_entity_is_working_properly(self):
        """testing if create_note is working properly
        """
        from stalker import db, User
        test_user = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@users.com',
            password='secret'
        )
        db.DBSession.add(test_user)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['content'] = 'This is the test content'
        request.params['created_by_id'] = test_user.id

        note_view = note.NoteViews(request)
        response = note_view.create_entity()

        from stalker import Note
        test_note1 = Note.query.first()

        from stalker_pyramid.views import EntityViewBase
        import stalker
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': test_user.id,
                    '$ref': '/api/users/%s' % test_user.id,
                    'name': test_user.name,
                    'entity_type': test_user.entity_type
                },
                'content': 'This is the test content',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_updated
                    ),
                'description': 'This is the test content',
                'entity_type': 'Note',
                'generic_text': '',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % test_note1.id,
                    'length': 0
                },
                'id': test_note1.id,
                'name': test_note1.name,
                'stalker_version': stalker.__version__,
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': test_user.id,
                    '$ref': '/api/users/%s' % test_user.id,
                    'name': test_user.name,
                    'entity_type': test_user.entity_type
                }
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if the delete_entity method is working properly
        """
        from stalker import db, Note
        test_note = Note(
            content='This is a test note'
        )
        db.DBSession.add(test_note)
        db.DBSession.commit()

        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_note.id

        note_view = note.NoteViews(request)
        note_view.delete_entity()

        test_note_db = Note.query.filter(Note.name == test_note.name).first()
        self.assertIsNone(test_note_db)


class NoteViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for the Note views
    """

    def test_get_entity_is_working_properly(self):
        """testing if GET /api/notes/{id} view is working properly
        """
        from stalker import db, Note
        test_note1 = Note(
            content='This is a test note',
            created_by=self.admin
        )
        db.DBSession.add(test_note1)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/notes/%s' % test_note1.id,
            status=200
        )

        import stalker
        from stalker_pyramid.views import EntityViewBase

        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                },
                'content': 'This is a test note',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_updated
                    ),
                'description': 'This is a test note',
                'entity_type': 'Note',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_note1.id,
                    'length': 0
                },
                'id': test_note1.id,
                'name': test_note1.name,
                'stalker_version': stalker.__version__,
                'thumbnail': None,
                'type': None,
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': self.admin.entity_type
                }
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing GET /api/notes is working properly
        """
        from stalker import db, Note
        note1 = Note(content='test content 1')
        note2 = Note(content='test content 2')
        note3 = Note(content='test content 3')
        note4 = Note(content='test content 4')
        db.DBSession.add_all([note1, note2, note3, note4])
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/notes',
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': note1.id,
                    '$ref': '/api/notes/%s' % note1.id,
                    'name': note1.name,
                    'entity_type': note1.entity_type
                },
                {
                    'id': note2.id,
                    '$ref': '/api/notes/%s' % note2.id,
                    'name': note2.name,
                    'entity_type': note2.entity_type
                },
                {
                    'id': note3.id,
                    '$ref': '/api/notes/%s' % note3.id,
                    'name': note3.name,
                    'entity_type': note3.entity_type
                },
                {
                    'id': note4.id,
                    '$ref': '/api/notes/%s' % note4.id,
                    'name': note4.name,
                    'entity_type': note4.entity_type
                },
            ])
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH /api/note/{id} is working properly
        """
        from stalker import db, Note
        note1 = Note(
            content='This is a test note'
        )
        db.DBSession.add(note1)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.patch(
            '/api/notes/%s' % note1.id,
            params={
                'content': 'this is the new content'
            },
            status=200
        )

        note1 = Note.query.first()
        self.assertEqual(
            note1.content,
            'this is the new content'
        )

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST /api/note/{id} is working properly
        """
        from stalker import db, Note
        note1 = Note(
            content='This is a test note'
        )
        db.DBSession.add(note1)
        db.DBSession.commit()

        self.admin_login()
        self.test_app.post(
            '/api/notes/%s' % note1.id,
            params={
                'content': 'this is the new content'
            },
            status=200
        )

        note1 = Note.query.first()
        self.assertEqual(
            note1.content,
            'this is the new content'
        )

    def test_create_entity_is_working_properly(self):
        """testing PUT:/api/notes is working properly
        """
        from stalker import db, User
        test_user = User(
            name='Test User',
            login='tuser',
            email='tuser@users.com',
            password='secret'
        )
        db.DBSession.add(test_user)

        from stalker import Type
        note_type = Type(
            name='Review Note',
            code='RNote',
            target_entity_type='Note'
        )
        db.DBSession.add(note_type)
        db.DBSession.commit()

        response = self.test_app.put(
            '/api/notes',
            params={
                'content': 'This is the test content',
                'created_by_id': test_user.id,
                'type_id': note_type.id
            },
            status=201
        )

        from stalker import Note
        test_note1 = Note.query.first()

        from stalker_pyramid.views import EntityViewBase
        import stalker
        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            {
                'created_by': {
                    'id': test_user.id,
                    '$ref': '/api/users/%s' % test_user.id,
                    'name': test_user.name,
                    'entity_type': test_user.entity_type
                },
                'content': 'This is the test content',
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        test_note1.date_updated
                    ),
                'description': 'This is the test content',
                'entity_type': 'Note',
                'generic_text': '',
                'generic_data': {
                    '$ref':
                        '/api/simple_entities/%s/generic_data' % test_note1.id,
                    'length': 0
                },
                'id': test_note1.id,
                'name': test_note1.name,
                'stalker_version': stalker.__version__,
                'thumbnail': None,
                'type': {
                    'id': note_type.id,
                    '$ref': '/api/types/%s' % note_type.id,
                    'name': note_type.name,
                    'entity_type': note_type.entity_type
                },
                'updated_by': {
                    'id': test_user.id,
                    '$ref': '/api/users/%s' % test_user.id,
                    'name': test_user.name,
                    'entity_type': test_user.entity_type
                }
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if DELETE /api/notes/{id} view is working properly
        """
        from stalker import db, Note
        test_note = Note(
            content='This is a test note'
        )
        db.DBSession.add(test_note)
        db.DBSession.commit()

        self.test_app.delete(
            '/api/notes/%s' % test_note.id,
            status=200
        )

        test_note_db = Note.query.filter(Note.name == test_note.name).first()
        self.assertIsNone(test_note_db)
