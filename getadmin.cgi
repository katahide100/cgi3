#!/usr/local/bin/perl

require './cust.cgi';
require 'duel.pl';

&decode;
&get_cookie;

($sec,$min,$hour,$mday,$mon,$year) = localtime(time);

if(($mon + 1 == 4) && ($mday == 1)) {
	if($F{'pass'} eq '') {
		&check;
	} else {
		&set_cookie;
		&decode2;
		&get_ini;
	
		&main;
	
	}
} else {
	print "Location: ./index.cgi\n\n";
}

sub check {
	&header;
	print <<"EOM";
<p align="center">
おめでとうございます！<br>
今すぐIDとパスワードを入力して<big>登録処理</big>を完了してください！<br>
<span style="color:#FF0000">管理権限</span>を手に入れれば嫌いなアイツを<big>アクセス制限</big>にしたり、<br>
<b>個人チャット</b>を<big>自由に覗き見</big>できるようになります！<br>
更に<span style="color:#0000FF"><i>管理者である勲章</i></span>がつくので周りの人に<b>自慢</b>も！！<br>
みんな貴方のことを羨ましがるようになり学校でも<span style="color:#FF0000">モ</span><span style="color:#0000FF">テ</span><span style="color:#FF0000">モ</span><span style="color:#0000FF">テ</span>に！！１！<br>
今すぐ登録を！<br>
<br>
<form action="getadmin.cgi" name="send" method="post">
<table border="0" cellpadding="2">
<tr><th>ID</th><td>：<input type="text" name="id" value="$c_id" size="14"></td></tr>
<tr><th>パスワード</th><td>：<input type="password" name="pass" value="$c_pass" size="14"></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="管理者権限を受け取る"></td></tr>
</table>
</form>
<br>
<a href="./index.cgi">やっぱり帰る</a>
</p>
EOM
	&footer;
}

sub main {
	if($P{'order_aprilfool'} == 1) {
		&header;
		print <<"EOM";
<p align="center">
だからエイプリルフールなんです＞＜<br>
<BR>
<a href="./index.cgi">トップに戻る</a>
</p>
EOM
		&footer;
	} else {
		$P{'order_aprilfool'} = 1;
		&pfl_write($id);
		
		&header;
		print <<"EOM";
<p align="center">
エイプリルフールなんです＞＜<br>
<br>
<a href="./index.cgi">トップに戻る</a>
</p>
EOM
		&footer;
	}
}

sub get_ini {
	&error("プレイヤーファイルがありません。<br>IDを設定しなおしてください。") if !(-e "${player_dir}/".$id.".cgi") && $pass ne $admin;
	&pfl_read($id) if -e "${player_dir}/".$id.".cgi";
	&pass_chk;
	for my $i(1..5){
		unless($P{"deck$i"}){ $dnam[$i] = "記録なし"; next; }
		else{($dnam[$i],$dum) = split(/-/,$P{"deck$i"}); }
	}
	$selstr[$P{'usedeck'}] = " selected" if $P{'usedeck'};
}

sub pfl_read {
	my $id = $_[0];
	undef(%P);
	chmod 0666, "${player_dir}/".$id.".cgi";
	open(PFL,"${player_dir}/".$id.".cgi") || &error("プレイヤーファイルが開けません");
	while(<PFL>){ chomp; ($key,$val) = split(/\t/); $P{$key} = $val; }
	close(PFL);
	chmod 0000, "${player_dir}/".$id.".cgi";
}

sub pass_chk{
	&error("IDまたはパスワードが間違っています。入力し直してください。") if $pass ne "" && crypt($pass, $pass) ne $P{'pass'};
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

sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
	"http://www.w3.org/TR/REC-html40/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<meta http-equiv="Pragma" content="no-cache">
	<link rel="stylesheet" href="$css/duel.css" type="text/css">
	<title>$title</title>
</head>
<body>
	<div align="center">
		<h1>$title</h1>
EOM
}

sub footer{
	print <<"EOM";
		<p>(c)Wizards of the Coast / Shogakukan / Mitsui-MP<br><a href="http://tsuru.pekori.to">つる＠帝国大劇場別館</a></p>
	<p><a href="javascript:history.back();">戻る</a></p>
	</div>
</body>
</html>
EOM
	exit;
}

sub error {
	&header;
	print <<"EOM";
		<hr>
		<h2>ERROR !</h2>
		<p><strong style="color:red">$_[0]</strong></p>
		<p><a href="javascript:history.back();">戻る</a></p>
		<hr>
EOM
	&footer;
}

sub filelock {
	if(-e $lockfile2){
		$ftm = (stat($lockfile2))[9];
		unlink $lockfile2 if $ftm < time-150 ;
	}
	foreach(1..5){
		if(-e $lockfile2){sleep(1);}
		else{open(LOCK,">$lockfile2");close(LOCK);return;}
	}
	&error("ファイルロック中です。"); 
}

sub fileunlock {
	unlink $lockfile2 if -e $lockfile2 ;
}

sub min {
	if($_[0] > $_[1]) { return $_[1]; }
	else		  { return $_[0]; }
}

sub decode{
	if(length($ENV{'QUERY_STRING'})>0){$INPUT=$ENV{'QUERY_STRING'};}
	elsif(length($ENV{'CONTENT_LENGTH'})>0){read(STDIN,$INPUT,$ENV{'CONTENT_LENGTH'});}
	else{$INPUT.=$TMP[0] while $TMP[0] = <STDIN>;}
	$INPUT=~s/\&+/\&/g;
	$INPUT=~s/#.+//;
	@TMP=split('&',$INPUT);
	foreach(@TMP){
		($KEY,$VAL)=split('=');
		$VAL =~ tr/+/ /;
		$VAL =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
#		&jcode'convert(*VAL,'euc');
		$VAL=~s/\015\012/\012/g;
		$VAL=~s/\015/\012/g;
		if($VAL){$F{$KEY}=$VAL;}
	}
}

sub decode2 {
	$id = $F{'id'};
	$pass = $F{'pass'}; $pass =~ s/\.//g; $pass =~ s/\///g;
	&error("IDが入力されていません") unless $id;
	&error("パスワードが入力されていません。") unless $pass;
}
