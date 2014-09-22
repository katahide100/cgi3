#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DAY COUNTER-EX : conv.cgi - 2011/10/07
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────
# [ Ver.3 から Ver.4 へログを変換するためのプログラムです ]
# [ ログ変換後は、必ず削除してください。                  ]
#
# [ 使い方 ]
#  1. 「dataディレクトリ」の中に「dayx.dat」「today.dat」「yes.dat」を置き、
#      全てパーミッションを666にする。
#  2. 「conv.cgi」を「dayxディレクトリ」に置き、パーミッションを755にする。
#  3. 「conv.cgi」にアクセスし、「変換完了!」の文字列が表示されたら成功。
#  4. 「conv.cgi」を削除する。

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

require "./init.cgi";
my %cf = &init;

# 旧データ
open(IN,"$cf{logfile}") || die;
my $data = <IN>;
close(IN);

my ($key, $yes, $today, $count, $youbi, $ip) = split(/<>/, $data);

open(DAT,"+> $cf{logfile}") || die;
print DAT "$key<>$count<>$youbi<>$ip";
close(DAT);

open(DAT,"+> $cf{todfile}") || die;
print DAT $today;
close(DAT);

open(DAT,"+> $cf{yesfile}") || die;
print DAT $yes;
close(DAT);

chmod( 0666, $cf{logfile}, $cf{todfile}, $cf{yesfile} );

print <<EOM;
Content-type: text/html

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>変換プログラム</title>
</head>
<body>
変換完了!
</body>
</html>
EOM
exit;

