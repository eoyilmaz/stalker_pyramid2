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

import datetime

from pyramid.httpexceptions import HTTPOk
from pyramid.view import view_config
from stalker import Type, Status, Asset
from stalker.db.session import DBSession

import logging
from webob import Response

from stalker_pyramid2.views import PermissionChecker

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_config(
    route_name='update_asset',
    permission='Update_Asset'
)
def update_asset(request):
    """updates an Asset
    """
    logger.debug('***update_asset method starts ***')
    logged_in_user = get_logged_in_user(request)

    # get params
    asset_id = request.matchdict.get('id', -1)
    asset = Asset.query.filter_by(id=asset_id).first()

    name = request.params.get('name')
    code = request.params.get('code')
    description = request.params.get('description')
    type_name = request.params.get('type_name')

    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()

    if asset and name and code and type_name and status:
        # get the type
        type_ = Type.query\
            .filter_by(target_entity_type='Asset')\
            .filter_by(name=type_name)\
            .first()

        if type_ is None:
            # create a new Type
            type_ = Type(
                name=type_name,
                code=type_name,
                target_entity_type='Asset'
            )

        # update the asset
        logger.debug('code      : %s' % code)
        asset.name = name
        asset.code = code
        asset.description = description
        asset.type = type_
        asset.status = status
        asset.updated_by = logged_in_user
        asset.date_updated = datetime.datetime.now()

        DBSession.add(asset)

    return HTTPOk()


@view_config(
    route_name='get_entity_assets_count',
    renderer='json',
    permission='List_Asset'
)
def get_assets_count(request):
    """returns the count of assets in a project
    """
    project_id = request.matchdict.get('id', -1)

    sql_query = """select count(1)
    from "Assets"
        join "Tasks" on "Assets".id = "Tasks".id
    where "Tasks".project_id = %s
    """ % project_id

    return DBSession.connection().execute(sql_query).fetchone()[0]


@view_config(
    route_name='get_assets_types',
    renderer='json'
)
def get_assets_types(request):
    """returns the Asset Types
    """
    sql_query = """select
     "Assets_Types_SimpleEntities".id,
     "Assets_Types_SimpleEntities".name

     from "Assets"

     join "SimpleEntities" as "Assets_SimpleEntities" on "Assets_SimpleEntities".id = "Assets".id
     join "SimpleEntities" as "Assets_Types_SimpleEntities" on "Assets_Types_SimpleEntities".id = "Assets_SimpleEntities".type_id

     group by
        "Assets_Types_SimpleEntities".name,
        "Assets_Types_SimpleEntities".id
     order by "Assets_Types_SimpleEntities".name
     """

    result = DBSession.connection().execute(sql_query)

    return_data = [
        {
            'asset_type_id': r[0],
            'asset_type_name': r[1]

        }
        for r in result.fetchall()
    ]

    content_range = '%s-%s/%s'

    type_count = len(return_data)
    content_range = content_range % (0, type_count - 1, type_count)

    logger.debug('content_range : %s' % content_range)

    resp = Response(
        json_body=return_data
    )
    resp.content_range = content_range
    return resp


@view_config(
    route_name='get_assets_children_task_type',
    renderer='json'
)
@view_config(
    route_name='get_assets_type_task_types',
    renderer='json'
)
def get_assets_type_task_types(request):
    """returns the Task Types defined under the Asset container
    """
    type_id = request.matchdict.get('t_id', None)

    logger.debug('type_id %s'% type_id)

    sql_query = """select
        "SimpleEntities".id as type_id,
        "SimpleEntities".name as type_name
    from "SimpleEntities"
    join "SimpleEntities" as "Task_SimpleEntities" on "SimpleEntities".id = "Task_SimpleEntities".type_id
    join "Tasks" on "Task_SimpleEntities".id = "Tasks".id

    join "Assets" on "Tasks".parent_id = "Assets".id
    join "SimpleEntities" as "Assets_SimpleEntities" on "Assets_SimpleEntities".id = "Assets".id

    %(where_condition)s

    group by "SimpleEntities".id, "SimpleEntities".name
    order by "SimpleEntities".name"""

    where_condition = ''

    if type_id:
        where_condition = 'where "Assets_SimpleEntities".type_id = %(type_id)s'%{'type_id': type_id}

    sql_query = sql_query %{'where_condition':where_condition}

    result = DBSession.connection().execute(sql_query)

    return_data = [
        {
            'id': r[0],
            'name': r[1]

        }
        for r in result.fetchall()
    ]

    content_range = '%s-%s/%s'

    type_count = len(return_data)
    content_range = content_range % (0, type_count - 1, type_count)

    logger.debug('content_range : %s' % content_range)

    resp = Response(
        json_body=return_data
    )
    resp.content_range = content_range
    return resp


