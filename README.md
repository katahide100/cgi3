# cgi3

### perlインストール
yum -y install perl perl-CGI
ln -s /usr/bin/perl /usr/local/bin/perl

### 必要なモジュールインストール
perl -MCPAN -e shell

install Net::SSLeay LWP::UserAgent HTTP::Request::Common JSON

### apache設定
vi /etc/httpd/conf.d/cgi3.conf

```
<Directory "/var/www/html">
    Options +ExecCGI
    AddHandler cgi-script .cgi .pl
</Directory>
```

### 初期設定
chmod 777 /var/www/html/cgi3

cd /var/www/html/cgi3

chmod 777 playerdata

touch popular.dat

chmod 777 popular.dat

chmod 777 room

chmod 777 chat/data

touch chat/data/data.log

chmod 777 chat/data/data.log

touch member.dat

chmod 777 member.dat

cp cust.default.cgi cust.cgi

上記実施後、cust.cgiを開き、必要な箇所を変更する


