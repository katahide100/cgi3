#!/bin/sh

find /var/www/html/cgi3/room_old/ -mtime 30 -exec rm -f {} \;
