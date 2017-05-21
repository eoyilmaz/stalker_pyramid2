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

from pyramid.view import view_config, view_defaults
from stalker import Department

import logging

from stalker_pyramid.views.entity import EntityViews, simple_entity_interpreter

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


# @view_config(
#     route_name='create_department'
# )
# def create_department(request):
#     """creates a new Department
#     """
#
#     logger.debug('***create department method starts ***')
#
#     logged_in_user = get_logged_in_user(request)
#
#     # get params
#     came_from = request.params.get('came_from', '/')
#     name = request.params.get('name')
#
#     logger.debug('new department name : %s' % name)
#
#     if name:
#         description = request.params.get('description')
#
#         lead_id = request.params.get('lead_id', -1)
#         lead = User.query.filter_by(id=lead_id).first()
#
#         # Tags
#         tags = get_tags(request)
#
#         logger.debug('new department description : %s' % description)
#         logger.debug('new department lead : %s' % lead)
#         logger.debug('new department tags : %s' % tags)
#
#         try:
#             new_department = Department(
#                 name=name,
#                 description=description,
#                 created_by=logged_in_user,
#                 tags=tags
#             )
#
#             # create a new Department_User with lead role
#             lead_role = query_role('Lead')
#             dpu = DepartmentUser(
#                 department=new_department,
#                 user=lead,
#                 role=lead_role
#             )
#
#             DBSession.add(new_department)
#             DBSession.add(dpu)
#
#             logger.debug('added new department successfully!')
#
#             request.session.flash(
#                 'success:Department <strong>%s</strong> is created '
#                 'successfully!' % name
#             )
#
#             logger.debug('***create department method ends ***')
#
#         except BaseException as e:
#             request.session.flash('error: %s' % e)
#             HTTPFound(location=came_from)
#     else:
#         logger.debug('not all parameters are in request.params')
#         log_param(request, 'name')
#         response = Response(
#             'There are missing parameters: '
#             'name: %s' % name, 500
#         )
#         transaction.abort()
#         return response
#
#     response = Response('successfully created %s department!' % name)
#     return response
#
#
# @view_config(
#     route_name='update_department'
# )
# def update_department(request):
#     """updates an Department
#     """
#
#     logger.debug('***update department method starts ***')
#
#     logged_in_user = get_logged_in_user(request)
#
#     # get params
#     came_from = request.params.get('came_from', '/')
#     department_id = request.matchdict.get('id', -1)
#     department = Department.query.filter_by(id=department_id).first()
#
#     name = request.params.get('name')
#
#     logger.debug('department : %s' % department)
#     logger.debug('department new name : %s' % name)
#
#     if department and name:
#
#         description = request.params.get('description')
#
#         lead_id = request.params.get('lead_id', -1)
#         lead = User.query.filter_by(id=lead_id).first()
#
#         # Tags
#         tags = get_tags(request)
#
#         logger.debug('department new description : %s' % description)
#         logger.debug('department new lead : %s' % lead)
#         logger.debug('department new tags : %s' % tags)
#
#         # update the department
#         department.name = name
#         department.description = description
#
#         department.lead = lead
#         lead_role = query_role('Lead')
#         # get the current department lead
#         dpu = DepartmentUser.query\
#             .filter(DepartmentUser.department == department)\
#             .filter(DepartmentUser.role == lead_role)\
#             .first()
#         if not dpu:
#             dpu = DepartmentUser(
#                 department=department,
#                 user=lead,
#                 role=lead_role
#             )
#             DBSession.add(dpu)
#         else:
#             dpu.user = lead
#
#         department.tags = tags
#         department.updated_by = logged_in_user
#         department.date_updated = datetime.datetime.now()
#
#         DBSession.add(department)
#
#         logger.debug('department is updated successfully')
#
#         request.session.flash(
#             'success:Department <strong>%s</strong> '
#             'is updated successfully' % name
#         )
#
#         logger.debug('***update department method ends ***')
#     else:
#         logger.debug('not all parameters are in request.params')
#         log_param(request, 'department_id')
#         log_param(request, 'name')
#         HTTPServerError()
#
#     return Response('Successfully updated department: %s' % department_id)
#
#
# @view_config(
#     route_name='get_departments',
#     renderer='json'
# )
# def get_departments(request):
#     """returns all the departments in the database
#     """
#     return [
#         {
#             'id': dep.id,
#             'name': dep.name
#         }
#         for dep in Department.query.order_by(Department.name.asc()).all()
#     ]
#
#
# @view_config(
#     route_name='get_department',
#     renderer='json'
# )
# def get_department(request):
#     """returns all the departments in the database
#     """
#     department_id = request.matchdict.get('id', -1)
#     department = Department.query.filter_by(id=department_id).first()
#
#     return[
#         {
#             'id': department.id,
#             'name': department.name,
#             'thumbnail_full_path': department.thumbnail.full_path if department.thumbnail else None,
#         }
#     ]
#
#
# @view_config(
#     route_name='get_departments',
#     renderer='json'
# )
# def get_departments(request):
#     """returns all the departments in the database
#     """
#     sql_query = """select
#     "SimpleEntities".id
#     "SimpleEntities".name
# from "Departments"
# join "SimpleEntities" on "Departments".id = "SimpleEntities".id
# order by "SimpleEntities".name
# """
#
#     result = DBSession.connection().execute(sql_query)
#
#     return [
#         {
#             'id': r[0],
#             'name': r[1]
#         }
#         for r in result.fetchall()
#     ]
#
#
# @view_config(
#     route_name='delete_department',
#     permission='Delete_Department'
# )
# def delete_department(request):
#     """deletes the department with the given id
#     """
#     department_id = request.matchdict.get('id')
#     department = Department.query.get(department_id)
#     name = department.name
#
#     if not department:
#         transaction.abort()
#         return Response(
#             'Can not find a Department with id: %s' % department_id, 500
#         )
#
#     try:
#         DBSession.delete(department)
#         transaction.commit()
#     except Exception as e:
#         transaction.abort()
#         c = StdErrToHTMLConverter(e)
#         transaction.abort()
#         return Response(c.html(), 500)
#
#     request.session.flash(
#         'success: <strong>%s Department</strong> is deleted '
#         'successfully' % name
#     )
#
#     return Response('Successfully deleted department: %s' % department_id)


