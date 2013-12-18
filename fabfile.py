from fabric.api import *

env.path = '/var/praekelt/ummeli'
env.sudo_user = 'ubuntu'
env.shell = '/bin/bash -c'

def qa(ssh_user=None):
    if not ssh_user:
        print 'You must provide your login username.'
        print 'format: fab <env>:<username> <command> e.g fab qa:miltontony push'
        raise RuntimeError('Username required')

    env.hosts = ['%s@qa-ummeli.za.prk-host.net' % ssh_user]

def production(ssh_user=None):
    if not ssh_user:
        print 'You must provide your login username.'
        print 'format: fab <env>:<username> <command> e.g fab production:ubuntu push'
        raise RuntimeError('Username required')

    env.hosts = ['%s@app1.praekeltfoundation.org' % ssh_user]

def push():
    with cd(env.path):
        sudo('git pull')

def static():
    with cd(env.path):
        sudo('ve/bin/python %(path)s/ummeli/manage.py collectstatic --noinput' % env, user=env.user)

def migrate(app='ummeli.base'):
    with cd(env.path):
        env.app = app
        sudo('ve/bin/python %(path)s/ummeli/manage.py migrate %(app)s' % env, user=env.user)

def deploy():
    with cd(env.path):
        sudo('git pull')
        sudo('kill -HUP `cat tmp/pids/u_gunicorn_*.pid`')
        sudo('sudo supervisorctl restart ummeli:u_celery')

def reload():
    with cd(env.path):
        sudo('git pull')
        sudo('kill -HUP `cat tmp/pids/u_gunicorn_*.pid`')

def restart(app=''):
    env.app = app
    sudo('sudo supervisorctl restart ummeli:%(app)s' % env)
