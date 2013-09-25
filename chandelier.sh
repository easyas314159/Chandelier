#! /bin/bash
# Copyright (c) 1996-2012 My Company.
# All rights reserved.
#
# Author: Bob Bobson, 2012
#
# Please send feedback to bob@bob.com
#
# /etc/init.d/testdaemon
#
### BEGIN INIT INFO
# Provides: chandelier
# Required-Start: $all
# Should-Start: 
# Required-Stop: 
# Should-Stop:
# Default-Start:  2 3 4 5
# Default-Stop:   0 1 6
# Short-Description: Test daemon process
# Description:    Runs up the test daemon process
### END INIT INFO

# Activate the python virtual environment
#    . /path_to_virtualenv/activate

DAEMON=/usr/share/chandelier/chandelier.py

case "$1" in
  start)
    echo "Starting server"
    # Start the daemon 
    python $DAEMON start
    ;;
  stop)
    echo "Stopping server"
    # Stop the daemon
    python $DAEMON stop
    ;;
  restart)
    echo "Restarting server"
    python $DAEMON restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/chandelier {start|stop|restart}"
    exit 1
    ;;
esac

exit 0