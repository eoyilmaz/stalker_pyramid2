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
from stalker_pyramid2.views.entity import EntityViews

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


@view_defaults(renderer='json')
class FilenameTemplateViews(EntityViews):
    """views for FilenameTemplate class
    """
    from stalker import FilenameTemplate
    som_class = FilenameTemplate
    local_params = [
        {'param_name': 'target_entity_type'},
        {'param_name': 'path'},
        {'param_name': 'filename'},
    ]

    @view_config(
        route_name='filename_template',
        request_method='GET'
    )
    def get_entity(self):
        """returns one FilenameTemplate instance data as JSON
        """
        response = super(FilenameTemplateViews, self).get_entity()

        from stalker.db.session import DBSession
        from stalker import FilenameTemplate
        r = DBSession\
            .query(
                FilenameTemplate.target_entity_type, FilenameTemplate.path,
                FilenameTemplate.filename
            )\
            .filter(FilenameTemplate.id == self.entity_id)\
            .first()

        data = {
            'target_entity_type': r[0],
            'path': r[1],
            'filename': r[2],
        }

        return self.update_response_data(response, data)

    @view_config(
        route_name='filename_templates',
        request_method='GET'
    )
    def get_entities(self):
        """returns all of the FilenameTemplates in the database
        """
        return super(FilenameTemplateViews, self).get_entities()

    @view_config(
        route_name='filename_templates',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a FilenameTemplate instance and returns it as JSON
        """
        return super(FilenameTemplateViews, self).create_entity()

    @view_config(
        route_name='filename_template',
        request_method='PATCH'
    )
    def update_entity(self):
        """updates one FilenameTemplate instance
        """
        return super(FilenameTemplateViews, self).update_entity()

    @view_config(
        route_name='filename_template',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes one FilenameTemplate
        """
        return super(FilenameTemplateViews, self).delete_entity()
