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
import calendar
import datetime

from pyramid.httpexceptions import HTTPServerError, HTTPForbidden
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import has_permission, authenticated_userid

from stalker import log, SimpleEntity
from stalker.db.session import DBSession
import transaction


logger = logging.getLogger(__name__)
logger.setLevel(log.logging_level)

# this is a dummy mail address change it in the config (*.ini) file
dummy_email_address = "Stalker Pyramid <stalker.pyramid@stalker.pyramid.com>"


def utc_to_local(utc_dt):
    """converts utc time to local time

    based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083
    """
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= datetime.timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def local_to_utc(local_dt):
    """converts local datetime to utc datetime

    based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083
    """
    # get the utc_dt as if the local_dt is utc and calculate the timezone
    # difference and add it to the local dt object
    logger.debug('utc_to_local(local_dt) : %s' % utc_to_local(local_dt))
    logger.debug('utc - local            : %s' % (utc_to_local(local_dt) - local_dt))
    logger.debug('local - (utc - local)  : %s' % (local_dt - (utc_to_local(local_dt) - local_dt)))
    return local_dt - (utc_to_local(local_dt) - local_dt)


def to_seconds(timing, unit):
    """converts timing to seconds"""
    return timing*seconds_in_unit(unit)


def seconds_in_unit(unit):
    # when connected to the database the defaults will be updated with the
    # studio defaults
    from stalker import defaults
    if unit == 'min':
        return 60
    elif 'h':
        return 3600
    elif 'd':
        return defaults.daily_working_hours * 3600
    elif 'w':
        return defaults.weekly_working_hours * 3600
    elif 'm':
        return 4 * defaults.weekly_working_hours * 3600
    elif 'y':
        return defaults.yearly_working_days * defaults.daily_working_hours
    else:
        return 0


class StdErrToHTMLConverter():
    """Converts stderr, stdout messages of TaskJuggler to html

    :param error: An exception
    """

    formatChars = {
        '\e[1m': '<strong>',
        '\e[21m': '</strong>',
        '\e[2m':  '<span class="dark">',
        '\e[22m': '</span>',
        '\n': '<br>',
        '\x1b[34m': '<span class="alert alert-info" style="overflow-wrap: break-word">',
        '\x1b[35m': '<span class="alert alert-warning" style="overflow-wrap: break-word">',
        '\x1b[31m': '<span class="alert alert-error" style="overflow-wrap: break-word">',
        '\x1b[0m': '</span>',
        'Warning:': '<strong>Warning:</strong>',
        'Info:': '<strong>Info:</strong>',
        'Error:': '<strong>Error:</strong>',
    }

    def __init__(self, error):
        if isinstance(error, Exception):
            self.error_message = str(error)
        else:
            self.error_message = error

    def replace_tjp_ids(self, message):
        """replaces tjp ids in error messages with proper links
        """
        import re
        pattern = r"Task[\w0-9\._]+[0-9]"

        all_tjp_ids = re.findall(pattern, message)
        new_message = message
        for tjp_id in all_tjp_ids:
            entity_type_and_id = tjp_id.split('.')[-1]
            entity_type = entity_type_and_id.split('_')[0]
            entity_id = entity_type_and_id.split('_')[1]

            # get the entity
            # entity = Entity.query.filter(Entity.id == entity_id).first()
            # assert isinstance(entity, Entity)

            link = '/%(class_name)ss/%(id)s/view' % {
                'class_name': entity_type.lower(),
                'id': entity_id
            }
            name = '%(name)s' % {
                'name': entity_type_and_id,
                # 'type': entity.entity_type
            }

            path = '<a href="%(link)s">%(name)s</a>' % {
                'link': link,
                'name': name
            }

            new_message = new_message.replace(tjp_id, path)
        return new_message

    def html(self, replace_links=False):
        """returns the html version of the message
        """
        # convert the error message to a string
        if isinstance(self.error_message, list):
            output_buffer = []
            for msg in self.error_message:
                # join the message in to <p> elements
                output_buffer.append('%s' % msg.strip())

            # convert the list to string
            str_buffer = '\n'.join(output_buffer)
        else:
            str_buffer = self.error_message

        if replace_links:
            str_buffer = self.replace_tjp_ids(str_buffer)

        # for each formatChar replace them with an html tag
        for key in self.formatChars.keys():
            str_buffer = str_buffer.replace(key, self.formatChars[key])
        # put everything inside a p
        str_buffer = '<p>%s</p>' % str_buffer

        return str_buffer


