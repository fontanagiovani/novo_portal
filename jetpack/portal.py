# coding: utf-8
from fabric.api import task, env, require, cd
from fabric.operations import run, sudo, local
# from jetpack.helpers import RunAsAdmin


@task
def merge(from_branch='develop', into_branch='master'):
    local('git checkout %s' % into_branch)
    local('git pull')
    local('git merge --no-ff %s' % from_branch)
    local('git push origin %s' % into_branch)
    local('git checkout %s' % from_branch)


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
        run('python manage.py migrate')

    sudo('supervisorctl restart portal')


@task
def migrate():
    require('PROJECT')

    with cd('~/portal'):
        run('python manage.py migrate')

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


@task
def log_error(lines=50):
    require('PROJECT')

    run('tail --lines=%s /home/dgti/portal/logs/error.log' % lines)
