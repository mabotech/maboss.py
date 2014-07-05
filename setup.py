import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    #'reportlab',
    #'scipy',
    #'numpy',
    #'gevent',
    #'pyzmq',
    'zerorpc',
    'pyodbc',
    'pylint',
    'msgpack-python',
    'simplejson',
    'gevent_zeromq',
    #'socket.io',
    #'matplotlib',
    'wmi',
    'pytz',
    'pip',
    #'psycopg2',
    #'PIL',
    'cx_Oracle',
    'SQLAlchemy',    
    'litex.cxpool',    
    'python_dateutil',    
    'pyserial',
    'lxml',
    'pyswip',
    'zope.interface',
    'twisted',    
    'flask',    
    'pywin32',
    'pyro',
    #'OpenOPC',
    'redis',    
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='maboss',
      version='1.2.2',
      description='maboss',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: ",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='MaboTech',
      license='MIT',
      author_email='mes@mabotech.com',
      url='http://www.mabotech.com',
      keywords='mabotech maboss lib web webx motorx',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='maboss',
      install_requires = requires,
      #entry_points = """\
      #[mabo.app_factory]
      #main = mabolab:main
      #""",
      
      data_files=[('maboss/webx/models',
                    ['maboss/webx/models/model_template.tpl',
                    'maboss/webx/models/form.html'])],  #sample configure file      

  )

