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
from pyramid.view import view_config

from stalker import db, Project, Status, Daily, Link

import transaction

from webob import Response
from stalker_pyramid.views import logger, PermissionChecker, local_to_utc


@view_config(
    route_name='create_daily'
)
def create_daily(request):
    """runs when creating a daily
    """

    logged_in_user = get_logged_in_user(request)
    utc_now = local_to_utc(datetime.datetime.now())

    name = request.params.get('name')
    description = request.params.get('description')

    status_id = request.params.get('status_id')
    status = Status.query.filter(Status.id == status_id).first()

    project_id = request.params.get('project_id', None)
    project = Project.query.filter(Project.id == project_id).first()

    if not name:
        return Response('Please supply a name', 500)

    if not description:
        return Response('Please supply a description', 500)

    if not status:
        return Response('There is no status with code: %s' % status_id, 500)

    if not project:
        return Response('There is no project with id: %s' % project_id, 500)

    daily = Daily(
        project=project,
        name=name,
        status=status,
        description=description,
        created_by=logged_in_user,
        date_created=utc_now,
        date_updated=utc_now
    )
    from stalker.db.session import DBSession
    DBSession.add(daily)

    return Response('Daily Created successfully')


@view_config(
    route_name='update_daily'
)
def update_daily(request):
    """runs when updating a daily
    """

    logged_in_user = get_logged_in_user(request)
    utc_now = local_to_utc(datetime.datetime.now())

    daily_id = request.matchdict.get('id', -1)
    daily = Daily.query.filter(Daily.id == daily_id).first()

    if not daily:
        transaction.abort()
        return Response('No daily with id : %s' % daily_id, 500)

    name = request.params.get('name')
    description = request.params.get('description')

    status_id = request.params.get('status_id')
    status = Status.query.filter(Status.id == status_id).first()

    if not name:
        return Response('Please supply a name', 500)

    if not description:
        return Response('Please supply a description', 500)

    if not status:
        return Response('There is no status with code: %s' % status.code, 500)

    daily.name = name
    daily.description = description
    daily.status = status
    daily.date_updated = utc_now
    daily.updated_by = logged_in_user

    request.session.flash('success: Successfully updated daily')
    return Response('Successfully updated daily')


def get_dailies(request):
    """returns dailies with the given id
    """

    project_id = request.matchdict.get('id')
    logger.debug('get_dailies is working for the project which id is: %s' % project_id)

    status_code = request.params.get('status_code',None)
    status = Status.query.filter(Status.code==status_code).first()

    sql_query = """
        select
            "Dailies_SimpleEntities".id,
            "Dailies_SimpleEntities".name,
            "Dailies_Statuses".code,
            "Dailies_Statuses".id,
            "Dailies_Statuses_SimpleEntities".name,
            "Dailies_SimpleEntities".created_by_id,
            "Dailies_Creator_SimpleEntities".name,
            daily_count.link_count,
            (extract(epoch from "Dailies_SimpleEntities".date_created::timestamp at time zone 'UTC') * 1000)::bigint as date_created

        from "Projects"
        join "Dailies" on "Dailies".project_id = "Projects".id
        join "SimpleEntities" as "Dailies_SimpleEntities" on "Dailies_SimpleEntities".id = "Dailies".id
        join "SimpleEntities" as "Dailies_Creator_SimpleEntities" on "Dailies_Creator_SimpleEntities".id = "Dailies_SimpleEntities".created_by_id
        join "Statuses" as "Dailies_Statuses" on "Dailies_Statuses".id = "Dailies".status_id
        join "SimpleEntities" as "Dailies_Statuses_SimpleEntities" on "Dailies_Statuses_SimpleEntities".id = "Dailies".status_id

        left outer join (
            select
                "Daily_Links".daily_id as daily_id,
                count("Daily_Links".link_id) as link_count
            from "Daily_Links"
            join "Dailies" on "Dailies".id = "Daily_Links".daily_id
            group by "Daily_Links".daily_id
        ) as daily_count on daily_count.daily_id ="Dailies".id
        where "Projects".id = %(project_id)s %(additional_condition)s
    """

    additional_condition = ''
    if status:
        additional_condition = 'and "Dailies_Statuses".id=%s' % status.id


    sql_query = sql_query % {'project_id': project_id, 'additional_condition':additional_condition}

    result = DBSession.connection().execute(sql_query)

    dailies = []

    update_daily_permission = \
        PermissionChecker(request)('Update_Daily')

    for r in result.fetchall():
        daily = {
            'id': r[0],
            'name': r[1],
            'status_code': r[2].lower(),
            'status_id': r[3],
            'status_name': r[4],
            'created_by_id': r[5],
            'created_by_name': r[6],
            'link_count': r[7] if r[7] else 0,
            'item_view_link': '/dailies/%s/view' % r[0],
            'date_created':r[8]
        }
        if update_daily_permission:
            daily['item_update_link'] = \
                '/dailies/%s/update/dialog' % daily['id']
            daily['item_remove_link'] =\
                '/entities/%s/delete/dialog?came_from=%s' % (
                    daily['id'],
                    request.current_route_path()
                )

        dailies.append(daily)

    resp = Response(
        json_body=dailies
    )

    return resp


