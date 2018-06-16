#!/bin/sh
cd /var/www/html/cgi3/
chmod 777 deck.cgi series.lib card1.txt card2.txt psychic.txt psychic_list.html EditSymbol/kunsyo.csv cust.cgi data/* etc/help.html syu.txt

chown apache:apache deck.cgi series.lib card1.txt card2.txt psychic.txt psychic_list.html EditSymbol/kunsyo.csv cust.cgi data/* etc/help.html syu.txt
