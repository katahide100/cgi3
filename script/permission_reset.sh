#!/bin/sh
cd /var/www/html/cgi3/
chmod 777 setting.txt action.pl deck.cgi series.lib card1.txt card2.txt psychic.txt psychic_list.html EditSymbol/kunsyo.csv cust.cgi data/* etc/help.html syu.txt taikai/*.txt taikai/*.csv

chown apache:apache setting.txt action.pl deck.cgi series.lib card1.txt card2.txt psychic.txt psychic_list.html EditSymbol/kunsyo.csv cust.cgi data/* etc/help.html syu.txt taikai/*.txt taikai/*.csv

chmod 777 /var/www/duel_node/script/active_check.sh