class PermissionChecker(object):
    """Helper class for permission check
    """

    def __init__(self, request):
        self.has_permission = has_permission
        self.request = request

    def __call__(self, perm):
        return self.has_permission(perm, self.request.context, self.request)


def multi_permission_checker(request, permissions):
    pc = PermissionChecker(request)
    return all(map(pc, permissions))


def log_param(request, param):
    if param in request.params:
        logger.debug('%s: %s' % (param, request.params[param]))
    else:
        logger.debug('%s not in params' % param)


@view_config(
    context=HTTPServerError
)
def server_error(exc, request):
    msg = exc.args[0] if exc.args else ''
    response = Response('Server Error: %s' % msg, 500)
    transaction.abort()
    return response


def get_parent_task_status(children_statuses):

    binary_status_codes = {
        'WFD':  256,
        'RTS':  128,
        'WIP':  64,
        'PREV': 32,
        'HREV': 16,
        'DREV': 8,
        'OH':   4,
        'STOP': 2,
        'CMPL': 1
    }

    children_to_parent_statuses_lut = [
        0, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2
    ]

    parent_statuses_lut = ['WFD', 'RTS', 'WIP', 'CMPL']

    binary_status = 0
    for child_status_code in children_statuses:
        binary_status += binary_status_codes[child_status_code]

    status_index = children_to_parent_statuses_lut[binary_status]
    status = parent_statuses_lut[status_index]

    return status


def invalidate_all_caches():
    """invalidates all cache values.
    Based on: http://stackoverflow.com/a/14251064/3259351
    """
    from beaker.cache import cache_managers
    for _cache in cache_managers.values():
        _cache.clear()


def simple_entity_interpreter(value):
    """interprets parameter values to get a SimpleEntity instance
    """
    if isinstance(value, (list, tuple)):
        return SimpleEntity.query.filter(SimpleEntity.id.in_(value)).all()
    else:
        return SimpleEntity.query.filter(SimpleEntity.id == value).first()


def datetime_interpreter(value):
    """interprets parameter values to get a Datetime instance
    """
    import datetime
    epoch = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(microseconds=int(value) * 1000)
    return epoch + delta


def timedelta_interpreter(value):
    """interprets parameter values to get a Timedelta instance
    """
    import datetime
    return datetime.timedelta(milliseconds=int(value))


