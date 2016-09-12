
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo, prompt
import random
from getpass import getpass


REPO_URL = 'https://github.com/rbyy/survey.git'

PG_DB_SETTINGS = """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%s',
        'USER': '%s',
        'PASSWORD': '%s',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""


def deploy(site=None):
    if not site:
        site = env.host
    site_folder = '/home/%s/sites/%s' % (env.user, site)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    PG_DB_SETTINGS = _create_pg_database()
    _get_latest_source(source_folder)
    _update_settings(source_folder, site, PG_DB_SETTINGS)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    apt_get("nginx")
    set_nginx(site_folder, site)
    set_gunicorn(site_folder, site)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def apt_get(package):
    sudo("apt-get -y install %s" % (package))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name, PG_DB_SETTINGS):
    settings_path = source_folder + '/pollproject/settings.py'
    requirements_path = source_folder + '/requirements.txt'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s", "pi"]' % (site_name,)
        )
    secret_key_file = source_folder + '/pollproject/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')
    append(settings_path, '\n%s' % (PG_DB_SETTINGS))
    STATIC_PATH = 'STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(PROJECT_ROOT)), "static")'
    sed(settings_path, 'STATIC_ROOT = os.+$', STATIC_PATH)
    append(requirements_path, 'psycopg2==2.6.2\ngunicorn==19.6.0')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))


def _create_pg_database():
    """Creates role and database"""
    db_user = get_user()
    db_pass = get_pass()
    db_db = get_db()
    pg_db_set = PG_DB_SETTINGS % (db_db, db_user, db_pass)
    sudo("systemctl enable postgresql")
    sudo('psql -c "CREATE USER %s WITH PASSWORD E\'%s\'"' % (db_user, db_pass), user='postgres', warn_only=True)
    sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"' % (db_db, db_user), user='postgres', warn_only=True)
    sudo('psql -c "ALTER ROLE %s WITH CREATEDB"' % (db_user), user='postgres', warn_only=True)
    return pg_db_set


def get_user():
    return prompt('choose postgres user:')


def get_pass():
    pass_1st = getpass('choose postgres password: ')
    pass_2nd = getpass('repeat postgres password: ')
    if pass_1st == pass_2nd:
        return pass_2nd
    else:

        get_pass()


def get_db():
    return prompt("pg database name: ")


def set_nginx(site_folder, site_name):
    nginx_available_folder = '/etc/nginx/sites-available'
    nginx_enabled_folder = '/etc/nginx/sites-enabled'
    nginx_ln_enabled = "%s/%s" % (nginx_enabled_folder, site_name)
    deploy_folder = "%s/source/deploy_tools" % (site_folder)
    nginx_site = "%s/nginx.site.template" % (deploy_folder)
    nginx_site_renamed = "%s/%s" % (deploy_folder, site_name)
    if not exists(nginx_site_renamed):
        run("mv %s %s" % (nginx_site, nginx_site_renamed))
        sed(nginx_site_renamed,
            'server_name.+$',
            'server_name %s;' % (site_name))
        sed(nginx_site_renamed,
            'alias.+',
            'alias %s/static;' % (site_folder))
        sed(nginx_site_renamed,
            'unix.+$',
            'unix:%s/myproject.sock;' % (site_folder))

    sudo("cp %s %s/%s" % (nginx_site_renamed, nginx_available_folder, site_name))
    if exists(nginx_ln_enabled):
        sudo("rm %s" % (nginx_ln_enabled))
    sudo("ln -s %s/%s %s" % (nginx_available_folder,
                             site_name,
                             nginx_ln_enabled
                             )
         )
    sudo("service nginx reload")


def set_gunicorn(site_folder, site_name):
    sysd_service = "/etc/systemd/system/gunicorn.{0}.service".format(site_name)
    gunic_template = "{0}/source/deploy_tools/gunicorn.service.template".format(site_folder)
    gunic_renamed = "{0}/source/deploy_tools/gunicorn.{1}.service".format(site_folder, site_name)
    if not exists(gunic_renamed):
        run("mv {0} {1}".format(gunic_template, gunic_renamed))
        sed(gunic_renamed, "User.+$", "User={0}".format(env.user))
        sed(gunic_renamed, "Group.+$", "Group={0}".format(env.user))
        sed(gunic_renamed, "WorkingD.+$", "WorkingDirectory={0}/source".format(site_folder))
        sed(gunic_renamed,
            "ExecSta.+$",
            "ExecStart={0}/virtualenv/bin/gunicorn \
 --workers 3 --bind unix:{0}/myproject.sock \
 pollproject.wsgi:application".format(site_folder))
    sudo("cp {0} {1}".format(gunic_renamed, sysd_service))
    sudo("systemctl stop gunicorn.{0}.service".format(site_name))
    sudo("systemctl enable gunicorn.{0}.service".format(site_name))
    sudo("systemctl start gunicorn.{0}.service".format(site_name))
