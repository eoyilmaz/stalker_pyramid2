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
import os

from pyramid.view import view_config
from pyramid.response import Response

from stalker import Task, Version, Entity, User

# from stalker_pyramid.views.link import MediaManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@view_config(
    route_name='create_version',
    permission='Create_Version'
)
def create_version(request):
    """runs when creating a version
    """
    logged_in_user = get_logged_in_user(request)

    task_id = request.params.get('task_id')
    task = Task.query.filter(Task.id == task_id).first()

    take_name = request.params.get('take_name', 'Main')
    is_published = \
        True if request.params.get('is_published') == 'true' else False
    description = request.params.get('description')
    bind_to_originals = \
        True if request.params.get('bind_to_originals') == 'true' else False

    file_object = request.POST.getall('file_object')[0]

    logger.debug('file_object: %s' % file_object)
    logger.debug('take_name: %s' % take_name)
    logger.debug('is_published: %s' % is_published)
    logger.debug('description: %s' % description)
    logger.debug('bind_to_originals: %s' % bind_to_originals)

    if task:
        extension = os.path.splitext(file_object.filename)[-1]
        mm = MediaManager()
        v = mm.upload_version(
            task=task,
            file_object=file_object.file,
            take_name=take_name,
            extension=extension
        )

        v.created_by = logged_in_user
        v.is_published = is_published
        v.created_with = "StalkerPyramid"
        v.description = description

        # check if bind_to_originals is true
        if bind_to_originals and extension == '.ma':
            from stalker_pyramid.views import archive
            arch = archive.Archiver()
            arch.bind_to_original(v.absolute_full_path)

        DBSession.add(v)
        logger.debug('version added to: %s' % v.absolute_full_path)
    else:
        return Response('No task with id: %s' % task_id, 500)

    return Response('Version is uploaded successfully!')


@view_config(
    route_name='get_entity_versions',
    renderer='json'
)
@view_config(
    route_name='get_task_versions',
    renderer='json'
)
def get_entity_versions(request):
    """returns all the Shots of the given Project
    """
    logger.debug('get_versions is running')

    entity_id = request.matchdict.get('id', -1)
    entity = Entity.query.filter_by(id=entity_id).first()

    user_os = get_user_os(request)

    logger.debug('entity_id : %s' % entity_id)
    logger.debug('user os: %s' % user_os)

    repo = entity.project.repository

    path_converter = lambda x: x
    if repo:
        if user_os == 'windows':
            path_converter = repo.to_windows_path
        elif user_os == 'linux':
            path_converter = repo.to_linux_path
        elif user_os == 'osx':
            path_converter = repo.to_osx_path

    return_data = [
        {
            'id': version.id,
            'task': {'id': version.task.id,
                     'name': version.task.name},
            'take_name': version.take_name,
            'parent': {
                'id': version.parent.id,
                'version_number': version.parent.version_number,
                'take_name': version.parent.take_name
                } if version.parent else None,
            'absolute_full_path': path_converter(version.absolute_full_path),
            'created_by': {
                'id': version.created_by.id if version.created_by else None,
                'name': version.created_by.name if version.created_by else None
            },
            'is_published': version.is_published,
            'version_number': version.version_number,
            'date_created': milliseconds_since_epoch(version.date_updated),
            'created_with': version.created_with,
            'description': version.description,
            'task_full_path': version.task.name
        }
        for version in entity.versions
    ]

    return return_data


