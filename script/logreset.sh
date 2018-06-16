#!/bin/sh
cd /var/www/html/cgi3/logs
rm -f request.log
touch request.log
chmod 777 request.log

cd /var/www/html/cgi3_test/logs
rm -f request.log
touch request.log
chmod 777 request.log
