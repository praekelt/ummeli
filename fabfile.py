from fabric.api import *

env.path = '/var/praekelt/ummeli'

def qa():
    env.supervisord_file = 'supervisord.staging.conf'
    env.hosts = ['ubuntu@cloud.praekeltfoundation.org']

def production():
    env.supervisord_file = 'supervisord.production.conf'
    env.hosts = ['ubuntu@app1.praekeltfoundation.org']

def deploy():
    with cd(env.path):
        run('git pull')
        run('kill -HUP `cat tmp/pids/gunicorn*.pid`')
        run('supervisorctl -c config/%(supervisord_file)s restart celery' % env)