@view_config(
    route_name='get_user_versions',
    renderer='json'
)
def get_user_versions(request):
    """returns all the Shots of the given Project
    """
    logger.debug('*******get_user_versions is running')

    user_id = request.matchdict.get('id', -1)
    user = User.query.filter_by(id=user_id).first()

    sql_query = """
        select
            "Versions".id,
            "Versions".is_published,
            "Version_SimpleEntities".date_updated,
            "Versions".take_name,
            "Versions".version_number,
            "Versions".created_with,
            "Version_SimpleEntities".description,
            tasks.id,
            tasks.name,
            tasks.path,
            tasks.full_path

        from "Versions"
        join "SimpleEntities" as "Version_SimpleEntities" on "Version_SimpleEntities".id = "Versions".id
        join "Users" on "Version_SimpleEntities".created_by_id = "Users".id
        join (
            %(tasks_hierarchical_name)s
        ) as tasks on tasks.id = "Versions".task_id

        where "Users".id = %(entity_id)s
        order by "Version_SimpleEntities".date_updated desc

        """

    sql_query = sql_query % {
                                'entity_id': user_id,
                                'tasks_hierarchical_name':
                                generate_recursive_task_query(ordered=False)
                            }

    from sqlalchemy import text  # to be able to use "%" sign use this function

    result = DBSession.connection().execute(text(sql_query))

    return_data = [
        {
            'id': r[0],
            'is_published':r[1],
            'date_created': milliseconds_since_epoch(r[2]),
            'take_name': r[3],
            'version_number': r[4],
            'created_with': r[5],
            'description': r[6],
            'task_name': r[8],
            'task_path': r[9],
            'task_full_path': r[10],
            'task': {'id': r[7],
                     'name': r[10]},
            'absolute_full_path':'',
            'created_by': {
                'id': user.id,
                'name': user.name
            }
        }
        for r in result.fetchall()
    ]

    return return_data


@view_config(
    route_name='pack_version'
)
def pack_version(request):
    """packs the requested version and returns a download link for it
    """
    version_id = request.matchdict.get('id')
    version = Version.query.get(version_id)

    if version:
        # before doing anything check if the file exists
        import os

        version_filename_without_extension = \
            os.path.splitext(version.filename)[0]
        archive_name = '%s%s' % (version_filename_without_extension, '.zip')
        archive_path = os.path.join(version.absolute_path, archive_name)
        logger.debug('ZIP Path: %s' % archive_path)
        if os.path.exists(archive_path):
            # just serve the same file
            logger.debug('ZIP exists, not creating it again!')
            new_zip_path = archive_path
        else:
            # create the zip file
            logger.debug('ZIP does not exists, creating it!')
            import shutil
            from stalker_pyramid.views.archive import Archiver

            path = version.absolute_full_path

            exclude_mask = [
                '.jpg', '.jpeg', '.png', '.tga', '.tif', '.tiff', '.ass',
                '.bmp', '.gif'
            ]

            arch = Archiver(exclude_mask=exclude_mask)
            task = version.task
            if False:
                assert(isinstance(version, Version))
                assert(isinstance(task, Task))
            project_name = version_filename_without_extension
            project_path = arch.flatten(path, project_name=project_name)

            # append link file
            stalker_link_file_path = os.path.join(project_path,
                                                  'scenes/stalker_links.txt')

            import stalker_pyramid
            version_upload_link = '%s/tasks/%s/versions/list' % (
                stalker_pyramid.stalker_server_external_url,
                task.id
            )
            request_review_link = '%s/tasks/%s/view' % (
                stalker_pyramid.stalker_server_external_url,
                task.id
            )
            with open(stalker_link_file_path, 'w+') as f:
                f.write("Version Upload Link: %s\n"
                        "Request Review Link: %s\n" % (version_upload_link,
                                                       request_review_link))
            zip_path = arch.archive(project_path)

            new_zip_path = os.path.join(
                version.absolute_path,
                os.path.basename(zip_path)
            )

            # move the zip right beside the original version file
            shutil.move(zip_path, new_zip_path)

            # now remove the temp files
            shutil.rmtree(project_path, ignore_errors=True)

        # open the zip file in browser
        # serve the file new_zip_path
        from pyramid.response import FileResponse

        logger.debug('serving packed version file: %s' % new_zip_path)

        response = FileResponse(
            new_zip_path,
            request=request,
            content_type='application/force-download',
        )

        # update the content-disposition header
        response.headers['content-disposition'] = \
            str('attachment; filename=' + os.path.basename(new_zip_path))

        return response
