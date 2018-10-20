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
from stalker import Task
from pyramid.view import view_defaults, view_config
from stalker_pyramid2.views import simple_entity_interpreter
from stalker_pyramid2.views.entity import EntityViews
from stalker_pyramid2.views.mixins import \
    StatusMixinViews, DateRangeMixinViews, ReferenceMixinViews, \
    ScheduleMixinViews, DAGMixinViews

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TaskViews(EntityViews, StatusMixinViews, DateRangeMixinViews,
                ReferenceMixinViews, ScheduleMixinViews, DAGMixinViews):
    """views related to the Task SOM class
    """
    som_class = Task
    local_params = [
        # simple arguments
        {
            'name': 'bid_timing',
            'interpreter': float,
        },
        {
            'name': 'bid_unit'
        },
        {
            'param_name': 'is_milestone',
            'interpreter': bool,
        },
        {
            'param_name': 'priority',
            'interpreter': int,
        },
        {
            'param_name': 'allocation_strategy',
            'interpreter': int,
        },
        {
            'param_name': 'persistent_allocation',
            'interpreter': bool,
        },

        # complex args
        {
            'param_name': 'project_id',
            'arg_name': 'project',
            'interpreter': simple_entity_interpreter,
            'nullable': False,
        },
        {
            'param_name': 'parent_id',
            'arg_name': 'parent',
            'interpreter': simple_entity_interpreter,
        },
        {
            'param_name': 'depends_id',
            'arg_name': 'depends',
            'interpreter': simple_entity_interpreter,
            'is_list': True,
        },
        {
            'param_name': 'resource_id',
            'arg_name': 'resources',
            'interpreter': simple_entity_interpreter,
            'is_list': True,
        },
        {
            'param_name': 'responsible_id',
            'arg_name': 'responsible',
            'interpreter': simple_entity_interpreter,
            'is_list': True
        },
        {
            'param_name': 'alternative_resource_id',
            'arg_name': 'alternative_resources',
            'interpreter': simple_entity_interpreter,
            'is_list': True
        },
        {
            'param_name': 'watcher_id',
            'arg_name': 'watchers',
            'interpreter': simple_entity_interpreter,
            'is_list': True
        },
        {
            'param_name': 'good_id',
            'arg_name': 'good',
            'interpreter': simple_entity_interpreter,
        }
    ]

    def get_entity(self):
        """returns one Task instance data
        """

        response = super(TaskViews, self).get_entity()
        # add the others
        
        # StatusMixinViews, DateRangeMixinViews,
        # ReferenceMixinViews, ScheduleMixinViews, DAGMixinViews
        response = self.update_response_data(
            response, StatusMixinViews.get_entity(self)
        )
        response = self.update_response_data(
            response, DateRangeMixinViews.get_entity(self)
        )
        response = self.update_response_data(
            response, ReferenceMixinViews.get_entity(self)
        )
        response = self.update_response_data(
            response, ScheduleMixinViews.get_entity(self)
        )
        response = self.update_response_data(
            response, DAGMixinViews.get_entity(self)
        )

        from stalker import Task
        from stalker.db.session import DBSession

        r = DBSession.query(
            Task.allocation_strategy, Task.bid_timing, Task.bid_unit,
            Task.is_milestone, Task.persistent_allocation, Task.priority,
            Task.schedule_constraint, Task.schedule_model,
            Task.schedule_timing, Task.schedule_unit,
        ).filter(Task.id == self.entity_id).first()

        data = {
            'allocation_strategy': r[0],
            'bid_timing': r[1],
            'bid_unit': r[2],
            'is_milestone': r[3],
            'persistent_allocation': r[4],
            'priority': r[5],
            'schedule_constraint': r[6],
            'schedule_model': r[7],
            'schedule_timing': r[8],
            'schedule_unit': r[9]
        }

        return self.update_response_data(
            response, data
        )
