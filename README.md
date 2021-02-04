# cgi3

yum -y install perl perl-CGI

vi /etc/httpd/conf.d/cgi3.conf

<Directory "/var/www/html">
    Options +ExecCGI
    AddHandler cgi-script .cgi .pl
</Directory>

ln -s /usr/bin/perl /usr/local/bin/perl

cp cust.default.cgi cust.cgi

perl -MCPAN -e shell
install Net::SSLeay LWP::UserAgent HTTP::Request::Common JSON

cd /var/www/html/cgi3
chmod 777 playerdata
touch popular.dat
chmod 777 popular.dat
chmod 777 room
