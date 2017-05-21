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
from stalker_pyramid.views import repository


class RepositoryViewsUnitTestCase(UnitTestBase):
    """unit tests for RepositoryViews class
    """

    def setUp(self):
        """create test data
        """
        super(RepositoryViewsUnitTestCase, self).setUp()

        from stalker import db, Repository
        self.test_repo1 = Repository(
            name='Test Repo 1',
            windows_path='T:/Projects/',
            linux_path='/mnt/T/Projects/',
            osx_path='/Volumes/T/Project/',
            created_by=self.admin
        )
        db.DBSession.add(self.test_repo1)

        self.test_repo2 = Repository(
            name='Test Repo 2',
            windows_path='T:/Projects/',
            linux_path='/mnt/T/Projects/',
            osx_path='/Volumes/T/Project/',
            created_by=self.admin
        )
        db.DBSession.add(self.test_repo2)

        self.test_repo3 = Repository(
            name='Test Repo 3',
            windows_path='T:/Projects/',
            linux_path='/mnt/T/Projects/',
            osx_path='/Volumes/T/Project/',
            created_by=self.admin
        )
        db.DBSession.add(self.test_repo3)

        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if get_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_repo1.id
        repo_view = repository.RepositoryViews(request)

        response = repo_view.get_entity()

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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_repo1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_repo1.date_updated
                    ),
                'description': '',
                'entity_type': 'Repository',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_repo1.id,
                    'length': 0
                },
                'id': self.test_repo1.id,
                'linux_path': self.test_repo1.linux_path,
                'name': 'Test Repo 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_repo1.id,
                    'length': 0
                },
                'osx_path': self.test_repo1.osx_path,
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_repo1.id,
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
                'windows_path': self.test_repo1.windows_path,
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if get_entities() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        repo_view = repository.RepositoryViews(request)

        response = repo_view.get_entities()

        from stalker import Repository
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Repository',
                    '$ref': '/api/repositories/%s' % r.id
                } for r in Repository.query.all()
            ]
        )

    def test_update_entity_is_working_properly(self):
        """testing if update_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict

        request = DummyRequest()
        request.matchdict['id'] = self.test_repo1.id

        request.params = DummyMultiDict()
        request.params['name'] = 'New Repo Name'
        request.params['description'] = 'New description'
        request.params['windows_path'] = 'C:/new/windows/path/'
        request.params['linux_path'] = '/mnt/new/linux/path/'
        request.params['osx_path'] = '/Volumes/new/osx/path/'

        repo_view = repository.RepositoryViews(request)

        self.patch_logged_in_user(request)
        response = repo_view.update_entity()

        from stalker import Repository
        repo_db = Repository.query.get(self.test_repo1.id)

        self.assertEqual(repo_db.name, 'New Repo Name')
        self.assertEqual(repo_db.description, 'New description')
        self.assertEqual(repo_db.windows_path, 'C:/new/windows/path/')
        self.assertEqual(repo_db.linux_path, '/mnt/new/linux/path/')
        self.assertEqual(repo_db.osx_path, '/Volumes/new/osx/path/')

    def test_create_entity_is_working_properly(self):
        """testing if create_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest, DummyMultiDict
        request = DummyRequest()
        request.params = DummyMultiDict()
        request.params['name'] = 'New Repository'
        request.params['windows_path'] = 'T:/new/repo/'
        request.params['linux_path'] = '/mnt/T/new/repo/'
        request.params['osx_path'] = '/Volumes/T/new/repo/'
        request.params['description'] = 'this is a new test repo'
        request.params['created_by_id'] = 3

        repo_view = repository.RepositoryViews(request)

        self.patch_logged_in_user(request)
        response = repo_view.create_entity()

        from stalker import Repository
        repo_db = Repository.query\
            .filter(Repository.name == 'New Repository')\
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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        repo_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        repo_db.date_updated
                    ),
                'description': 'this is a new test repo',
                'entity_type': 'Repository',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            repo_db.id,
                    'length': 0
                },
                'id': repo_db.id,
                'linux_path': '/mnt/T/new/repo/',
                'name': 'New Repository',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % repo_db.id,
                    'length': 0
                },
                'osx_path': '/Volumes/T/new/repo/',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % repo_db.id,
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
                'windows_path': 'T:/new/repo/',
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if delete_entity() method is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        request.matchdict['id'] = self.test_repo1.id

        repo_view = repository.RepositoryViews(request)

        self.patch_logged_in_user(request)
        response = repo_view.delete_entity()

        from stalker import Repository
        self.assertIsNone(
            Repository.query.filter(
                Repository.id == self.test_repo1.id
            ).first()
        )


