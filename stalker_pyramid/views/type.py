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

from stalker import Type
from stalker_pyramid.views.entity import EntityViews

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class TypeViews(EntityViews):
    """views for Type class
    """
    som_class = Type
    local_params = [
        {'param_name': 'target_entity_type', 'nullable': False},
        {'param_name': 'code', 'nullable': False}
    ]

    @view_config(
        route_name='type',
        request_method='GET',
    )
    def get_entity(self):
        """returns one Type instance data as json
        """
        sql = """select
            "Types".id,
            "Types".code
        from "Types"
        where "Types".id = :id
        """
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        from sqlalchemy import text
        result = conn.execute(text(sql), id=self.entity_id)

        r = result.fetchone()
        data = {
            'id': r[0],
            'code': r[1]
        }

        response = super(TypeViews, self).get_entity()
        return self.update_response_data(response, data)

    @view_config(
        route_name='types',
        request_method='GET',
    )
    def get_entities(self):
        """returns all Types in the database
        """
        return super(TypeViews, self).get_entities()

    @view_config(
        route_name='types',
        request_method='PUT',
    )
    def create_entity(self):
        """creates one Type instance
        """
        return super(TypeViews, self).create_entity()

    @view_config(
        route_name='type',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates a Type instance
        """
        return super(TypeViews, self).update_entity()

    @view_config(
        route_name='type',
        request_method='DELETE',
    )
    def delete_entity(self):
        """deletes one Type instance
        """
        return super(TypeViews, self).delete_entity()
