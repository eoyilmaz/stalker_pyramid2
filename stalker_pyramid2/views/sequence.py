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

from pyramid.httpexceptions import HTTPServerError, HTTPOk
from pyramid.view import view_config

from stalker.db.session import DBSession
from stalker import Project, StatusList, Status, Sequence, Entity


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_config(
    route_name='create_sequence'
)
def create_sequence(request):
    """runs when adding a new sequence
    """
    logged_in_user = get_logged_in_user(request)

    name = request.params.get('name')
    code = request.params.get('code')

    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()

    project_id = request.params.get('project_id')
    project = Project.query.filter_by(id=project_id).first()

    logger.debug('project_id   : %s' % project_id)

    if name and code and status and project:
        # get descriptions
        description = request.params.get('description')

        # get the status_list
        status_list = StatusList.query.filter_by(
            target_entity_type='Sequence'
        ).first()

        # there should be a status_list
        # TODO: you should think about how much possible this is
        if status_list is None:
            return HTTPServerError(detail='No StatusList found')

        new_sequence = Sequence(
            name=name,
            code=code,
            description=description,
            status_list=status_list,
            status=status,
            created_by=logged_in_user,
            project=project
        )

        DBSession.add(new_sequence)

    else:
        logger.debug('there are missing parameters')
        logger.debug('name      : %s' % name)
        logger.debug('code      : %s' % code)
        logger.debug('status    : %s' % status)
        logger.debug('project   : %s' % project)
        HTTPServerError()

    return HTTPOk()


@view_config(
    route_name='update_sequence'
)
def update_sequence(request):
    """runs when adding a new sequence
    """
    logged_in_user = get_logged_in_user(request)

    sequence_id = request.params.get('sequence_id')
    sequence = Sequence.query.filter_by(id=sequence_id).first()

    name = request.params.get('name')
    code = request.params.get('code')

    status_id = request.params.get('status_id')
    status = Status.query.filter_by(id=status_id).first()

    if sequence and code and name and status:
        # get descriptions
        description = request.params.get('description')

        #update the sequence
        sequence.name = name
        sequence.code = code
        sequence.description = description
        sequence.status = status
        sequence.updated_by = logged_in_user
        sequence.date_updated = datetime.datetime.now()

        DBSession.add(sequence)

    else:
        logger.debug('there are missing parameters')
        logger.debug('name      : %s' % name)
        logger.debug('status    : %s' % status)
        HTTPServerError()

    return HTTPOk()


@view_config(
    route_name='get_sequences',
    renderer='json'
)
def get_sequences(request):
    """returns all sequences as a json data
    """
    return [
        {
            'id': sequence.id,
            'name': sequence.name,
            'status': sequence.status.name,
            'status_color': sequence.status.html_class,
            'entity_id': sequence.created_by.id,
            'user_name': sequence.created_by.name,
            'thumbnail_full_path': sequence.thumbnail.full_path
            if sequence.thumbnail else None
        }
        for sequence in Sequence.query.all()
    ]


@view_config(
    route_name='get_entity_sequences_count',
    renderer='json'
)
def get_project_sequences_count(request):
    """returns the count of sequences in a project
    """
    project_id = request.matchdict.get('id', -1)

    sql_query = """select
        count(1)
    from "Sequences"
        join "Tasks" on "Sequences".id = "Tasks".id
    where "Tasks".project_id = %s""" % project_id

    return DBSession.connection().execute(sql_query).fetchone()[0]


@view_config(
    route_name='get_entity_sequences',
    renderer='json'
)
def get_project_sequences(request):
    """returns the related sequences of the given project as a json data
    """
    # TODO: use pure SQL query
    entity_id = request.matchdict.get('id', -1)
    entity = Entity.query.filter_by(id=entity_id).first()

    return [
        {
            'thumbnail_full_path': sequence.thumbnail.full_path
            if sequence.thumbnail else None,
            'code': sequence.code,
            'id': sequence.id,
            'name': sequence.name,
            'status': sequence.status.name,
            'status_color': sequence.status.html_class
            if sequence.status.html_class else 'grey',
            'created_by_id': sequence.created_by.id,
            'created_by_name': sequence.created_by.name,
            'description': sequence.description,
            'date_created': milliseconds_since_epoch(sequence.date_created),
            'percent_complete': sequence.percent_complete
        }
        for sequence in entity.sequences
    ]
