import os

from setuptools import setup, find_packages
import stalker_pyramid

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

requires = [
    'pyramid',
    'transaction',
    'pyramid_tm',
    'pyramid_beaker',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'zope.sqlalchemy',
    'waitress',
    'jinja2',
    'pyramid_jinja2',
    'pillow',
    'stalker',
    'exifread',
]

test_requires = [
    'webtest',
]

setup(name='stalker_pyramid',
      version=stalker_pyramid.__version__,
      description='Stalker Based Web App',
      long_description='%s\n\n%s' % (README, CHANGES),
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Topic :: Office/Business :: Scheduling",
      ],
      author='Erkan Ozgur Yilmaz',
      author_email='eoyilmaz@gmail.com',
      url='https://www.github.com/eoyilmaz/stalker_pyramid/',
      keywords=['web', 'wsgi', 'bfg', 'pylons', 'pyramid', 'production',
                'asset', 'management', 'vfx', 'animation', 'houdini', 'nuke',
                'fusion', 'xsi', 'blender', 'vue', 'stalker'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require=test_requires,
      test_suite='stalker_pyramid',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = stalker_pyramid:main
      [console_scripts]
      initialize_stalker_pyramid_db = stalker_pyramid.scripts.initializedb:main
      """,
)

