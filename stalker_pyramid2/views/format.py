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

from stalker import ImageFormat
from pyramid.view import view_defaults, view_config
from stalker_pyramid2.views.entity import EntityViews

import logging
from stalker import log
logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)


@view_defaults(renderer='json')
class ImageFormatViews(EntityViews):
    """views for ImageFormat class
    """
    som_class = ImageFormat
    local_params = [
        {'param_name': 'width', 'interpreter': int},
        {'param_name': 'height', 'interpreter': int},
        {'param_name': 'pixel_aspect', 'interpreter': float},
        {'param_name': 'print_resolution', 'interpreter': float}
    ]

    @view_config(
        route_name='image_format',
        request_method='GET',
        renderer='json'
    )
    def get_entity(self):
        """returns one ImageFormat instance data as json
        """
        sql = """select
            "ImageFormats".id,
            "ImageFormats".width,
            "ImageFormats".height,
            "ImageFormats".pixel_aspect,
            "ImageFormats".print_resolution
        from "ImageFormats"
        where "ImageFormats".id = :id
        """
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        from sqlalchemy import text
        result = conn.execute(text(sql), id=self.entity_id)

        r = result.fetchone()
        data = {
            'id': r[0],
            'width': r[1],
            'height': r[2],
            'pixel_aspect': r[3],
            'print_resolution': r[4],
        }

        response = super(ImageFormatViews, self).get_entity()
        return self.update_response_data(response, data)

    @view_config(
        route_name='image_formats',
        request_method='GET',
        renderer='json'
    )
    def get_entities(self):
        """returns all the ImageFormat instances in the db
        """
        return super(ImageFormatViews, self).get_entities()

    @view_config(
        route_name='image_formats',
        request_method='PUT',
        renderer='json'
    )
    def create_entity(self):
        """creates an ImageFormat instance
        """
        return super(ImageFormatViews, self).create_entity()

    @view_config(
        route_name='image_format',
        request_method=['PATCH', 'POST'],
        renderer='json'
    )
    def update_entity(self):
        """updates one ImageFormat instance
        """
        return super(ImageFormatViews, self).update_entity()

    @view_config(
        route_name='image_format',
        request_method='DELETE',
        renderer='json'
    )
    def delete_entity(self):
        """deletes one ImageFormat instance
        """
        return super(ImageFormatViews, self).delete_entity()
