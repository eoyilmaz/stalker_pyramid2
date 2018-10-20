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
from stalker import User
from stalker_pyramid2.views import simple_entity_interpreter
from stalker_pyramid2.views.entity import EntityViews

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class UserViews(EntityViews):
    """the user view
    """
    som_class = User
    local_params = [
        # simple arguments/attributes
        {'param_name': 'login', 'nullable': False},
        {'param_name': 'email', 'nullable': False},
        {'param_name': 'password', 'nullable': False},
        {'param_name': 'efficiency', 'interpreter': float},
        {'param_name': 'rate', 'interpreter': float},

        # complex arguments/attributes
        {
            'param_name': 'department_id',
            'arg_name': 'departments',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'company_id',
            'arg_name': 'companies',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'group_id',
            'arg_name': 'groups',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
    ]

    # User - Base
    @view_config(
        route_name='user',
        request_method='GET',
        permission='Read_User',
    )
    def get_entity(self):
        """returns one User instance
        """
        sql_query = """select
            "Users".id,
            "Users".login,
            "Users".email,
            "Users".rate
        from "Users"
        where "Users".id = :id
        """

        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        result = conn.execute(text(sql_query), id=self.entity_id)
        r = result.fetchone()

        # get department count
        from stalker import DepartmentUser
        department_count = DBSession.query(DepartmentUser.user_id)\
            .filter(DepartmentUser.user_id == self.entity_id)\
            .count()

        # get group count
        from stalker.models.auth import Group_Users
        group_count = DBSession.query(Group_Users.c.gid)\
            .filter(Group_Users.c.uid == self.entity_id)\
            .count()

        # get project count
        from stalker import ProjectUser
        projects_count = DBSession.query(ProjectUser.project_id)\
            .filter(ProjectUser.user_id == self.entity_id)\
            .count()

        # get reviews count
        from stalker import Review
        reviews_count = DBSession.query(Review.id)\
            .filter(Review.reviewer_id == self.entity_id)\
            .count()

        # get pending reviews count
        from stalker import Status
        new_status_id = DBSession.query(Status.id)\
            .filter(Status.code == 'NEW')\
            .first()
        pending_reviews_count = DBSession.query(Review.id)\
            .filter(Review.reviewer_id == self.entity_id)\
            .filter(Review.status_id == new_status_id)\
            .count()

        # get tasks count
        from stalker.models.task import Task_Resources
        tasks_count = DBSession.query(Task_Resources.c.task_id)\
            .filter(Task_Resources.c.resource_id == self.entity_id)\
            .count()

        # get tickets count
        from stalker import Ticket
        tickets_count = DBSession.query(Ticket.id)\
            .filter(Ticket.owner_id == self.entity_id)\
            .count()

        # get open tickets count
        closed_status_id = DBSession.query(Status.id)\
            .filter(Status.code=='CLS')\
            .first()

        open_ticket_count = DBSession.query(Ticket.id)\
            .filter(Ticket.owner_id == self.entity_id)\
            .filter(Ticket.status_id != closed_status_id)\
            .count()

        # get vacations count
        from stalker import Vacation
        vacations_count = DBSession.query(Vacation.id)\
            .filter(Vacation.user_id == self.entity_id)\
            .count()

        if r:
            from stalker_pyramid2 import entity_type_to_url
            users_url = entity_type_to_url['User']
            data = {
                'id': r[0],
                'login': r[1],
                'email': r[2],
                'rate': r[3],
                'departments': {
                    '$ref': '%s/%s/departments' % (users_url, r[0]),
                    'length': department_count
                },
                'groups': {
                    '$ref': '%s/%s/groups' % (users_url, r[0]),
                    'length': group_count
                },
                'projects': {
                    '$ref': '%s/%s/projects' % (users_url, r[0]),
                    'length': projects_count
                },
                'reviews': {
                    '$ref': '%s/%s/reviews' % (users_url, r[0]),
                    'length': reviews_count
                },
                'pending_reviews': {
                    '$ref': '%s/%s/reviews?status=new' % (users_url, r[0]),
                    'length': pending_reviews_count
                },
                'tasks': {
                    '$ref': '%s/%s/tasks' % (users_url, r[0]),
                    'length': tasks_count
                },
                'tickets': {
                    '$ref': '%s/%s/tickets' % (users_url, r[0]),
                    'length': tickets_count
                },
                'open_tickets': {
                    '$ref': '%s/%s/tickets?status=open' % (users_url, r[0]),
                    'length': open_ticket_count
                },
                'vacations': {
                    '$ref': '%s/%s/vacations' % (users_url, r[0]),
                    'length': vacations_count
                },
            }
            response = super(UserViews, self).get_entity()
            return self.update_response_data(response, data)
        else:
            from pyramid.response import Response
            return Response(body='Not Found', status=404)

    @view_config(
        route_name='users',
        request_method='GET',
        permission='List_User'
    )
    def get_entities(self):
        """simply return the users without dealing a lot of other details
        """
        return super(UserViews, self).get_entities()

    @view_config(
        route_name='logged_in_user',
        request_method='GET'
    )
    def logged_in_user(self):
        """Returns the logged in user as JSON data
        """
        from pyramid.security import authenticated_userid
        login_name = authenticated_userid(self.request)
        from stalker import User
        from stalker.db.session import DBSession
        from sqlalchemy import or_
        user_id = DBSession.query(User.id) \
            .filter(or_(User.login == login_name, User.email == login_name)) \
            .first()

        if not user_id:
            from pyramid.exceptions import HTTPForbidden
            raise HTTPForbidden(self.request)
        else:
            self.entity_id = user_id
            return self.get_entity()

    @view_config(
        route_name='check_availability',
        request_method='GET',
    )
    def check_availability(self):
        """checks it the given login or email is available
        """
        login_name = self.request.params.get('login')
        email = self.request.params.get('email')

        login_available = True
        if login_name:
            logger.debug('checking login availability for: %s' % login_name)
            from stalker import User
            user = User.query.filter(User.login == login_name).first()
            if user:
                login_available = False

        email_available = True
        if email:
            logger.debug('checking email availability for: %s' % email)
            from stalker import User
            user = User.query.filter(User.email == email).first()
            if user:
                email_available = False

        return {
            'login_available': login_available,
            'email_available': email_available
        }

    @view_config(
        route_name='users',
        request_method='PUT',
    )
    def create_entity(self):
        """called when adding a User
        """
        availability_data = self.check_availability()
        login_available = availability_data['login_available']
        email_available = availability_data['email_available']
        if login_available and email_available:
            return super(UserViews, self).create_entity()
        else:
            body = ''
            if not login_available:
                login_name = self.request.params.get('login')
                body = 'Login not available: %s' % login_name
            elif not email_available:
                email = self.request.params.get('email')
                body = 'Email not available: %s' % email

            from pyramid.response import Response
            return Response(body, status=500)

    @view_config(
        route_name='user',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """update user view
        """
        # before updating the login and email, check availability
        availability_data = self.check_availability()
        login_name = self.request.params.get('login')
        if login_name:
            login_available = availability_data['login_available']
            if not login_available:
                from pyramid.response import Response
                return Response(
                    'Login not available: %s' % login_name,
                    status=500
                )

        email = self.request.params.get('email')
        if email:
            email_available = availability_data['email_available']
            if not email_available:
                from pyramid.response import Response
                return Response(
                    'Email not available: %s' % email,
                    status=500
                )

        # update super data
        try:
            return super(UserViews, self).update_entity()
        except Exception as e:
            import transaction
            transaction.abort()
            from pyramid.response import Response
            return Response(
                body=str(e),
                status=500
            )

    @view_config(
        route_name='user',
        request_method='DELETE',
        permission='Delete_User',
    )
    def delete_entity(self):
        """deletes the user with the given id
        """
        return super(UserViews, self).delete_entity()

    # User <-> Department
    @view_config(
        route_name='user_departments',
        request_method='GET',
    )
    def get_departments(self):
        """returns user departments
        """
        from stalker.models.department import Department, DepartmentUser
        join = DepartmentUser
        filters = [DepartmentUser.user_id == self.entity_id]
        filters.extend(self.filter_generator(Department))
        return self.collection_query(Department, join=join, filters=filters)

    @view_config(
        route_name='user_departments',
        request_method=['PATCH', 'POST'],
    )
    def update_departments(self):
        """updates the user departments
        """
        # get departments
        dep_ids = self.get_multi_integer(self.request, 'dep_id[]')

        from stalker.db.session import DBSession
        from stalker import Department
        with DBSession.no_autoflush:
            all_deps = Department.query\
                .filter(Department.id.in_(dep_ids)).all()

        if self.request.method == 'POST':
            with DBSession.no_autoflush:
                self.entity.departments = all_deps
        elif self.request.method == 'PATCH':
            with DBSession.no_autoflush:
                self.entity.departments += all_deps

        DBSession.add(self.entity)
        DBSession.flush()

    @view_config(
        route_name='user_departments',
        request_method='DELETE',
    )
    def remove_departments(self):
        """removes the given department(s) from  the User.departments attribute
        """
        dep_ids = self.get_multi_integer(
            self.request,
            'dep_id[]'
        )
        from stalker import Department
        all_deps = Department.query\
            .filter(Department.id.in_(dep_ids)).all()

        for dep in all_deps:
            try:
                self.entity.departments.remove(dep)
            except ValueError:
                pass

    # User <-> Group
    @view_config(
        route_name='user_groups',
        request_method='GET',
    )
    def get_groups(self):
        """returns user groups
        """
        from stalker.models.auth import Group, Group_Users
        join = Group_Users
        filters = [Group_Users.c.uid == self.entity_id]
        filters.extend(self.filter_generator(Group))
        return self.collection_query(Group, join=join, filters=filters)

    @view_config(
        route_name='user_groups',
        request_method=['PATCH', 'POST'],
    )
    def update_groups(self):
        """updates the user groups
        """
        # get groups
        group_ids = self.get_multi_integer(
            self.request,
            'group_id[]'
        )

        from stalker import Group
        all_groups = Group.query \
            .filter(Group.id.in_(group_ids)).all()

        if self.request.method == 'POST':
            self.entity.groups = all_groups
        elif self.request.method == 'PATCH':
            self.entity.groups += all_groups

        from stalker.db.session import DBSession
        DBSession.add(self.entity)
        DBSession.flush()

    @view_config(
        route_name='user_groups',
        request_method='DELETE',
    )
    def remove_groups(self):
        """removes the given group(s) from  the User.groups attribute
        """
        group_ids = self.get_multi_integer(
            self.request,
            'group_id[]'
        )
        from stalker import Group
        all_groups = Group.query \
            .filter(Group.id.in_(group_ids)).all()

        for group in all_groups:
            try:
                self.entity.groups.remove(group)
            except ValueError:
                # user not in group
                pass

    # User <-> Project
    @view_config(
        route_name='user_projects',
        request_method='GET',
    )
    def get_projects(self):
        """returns user projects
        """
        from stalker import Project, ProjectUser
        join = ProjectUser
        filters = [ProjectUser.user_id == self.entity_id]
        filters.extend(self.filter_generator(Project))
        return self.collection_query(Project, join=join, filters=filters)

    @view_config(
        route_name='user_projects',
        request_method=['PATCH', 'POST'],
    )
    def update_projects(self):
        """updates the user projects
        """
        # get projects
        project_ids = self.get_multi_integer(
            self.request,
            'project_id[]'
        )

        from stalker import Project
        all_projects = Project.query \
            .filter(Project.id.in_(project_ids)).all()

        if self.request.method == 'POST':
            self.entity.projects = all_projects
        elif self.request.method == 'PATCH':
            self.entity.projects += all_projects

        from stalker.db.session import DBSession
        DBSession.add(self.entity)
        DBSession.flush()

    @view_config(
        route_name='user_projects',
        request_method='DELETE',
    )
    def remove_projects(self):
        """removes the given project(s) from  the User.projects attribute
        """
        project_ids = self.get_multi_integer(
            self.request,
            'project_id[]'
        )
        from stalker import Project
        all_projects = Project.query \
            .filter(Project.id.in_(project_ids)).all()

        for project in all_projects:
            try:
                self.entity.projects.remove(project)
            except ValueError:
                pass

    # User <-> Vacation
    @view_config(
        route_name='user_vacations',
        request_method='GET',
    )
    def get_vacations(self):
        """returns user vacations
        """
        sql = """
        select
            "Vacations".id,
            "SimpleEntities".name,
              "SimpleEntities".entity_type
        from "Vacations"
        join "SimpleEntities" on "Vacations".id = "SimpleEntities".id
        where "Vacations".user_id = :id
        """

        from stalker.db.session import DBSession
        conn = DBSession.connection()
        from sqlalchemy import text
        result = conn.execute(text(sql), id=self.entity_id)

        from stalker_pyramid2 import entity_type_to_url
        data = [{
            'id': r[0],
            '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0]),
            'name': r[1],
            'entity_type': r[2]
        } for r in result.fetchall()]

        from pyramid.response import Response
        return Response(
            json_body=data,
            status=200
        )

    # User <-> Task
    @view_config(
        route_name='user_tasks',
        request_method='GET',
    )
    def get_tasks(self):
        """returns user tasks
        """
        from stalker.models.task import Task
        filters = [Task.resources.contains(self.entity)]
        filters.extend(self.filter_generator(Task))
        return self.collection_query(Task, filters=filters)

    @view_config(
        route_name='user_tasks_watched',
        request_method='GET',
    )
    def get_tasks_watched(self):
        """returns the watched tasks
        """
        from stalker.models.task import Task
        filters = [Task.watchers.contains(self.entity)]
        filters.extend(self.filter_generator(Task))
        return self.collection_query(Task, filters=filters)

    @view_config(
        route_name='user_tasks_responsible',
        request_method='GET',
    )
    def get_tasks_responsible(self):
        """returns the responsible tasks
        """
        from stalker.models.task import Task
        filters = [Task.responsible.contains(self.entity)]
        filters.extend(self.filter_generator(Task))
        return self.collection_query(Task, filters=filters)

    @view_config(
        route_name='user_tasks',
        request_method=['PATCH', 'POST'],
    )
    def update_tasks(self):
        """updates the user task relation
        """
        raise NotImplementedError

    @view_config(
        route_name='user_tasks',
        request_method='DELETE',
    )
    def remove_tasks(self):
        """removes the user from task
        """
        task_ids = self.get_multi_integer(self.request, 'task_id')

        as_param = self.request.params.get('as', None)

        from stalker import Task
        # get the tasks that the user is a resource only
        task_filter = Task.query\
            .filter(Task.id.in_(task_ids))

        if as_param is None or as_param == 'resource':
            tasks = task_filter\
                .filter(Task.resources.contains(self.entity))\
                .all()
            for task in tasks:
                task.resources.remove(self.entity)
        elif as_param == 'responsible':
            tasks = task_filter\
                .filter(Task.responsible.contains(self.entity))\
                .all()
            for task in tasks:
                task.responsible.remove(self.entity)
        elif as_param == 'watcher':
            tasks = task_filter\
                .filter(Task.watchers.contains(self.entity))\
                .all()
            for task in tasks:
                task.watchers.remove(self.entity)

        from stalker.db.session import DBSession
        DBSession.flush()

    # User <-> Review
    @view_config(
        route_name='user_reviews',
        request_method='GET',
    )
    def get_reviews(self):
        """returns user reviews
        """
        status = self.request.params.get('status')

        from stalker import Review
        join = None
        filters = [Review.reviewer_id == self.entity_id]
        filters.extend(self.filter_generator(Review))

        logger.debug('filter_: %s' % filters)

        # special case
        if status:
            from stalker import Status
            join = Status, Review.status_id == Status.id
            filters.append(Status.code == status.upper())

        return self.collection_query(Review, join=join, filters=filters)

    # User <-> Ticket
    @view_config(
        route_name='user_tickets',
        request_method='GET',
    )
    def get_tickets(self):
        """returns user tickets
        """
        from stalker import Ticket
        filters = [Ticket.owner_id == self.entity_id]
        filters.extend(self.filter_generator(Ticket))
        return self.collection_query(Ticket, filters=filters)

    @view_config(
        route_name='user_time_logs',
        request_method='GET',
    )
    def get_time_logs(self):
        """returns time logs of the user
        """
        sql = """
        select
          "TimeLogs".id,
          "SimpleEntities".name,
          "SimpleEntities".entity_type
        from "TimeLogs"
        join "SimpleEntities" on "TimeLogs".id = "SimpleEntities".id
        where "TimeLogs".resource_id = :id
        """
        from sqlalchemy import text
        from stalker.db.session import DBSession
        conn = DBSession.connection()
        result = conn.execute(text(sql), id=self.entity_id).fetchall()

        from stalker_pyramid2 import entity_type_to_url
        data = [
            {
                'id': r[0],
                'name': r[1],
                'entity_type': r[2],
                '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0])
            } for r in result
        ]

        from pyramid.response import Response
        return Response(
            json_body=data,
            status=200
        )
