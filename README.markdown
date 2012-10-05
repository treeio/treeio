[![Build Status](https://secure.travis-ci.org/treeio/treeio.png?branch=master)](http://travis-ci.org/treeio/treeio)

==========================
Tree.io Business Management Platform
==========================

Tree.io is a powerful business management platform with tons of great features including integrated Project Management, Help Desk (support ticketing) and CRM modules. For a full list of features please see http://www.tree.io

For FAQ see the Tree.io community site http://www.tree.io/community/

There is also a pre-built micro [Amazon AMI Image](https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-6af22f03&source=tree.io) available which will run on [Amazon's Free Usage Tier](http://aws.amazon.com/free/) for 1 year.

License
=======

Tree.io is licensed under the MIT License. See the `LICENSE` file.


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
1.  `sudo apt-get install git python-flup python-pip`


Install services (In Production)
------------------------

1.  Install database `sudo apt-get install mysql-server` (Aside from MySQL you can also use Postgre, SQLite or OracleDB)
1.  Install web server `sudo apt-get install nginx` 

Alternatively you can use Apache, see this [community post](http://tree.io/en/community/questions/186/treeio-with-wsgi-for-apache-deploy) for an example configuration.

Create a clone of this repository
------------------------

1.  Clone the repo by running: `git clone https://github.com/treeio/treeio.git`
1.  Install dependencies: `pip install -r requirements.pip`
1.  Run the patch: `python related_fields_patch.py`


Install the database (Example showing MySQL)
------------------------

    $ mysql -u username -p
           > create database database_name;
           > grant all privileges on database_name.* to some_user@localhost identified by 'some_password';
           > \q

1.  Install your database `python manage.py installdb`
1.  Setup initial data `python manage.py loaddata data.json`

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
Our community support forum is the first stop for any questions http://www.tree.io/community
Please see http://www.tree.io/ or contact info@tree.io for more details.

Acknowledgements
================

* Greek translation contributed by Nick Apostolakis http://nick.oncrete.gr
* Brasilian translation contributed by Davi Ribeiro
* Simple Chinese translation contributed by @sunliwen
* French translation contributed by morago.com
