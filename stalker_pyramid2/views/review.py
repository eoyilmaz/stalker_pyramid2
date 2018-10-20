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

import transaction
from pyramid.response import Response
from pyramid.view import view_config

from stalker.db.session import DBSession
from stalker import User, Task, Project

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_config(
    route_name='get_task_reviewers',
    renderer='json'
)
def get_task_reviewers(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_task_reviewers is running')

    task_id = request.matchdict.get('id', -1)
    task = Task.query.filter(Task.id == task_id).first()

    if not task:
        transaction.abort()
        return Response('There is no task with id: %s' % task_id, 500)

    sql_query = """
        select
            "Reviewers".name as reviewers_name,
            "Reviewers".id as reviewers_id

        from "Reviews"
            join "Tasks" as "Review_Tasks" on "Review_Tasks".id = "Reviews".task_id
            join "SimpleEntities" as "Reviewers" on "Reviewers".id = "Reviews".reviewer_id

        %(where_conditions)s

        group by "Reviewers".id, "Reviewers".name
    """

    where_conditions = """where "Review_Tasks".id = %(task_id)s""" % {
        'task_id': task.id
    }

    logger.debug('where_conditions %s ' % where_conditions)

    sql_query = sql_query % {'where_conditions': where_conditions}

    result = DBSession.connection().execute(sql_query)

    return_data = [
        {
            'reviewer_name': r[0],
            'reviewer_id': r[1]
        }
        for r in result.fetchall()
    ]

    return return_data


@view_config(
    route_name='get_task_reviews',
    renderer='json'
)
def get_task_reviews(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_task_reviews is running')

    task_id = request.matchdict.get('id', -1)
    #task = Task.query.filter(Task.id == task_id).first()

    # if not task:
    #     transaction.abort()
    #     return Response('There is no task with id: %s' % task_id, 500)

    where_conditions = """where "Review_Tasks".id = %(task_id)s""" % {
        'task_id': task_id
    }

    return get_reviews(request, where_conditions)


@view_config(
    route_name='get_task_reviews_count',
    renderer='json'
)
def get_task_reviews_count(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_task_reviews_count is running')

    task_id = request.matchdict.get('id', -1)
    task = Task.query.filter(Task.id == task_id).first()

    if not task:
        transaction.abort()
        return Response('There is no task with id: %s' % task_id, 500)

    where_conditions = """where "Review_Tasks".id = %(task_id)s
    and "Reviews_Statuses".code ='NEW' """ % {'task_id': task_id}

    reviews = get_reviews(request, where_conditions)

    return len(reviews)


@view_config(
    route_name='get_task_last_reviews',
    renderer='json'
)
def get_task_last_reviews(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_task_last_reviews is running')

    task_id = request.matchdict.get('id', -1)
    task = Task.query.filter(Task.id == task_id).first()

    if not task:
        transaction.abort()
        return Response('There is no task with id: %s' % task_id, 500)

    where_condition1 = """where "Review_Tasks".id = %(task_id)s""" % {
        'task_id': task_id
    }
    where_condition2 = ''

    logger.debug("task.status.code : %s" % task.status.code)
    if task.status.code == 'PREV':
        where_condition2 = """ and "Review_Tasks".review_number +1 = "Reviews".review_number"""
        where_conditions = '%s %s' % (where_condition1, where_condition2)

        reviews = get_reviews(request, where_conditions)

    else:
        # where_condition2 =""" and "Review_Tasks".review_number = "Reviews".review_number"""

        reviews = [
            {
                'review_number': task.review_number,
                'review_id': 0,
                'review_status_code': 'WTNG',
                'review_status_name': 'Waiting',
                'review_status_color': 'wip',
                'task_id': task.id,
                'task_review_number': task.review_number,
                'reviewer_id': responsible.id,
                'reviewer_name': responsible.name,
                'reviewer_thumbnail_full_path':
                responsible.thumbnail.full_path
                if responsible.thumbnail else None,
                'reviewer_department': responsible.departments[0].name
            }
            for responsible in task.responsible
        ]

    return reviews


# @view_config(
#     route_name='get_user_reviews',
#     renderer='json'
# )
def get_user_reviews(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_user_reviews is running')

    reviewer_id = request.matchdict.get('id', -1)

    # also try to get reviews with specified status
    review_status = request.params.get('status', None)

    if review_status:
        where_conditions = \
        """where "Reviews".reviewer_id = %(reviewer_id)s and 
        "Reviews_Statuses".code = '%(status)s' """ % {
            'reviewer_id': reviewer_id,
            'status': review_status
        }
    else:
        where_conditions = """where "Reviews".reviewer_id = %(reviewer_id)s""" % {
            'reviewer_id': reviewer_id
        }

    return get_reviews(request, where_conditions)


# @view_config(
#     route_name='get_user_reviews_count',
#     renderer='json'
# )
def get_user_reviews_count(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_user_reviews_count is running')

    reviewer_id = request.matchdict.get('id', -1)
    reviewer = User.query.filter(User.id == reviewer_id).first()

    if not reviewer:
        transaction.abort()
        return Response('There is no user with id: %s' % reviewer_id, 500)

    where_conditions = """where "Reviews".reviewer_id = %(reviewer_id)s
    and "Reviews_Statuses".code ='NEW' """ % {'reviewer_id': reviewer_id}

    reviews = get_reviews(request, where_conditions)

    return len(reviews)


def get_project_reviews(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_project_reviews is running')

    project_id = request.matchdict.get('id', -1)
    project = Project.query.filter(Project.id == project_id).first()

    if not project:
        transaction.abort()
        return Response('There is no user with id: %s' % project_id, 500)

    where_conditions = 'where "Review_Tasks".project_id = %(project_id)s' %\
                       {'project_id': project_id}

    return get_reviews(request, where_conditions)


def get_project_reviews_count(request):
    """RESTful version of getting all reviews of a task
    """
    logger.debug('get_project_reviews_count is running')

    project_id = request.matchdict.get('id', -1)
    # project = Project.query.filter(Project.id == project_id).first()

    # if not project:
    #     transaction.abort()
    #     return Response('There is no project with id: %s' % project_id, 500)

    where_conditions = """
    where "Review_Tasks".project_id = %(project_id)s
    and "Reviews_Statuses".code = 'NEW'
    """ % {'project_id': project_id}

    reviews = get_reviews(request, where_conditions)

    return len(reviews)


def get_reviews(request, where_conditions):
    """TODO: add docstring
    """
    logger.debug('get_reviews is running')

    logged_in_user = get_logged_in_user(request)

    sql_query = """
    select
        "Reviews".review_number as review_number,
        "Reviews".id as review_id,
        "Reviews_Statuses".code as review_status_code,
        "Statuses_Simple_Entities".name as review_status_name,
        "Statuses_Simple_Entities".html_class as review_status_color,
        "Reviews".task_id as task_id,
        "ParentTasks".full_path as task_name,
        "Review_Tasks".review_number as task_review_number,
        "Reviews".reviewer_id as reviewer_id,
        "Reviewers_SimpleEntities".name as reviewer_name,
        "Reviewers_SimpleEntities_Links".full_path as reviewer_thumbnail_path,
        array_agg("Reviewer_Departments_SimpleEntities".name) as reviewer_departments,
        extract(epoch from"Reviews_Simple_Entities".date_created::timestamp AT TIME ZONE 'UTC') * 1000 as date_created,
        "Reviews_Simple_Entities".description,
        "Review_Types".name as type_name

    from "Reviews"
        join "SimpleEntities" as "Reviews_Simple_Entities" on "Reviews_Simple_Entities".id = "Reviews".id
        join "Tasks" as "Review_Tasks" on "Review_Tasks".id = "Reviews".task_id
        join "Statuses" as "Reviews_Statuses" on "Reviews_Statuses".id = "Reviews".status_id
        join "SimpleEntities" as "Statuses_Simple_Entities" on "Statuses_Simple_Entities".id = "Reviews".status_id
        join "SimpleEntities" as "Reviewers_SimpleEntities" on "Reviewers_SimpleEntities".id = "Reviews".reviewer_id
        join "Department_Users" as "Reviewers_Departments" on "Reviewers_Departments".uid = "Reviews".reviewer_id
        join "SimpleEntities" as "Reviewer_Departments_SimpleEntities" on "Reviewer_Departments_SimpleEntities".id = "Reviewers_Departments".did
        left join "SimpleEntities" as "Review_Types" on "Reviews_Simple_Entities".type_id = "Review_Types".id
        left join (%(recursive_task_query)s) as "ParentTasks" on "Review_Tasks".id = "ParentTasks".id

        left outer join "Links" as "Reviewers_SimpleEntities_Links" on "Reviewers_SimpleEntities_Links".id = "Reviewers_SimpleEntities".thumbnail_id

    %(where_conditions)s

    group by

        "Reviews".review_number,
        "Reviews".id,
        "Reviews_Statuses".code,
        "Reviews_Simple_Entities".date_created,
        "Statuses_Simple_Entities".name,
        "Statuses_Simple_Entities".html_class,
        "Reviews".task_id,
        "ParentTasks".full_path,
        "Review_Tasks".review_number,
        "Reviews".reviewer_id,
        "Reviewers_SimpleEntities".name,
        "Reviewers_SimpleEntities_Links".full_path,
        "Reviews_Simple_Entities".description,
        "Review_Types".name

    order by "Reviews_Simple_Entities".date_created desc
    """

    # logger.debug('where_conditions: %s ' % where_conditions)

    sql_query = sql_query % {
        'where_conditions': where_conditions,
        'recursive_task_query': generate_recursive_task_query()
    }

    result = DBSession.connection().execute(sql_query)

    return_data = [
        {
            'review_number': r[0],
            'review_id': r[1],
            'review_status_code': r[2].lower(),
            'review_status_name': r[3],
            'review_status_color': r[4],
            'task_id': r[5],
            'task_name': r[6],
            'task_review_number': r[7],
            'reviewer_id': r[8],
            'reviewer_name': r[9],
            'reviewer_thumbnail_full_path':r[10],
            'reviewer_department':r[11],
            'date_created':r[12],
            'is_reviewer':'1' if logged_in_user.id == r[8] else None,
            'review_description': r[13],
            'review_type': r[14] if r[14] else ''
        }
        for r in result.fetchall()
    ]

    return return_data


def get_reviews_count(request, where_conditions):
    """returns the count of reviews
    """
    sql_query = """
select
    count(1)
from "Reviews"
    join "Tasks" as "Review_Tasks" on "Review_Tasks".id = "Reviews".task_id
    join "Statuses" as "Reviews_Statuses" on "Reviews_Statuses".id = "Reviews".status_id
where %(where_conditions)s
    """

    sql_query = sql_query % {
        'where_conditions': where_conditions
    }

    return DBSession.connection().execute(sql_query).fetchone()[0]