def get_dailies_count(request):
    """missing docstring
    """
    project_id = request.matchdict.get('id')
    logger.debug('get_dailies_count is working for the project which id is %s' % project_id)

    sql_query = """
select count(1) from (
select "Dailies".id

from "Projects"
join "Dailies" on "Dailies".project_id = "Projects".id
join "Statuses" on "Dailies".status_id = "Statuses".id

where "Statuses".code = 'OPEN' and "Projects".id = %(project_id)s
) as data
    """
    sql_query = sql_query % {'project_id': project_id}

    from sqlalchemy import text  # to be able to use "%" sign use this function
    result = DBSession.connection().execute(text(sql_query))

    return result.fetchone()[0]


@view_config(
    route_name='get_daily_outputs',
    renderer='json'
)
def get_daily_outputs(request):
    """missing docstring
    """

    daily_id = request.matchdict.get('id')
    logger.debug('get_daily_outputs is working for the daily which id is : %s' % daily_id)

    sql_query = """
        select
            "Link_Tasks".id as task_id,
            "ParentTasks".full_path as task_name,
            "Task_Statuses".code as task_status_code,
            "Task_Status_SimpleEntities".name as task_status_name,
            array_agg(link_data.link_id) as link_id,

            array_agg(link_data.original_filename) as link_original_filename,
            array_agg(link_data.hires_full_path) as link_hires_full_path,
            array_agg(link_data.webres_full_path) as link_webres_full_path,
            array_agg(link_data.thumbnail_full_path) as link_thumbnail_full_path,

            array_agg(link_data.version_id) as version_id,
            array_agg(link_data.version_take_name) as version_take_name,
            array_agg(link_data.version_number) as version_number,
            array_agg(link_data.version_is_published) as version_is_published,

            daily_note.note_id as note_id,
            daily_note.entity_id as entity_id,
            daily_note.user_name as user_name,
            daily_note.user_thumbnail as user_thumbnail,
            daily_note.note_content as note_content,
            daily_note.note_date_created as note_date_created,
            daily_note.note_type_name as note_type_name,

            "Resource_SimpleEntities".name as resource_name,
            "Resource_SimpleEntities".id as resource_id

        from "Dailies"
        join "Daily_Links" on "Daily_Links".daily_id = "Dailies".id
        join (
            select
                "Tasks".id as task_id,
                "Versions".id as version_id,
                "Versions".take_name as version_take_name,
                "Versions".version_number as version_number,
                "Versions".is_published as version_is_published,
                "Links".id as link_id,
                "Links".original_filename as original_filename,

                "Links".full_path as hires_full_path,
                "Links_ForWeb".full_path as webres_full_path,
                "Thumbnails".full_path as thumbnail_full_path

            from "Links"
            join "SimpleEntities" as "Link_SimpleEntities" on "Link_SimpleEntities".id = "Links".id
            join "Links" as "Links_ForWeb" on "Link_SimpleEntities".thumbnail_id = "Links_ForWeb".id
            join "SimpleEntities" as "Links_ForWeb_SimpleEntities" on "Links_ForWeb".id = "Links_ForWeb_SimpleEntities".id
            join "Links" as "Thumbnails" on "Links_ForWeb_SimpleEntities".thumbnail_id = "Thumbnails".id
            join "Version_Outputs" on "Version_Outputs".link_id = "Links".id
            join "Versions" on "Versions".id = "Version_Outputs".version_id
            join "Tasks" on "Tasks".id = "Versions".task_id
        ) as link_data on link_data.link_id = "Daily_Links".link_id
        join "Tasks" as "Link_Tasks" on "Link_Tasks".id = link_data.task_id
        join "Statuses" as "Task_Statuses" on "Task_Statuses".id = "Link_Tasks".status_id
        join "SimpleEntities" as "Task_Status_SimpleEntities" on "Task_Status_SimpleEntities".id = "Link_Tasks".status_id
        join "Task_Resources" on "Task_Resources".task_id = "Link_Tasks".id
        join "SimpleEntities" as "Resource_SimpleEntities" on "Resource_SimpleEntities".id = "Task_Resources".resource_id
        --find the task daily notes
        left outer join (
            select
                "Task_Notes".entity_id as task_id,
                array_agg( "User_SimpleEntities".id) as entity_id,
                array_agg( "User_SimpleEntities".name) as user_name,
                array_agg( "Users_Thumbnail_Links".full_path) as user_thumbnail,
                array_agg( "Notes_SimpleEntities".id) as note_id,
                array_agg( "Notes_SimpleEntities".description) as note_content,
                array_agg( "Notes_SimpleEntities".date_created) as note_date_created,
                array_agg( "Notes_Types_SimpleEntities".id) as note_type_id,
                array_agg( "Notes_Types_SimpleEntities".name) as note_type_name

            from "Notes"
            join "SimpleEntities" as "Notes_SimpleEntities" on "Notes_SimpleEntities".id = "Notes".id
            left outer join "SimpleEntities" as "Notes_Types_SimpleEntities" on "Notes_Types_SimpleEntities".id = "Notes_SimpleEntities".type_id
            join "SimpleEntities" as "User_SimpleEntities" on "Notes_SimpleEntities".created_by_id = "User_SimpleEntities".id
            left outer join "Links" as "Users_Thumbnail_Links" on "Users_Thumbnail_Links".id = "User_SimpleEntities".thumbnail_id
            join "Entity_Notes" as "Daily_Notes" on "Daily_Notes".note_id = "Notes".id
            join "Entity_Notes" as "Task_Notes" on "Task_Notes".note_id = "Daily_Notes".note_id

            where "Daily_Notes".entity_id =  %(daily_id)s and "Notes_Types_SimpleEntities".name = 'Daily_Note'

            group by "Task_Notes".entity_id
        ) as daily_note on daily_note.task_id = "Link_Tasks".id

        left join (
            %(generate_recursive_task_query)s
        ) as "ParentTasks" on "Link_Tasks".id = "ParentTasks".id

        where "Dailies".id = %(daily_id)s

        group by
            "Link_Tasks".id,
            "ParentTasks".full_path,
            "Task_Statuses".code,
            "Task_Status_SimpleEntities".name,
            "Resource_SimpleEntities".name,
            "Resource_SimpleEntities".id,
            daily_note.note_id,
            daily_note.entity_id,
            daily_note.user_name,
            daily_note.user_thumbnail,
            daily_note.note_content,
            daily_note.note_date_created,
            daily_note.note_type_name
        order by
            "ParentTasks".full_path


    """
    sql_query = sql_query % {'daily_id': daily_id, 'generate_recursive_task_query': generate_recursive_task_query()}

    result = DBSession.connection().execute(sql_query)

    tasks = []

    for r in result.fetchall():
        links = []

        link_ids = r[4]
        original_filename = r[5]
        hires_full_path = r[6]
        full_path = r[7]
        thumbnail_full_path = r[8]

        version_ids = r[9]
        version_take_names = r[10]
        version_numbers = r[11]
        versions_is_published = r[12]

        for i in range(len(link_ids)):
            link = {
                'id': link_ids[i],
                'original_filename': original_filename[i],
                'hires_full_path': hires_full_path[i],
                'webres_full_path': full_path[i],
                'thumbnail_full_path': thumbnail_full_path[i],
                'version_id': version_ids[i],
                'version_take_name': version_take_names[i],
                'version_number': version_numbers[i],
                'version_is_published': versions_is_published[i]
            }
            if link not in links:
                links.append(link)

        notes = []

        note_ids = r[13]
        note_created_by_ids = r[14]
        note_created_by_names = r[15]
        note_created_by_thumbnails = r[16]
        note_contents = r[17]
        note_created_dates = r[18]
        note_type_names = r[19]

        if note_ids:
            for j in range(len(note_ids)):
                if note_ids[j]:
                    note = {
                        'id': note_ids[j],
                        'created_by_id': note_created_by_ids[j],
                        'created_by_name': note_created_by_names[j],
                        'created_by_thumbnail': note_created_by_thumbnails[j],
                        'content': note_contents[j],
                        'created_date': milliseconds_since_epoch(note_created_dates[j]),
                        'note_type_name': note_type_names[j]
                    }
                    if note not in notes:
                        notes.append(note)

        task = {
            'task_id': r[0],
            'task_name': r[1],
            'task_status_code': r[2].lower(),
            'task_status_name': r[3],
            'task_resource_name': r[20],
            'task_resource_id': r[21],
            'links': links,
            'notes': notes
        }
        tasks.append(task)

    resp = Response(
        json_body=tasks
    )

    return resp


