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
import datetime

from pyramid.httpexceptions import HTTPOk
from pyramid.response import Response
from pyramid.view import view_config

from stalker.db.session import DBSession
from stalker import Studio, WorkingHours, TaskJugglerScheduler, Project
import transaction
from stalker_pyramid2.views import (local_to_utc, StdErrToHTMLConverter,
                                    invalidate_all_caches)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_config(
    route_name='create_studio'
)
def create_studio(request):
    """creates the studio
    """
    name = request.params.get('name', None)
    dwh = request.params.get('dwh', None)
    wh_mon_start = get_time(request, 'mon_start')
    wh_mon_end   = get_time(request, 'mon_end')
    wh_tue_start = get_time(request, 'tue_start')
    wh_tue_end   = get_time(request, 'tue_end')
    wh_wed_start = get_time(request, 'wed_start')
    wh_wed_end   = get_time(request, 'wed_end')
    wh_thu_start = get_time(request, 'thu_start')
    wh_thu_end   = get_time(request, 'thu_end')
    wh_fri_start = get_time(request, 'fri_start')
    wh_fri_end   = get_time(request, 'fri_end')
    wh_sat_start = get_time(request, 'sat_start')
    wh_sat_end   = get_time(request, 'sat_end')
    wh_sun_start = get_time(request, 'sun_start')
    wh_sun_end   = get_time(request, 'sun_end')

    if name and dwh:
        # create new studio
        studio = Studio(
            name=name,
            daily_working_hours=int(dwh)
        )
        wh = WorkingHours()

        def set_wh_for_day(day, start, end):
            if start != end:
                wh[day] = [[start.seconds/60, end.seconds/60]]
            else:
                wh[day] = []

        set_wh_for_day('mon', wh_mon_start, wh_mon_end)
        set_wh_for_day('tue', wh_tue_start, wh_tue_end)
        set_wh_for_day('wed', wh_wed_start, wh_wed_end)
        set_wh_for_day('thu', wh_thu_start, wh_thu_end)
        set_wh_for_day('fri', wh_fri_start, wh_fri_end)
        set_wh_for_day('sat', wh_sat_start, wh_sat_end)
        set_wh_for_day('sun', wh_sun_start, wh_sun_end)

        studio.working_hours = wh

        DBSession.add(studio)
        # Commit will be handled by the zope transaction extension

    return HTTPOk()


@view_config(
    route_name='update_studio'
)
def update_studio(request):
    """updates the studio
    """

    studio_id = request.params.get('studio_id')
    studio = Studio.query.filter_by(id=studio_id).first()

    name = request.params.get('name', None)
    dwh = request.params.get('dwh', None)
    wh_mon_start = get_time(request, 'mon_start')
    wh_mon_end   = get_time(request, 'mon_end')
    wh_tue_start = get_time(request, 'tue_start')
    wh_tue_end   = get_time(request, 'tue_end')
    wh_wed_start = get_time(request, 'wed_start')
    wh_wed_end   = get_time(request, 'wed_end')
    wh_thu_start = get_time(request, 'thu_start')
    wh_thu_end   = get_time(request, 'thu_end')
    wh_fri_start = get_time(request, 'fri_start')
    wh_fri_end   = get_time(request, 'fri_end')
    wh_sat_start = get_time(request, 'sat_start')
    wh_sat_end   = get_time(request, 'sat_end')
    wh_sun_start = get_time(request, 'sun_start')
    wh_sun_end   = get_time(request, 'sun_end')

    if studio and name and dwh:
        # update new studio

        studio.name=name
        studio.daily_working_hours=int(dwh)

        wh = WorkingHours()

        def set_wh_for_day(day, start, end):
            if start != end:
                wh[day] = [[start.seconds/60, end.seconds/60]]
            else:
                wh[day] = []

        set_wh_for_day('mon', wh_mon_start, wh_mon_end)
        set_wh_for_day('tue', wh_tue_start, wh_tue_end)
        set_wh_for_day('wed', wh_wed_start, wh_wed_end)
        set_wh_for_day('thu', wh_thu_start, wh_thu_end)
        set_wh_for_day('fri', wh_fri_start, wh_fri_end)
        set_wh_for_day('sat', wh_sat_start, wh_sat_end)
        set_wh_for_day('sun', wh_sun_start, wh_sun_end)

        studio.working_hours = wh

        DBSession.add(studio)
        # Commit will be handled by the zope transaction extension

    return HTTPOk()


