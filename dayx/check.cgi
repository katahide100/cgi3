#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DAY COUNTER-EX : check.cgi - 2011/10/07
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

require "./init.cgi";
my %cf = &init;

print <<EOM;
Content-type: text/html

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
EOM

# ログファイル確認
my %log = (
	logfile => '累計',
	todfile => '本日',
	yesfile => '昨日',
	dayfile => '日次',
	monfile => '月次',
	);
foreach ( keys(%log) ) {
	if (-f $cf{$_}) {
		print "<li>$log{$_}ファイルパス : OK\n";

		# ログファイルのパーミッション
		if (-r $cf{$_} && -w $cf{$_}) {
			print "<li>$log{$_}ファイルパーミッション : OK\n";
		} else {
			print "<li>$log{$_}ファイルパーミッション : NG\n";
		}
	} else {
		print "<li>$log{$_}ファイルパス : NG\n";
	}
}

# テンプレート
if (-f "$cf{tmpldir}/list.html") {
	print "<li>テンプレート : OK\n";
} else {
	print "<li>テンプレート : NG\n";
}

# 画像チェック
foreach ( $cf{gifdir1}, $cf{gifdir2} ) {
	foreach my $i (0 .. 9) {
		if (-e "$_/$i.gif") {
			print "<li>画像 : $_/$i.gif → OK\n";
		} else {
			print "<li>画像 : $_/$i.gif → NG\n";
		}
	}
}

eval { require $cf{gifcat_pl}; };
if ($@) {
	print "<li>gifcat.plテスト : NG\n";
} else {
	print "<li>gifcat.plテスト : OK\n";
}

eval { require Image::Magick; };
if ($@) {
	print "<li>Image::Magickテスト : NG\n";
} else {
	print "<li>Image::Magickテスト : OK\n";
}

# 著作権表示：削除改変禁止
print <<EOM;
</ul>
<p style="font-size:10px;font-family:Verdana,Helvetica,Arial;margin-top:5em;text-align:center;">
- <a href="http://www.kent-web.com/">DayCounter-EX</a> -
</p>
</body>
</html>
EOM
exit;

