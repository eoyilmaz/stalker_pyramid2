=====
About
=====

Stalker is an Open Source Production Asset Management (ProdAM) System designed
specifically for Animation and VFX Studios but can be used for any kind of
projects. Stalker is licensed under LGPL v3. And Stalker Pyramid is the
Pyramid Web App package based on Stalker. Basically it supplies the web
interfaces to the system. It is also licensed under LGPL v3.

Features:
 * Designed for animation and VFX Studios.
 * It is a Pyramid Web Application.
 * Platform independent.
 * Default installation handles nearly all the asset and project management
   needs of an animation and vfx studio.
 * Customizable with configuration scripts.
 * Customizable object model (Stalker Object Model - SOM).
 * Uses TaskJuggler as the project planing and tracking backend.
 * Can be used with any kind of databases supported by SQLAlchemy.

Stalker Pyramid is build over these other OpenSource projects:
 * Python
 * Stalker
 * Pyramid
 * SQLAlchemy and Alembic
 * Jinja2
 * TaskJuggler
 * Angular2/4
 * Twitter Bootstrap

Source
======

The latest development version is available in `GitHub`_::

  git clone https://github.com/eoyilmaz/stalker_pyramid

.. _GitHub: https://github.com/eoyilmaz/stalker_pyramid

Installation
============

Installing Stalker Pyramid is a little bit involved, but it trust me it is
easy.

First you need to download and install a couple of programs like `Python`_,
`node.js`_, `git`_, `PostgreSQL`_. If you use a Linux flavour chances are they
are already installed in your system and if not use the package manager of your
Linux distro to install them. For Windows use the supplied links.

Install those programs and restart your computer or logout and login again if
you are in Linux.

Stalker Pyramid is written for Python 2.7 but in near feature it should also
support Python 3.0+. For now Python 2.7 is the best version to run Stalker
Pyramid.

Running Stalker Pyramid in its own virtual environment is the best practice. To
install ``virtualenv`` run the following command on a Command Prompt for
Windows or in a Terminal for OSX and Linux::

  pip install virtualenv

Let's create a virtual environment for Stalker Pyramid. Browse to a folder that
you want to store the Stalker Pyramid installation and run the following
command::

  virtualenv stalker_pyramid

This will create a folder called ``stalker_pyramid`` in the current directory.
Run the following command to change the current dir to ``stalker_pyramid``::

  cd stalker_pyramid

The following command will clone the GitHub repository::

  git clone https://github.com/eoyilmaz/stalker_pyramid

Under Windows you may need to run this command through the ``Git Bash`` which
should be installed if you used the default installation settings. If you're
using the Git Bash, you need to browse to the virtualenv directory we have just
created.

This will create a folder named ``stalker_pyramid`` in the same folder that you
have run that command and it will contain all the source files.

Now it is time to install all the JavaScript libraries required to run the
system. While in the root of the virtual environment directory we have just
created run the following commands::

  cd stalker_pyramid
  cd stalker_pyramid
  cd static
  npm install bootstrap jquery@3.2.1 angular@1.6.4

This should create a folder called ``node_modules`` and install all the
libraries in it.

Now browse back to the root source folder:

  cd <full_path_to_the_virtual_env>/stalker_pyramid/stalker_pyramid

(use backslashes if you are under Windows)

And run the following command to install the required Python packages.

For Linux::

  ../bin/python setup.py develop

For Windows:

  ..\Scripts\python setup.py develop

This should install all the required Python packages for Stalker Pyramid. If
you get any errors, read them and install the packages one by one.

Now it is time to create our PostgreSQL database that Stalker will use. There
are tons of tutorials for that on web. Just create a user with name
``stalker_admin`` and give it the admin privileges and set its password to
``stalker`` for example. Then create a database with the name ``stalker`` and
run the PostgreSQL server. The postgresql server should be using the default
port 5432 (if you want to use a different user name, password and port you can
specify them in the ``production.ini`` file in the root folder of Stalker
Pyramid.

Now we need to initialize the database::

For Linux::

  ../bin/python scripts/initializedb.py production.ini

For Windows::

  ..\Scripts\python scripts/initializedb.py production.ini

This should create the tables and some default data.

Now we can run the web server that will serve our Pyramid application::

For Linux::

  ../bin/pserve production.ini

For Windows::

  ..\Scripts\pserve production.ini

Now you can open your favourite browser and enter the following address::

  http:://localhost:6543

And you should see the login page. Use ``admin`` for username and ``admin`` as
the password.

And that's it. Congratulations now you have Stalker Pyramid running in your
system.

If you liked Stalker Pyramid and want to use it in your studio it is best to
setup a dedicated server for Stalker Pyramid preferably running a Linux distro
like `CentOS`_.

.. _Python: https://www.python.org/
.. _git: https://git-scm.com/downloads
.. _node.js: https://nodejs.org/en/download/
.. _PostgreSQL: https://www.postgresql.org/download/
.. _CentOS: https://www.centos.org/
