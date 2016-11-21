import random
import subprocess

from fabric.api import env, local, run
from fabric.contrib.files import append, exists, sed

env.use_ssh_config = True
REPO_URL = 'https://github.com/btcorp/basket-together-webserver-django.git'   # git repo url setting
PROJECT_NAME = 'basket_together'
SERVER_TYPE = 'web_server'


def deploy():
    site_folder = '/home/ubuntu/home/{0}/sites/{1}'.format(env.user, PROJECT_NAME)
    source_folder = site_folder + '/' + SERVER_TYPE

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _chown_database_to_ubuntu(source_folder)
    _update_database(source_folder)
    _chown_database_to_wwwdata(source_folder)
    _copy_secret_key(site_folder)


def _create_directory_structure_if_necessary(site_folder):
    print('=========================Create directory according to project structure=============================')
    for subfolder in ('database', SERVER_TYPE, 'static', 'virtualenv', 'media'):
        run('mkdir -p {0}/{1}'.format(site_folder, subfolder))


def _get_latest_source(source_folder):
    print('==========================Deploy latest source in server(Fetch or Clone)==============================')
    if exists(source_folder + '/.git'):
        print(1)
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))

    print(2)
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd {0} && git reset --hard {1}'.format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    print('==========================Set settings.py file=========================================================')
    settings_path = source_folder + '/' + PROJECT_NAME + '/settings/common.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(
        settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["{0}"]'.format('*')
    )

    secret_key_file = source_folder + '/' + PROJECT_NAME + '/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "{0}"'.format(key))
    append(settings_path, '\nfrom ..secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    print('==========================set virtualenv and install requirements.txt===============================')
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 {0}'.format(virtualenv_folder))
    run('{0}/bin/pip3 install -r {1}/requirements.txt'.format(virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    print('==========================Collect static file!!!!!====================================================')
    run('cd {0} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(source_folder))


def _chown_database_to_ubuntu(source_folder):
    print('==========================chown database directory & file============================================')
    run('cd {0}/../ && sudo chown -R ubuntu:ubuntu database '.format(source_folder))


def _update_database(source_folder):
    print('==========================Execute migrate!!!!!!!=====================================================')
    run('cd {0} && ../virtualenv/bin/python3 manage.py migrate --noinput'.format(source_folder))


def _chown_database_to_wwwdata(source_folder):
    print('==========================chown database directory & file============================================')
    run('cd {0}/../ && sudo chown -R www-data:www-data database'.format(source_folder))


def _copy_secret_key(site_folder):
    print('==========================set secret_key.json=========================================================')
    pem_path = '/Users/Jin-TaeWoo/.ssh/basket_together.pem'
    subprocess.call('scp -i '+pem_path+' ../secret_key.json ubuntu@52.78.69.17:'+site_folder, shell=True)