class EntityViewBase(object):
    """The base class for all Entity views

    GET    : To get existing data, this is the simplest one.
    POST   : To update an existing entity.
    PUT    : To crate a new entity.
    PATCH  : To update an existing entity with a subset of parameters.
    DELETE : To delete an entity

    ** GET **
    Individual and multiple entities queried through a GET request to their
    views. So to get one User instance a GET request should be send to
    /api/users/{id} (GET: /api/users/{id}), to get multiple or all users in the
    system a GET request to /api/users (notice the missing forward slash at the
    end of the view address) should be created (GET: /api/users).

        To get multiple user instances

            GET: /api/users

        To get only one specific user

            GET: /api/users/{id}

    ** POST **
    Entity attributes are updated or relations are created through POST calls
    to entity views. For example, to assign a user to only one department
    (removing the others from User.departments) a POST request to
    /api/users/{id}/departments should be created with ``dep_id`` parameter.
    But for simple (non collection) attributes there is no difference between
    POST and PATCH.

        To update all User parameters:

            POST: /api/users/{id}?name=Test%2User&email=user@users.com&login=user&password=12345

        To assign a user only to the given departments:

            POST: /api/users/{id}/departments?dep_id=23&dep_id=34

    ** PUT **
    Any entity should be created to a PUT call through their view. In return
    the view will respond with a JSON object that has the user details and most
    importantly with an id field that can be used to create further details
    about that user. An entity can not be created through its relation to
    another entity, ex. it is not possible to create a Department through its
    relation of User.

        To create a new user:

            PUT: /api/users?name=Test%2User&email=user@users.com&login=user&password=12345

        This will raise a 404:

            PUT: /api/users/{id}/departments?name=New%2Department

    ** PATCH **
    Patch requests can be used like POST requests, but with a subset of
    parameters. It can be used to update simple parameters or it can be used to
    create relations without breaking the other relations. So to  add a user to
    a department without removing it from other departments use a PATCH request
    to /api/users/{id}/departments with only one single dep_id (but it can also
    accept multiple dep_ids)

        Update ``User.name`` and ``User.email`` without supplying all the other
        parameters:

            PATCH: /api/users/{id}?name=user1&email=user1@users.com

        To add aa user to a department without removing from the other
        departments:

            PATCH: /api/users/{id}/departments?dep_id=23

    ** DELETE **
    To delete an entity or to remove a relation between two entities a DELETE
    request can be used. For example, to delete a User instance create a DELETE
    request to /api/users/{id} (DELETE: /api/users/{id}), to remove a user from
    one department do a DELETE request to /api/users/{id}/departments with one
    or multiple ``dep_id`` parameters
    (DELETE: /api/users/{id}/departments?dep_id=23&dep_id=563).

        DELETE: /api/users/{id}                       (To delete a user
        DELETE: /api/users/{id}/departments?dep_id=23 (To remove a user from
                                                       department with id=23)
        DELETE: /api/users                            (This will raise 404)

    """

    som_class = None
    local_params = []

    @property
    def param_resolution(self):
        """returns the param resolution

        TODO: This is stupid, but it is what we have at hand for now
              In later versions use the SQLAlchemy instrumented attributes to
              automatically discover the attributes.
        """
        # I don't know if this is a good hack
        # gather all the local_params from all of the super classes
        supers_params = []
        for c in self.__class__.__mro__:
            try:
                supers_params += c.local_params
            except AttributeError:
                pass

        supers_params.extend(self.local_params)
        return supers_params

    def __init__(self, request):
        self.request = request
        self.entity_id = request.matchdict.get('id')
        self.entity = None

        if self.entity_id:
            from stalker import SimpleEntity
            from sqlalchemy.exc import DataError
            try:
                self.entity = SimpleEntity.query\
                    .filter(SimpleEntity.id == self.entity_id).first()
            except DataError:
                self.entity = None

            if not self.entity:
                from pyramid.exceptions import HTTPNotFound
                raise HTTPNotFound('Entity not found!')

    @classmethod
    def update_response_data(cls, response, data):
        """updates the response data
        """
        response_data = response.json_body
        response_data.update(data)
        response.json_body = response_data
        return response

    def get_entity(self):
        """abstract base method for getting one entity
        """
        raise NotImplementedError

    def get_entities(self):
        """abstract base method for getting multiple entities
        """
        filters = self.filter_generator(self.som_class)
        return self.collection_query(self.som_class, filters=filters)

    def create_entity(self):
        """abstract base method for creating one entity
        """
        new_entity = self.entity_creator(self.som_class, self.param_resolution)
        self.entity = new_entity

        # return the newly created note data as JSON
        self.entity_id = new_entity.id
        response = self.get_entity()
        response.status_code = 201
        return response

    def resolve_param_resolution(self, param_resolution, raise_nullable_errors=True):
        """Resolves the given parameter resolution and converts it to a arg
        list which is suitable to be used in __init__() of a given class.

        :param raise_nullable_errors: Sets the method to a "raise error" mode
          in which it will raise a HTTPServerError for any parameter that is
          not nullable but doesn't have a value in the ``self.request.params``.
        :param param_resolution: A list of dictionaries in following format::

            [
                # For Simple arguments
                {
                    'param_name': ...,
                    'interpreter': ...,
                    'nullable: ...,
                }

                # or for complex arguments
                {
                    'param_name': ...,
                    'arg_name': ...,
                    'is_list': ...,
                    'interpreter': ...,
                    'nullable': ...,
                }

                # for complex attributes with specified query Class
                {
                    'param_name': ...,
                    'arg_name': ...,
                    'is_list': ...,
                    'query_class': ...,
                    'interpreter': ...,
                    'nullable': ...,
                }

            ]

            param_name: The name of the parameter
            arg_name: The name of the argument on __init__ of the SOM class.
              Default value is equal to ``param_name``.
            is_list: A boolean value to show if this arg is a list. Default
              value is False.
            interpreter: A callable that will convert the incoming data to the
              required type, None if the data is already in good condition.
              Default value is None.
            nullable: A bool value of True or False, showing that the parameter
              can be skipped. Default value is True. It can also be set to a
              string value showing another parameter name, which defines it is
              not nullable but if the other parameter is filled than it can be
              skipped.
        """

        # get arguments
        import transaction
        from pyramid.httpexceptions import HTTPServerError

        args = {}
        for res in param_resolution:
            param_name = res.get('param_name')
            arg_name = res.get('arg_name', param_name)
            is_list = res.get('is_list', False)
            nullable = res.get('nullable', True)
            interpreter = res.get('interpreter', None)

            # This is a complex attr
            data_source = self.get_data_source(self.request)
            if is_list:
                arg_value = data_source.getall(param_name)
            else:
                arg_value = data_source.get(param_name)

            if arg_value and interpreter:
                arg_value = interpreter(arg_value)

            if not nullable and not arg_value and raise_nullable_errors:
                transaction.abort()
                raise HTTPServerError(
                    'Missing "%s" parameter' % param_name
                )

            if arg_value:
                args[arg_name] = arg_value

        return args

    def entity_creator(self, entity_class, param_resolution):
        """Creates SOM class instances by using param_resolution.

        :param entity_class: A SOM Class
        :param param_resolution: A list of dictionaries. See
          :method:``.resolve_param_resolution`` for details.
        """
        args = self.resolve_param_resolution(param_resolution)

        # fix created_by value if skipped
        # and use the logged in user as the creator
        if 'created_by' not in args:
            logged_in_user = self.get_logged_in_user(self.request)
            args['created_by'] = logged_in_user

        from stalker.db.session import DBSession
        new_entity = entity_class(**args)
        DBSession.add(new_entity)
        DBSession.flush()
        transaction.commit()

        return new_entity

    def entity_updater(self, entity, param_resolution):
        """updates entity parameters with the given param_resolution

        :param entity: A SOM entity
        :param param_resolution: A is list of dictionaries. See
          :method:``.resolve_param_resolution`` for details.
        """
        # get arguments
        args = self.resolve_param_resolution(
            param_resolution,
            raise_nullable_errors=False
        )

        # fix updated_by value if skipped
        # and use the logged in user as the updater
        if 'updated_by' not in args:
            logged_in_user = self.get_logged_in_user(self.request)
            args['updated_by'] = logged_in_user

        for attr_name, attr_value in args.iteritems():
            setattr(entity, attr_name, attr_value)

    def update_entity(self):
        """abstract base method for updating one entity
        """
        raise NotImplementedError

    def delete_entity(self):
        """deletes one note
        """
        from stalker.db.session import DBSession
        DBSession.delete(self.entity)
        DBSession.flush()

    @classmethod
    def get_time(cls, request, time_attr):
        """Extracts a time object from the given request

        :param request: the request object
        :param time_attr: the attribute name
        :return: datetime.timedelta
        """
        time_part = datetime.datetime.strptime(
            request.params[time_attr][:-4],
            '%a, %d %b %Y %H:%M:%S'
        )

        return datetime.timedelta(
            hours=time_part.hour,
            minutes=time_part.minute
        )

    @classmethod
    def get_date(cls, request, date_attr):
        """Extracts a UTC datetime object from the given request

        :param request: the request instance
        :param date_attr: the attribute name
        :return: datetime.datetime
        """
        # Always work with UTC
        return datetime.datetime.strptime(
            request.params[date_attr][:-4],
            '%a, %d %b %Y %H:%M:%S'
        )

    @classmethod
    def get_date_range(cls, request, date_range_attr):
        """Extracts a UTC datetime object from the given request

        :param request: the request instance
        :param date_range_attr: the attribute name
        :return: datetime.datetime
        """
        date_range_string = request.params.get(date_range_attr)
        start_str, end_str = date_range_string.split(' - ')
        start = datetime.datetime.strptime(start_str, '%m/%d/%Y')
        end = datetime.datetime.strptime(end_str, '%m/%d/%Y')
        return start, end

    @classmethod
    def get_datetime(cls, request, date_attr, time_attr):
        """Extracts a UTC  datetime object from the given request
        :param request: the request object
        :param date_attr: the attribute name
        :return: datetime.datetime
        """
        date_part = datetime.datetime.strptime(
            request.params[date_attr][:-4],
            '%a, %d %b %Y %H:%M:%S'
        )

        time_part = datetime.datetime.strptime(
            request.params[time_attr][:-4],
            '%a, %d %b %Y %H:%M:%S'
        )

        # update the time values of date_part with time_part
        return date_part.replace(
            hour=time_part.hour,
            minute=time_part.minute,
            second=time_part.second,
            microsecond=time_part.microsecond
        )

    @classmethod
    def get_logged_in_user(cls, request):
        """Returns the logged in user as User instance

        :param request: Request object
        """
        from stalker import User
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            user = User.query \
                .filter_by(login=authenticated_userid(request)).first()

        if not user:
            raise HTTPForbidden(request)

        return user

    @classmethod
    def get_data_source(cls, request):
        """returns the data source which can be request.POST or request.params
        depending on the content-type value
        """
        data = request.params
        if hasattr(request, 'content_type'):
            if request.content_type.startswith('multipart'):
                data = request.POST
        return data

    @classmethod
    def get_multi_integer(cls, request, param_name):
        """Extracts multi data from request.POST

        :param request: Request object
        :param param_name: Parameter name to extract data from
        :return:
        """
        data = cls.get_data_source(request)
        return map(int, data.getall(param_name))

    @classmethod
    def get_multi_string(cls, request, param_name):
        """Extracts multi data from request.POST

        :param request: Request object
        :param param_name: Attribute name to extract data from
        :return:
        """
        data = cls.get_data_source(request)
        return data.getall(param_name)

    @classmethod
    def get_color_as_int(cls, request, param_name):
        """Extracts a color from request
        """
        return int(request.params.get(param_name, '#000000')[1:], 16)

    @classmethod
    def get_tags_data(cls, request, parameter='tags[]'):
        """Extracts Tags from the given request

        :param request: Request object
        :param str parameter:
        :return: A list of stalker.models.tag.Tag instances
        """
        # Tags
        tags = []
        tag_names = request.POST.getall(parameter)
        for tag_name in tag_names:
            logger.debug('tag_name : %s' % tag_name)
            if tag_name == '':
                continue
            from stalker import Tag
            tag = Tag.query.filter(Tag.name == tag_name).first()
            if not tag:
                logger.debug('new tag is created %s' % tag_name)
                tag = Tag(name=tag_name)
                DBSession.add(tag)
            tags.append(tag)
        return tags

    @classmethod
    def get_user_os(cls, request):
        """returns the user operating system name
        """
        user_agent = request.headers['user-agent']

        if 'Windows' in user_agent:
            return 'windows'
        elif 'Linux' in user_agent:
            return 'linux'
        elif 'OS X' in user_agent:
            return 'osx'

    @classmethod
    def get_path_converter(cls, request, task):
        """returns a partial function that converts the given path to another path
        that is visible to other OSes.
        """
        user_os = cls.get_user_os(request)
        repo = task.project.repository

        path_converter = lambda x: x

        if user_os == 'windows':
            path_converter = repo.to_windows_path
        elif user_os == 'linux':
            path_converter = repo.to_linux_path
        elif user_os == 'osx':
            path_converter = repo.to_osx_path

        return path_converter

    @classmethod
    def seconds_since_epoch(cls, dt):
        """converts the given datetime.datetime instance to an integer showing the
        seconds from epoch, and does it without using the strftime('%s') which
        uses the time zone info of the system.

        :param dt: datetime.datetime instance to be converted
        :returns int: showing the seconds since epoch
        """
        dts = dt - datetime.datetime(1970, 1, 1)
        return dts.days * 86400 + dts.seconds

    @classmethod
    def milliseconds_since_epoch(cls, dt):
        """converts the given datetime.datetime instance to an integer showing the
        milliseconds from epoch, and does it without using the strftime('%s') which
        uses the time zone info of the system.

        :param dt: datetime.datetime instance to be converted
        :returns int: showing the milliseconds since epoch
        """
        dts = dt - datetime.datetime(1970, 1, 1)
        return dts.days * 86400000 + dts.seconds * 1000 + dts.microseconds / 1000

    @classmethod
    def from_microseconds(cls, t):
        """converts the given microseconds showing the time since epoch to datetime
        instance
        """
        # TODO: This should be a date with UTC timezone injected.
        epoch = datetime.datetime(1970, 1, 1)
        delta = datetime.timedelta(microseconds=t)
        return epoch + delta

    @classmethod
    def from_milliseconds(cls, t):
        """converts the given milliseconds showing the time since epoch to datetime
        instance
        """
        return cls.from_microseconds(t * 1000)

    @classmethod
    def type_interpreter(cls, value):
        """Guesses the data type by looking at the given value.

        This method searches for ':' sign where the left of the sign defines
        the data type and the right defines the value (ex: date:141545123600
        which is a date value in form that is usually represented in JSON).

        Values without a ':' will not be interpreted.
        """
        if value and ':' in value:
            type_name, value = value.split(':')
            if type_name.lower() == 'date':
                # convert the date value in to utc date
                value = datetime_interpreter(value)

        # in any other case use the raw value
        return value

    def filter_generator(self, class_):
        """generates simple filters for SOM query
        """
        filters = []
        if self.request.params.keys():
            for key, value in self.request.params.iteritems():
                try:
                    if '!' in value:
                        if '~' in value:
                            formatted_value = '%{v}%'.format(v=value[2:])
                            formatted_value = \
                                self.type_interpreter(formatted_value)
                            f = ~getattr(class_, key).ilike(formatted_value)
                        else:
                            formatted_value = value[1:]
                            formatted_value = \
                                self.type_interpreter(formatted_value)
                            f = getattr(class_, key) != formatted_value
                    elif '~' in value:
                        formatted_value = '%{v}%'.format(v=value[1:])
                        formatted_value = \
                            self.type_interpreter(formatted_value)
                        f = getattr(class_, key).ilike(formatted_value)
                    elif '>' in value:
                        value = self.type_interpreter(value[1:])
                        f = getattr(class_, key) > value
                    elif '<' in value:
                        value = self.type_interpreter(value[1:])
                        f = getattr(class_, key) < value
                    else:
                        formatted_value = \
                            self.type_interpreter(value)
                        f = getattr(class_, key) == formatted_value

                    filters.append(f)
                except AttributeError:
                    pass
        return filters

    @classmethod
    def collection_query(cls,
                         collection_class,
                         join=None,
                         filters=None,
                         order_by=None
                         ):
        """returns the simplest data of the given collection
        """
        from stalker.db.session import DBSession
        query = DBSession\
            .query(
                collection_class.id,
                collection_class.name,
                collection_class.entity_type
            )

        if join is not None:
            query = query.join(join)

        if filters is not None:
            if isinstance(filters, list):
                # it is a list like object
                # stack it up
                for f in filters:
                    query = query.filter(f)
            else:
                # it is a singular element
                query = query.filter(filters)

        if order_by is not None:
            query = query.order_by(order_by)

        logger.debug('query:%s' % query)

        result = query.all()

        from stalker_pyramid2 import entity_type_to_url
        data = [
            {
                'id': r[0],
                'name': r[1],
                'entity_type': r[2],
                '$ref': '%s/%s' % (entity_type_to_url[r[2]], r[0]),
            } for r in result
        ]
        from pyramid.response import Response
        return Response(json_body=data, status=200)
