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

    $ sudo apt-get install postgresql-9.5 nginx git python3 python3-pip
    $ sudo pip3 install virtualenv 


## Create a folder structure:
    Assume we have a user account at /home/username
    example:

    /home/username
    └── sites
        └── SITENAME (eg. my-domain.com)
             ├── source (all the code ...)
             ├── static (where static files are served from)
             └── virtualenv (python binaries, libs)


## Clone the repo from github to source directory
    eg. $ git clone https://github.com/rbyy/survey.git /home/<USERNAME>/sites/<SITENAME>/source
    or just fetch if it is already there: $ cd <source_folder> && git fetch


## Create virtualenv and install dependencies listed in "source/requirements.txt" 
    $ virtualenv --python=python3 /home/<USERNAME>/sites/<SITENAME>/virtualenv
    $ <path_to_virtualenv>/bin/pip install -r <path_to_source>/requirements.txt


## Create Database
    
    

## Nginx Virtual Host config 

* see nginx.template.conf
* replace SITENAME with, eg, my-domain.com 


## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, my-domain.com 





## deploy remotely using a deploy script fabfile.py (from terminal):

    * install fabric: 
        $ sudo apt-get install fabric

    fab command:
        get fabfile.py from https://github.com/RbYy/survey/blob/master/deploy_tools/fabfile.py
	    eg, $ fab deploy:site=my-domain.com -H username@domain
        $ fab deploy:site=my-domain.com -H username@domain -f deploy_tools/fabfile.py

