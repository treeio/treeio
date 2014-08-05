[![Build Status](https://secure.travis-ci.org/treeio/treeio.png?branch=master)](http://travis-ci.org/treeio/treeio)

==========================
Tree.io Business Management Platform
==========================

*Due to lack of time I can no longer maintain Tree. If you are interested in working on it get in touch*


Apache
======

For those installing with Apache check out this tutorial:
http://www.makeyouadmin.com/2014/04/install-treeio-on-ubuntu-with-apache-mysql.html#.U1KlJKaINQI

Amazon AMI
==========

There is also a pre-built micro [Amazon AMI Image](https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-6af22f03&source=tree.io) available which will run on [Amazon's Free Usage Tier](http://aws.amazon.com/free/) for 1 year.

There is also now a Docker Container and bootstrap script to run treeio and a micro PostgreSQL instance inside Docker:


Docker Container Installation
=============================

07/2013: I have created a Docker container and a shell script to create a postgresql instance and a dynamically configured treeio instance.

To use this you only need to [install Docker](http://www.docker.io/gettingstarted/) and run this script: https://gist.github.com/funkotron/6025664
 

License
=======

Tree.io is licensed under the MIT License. See the `LICENSE` file.

Tree.io comes with no warranty, Tree.io Ltd. can accept no responsibility for any damages, losses etc.


Installation on Ubuntu or Debian with MySQL
================================

Although you can install on most any UNIX system very easily, debian based distros are easier due to their package management.

You can also install on Max OSX or with other databases aside from MySQL very easily.


Install any dependencies
------------------------

1.  Update your local cache `sudo apt-get update`
1.  Upgrade your system `sudo apt-get upgrade` (Recommended but optional)
1.  `sudo apt-get install python build-essential python-dev`
1.  `sudo apt-get build-dep python-lxml python-imaging`
1.  `sudo apt-get install git python-flup python-pip python-virtualenv`


Install services (In Production)
------------------------

1.  Install database `sudo apt-get install mysql-server` (Aside from MySQL you can also use Postgre, SQLite or OracleDB)
1.  Install web server `sudo apt-get install nginx` 

Alternatively you can use Apache, see this [community post](http://tree.io/en/community/questions/186/treeio-with-wsgi-for-apache-deploy) for an example configuration and read this [GitHub issue](https://github.com/treeio/treeio/issues/98) which clarifies things further.

Create a clone of this repository
------------------------

1.  Make a directory for treeio and go inside `mkdir treeio && cd treeio`
1.  Clone the repo by running: `git clone https://github.com/treeio/treeio.git`
2.  Go into this directory `cd treeio` (The directory structure should be `treeio/treeio/<project files>`)
2.  Create a virtual environment to keep your packages & versions thereof separate from the rest of the system `virtualenv venv`
3.  Activate the virtual environment `source ./venv/bin/activate`
4.  Install system prerequisites for image processing module according to [instuctions](https://github.com/python-imaging/Pillow#platform-specific-instructions)
1.  Install dependencies: `pip install -r requirements.pip`
2.  ```DJANGO_DIR=`python -c "import django; import os; print os.path.dirname(django.__file__)"` ```
1.  Run the patch: `python related_fields_patch.py $DJANGO_DIR`


Install the database (Example showing MySQL)
------------------------

    $ mysql -u treeio -ptreeio
           > create database treeio;
           > grant all privileges on treeio.* to treeio@localhost identified by 'treeio';
           > \q

1.  Install mysql, client libraries and python driver: `sudo apt-get install mysql-server mysql libmysqlclient-dev python-mysqldb`
1.  Install your database: `python manage.py installdb`
1.  Setup initial data: `python manage.py loaddata data.json` or if using mysql: `mysql -u treeio -ptreeio treeio < sql/mysql-treeio-current.sql`

Test install 
------------------------

1.  Run the built-in Django server `python manage.py runserver`
1.  In your browser go to `http://localhost:8000`
1.  Log in using username: `admin` and password: `admin`
1.  Profit!

Next steps (In Production)
------------------------

* Configure nginx
* Set up a mailserver
* Set up a domain to point to your new server (Set A Record)


Support
=======

Commercial installation and support is available from Tree.io Ltd, London, UK.
Please see http://www.tree.io/ or contact info@tree.io for more details.

Acknowledgements
================

* Spanish translation contributed to by @sytabaresa
* Greek translation contributed by Nick Apostolakis http://nick.oncrete.gr
* Brasilian Portugese translation contributed by Davi Ribeiro
* Simple Chinese translation contributed by @sunliwen
* French translation contributed by morago.com
* An [achievements addon](https://github.com/pascalmouret/treeio-achievements) is available courtesy of Pascal Mouret as shown in our [Djangocon Europe video](http://klewel.com/conferences/djangocon-2012/index.php?talkID=15).


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/treeio/treeio/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

