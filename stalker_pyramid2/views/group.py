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
from stalker import Group
from stalker_pyramid2.views import simple_entity_interpreter
from stalker_pyramid2.views.entity import EntityViews

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def permission_interpreter(value):
    """an interpreter for permission values
    """
    # get the params
    if isinstance(value, (list, tuple)):
        all_permissions = []
        for p_value in value:
            access, action, class_name = p_value.split('_')

            # get the permission instance
            from stalker import Permission
            p = Permission.query\
                .filter(Permission.access == access)\
                .filter(Permission.action == action)\
                .filter(Permission.class_name == class_name)\
                .first()
            if p:
                all_permissions.append(p)

        return all_permissions
    else:
        access, action, class_name = value.split('_')

        # get the permission instance
        from stalker import Permission
        return Permission.query \
            .filter(Permission.access == access) \
            .filter(Permission.action == action) \
            .filter(Permission.class_name == class_name) \
            .first()


@view_defaults(renderer='json')
class GroupViews(EntityViews):
    """views for Group class
    """
    som_class = Group
    local_params = [
        # complex params
        {
            'param_name': 'user_id',
            'arg_name': 'users',
            'is_list': True,
            'nullable': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'permission',
            'arg_name': 'permissions',
            'is_list': True,
            'nullable': True,
            'interpreter': permission_interpreter
        }
    ]

    @view_config(
        route_name='group',
        request_method='GET'
    )
    def get_entity(self):
        """return one Group instance data as JSON
        """
        # get supers response
        response = super(GroupViews, self).get_entity()

        # get entity type
        entity_type = response.json_body['entity_type']

        # get user count
        from stalker.db.session import DBSession
        from stalker.models.auth import Group_Users
        user_count = DBSession.query(Group_Users.c.uid)\
            .filter(Group_Users.c.gid == self.entity_id)\
            .count()

        # get permission count
        sql = """select
            "Permissions".access || '_' || "Permissions".action || '_' || "Permissions".class_name
        from "Group_Permissions"
        join "Permissions" on "Group_Permissions".permission_id = "Permissions".id
        where "Group_Permissions".group_id = :id
        """
        from sqlalchemy import text
        conn = DBSession.connection()
        permissions = conn.execute(text(sql), id=self.entity_id).fetchall()

        # prepare data
        from stalker_pyramid2 import entity_type_to_url
        data = {
            'permissions': [r[0] for r in permissions],
            'users': {
                '$ref': '%s/%s/users' %
                        (entity_type_to_url[entity_type], self.entity_id),
                'length': user_count
            }
        }

        # update supers response with our data and return
        return self.update_response_data(response, data)

    @view_config(
        route_name='groups',
        request_method='GET'
    )
    def get_entities(self):
        """returns all Group instances in the database
        """
        return super(GroupViews, self).get_entities()

    @view_config(
        route_name='group',
        request_method=['PATCH', 'POST']
    )
    def update_entity(self):
        """updates a Group instance
        """
        return super(GroupViews, self).update_entity()

    @view_config(
        route_name='group',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes one Group instance
        """
        return super(GroupViews, self).delete_entity()

    @view_config(
        route_name='groups',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a new Group instance
        """
        return super(GroupViews, self).create_entity()

    @view_config(
        route_name='group_users',
        request_method='GET'
    )
    def get_users(self):
        """returns the Group.users attribute as JSON data
        """
        from stalker.models.auth import User, Group_Users
        join = Group_Users
        filters = [Group_Users.c.gid == self.entity_id]
        filters.extend(self.filter_generator(User))
        return self.collection_query(User, join=join, filters=filters)

    @view_config(
        route_name='group_users',
        request_method=['PATCH', 'POST']
    )
    def update_users(self):
        """updates the Group.users attribute content
        """
        user_ids = self.get_multi_integer(self.request, 'user_id')

        from stalker import User
        users = User.query.filter(User.id.in_(user_ids)).all()

        if self.request.method == 'PATCH':
            self.entity.users += users
        elif self.request.method == 'POST':
            self.entity.users = users

    @view_config(
        route_name='group_users',
        request_method='DELETE'
    )
    def remove_users(self):
        """removes the users from Group.users attribute
        """
        user_ids = self.get_multi_integer(self.request, 'user_id')

        from stalker import User
        users = User.query.filter(User.id.in_(user_ids)).all()

        for user in users:
            try:
                self.entity.users.remove(user)
            except ValueError:
                pass
