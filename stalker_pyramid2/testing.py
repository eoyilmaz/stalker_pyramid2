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



import unittest

from pyramid.decorator import reify
from pyramid.testing import DummyRequest  # just to simplify imports


class DummyMultiDict(dict):
    """dummy MultiDict class for testing
    """

    def getall(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            return []


class DummyFileParam(object):
    """dummy FileParam object for testing
    """

    def __init__(self, filename=None, file=None):
        self.filename = filename
        self.file = file


class DummySession(object):
    """dummy session object for testing
    """

    def __init__(self):
        self.messages = []

    def flash(self, message):
        self.messages.append(message)


class UnitTestBase(unittest.TestCase):
    """the base for Stalker Pyramid Views unit tests
    """

    config = {
        'sqlalchemy.url':
            'postgresql://stalker_admin:stalker@localhost/stalker_test',
        'sqlalchemy.echo': False
    }

    def patch_logged_in_user(self, request):
        """patches the logged in user so it will always return the admin
        """
        # not a good way of patching it, but it saves the day for now
        from stalker_pyramid2.views import EntityViewBase
        orig_method = EntityViewBase.get_logged_in_user
        admin = self.admin

        def patched_f(*args, **kwargs):
            # replace the original
            EntityViewBase.get_logged_in_user = orig_method
            # and return the admin user
            from stalker import User
            return User.query.filter(User.login == 'admin').first()

        EntityViewBase.get_logged_in_user = patched_f

    def setUp(self):
        """setup test
        """
        import datetime
        from stalker import defaults
        defaults.timing_resolution = datetime.timedelta(hours=1)
        from pyramid import testing
        testing.setUp()

        # init database
        from stalker import db
        db.setup(self.config)
        db.init()

    def tearDown(self):
        """clean up the test
        """
        import datetime
        import transaction
        from stalker import defaults
        from stalker.db.session import DBSession
        from stalker.db.declarative import Base
        from pyramid import testing

        testing.tearDown()

        # clean up test database
        connection = DBSession.connection()
        engine = connection.engine
        connection.close()
        Base.metadata.drop_all(engine)
        transaction.commit()
        DBSession.remove()

        defaults.timing_resolution = datetime.timedelta(hours=1)

    @reify
    def admin(self):
        """returns the admin user
        """
        from stalker import User
        return User.query.filter(User.login == 'admin').first()


class FunctionalTestBase(unittest.TestCase):
    """functional tests for Vacation views
    """

    def setUp(self):
        """set up the test
        """
        import transaction
        from pyramid import paster, testing
        from webtest import TestApp
        from stalker import db
        from stalker.db.session import DBSession

        testing.setUp()
        import os
        import stalker_pyramid2
        app = paster.get_app(
            os.path.join(
                os.path.dirname(
                    stalker_pyramid2.__path__[0],
                ),
                'testing.ini'
            ).replace('\\', '/')
        )

        self.test_app = TestApp(app)

        # patch DBSession commit, to let the db.init() work
        # with its calls to DBSession.commit()
        _orig_commit = DBSession.commit
        DBSession.commit = transaction.commit
        db.setup(app.registry.settings)
        db.init()
        # restore DBSession.commit
        DBSession.commit = _orig_commit

        from stalker import User
        self.admin = User.query.filter(User.name == 'admin').first()

    def tearDown(self):
        """clean up the test
        """
        import datetime
        import transaction
        from stalker import defaults
        from stalker.db.declarative import Base
        from stalker.db.session import DBSession

        from pyramid import testing
        testing.tearDown()

        # clean up test database
        connection = DBSession.connection()
        engine = connection.engine
        connection.close()
        Base.metadata.drop_all(engine)
        transaction.commit()
        DBSession.remove()

        defaults.timing_resolution = datetime.timedelta(hours=1)

    def admin_login(self):
        """login as admin
        """
        self.test_app.post(
            '/api/login',
            params={
                'login': 'admin',
                'password': 'admin',
            },
            status=200
        )
