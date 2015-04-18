#!/usr/bin/env bash
# this was tested on centos, installing oracle and/or cx_Oracle on debian/ubuntu is theoretically possible, but I gave up on that
sudo yum install libaio bc flex
export DB=oracle

# fake free so we can install oracle
sudo mv /usr/bin/free /usr/bin/free.original
sudo tee /usr/bin/free <<EOF > /dev/null
#!/bin/sh
cat <<__eof
             total       used       free     shared    buffers     cached
Mem:       1048576     327264     721312          0          0          0
-/+ buffers/cache:     327264     721312
Swap:      2000000          0    2000000
__eof
exit
EOF

sudo chmod 755 /usr/bin/free

wget -q http://dl.nucleoos.com.br/oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm
wget -q http://dl.nucleoos.com.br/oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm
wget -q http://dl.nucleoos.com.br/oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm
wget -q http://dl.nucleoos.com.br/oracle-xe-11.2.0-1.0.x86_64.rpm
sudo rpm -ivh oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm
sudo rpm -ivh oracle-xe-11.2.0-1.0.x86_64.rpm

export ORACLE_VERSION="12.1"
export ORACLE_HOME="/usr/lib/oracle/$ORACLE_VERSION/client64/"
#export PATH=$PATH:"$ORACLE_HOME/bin"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$ORACLE_HOME/lib"
pip install cx_Oracle

sudo cp /usr/bin/free.original /usr/bin/free