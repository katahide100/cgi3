#!/usr/local/bin/perl

require 'cust.cgi';
require 'duel.pl';

&decode;
&get_cookie;
$F{'id'} = $c_id if(!$F{'id'});
$F{'pass'} = $c_pass if(!$F{'pass'});
&set_cookie;

&decode2;
&pfl_read($id);
&pass_chk;

&regist		if $F{'mode'} eq "regist";
&white		if $F{'mode'} eq "white";
&black		if $F{'mode'} eq "black";
&html;

sub regist {
	return unless $id;

	$F{'wlist'} =~ s/\r\n/\,/g;
	$F{'wlist'} =~ s/\r/\,/g;
	$F{'wlist'} =~ s/\n/\,/g;
	$F{'wlist'} =~ s/\,+/\,/g;
	$P{'white'} = $F{'wlist'};

	$F{'blist'} =~ s/\r\n/\,/g;
	$F{'blist'} =~ s/\r/\,/g;
	$F{'blist'} =~ s/\n/\,/g;
	$F{'blist'} =~ s/\,+/\,/g;
	$P{'black'} = $F{'blist'};

	&pfl_write($id);
}

sub white {
	return unless $id;
	return if($F{'chara'} eq '');

	my(@wlist) = split(/\,/, $P{'white'});
	my($flag) = 0;
	for(my($i) = 0; $i <= $#wlist; $i ++) {
		if($wlist[$i] eq $F{'chara'}) {
			splice(@wlist, $i, 1);
			$flag = 1;
			last;
		}
	}
	if($flag == 0) {
		push(@wlist, $F{'chara'});
	}
	$P{'white'} = join(',', @wlist);

	&pfl_write($id);

	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
function sForm(F,C){
	with(list){
		mode.value = F;
		chara.value = C;
		action = F == "prof" ? "taisen.cgi" : "list.cgi";
		submit();
	}
}
// --></script>
</head>
<body>
<div align="center">
	<form name="list" action="list.cgi" method="post">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="">
		<input type="hidden" name="chara" value="">
	<table border="4" cellpadding="5" class="table"><tr valign="top">
		<td colspan="2" align="center">
EOM
	if($flag == 0) {
		print <<"EOM";
$F{'chara'}をホワイトリストに登録しました。<br>
EOM
	} else {
		print <<"EOM";
$F{'chara'}をホワイトリストから除外しました。<br>
EOM
	}
	print <<"EOM";
<br>
<a href="javascript:sForm('prof', '$F{'chara'}')">戻る</a>
		</td></tr>
	</table>
	</form>
</div>
EOM
	&footer;
}

sub black {
	return unless $id;
	return if($F{'chara'} eq '');

	my(@blist) = split(/\,/, $P{'black'});
	my($flag) = 0;
	for(my($i) = 0; $i <= $#blist; $i ++) {
		if($blist[$i] eq $F{'chara'}) {
			splice(@blist, $i, 1);
			$flag = 1;
			last;
		}
	}
	if($flag == 0) {
		push(@blist, $F{'chara'});
	}

	$P{'black'} = join(',', @blist);

	&pfl_write($id);

	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
function sForm(F,C){
	with(list){
		mode.value = F;
		chara.value = C;
		action = F == "prof" ? "taisen.cgi" : "list.cgi";
		submit();
	}
}
// --></script>
</head>
<body>
<div align="center">
	<form name="list" action="list.cgi" method="post">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="">
		<input type="hidden" name="chara" value="">
	<table border="4" cellpadding="5" class="table"><tr valign="top">
		<td colspan="2" align="center">
EOM
	if($flag == 0) {
		print <<"EOM";
$F{'chara'}をブラックリストに登録しました。<br>
EOM
	} else {
		print <<"EOM";
$F{'chara'}をブラックリストから除外しました。<br>
EOM
	}
	print <<"EOM";
<br>
<a href="javascript:sForm('prof', '$F{'chara'}')">戻る</a>
		</td></tr>
	</table>
	</form>
</div>
EOM
	&footer;
}

sub html{
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
function sForm(F){
	with(list){
		mode.value = F;
		action = F == "taisen" ? "taisen.cgi" : F == "deck" ? "deck.cgi" : F == "group" ? "group.cgi" : F == "log" ? "log.cgi" : F == "nuisance" ? "nuisance.cgi" : "list.cgi";
		submit();
	}
}
// --></script>
</head>
<body>
<div align="center">
	<form name="list" action="list.cgi" method="post">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="">
	<table border="4" cellpadding="5" class="table"><tr valign="top">
		<td colspan="2" align="center">
			<p><a href="./etc/help.html#group" target="_blank">説明</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('taisen');">対戦する</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('deck');">デッキ構築</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('group');">グループ構築</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('log');">過去ログ</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('nuisance');">迷惑報告</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="index.cgi">戻る</a></p>
<p><input type="button" value="リストセーブ" onclick="sForm('regist');"></p>
</td></tr>
	<tr valign="top">
	<td width="400">
	ここのリストには、対象にしたいユーザーIDをそれぞれに改行区切りで入れます。
	</td></tr>
	<tr valign="top">
	<td width="400">
	<strong>ホワイトリスト</strong><br>
	ここにお友達のIDを登録することで、伝言板にその人にしか見えない記事を書いたり、<br>
	その人しか入室することのできない部屋を作ることができるようになります。<br>
	<textarea name="wlist" cols="80" rows="10">
EOM
	my(@w_list) = split(/\,/, $P{'white'});
	foreach (@w_list) {
		print "$_\n";
	}
	print <<"EOM";
</textarea>
	</td></tr>
	<tr valign="top">
	<td width="400">
	<strong>ブラックリスト</strong><br>
	ここに登録されたIDが伝言板に書き込んだ記事は見えなくなり、<br>
	お互いの作った部屋にも入室できなくなります。<br>
	<textarea name="blist" cols="80" rows="10">
EOM
	my(@b_list) = split(/\,/, $P{'black'});
	foreach (@b_list) {
		print "$_\n";
	}
	print <<"EOM";
</textarea>
		</td></tr>
	</table>
	</form>
</div>
EOM
	&footer;
}

sub set_cookie{ 
	($sec,$min,$hour,$mday,$mon,$year) = gmtime(time + 30*24*60*60);
	$gdate = sprintf("%02d\-%s\-%04d %02d:%02d:%02d", $mday, ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mon], $year + 1900, $hour, $min, $sec);
	$cook = "id:$F{'id'},pass:$F{'pass'}";
	print "Set-Cookie: duel=$cook; expires=$gdate GMT\n";
}

sub get_cookie{
	$cookies = $ENV{'HTTP_COOKIE'};
	@pairs = split(/;/,$cookies);
	foreach $pair(@pairs){
		($name,$value) = split(/=/,$pair);
		$name =~ s/ //g;
		$D{$name} = $value;
	}
	@pairs = split(/,/,$D{'duel'});
	foreach $pair(@pairs){
		($name,$value) = split(/:/,$pair);
		$C{$name} = $value;
	}
	$c_id = $C{'id'};
	$c_pass = $C{'pass'};
}

sub decode2 {
	$id = $F{'id'};
	$pass = $F{'pass'}; $pass =~ s/\.//g; $pass =~ s/\///g;
	&error("IDが入力されていません") unless $id;
	&error("パスワードが入力されていません。") unless $pass;
}