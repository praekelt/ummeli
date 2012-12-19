from fabric.api import *

env.path = '/var/praekelt/ummeli'

def qa(user='ubuntu'):
    env.user = user
    env.hosts = ['%s@cloud.praekeltfoundation.org' % user]

def production(user='ubuntu'):
    env.user = user
    env.hosts = ['%s@cloud.praekeltfoundation.org' % user]

def push():
    run('sudo su ubuntu' % env)
    with cd(env.path):
        run('git pull')

def static():
    run('sudo su ubuntu' % env)
    with cd(env.path):
        run('ve/bin/python %(path)s/ummeli/manage.py collectstatic --noinput' % env)

def migrate(app='ummeli.base'):
    run('sudo su ubuntu' % env)
    with cd(env.path):
        env.app = app
        run('ve/bin/python %(path)s/ummeli/manage.py migrate %(app)s' % env)


def deploy():
    run('sudo su ubuntu' % env)
    with cd(env.path):
        run('git pull')
        run('kill -HUP `cat tmp/pids/u_gunicorn_*.pid`')
        run('sudo supervisorctl restart ummeli:u_celery' % env)

def reload():
    run('sudo su ubuntu' % env)
    with cd(env.path):
        run('git pull')
        run('kill -HUP `cat tmp/pids/u_gunicorn_*.pid`')

def restart(app=''):
    env.app = app
    run('sudo supervisorctl restart ummeli:%(app)s' % env)
