from fabric.api import *

env.path = '/var/praekelt/ummeli'

def qa():
    env.hosts = ['ubuntu@cloud.praekeltfoundation.org']

def production():
    env.hosts = ['ubuntu@app1.praekeltfoundation.org']

def deploy():
    with cd(env.path):
        run('git pull')
        run('kill -HUP `cat tmp/pids/gunicorn*.pid`')
