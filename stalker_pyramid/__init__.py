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

__version__ = '0.2.0'

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


stalker_server_external_url = None
stalker_server_internal_url = None


entity_type_to_url = {
    'Asset': '/api/assets',
    'Budget': '/api/budgets',
    'BudgetEntry': '/api/budget_entries',
    'Client': '/api/clients',
    'Daily': '/api/dailies',
    'DailyLink': '/api/daily_links',
    'Department': '/api/departments',
    'Entity': '/api/entities',
    'EntityGroup': '/api/entity_groups',
    'FilenameTemplate': '/api/filename_templates',
    'Good': '/api/goods',
    'Group': '/api/groups',
    'ImageFormat': '/api/image_formats',
    'Link': '/api/links',
    'Message': '/api/messages',
    'Note': '/api/notes',
    'Page': '/api/pages',
    'Permission': '/api/permissions',
    'PriceList': '/api/price_lists',
    'Project': '/api/projects',
    'Repository': '/api/repositories',
    'Review': '/api/reviews',
    'Role': '/api/roles',
    'Scene': '/api/scenes',
    'Sequence': '/api/sequences',
    'Shot': '/api/shots',
    'SimpleEntity': '/api/simple_entities',
    'Status': '/api/statuses',
    'StatusList': '/api/status_lists',
    'Structure': '/api/structures',
    'Studio': '/api/studios',
    'Tag': '/api/tags',
    'Task': '/api/tasks',
    'Ticket': '/api/tickets',
    'TicketLog': '/api/ticket_logs',
    'TimeLog': '/api/time_logs',
    'Type': '/api/types',
    'User': '/api/users',
    'Vacation': '/api/vacations',
    'Version': '/api/versions',
}


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # use the ZopeTransactionExtension for session
    from zope.sqlalchemy import ZopeTransactionExtension
    from stalker.db.session import DBSession
    DBSession.remove()
    DBSession.configure(extension=ZopeTransactionExtension())

    # setup the database to the given settings
    from stalker import db
    db.setup(settings)

    import os
    for key in os.environ:
        logger.debug('%s: %s' % (key, os.environ[key]))

    # setup internal and external urls
    global stalker_server_external_url
    global stalker_server_internal_url
    stalker_server_external_url = settings.get('stalker.external_url')
    stalker_server_internal_url = settings.get('stalker.internal_url')

    # setup authorization and authentication
    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy
    from stalker_pyramid.views.auth import group_finder
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret',
        hashalg='sha512',
        callback=group_finder
    )
    authz_policy = ACLAuthorizationPolicy()

    from pyramid.config import Configurator
    config = Configurator(
        settings=settings,
        root_factory='stalker_pyramid.views.auth.RootFactory'
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # Configure Beaker sessions and caching
    import pyramid_beaker
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    pyramid_beaker.set_cache_regions_from_settings(settings)

    # config.include('pyramid_jinja2')
    # config.include('pyramid_mailer')
    config.add_jinja2_renderer('.html')
    config.add_jinja2_search_path('templates', name='.html')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('angular', 'angular', cache_max_age=3600)
    config.add_static_view('templates', 'templates', cache_max_age=3600)

    # *************************************************************************
    # Basics
    config.add_route('home', '/')
    config.add_route('me_menu', 'me_menu')
    config.add_route('signin', 'signin')
    config.add_route('login', '/api/login')
    config.add_route('logout', '/api/logout')
    config.add_route('logged_in_user', '/api/logged_in_user')

    config.add_route('flash_message', '/flash_message')

    # addresses like http:/localhost:6543/SPL/{some_path} will let SP to serve
    # those files
    # SPL   : Stalker Pyramid Local
    config.add_route(
        'serve_files',
        'SPL/{partial_file_path:[a-zA-Z0-9/\.]+}'
    )

    # addresses like http:/localhost:6543/FDSPL/{some_path} will serve the
    # files with their original filename in a forced download mode.
    # FDSPL : Forced Download Stalker Pyramid Local
    config.add_route(
        'forced_download_files',
        'FDSPL/{partial_file_path:[a-zA-Z0-9/\.]+}'
    )

    # before anything about stalker create the defaults
    from stalker import defaults
    logger.debug(
        os.path.normpath(
            defaults.server_side_storage_path + '/{partial_file_path}'
        ).replace('\\', '/')
    )

    # *************************************************************************
    # DATA VIEWS
    # *************************************************************************

    # *************************************************************************
    # SimpleEntities
    config.add_route('simple_entity',   '/api/simple_entities/{id}')
    config.add_route('simple_entities', '/api/simple_entities')
    config.add_route('simple_entity_generic_data', '/api/simple_entities/{id}/generic_data')

    # *************************************************************************
    # Entities
    config.add_route('entity',       '/api/entities/{id}')
    config.add_route('entities',     '/api/entities')
    config.add_route('entity_notes', '/api/entities/{id}/notes')
    config.add_route('entity_tags',  '/api/entities/{id}/tags')

    # OLD VIEWS
    config.add_route('get_search_result', '/search')  # json
    config.add_route('submit_search', '/submit_search')

    # TODO: Do we still really need "get_entity_tasks_by_filter"
    config.add_route('get_entity_tasks_by_filter',     'api/entities/{id}/tasks/filter/{f_id}/')

    config.add_route('get_entity_tickets',             'api/entities/{id}/tickets/')
    config.add_route('get_entity_tickets_count',       'api/entities/{id}/tickets/count/')
    config.add_route('get_entity_time_logs',           'api/entities/{id}/time_logs/')
    config.add_route('get_entity_projects',            'api/entities/{id}/projects/')
    config.add_route('get_entity_sequences',           'api/entities/{id}/sequences/')
    config.add_route('get_entity_sequences_count',     'api/entities/{id}/sequences/count/')
    config.add_route('get_entity_assets',              'api/entities/{id}/assets/')
    config.add_route('get_entity_assets_count',        'api/entities/{id}/assets/count/')
    config.add_route('get_entity_shots',               'api/entities/{id}/shots/')
    config.add_route('get_entity_shots_simple',        'api/entities/{id}/shots/simple/')
    config.add_route('get_entity_shots_count',         'api/entities/{id}/shots/count/')
    config.add_route('get_entity_scenes',              'api/entities/{id}/scenes/')
    config.add_route('get_entity_scenes_simple',       'api/entities/{id}/scenes/simple/')
    config.add_route('get_entity_scenes_count',        'api/entities/{id}/scenes/count/')
    config.add_route('get_entity_vacations',           'api/entities/{id}/vacations/')
    config.add_route('get_entity_vacations_count',     'api/entities/{id}/vacations/count/')
    config.add_route('get_entity_entities_out_stack',  'api/entities/{id}/{entities}/out_stack/' )
    config.add_route('get_entity_events',              'api/entities/{id}/events/')  #json
    config.add_route('get_entity_notes',               'api/entities/{id}/notes/') #json
    config.add_route('get_entity_task_min_start',      'api/entities/{id}/task_min_start/') #json
    config.add_route('get_entity_task_max_end',        'api/entities/{id}/task_max_end/') #json
    config.add_route('get_entity_users_roles',         'api/entities/{id}/users/roles/')#json

    config.add_route('append_entities_to_entity',      'api/entities/{id}/append')

    # *************************************************************************
    # Notes
    config.add_route('note', '/api/notes/{id}')
    config.add_route('notes', '/api/notes')

    # *************************************************************************
    # Thumbnail  and Links
    config.add_route('link',  '/api/links/{id}')
    config.add_route('links', '/api/links')

    # config.add_route('upload_files',         'api/upload_files')
    # config.add_route('assign_thumbnail',     'api/assign_thumbnail')

    # *************************************************************************
    # References

    config.add_route('get_task_references',        'api/tasks/{id}/references/')  # json
    config.add_route('get_task_references_count',  'api/tasks/{id}/references/count/')  # json
    config.add_route('get_asset_references',       'api/assets/id}/references/')  # json
    config.add_route('get_asset_references_count', 'api/assets/id}/references/count/')  # json

    config.add_route('get_shot_references',        'api/shots/{id}/references/')  # json
    config.add_route('get_shot_references_count',  'api/shots/{id}/references/count/')  # json

    config.add_route('get_references',       'api/references/')
    config.add_route('get_reference',        'api/references/{id}')

    config.add_route('assign_reference',     'api/assign_reference')
    config.add_route('delete_reference',     'api/references/{id}/delete')

    config.add_route('update_reference',        'api/references/{id}/update')

    # *************************************************************************
    # Outputs
    config.add_route('get_entity_outputs',          'api/entities/{id}/outputs/')
    config.add_route('get_entity_outputs_count',    'api/entities/{id}/outputs/count/')

    config.add_route('get_task_outputs',            'api/tasks/{id}/outputs/')
    config.add_route('get_task_outputs_count',      'api/tasks/{id}/outputs/count/')

    config.add_route('get_version_outputs',         'api/versions/{id}/outputs/')
    config.add_route('get_version_outputs_count',   'api/versions/{id}/outputs/count/')

    config.add_route('assign_output',               'api/assign_output')
    config.add_route('delete_output',               'api/outputs/{id}/delete')

    # *************************************************************************
    # Studio
    config.add_route('create_studio',         'api/studios/create')
    config.add_route('update_studio',         'api/studios/{id}/update')

    config.add_route('get_studio_tasks',      'api/studios/{id}/tasks/')
    config.add_route('get_studio_vacations',  'api/studios/{id}/vacations/')  # json
    config.add_route('get_studio_vacations_count',  'api/studios/{id}/vacations/count/')  # json

    config.add_route('schedule_info',               'api/schedule_info')  # json
    config.add_route('studio_scheduling_mode',      'api/studio_scheduling_mode')
    config.add_route('auto_schedule_tasks',         'api/auto_schedule_tasks')

    # *************************************************************************
    # Project
    config.add_route('projects',             '/api/projects')
    config.add_route('project',              '/api/projects/{id}')
    config.add_route('project_budgets',      '/api/projects/{id}/budgets')
    config.add_route('project_clients',      '/api/projects/{id}/clients')
    config.add_route('project_dailies',      '/api/projects/{id}/dailies')
    config.add_route('project_references',   '/api/projects/{id}/references')
    config.add_route('project_repositories', '/api/projects/{id}/repositories')
    config.add_route('project_tasks',        '/api/projects/{id}/tasks')
    config.add_route('project_tickets',      '/api/projects/{id}/tickets')
    config.add_route('project_users',        '/api/projects/{id}/users')

    # config.add_route('project_assets',       '/api/projects/{id}/tasks?entity_type=Asset')
    # config.add_route('project_shots',        '/api/projects/{id}/tasks?entity_type=Shot')
    # config.add_route('project_sequences',    '/api/projects/{id}/tasks?entity_type=Sequence')
    # config.add_route('project_scenes',       '/api/projects/{id}/tasks?entity_type=Scene')

    # config.add_route('project_reviews',         'api/projects/{id}/reviews/') #json
    # config.add_route('project_tasks_cost',      'api/projects/{id}/tasks/cost/') #json
    # config.add_route('add_project_entries_to_budget',   'api/projects/{id}/entries/budgets/{bid}/add')
    # config.add_route('get_project_tasks_today',    'api/projects/{id}/tasks/{action}/today/')  # json
    # config.add_route('get_project_tasks_in_date',  'api/projects/{id}/tasks/{action}/{date}/')  # json

    # *************************************************************************
    # Clients
    config.add_route('append_user_to_client',        'api/clients/{id}/user/append')

    config.add_route('create_client',                'api/clients/create')
    config.add_route('update_client',                'api/clients/{id}/update')

    config.add_route('get_studio_clients',           'api/studios/{id}/clients/')
    config.add_route('get_clients',                  'api/clients/')
    config.add_route('get_client_users_out_stack',   'api/clients/{id}/users/out_stack/' )
    config.add_route('get_client_users',             'api/clients/{id}/users/' )

    # *************************************************************************
    # Budgets
    config.add_route('create_budget',        'api/budgets/create')
    config.add_route('update_budget',        'api/budgets/{id}/update')

    config.add_route('save_budget_calendar', 'api/budgets/{id}/save/calendar')

    config.add_route('duplicate_budget',   'api/budgets/{id}/duplicate')
    config.add_route('change_budget_type',   'api/budgets/{id}/type/{type_name}')
    config.add_route('get_budget_entries',   'api/budgets/{id}/entries/')

    # *************************************************************************
    # BudgetEntries
    config.add_route('create_budgetentry', 'api/budgetentries/create')
    config.add_route('edit_budgetentry',   'api/budgetentries/edit')
    config.add_route('update_budgetentry', 'api/budgetentries/update')
    config.add_route('delete_budgetentry', 'api/budgetentries/delete')

    # *************************************************************************
    # Dailies
    config.add_route('create_daily',        'api/dailies/create')
    config.add_route('update_daily',        'api/dailies/{id}/update')
    config.add_route('inline_update_daily', 'api/dailies/{id}/update/inline')

    config.add_route('get_daily_outputs',   'api/dailies/{id}/outputs/') # json

    config.add_route('append_link_to_daily', 'api/links/{id}/dailies/{did}/append')
    config.add_route('remove_link_to_daily', 'api/links/{id}/dailies/{did}/remove')
    config.add_route('convert_to_webm',      'api/links/{id}/convert_to_webm')

    # *************************************************************************
    # ImageFormat
    config.add_route('image_format',  '/api/image_formats/{id}')
    config.add_route('image_formats', '/api/image_formats')

    # *************************************************************************
    # Repository
    config.add_route('repository',   '/api/repositories/{id}')
    config.add_route('repositories', '/api/repositories')

    # serve files in repository
    config.add_route('serve_repository_files',
                     '$REPO{id}/{partial_file_path:[a-zA-Z0-9/\._\-\+\(\)]*}')

    config.add_route(
        'forced_download_repository_files',
        'FD{file_path:[a-zA-Z0-9/\._\-\+\(\)/$]*}'
    )

    config.add_route('video_player', 'video_player')  # html

    # *************************************************************************
    # Structure
    config.add_route('structure',  '/api/structures/{id}')
    config.add_route('structures', '/api/structures')
    config.add_route('structure_templates', '/api/structures/{id}/templates')

    # *************************************************************************
    # User
    config.add_route('users',                  '/api/users')
    config.add_route('user',                   '/api/users/{id}')
    config.add_route('user_departments',       '/api/users/{id}/departments')
    config.add_route('user_groups',            '/api/users/{id}/groups')
    config.add_route('user_projects',          '/api/users/{id}/projects')
    config.add_route('user_vacations',         '/api/users/{id}/vacations')
    config.add_route('user_tasks',             '/api/users/{id}/tasks')
    config.add_route('user_tasks_watched',     '/api/users/{id}/tasks_watched')
    config.add_route('user_tasks_responsible',
                     '/api/users/{id}/tasks_responsible')
    config.add_route('user_reviews',           '/api/users/{id}/reviews')
    config.add_route('user_tickets',           '/api/users/{id}/tickets')
    config.add_route('user_time_logs',         '/api/users/{id}/time_logs')

    # other views
    config.add_route('check_availability', '/api/check_availability')

    # *************************************************************************
    # FilenameTemplate
    config.add_route('filename_template',  '/api/filename_templates/{id}')
    config.add_route('filename_templates', '/api/filename_templates')

    # *************************************************************************
    # Status
    config.add_route('status',       '/api/statuses/{id}')
    config.add_route('statuses',     '/api/statuses')

    # *************************************************************************
    # StatusList
    # base views
    config.add_route('status_list',          '/api/status_lists/{id}')
    config.add_route('status_lists',         '/api/status_lists')

    # collection views
    config.add_route('status_list_statuses', '/api/status_lists/{id}/statuses')

    # *************************************************************************
    # Assets
    config.add_route('create_asset',        'api/assets/create')
    config.add_route('update_asset',        'api/assets/{id}/update')

    config.add_route('get_asset_tickets',   'api/assets/{id}/tickets/')

    config.add_route('get_assets_types', 'api/assets/types/')  # json
    config.add_route('get_assets_type_task_types', 'api/assets/types/{t_id}/task_types/')  # json
    config.add_route('get_assets_children_task_type',  'api/assets/children/task_type/')  # json

    # *************************************************************************
    # Shots
    config.add_route('create_shot',        'api/shots/create')
    config.add_route('update_shot',        'api/shots/{id}/update')

    config.add_route('get_shots_children_task_type',  'api/shots/children/task_type/')  # json

    # *************************************************************************
    # Scene
    config.add_route('get_scenes_children_task_type',  'api/scenes/children/task_type/')  # json
    config.add_route('create_scene',  'api/scenes/create')  # html

    # *************************************************************************
    # Sequence
    config.add_route('create_sequence',        'api/sequences/create')
    config.add_route('update_sequence',        'api/sequences/{id}/update')

    config.add_route('get_sequence_references', 'api/sequences/{id}/references/')  # json
    config.add_route('get_sequence_references_count', 'api/sequences/{id}/references/count/')  # json
    config.add_route('get_sequence_tickets',    'api/sequences/{id}/tickets/')  # json
    config.add_route('get_sequence_tasks',      'api/sequences/{id}/tasks/')  # json
    config.add_route('get_sequences',           'api/sequences/')  # json

    # *************************************************************************
    # Task
    config.add_route('get_task_external_link',  'api/tasks/{id}/external_link')
    config.add_route('get_task_internal_link',  'api/tasks/{id}/internal_link')

    # Actions
    config.add_route('create_task',                         'api/tasks/create')
    config.add_route('update_task',                         'api/tasks/{id}/update')
    config.add_route('inline_update_task',                  'api/tasks/{id}/update/inline')
    config.add_route('update_task_schedule_timing',         'api/tasks/{id}/update/schedule_timing')
    config.add_route('update_task_dependencies',            'api/tasks/{id}/update/dependencies')
    config.add_route('force_task_status',                   'api/tasks/{id}/force_status/{status_code}')
    config.add_route('force_tasks_status',                  'api/tasks/force_status/{status_code}')
    config.add_route('resume_task',                         'api/tasks/{id}/resume')
    config.add_route('review_task',                         'api/tasks/{id}/review')
    config.add_route('cleanup_task_new_reviews',            'api/tasks/{id}/cleanup_new_reviews')

    config.add_route('duplicate_task_hierarchy',            'api/tasks/{id}/duplicate')

    config.add_route('get_gantt_tasks',          'api/tasks/{id}/gantt')
    config.add_route('get_gantt_task_children',  'api/tasks/{id}/children/gantt')

    config.add_route('get_tasks',                'api/tasks/')
    config.add_route('get_tasks_count',          'api/tasks/count/')

    config.add_route('get_task',                        'api/tasks/{id}/')
    config.add_route('get_task_events',                 'api/tasks/{id}/events/')  #json
    config.add_route('get_task_children_task_types',    'api/tasks/{id}/children_task_types/')  # json
    config.add_route('get_task_children_tasks',         'api/tasks/{id}/children_tasks/')  # json
    config.add_route('get_task_leafs_in_hierarchy',     'api/tasks/{id}/leafs_in_hierarchy/') #json

    config.add_route('get_task_related_entities',       'api/tasks/{id}/related/{e_type}/{d_type}/') # json
    config.add_route('get_task_dependency',             'api/tasks/{id}/dependency/{type}/') # json
    config.add_route('get_task_tickets',                'api/tasks/{id}/tickets')  # json

    config.add_route('get_task_reviews',        'api/tasks/{id}/reviews/')  # json
    config.add_route('get_task_reviews_count',  'api/tasks/{id}/reviews/count/')  # json
    config.add_route('get_task_reviewers',      'api/tasks/{id}/reviewers/')  # json
    config.add_route('get_task_last_reviews',   'api/tasks/{id}/last_reviews/') #json

    config.add_route('request_review',          'api/tasks/{id}/request_review')

    config.add_route('approve_task',       'api/tasks/{id}/approve')
    config.add_route('request_revision',   'api/tasks/{id}/request_revision')
    config.add_route('request_revisions',  'api/tasks/request_revisions')

    config.add_route('request_extra_time', 'api/tasks/{id}/request_extra_time')

    config.add_route('get_task_resources',     'api/tasks/{id}/resources/') #json
    config.add_route('remove_task_user',       'api/tasks/{id}/remove/{user_type}/{user_id}')
    config.add_route('change_tasks_users',     'api/tasks/change/{user_type}')

    config.add_route('change_task_users',      'api/tasks/{id}/change/{user_type}')
    config.add_route('change_tasks_priority',  'api/tasks/change_priority')

    config.add_route('add_tasks_dependencies', 'api/tasks/add/dependencies')

    config.add_route('delete_task', 'api/tasks/delete')

    config.add_route('fix_tasks_statuses',     'api/tasks/fix/statuses/')
    config.add_route('fix_task_statuses',      'api/tasks/{id}/fix/statuses/')
    config.add_route('fix_task_schedule_info', 'api/tasks/{id}/fix/schedule_info/')

    config.add_route('watch_task',   'api/tasks/{id}/watch')
    config.add_route('unwatch_task', 'api/tasks/{id}/unwatch')

    # *************************************************************************
    # TimeLog
    config.add_route('time_log', '/api/time_logs/{id}')
    config.add_route('time_logs', '/api/time_logs')

    # *************************************************************************
    # Ticket
    config.add_route('ticket', '/api/tickets/{id}')
    config.add_route('tickets', '/api/tickets')

    config.add_route('ticket_links',           '/api/tickets/{id}/links')
    config.add_route('ticket_related_tickets', '/api/tickets/{id}/related_tickets')
    config.add_route('ticket_logs',            '/api/tickets/{id}/logs')

    # extra urls
    config.add_route('ticket_resolutions', '/api/ticket_resolutions')
    config.add_route('ticket_workflow',    '/api/ticket_workflow')

    # *************************************************************************
    # Vacation
    config.add_route('vacation',   '/api/vacations/{id}')
    config.add_route('vacations',  '/api/vacations')

    # *************************************************************************
    # Version
    config.add_route('create_version',                      'api/versions/create')

    config.add_route('get_task_versions',                   'api/tasks/{id}/versions/')  # jsons
    config.add_route('get_user_versions',                   'api/users/{id}/versions/')  # jsons
    config.add_route('get_entity_versions',                 'api/entities/{id}/versions/')  # json
    config.add_route('get_entity_versions_used_by_tasks',   'api/entities/{id}/version/used_by/tasks/') # json

    config.add_route('pack_version', 'api/versions/{id}/pack')  # json

    # *************************************************************************
    # Department
    config.add_route('department',  '/api/departments/{id}')
    config.add_route('departments', '/api/departments')
    config.add_route('department_users', '/api/departments/{id}/users')
    config.add_route('department_user_roles', '/api/departments/{id}/user_roles')

    # old ones
    config.add_route('department_tasks', '/api/departments/{id}/tasks')

    # *************************************************************************
    # Group
    config.add_route('group',       '/api/groups/{id}')
    config.add_route('groups',      '/api/groups')

    # collection views
    config.add_route('group_users', '/api/groups/{id}/users')

    # *************************************************************************
    # Tag
    config.add_route('tag',    'api/tags/{id}')
    config.add_route('tags',   'api/tags')

    # *************************************************************************
    # Type
    config.add_route('type',   'api/types/{id}')
    config.add_route('types',  'api/types')

    # *************************************************************************
    # Role
    config.add_route('role',  '/api/roles/{id}')
    config.add_route('roles', '/api/roles')

    # *************************************************************************
    # Price Lists / Good
    config.add_route('get_studio_goods',  'api/studios/{id}/goods/')
    config.add_route('get_goods', 'api/goods/')

    config.add_route('get_studio_price_lists', 'api/studios/{id}/price_lists/')
    config.add_route('get_price_lists', 'api/price_lists/')

    config.add_route('create_good', 'api/goods/create')
    config.add_route('edit_good',   'api/goods/edit')
    config.add_route('update_good', 'api/goods/update')
    config.add_route('delete_good', 'api/goods/delete')

    # *************************************************************************
    # Anima
    config.add_route('add_related_assets',   'api/entities/{id}/assets/add')
    config.add_route('remove_related_asset', 'api/entities/{id}/assets/{a_id}/remove')
    config.add_route('get_entity_task_type_result', 'api/entities/{id}/{task_type}/result')

    # *************************************************************************
    # Test
    config.add_route('test_page', 'test_page')

    config.scan(ignore='stalker.env')
    return config.make_wsgi_app()


# TODO: auto register created_by and updated_by values by using SQLAlchemy
#       events 'before_update' and 'before_create'
