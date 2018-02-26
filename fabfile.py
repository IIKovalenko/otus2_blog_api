import os

from fabric.state import env
from fabric.api import cd, run, sudo, settings
from fabric.contrib.files import exists, upload_template


def _set_env():
    env.DOMAIN_NAME = 'otus2.ru'
    env.hosts = ['user@%s' % env.DOMAIN_NAME]
    env.BASE_PATH = '/var/www/'
    env.PROJECT_NAME = 'otus_blog'
    env.VIRTUALENV_PATH = os.path.join(
        env.BASE_PATH,
        '.virtualenvs',
        env.PROJECT_NAME
    )
    env.SYSTEM_PYTHON_PATH = '/usr/bin/python3'
    env.PROJECT_PATH = os.path.join(env.BASE_PATH, env.PROJECT_NAME)
    env.GIT_REPO_PATH = 'https://github.com/Melevir/melevir.github.io.git'
    env.UWSGI_PROCESSES = 5


def bootstrap():
    _set_env()

    install_system_packages(
        packages=[
            # python related packages
            'python3-dev',
            'python-pip',

            # nginx related packages
            'nginx',
        ]
    )
    create_folders()
    create_virtualenv()
    clone_src()
    install_requirements()
    configure_uwsgi()
    configure_nginx()
    run_management_commands()
    restart_all()


def install_system_packages(packages, do_apt_get_update=True):
    if do_apt_get_update:
        sudo('apt-get update')
    sudo('apt-get install %s' % (' '.join(packages)))


def create_folders():
    _mkdir(env.PROJECT_PATH)
    _mkdir(env.VIRTUALENV_PATH)


def _mkdir(path):
    run('mkdir -p %s' % path)


def create_virtualenv():
    run('virtualenv --python=%s %s' % (
        env.SYSTEM_PYTHON_PATH,
        env.VIRTUALENV_PATH
    ))


def clone_src():
    with cd(env.PROJECT_PATH):
        run('git clone %s' % env.GIT_REPO_PATH)


def install_requirements():
    virtualenv_python_path = os.path.join(
        env.VIRTUALENV_PATH,
        'bin',
        'python',
    )
    run('%s -m pip install -r requirements.txt' % virtualenv_python_path)


def configure_uwsgi():
    _upload_template(
        'uwsgi.ini',
        '/etc/uwsgi/apps-available/%s.ini' % env.PROJECT_NAME,
    )


def configure_nginx():
    _upload_template(
        'nginx.conf',
        '/etc/nginx/apps-available/%s.conf' % env.PROJECT_NAME,
    )


def _upload_template(template_name, dest_path):
    upload_template(
        os.path.join('deploy_templates', template_name),
        dest_path,
        context={
            'uwsgi_processes_amount': env.UWSGI_PROCESSES,
            'domain_name': env.DOMAIN_NAME,
            'project_name': env.PROJECT_NAME,
        },
    )


def run_management_commands():
    pass


def restart_all(services=None):
    services = services or ['nginx', 'uwsgi']
    for service in services:
        sudo('service %s restart' % service)
