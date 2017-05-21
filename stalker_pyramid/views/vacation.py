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

from stalker import Vacation
from pyramid.view import view_defaults, view_config
from stalker_pyramid.views import (simple_entity_interpreter,
                                   datetime_interpreter)
from stalker_pyramid.views.entity import SimpleEntityViews

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class VacationViews(SimpleEntityViews):
    """the vacations view
    """
    som_class = Vacation
    local_params = [
        {
            'param_name': 'end',
            'interpreter': datetime_interpreter,
            'nullable': False,
        },
        {
            'param_name': 'start',
            'interpreter': datetime_interpreter,
            'nullable': False,
        },
        {
            'param_name': 'user_id',
            'arg_name': 'user',
            'nullable': False,
            'interpreter': simple_entity_interpreter
        },
    ]

    @view_config(
        route_name='vacation',
        request_method='GET',
    )
    def get_entity(self):
        """returns stalker.models.vacation.Vacation instance
        """
        sql = """
        select
          "Vacations".id,
          (extract(epoch from "Vacations".start::timestamp at time zone 'UTC') * 1000)::bigint as start,
          (extract(epoch from "Vacations".end::timestamp at time zone 'UTC') * 1000)::bigint as end,
          "Vacations".user_id,
          "User_SimpleEntities".name,
          "User_SimpleEntities".entity_type
        from "Vacations"
        left outer join "SimpleEntities" as "User_SimpleEntities" on "Vacations".user_id = "User_SimpleEntities".id
        where "Vacations".id = :id
        """

        from stalker.db.session import DBSession
        conn = DBSession.connection()
        from sqlalchemy import text
        result = conn.execute(text(sql), id=self.entity_id)
        r = result.fetchone()

        from stalker_pyramid import entity_type_to_url
        data = {
            'id': r[0],
            'start': r[1],
            'end': r[2],
            'user': {
                'id': r[3],
                '$ref': '%s/%s' % (entity_type_to_url[r[5]], r[3]),
                'name': r[4],
                'entity_type': r[5]
            }
        }

        response = super(VacationViews, self).get_entity()
        return self.update_response_data(response, data)

    @view_config(
        route_name='vacations',
        request_method='GET',
    )
    def get_entities(self):
        """returns vacations
        """
        return super(VacationViews, self).get_entities()

    @view_config(
        route_name='vacations',
        request_method='PUT',
    )
    def create_entity(self):
        """creates vacation
        """
        return super(VacationViews, self).create_entity()

    @view_config(
        route_name='vacation',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates the vacation instance
        """
        # update super data
        return super(VacationViews, self).update_entity()

    @view_config(
        route_name='vacation',
        request_method='DELETE',
    )
    def delete_entity(self):
        """deletes a vacation instance
        """
        return super(VacationViews, self).delete_entity()
