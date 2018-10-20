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
from stalker_pyramid2.views import simple_entity_interpreter
from stalker_pyramid2.views.entity import EntityViews

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


@view_defaults(renderer='json')
class StatusViews(EntityViews):
    """views for Status class
    """
    from stalker import Status
    som_class = Status
    local_params = [
        {'param_name': 'code', 'nullable': False},
    ]

    @view_config(
        route_name='status',
        request_method='GET',
    )
    def get_entity(self):
        """returns one Status instance
        """
        sql = """
        select
            "Statuses".code
        from "Statuses"
        where "Statuses".id = :id
        """

        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        result = conn.execute(text(sql), id=self.entity_id)

        data = {
            'code': result.fetchone()[0]
        }
        response = super(StatusViews, self).get_entity()
        return self.update_response_data(response, data)

    @view_config(
        route_name='statuses',
        request_method='GET',
    )
    def get_entities(self):
        """return all Statuses in the database
        """
        return super(StatusViews, self).get_entities()

    @view_config(
        route_name='status',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates one Status
        """
        return super(StatusViews, self).update_entity()

    @view_config(
        route_name='statuses',
        request_method='PUT',
    )
    def create_entity(self):
        """creates a Status instance
        """
        return super(StatusViews, self).create_entity()

    @view_config(
        route_name='status',
        request_method='DELETE',
    )
    def delete_entity(self):
        """deletes one Status instance
        """
        return super(StatusViews, self).delete_entity()


@view_defaults(renderer='json')
class StatusListViews(EntityViews):
    """views for StatusList classes
    """
    from stalker import StatusList
    som_class = StatusList
    local_params = [
        # simple arguments
        {'param_name': 'target_entity_type', 'nullable': False},

        # complex arguments
        {
            'param_name': 'status_id',
            'arg_name': 'statuses',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
    ]

    @view_config(
        route_name='status_list',
        request_method='GET',
    )
    def get_entity(self):
        """return one StatusList instance as json
        """
        sql = """select
            "StatusLists".target_entity_type
        from "StatusLists"
        where "StatusLists".id = :id
        """
        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        result = conn.execute(text(sql), id=self.entity_id)
        r = result.fetchone()

        # get statuses count
        from stalker.models.status import StatusList_Statuses
        statuses_count = DBSession.query(StatusList_Statuses.c.status_id)\
            .filter(StatusList_Statuses.c.status_list_id == self.entity_id)\
            .count()

        from stalker_pyramid2 import entity_type_to_url
        data = {
            'statuses': {
                '$ref':
                    '%s/%s/statuses' %
                    (entity_type_to_url['StatusList'], self.entity_id),
                'length': statuses_count
            },
            'target_entity_type': r[0]
        }

        # update with super data
        response = super(StatusListViews, self).get_entity()
        return self.update_response_data(response, data)

    @view_config(
        route_name='status_lists',
        request_method='GET',
    )
    def get_entities(self):
        """returns all the StatusLists in the database
        """
        return super(StatusListViews, self).get_entities()

    @view_config(
        route_name='status_list',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates the entity
        """
        return super(StatusListViews, self).update_entity()

    @view_config(
        route_name='status_lists',
        request_method='PUT',
    )
    def create_entity(self):
        """creates one StatusList instance
        """
        return super(StatusListViews, self).create_entity()

    @view_config(
        route_name='status_list',
        request_method='DELETE',
    )
    def delete_entity(self):
        """deletes a StatusList
        """
        return super(StatusListViews, self).delete_entity()

    @view_config(
        route_name='status_list_statuses',
        request_method='GET',
    )
    def get_statuses(self):
        """returns the statuses of this list
        """
        from stalker.models.status import Status, StatusList_Statuses
        join = StatusList_Statuses
        filters = [StatusList_Statuses.c.status_list_id == self.entity_id]
        filters.extend(self.filter_generator(Status))
        return self.collection_query(Status, join=join, filters=filters)

    @view_config(
        route_name='status_list_statuses',
        request_method=['PATCH', 'POST'],
    )
    def update_statuses(self):
        """updates the statuses list
        """
        status_ids = self.get_multi_integer(self.request, 'status_id')

        from stalker import Status
        statuses = Status.query.filter(Status.id.in_(status_ids)).all()

        if self.request.method == 'PATCH':
            self.entity.statuses += statuses
        elif self.request.method == 'POST':
            self.entity.statuses = statuses

    @view_config(
        route_name='status_list_statuses',
        request_method='DELETE',
    )
    def delete_statuses(self):
        """deletes the given statuses from statuses list
        """
        status_ids = self.get_multi_integer(self.request, 'status_id')

        from stalker import Status
        statuses = Status.query.filter(Status.id.in_(status_ids)).all()

        for status in statuses:
            try:
                self.entity.statuses.remove(status)
            except ValueError:
                pass
