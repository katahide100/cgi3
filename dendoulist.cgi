#!/usr/local/bin/perl

require "cust.cgi";
require "duel.pl";

&cardread;

@cardlist = (0 .. $#c_name);

&header;
print <<"EOM";
<style type="text/css">
<!--
.valign_top	{ vertical-align: top; }
-->
</style>
</head>
<body>
<div align="center">
<h1>$title</h1>
<table border="1" width="600" cellspacing="0" cellpadding="10" rules="none">
<tr><td class="table" colspan="2"> 
<p>この対戦ＣＧＩでの殿堂入りカード情報です。</p>
</td></tr>
<tr><td class="table valign_top" border="0">
<div align="center">
<table border="0" cellpadding="4" cellspacing="0">
<tr bgcolor="#0000FF"><td><font color="#FFFFFF">殿堂入りカード</font></td></tr>
EOM

@cardlist = sort s_pop @cardlist;

# 殿堂リスト表示

foreach(@dendou) {
$bgc = ($cnt % 2 == 0) ? "#00FFFF" : "#87CEEB";
print <<"EOM";
	<tr bgcolor="$bgc"><td>$c_name[$_]</td></tr>
EOM
$cnt ++;
}
print <<"EOM";
</div>
</table>
</td>
<td class="table valign_top">
<div align="center">
<table border="0" cellpadding="4" cellspacing="0">
<tr bgcolor="#0000FF"><td><font color="#FFFF00">プレミアム殿堂入りカード</font></td></tr>
EOM

# プレミアム殿堂リスト表示
my($cnt) = 0;
foreach(@premium) {
$bgc = ($cnt % 2 == 0) ? "#7B68EE" : "#FF00FF";
print <<"EOM";
	<tr bgcolor="$bgc"><td><font color="#FFFF00">$c_name[$_]</font></td></tr>
EOM
$cnt ++;
}
print <<"EOM";
</div>
</table>
</td></tr>
<tr><td class="table" colspan="2">
<div align="center">
<br>
<p><a href="index.cgi">戻る</a></p>
</div>
</td></tr>
</table>
EOM
&footer;

sub s_pop { $c_pop[$b] <=> $c_pop[$a]; }
