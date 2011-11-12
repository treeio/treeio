#!/bin/bash
MYAPP=treeio
PIDFILE=/var/run/${MYAPP}_fcgi.pid
SOCKET=/tmp/${MYAPP}.fcgi
# Site settings
SETTINGS=treeio.settings
# Maximum requests for a child to service before expiring
#MAXREQ=100
# Spawning method - prefork or threaded
METHOD=prefork
# Maximum number of children to have idle
MAXSPARE=10
# Minimum number of children to have idle
MINSPARE=5
# Maximum number of children to spawn
MAXCHILDREN=100

cd "`dirname $0`"

function failure () {
  STATUS=$?;
  echo; echo "Failed $1 (exit code ${STATUS}).";
  exit ${STATUS};
}

function start_server () {
  python manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE \
    ${MAXREQ:+maxrequests=$MAXREQ} \
    ${METHOD:+method=$METHOD} \
    ${MAXSPARE:+maxspare=$MAXSPARE} \
    ${MINSPARE:+minspare=$MINSPARE} \
    ${MAXCHILDREN:+maxchildren=$MAXCHILDREN} \
    ${DAEMONISE:+damonize=True} \
    ${SETTINGS:+--settings=$SETTINGS}
  echo python manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE \
    ${MAXREQ:+maxrequests=$MAXREQ} \
    ${METHOD:+method=$METHOD} \
    ${MAXSPARE:+maxspare=$MAXSPARE} \
    ${MINSPARE:+minspare=$MINSPARE} \
    ${MAXCHILDREN:+maxchildren=$MAXCHILDREN} \
    ${DAEMONISE:+damonize=True} \
    ${SETTINGS:+--settings=$SETTINGS}
  chmod 777 $SOCKET
}

function stop_server () {
  kill `cat $PIDFILE` || failure "stopping fcgi"
  rm $PIDFILE
}

DAEMONISE=$2

case "$1" in
  start)
    echo -n "Starting fcgi: "
    [ -e $PIDFILE ] && { echo "PID file exsts."; exit; }
    start_server || failure "starting fcgi"
    echo "Done."
    ;;
  stop)
    echo -n "Stopping fcgi: "
    [ -e $PIDFILE ] || { echo "No PID file found."; exit; }
    stop_server
    echo "Done."
    ;;
  poll)
    [ -e $PIDFILE ] && exit;
    start_server || failure "starting fcgi"
    ;;
  restart)
    echo -n "Restarting fcgi: "
    [ -e $PIDFILE ] || { echo -n "No PID file found..."; }
    stop_server
    start_server || failure "restarting fcgi"
    echo "Done."
    ;;
  *)
    echo "Usage: $0 {start|stop|restart} [--daemonise]"
    ;;
esac

exit 0
