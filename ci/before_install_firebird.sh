sudo apt-get install -qq firebird2.5-super firebird2.5-dev

# Configure Firebird server
# See: Non-interactive setup for travis-ci.org
# http://tech.groups.yahoo.com/group/firebird-support/message/120883
#sudo dpkg-reconfigure -f noninteractive firebird2.5-super
sudo sed /ENABLE_FIREBIRD_SERVER=/s/no/yes/ -i /etc/default/firebird2.5
cat /etc/default/firebird2.5 | grep ENABLE_FIREBIRD_SERVER
sudo service firebird2.5-super start

pip install django-firebird