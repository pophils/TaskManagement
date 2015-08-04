
from fabric.api import run, local, env, cd, lcd
from fabric.contrib.files import exists
import os

env.hosts = ['localhost']
env.user = 'pophils'

root_folder = os.path.dirname(__file__)


def run_production():
    with cd('/home/%s/Documents/GitBase/djangobase/yasanaproject'  % env.user):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py runserver --settings=yasanaproject.settings.production', 
              capture=True)        

def run_local():
    with lcd('%s' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py runserver --settings=yasanaproject.settings.local', 
              capture=False)      
    
def run_unit():
    with lcd('%s/tests/unit/' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 ../../manage.py test -s --verbosity=1 --rednose --settings=yasanaproject.settings.test', 
              capture=False)

def run_functional():
    with lcd('%s/tests/functional/' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 ../../manage.py test -s --verbosity=1 --rednose --settings=yasanaproject.settings.test', 
              capture=False)
      
def makemigration_local():
    with lcd('/home/%s/Documents/GitBase/djangobase/yasanaproject'  % env.user):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py makemigrations --settings=yasanaproject.settings.local')

def makemigration_test():
    with lcd('%s' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py makemigrations --settings=yasanaproject.settings.test')

def migrate_local():
    with lcd('%s' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py migrate --settings=yasanaproject.settings.local')

def migrate_test():
    with lcd('%s' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py migrate --settings=yasanaproject.settings.test')

def create_cache_table():
    with lcd('%s' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py createcachetable --settings=yasanaproject.settings.local')
        
def start_app(appname):
    with lcd('%s' % root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py startapp {}'.format(appname), 
              capture=False)