@view_config(
    route_name='append_link_to_daily',
    renderer='json'
)
def append_link_to_daily(request):

    link_id = request.matchdict.get('id')
    link = Link.query.filter_by(id=link_id).first()

    daily_id = request.matchdict.get('did')
    daily = Daily.query.filter_by(id=daily_id).first()

    if not link:
        transaction.abort()
        return Response('There is no link with id: %s' % link_id, 500)

    if not daily:
        transaction.abort()
        return Response('There is no daily with id: %s' % daily_id, 500)

    if link not in daily.links:
        daily.links.append(link)

    request.session.flash(
        'success: Output is added to daily: %s '% daily.name
    )

    return Response('Output is added to daily: %s '% daily.name)


@view_config(
    route_name='remove_link_to_daily'
)
def remove_link_to_daily(request):

    link_id = request.matchdict.get('id')
    link = Link.query.filter_by(id=link_id).first()

    daily_id = request.matchdict.get('did')
    daily = Daily.query.filter_by(id=daily_id).first()

    if not link:
        transaction.abort()
        return Response('There is no link with id: %s' % link_id, 500)

    if not daily:
        transaction.abort()
        return Response('There is no daily with id: %s' % daily_id, 500)

    if link in daily.links:
        daily.links.remove(link)

    request.session.flash(
        'success: Output is removed from daily: %s '% daily.name
    )

    return Response('Output is removed to daily: %s '% daily.name)


