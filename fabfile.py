from fabric.api import *

env.path = '/var/praekelt/ummeli'

def qa():
    env.hosts = ['ubuntu@cloud.praekeltfoundation.org']

def production():
    env.hosts = ['ubuntu@app1.praekeltfoundation.org']

def push():
    with cd(env.path):
        run('git pull')

def static():
    with cd(env.path):
        run('ve/bin/python %(path)s/ummeli/manage.py collectstatic --noinput' % env)

def migrate(app='ummeli.base'):
    with cd(env.path):
        env.app = app
        run('ve/bin/python %(path)s/ummeli/manage.py migrate %(app)s' % env)


def deploy():
    with cd(env.path):
        run('git pull')
        run('kill -HUP `cat tmp/pids/u_gunicorn_*.pid`')
        run('sudo supervisorctl restart ummeli:u_celery' % env)

def reload():
    with cd(env.path):
        run('git pull')
        run('kill -HUP `cat tmp/pids/u_gunicorn_*.pid`')

def restart(app=''):
    env.app = app
    with cd(env.path):
        run('sudo supervisorctl restart ummeli:%(app)s' % env)
