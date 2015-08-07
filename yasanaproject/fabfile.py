

import os
from fabric.api import run, env, cd, abort, lcd, local
from fabric.contrib.files import exists
from fabric.contrib.console import confirm, prompt

env.hosts = ['ubuntu@whatever.com:5567'] # change tis later
env.user = 'pophils'
env.key_filename = '~/.ssh/ec2_private_key.pem'
env.repo_url = 'https://github.com/pophils/TaskManagement.git'

remote_root_folder = '/opt/'
local_root_folder = os.path.dirname(__file__)

remote_virtual_env_folder = '%s/virtual' % remote_root_folder
remote_static_folder = '%s/static' % remote_root_folder
remote_source_code_folder = '%s/source_code' % remote_root_folder

sub_dir_list = ['virtual', 'source_code', 'static']



def check_key_permission_file():
    if not exists(env.key_filename):
        abort('The SSH key filename not found at specified path: %(key_filename)s' % env)

def setup_directory():
    if len(sub_dir_list) < 3:
        abort('sub directories not complete')
        
    for dir_name in sub_dir_list: 
        if not exists('%s/%s' % (remote_root_folder, dir_name)):
            run('mkdir -p %s/%s' % (remote_root_folder, dir_name))

def setup_code_branch():
    with cd(remote_source_code_folder):
        if check_code_branch_checked_out():
            pull_code_request()
        else:
            clone_code_branch()
            

def setup_virtual_environment():
    with cd(remote_virtual_env_folder):
        if not check_virtual_env_existence():
            run('virtual_env --python=python3 ')

def check_virtual_env_existence():
    with cd(remote_virtual_env_folder):
        return exists('bin/pip')

def check_code_branch_checked_out():
    with cd(remote_source_code_folder):
        return exists('.git')

def pull_code_request():
    with cd(remote_source_code_folder):
        run('git pull origin')    

def clone_code_branch():
    with cd(remote_source_code_folder):
        run('git clone %(repo_url)s' % env)

def pip_install_requirement():
    with cd(remote_virtual_env_folder):
        run('bin/pip install -r %s/requirement.txt' % (remote_source_code_folder,))

def run_migration():
    with cd(remote_virtual_env_folder):
        run('bin/python3 %s/manage.py makemigrations' % (remote_source_code_folder,))
        run('bin/python3 %s/manage.py migrate' % (remote_source_code_folder,))

def collect_static():
    with cd(remote_virtual_env_folder):
        run('bin/python3 %s/manage.py collectstatic --no-input' % (remote_source_code_folder,))   

def create_cache_table():
    with cd(remote_virtual_env_folder):
        if confirm('Do you want to create a cache table for the project'):
            if confirm('Do you want to use the default cache table name: django-cache'):
                run('bin/python3 %s/manage.py createcachetable django-cache ' % (remote_source_code_folder,)) 
            else:
                table_name = prompt('Please enter the cache table name')
                if len(table_name.strip()) == 0:
                    print 'cache table name cannot be empty'
                    table_name = prompt('Proceed by entering a non-empty name or empty to abort')
                    if len(table_name.strip()) == 0:
                        abort('Dude, program aborted')
                
                run('bin/python3 %s/manage.py createcachetable %s ' % (remote_source_code_folder, table_name))                        
        
def run_unit_test():
    with cd(remote_source_code_folder):
        run('%s/bin/python3 /manage.py test /test/unit' % (remote_source_code_folder,))   

def deploy():
    check_key_permission_file()
    setup_directory()
    setup_code_branch()
    setup_virtual_environment()
    pip_install_requirement()
    run_migration()
    collect_static()
    create_cache_table()
    run_unit_test()


# Local stuff


def run_local():
    with lcd('%s' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py runserver '
              '--settings=yasanaproject.settings.local')
    
def run_unit():
    with lcd('%s/tests/unit/' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 ../../manage.py test -s --verbosity=1 --rednose '
              '--settings=yasanaproject.settings.test')

def run_functional():
    with lcd('%s/tests/functional/' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 ../../manage.py test -s --verbosity=1 --rednose '
              '--settings=yasanaproject.settings.test', )
      
def makemigration_local():
    with lcd('/home/%s/Documents/GitBase/djangobase/yasanaproject'  % env.user):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py makemigrations '
              '--settings=yasanaproject.settings.local')

def makemigration_test():
    with lcd('%s' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py makemigrations '
              '--settings=yasanaproject.settings.test')

def migrate_local():
    with lcd('%s' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py migrate '
              '--settings=yasanaproject.settings.local')

def migrate_test():
    with lcd('%s' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py migrate '
              '--settings=yasanaproject.settings.test')

def create_local_cache_table():
    with lcd('%s' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py createcachetable '
              '--settings=yasanaproject.settings.local')
        
def start_app(appname):
    with lcd('%s' % local_root_folder):
        local('/home/pophils/Documents/venv/py3.4/bin/python3.4 manage.py startapp {}'.format(appname))

    


