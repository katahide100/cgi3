#!/usr/local/bin/perl

require "cust.cgi";
require "duel.pl";

&cardread;

&header;
print <<"EOM";
</head>
<body>
<div align="center">
<h1>$title</h1>
<table border="1" width="600" cellspacing="0" cellpadding="10">
<tr><td class="table"> 
<p>この対戦ＣＧＩの設定情報です。</p>
<div align="center">
<table border="0" cellpadding="2">
<tr><th>タイトル</th><td>：$title</td></tr>
</table><br>
<hr>
<table border="0" cellpadding="2">
<tr><th>勲章一覧</th></tr>
EOM
foreach (@order_per) {
#	print "<tr align=\"left\"><td><font color=\"$order_color{$_}\">$order_symbol{$_}</font> 『$order_text{$_}』</td></tr>\n";
	print "<tr align=\"left\"><td><img src=\"${symbol_dir}/symbol_${_}.png\" width=\"20\" height=\"20\" align=\"middle\"> 『$order_text{$_}』</td></tr>\n";
}
print <<"EOM";
</table>
<hr>
<table border="0" cellpadding="2">
<tr><th>ポイント減算カード</th></tr>
<tr><th>－１０</th></tr>
<tr><td>
EOM
foreach (@minus10) {
	print "<tr align=\"left\"><td>$c_name[$_] ($_)</td></tr>\n";
}
print <<"EOM";
</td></tr>
<tr><th>－５</th></tr>
<tr><td>
EOM
foreach (@minus5) {
	print "<tr align=\"left\"><td>$c_name[$_] ($_)</td></tr>\n";
}
print <<"EOM";
</td></tr>
<tr><th>－３</th></tr>
<tr><td>
EOM
foreach (@minus3) {
	print "<tr align=\"left\"><td>$c_name[$_] ($_)</td></tr>\n";
}
print <<"EOM";
</td></tr>
<tr><th>－１</th></tr>
<tr><td>
EOM
foreach (@minus1) {
	print "<tr align=\"left\"><td>$c_name[$_] ($_)</td></tr>\n";
}
print <<"EOM";
</td></tr>
<tr><th>＋１</th></tr>
<tr><td>
EOM
foreach (@plus1) {
	print "<tr align=\"left\"><td>$c_name[$_] ($_)</td></tr>\n";
}
print <<"EOM";
</td></tr>
</table><br>
<p><a href="index.cgi">戻る</a></p>
</div>
</td></tr>
</table>
EOM
&footer;
