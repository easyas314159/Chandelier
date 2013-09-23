#! /bin/bash
# /etc/init.d/chandelier
#
### BEGIN INIT INFO
# Provides: chandelier
# Required-Start: 
# Should-Start: 
# Required-Stop: 
# Should-Stop:
# Default-Start:  3 5
# Default-Stop:   0 1 2 6
# Short-Description: Chandelier daemon process
# Description: 
### END INIT INFO

path=/usr/share/chandelier/chandelier.py

case "$1" in
  start)
    echo "Starting chandelier client"
    # Start the daemon 
    python "$path" start
    ;;
  stop)
    echo "Stopping chandelier client"
    # Stop the daemon
    python "$path" stop
    ;;
  restart)
    echo "Restarting chandelier client"
    python "$path" restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/chandelier {start|stop|restart}"
    exit 1
    ;;
esac

exit 0