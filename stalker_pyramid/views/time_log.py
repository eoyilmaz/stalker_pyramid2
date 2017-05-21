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
from stalker import TimeLog

from stalker_pyramid.views import simple_entity_interpreter
from stalker_pyramid.views.entity import EntityViews
from stalker_pyramid.views.mixins import DateRangeMixinViews

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class TimeLogViews(EntityViews, DateRangeMixinViews):
    """views for TimeLog instances
    """
    som_class = TimeLog

    local_params = [
        # complex arguments/attributes
        {
            'param_name': 'task_id',
            'arg_name': 'task',
            'nullable': False,
            'interpreter': simple_entity_interpreter,
        },
        {
            'param_name': 'resource_id',
            'arg_name': 'resource',
            'nullable': False,
            'interpreter': simple_entity_interpreter,
        },
    ]

    @view_config(
        route_name='time_log',
        request_method='GET',
    )
    def get_entity(self):
        """returns one TimeLog instance as JSON
        """
        sql = """
        select
          "TimeLogs".resource_id,
          "SimpleEntities".name,
          "SimpleEntities".entity_type
        from "TimeLogs"
          left join "SimpleEntities" on "TimeLogs".resource_id = "SimpleEntities".id
        where "TimeLogs".id = :id
        """
        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        r = conn.execute(text(sql), id=self.entity_id).fetchone()

        from stalker_pyramid import entity_type_to_url
        data = {
            'resource': {
                'id': r[0],
                'name': r[1],
                'entity_type': r[2],
                '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0]),
            } if r else None,
        }
        data.update(DateRangeMixinViews.get_entity(self))
        entity_response = super(TimeLogViews, self).get_entity()

        return self.update_response_data(entity_response, data)

    @view_config(
        route_name='time_logs',
        request_method='GET',
    )
    def get_entities(self):
        """returns multiple TimeLog instances as JSON
        """
        return super(TimeLogViews, self).get_entities()

    @view_config(
        route_name='time_log',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates one TimeLog instance
        """
        return super(TimeLogViews, self).update_entity()

    @view_config(
        route_name='time_logs',
        request_method='PUT',
    )
    def create_entity(self):
        """creates a TimeLog instance
        """
        return super(TimeLogViews, self).create_entity()

    @view_config(
        route_name='time_log',
        request_method='DELETE',
    )
    def delete_entity(self):
        """deletes a TimeLog instance
        """
        return super(TimeLogViews, self).delete_entity()
