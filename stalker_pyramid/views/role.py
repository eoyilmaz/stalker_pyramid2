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


from pyramid.view import view_defaults, view_config
from stalker_pyramid.views.entity import EntityViews

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class RoleViews(EntityViews):
    """views for Role class
    """
    from stalker import Role
    som_class = Role

    @view_config(
        route_name='role',
        request_method='GET'
    )
    def get_entity(self):
        """returns one Role instance data as JSON
        """
        return super(RoleViews, self).get_entity()

    @view_config(
        route_name='roles',
        request_method='GET'
    )
    def get_entities(self):
        """returns all of the Role instances in the database as JSON
        """
        return super(RoleViews, self).get_entities()

    @view_config(
        route_name='role',
        request_method=['PATCH', 'POST']
    )
    def update_entity(self):
        """updates one Role instance
        """
        return super(RoleViews, self).update_entity()

    @view_config(
        route_name='roles',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a new Role instance
        """
        return super(RoleViews, self).create_entity()

    @view_config(
        route_name='role',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes a Role instance
        """
        return super(RoleViews, self).delete_entity()
