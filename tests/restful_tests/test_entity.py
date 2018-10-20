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
from stalker_pyramid2.views import entity


class EntityViewsUnitTestCase(UnitTestBase):
    """unit tests for the Entity views
    """

    def test_get_entity(self):
        """testing get_entity() is working properly
        """
        # create a test entity
        from stalker import db, Entity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)
        test_entity = Entity(
            name='Test Entity',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_entity.id

        entity_view = entity.EntityViews(request)
        response = entity_view.get_entity()

        from stalker_pyramid2.views import EntityViewBase
        import stalker

        expected = {
            'created_by': {
                'id': self.admin.id,
                '$ref': '/api/users/%s' % self.admin.id,
                'name': self.admin.name,
                'entity_type': 'User'
            },
            'date_created':
                EntityViewBase.milliseconds_since_epoch(date_created),
            'date_updated':
                EntityViewBase.milliseconds_since_epoch(date_created),
            'description': 'This is a test description',
            'entity_type': 'Entity',
            'generic_text': '',
            'generic_data': {
                '$ref': '/api/simple_entities/%s/generic_data' %
                        test_entity.id,
                'length': 0
            },
            'id': test_entity.id,
            'name': 'Test Entity',
            'notes': {
                '$ref': '/api/entities/%s/notes' % test_entity.id,
                'length': 0
            },
            'stalker_version': stalker.__version__,
            'tags': {
                '$ref': '/api/entities/%s/tags' % test_entity.id,
                'length': 0
            },
            'thumbnail': {
                'id': test_thumbnail.id,
                '$ref': '/api/links/%s' % test_thumbnail.id,
                'name': test_thumbnail.name,
                'entity_type': 'Link'
            },
            'type': {
                'id': test_entity.type_id,
                '$ref': '/api/types/%s' % test_entity.type_id,
                'name': test_entity.type.name,
                'entity_type': 'Type'
            },
            'updated_by': {
                'id': self.admin.id,
                '$ref': '/api/users/%s' % self.admin.id,
                'name': self.admin.name,
                'entity_type': 'User'
            },
        }

        import pprint
        pprint.pprint(response.json_body)

        self.maxDiff = None
        self.assertEqual(
            response.json_body,
            expected
        )

    def test_get_entities(self):
        """testing get_entities() is working properly
        """
        # create a couple of test entities
        from stalker import db, Entity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)

        # Test Entity 1
        test_entity1 = Entity(
            name='Test Entity 1',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity1)

        # Test Entity 2
        test_entity2 = Entity(
            name='Test Entity 2',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity2)

        # Test Entity 3
        test_entity3 = Entity(
            name='Test Entity 3',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity3)

        # commit data
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()

        entity_view = entity.EntityViews(request)
        response = entity_view.get_entities()

        # admins department
        admins_department = Entity.query\
            .filter(Entity.name == 'admins')\
            .filter(Entity.entity_type == 'Department')\
            .first()

        # admins group
        admins_group = Entity.query\
            .filter(Entity.name == 'admins')\
            .filter(Entity.entity_type == 'Group')\
            .first()

        # Statuses
        status_new = Entity.query\
            .filter(Entity.name == 'New').first()
        status_accepted = Entity.query\
            .filter(Entity.name == 'Accepted').first()
        status_assigned = Entity.query\
            .filter(Entity.name == 'Assigned').first()
        status_reopened = Entity.query\
            .filter(Entity.name == 'Reopened').first()
        status_closed = Entity.query\
            .filter(Entity.name == 'Closed').first()
        status_open = Entity.query\
            .filter(Entity.name == 'Open').first()
        status_wfd = Entity.query\
            .filter(Entity.name == 'Waiting For Dependency').first()
        status_rts = Entity.query\
            .filter(Entity.name == 'Ready To Start').first()
        status_wip = Entity.query\
            .filter(Entity.name == 'Work In Progress').first()
        status_prev = Entity.query\
            .filter(Entity.name == 'Pending Review').first()
        status_hrev = Entity.query\
            .filter(Entity.name == 'Has Revision').first()
        status_drev = Entity.query\
            .filter(Entity.name == 'Dependency Has Revision').first()
        status_oh = Entity.query\
            .filter(Entity.name == 'On Hold').first()
        status_stop = Entity.query\
            .filter(Entity.name == 'Stopped').first()
        status_cmpl = Entity.query\
            .filter(Entity.name == 'Completed').first()
        status_rrev = Entity.query\
            .filter(Entity.name == 'Requested Revision').first()
        status_app = Entity.query\
            .filter(Entity.name == 'Approved').first()

        # Status Lists
        ticket_statuses = Entity.query\
            .filter(Entity.name == 'Ticket Statuses').first()
        daily_statuses = Entity.query\
            .filter(Entity.name == 'Daily Statuses').first()
        task_statuses = Entity.query\
            .filter(Entity.name == 'Task Statuses').first()
        asset_statuses = Entity.query\
            .filter(Entity.name == 'Asset Statuses').first()
        shot_statuses = Entity.query\
            .filter(Entity.name == 'Shot Statuses').first()
        sequence_statuses = Entity.query\
            .filter(Entity.name == 'Sequence Statuses').first()
        review_statuses = Entity.query\
            .filter(Entity.name == 'Review Statuses').first()

        # Types
        type_defect = Entity.query\
            .filter(Entity.name == 'Defect').first()
        type_enhancement = Entity.query\
            .filter(Entity.name == 'Enhancement').first()

        all_data = [
            test_entity1, test_entity2, test_entity3,
            admins_department, admins_group, self.admin,
            status_new, status_accepted, status_assigned, status_reopened,
            status_closed, status_open, status_wfd, status_rts, status_wip,
            status_prev, status_hrev, status_drev, status_oh, status_stop,
            status_cmpl, status_rrev, status_app,
            ticket_statuses, daily_statuses, task_statuses, asset_statuses,
            shot_statuses, sequence_statuses, review_statuses,
            type_defect, type_enhancement, test_type, test_thumbnail,
        ]

        self.maxDiff = None
        from stalker_pyramid2 import entity_type_to_url
        expected_response = [
            {
                'id': r.id,
                '$ref': '%s/%s' % (entity_type_to_url[r.entity_type], r.id),
                'name': r.name,
                'entity_type': r.entity_type
            } for r in all_data
        ]

        self.assertEqual(
            sorted(response.json_body, key=lambda x: x['id']),
            sorted(expected_response, key=lambda x: x['id'])
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if the update_entity() method is working properly when the
        request method is PATCH
        """
        from stalker import db, Entity, User
        test_user_1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_1)

        test_user_2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_2)

        test_entity = Entity(
            name='Test Entity',
            created_by=test_user_1
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.method = 'PATCH'
        request.matchdict['id'] = test_entity.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Entity Name'
        request.params['description'] = 'New Description'
        request.params['updated_by_id'] = test_user_2.id

        self.patch_logged_in_user(request)

        entity_view = entity.EntityViews(request)
        entity_view.update_entity()

        test_entity_db = Entity.query.get(test_entity.id)
        self.assertEqual(
            test_entity_db.name,
            'New Entity Name'
        )
        self.assertEqual(
            test_entity_db.description,
            'New Description'
        )
        self.assertEqual(
            test_entity_db.updated_by,
            test_user_2
        )

    def test_update_entity_is_working_properly_with_post(self):
        """testing if the update_entity() method is working properly when the
        request method is POST
        """
        from stalker import db, Entity, User
        test_user_1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_1)

        test_user_2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_2)

        test_entity = Entity(
            name='Test Entity',
            created_by=test_user_1
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.method = 'POST'
        request.matchdict['id'] = test_entity.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Entity Name'
        request.params['description'] = 'New Description'
        request.params['updated_by_id'] = test_user_2.id

        self.patch_logged_in_user(request)

        entity_view = entity.EntityViews(request)
        entity_view.update_entity()

        test_entity_db = Entity.query.get(test_entity.id)
        self.assertEqual(
            test_entity_db.name,
            'New Entity Name'
        )
        self.assertEqual(
            test_entity_db.description,
            'New Description'
        )
        self.assertEqual(
            test_entity_db.updated_by,
            test_user_2
        )

    def test_get_notes_is_working_properly(self):
        """testing get_notes() is working properly
        """
        # create a test entity with notes
        from stalker import db, Entity, Note
        # test note 1
        test_note1 = Note(
            content='Test note 1'
        )
        db.DBSession.add(test_note1)

        # test note 2
        test_note2 = Note(
            content='Test note 2'
        )
        db.DBSession.add(test_note2)

        # test note 3
        test_note3 = Note(
            content='Test note 3'
        )
        db.DBSession.add(test_note3)

        # some other note
        test_note4 = Note(
            content='Test note 4'
        )
        db.DBSession.add(test_note4)

        test_entity = Entity(
            name='Test Entity',
            notes=[test_note1, test_note2, test_note3]
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        dummy_request = DummyRequest()
        dummy_request.matchdict['id'] = test_entity.id
        entity_view = entity.EntityViews(dummy_request)

        response = entity_view.get_notes()

        self.assertEqual(
            sorted(response.json_body),
            sorted(
                [{
                    'id': n.id,
                    '$ref': '/api/notes/%s' % n.id,
                    'name': n.name,
                    'entity_type': n.entity_type
                } for n in [test_note1, test_note2, test_note3]]
            )
        )

    # TAGS
    def test_get_tags_is_working_properly(self):
        """testing if get tags is working properly
        """
        # create some tags
        from stalker import db, Tag
        t1 = Tag(name='tag1')
        t2 = Tag(name='tag2')
        t3 = Tag(name='tag3')

        # create a test entity
        from stalker import Entity
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)
        test_entity.tags = [t1, t2]
        db.DBSession.add_all([t1, t2, t3, test_entity])
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_entity.id

        # get the tags of the entity
        entity_view = entity.EntityViews(request)
        response = entity_view.get_tags()
        expected = [
            {
                'id': t1.id,
                '$ref': '/api/tags/%s' % t1.id,
                'name': 'tag1',
                'entity_type': 'Tag'
            },
            {
                'id': t2.id,
                '$ref': '/api/tags/%s' % t2.id,
                'name': 'tag2',
                'entity_type': 'Tag'
            }
        ]
        self.assertEqual(
            sorted(response.json_body),
            sorted(expected)
        )

    def test_update_tags_is_working_properly_with_post(self):
        """testing if the update_tags() view is working properly when the
        request.method is POST
        """
        # create some tags
        from stalker import db, Tag
        t1 = Tag(name='tag1')
        t2 = Tag(name='tag2')
        t3 = Tag(name='tag3')
        db.DBSession.add_all([t1, t2, t3])

        from stalker import Entity
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_entity.id

        request.method = 'POST'
        request.params = DummyMultiDict()
        request.params['tag'] = ['tag1', 'tag2']
        request.POST = request.params

        entity_view = entity.EntityViews(request)
        entity_view.update_tags()

        # now query entity tags
        test_entity = Entity.query.filter(Entity.id == test_entity.id).first()

        self.assertEqual(
            sorted([t.name for t in test_entity.tags]),
            sorted(['tag1', 'tag2'])
        )

    def test_update_tags_is_working_properly_with_patch(self):
        """testing if the update_tags() is working properly when the
        request method is patch
        """
        # create some tags
        from stalker import db, Tag
        t1 = Tag(name='tag1')
        t2 = Tag(name='tag2')
        t3 = Tag(name='tag3')

        from stalker import Entity
        test_entity = Entity(
            name='Test Entity',
            tags=[t1, t2]
        )
        db.DBSession.add_all([t1, t2, t3, test_entity])
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_entity.id

        request.method = 'PATCH'
        request.params = DummyMultiDict()
        request.params['tag'] = ['tag3']
        request.POST = request.params

        entity_view = entity.EntityViews(request)
        entity_view.update_tags()

        # now query user tags
        test_user1 = Entity.query.filter(Entity.id == test_entity.id).first()

        response = [t.name for t in test_user1.tags]
        expected = ['tag1', 'tag2', 'tag3']
        self.assertEqual(sorted(response), sorted(expected))

    def test_remove_tags_is_working_properly(self):
        """testing if the remove_tags() method is working properly
        """
        # create some tags
        from stalker import db, Tag
        t1 = Tag(name='tag1')
        t2 = Tag(name='tag2')
        t3 = Tag(name='tag3')

        from stalker import Entity
        test_entity = Entity(
            name='Test Entity',
            tags=[t1, t2, t3]
        )
        db.DBSession.add_all([t1, t2, t3, test_entity])
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.method = 'DELETE'
        request.matchdict['id'] = test_entity.id

        request.params = DummyMultiDict()
        request.params['tag'] = ['tag2', 'tag3']
        request.POST = request.params

        entity_view = entity.EntityViews(request)
        entity_view.remove_tags()

        # now query entity tags
        test_entity = Entity.query.filter(Entity.id == test_entity.id).first()

        response = [t.name for t in test_entity.tags]
        expected = ['tag1']
        self.assertEqual(sorted(response), sorted(expected))

    def test_remove_tags_is_working_properly_with_non_existing_tags(self):
        """testing if the remove_tags() method is working properly
        """
        # create some tags
        from stalker import db, Tag
        t1 = Tag(name='tag1')
        t2 = Tag(name='tag2')
        t3 = Tag(name='tag3')

        from stalker import Entity
        test_entity = Entity(
            name='Test Entity',
            tags=[t1, t2]
        )
        db.DBSession.add_all([t1, t2, t3, test_entity])
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.method = 'DELETE'
        request.matchdict['id'] = test_entity.id

        request.params = DummyMultiDict()
        request.params['tag'] = ['tag3']
        request.POST = request.params

        entity_view = entity.EntityViews(request)
        entity_view.remove_tags()

        # now query entity tags
        test_entity = Entity.query.filter(Entity.id == test_entity.id).first()

        response = [t.name for t in test_entity.tags]
        expected = ['tag1', 'tag2']
        self.assertEqual(sorted(response), sorted(expected))

    # NOTES
    def test_entity_notes_is_working_properly(self):
        """testing if get_notes is working properly
        """
        from stalker import db, Entity, Note
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)

        # Note 1
        test_note1 = Note(content='Note 1')
        db.DBSession.add(test_note1)

        # Note 2
        test_note2 = Note(content='Note 2')
        db.DBSession.add(test_note2)

        # Note 3
        test_note3 = Note(content='Note 3')
        db.DBSession.add(test_note3)

        # dummy Note 4
        test_note4 = Note(content='Note 4')
        db.DBSession.add(test_note4)

        test_entity.notes = [test_note1, test_note2, test_note3]
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_entity.id
        request.method = 'GET'

        entity_view = entity.EntityViews(request)
        response = entity_view.get_notes()

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': test_note1.id,
                    '$ref': '/api/notes/%s' % test_note1.id,
                    'name': test_note1.name,
                    'entity_type': 'Note'
                },
                {
                    'id': test_note2.id,
                    '$ref': '/api/notes/%s' % test_note2.id,
                    'name': test_note2.name,
                    'entity_type': 'Note'
                },
                {
                    'id': test_note3.id,
                    '$ref': '/api/notes/%s' % test_note3.id,
                    'name': test_note3.name,
                    'entity_type': 'Note'
                },
            ])
        )

    def test_update_notes_is_working_properly_with_patch(self):
        """testing if update_notes is working properly when the request method
        is PATCH
        """
        from stalker import db, Entity, Note
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)

        # Note 1
        test_note1 = Note(content='Note 1')
        db.DBSession.add(test_note1)

        # Note 2
        test_note2 = Note(content='Note 2')
        db.DBSession.add(test_note2)

        # Note 3
        test_note3 = Note(content='Note 3')
        db.DBSession.add(test_note3)

        # Note 4
        test_note4 = Note(content='Note 4')
        db.DBSession.add(test_note4)

        # Note 5
        test_note5 = Note(content='Note 5')
        db.DBSession.add(test_note5)

        test_entity.notes = [test_note1, test_note2, test_note3]
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_entity.id
        request.method = 'PATCH'

        # add the 4th and 5th notes
        request.params = DummyMultiDict()
        request.params['note_id'] = [test_note4.id, test_note5.id]
        request.POST = request.params

        entity_view = entity.EntityViews(request)
        entity_view.update_notes()

        test_entity = Entity.query.filter(Entity.id == test_entity.id).first()
        self.assertEqual(
            sorted(test_entity.notes),
            sorted([
                test_note1, test_note2, test_note3, test_note4, test_note5
            ])
        )

    def test_update_notes_is_working_properly_with_post(self):
        """testing if update_notes is working properly when the request method
        is POST
        """
        from stalker import db, Entity, Note
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)

        # Note 1
        test_note1 = Note(content='Note 1')
        db.DBSession.add(test_note1)

        # Note 2
        test_note2 = Note(content='Note 2')
        db.DBSession.add(test_note2)

        # Note 3
        test_note3 = Note(content='Note 3')
        db.DBSession.add(test_note3)

        # Note 4
        test_note4 = Note(content='Note 4')
        db.DBSession.add(test_note4)

        # Note 5
        test_note5 = Note(content='Note 5')
        db.DBSession.add(test_note5)

        test_entity.notes = [test_note1, test_note2, test_note3]
        db.DBSession.commit()

        from stalker_pyramid2.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.matchdict['id'] = test_entity.id
        request.method = 'POST'

        # add the 4th and 5th notes
        request.params = DummyMultiDict()
        request.params['note_id'] = [test_note4.id, test_note5.id]
        request.POST = request.params

        entity_view = entity.EntityViews(request)
        entity_view.update_notes()

        test_entity = Entity.query.filter(Entity.id == test_entity.id).first()
        self.assertEqual(
            sorted(test_entity.notes),
            sorted([test_note4, test_note5])
        )

    def test_delete_entity_method_is_working_properly(self):
        """testing if the delete_entity() method is working properly
        """
        from stalker import db, Entity
        test_entity = Entity(
            name='Test Entity'
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        test_entity_db = Entity.query\
            .filter(Entity.name == test_entity.name).first()

        self.assertIsNotNone(test_entity_db)

        from stalker_pyramid2.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = test_entity_db.id

        entity_view = entity.EntityViews(request)
        entity_view.delete_entity()

        test_entity_db = Entity.query\
            .filter(Entity.name == test_entity.name).first()
        self.assertIsNone(test_entity_db)


class EntityViewFunctionalTests(FunctionalTestBase):
    """functional tests for the EntityView
    """

    def test_get_entity_view_is_working_properly(self):
        """testing if GET /api/entities/{id} view is working properly
        """

        # create a test entity
        from stalker import db, Entity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)
        test_entity = Entity(
            name='Test Entity',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/entities/%s' % test_entity.id,
            status=200
        )

        from stalker_pyramid2.views import EntityViewBase
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
                    EntityViewBase.milliseconds_since_epoch(date_created),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(date_created),
                'description': 'This is a test description',
                'entity_type': 'Entity',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            test_entity.id,
                    'length': 0
                },
                'id': test_entity.id,
                'name': 'Test Entity',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % test_entity.id,
                    'length': 0
                },
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % test_entity.id,
                    'length': 0
                },
                'thumbnail': {
                    'id': test_thumbnail.id,
                    '$ref': '/api/links/%s' % test_thumbnail.id,
                    'name': test_thumbnail.name,
                    'entity_type': 'Link'
                },
                'type': {
                    'id': test_entity.type_id,
                    '$ref': '/api/types/%s' % test_entity.type_id,
                    'name': test_entity.type.name,
                    'entity_type': 'Type'
                },
                'updated_by': {
                    'id': self.admin.id,
                    '$ref': '/api/users/%s' % self.admin.id,
                    'name': self.admin.name,
                    'entity_type': 'User'
                },
            }
        )

    def test_get_entities_view_is_working_properly(self):
        """testing if GET /api/entities view is working properly
        """
        # create a couple of test entities
        from stalker import db, Entity, Type
        test_type = Type(
            name='Test User',
            code='testuser',
            target_entity_type='User'
        )
        db.DBSession.add(test_type)

        from stalker import Link
        test_thumbnail = Link(
            full_path='/some/full/path'
        )
        db.DBSession.add(test_thumbnail)

        import datetime
        date_created = datetime.datetime(2016, 6, 20, 13, 55)

        # Test Entity 1
        test_entity1 = Entity(
            name='Test Entity 1',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity1)

        # Test Entity 2
        test_entity2 = Entity(
            name='Test Entity 2',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity2)

        # Test Entity 3
        test_entity3 = Entity(
            name='Test Entity 3',
            description='This is a test description',
            created_by=self.admin,
            type=test_type,
            date_created=date_created,
            thumbnail=test_thumbnail
        )
        db.DBSession.add(test_entity3)

        # commit data
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/entities',
            status=200
        )

        # admins department
        admins_department = Entity.query \
            .filter(Entity.name == 'admins') \
            .filter(Entity.entity_type == 'Department') \
            .first()

        # admins group
        admins_group = Entity.query \
            .filter(Entity.name == 'admins') \
            .filter(Entity.entity_type == 'Group') \
            .first()

        # Statuses
        status_new = Entity.query \
            .filter(Entity.name == 'New').first()
        status_accepted = Entity.query \
            .filter(Entity.name == 'Accepted').first()
        status_assigned = Entity.query \
            .filter(Entity.name == 'Assigned').first()
        status_reopened = Entity.query \
            .filter(Entity.name == 'Reopened').first()
        status_closed = Entity.query \
            .filter(Entity.name == 'Closed').first()
        status_open = Entity.query \
            .filter(Entity.name == 'Open').first()
        status_wfd = Entity.query \
            .filter(Entity.name == 'Waiting For Dependency').first()
        status_rts = Entity.query \
            .filter(Entity.name == 'Ready To Start').first()
        status_wip = Entity.query \
            .filter(Entity.name == 'Work In Progress').first()
        status_prev = Entity.query \
            .filter(Entity.name == 'Pending Review').first()
        status_hrev = Entity.query \
            .filter(Entity.name == 'Has Revision').first()
        status_drev = Entity.query \
            .filter(Entity.name == 'Dependency Has Revision').first()
        status_oh = Entity.query \
            .filter(Entity.name == 'On Hold').first()
        status_stop = Entity.query \
            .filter(Entity.name == 'Stopped').first()
        status_cmpl = Entity.query \
            .filter(Entity.name == 'Completed').first()
        status_rrev = Entity.query \
            .filter(Entity.name == 'Requested Revision').first()
        status_app = Entity.query \
            .filter(Entity.name == 'Approved').first()

        # Status Lists
        ticket_statuses = Entity.query \
            .filter(Entity.name == 'Ticket Statuses').first()
        daily_statuses = Entity.query \
            .filter(Entity.name == 'Daily Statuses').first()
        task_statuses = Entity.query \
            .filter(Entity.name == 'Task Statuses').first()
        asset_statuses = Entity.query \
            .filter(Entity.name == 'Asset Statuses').first()
        shot_statuses = Entity.query \
            .filter(Entity.name == 'Shot Statuses').first()
        sequence_statuses = Entity.query \
            .filter(Entity.name == 'Sequence Statuses').first()
        review_statuses = Entity.query \
            .filter(Entity.name == 'Review Statuses').first()

        # Types
        type_defect = Entity.query \
            .filter(Entity.name == 'Defect').first()
        type_enhancement = Entity.query \
            .filter(Entity.name == 'Enhancement').first()

        all_data = [
            test_entity1, test_entity2, test_entity3,
            admins_department, admins_group, self.admin,
            status_new, status_accepted, status_assigned, status_reopened,
            status_closed, status_open, status_wfd, status_rts, status_wip,
            status_prev, status_hrev, status_drev, status_oh, status_stop,
            status_cmpl, status_rrev, status_app,
            ticket_statuses, daily_statuses, task_statuses, asset_statuses,
            shot_statuses, sequence_statuses, review_statuses,
            type_defect, type_enhancement, test_type, test_thumbnail,
        ]

        self.maxDiff = None
        from stalker_pyramid2 import entity_type_to_url
        expected_response = [
            {
                'id': r.id,
                '$ref': '%s/%s' % (entity_type_to_url[r.entity_type], r.id),
                'name': r.name,
                'entity_type': r.entity_type
            } for r in all_data
        ]

        self.assertEqual(
            sorted(response.json_body, key=lambda x: x['id']),
            sorted(expected_response, key=lambda x: x['id'])
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/entities/{id} is working properly
        """
        from stalker import db, Entity, User
        test_user_1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_1)

        test_user_2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_2)

        test_entity = Entity(
            name='Test Entity',
            created_by=test_user_1
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        self.test_app.patch(
            '/api/entities/%s' % test_entity.id,
            params={
                'name': 'New Entity Name',
                'description': 'New Description',
                'updated_by_id': test_user_2.id
            },
            status=200
        )

        test_entity_db = Entity.query.get(test_entity.id)
        self.assertEqual(
            test_entity_db.name,
            'New Entity Name'
        )
        self.assertEqual(
            test_entity_db.description,
            'New Description'
        )
        self.assertEqual(
            test_entity_db.updated_by,
            test_user_2
        )

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/entities/{id} is working properly
        """
        from stalker import db, Entity, User
        test_user_1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_1)

        test_user_2 = User(
            name='Test User 2',
            login='tuser2',
            email='tuser2@user.com',
            password='secret'
        )
        db.DBSession.add(test_user_2)

        test_entity = Entity(
            name='Test Entity',
            created_by=test_user_1
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        self.test_app.post(
            '/api/entities/%s' % test_entity.id,
            params={
                'name': 'New Entity Name',
                'description': 'New Description',
                'updated_by_id': test_user_2.id
            },
            status=200
        )

        test_entity_db = Entity.query.get(test_entity.id)
        self.assertEqual(
            test_entity_db.name,
            'New Entity Name'
        )
        self.assertEqual(
            test_entity_db.description,
            'New Description'
        )
        self.assertEqual(
            test_entity_db.updated_by,
            test_user_2
        )

    def test_get_tags_view_is_working_properly(self):
        """testing if the GET /api/entities/{id}/tags view is working properly
        """
        from stalker import db, User, Tag
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@gmail.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        tag1 = Tag(name='Tag1')
        tag2 = Tag(name='Tag2')
        tag3 = Tag(name='Tag3')
        tag4 = Tag(name='Tag4')
        tag5 = Tag(name='Tag5')
        db.DBSession.add_all([tag1, tag2, tag3, tag4, tag5])

        test_user1.tags = [tag1, tag2, tag3]

        import transaction
        transaction.commit()

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        response = self.test_app.get(
            '/api/entities/%s/tags' % test_user1.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': tag1.id,
                    '$ref': '/api/tags/%s' % tag1.id,
                    'name': 'Tag1',
                    'entity_type': 'Tag'
                },
                {
                    'id': tag2.id,
                    '$ref': '/api/tags/%s' % tag2.id,
                    'name': 'Tag2',
                    'entity_type': 'Tag'
                },
                {
                    'id': tag3.id,
                    '$ref': '/api/tags/%s' % tag3.id,
                    'name': 'Tag3',
                    'entity_type': 'Tag'
                }
            ])
        )

    def test_patch_tags_view_is_working_properly(self):
        """testing if the PATCH /api/entities/{id}/tags view is working
        properly
        """
        from stalker import db, User, Tag
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@gmail.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        tag1 = Tag(name='Tag1')
        tag2 = Tag(name='Tag2')
        tag3 = Tag(name='Tag3')
        tag4 = Tag(name='Tag4')
        tag5 = Tag(name='Tag5')
        db.DBSession.add_all([tag1, tag2, tag3, tag4, tag5])

        test_user1.tags = [tag1, tag2, tag3]

        import transaction
        transaction.commit()

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        self.test_app.patch(
            '/api/entities/%s/tags?tag=%s' % (test_user1.id, tag4.name),
            status=200
        )

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        self.assertEqual(
            sorted([tag.name for tag in test_user1.tags]),
            ['Tag1', 'Tag2', 'Tag3', 'Tag4']
        )

    def test_put_tags_view_will_raise_404(self):
        """testing if the PUT /api/entities/{id}/tags view will return 404
        """
        from stalker import db, User, Tag
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@gmail.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        tag1 = Tag(name='Tag1')
        tag2 = Tag(name='Tag2')
        tag3 = Tag(name='Tag3')
        tag4 = Tag(name='Tag4')
        tag5 = Tag(name='Tag5')
        db.DBSession.add_all([tag1, tag2, tag3, tag4, tag5])

        test_user1.tags = [tag1, tag2, tag3]

        import transaction
        transaction.commit()

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        self.test_app.put(
            '/api/entities/%s/tags?tag=%s' % (test_user1.id, tag4.name),
            status=404
        )

    def test_post_tags_view_is_working_properly(self):
        """testing if the POST /api/entities/{id}/tags view is working properly
        """
        from stalker import db, User, Tag
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@gmail.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        tag1 = Tag(name='Tag1')
        tag2 = Tag(name='Tag2')
        tag3 = Tag(name='Tag3')
        tag4 = Tag(name='Tag4')
        tag5 = Tag(name='Tag5')
        db.DBSession.add_all([tag1, tag2, tag3, tag4, tag5])

        test_user1.tags = [tag1, tag2, tag3]

        import transaction
        transaction.commit()

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        self.test_app.post(
            '/api/entities/%s/tags?tag=%s' % (test_user1.id, tag4.name),
            status=200
        )

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        self.assertEqual(
            sorted([tag.name for tag in test_user1.tags]),
            ['Tag4']
        )

    def test_delete_tags_view_is_working_properly(self):
        """testing if the DELETE /api/entities/{id}/tags view is working
        properly
        """
        from stalker import db, User, Tag
        test_user1 = User(
            name='Test User 1',
            login='tuser1',
            email='tuser1@gmail.com',
            password='secret'
        )
        db.DBSession.add(test_user1)

        tag1 = Tag(name='Tag1')
        tag2 = Tag(name='Tag2')
        tag3 = Tag(name='Tag3')
        tag4 = Tag(name='Tag4')
        tag5 = Tag(name='Tag5')
        db.DBSession.add_all([tag1, tag2, tag3, tag4, tag5])

        test_user1.tags = [tag1, tag2, tag3]

        import transaction
        transaction.commit()

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        self.test_app.delete(
            '/api/entities/%s/tags?tag=%s' % (test_user1.id, tag3.name),
            status=200
        )

        test_user1 = User.query.filter(User.login == test_user1.login).first()
        self.assertEqual(
            sorted([tag.name for tag in test_user1.tags]),
            ['Tag1', 'Tag2']
        )

    def test_get_notes_view_is_working_properly(self):
        """testing if GET /api/entities/{id}/notes view is working properly
        """
        from stalker import db, Entity, Note
        test_entity = Entity(
            name='Test Entity'
        )
        db.DBSession.add(test_entity)

        test_note1 = Note(
            description='This is a Test note 1'
        )
        db.DBSession.add(test_note1)

        test_note2 = Note(
            description='This is a Test note 2'
        )
        db.DBSession.add(test_note2)

        test_entity.notes = [test_note1, test_note2]
        db.DBSession.commit()

        response = self.test_app.get(
            '/api/entities/%s/notes' % test_entity.id,
            status=200
        )

        self.assertEqual(
            sorted(response.json_body),
            sorted([
                {
                    'id': test_note1.id,
                    '$ref': '/api/notes/%s' % test_note1.id,
                    'name': test_note1.name,
                    'entity_type': test_note1.entity_type
                },
                {
                    'id': test_note2.id,
                    '$ref': '/api/notes/%s' % test_note2.id,
                    'name': test_note2.name,
                    'entity_type': test_note2.entity_type
                }
            ])
        )

    def test_update_notes_is_working_properly_with_patch(self):
        """testing if PATCH /api/entities/{id}/notes view is working properly
        """
        from stalker import db, Entity, Note
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)

        # Note 1
        test_note1 = Note(content='Note 1')
        db.DBSession.add(test_note1)

        # Note 2
        test_note2 = Note(content='Note 2')
        db.DBSession.add(test_note2)

        # Note 3
        test_note3 = Note(content='Note 3')
        db.DBSession.add(test_note3)

        # Note 4
        test_note4 = Note(content='Note 4')
        db.DBSession.add(test_note4)

        # Note 5
        test_note5 = Note(content='Note 5')
        db.DBSession.add(test_note5)

        test_entity.notes = [test_note1, test_note2, test_note3]
        db.DBSession.commit()

        self.test_app.patch(
            '/api/entities/%s/notes' % test_entity.id,
            params={
                'note_id': [test_note4.id, test_note5.id]
            },
            status=200
        )

        test_entity = Entity.query.filter(Entity.id == test_entity.id).first()
        self.assertEqual(
            sorted(test_entity.notes),
            sorted([
                test_note1, test_note2, test_note3, test_note4, test_note5
            ])
        )

    def test_update_notes_is_working_properly_with_post(self):
        """testing if POST /api/entities/{id}/notes is working properly
        """
        from stalker import db, Entity, Note
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)

        # Note 1
        test_note1 = Note(content='Note 1')
        db.DBSession.add(test_note1)

        # Note 2
        test_note2 = Note(content='Note 2')
        db.DBSession.add(test_note2)

        # Note 3
        test_note3 = Note(content='Note 3')
        db.DBSession.add(test_note3)

        # Note 4
        test_note4 = Note(content='Note 4')
        db.DBSession.add(test_note4)

        # Note 5
        test_note5 = Note(content='Note 5')
        db.DBSession.add(test_note5)

        test_entity.notes = [test_note1, test_note2, test_note3]
        db.DBSession.commit()

        self.test_app.post(
            '/api/entities/%s/notes' % test_entity.id,
            params={
                'note_id': [test_note4.id, test_note5.id]
            },
            status=200
        )

        test_entity = Entity.query.filter(Entity.id == test_entity.id).first()
        self.assertEqual(
            sorted(test_entity.notes),
            sorted([test_note4, test_note5])
        )

    def test_update_notes_is_working_properly_with_put(self):
        """testing if PUT: /api/entities/{id}/notes should raise 404
        """
        from stalker import db, Entity, Note
        test_entity = Entity(name='Test Entity')
        db.DBSession.add(test_entity)

        # Note 1
        test_note1 = Note(content='Note 1')
        db.DBSession.add(test_note1)

        # Note 2
        test_note2 = Note(content='Note 2')
        db.DBSession.add(test_note2)

        # Note 3
        test_note3 = Note(content='Note 3')
        db.DBSession.add(test_note3)

        # Note 4
        test_note4 = Note(content='Note 4')
        db.DBSession.add(test_note4)

        # Note 5
        test_note5 = Note(content='Note 5')
        db.DBSession.add(test_note5)

        test_entity.notes = [test_note1, test_note2, test_note3]
        db.DBSession.commit()

        self.test_app.put(
            '/api/entities/%s/notes' % test_entity.id,
            params={
                'note_id': [test_note4.id, test_note5.id]
            },
            status=404
        )

    def test_delete_entity_method_is_working_properly(self):
        """testing if DELETE /api/entities/{id} is working properly
        """
        from stalker import db, Entity
        test_entity = Entity(
            name='Test Entity'
        )
        db.DBSession.add(test_entity)
        db.DBSession.commit()

        test_entity_db = Entity.query\
            .filter(Entity.name == test_entity.name).first()

        self.assertIsNotNone(test_entity_db)

        self.test_app.delete(
            '/api/entities/%s' % test_entity_db.id,
            status=200
        )

        test_entity_db = Entity.query\
            .filter(Entity.name == test_entity.name).first()
        self.assertIsNone(test_entity_db)
