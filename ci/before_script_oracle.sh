. /usr/lib/oracle/xe/app/oracle/product/10.2.0/server/bin/oracle_env.sh

# create user for testing
echo "CREATE USER treeio IDENTIFIED BY treeio;" | \
sqlplus -S -L sys/admin AS SYSDBA

echo "grant connect, resource to treeio;" | \
sqlplus -S -L sys/admin AS SYSDBA

echo "grant create session, alter any procedure to treeio;" | \
sqlplus -S -L sys/admin AS SYSDBA

# to enable xa recovery, see: https://community.oracle.com/thread/378954
echo "grant select on sys.dba_pending_transactions to treeio;" | \
sqlplus -S -L sys/admin AS SYSDBA
echo "grant select on sys.pending_trans$ to treeio;" | \
sqlplus -S -L sys/admin AS SYSDBA
echo "grant select on sys.dba_2pc_pending to treeio;" | \
sqlplus -S -L sys/admin AS SYSDBA
echo "grant execute on sys.dbms_system to treeio;" | \
sqlplus -S -L sys/admin AS SYSDBA