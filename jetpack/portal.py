# coding: utf-8
from fabric.api import task, env, require, cd
from fabric.operations import run, sudo
from jetpack.helpers import RunAsAdmin


@task
def pull():
    require('PROJECT')

    with cd('~/portal'):
        run('git pull')


@task
def update():
    require('PROJECT')

    with cd('~/portal'):
        run('git pull')

    sudo('supervisorctl restart portal')


@task
def restart_services():
    require('PROJECT')

    sudo('/etc/init.d/nginx restart')
    sudo('supervisorctl restart portal')


@task
def log_django(lines=50):
    require('PROJECT')

    run('tail --lines=%s /home/dgti/portal/logs/django.log' % lines)