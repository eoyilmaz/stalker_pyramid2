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

import logging

from stalker import Note
from pyramid.view import view_defaults, view_config
from stalker_pyramid2.views.entity import SimpleEntityViews

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class NoteViews(SimpleEntityViews):
    """views for Note instances
    """
    som_class = Note
    local_params = [
        # simple arguments/attributes
        {'param_name': 'content'},
    ]

    @view_config(
        route_name='note',
        request_method='GET',
    )
    def get_entity(self):
        """returns one note instance
        """
        response = super(NoteViews, self).get_entity()
        data = response.json_body
        data['content'] = data['description']
        response.json_body = data
        return response

    @view_config(
        route_name='notes',
        request_method='GET',
    )
    def get_entities(self):
        """return multiple notes
        """
        return super(NoteViews, self).get_entities()

    @view_config(
        route_name='note',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates the given note
        """
        return super(NoteViews, self).update_entity()

    @view_config(
        route_name='notes',
        request_method='PUT',
    )
    def create_entity(self):
        """creates one note
        """
        return super(NoteViews, self).create_entity()

    @view_config(
        route_name='note',
        request_method='DELETE',
    )
    def delete_entity(self):
        """deletes a note
        """
        return super(NoteViews, self).delete_entity()
