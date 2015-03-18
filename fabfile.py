# coding: utf-8
from fabric.api import task, env
from unipath import Path
from jetpack.helpers import Project

# Exposes other functionalities
# from jetpack import setup, deploy, db, config, django, logs
from jetpack.portal import *

# Always run fabric from the repository root dir.
Path(__file__).parent.chdir()


@task
def portal():
    env.PROJECT = Project(project='novo_portal', instance='portal')
    env.hosts = ['10.0.0.30']
    env.user = 'dgti'


@task
def portaldemo():
    env.PROJECT = Project(project='novo_portal', instance='portaldemo')
    env.hosts = ['portaldemo.ifmt.edu.br']
    env.user = 'dgti'