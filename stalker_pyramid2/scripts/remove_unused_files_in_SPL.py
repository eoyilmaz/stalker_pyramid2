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
"""This is a helper script for removing unused files in SPL.

Walks through SPL and checks if there is a Link instance per file in SPL and
removes the ones that doesn't have a related Link instance.
"""

import os
import sys

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)


from stalker import db, defaults, Link


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def remove_unused_files():
    """removes unused files from SPL
    """
    path = os.path.expandvars(
        os.path.expanduser(defaults.server_side_storage_path)
    )

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            spl_relative_path = full_path.replace(path, 'SPL')
            l = Link.query.filter(Link.full_path == spl_relative_path).first()
            if l is None:
                print spl_relative_path
                os.remove(full_path)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    db.setup(settings)
    # db.init() # no init needed

    remove_unused_files()


if __name__ == '__main__':
    main()
