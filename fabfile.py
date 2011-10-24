from fabric.api import *

env.path = '/var/praekelt/ummeli'

def qa():
    env.hosts = ['ubuntu@cloud.praekeltfoundation.org']

def production():
    env.hosts = ['ubuntu@ummeli.praekeltfoundation.org']

def deploy():
    with cd(env.path):
        run('git pull')
        run('ve/bin/supervisorctl -c config/supervisord.conf restart all')