class RepositoryViewsFunctionalTestCase(FunctionalTestBase):
    """functional tests for RepositoryViews class
    """

    def setUp(self):
        """create test data
        """
        super(RepositoryViewsFunctionalTestCase, self).setUp()

        from stalker import db, Repository
        self.test_repo1 = Repository(
            name='Test Repo 1',
            windows_path='T:/Projects/',
            linux_path='/mnt/T/Projects/',
            osx_path='/Volumes/T/Project/',
            created_by=self.admin
        )
        db.DBSession.add(self.test_repo1)

        self.test_repo2 = Repository(
            name='Test Repo 2',
            windows_path='T:/Projects/',
            linux_path='/mnt/T/Projects/',
            osx_path='/Volumes/T/Project/',
            created_by=self.admin
        )
        db.DBSession.add(self.test_repo2)

        self.test_repo3 = Repository(
            name='Test Repo 3',
            windows_path='T:/Projects/',
            linux_path='/mnt/T/Projects/',
            osx_path='/Volumes/T/Project/',
            created_by=self.admin
        )
        db.DBSession.add(self.test_repo3)

        db.DBSession.commit()

    def test_get_entity_is_working_properly(self):
        """testing if GET: /api/entities/{id} view is working properly
        """
        response = self.test_app.get(
            '/api/repositories/%s' % self.test_repo1.id,
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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_repo1.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        self.test_repo1.date_updated
                    ),
                'description': '',
                'entity_type': 'Repository',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            self.test_repo1.id,
                    'length': 0
                },
                'id': self.test_repo1.id,
                'linux_path': self.test_repo1.linux_path,
                'name': 'Test Repo 1',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % self.test_repo1.id,
                    'length': 0
                },
                'osx_path': self.test_repo1.osx_path,
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % self.test_repo1.id,
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
                'windows_path': self.test_repo1.windows_path,
            }
        )

    def test_get_entities_is_working_properly(self):
        """testing if GET: /api/repositories view is working properly
        """
        from stalker_pyramid.testing import DummyRequest
        request = DummyRequest()
        repo_view = repository.RepositoryViews(request)

        response = self.test_app.get(
            '/api/repositories',
            status=200
        )

        from stalker import Repository
        self.assertEqual(
            response.json_body,
            [
                {
                    'id': r.id,
                    'name': r.name,
                    'entity_type': 'Repository',
                    '$ref': '/api/repositories/%s' % r.id
                } for r in Repository.query.all()
            ]
        )

    def test_update_entity_is_working_properly_with_patch(self):
        """testing if PATCH: /api/repositories/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.patch(
            '/api/repositories/%s' % self.test_repo1.id,
            status=200,
            params={
                'name': 'New Repo Name',
                'description': 'New description',
                'windows_path': 'C:/new/windows/path/',
                'linux_path': '/mnt/new/linux/path/',
                'osx_path': '/Volumes/new/osx/path/',
            }
        )

        from stalker import Repository
        repo_db = Repository.query.get(self.test_repo1.id)

        self.assertEqual(repo_db.name, 'New Repo Name')
        self.assertEqual(repo_db.description, 'New description')
        self.assertEqual(repo_db.windows_path, 'C:/new/windows/path/')
        self.assertEqual(repo_db.linux_path, '/mnt/new/linux/path/')
        self.assertEqual(repo_db.osx_path, '/Volumes/new/osx/path/')

    def test_update_entity_is_working_properly_with_post(self):
        """testing if POST: /api/repositories/{id} view is working properly
        """
        self.admin_login()
        response = self.test_app.post(
            '/api/repositories/%s' % self.test_repo1.id,
            status=200,
            params={
                'name': 'New Repo Name',
                'description': 'New description',
                'windows_path': 'C:/new/windows/path/',
                'linux_path': '/mnt/new/linux/path/',
                'osx_path': '/Volumes/new/osx/path/',
            }
        )

        from stalker import Repository
        repo_db = Repository.query.get(self.test_repo1.id)

        self.assertEqual(repo_db.name, 'New Repo Name')
        self.assertEqual(repo_db.description, 'New description')
        self.assertEqual(repo_db.windows_path, 'C:/new/windows/path/')
        self.assertEqual(repo_db.linux_path, '/mnt/new/linux/path/')
        self.assertEqual(repo_db.osx_path, '/Volumes/new/osx/path/')

    def test_create_entity_is_working_properly(self):
        """testing if PUT: /api/repositories view is working properly
        """
        self.admin_login()
        response = self.test_app.put(
            '/api/repositories',
            params={
                'name': 'New Repository',
                'windows_path': 'T:/new/repo/',
                'linux_path': '/mnt/T/new/repo/',
                'osx_path': '/Volumes/T/new/repo/',
                'description': 'this is a new test repo',
                'created_by_id': 3,
            },
            status=201
        )

        from stalker import Repository
        repo_db = Repository.query\
            .filter(Repository.name == 'New Repository')\
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
                'date_created':
                    EntityViewBase.milliseconds_since_epoch(
                        repo_db.date_created
                    ),
                'date_updated':
                    EntityViewBase.milliseconds_since_epoch(
                        repo_db.date_updated
                    ),
                'description': 'this is a new test repo',
                'entity_type': 'Repository',
                'generic_text': '',
                'generic_data': {
                    '$ref': '/api/simple_entities/%s/generic_data' %
                            repo_db.id,
                    'length': 0
                },
                'id': repo_db.id,
                'linux_path': '/mnt/T/new/repo/',
                'name': 'New Repository',
                'notes': {
                    '$ref': '/api/entities/%s/notes' % repo_db.id,
                    'length': 0
                },
                'osx_path': '/Volumes/T/new/repo/',
                'stalker_version': stalker.__version__,
                'tags': {
                    '$ref': '/api/entities/%s/tags' % repo_db.id,
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
                'windows_path': 'T:/new/repo/',
            }
        )

    def test_delete_entity_is_working_properly(self):
        """testing if DELETE: /api/repositories/{id} view is working properly
        """
        response = self.test_app.delete(
            '/api/repositories/%s' % self.test_repo1.id,
            status=200
        )

        from stalker import Repository
        self.assertIsNone(
            Repository.query.filter(
                Repository.id == self.test_repo1.id
            ).first()
        )