@view_config(
    route_name='inline_update_daily'
)
def inline_update_daily(request):
    """Inline updates the given daily with the data coming from the request
    """

    logger.debug('inline_update_daily is working')

    logged_in_user = get_logged_in_user(request)

    # *************************************************************************
    # collect data
    attr_name = request.params.get('attr_name', None)
    attr_value = request.params.get('attr_value', None)

    logger.debug('attr_name %s', attr_name)
    logger.debug('attr_value %s', attr_value)

    # get daily
    daily_id = request.matchdict.get('id', -1)
    daily = Daily.query.filter(Daily.id == daily_id).first()

    # update the daily
    if not daily:
        transaction.abort()
        return Response("No daily found with id : %s" % daily_id, 500)

    if attr_name and attr_value:

        logger.debug('attr_name %s', attr_name)

        if attr_name == 'status':


            status = Status.query.filter_by(code=attr_value).first()

            if not status:
                transaction.abort()
                return Response("No type found with id : %s" % attr_value, 500)

            daily.status = status
        else:
            setattr(daily, attr_name, attr_value)

        daily.updated_by = logged_in_user
        utc_now = local_to_utc(datetime.datetime.now())
        daily.date_updated = utc_now

    else:
        logger.debug('not updating')
        return Response("MISSING PARAMETERS", 500)

    return Response(
        'Daily updated successfully %s %s' % (attr_name, attr_value)
    )

