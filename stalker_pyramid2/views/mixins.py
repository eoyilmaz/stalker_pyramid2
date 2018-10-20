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
from stalker_pyramid2.views import (simple_entity_interpreter,
                                    datetime_interpreter)


class StatusMixinViews(object):
    """A mixin view class for SOM classes that is mixed with StatusMixin
    """

    local_params = [
        {
            'param_name': 'status',
            'nullable': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'status_list',
            'nullable': True,
            'interpreter': simple_entity_interpreter
        }
    ]

    def get_entity(self):
        """returns StatusMixin part of the entity
        """
        from stalker_pyramid2 import entity_type_to_url
        from stalker.db.session import DBSession
        from stalker import Status, StatusList
        status_id, status_list_id = DBSession.query(
            self.som_class.status_id,
            self.som_class.status_list_id
        ).filter(self.som_class.id == self.entity_id).first()

        status_data = DBSession\
            .query(Status.id, Status.name, Status.entity_type)\
            .filter(Status.id == status_id)\
            .first()

        status_list_data = DBSession\
            .query(StatusList.id, StatusList.name, StatusList.entity_type)\
            .filter(StatusList.id == status_list_id)\
            .first()
        data = {
            'status': {
                'id': status_data[0],
                'name': status_data[1],
                'entity_type': status_data[2],
                '$ref': '%s/%s' % (
                    entity_type_to_url[status_data[2]],
                    status_data[0]
                )
            },
            'status_list': {
                'id': status_list_data[0],
                'name': status_list_data[1],
                'entity_type': status_list_data[2],
                '$ref': '%s/%s' % (
                    entity_type_to_url[status_list_data[2]],
                    status_list_data[0]
                )
            }
        }
        return data


class ReferenceMixinViews(object):
    """A mixin view class for SOM classes that is mixed with ReferenceMixin
    """
    local_params = [
        {
            'param_name': 'reference_id',
            'arg_name': 'references',
            'is_list': True
        }
    ]

    def get_entity(self):
        """returns the ReferenceMixin portion of this mixed-in class data
        """
        # get references count
        sql = """select
            er.link_id
          from "%s_References" as er
          where er.%s_id = :id
        """ % (
            self.entity.entity_type,
            self.entity.entity_type.lower()
        )
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        from sqlalchemy import text
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        reference_count = r[0] if r else 0

        from stalker_pyramid2 import entity_type_to_url
        data = {
            'references': {
                '$ref': '%s/%s/references' % (
                    entity_type_to_url[self.entity.entity_type],
                    self.entity_id
                ),
                'length': reference_count
            },
        }

        return data

    def get_references(self):
        """returns the ReferenceMixin portion of this mixed-in class data
        """
        sql = """select
          entity_references.link_id,
          "SimpleEntities".name,
          "SimpleEntities".entity_type
        from "%s_References" as entity_references
        join "SimpleEntities" on entity_references.link_id = "SimpleEntities".id
        where entity_references.%s_id = :id
        """ % (
            self.entity.__class__.__name__,
            self.entity.__class__.__name__.lower()
        )

        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        result = conn.execute(text(sql), id=self.entity_id)

        from stalker_pyramid2 import entity_type_to_url
        data = [
            {
                'id': r[0],
                'name': r[1],
                'entity_type': r[2],
                '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0])
            }
            for r in result.fetchall()
        ]

        return data


class DateRangeMixinViews(object):
    """A mixin view class for SOM classes that is mixed with DateRangeMixin
    """
    local_params = [
        # simple arguments/attributes
        {
            'param_name': 'start',
            'interpreter': datetime_interpreter,
            'nullable': False
        },
        {
            'param_name': 'end',
            'interpreter': datetime_interpreter,
            'nullable': False
        },
    ]

    def get_entity(self):
        """returns the DateRangeMixin portion of this mixed-in class data
        """
        sql = """
        select
          (extract(epoch from entity_table.start::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as start,
          (extract(epoch from entity_table.end::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as end
        from "%s" as entity_table
        where entity_table.id = :id
        """ % self.entity.__tablename__

        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        r = conn.execute(text(sql), id=self.entity_id).fetchone()

        data = {}
        if r:
            data = {
                'start': r[0],
                'end': r[1],
            }

        return data


class CodeMixinViews(object):
    """A mixin view class for SOM classes that is mixed with CodeMixin
    """
    local_params = [
        {'param_name': 'code', 'nullable': False},
    ]

    def get_entity(self):
        """returns the CodeMixin portion of this mixed in class
        """
        data = {
            'code': self.entity.code
        }
        return data


class ScheduleMixinViews(object):
    """A mixin view class for SOM classes that is mixed with ScheduleMixin
    """
    local_params = [
        {
            'param_name': 'schedule_constraint',
            'interpreter': int
        },
        {
            'param_name': 'schedule_model'
        },
        {
            'param_name': 'schedule_timing',
            'interpreter': float
        },
        {
            'param_name': 'schedule_unit',
        },
    ]

    def get_entity(self):
        """returns the ScheduleMixin portion of this mixed in class
        """
        from stalker.db.session import DBSession
        r = DBSession\
            .query(self.som_class.schedule_constraint,
                   self.som_class.schedule_model,
                   self.som_class.schedule_timing,
                   self.som_class.schedule_unit)\
            .filter(self.som_class.id == self.entity_id).first()

        data = {
            'schedule_constraint': r[0],
            'schedule_model': r[1],
            'schedule_timing': r[2],
            'schedule_unit': r[3],
        }
        return data


class DAGMixinViews(object):
    """A mixin view class for SOM classes that is mixed with DAGMixin
    """

    local_params = [
        {
            'param_name': 'parent_id',
            'arg_name': 'parent',
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'child_id',
            'arg_name': 'children',
            'interpreter': simple_entity_interpreter,
            'is_list': True
        }
    ]

    def get_entity(self):
        """returns the DAGMixin portion of this mixed in class
        """
        from stalker.db.session import DBSession

        parent_id = DBSession.query(self.som_class.parent_id,)\
            .filter(self.som_class.id == self.entity_id).first()

        parent_data = []
        if parent_id:
            from stalker import SimpleEntity
            parent_data = DBSession.query(
                SimpleEntity.id,
                SimpleEntity.name,
                SimpleEntity.entity_type
            ).filter(SimpleEntity.id == parent_id[0]).first()

        children_count = DBSession.query(
            self.som_class.children
        ).filter(self.som_class.id == self.entity_id)\
        .count()

        from stalker_pyramid2 import entity_type_to_url

        data = {
            'parent': {
                'id': parent_data[0],
                'name': parent_data[1],
                'entity_type': parent_data[2],
                '$ref': '%s/%s' % (entity_type_to_url[parent_data[2]],
                                   parent_data[0])
            } if parent_data else None,
            'children': {
                '%ref': '%s/%s/children',
                'length': children_count
            }
        }

        return data