@view_config(
    route_name='get_entity_assets',
    renderer='json',
    permission='List_Asset'
)
def get_assets(request):
    """returns all the Assets of a given Project
    """
    logger.debug('*** get_assets method starts ***')

    project_id = request.matchdict.get('id', -1)
    asset_type_id = request.params.get('asset_type_id', None)

    asset_id = request.params.get('entity_id', None)

    asset_type_names = get_multi_string(request, 'asset_type_names')

    sql_query = """
        select
            "Assets".id as asset_id,
            assets.full_path as asset_name,
            "Asset_SimpleEntities".description as asset_description,
            "Links".full_path as asset_full_path,
            "Distinct_Asset_Statuses".asset_status_code as asset_status_code,
            "Distinct_Asset_Statuses".asset_status_html_class as asset_status_html_class,
            array_agg("Distinct_Asset_Task_Types".type_name) as type_name,
            array_agg("Tasks".id) as task_id,
            array_agg("Task_SimpleEntities".name) as task_name,
            array_agg("Task_Statuses".code) as status_code,
            array_agg("Task_Statuses_SimpleEntities".html_class) as status_html_class,
            array_agg(coalesce(
                    -- for parent tasks
                    (case "Tasks".schedule_seconds
                        when 0 then 0
                        else "Tasks".total_logged_seconds::float / "Tasks".schedule_seconds * 100
                     end
                    ),
                    -- for child tasks we need to count the total seconds of related TimeLogs
                    (coalesce("Task_TimeLogs".duration, 0.0))::float /
                        ("Tasks".schedule_timing * (case "Tasks".schedule_unit
                            when 'min' then 60
                            when 'h' then 3600
                            when 'd' then 32400
                            when 'w' then 183600
                            when 'm' then 734400
                            when 'y' then 9573418
                            else 0
                        end)) * 100.0
                )) as percent_complete,
            "Assets_Types_SimpleEntities".name as asset_type_name,
            array_agg("Task_Resource_SimpleEntities".name) as resources_name,
            array_agg("Task_Resource_SimpleEntities".id) as resources_id
        from "Tasks"
        join "Assets" on "Assets".id = "Tasks".parent_id
        join (
            %(generate_recursive_task_query)s
        ) as assets on assets.id = "Assets".id
        join "SimpleEntities" as "Asset_SimpleEntities" on "Assets".id = "Asset_SimpleEntities".id
        join "SimpleEntities" as "Task_SimpleEntities" on "Tasks".id = "Task_SimpleEntities".id
        left outer join "Task_Resources"  on "Tasks".id = "Task_Resources".task_id
        left outer join "SimpleEntities" as "Task_Resource_SimpleEntities" on "Task_Resources".resource_id = "Task_Resource_SimpleEntities".id
        left join "Types" as "Assets_Types" on "Assets_Types".id = "Asset_SimpleEntities".type_id
        join "SimpleEntities" as "Assets_Types_SimpleEntities" on "Assets_Types_SimpleEntities".id = "Assets_Types".id
        left join "Links" on "Asset_SimpleEntities".thumbnail_id = "Links".id
        join(
            select
                "Assets".id as asset_id,
                "Statuses".code as asset_status_code,
                "SimpleEntities".html_class as asset_status_html_class
            from "Tasks"
            join "Assets" on "Assets".id = "Tasks".id
            join "Statuses" on "Statuses".id = "Tasks".status_id
            join "SimpleEntities" on "SimpleEntities".id = "Statuses".id
            )as "Distinct_Asset_Statuses" on "Assets".id = "Distinct_Asset_Statuses".asset_id
        left join (
            select
                "SimpleEntities".id as type_id,
                "SimpleEntities".name as type_name
            from "SimpleEntities"
            join "SimpleEntities" as "Task_SimpleEntities" on "SimpleEntities".id = "Task_SimpleEntities".type_id
            join "Tasks" on "Task_SimpleEntities".id = "Tasks".id
            join "Assets" on "Tasks".parent_id = "Assets".id
            group by "SimpleEntities".id, "SimpleEntities".name
            order by "SimpleEntities".id
        ) as "Distinct_Asset_Task_Types" on "Task_SimpleEntities".type_id = "Distinct_Asset_Task_Types".type_id
        join "Statuses" as "Task_Statuses" on "Tasks".status_id = "Task_Statuses".id
        join "SimpleEntities" as "Task_Statuses_SimpleEntities" on "Task_Statuses_SimpleEntities".id = "Tasks".status_id

        left outer join (
                    select
                        "TimeLogs".task_id,
                        extract(epoch from sum("TimeLogs".end::timestamp AT TIME ZONE 'UTC' - "TimeLogs".start::timestamp AT TIME ZONE 'UTC')) as duration
                    from "TimeLogs"
                    group by task_id
                ) as "Task_TimeLogs" on "Task_TimeLogs".task_id = "Tasks".id
        where "Tasks".project_id = %(project_id)s  %(where_conditions)s
        group by
            "Assets".id,
            "Asset_SimpleEntities".name,
            assets.full_path,
            "Asset_SimpleEntities".description,
            "Links".full_path,
            "Distinct_Asset_Statuses".asset_status_code,
            "Distinct_Asset_Statuses".asset_status_html_class,
            "Assets_Types_SimpleEntities".name
        order by "Asset_SimpleEntities".name
    """

    where_conditions = ''

    if asset_type_id:
        where_conditions = """and "Assets_Types_SimpleEntities".id = %(asset_type_id)s""" %({'asset_type_id':asset_type_id})
    if asset_id:
        where_conditions = """and "Assets".id = %(asset_id)s""" %({'asset_id':asset_id})
    if len(asset_type_names):
        asset_type_names_buffer = []
        for asset_type_name in asset_type_names:
            asset_type_names_buffer.append(
                """"Assets_Types_SimpleEntities".name = '%s'""" %
                asset_type_name
            )

        logger.debug('asset_type_names_buffer : %s' % asset_type_names_buffer)
        where_conditions_for_type_names = ' or '.join(asset_type_names_buffer)
        where_conditions = """and (%s)""" % where_conditions_for_type_names
        logger.debug('where_conditions : %s' % where_conditions)

    sql_query = sql_query % {
        'where_conditions': where_conditions,
        'project_id': project_id,
        'generate_recursive_task_query': generate_recursive_task_query(),
    }

    update_asset_permission = \
        PermissionChecker(request)('Update_Asset')
    delete_asset_permission = \
        PermissionChecker(request)('Delete_Asset')

    result = DBSession.connection().execute(sql_query)

    return_data = []

    for r in result.fetchall():
        r_data = {
            'id': r[0],
            'name': r[1],
            'description': r[2],
            'thumbnail_full_path': r[3] if r[3] else None,
            'status': r[4],
            'status_color': r[5],
            'update_asset_action': '/tasks/%s/update/dialog' % r[0]
                if update_asset_permission else None,
            'delete_asset_action': '/tasks/%s/delete/dialog' % r[0]
                if delete_asset_permission else None
        }
        task_types_names = r[6]
        task_ids = r[7]
        task_names = r[8]
        task_statuses = r[9]
        task_percent_complete = r[11]
        task_resource_name = r[13]
        task_resource_id = r[14]

        # logger.debug('task_types_names %s ' % task_types_names)
        r_data['nulls'] = []

        for index1 in range(len(task_types_names)):
            if task_types_names[index1]:
                r_data[task_types_names[index1]]= []

        for index in range(len(task_types_names)):
            task = {
                'id': task_ids[index],
                'name': task_names[index],
                'status': task_statuses[index],
                'percent': task_percent_complete[index],
                'resource_name': task_resource_name[index],
                'resource_id': task_resource_id[index]
            }
            if task_types_names[index]:
                r_data[task_types_names[index]].append(task)
            else:
                r_data['nulls'].append(task)

        return_data.append(r_data)

    return return_data
