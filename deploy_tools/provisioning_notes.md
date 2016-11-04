Provisioning a new site
    - this is how I usually do it
=======================

## Required packages:

* nginx
* postgresql
* Python 3
* Git
* pip
* virtualenv

eg, on Debian, Ubuntu:
    (some of these dependencies are required by specific libs used by this app.)
    
    $ sudo apt-get install postgresql libtiff5-dev zlib1g-dev libjpeg8-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev \
    python-tk libpq-dev nginx git python3 python3-dev python3-setuptools python3-pip
    $ sudo pip3 install virtualenv 


## Create a folder structure:
    Assume we have a user account at /home/<USERNAME>
    example:

    /home/<USERNAME>
    └── sites
        └── SITENAME (eg. my-domain.com)
             ├── source (all the code ...)
             ├── static (where static files are served from)
             └── virtualenv (python binaries, libs)


## Clone the repo from github to source directory
    eg. $ git clone https://github.com/rbyy/survey.git /home/<USERNAME>/sites/<SITENAME>/source
    or just fetch if it is already there: $ cd <path_to_source> && git fetch


## Create virtualenv and install dependencies listed in "source/requirements.txt" 
    $ virtualenv --python=python3 /home/<USERNAME>/sites/<SITENAME>/virtualenv
    $ <path_to_virtualenv>/bin/pip install -r <path_to_source>/requirements.txt


## Create Database
    $ sudo systemctl enable postgresql
    $ sudo psql -c "CREATE USER <database_user> WITH PASSWORD <database_password>
    $ sudo psql -c "CREATE DATABASE <database_name> WITH OWNER <database_user>
    $ sudo psql -c "ALTER ROLE <database_user> WITH CREATEDB


## Update application settings
    * Appent the following to the end of <path_to_source>/pollproject/setings.py

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': '<database_name>',
                'USER': '<database_user>',
                'PASSWORD': '<database_password>',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }

    # In this case the credentials are hardcoded into settings.py which is not supposed to be an ideal solution. Maybe consider environment variables or something.


## Collect static files
    Copy static files from all parts of the application to 
    eg. ... /sites/<SITENAME>/static  to be served directly by Nginx.
        $ cd <path_to_source> && ../virtualenv/bin/python3 manage.py migrate --noinput


## Nginx Virtual Host config 

    * see nginx.template.conf (in <path_to_source>/deploy_tools)
    * update paths; replace <SITENAME> with, eg, my-domain.com 
    * copy it to /etc/nginx/sites-available
    * rename it to <SITENAME>

    * make sym link of it to /etc/nginx/sites-enabled:
        $ sudo ln -s /etc/nginx/sites-available/<SITENAME> /etc/nginx/sites-enabled

    *start nginx:
        $ sudo service nginx reload



## Upstart Job

    * see gunicorn-upstart.template.conf (in <path_to_source>/deploy_tools)
    * update paths, user, group, path to wsgi (project.wsgi to pollproject.wsgi);
    * replace <SITENAME> with, eg, my-domain.com
    * copy it to /etc/systemd/system
    * rename it to gunicorn.<SITENAME>.service

    * start gunicorn (python server)
        $ sudo systemctl enable gunicorn.<SITENAME>.service
        $ sudo systemctl start gunicorn.<SITENAME>.service



## deploy remotely using a deploy script fabfile.py (from terminal):
The steps listed above are wrapped in a script which uses "fabric" and connects to server via ssh. Feel free to tweak it to suit your needs.

    * install fabric locally (requires python 2!): 
        $ sudo apt-get install fabric

    fab command:
        get fabfile.py from https://github.com/RbYy/survey/blob/master/deploy_tools/fabfile.py
	    eg, $ fab deploy:site=my-domain.com -H username@domain
        $ fab deploy:site=my-domain.com -H username@domain -f deploy_tools/fabfile.py

Tested on Ubuntu 16.04 and OSMC (Debian 8.6 on Raspberry Pi 3)
Good luck!