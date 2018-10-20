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

from stalker import Project
from pyramid.view import view_config, view_defaults
from stalker_pyramid2.views import simple_entity_interpreter
from stalker_pyramid2.views.entity import EntityViews
from stalker_pyramid2.views.mixins import (StatusMixinViews,
                                           ReferenceMixinViews,
                                           DateRangeMixinViews, CodeMixinViews)

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_defaults(renderer='json')
class ProjectViews(EntityViews, ReferenceMixinViews, StatusMixinViews,
                   DateRangeMixinViews, CodeMixinViews):
    """views for Project class
    """

    som_class = Project
    local_params = [
        # simple arguments/attributes
        {'param_name': 'name', 'nullable': False},
        {'param_name': 'fps', 'interpreter': float},

        # complex arguments/attributes
        {
            'param_name': 'image_format_id',
            'arg_name': 'image_format',
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'repository_id',
            'arg_name': 'repositories',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'client_id',
            'arg_name': 'clients',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'structure_id',
            'arg_name': 'structure',
            'interpreter': simple_entity_interpreter
        },
        {
            'param_name': 'user_id',
            'arg_name': 'users',
            'is_list': True,
            'interpreter': simple_entity_interpreter
        }
    ]

    @view_config(
        route_name='project',
        request_method='GET'
    )
    def get_entity(self):
        """returns one Project instance info
        """
        from sqlalchemy import text
        from stalker.db.session import DBSession
        from stalker_pyramid2 import entity_type_to_url
        conn = DBSession.connection()

        # get image format data
        sql = """select
          "SimpleEntities".id,
          "SimpleEntities".name,
          "SimpleEntities".entity_type
        from "Projects"
        join "SimpleEntities" on "Projects".image_format_id = "SimpleEntities".id
        where "Projects".id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        image_format_data = {
            'id': r[0],
            'name': r[1],
            'entity_type': r[2],
            '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0])
        } if r else None

        # get structure data
        sql = """select
          "SimpleEntities".id,
          "SimpleEntities".name,
          "SimpleEntities".entity_type
        from "Projects"
        join "SimpleEntities" on "Projects".structure_id = "SimpleEntities".id
        where "Projects".id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        structure_data = {
            'id': r[0],
            'name': r[1],
            'entity_type': r[2],
            '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0])
        } if r else None

        # get clients count
        sql = """select
          count(1)
        from "Project_Clients"
        where "Project_Clients".project_id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        client_count = r[0] if r else 0

        # get users count
        sql = """select
          count(1)
        from "Project_Users"
        where "Project_Users".project_id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        user_count = r[0] if r else 0

        # get repositories count
        sql = """select
          count(1)
        from "Project_Repositories"
        where "Project_Repositories".project_id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        repository_count = r[0] if r else 0

        # get references count
        sql = """select
            count(1)
        from (
          select
            pr.link_id
          from "Project_References" as pr
          where pr.project_id = :id
        union
          select
            tr.link_id
          from "Task_References" as tr
          join "Tasks" as t on tr.task_id = t.id
          where t.project_id = :id
        ) as refs
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        reference_count = r[0] if r else 0

        # get dailies count
        sql = """select
            count(1)
        from "Dailies"
        where "Dailies".project_id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        daily_count = r[0] if r else 0

        # get tickets count
        sql = """select
          count(1)
        from "Tickets"
        where "Tickets".project_id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        ticket_count = r[0] if r else 0

        # get task count
        sql = """select
          count(1)
        from "Tasks"
        where "Tasks".project_id = :id
        """
        r = conn.execute(text(sql), id=self.entity_id).fetchone()
        task_count = r[0] if r else 0

        data = {
            'clients': {
                '$ref': '%s/%s/clients' % (
                    entity_type_to_url[self.entity.entity_type], self.entity_id
                ),
                'length': client_count
            },
            'dailies': {
                '$ref': '%s/%s/dailies' % (
                    entity_type_to_url[self.entity.entity_type], self.entity_id
                ),
                'length': daily_count
            },
            'fps': self.entity.fps,
            'image_format': image_format_data,
            'references': {
                '$ref': '%s/%s/references' % (
                    entity_type_to_url[self.entity.entity_type], self.entity_id
                ),
                'length': reference_count
            },
            'repositories': {
                '$ref': '%s/%s/repositories' % (
                    entity_type_to_url[self.entity.entity_type], self.entity_id
                ),
                'length': repository_count
            },
            'structure': structure_data,
            'tasks': {
                '$ref': '%s/%s/tasks' % (
                    entity_type_to_url[self.entity.entity_type], self.entity_id
                ),
                'length': task_count
            },
            'tickets': {
                '$ref': '%s/%s/tickets' % (
                    entity_type_to_url[self.entity.entity_type], self.entity_id
                ),
                'length': ticket_count
            },
            'users': {
                '$ref': '%s/%s/users' % (
                    entity_type_to_url[self.entity.entity_type], self.entity_id
                ),
                'length': user_count
            },
        }

        # we can't use ReferenceMixin.get_entity() because we're also joining
        # Task.references here

        data.update(StatusMixinViews.get_entity(self))
        data.update(DateRangeMixinViews.get_entity(self))
        data.update(CodeMixinViews.get_entity(self))
        entity_response = EntityViews.get_entity(self)
        return self.update_response_data(entity_response, data)

    @view_config(
        route_name='projects',
        request_method='GET'
    )
    def get_entities(self):
        """returns all projects
        """
        return super(ProjectViews, self).get_entities()

    @view_config(
        route_name='project',
        request_method=['PATCH', 'POST'],
    )
    def update_entity(self):
        """updates the current project instance
        """
        return super(ProjectViews, self).update_entity()

    @view_config(
        route_name='projects',
        request_method='PUT'
    )
    def create_entity(self):
        """creates a project instance
        """
        return super(ProjectViews, self).create_entity()

    @view_config(
        route_name='project',
        request_method='DELETE'
    )
    def delete_entity(self):
        """deletes the current project instance
        """
        return super(ProjectViews, self).delete_entity()

    @view_config(
        route_name='project_budgets',
        request_method='GET'
    )
    def get_budgets(self):
        """returns the budgets of this projects
        """
        from stalker import Budget
        filters = [Budget.project_id == self.entity_id]
        filters.extend(self.filter_generator(Budget))
        return self.collection_query(Budget, filters=filters)

    @view_config(
        route_name='project_clients',
        request_method='GET'
    )
    def get_clients(self):
        """returns clients of this project
        """
        from stalker import Client, ProjectClient
        join = Client, ProjectClient.client
        filters = [ProjectClient.project_id == self.entity_id]
        filters.extend(self.filter_generator(Client))
        return self.collection_query(Client, join=join, filters=filters)

    @view_config(
        route_name='project_clients',
        request_method=['PATCH', 'POST']
    )
    def update_clients(self):
        """updates the clients list of this project instance
        """
        client_ids = self.get_multi_integer(self.request, 'client_id')

        from stalker import Client
        clients = Client.query.filter(Client.id.in_(client_ids)).all()

        if self.request.method == 'PATCH':
            self.entity.clients.extend(clients)
        elif self.request.method == 'POST':
            self.entity.clients = clients

    @view_config(
        route_name='project_clients',
        request_method='DELETE'
    )
    def delete_clients(self):
        """removes the given client instances from the project.clients list
        """
        client_ids = self.get_multi_integer(self.request, 'client_id')

        from stalker import Client
        clients = Client.query.filter(Client.id.in_(client_ids)).all()

        for client in clients:
            try:
                self.entity.clients.remove(client)
            except ValueError:
                pass

    @view_config(
        route_name='project_repositories',
        request_method='GET'
    )
    def get_repositories(self):
        """returns the repositories of this project
        """
        # the order of the repositories is important so get them in that order
        from stalker import Repository, ProjectRepository
        join = Repository, ProjectRepository.repository
        filters = [ProjectRepository.project_id == self.entity_id]
        filters.extend(self.filter_generator(Repository))
        order_by = ProjectRepository.position
        return self.collection_query(Repository, join=join, filters=filters,
                                     order_by=order_by)

    @view_config(
        route_name='project_repositories',
        request_method=['PATCH', 'POST']
    )
    def update_repositories(self):
        """updates the repositories of the current project
        """
        repo_ids = self.get_multi_integer(self.request, 'repo_id')
        from stalker import Repository
        repositories = \
            Repository.query.filter(Repository.id.in_(repo_ids)).all()

        if self.request.method == 'PATCH':
            for r in repositories:
                if r not in self.entity.repositories:
                    self.entity.repositories.append(r)
        elif self.request.method == 'POST':
            self.entity.repositories = repositories

    @view_config(
        route_name='project_repositories',
        request_method='DELETE'
    )
    def delete_repositories(self):
        """removes the given repositories from the current project
        """
        repo_ids = self.get_multi_integer(self.request, 'repo_id')
        from stalker import Repository
        repositories = \
            Repository.query.filter(Repository.id.in_(repo_ids)).all()

        for repo in repositories:
            try:
                self.entity.repositories.remove(repo)
            except ValueError:
                pass

    @view_config(
        route_name='project_tasks',
        request_method='GET'
    )
    def get_tasks(self):
        """returns the tasks of this project in no particular order
        """
        from stalker import Task
        filters = [Task.project_id == self.entity_id]
        filters.extend(self.filter_generator(Task))
        return self.collection_query(
            Task,
            filters=filters
        )

    @view_config(
        route_name='project_tickets',
        request_method='GET'
    )
    def get_tickets(self):
        """returns tickets
        """
        from stalker import Ticket
        filters = [Ticket.project_id == self.entity_id]
        filters.extend(self.filter_generator(Ticket))
        return self.collection_query(
            Ticket,
            filters=filters
        )

    @view_config(
        route_name='project_users',
        request_method='GET'
    )
    def get_users(self):
        """returns users assigned to this project
        """
        from stalker import ProjectUser, User
        join = User, ProjectUser.user
        filters = [ProjectUser.project_id == self.entity_id]
        filters.extend(self.filter_generator(User))
        return self.collection_query(User, filters=filters, join=join)

    @view_config(
        route_name='project_users',
        request_method=['PATCH', 'POST']
    )
    def update_users(self):
        """updates the users of this project
        """
        user_ids = self.get_multi_integer(self.request, 'user_id')
        from stalker import User
        users = User.query.filter(User.id.in_(user_ids)).all()

        from stalker.db.session import DBSession
        if self.request.method == 'PATCH':
            with DBSession.no_autoflush:
                self.entity.users.extend(users)
        elif self.request.method == 'POST':
            with DBSession.no_autoflush:
                self.entity.users = users

    @view_config(
        route_name='project_users',
        request_method='DELETE'
    )
    def delete_users(self):
        """removes the given users from this project
        """
        user_ids = self.get_multi_integer(self.request, 'user_id')
        from stalker import User
        users = User.query.filter(User.id.in_(user_ids)).all()

        for user in users:
            try:
                self.entity.users.remove(user)
            except ValueError:
                pass

    @view_config(
        route_name='project_dailies',
        request_method='GET'
    )
    def get_dailies(self):
        """returns the dailies of this project
        """
        from stalker import Daily
        filters = [Daily.project_id == self.entity_id]
        filters.extend(self.filter_generator(Daily))
        return self.collection_query(Daily,
                                     filters=filters)

    @view_config(
        route_name='project_references',
        request_method='GET'
    )
    def get_references(self):
        """returns the references of this project
        """
        sql = """select
              rse.id,
              rse.name,
              rse.entity_type
            from "Project_References" as pr
            join "SimpleEntities" as rse on pr.link_id = rse.id
            where pr.project_id = :id
        union
            select
              rse.id,
              rse.name,
              rse.entity_type
            from "Task_References" as tr
            join "Tasks" as t on tr.task_id = t.id
            join "SimpleEntities" as rse on tr.link_id = rse.id
            where t.project_id = :id
        """

        from stalker.db.session import DBSession
        from sqlalchemy import text

        conn = DBSession.connection()
        result = conn.execute(text(sql), id=self.entity_id).fetchall()

        from stalker_pyramid2 import entity_type_to_url
        project_ref_data = [
            {
                'id': r[0],
                'name': r[1],
                'entity_type': r[2],
                '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0])
            } for r in result
        ]

        from pyramid.response import Response
        return Response(json_body=project_ref_data, status=200)