@view_defaults(renderer='json')
class DepartmentViews(EntityViews):
    """views for Department instances
    """
    som_class = Department
    local_params = [
        {
            'param_name': 'user_id',
            'arg_name': 'users',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
    ]

    @view_config(
        route_name='department',
        request_method='GET'
    )
    def get_entity(self):
        """returns one Department instance data as JSON
        """
        response = super(DepartmentViews, self).get_entity()

        # get entity type
        from stalker import SimpleEntity
        from stalker.db.session import DBSession
        entity_type = DBSession.query(SimpleEntity.entity_type)\
            .filter(SimpleEntity.id == self.entity_id)\
            .first()[0]

        # get user count
        from stalker import DepartmentUser
        user_count = DBSession\
            .query(DepartmentUser.user_id)\
            .filter(DepartmentUser.department_id == self.entity_id)\
            .count()

        from stalker_pyramid import entity_type_to_url
        data = {
            'user_roles': {
                '$ref': '%s/%s/user_roles' %
                        (entity_type_to_url[entity_type], self.entity_id),
                'length': user_count
            },
            'users': {
                '$ref': '%s/%s/users' %
                        (entity_type_to_url[entity_type], self.entity_id),
                'length': user_count
            }
        }

        return self.update_response_data(response, data)

    @view_config(
        route_name='departments',
        request_method='GET'
    )
    def get_entities(self):
        """returns all Department instances
        """
        return super(DepartmentViews, self).get_entities()

    @view_config(
        route_name='department',
        request_method=['PATCH', 'POST']
    )
    def update_entity(self):
        """updates a Department instance
        """
        return super(DepartmentViews, self).update_entity()

    @view_config(
        route_name='departments',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a Department instance
        """
        return super(DepartmentViews, self).create_entity()

    @view_config(
        route_name='department',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes a Department instance
        """
        return super(DepartmentViews, self).delete_entity()

    @view_config(
        route_name='department_users',
        request_method='GET'
    )
    def get_users(self):
        """returns department users as JSON data
        # """
        from stalker import DepartmentUser, User
        join = User, DepartmentUser.user
        filters = [DepartmentUser.department_id == self.entity_id]
        filters.extend(self.filter_generator(User))
        return self.collection_query(User, join=join, filters=filters)

    @view_config(
        route_name='department_users',
        request_method=['PATCH', 'POST']
    )
    def update_users(self):
        """updates Department.users
        """
        # get user ids
        user_ids = self.get_multi_integer(self.request, 'user_id')
        from stalker import User
        users = User.query.filter(User.id.in_(user_ids)).all()

        from stalker.db.session import DBSession
        if self.request.method == 'PATCH':
            with DBSession.no_autoflush:
                self.entity.users += users
        elif self.request.method == 'POST':
            with DBSession.no_autoflush:
                self.entity.users = users

    @view_config(
        route_name='department_users',
        request_method='DELETE'
    )
    def remove_users(self):
        """removes users from Department.users attribute
        """
        # get user ids
        user_ids = self.get_multi_integer(self.request, 'user_id')
        from stalker import User
        users = User.query.filter(User.id.in_(user_ids)).all()

        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            for user in users:
                try:
                    self.entity.users.remove(user)
                except ValueError:
                    pass

        DBSession.flush()

    @view_config(
        route_name='department_user_roles',
        request_method='GET'
    )
    def get_user_roles(self):
        """returns department users as JSON data
        """
        sql = """
        select
            user_se.id,
            user_se.name,
            user_se.entity_type,

            role_se.id,
            role_se.name,
            role_se.entity_type
        from "Department_Users" as du
        join "SimpleEntities" as user_se on du.uid = user_se.id
        left outer join "SimpleEntities" as role_se on du.rid = role_se.id
        where du.did = :id
        """
        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        result = conn.execute(text(sql), id=self.entity_id).fetchall()

        from stalker_pyramid import entity_type_to_url
        data = [{
            'user': {
                'id': r[0],
                'name': r[1],
                'entity_type': r[2],
                '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0])
            },
            'role': {
                'id': r[3],
                'name': r[4],
                'entity_type': r[5],
                '$ref': '%s/%s' % (entity_type_to_url[r[5]], r[3])
            } if r[3] else None
        } for r in result]

        from pyramid.response import Response
        return Response(
            json_body=data,
            status=200
        )

    @view_config(
        route_name='department_user_roles',
        request_method=['PATCH', 'POST']
    )
    def update_user_role(self):
        """updates user roles
        """
        # get parameters
        user_role_ids = self.request.params.getall('user_role')

        from stalker import DepartmentUser
        for user_role_id in user_role_ids:
            user_id, role_id = user_role_id.split(',')

            department_user = DepartmentUser.query\
                .filter(DepartmentUser.department_id == self.entity_id)\
                .filter(DepartmentUser.user_id == user_id)\
                .first()

            if department_user:
                department_user.role_id = role_id

    @view_config(
        route_name='department_user_roles',
        request_method='DELETE'
    )
    def remove_user_role(self):
        """removes user roles
        """
        # get parameters
        user_ids = map(int, self.request.params.getall('user_id'))

        from stalker import DepartmentUser
        for user_id in user_ids:
            department_user = DepartmentUser.query\
                .filter(DepartmentUser.department_id == self.entity_id)\
                .filter(DepartmentUser.user_id == user_id)\
                .first()

            if department_user:
                department_user.role_id = None

