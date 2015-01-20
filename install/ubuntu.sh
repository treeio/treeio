#!/bin/sh

#apt-get install build-essential python-dev
#apt-get build-dep python-lxml python-imaging
#apt-get install git python-flup python-pip python-virtualenv

sudo mkdir /usr/local/treeio
sudo chown $USER /usr/local/treeio
cd /usr/local/treeio

sudo apt-get install python-virtualenv python-pip python-dev unzip nginx -y
# libs for pillow
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk -y

virtualenv env
source env/bin/activate
pip install -U setuptools pip
pip install uwsgi

wget https://github.com/tovmeod/treeio/archive/master.zip
unzip master.zip
mv treeio-master/ treeio
# to update:
# rsync -a treeio-master/ treeio
# rm -rf treeio-master/
rm master.zip

pip install -r treeio/requirements.pip

# see http://www.postgresql.org/download/linux/ubuntu/
# this should work for lucid (10.04), precise (12.04), trusty (14.04) and utopic (14.10)
echo "deb http://apt.postgresql.org/pub/repos/apt/ "$(lsb_release -a | grep Codename | awk -F' ' '{print $2}')"-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.4 -y
sudo -u postgres createuser --pwprompt treeio
sudo -u postgres createdb treeio --owner=treeio

cd treeio
python manage.py installdb

add uwsgi to upstart
sudo ln -s /usr/local/treeio/treeio/install/upstart.conf  /etc/init/treeio.conf
sudo initctl reload-configuration
sudo start treeio
sudo ln -s /usr/local/treeio/treeio/install/nginx.conf  /etc/nginx/sites-enabled/treeio
sudo rm  /etc/nginx/sites-enabled/default
sudo nginx -s reload