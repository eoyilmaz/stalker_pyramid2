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
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class StructureViews(EntityViews):
    """views for Structure class
    """
    from stalker import Structure
    som_class = Structure
    local_params = [
        {'param_name': 'custom_template'},
        {
            'param_name': 'template_id',
            'arg_name': 'templates',
            'interpreter': simple_entity_interpreter,
            'is_list': True
        },
    ]

    @view_config(
        route_name='structure',
        request_method='GET'
    )
    def get_entity(self):
        """returns one Structure instance data as JSON
        """
        response = super(StructureViews, self).get_entity()

        from stalker import Structure
        from stalker.db.session import DBSession
        r = DBSession.query(Structure.custom_template)\
            .filter(Structure.id == self.entity_id)\
            .first()

        # get template counts
        from stalker.models.structure import Structure_FilenameTemplates
        template_count = \
            DBSession.query(
                Structure_FilenameTemplates.c.filenametemplate_id
            ).filter(
                Structure_FilenameTemplates.c.structure_id == self.entity_id
            ).count()

        from stalker_pyramid2 import entity_type_to_url
        data = {
            'custom_template': r[0],
            'templates': {
                '$ref': '%s/%s/templates' %
                        (entity_type_to_url['Structure'], self.entity_id),
                'length': template_count
            }
        }
        return self.update_response_data(response, data)

    @view_config(
        route_name='structures',
        request_method='GET'
    )
    def get_entities(self):
        """returns multiple Structure data as JSON
        """
        return super(StructureViews, self).get_entities()

    @view_config(
        route_name='structure',
        request_method=['PATCH', 'POST']
    )
    def update_entity(self):
        """updates one Structure instance data
        """
        return super(StructureViews, self).update_entity()

    @view_config(
        route_name='structures',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a new Structure instance
        """
        return super(StructureViews, self).create_entity()

    @view_config(
        route_name='structure',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes one Structure instance
        """
        return super(StructureViews, self).delete_entity()

    @view_config(
        route_name='structure_templates',
        request_method='GET'
    )
    def get_templates(self):
        """returns filename templates related to this Structure
        """
        from stalker import FilenameTemplate
        from stalker.models.structure import Structure_FilenameTemplates
        join = Structure_FilenameTemplates
        filters = \
            [Structure_FilenameTemplates.c.structure_id == self.entity_id]
        filters.extend(self.filter_generator(FilenameTemplate))
        return self.collection_query(
            FilenameTemplate,
            join=join,
            filters=filters
        )

    @view_config(
        route_name='structure_templates',
        request_method=['PATCH', 'POST']
    )
    def update_templates(self):
        """updates filename templates of this Structure
        """
        ft_ids = self.get_multi_integer(self.request, 'template_id')
        from stalker import FilenameTemplate
        fts = FilenameTemplate.query\
            .filter(FilenameTemplate.id.in_(ft_ids)).all()

        if self.request.method == 'PATCH':
            self.entity.templates += fts
        elif self.request.method == 'POST':
            self.entity.templates = fts

    @view_config(
        route_name='structure_templates',
        request_method='DELETE'
    )
    def remove_templates(self):
        """removes filename templates from this Structure
        """
        ft_ids = self.get_multi_integer(self.request, 'template_id')
        from stalker import FilenameTemplate
        fts = FilenameTemplate.query\
            .filter(FilenameTemplate.id.in_(ft_ids)).all()

        for ft in fts:
            try:
                self.entity.templates.remove(ft)
            except ValueError:
                pass
