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
from stalker_pyramid.views.entity import SimpleEntityViews
from stalker import Tag


@view_defaults(renderer='json')
class TagViews(SimpleEntityViews):
    """views for Tag instances
    """
    som_class = Tag
    local_params = [
        # simple arguments/attributes
        {'param_name': 'name', 'nullable': False}  # name should not be
                                                   # nullable in a Tag
    ]

    @view_config(
        route_name='tag',
        request_method='GET',
    )
    def get_entity(self):
        """returns one Tag instance
        """
        return super(TagViews, self).get_entity()

    @view_config(
        route_name='tags',
        request_method='GET',
    )
    def get_entities(self):
        """returns all the tags in database
        """
        return super(TagViews, self).get_entities()

    @view_config(
        route_name='tags',
        request_method='PUT',
    )
    def create_entity(self):
        """creates a tag instance
        """
        return super(TagViews, self).create_entity()

    @view_config(
        route_name='tag',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates one Tag instance
        """
        return super(TagViews, self).update_entity()

    @view_config(
        route_name='tag',
        request_method='DELETE',
    )
    def delete_entity(self):
        """deletes one tag instance
        """
        return super(TagViews, self).delete_entity()
