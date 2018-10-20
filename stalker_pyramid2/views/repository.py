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
from pyramid.view import view_defaults, view_config

from stalker_pyramid2.views.entity import EntityViews

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


@view_defaults(renderer='json')
class RepositoryViews(EntityViews):
    """views for Repository class
    """
    from stalker import Repository
    som_class = Repository
    local_params = [
        {'param_name': 'windows_path'},
        {'param_name': 'linux_path'},
        {'param_name': 'osx_path'},
    ]

    @view_config(
        route_name='repository',
        request_method='GET'
    )
    def get_entity(self):
        """returns one Repository instance data as JSON
        """
        response = super(RepositoryViews, self).get_entity()

        from stalker import Repository
        from stalker.db.session import DBSession
        r = DBSession.query(
            Repository.windows_path,
            Repository.linux_path,
            Repository.osx_path)\
            .filter(Repository.id == self.entity_id)\
            .first()

        data = {
            'windows_path': r[0],
            'linux_path': r[1],
            'osx_path': r[2]
        }

        return self.update_response_data(response, data)

    @view_config(
        route_name='repositories',
        request_method='GET'
    )
    def get_entities(self):
        """returns all the Repositories in the database
        """
        return super(RepositoryViews, self).get_entities()

    @view_config(
        route_name='repository',
        request_method=['PATCH', 'POST']
    )
    def update_entity(self):
        """updates one Repository instance
        """
        return super(RepositoryViews, self).update_entity()

    @view_config(
        route_name='repositories',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a single Repository instance
        """
        return super(RepositoryViews, self).create_entity()

    @view_config(
        route_name='repository',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes a single Repository instance
        """
        return super(RepositoryViews, self).delete_entity()
