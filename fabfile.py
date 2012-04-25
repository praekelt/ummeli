from fabric.api import *

env.path = '/var/praekelt/ummeli'

def qa():
    env.supervisord_file = 'supervisord.staging.conf'
    env.hosts = ['ubuntu@cloud.praekeltfoundation.org']

def production():
    env.supervisord_file = 'supervisord.production.conf'
    env.hosts = ['ubuntu@app1.praekeltfoundation.org']

def push():
    with cd(env.path):
        run('git pull')

def deploy():
    with cd(env.path):
        run('git pull')
        run('kill -HUP `cat tmp/pids/gunicorn*.pid`')
        run('supervisorctl -c config/%(supervisord_file)s restart celery' % env)

def reload():
    with cd(env.path):
        run('source ve/bin/activate && kill -HUP `cat tmp/pids/*gunicorn*.pid`')

def restart(app='all'):
    env.app = app
    with cd(env.path):
        run('supervisorctl -c config/%(supervisord_file)s restart %(app)s' % env)