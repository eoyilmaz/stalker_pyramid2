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

import re
import logging

from pyramid.view import view_defaults, view_config
from stalker import SimpleEntity, Entity
from stalker_pyramid2.views import (EntityViewBase, simple_entity_interpreter,
                                    datetime_interpreter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_config(
    route_name='get_entity_entities_out_stack',
    renderer='json'
)
def get_entity_entities_out_stack(request):

    logger.debug('get_entity_entities_out_stack is running')

    entity_id = request.matchdict.get('id', -1)
    from stalker import Entity
    entity = Entity.query.filter_by(id=entity_id).first()

    entities_name = request.matchdict.get('entities', -1)
    attr_name = entity.plural_class_name.lower()

    logger.debug('entities_name %s'% entities_name)
    logger.debug('attr_name %s'% attr_name)

    query_string = '%(class_name)s.query.filter(~%(class_name)s.%(attr_name)s.contains(entity)).order_by(%(class_name)s.name.asc())'
    q = eval(query_string % {'class_name': entities_name, 'attr_name': attr_name})
    list_of_container_objects = q.all()

    out_stack = []

    for entity_s in list_of_container_objects:
        # logger.debug('entity_s %s' % entity_s.name)
        out_stack.append({
             'id': entity_s.id,
            'name':entity_s.name,
            'thumnail_path':entity_s.thumbnail.full_path if entity_s.thumbnail else None,
            'description':entity_s.description if entity_s.description else None
        })

    return out_stack


@view_config(
    route_name='append_entities_to_entity',
)
def append_entities_to_entity(request):
    """Appends entities to entity for example appends Projects to user.projects
    etc.
    """
    logger.debug('append_class_to_entity is running')

    entity_id = request.matchdict.get('id', -1)
    from stalker import Entity
    entity = Entity.query.filter_by(id=entity_id).first()

    # selected_list = get_multi_integer(request, 'selected_items[]')
    from stalker_pyramid2.views import EntityViewBase
    selected_list = EntityViewBase.get_multi_integer(request, 'selected_ids')
    logger.debug('selected_list: %s' % selected_list)

    if entity and selected_list:

        appended_entities = Entity.query\
            .filter(Entity.id.in_(selected_list)).all()
        if appended_entities:
            attr_name = appended_entities[0].plural_class_name.lower()
            eval(
                'entity.%(attr_name)s.extend(appended_entities)' %
                {'attr_name': attr_name}
            )
            from stalker.db.session import DBSession
            DBSession.add(entity)

            logger.debug('entity is updated successfully')

            request.session.flash(
                'success:User <strong>%s</strong> is updated successfully' %
                entity.name
            )
            logger.debug('***append_entities_to_entity method ends ***')
    else:
        logger.debug('not all parameters are in request.params')
        from pyramid.httpexceptions import HTTPServerError
        HTTPServerError()

    from pyramid.httpexceptions import HTTPOk
    return HTTPOk()


def remove_entity_from_entity(request):
    """Removes entity from entity for example removes selected project from
    user.projects etc.
    """
    logger.debug('remove_entity_from_entity is running')

    came_from = request.params.get('came_from', '/')

    entity_id = request.matchdict.get('id', -1)
    from stalker import Entity
    entity = Entity.query.filter_by(id=entity_id).first()

    selected_entity_id = request.matchdict.get('entity_id', -1)
    selected_entity = Entity.query.filter_by(id=selected_entity_id).first()

    logger.debug('selected_entity: %s' % selected_entity)

    if entity and selected_entity:

        attr_name = selected_entity.plural_class_name.lower()
        eval('entity.%(attr_name)s.remove(selected_entity)' % {'attr_name': attr_name})
        from stalker.db.session import DBSession
        DBSession.add(entity)

        logger.debug('entity is updated successfully')

        request.session.flash(
            'success:%s <strong>%s</strong> is successfully removed from %s '
            '\'s %s' % (
                selected_entity.entity_type,
                selected_entity.name, entity.name, attr_name
            )
        )
        logger.debug('***remove_entity_from_entity method ends ***')
    else:
        logger.debug('not all parameters are in request.params')
        request.session.flash(
            'failed:not all parameters are in request.params'
        )
        from pyramid.httpexceptions import HTTPServerError
        HTTPServerError()

    from pyramid.response import Response
    return Response(
        'success:%s <strong>%s</strong> is '
        'successfully removed from %s \'s %s' % (
            selected_entity.entity_type,
            selected_entity.name,
            entity.name,
            attr_name
        )
    )


@view_config(
    route_name='get_entity_events',
    renderer='json'
)
# @view_config(
#     route_name='get_user_events',
#     renderer='json'
# )
def get_entity_events(request):
    """Returns entity "events" like TimeLogs, Vacations and Tasks which are
    events to be drawn in Calendars
    """
    logger.debug('get_entity_events is running')

    from stalker_pyramid2.views import multi_permission_checker
    if not multi_permission_checker(
            request, ['Read_User', 'Read_TimeLog', 'Read_Vacation']):
        from pyramid.httpexceptions import HTTPForbidden
        return HTTPForbidden(headers=request)

    from stalker_pyramid2.views import EntityViewBase
    keys = EntityViewBase.get_multi_string(request, 'keys')
    entity_id = request.matchdict.get('id', -1)

    logger.debug('keys: %s' % keys)
    logger.debug('entity_id : %s' % entity_id)

    sql_query = ""
    if 'time_log' in keys:
        sql_query = """
        select
            "TimeLogs".id,
            'timelogs' as entity_type, -- entity_type
            "Task_SimpleEntities".name || ' (' || parent_names.path_names || ')' as title,
            (extract(epoch from "TimeLogs".start::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as start,
            (extract(epoch from "TimeLogs".end::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as end,
            'label-success' as "className",
            false as "allDay",
            "Status_SimpleEntities".name as status
        from "TimeLogs"
        join "Tasks" on "TimeLogs".task_id = "Tasks".id
        join "SimpleEntities" as "Task_SimpleEntities" on "Tasks".id = "Task_SimpleEntities".id
        join "SimpleEntities" as "Status_SimpleEntities" on "Tasks".status_id = "Status_SimpleEntities".id

        join (
            with recursive recursive_task(id, parent_id, path, path_names) as (
                select
                    task.id,
                    task.project_id,
                    array[task.project_id] as path,
                    ("Projects".code || '') as path_names
                from "Tasks" as task
                join "Projects" on task.project_id = "Projects".id
                where task.parent_id is NULL
            union all
                select
                    task.id,
                    task.parent_id,
                    (parent.path || task.parent_id) as path,
                    (parent.path_names || '|' || "Parent_SimpleEntities".name) as path_names
                from "Tasks" as task
                join recursive_task as parent on task.parent_id = parent.id
                join "SimpleEntities" as "Parent_SimpleEntities" on parent.id = "Parent_SimpleEntities".id
                --where parent.id = t_path.parent_id
            ) select
                recursive_task.id,
                recursive_task.path,
                recursive_task.path_names
            from recursive_task
            order by path
        ) as parent_names on "TimeLogs".task_id = parent_names.id

        where "TimeLogs".resource_id = %(id)s
        """ % {'id': entity_id}

    if 'vacation' in keys:
        vacation_sql_query = """
        select
            "Vacations".id,
            'vacations' as entity_type,
            "Type_SimpleEntities".name as title,
            (extract(epoch from "Vacations".start::timestamp at time zone 'UTC') * 1000)::bigint as start,
            (extract(epoch from "Vacations".end::timestamp at time zone 'UTC') * 1000)::bigint as end,
            'label-yellow' as "className",
            true as "allDay",
            NULL as status
        from "Vacations"
        join "SimpleEntities" on "Vacations".id = "SimpleEntities".id
        join "Types" on "SimpleEntities".type_id = "Types".id
        join "SimpleEntities" as "Type_SimpleEntities" on "Types".id = "Type_SimpleEntities".id
        where "Vacations".entity_id is NULL or "Vacations".entity_id = %(id)s
        """ % {'id': entity_id}

        if sql_query != '':
            sql_query = '(%s) union (%s)' % (sql_query, vacation_sql_query)
        else:
            sql_query = vacation_sql_query

    if 'task' in keys:
        task_sql_query = """
        select
            "Tasks".id,
            'tasks' as entity_type,
            "Task_SimpleEntities".name || ' (' || parent_names.path_names || ')' as title,
            (extract(epoch from "Tasks".computed_start::timestamp at time zone 'UTC') * 1000)::bigint as start,
            (extract(epoch from "Tasks".computed_end::timestamp at time zone 'UTC') * 1000)::bigint as end,
            'label' as "className",
            false as "allDay",
            "Status_SimpleEntities".name as status
        from "Tasks"
        join "SimpleEntities" as "Task_SimpleEntities" on "Tasks".id = "Task_SimpleEntities".id
        join "SimpleEntities" as "Status_SimpleEntities" on "Tasks".status_id = "Status_SimpleEntities".id

        join (
            with recursive recursive_task(id, parent_id, path, path_names) as (
                select
                    task.id,
                    task.project_id,
                    array[task.project_id] as path,
                    ("Projects".code || '') as path_names
                from "Tasks" as task
                join "Projects" on task.project_id = "Projects".id
                where task.parent_id is NULL
            union all
                select
                    task.id,
                    task.parent_id,
                    (parent.path || task.parent_id) as path,
                    (parent.path_names || '|' || "Parent_SimpleEntities".name) as path_names
                from "Tasks" as task
                join recursive_task as parent on task.parent_id = parent.id
                join "SimpleEntities" as "Parent_SimpleEntities" on parent.id = "Parent_SimpleEntities".id
                --where parent.id = t_path.parent_id
            ) select
                recursive_task.id,
                recursive_task.path,
                recursive_task.path_names
            from recursive_task
            order by path
        ) as parent_names on "Tasks".id = parent_names.id

        join "Task_Resources" on "Tasks".id = "Task_Resources".task_id

        where "Task_Resources".resource_id = %(id)s and "Tasks".computed_end > current_date::date at time zone 'UTC'
        """ % {'id': entity_id}

        if sql_query != '':
            sql_query = '(%s) union (%s)' % (sql_query, task_sql_query)
        else:
            sql_query = task_sql_query

    from stalker.db.session import DBSession
    result = DBSession.connection().execute(sql_query)
    return [{
        'id': r[0],
        'entity_type': r[1],
        'title': r[2],
        'start': r[3],
        'end': r[4],
        'className': r[5],
        'allDay': r[6],
        'status': r[7]
    } for r in result.fetchall()]


@view_config(
    route_name='get_search_result',
    renderer='json'
)
def get_search_result(request):
    """returns search result
    """
    logger.debug('get_search_result is running')

    q_string = request.params.get('str', -1)

    sql_query_buffer = [
        'select id, name, entity_type from "SimpleEntities"',
        'where'
    ]

    for i, part in enumerate(re.findall(r'[\w\d]+', q_string)):
        if i > 0:
            sql_query_buffer.append('and')
        sql_query_buffer.append(
            """"SimpleEntities".name ilike '%{s}%' """.format(s=part)
        )

    sql_query_buffer.append('order by "SimpleEntities".name')

    sql_query = '\n'.join(sql_query_buffer)

    from sqlalchemy import text  # to be able to use "%" sign use this function
    from stalker.db.session import DBSession
    result = DBSession.connection().execute(text(sql_query))
    return [
        {
            'id': r[0],
            'name': r[1],
            'entity_type': r[2]
        }
        for r in result.fetchall()
    ]


@view_config(
    route_name='submit_search',
    renderer='json'
)
def submit_search(request):
    """submits a search link suitable to be used with list_search_results()
    function.
    """
    logger.debug('***submit_search user method starts ***')

    # get params
    q_string = request.params.get('str', None)
    entity_id = request.params.get('id', None)

    logger.debug('qString : %s' % q_string)

    logger.debug('q_string: %s' % q_string)
    entity_type = None
    q_entity_type = ''
    if ':' in q_string:
        q_string, entity_type = q_string.split(':')

    result_location = '/'

    if q_string:
        sql_query_buffer = [
            'select count(1)',
            'from "Entities"',
            'join "SimpleEntities" on "Entities".id = "SimpleEntities".id',
            'where'
        ]

        for i, part in enumerate(re.findall(r'[\w\d]+', q_string)):
            if i > 0:
                sql_query_buffer.append('and')
            sql_query_buffer.append(
                """"SimpleEntities".name ilike '%{s}%' """.format(s=part)
            )
        if entity_type:

            q_entity_type = '&entity_type=%s'%entity_type

            sql_query_buffer.append(
                """and "SimpleEntities".entity_type='%s' """ % entity_type
            )
        sql_query = '\n'.join(sql_query_buffer)

        logger.debug('sql_query:  %s' % sql_query)

        from sqlalchemy import text
        from stalker.db.session import DBSession
        result = DBSession.connection().execute(text(sql_query))

        entity_count = result.fetchone()[0]
        logger.debug('entity_count : %s' % entity_count)

        # if entity_count > 1:
        result_location = \
            '/list/search_results?str=%s&eid=%s%s' % \
            (q_string, entity_id, q_entity_type)

        # elif entity_count == 1:
        #     sql_query_buffer[0] = 'select "SimpleEntities".id'
        #     sql_query = '\n'.join(sql_query_buffer)
        #
        #     logger.debug('sql_query: %s' % sql_query)
        #     result = DBSession.connection().execute(text(sql_query))
        #
        #     entity = Entity.query.get(result.fetchone()[0])
        #     result_location = \
        #         '/%s/%s/view' % (entity.plural_class_name.lower(), entity.id)

    logger.debug('result_location : %s' % result_location)

    return {
        'url': result_location
    }


def get_entity_total_schedule_seconds(request):
    """gives entity's task total schedule_seconds
    """
    logger.debug('get_project_total_schedule_seconds starts')
    entity_id = request.matchdict.get('id')
    from stalker import Entity
    entity = Entity.query.filter_by(id=entity_id).first()

    sql_query = """select
    SUM(("Tasks".schedule_timing
             * (
                case "Tasks".schedule_unit
                    when 'min' then 60
                    when 'h' then 3600
                    when 'd' then 32400 -- 9 hours/day
                    when 'w' then 183600 -- 51 hours/week
                    when 'm' then 734400  -- 4 week/month * 51 hours/week
                    when 'y' then 9573418 -- 52.1428 week * 51 hours/week
                    else 0
                end
               )
            - coalesce(timelogs.total_timelogs, 0)
            )
            / %(division)s
         )
         as schedule_seconds

    from "Tasks"
    join "Task_Resources" on "Task_Resources".task_id = "Tasks".id
    join "Statuses" on "Statuses".id = "Tasks".status_id
    left outer join (
        select
            "Tasks".id as task_id,
            sum(extract(epoch from "TimeLogs".end::timestamp AT TIME ZONE 'UTC' - "TimeLogs".start::timestamp AT TIME ZONE 'UTC')) as total_timelogs
        from "TimeLogs"
        join "Tasks" on "Tasks".id = "TimeLogs".task_id

        group by "Tasks".id
    ) as timelogs on timelogs.task_id = "Tasks".id

   where "Statuses".code !='CMPL'
    %(where_conditions)s
    """
    where_conditions = ''
    division = '1'

    if entity.entity_type == 'Project':
        where_conditions = """and "Tasks".project_id = %(project_id)s """ % {'project_id': entity_id}
    elif entity.entity_type == 'User':
        where_conditions = """and "Task_Resources".resource_id = %(resource_id)s """ % {'resource_id': entity_id}
        division = """(
                select
                    count(1)
                from "Task_Resources" as inner_task_resources
                where inner_task_resources.task_id = "Tasks".id
            )"""
    elif entity.entity_type == 'Department':

        temp_buffer = [""" and ("""]
        for i, resource in enumerate(entity.users):
            if i > 0:
                temp_buffer.append(' or')
            temp_buffer.append(""" "Task_Resources".resource_id='%s'""" % resource.id)
        temp_buffer.append(' )')
        where_conditions = ''.join(temp_buffer)

        division = """(
                select
                    count(1)
                from "Task_Resources" as inner_task_resources
                where inner_task_resources.task_id = "Tasks".id
            )"""

    logger.debug('where_conditions: %s' % where_conditions)

    sql_query = sql_query % {'where_conditions': where_conditions, 'division':division}

    from stalker.db.session import DBSession
    result = DBSession.connection().execute(sql_query).fetchone()

    logger.debug('get_project_total_schedule_seconds: %s' % result[0])
    return result[0]


@view_config(
    route_name='get_entity_task_min_start',
    renderer='json'
)
def get_entity_task_min_start(request):
    """gives entity's tasks min start date
    """
    logger.debug('get_entity_task_min_start starts')
    entity_id = request.matchdict.get('id')
    from stalker import Entity
    entity = Entity.query.filter_by(id=entity_id).first()

    sql_query = """select
            min(extract(epoch from "Tasks".start::timestamp AT TIME ZONE 'UTC')) as start
        from "Users"
        join "Task_Resources" on "Task_Resources".resource_id = "Users".id
        join "Tasks" on "Tasks".id = "Task_Resources".task_id

    where not exists(select 1 from "Tasks" as t where t.parent_id = "Tasks".id)
    %(where_conditions)s
    """
    where_conditions = ''

    if entity.entity_type == 'Project':
        where_conditions = """and "Tasks".project_id = %(project_id)s """ % {'project_id': entity_id}
    elif entity.entity_type == 'User':
        where_conditions = """and "Task_Resources".resource_id = %(resource_id)s """ % {'resource_id': entity_id}
    elif entity.entity_type == 'Department':
        temp_buffer = [""" and ("""]
        for i, resource in enumerate(entity.users):
            if i > 0:
                temp_buffer.append(' or')
            temp_buffer.append(""" "Task_Resources".resource_id='%s'""" % resource.id)
        temp_buffer.append(' )')
        where_conditions = ''.join(temp_buffer)

    logger.debug('where_conditions: %s' % where_conditions)

    sql_query = sql_query % {'where_conditions': where_conditions}

    from stalker.db.session import DBSession
    result = DBSession.connection().execute(sql_query).fetchone()

    return result[0]


@view_config(
    route_name='get_entity_task_max_end',
    renderer='json'
)
def get_entity_task_max_end(request):
    """gives entity's tasks max end date
    """
    logger.debug('get_entity_task_max_end starts')
    entity_id = request.matchdict.get('id')
    from stalker import Entity
    entity = Entity.query.filter_by(id=entity_id).first()

    sql_query = """select
            max(extract(epoch from "Tasks".end::timestamp AT TIME ZONE 'UTC')) as end
        from "Users"
        join "Task_Resources" on "Task_Resources".resource_id = "Users".id
        join "Tasks" on "Tasks".id = "Task_Resources".task_id

    --where not exists(select 1 from "Tasks" as t where t.parent_id = "Tasks".id)
    %(where_conditions)s
    """
    where_conditions = ''

    if entity.entity_type == 'Project':
        where_conditions = """where "Tasks".project_id = %(project_id)s """ % {'project_id': entity_id}
    elif entity.entity_type == 'User':
        where_conditions = """where "Task_Resources".resource_id = %(resource_id)s """ % {'resource_id': entity_id}
    elif entity.entity_type == 'Department':
        temp_buffer = ["""where ("""]
        for i, resource in enumerate(entity.users):
            if i > 0:
                temp_buffer.append(' or')
            temp_buffer.append(""" "Task_Resources".resource_id='%s'""" % resource.id)
        temp_buffer.append(' )')
        where_conditions = ''.join(temp_buffer)

    logger.debug('where_conditions: %s' % where_conditions)

    sql_query = sql_query % {'where_conditions': where_conditions}

    from stalker.db.session import DBSession
    result = DBSession.connection().execute(sql_query).fetchone()

    return result[0]


@view_defaults(renderer='json')
class SimpleEntityViews(EntityViewBase):
    """vies for SimpleEntity instances
    """
    som_class = SimpleEntity
    local_params = [
        # simple arguments
        {'param_name': 'date_crated', 'interpreter': datetime_interpreter},
        {'param_name': 'date_updated', 'interpreter': datetime_interpreter},
        {'param_name': 'description'},
        {'param_name': 'name'},
        {'param_name': 'generic_text'},

        # complex arguments
        {
            'param_name': 'created_by_id',
            'arg_name': 'created_by',
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'updated_by_id',
            'arg_name': 'updated_by',
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'thumbnail_id',
            'arg_name': 'thumbnail',
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'type_id',
            'arg_name': 'type',
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'generic_data_id',
            'arg_name': 'generic_data',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        }
    ]

    @view_config(
        route_name='simple_entity',
        request_method='GET'
    )
    def get_entity(self):
        """returns one simple entity instance data
        """
        sql = """
        select
          "SimpleEntities".id,
          "SimpleEntities".name,
          "SimpleEntities".description,
          "SimpleEntities".created_by_id,
          "SimpleEntities".updated_by_id,
          (extract(epoch from "SimpleEntities".date_created::timestamp at time zone 'UTC') * 1000)::bigint as date_created,
          (extract(epoch from "SimpleEntities".date_updated::timestamp at time zone 'UTC') * 1000)::bigint as date_updated,
          "SimpleEntities".thumbnail_id,
          "SimpleEntities".stalker_version,
          "SimpleEntities".generic_text,
          "SimpleEntities".entity_type,
          "SimpleEntities".type_id
        from "SimpleEntities"
        where "SimpleEntities".id = :id
        """

        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        result = conn.execute(text(sql), id=self.entity_id)
        r = result.fetchone()

        # get generic_data_count
        from stalker.models.entity import SimpleEntity_GenericData
        generic_data_count = \
            DBSession.query(SimpleEntity_GenericData.c.simple_entity_id)\
            .filter(
                SimpleEntity_GenericData.c.simple_entity_id == self.entity_id
            )\
            .count()

        # get created_by name
        created_by_name = created_by_entity_type = None
        if r[3]:
            sub_query_result = DBSession\
                .query(SimpleEntity.name, SimpleEntity.entity_type)\
                .filter(SimpleEntity.id == r[3])\
                .first()
            created_by_name = sub_query_result[0]
            created_by_entity_type = sub_query_result[1]

        # get updated_by name
        updated_by_name = updated_by_entity_type = None
        if r[4]:
            if r[3] == r[4]:
                updated_by_name = created_by_name
                updated_by_entity_type = created_by_entity_type
            else:
                sub_query_result = DBSession \
                    .query(SimpleEntity.name, SimpleEntity.entity_type)\
                    .filter(SimpleEntity.id == r[4]) \
                    .first()
                updated_by_name = sub_query_result[0]
                updated_by_entity_type = sub_query_result[1]

        # get thumbnail name - we need to do that to be consistent
        thumbnail_name = thumbnail_entity_type = None
        if r[7]:
            sub_query_result = DBSession\
                .query(SimpleEntity.name, SimpleEntity.entity_type)\
                .filter(SimpleEntity.id == r[7])\
                .first()
            thumbnail_name = sub_query_result[0]
            thumbnail_entity_type = sub_query_result[1]

        # get type name
        type_name = type_entity_type = None
        if r[11]:
            sub_query_result = DBSession\
                .query(SimpleEntity.name, SimpleEntity.entity_type)\
                .filter(SimpleEntity.id == r[11])\
                .first()
            type_name = sub_query_result[0]
            type_entity_type = sub_query_result[1]

        from stalker_pyramid2 import entity_type_to_url
        data = {
            'id': r[0],
            'name': r[1],
            'description': r[2],
            'created_by': {
                'id': r[3],
                '$ref':
                    '%s/%s' % (
                        entity_type_to_url[created_by_entity_type],
                        r[3]
                    ),
                'name': created_by_name,
                'entity_type': created_by_entity_type
            } if r[3] else None,
            'updated_by': {
                'id': r[4],
                '$ref':
                    '%s/%s' % (
                        entity_type_to_url[updated_by_entity_type],
                        r[4]
                    ),
                'name': updated_by_name,
                'entity_type': updated_by_entity_type
            } if r[4] else None,
            'date_created': r[5],
            'date_updated': r[6],
            'thumbnail': {
                'id': r[7],
                '$ref':
                    '%s/%s' % (
                        entity_type_to_url[thumbnail_entity_type],
                        r[7]
                    ),
                'name': thumbnail_name,
                'entity_type': thumbnail_entity_type
            } if r[7] else None,
            'stalker_version': r[8],
            'generic_text': r[9],
            'generic_data': {
                '$ref': '%s/%s/generic_data' %
                        (entity_type_to_url['SimpleEntity'], r[0]),
                'length': generic_data_count
            },
            'entity_type': r[10],
            'type': {
                'id': r[11],
                '$ref':
                    '%s/%s' % (entity_type_to_url[type_entity_type], r[11]),
                'name': type_name,
                'entity_type': type_entity_type
            } if r[11] else None
        }

        from pyramid.response import Response
        return Response(json_body=data)

    @view_config(
        route_name='simple_entities',
        request_method='GET'
    )
    def get_entities(self):
        """returns all SimpleEntity instances in database
        """
        return super(SimpleEntityViews, self).get_entities()

    @view_config(
        route_name='simple_entity',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates entity info
        """
        return self.entity_updater(self.entity, self.param_resolution)

    @view_config(
        route_name='simple_entity',
        request_method='DELETE',
    )
    def delete_entity(self):
        """delete one SimpleEntity instance
        """
        return super(SimpleEntityViews, self).delete_entity()

    # SimpleEntity <-> GenericData
    @view_config(
        route_name='simple_entity_generic_data',
        request_method='GET'
    )
    def get_generic_data(self):
        """returns the generic data assigned to a simple entity
        """
        from stalker.models.entity import (SimpleEntity,
                                           SimpleEntity_GenericData)
        join = (
            SimpleEntity_GenericData,
            SimpleEntity.id ==
            SimpleEntity_GenericData.c.other_simple_entity_id
        )
        filters = \
            [SimpleEntity_GenericData.c.simple_entity_id == self.entity_id]
        filters.extend(self.filter_generator(SimpleEntity))
        return self.collection_query(
            SimpleEntity, join=join, filters=filters
        )

    @view_config(
        route_name='simple_entity_generic_data',
        request_method=['PATCH', 'PUT', 'POST'],
    )
    def update_generic_data(self):
        """updates the generic_data attribute
        """
        entity_ids = self.get_multi_integer(self.request, 'entity_id')

        from stalker import SimpleEntity
        entities = SimpleEntity.query\
            .filter(SimpleEntity.id.in_(entity_ids)).all()

        if self.request.method == 'PATCH':
            self.entity.generic_data += entities
        elif self.request.method in ['PUT', 'POST']:
            self.entity.generic_data = entities

    @view_config(
        route_name='simple_entity_generic_data',
        request_method='DELETE',
    )
    def delete_generic_data(self):
        """removes the given entity from the generic_data attribute
        """
        entity_ids = self.get_multi_integer(self.request, 'entity_id')

        from stalker import SimpleEntity
        entities = SimpleEntity.query\
            .filter(SimpleEntity.id.in_(entity_ids)).all()

        for entity in entities:
            try:
                self.entity.generic_data.remove(entity)
            except ValueError:
                pass


@view_defaults(renderer='json')
class EntityViews(SimpleEntityViews):
    """views for Entity instances
    """
    som_class = Entity
    local_params = [
        # complex arguments
        {
            'param_name': 'note_id',
            'arg_name': 'notes',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'tag_id',
            'arg_name': 'tags',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        }
    ]

    @view_config(
        route_name='entity',
        request_method='GET'
    )
    def get_entity(self):
        """returns one Entity instance
        """
        sql = """
        select
          "Entities".id
        from "Entities"
        where "Entities".id = :id
        """
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        from sqlalchemy import text
        result = conn.execute(text(sql), id=self.entity_id)
        r = result.fetchone()

        # get notes count
        from stalker.models.entity import Entity_Notes
        notes_count = DBSession.query(Entity_Notes.c.entity_id)\
            .filter(Entity_Notes.c.entity_id == self.entity_id)\
            .count()

        # get tags count
        from stalker.models.entity import Entity_Tags
        tags_count = DBSession.query(Entity_Tags.c.entity_id)\
            .filter(Entity_Tags.c.entity_id == self.entity_id)\
            .count()

        from stalker_pyramid2 import entity_type_to_url
        data = {
            'id': r[0],
            'notes': {
                '$ref': '%s/%s/notes' %
                        (entity_type_to_url['Entity'], r[0]),
                'length': notes_count
            },
            'tags': {
                '$ref': '%s/%s/tags' % (entity_type_to_url['Entity'], r[0]),
                'length': tags_count
            },
        }

        # update with super data
        response = super(EntityViews, self).get_entity()
        return self.update_response_data(response, data)

    @view_config(
        route_name='entities',
        request_method='GET'
    )
    def get_entities(self):
        """returns all Entity instances in database
        """
        return super(EntityViews, self).get_entities()

    @view_config(
        route_name='entity',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates one entity
        """
        # we can only change audit information which is done by
        # SimpleEntity.views
        return super(EntityViews, self).update_entity()

    @view_config(
        route_name='entity',
        request_method='DELETE',
    )
    def delete_entity(self):
        """delete one Entity instance
        """
        return super(EntityViews, self).delete_entity()

    # Entity <-> Tags
    @view_config(
        route_name='entity_tags',
        request_method='GET',
    )
    def get_tags(self):
        """returns entity tags
        """
        from stalker import Tag
        from stalker.models.entity import Entity_Tags
        join = Entity_Tags
        filters = [Entity_Tags.c.entity_id == self.entity_id]
        filters.extend(self.filter_generator(Tag))
        return self.collection_query(Tag, join=join, filters=filters)

    @view_config(
        route_name='entity_tags',
        request_method=['PATCH', 'POST'],
    )
    def update_tags(self):
        """updates entity tags
        """
        tag_names = self.get_multi_string(self.request, 'tag')
        from stalker import Tag
        tags = Tag.query.filter(Tag.name.in_(tag_names)).all()
        if tags:
            if self.request.method == 'POST':
                # return the result if POST
                self.entity.tags = tags
            elif self.request.method == 'PATCH':
                self.entity.tags += tags

    @view_config(
        route_name='entity_tags',
        request_method='DELETE',
    )
    def remove_tags(self):
        """removes user tags
        """
        tag_names = self.get_multi_string(self.request, 'tag')
        from stalker import Tag
        tags = Tag.query.filter(Tag.name.in_(tag_names)).all()
        if tags:
            for t in tags:
                try:
                    self.entity.tags.remove(t)
                except ValueError:
                    # tag not in user.tags skip it
                    pass

    # Entity <-> Note
    @view_config(
        route_name='entity_notes',
        request_method='GET',
    )
    def get_notes(self):
        """returns entity notes
        """
        from stalker import Note
        from stalker.models.entity import Entity_Notes
        join = Entity_Notes
        filters = [Entity_Notes.c.entity_id == self.entity_id]
        filters.extend(self.filter_generator(Note))
        return self.collection_query(Note, join=join, filters=filters)

    @view_config(
        route_name='entity_notes',
        request_method=['PATCH', 'POST'],
    )
    def update_notes(self):
        """updates entity notes
        """
        # get the note_id
        note_ids = self.get_multi_integer(self.request, 'note_id')

        from stalker import Note
        notes = Note.query.filter(Note.id.in_(note_ids)).all()

        if self.request.method == 'PATCH':
            self.entity.notes += notes
        elif self.request.method == 'POST':
            self.entity.notes = notes

    @view_config(
        route_name='entity_notes',
        request_method='DELETE',
    )
    def remove_notes(self):
        """removes the given notes from the Entity.notes attribute
        """
        raise NotImplementedError
