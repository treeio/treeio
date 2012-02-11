==========================
Tree.io Business Management Platform
==========================

Tree.io is a powerful business management platform with tons of great features including integrated Project Management, Help Desk (support ticketing) and CRM modules. For a full list of features please see http://www.tree.io

For FAQ see the Tree.io community site http://www.tree.io/community/


License
=======

Tree.io is licensed under the Creative Commons Attribution-NonCommercial 3.0 License.

If you wish to re-sell or charge for install you must contact us for a Reseller License. 

For more details see LICENSE.

Tree.io cannot accept any responsibility for damage or losses caused by use of this software. Use at your own risk!


Installation on Ubuntu or Debian with MySQL
================================

Although you can install on most any UNIX system very easily, debian based distros are easier due to their package management.

You can also install on Max OSX or with other databases aside from MySQL very easily.


Install any dependencies
------------------------

1.  Update your local cache `sudo apt-get update`
1.  Upgrade your system `sudo apt-get upgrade` (Recommended but optional)
1.  `sudo apt-get install python build-essential python-dev`
1.  `sudo apt-get build-dep python-lxml python-imaging
1.  `sudo apt-get install git python-flup python-pip`


Install services (In Production)
------------------------

1.  Install database `sudo apt-get install mysql-server` (Aside from MySQL you can also use Postgre, SQLite or OracleDB)
1.  Install web server `sudo apt-get install nginx` (You may also use Apache following instructions for setting up Django with Apache)

Create a fork and clone this repository
------------------------

1.  Fork this repository by clicking Fork in the top toolbar (Forking will make it easier to contribute as you commit changes and have them merged into this Tree.io master repository)
1.  Create a folder called treeio `mkdir treeio && cd treeio` (**Tree.io must be run inside another folder called treeio to work correctly**)
1.  Clone the repo by running: `git clone git@github.com:your_git/treeio.git`
1.  Update your virtual environment `python manage.py update_ve`
1.  Perform the patch `./bin/patch`

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
