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

from beaker.cache import cache_region
from pyramid.view import view_config

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@cache_region('long_term', 'load_users')
def cached_group_finder(login_name):
    if ':' in login_name:
        login_name = login_name.split(':')[1]

    # return the group of the given User object
    from stalker import User
    user_obj = User.query.filter_by(login=login_name).first()
    if user_obj:
        # just return the groups names if there is any group
        groups = user_obj.groups
        if len(groups):
            return map(lambda x: 'Group:' + x.name, groups)
    return []


def group_finder(login_name, request):
    """Returns the group of the given login name. The login name will be in
    'User:{login}' format.

    :param login_name: The login name of the user, both '{login_name}' and
      'User:{login_name}' format is accepted.

    :param request: The Request object

    :return: Will return the groups of the user in ['Group:{group_name}']
      format.
    """
    return cached_group_finder(login_name)


class RootFactory(object):
    """The main purpose of having a root factory is to generate the objects
    used as the context by the request. But in our case it just used to
    determine the default ACLs.
    """

    @property
    def __acl__(self):
        # create the default acl and give admins all the permissions
        from stalker import defaults, User, Group, Permission
        all_permissions = map(
            lambda x: x.action + '_' + x.class_name,
            Permission.query.all()
        )

        # start with default ACLs

        ACLs = [
            ('Allow', 'Group:%s' % defaults.admin_department_name,
             all_permissions),
            ('Allow', 'User:%s' % defaults.admin_name, all_permissions)
        ]

        # get all users and their ACLs
        for user in User.query.all():
            ACLs.extend(user.__acl__)

        # get all groups and their ACLs
        for group in Group.query.all():
            ACLs.extend(group.__acl__)

        return ACLs

    def __init__(self, request):
        pass


@view_config(
    route_name='login',
    renderer='json'
)
def login(request):
    """the login view
    """
    logger.debug('login start')

    login_name = request.params.get('login', '')
    password = request.params.get('password', '')

    # get the user again (first got it in validation)
    from stalker import User
    from sqlalchemy import or_
    user = User.query \
        .filter(or_(User.login == login_name, User.email == login_name))\
        .first()

    if user and user.check_password(password):
        logger.debug('Login successful!')
        from pyramid.security import remember
        headers = remember(request, login_name)
        from stalker_pyramid2.views.user import UserViews
        user_view = UserViews(request)
        user_view.entity_id = user.id
        response = user_view.get_entity()
        response.headers = headers
        return response
    else:
        logger.debug('Bad Login')
        from pyramid.httpexceptions import HTTPUnauthorized
        return HTTPUnauthorized(detail='Bad Login')


@view_config(
    route_name='logout'
)
def logout(request):
    from pyramid.security import forget
    headers = forget(request)
    from pyramid.httpexceptions import HTTPFound
    return HTTPFound(
        location='/',
        headers=headers
    )


@view_config(
    route_name='home',
    renderer='angular/index.html'
)
def home(request):
    return {}