@view_config(route_name='auto_schedule_tasks')
def auto_schedule_tasks(request):
    """schedules all the tasks of active projects
    """
    logged_in_user = get_logged_in_user(request)

    # get the studio
    studio = Studio.query.first()

    if not studio:
        transaction.abort()
        return Response("There is no Studio instance\n"
                        "Please create a studio first", 500)

    project_id = request.params.get('project', -1)
    project = Project.query.filter(Project.id == project_id).first()
    logger.debug('project_id: %s' % project_id)

    tj_scheduler = TaskJugglerScheduler()
    studio.scheduler = tj_scheduler
    if project:
        studio.scheduler.projects = [project]

    try:
        stderr = studio.schedule(scheduled_by=logged_in_user)

        # update schedule timings to UTC
        studio.scheduling_started_at = \
            local_to_utc(studio.scheduling_started_at)
        studio.last_scheduled_at = local_to_utc(studio.last_scheduled_at)

        # invalidate cache regions
        from stalker_pyramid2.views.task import cached_query_tasks,\
            get_cached_user_tasks, get_cached_tasks_count
        invalidate_all_caches()
        check_all_tasks_status_by_schedule_model()

        c = StdErrToHTMLConverter(stderr)
        return Response(c.html(replace_links=True))
    except RuntimeError as e:
        c = StdErrToHTMLConverter(e)
        transaction.abort()
        return Response(c.html(replace_links=True), 500)


@view_config(
    route_name='schedule_info',
    renderer='json'
)
def schedule_info(request):
    """returns the last schedule info
    """
    # there should be only one studio
    sql_query = """
    select
        is_scheduling,
        "CurrentScheduler_SimpleEntities".id as is_scheduling_by_id,
        "CurrentScheduler_SimpleEntities".name as is_scheduling_by,
        (extract(epoch from scheduling_started_at::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as scheduling_started_at,
        (extract(epoch from last_scheduled_at::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as last_scheduled_at,
        extract(epoch from last_scheduled_at::timestamp AT TIME ZONE 'UTC' - scheduling_started_at::timestamp AT TIME ZONE 'UTC') as last_scheduling_duration,
        "LastScheduler_SimpleEntities".name as last_scheduled_by,
        (extract(epoch from "Studios".start::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as start,
        (extract(epoch from "Studios".end::timestamp AT TIME ZONE 'UTC') * 1000)::bigint as end
    from "Studios"
    left outer join "SimpleEntities" as "LastScheduler_SimpleEntities" on "Studios".last_scheduled_by_id = "LastScheduler_SimpleEntities".id
    left outer join "SimpleEntities" as "CurrentScheduler_SimpleEntities" on "Studios".is_scheduling_by_id = "CurrentScheduler_SimpleEntities".id
    """

    from stalker.db.session import DBSession
    result = DBSession.connection().execute(sql_query)
    r = result.fetchone()

    return {
        'is_scheduling': r[0],
        'is_scheduling_by_id': r[1],
        'is_scheduling_by': r[2],
        'scheduling_started_at': r[3],
        'last_scheduled_at': r[4],
        'last_scheduling_took': r[5],
        'last_scheduled_by': r[6],
        'start': r[7],
        'end': r[8]
    }


@view_config(
    route_name='studio_scheduling_mode'
)
def studio_scheduling_mode(request):
    """Sets the system to "in schedule" mode or "normal" mode. When the system
    is "in schedule" mode (Studio.is_scheduling == True) it is not allowed to
    schedule the system again until the previous one is finishes.
    """
    logged_in_user = get_logged_in_user(request)

    # get the studio
    studio = Studio.query.first()

    mode = request.params.get('mode')
    logger.debug('schedule mode: %s' % mode)

    if not studio:
        transaction.abort()
        return Response("There is no Studio instance\n"
                        "Please create a studio first", 500)

    if mode:  # set the mode
        mode = bool(int(mode))

        studio.is_scheduling = mode
        studio.is_scheduling_by = logged_in_user
        studio.scheduling_started_at = local_to_utc(datetime.datetime.now())

        return Response(
            "Successfully, set the scheduling mode to: %s" % mode
        )
