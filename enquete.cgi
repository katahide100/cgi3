#!/usr/local/bin/perl

require './cust.cgi';
require 'duel.pl';

&decode;
&get_cookie;

($sec,$min,$hour,$mday,$mon,$year) = localtime(time);

if($F{'mode'} eq 'view') {
	&view;
} elsif($F{'pass'} eq '') {
	&check;
} else {
	&set_cookie;
	&decode2;
	&get_ini;
	
	&main;
	
}

sub check {
	&header;
	print <<"EOM";
<p align="center">
新CGIの仕様に関するアンケートです。<br>
<br>
<form action="enquete.cgi" name="send" method="post">
<table border="0" cellpadding="2" bgcolor="#FFFFFF">
<tr><td colspan="2">まずはIDとパスワードを入力してください。</td></tr>
<tr><th>ID</th><td>：<input type="text" name="id" value="$c_id" size="14"></td></tr>
<tr><th>パスワード</th><td>：<input type="password" name="pass" value="$c_pass" size="14"></td></tr>
<tr><td colspan="2"><hr size="1"></td></tr>
<tr><td colspan="2">年齢を教えてください。</td></tr>
<tr><th>&nbsp;</th><td align="left"><input type="radio" name="age" value="0" id="age_0" checked><label for="age_0">回答しない</label><br>
<input type="radio" name="age" value="1" id="age_1"><label for="age_1">10才以下</label><br>
<input type="radio" name="age" value="2" id="age_2"><label for="age_2">11～15才</label><br>
<input type="radio" name="age" value="3" id="age_3"><label for="age_3">16～20才</label><br>
<input type="radio" name="age" value="4" id="age_4"><label for="age_4">21～25才</label><br>
<input type="radio" name="age" value="5" id="age_5"><label for="age_5">26～30才</label><br>
<input type="radio" name="age" value="6" id="age_6"><label for="age_6">31才以上</label></td></tr>
<tr><td colspan="2"><hr size="1"></td></tr>
<tr><td colspan="2">ＤＭを始めて何年程度経つか教えてください。</td></tr>
<tr><th>&nbsp;</th><td align="left"><input type="radio" name="dm" value="0" id="dm_0" checked><label for="dm_0">回答しない</label><br>
<input type="radio" name="dm" value="1" id="dm_1"><label for="dm_1">1年未満</label><br>
<input type="radio" name="dm" value="2" id="dm_2"><label for="dm_2">1～2年</label><br>
<input type="radio" name="dm" value="3" id="dm_3"><label for="dm_3">2～3年</label><br>
<input type="radio" name="dm" value="4" id="dm_4"><label for="dm_4">3～4年</label><br>
<input type="radio" name="dm" value="5" id="dm_5"><label for="dm_5">4～5年</label><br>
<input type="radio" name="dm" value="6" id="dm_6"><label for="dm_6">5年以上</label></td></tr>
<tr><td colspan="2"><hr size="1"></td></tr>
<tr><td colspan="2">対戦CGIの操作には慣れていますか？</td></tr>
<tr><th>&nbsp;</th><td align="left"><input type="radio" name="cgi" value="0" id="cgi_0" checked><label for="cgi_0">回答しない</label><br>
<input type="radio" name="cgi" value="1" id="cgi_1"><label for="cgi_1">ほぼ完璧に慣れている。(熟練者)</label><br>
<input type="radio" name="cgi" value="2" id="cgi_2"><label for="cgi_2">それなりに慣れている。(中級者)</label><br>
<input type="radio" name="cgi" value="3" id="cgi_3"><label for="cgi_3">まったく慣れていない。(初心者)</label><br>
<tr><td colspan="2"><hr size="1"></td></tr>
<tr><td colspan="2">新CGIに行動の確認は必要か教えてください。<br>(ボタンを押した時に出てくるアラートが必要か)</td></tr>
<tr><th>&nbsp;</th><td align="left"><input type="radio" name="alert" value="0" id="alert_0" checked><label for="alert_0">回答しない</label><br>
<input type="radio" name="alert" value="1" id="alert_1"><label for="alert_1">絶対に必要だと思う。</label><br>
<input type="radio" name="alert" value="2" id="alert_2"><label for="alert_2">必要だと思う。</label><br>
<input type="radio" name="alert" value="3" id="alert_3"><label for="alert_3">どうでもいいと思う。</label><br>
<input type="radio" name="alert" value="4" id="alert_4"><label for="alert_4">必要ないと思う。</label><br>
<input type="radio" name="alert" value="5" id="alert_5"><label for="alert_5">絶対に要らない。</label><br>
<input type="radio" name="alert" value="6" id="alert_6"><label for="alert_6">よくわからない。</label><br>
<input type="radio" name="alert" value="7" id="alert_7"><label for="alert_7">そう　かんけいないね</label><br>
<tr><td colspan="2"><hr size="1"></td></tr>
<tr><td colspan="2">新CGIに行動フェイズは必要か教えてください。<br>(ドロー～アタックまでの各フェイズが必要か)</td></tr>
<tr><th>&nbsp;</th><td align="left"><input type="radio" name="phase" value="0" id="phase_0" checked><label for="phase_0">回答しない</label><br>
<input type="radio" name="phase" value="1" id="phase_1"><label for="phase_1">絶対に必要だと思う。</label><br>
<input type="radio" name="phase" value="2" id="phase_2"><label for="phase_2">必要だと思う。</label><br>
<input type="radio" name="phase" value="3" id="phase_3"><label for="phase_3">どうでもいいと思う。</label><br>
<input type="radio" name="phase" value="4" id="phase_4"><label for="phase_4">必要ないと思う。</label><br>
<input type="radio" name="phase" value="5" id="phase_5"><label for="phase_5">絶対に要らない。</label><br>
<input type="radio" name="phase" value="6" id="phase_6"><label for="phase_6">よくわからない。</label><br>
<input type="radio" name="phase" value="7" id="phase_7"><label for="phase_7">( ﾟдﾟ )</label><br>
<tr><td colspan="2"><hr size="1"></td></tr>
<tr><td colspan="2">ＶＩＰＰＥＲですか？</td></tr>
<tr><th>&nbsp;</th><td align="left"><input type="radio" name="vip" value="0" id="vip_0" checked><label for="vip_0">回答しない</label><br>
<input type="radio" name="vip" value="1" id="vip_1"><label for="vip_1">はい。</label><br>
<input type="radio" name="vip" value="2" id="vip_2"><label for="vip_2">いいえ。</label><br>
<input type="radio" name="vip" value="3" id="vip_3"><label for="vip_3">ＶＩＰＰＥＳＴです。</label><br>
<input type="radio" name="vip" value="4" id="vip_4"><label for="vip_4">よくわからない。</label><br>
<tr><td colspan="2"><hr size="1"></td></tr>
<tr><td colspan="2">お疲れ様でした。以上でアンケートは終了です。</td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="アンケートを投函する"></td></tr>
</table>
</form>
<br>
<a href="./index.cgi">やっぱり帰る</a>
</p>
EOM
	&footer;
}

sub view {
	&filelock("enquete");
	open(IN,"enquete/enq1.dat");
	@enq = <IN>;
	close(IN);
		&header;
		print <<"EOM";
<p align="center">
<table border="0" cellpadding="2" bgcolor="#FFFFFF">
<tr><th>年齢</th><th>ＤＭ暦</th><th>CGI慣</th><th>行動確認</th><th>フェイズ</th><th>&nbsp;</th></tr>
EOM

	foreach $enq (@enq) {
		my($e_id, $e_name, $e_shohai, $e_age, $e_dm, $e_cgi, $e_alert, $e_phase, $e_vip) = split(/<>/, $enq);
		my($age_v) = ($e_age == 1) ? "10歳以下" : ($e_age == 2) ? "11～15歳" : ($e_age == 3) ? "16～20歳" : ($e_age == 4) ? "21～25歳" : ($e_age == 5) ? "26～30歳" : ($e_age == 6) ? "31歳以上" : "回答しない";
		my($dm_v) = ($e_dm == 1) ? "1年未満" : ($e_dm == 2) ? "1～2年" : ($e_dm == 3) ? "2～3年" : ($e_dm == 4) ? "3～4年未満" : ($e_dm == 5) ? "4～5年" : ($e_dm == 6) ? "5年以上" : "回答しない";
		my($cgi_v) = ($e_cgi == 1) ? "熟練者" : ($e_cgi == 2) ? "中級者" : ($e_cgi == 3) ? "初心者" : "回答しない";
		my($alert_v) = ($e_alert == 1) ? "絶対に必要" : ($e_alert == 2) ? "必要" : ($e_alert == 3) ? "どっちでも" : ($e_alert == 4) ? "不要" : ($e_alert == 5) ? "絶対に不要" : "回答しない";
		my($phase_v) = ($e_phase == 1) ? "絶対に必要" : ($e_phase == 2) ? "必要" : ($e_phase == 3) ? "どっちでも" : ($e_phase == 4) ? "不要" : ($e_phase == 5) ? "絶対に不要" : "回答しない";
		my($vip_v) = (($e_vip == 1) || ($e_vip == 3)) ? "[VIPPER]" : "&nbsp;";
		print <<"EOM";
<tr><td>$age_v</td><td>$dm_v</td><td>$cgi_v</td><td>$alert_v</td><td>$phase_v</td><td>$vip_v</td></tr>
<tr><td colspan="6"><hr size="1"></td></tr>
EOM
	}
		print <<"EOM";
</table>
<a href="./index.cgi">トップに戻る</a>
</p>
EOM
	&footer;
}

sub main {
	&filelock("enquete");
	open(IN,"enquete/enq1.dat");
	@enq = <IN>;
	close(IN);
	my($flag) = 0;
	foreach $enq (@enq) {
		my($e_id, $e_name, $e_shohai, $e_age, $e_dm, $e_cgi, $e_alert, $e_phase, $e_vip) = split(/<>/, $enq);
		if ($e_id eq $id) {
			$flag = 1;
			last;
		}
	}
	if ($flag == 0) {
		unshift(@enq, "$id<>$P{'name'}<>$P{'shohai'}<>$F{'age'}<>$F{'dm'}<>$F{'cgi'}<>$F{'alert'}<>$F{'phase'}<>$F{'vip'}<>\n");
		open(OUT,">enquete/enq1.dat");
		print OUT @enq;
		close(OUT);
	}
	&fileunlock("enquete");

	if($flag == 1) {
		&header;
		print <<"EOM";
<p align="center">
このアンケートはすでに回答済みです。<br>
<br>
<a href="./index.cgi">トップに戻る</a>
</p>
EOM
		&footer;
	} elsif($P{'order_enquete'} == 1) {
		&header;
		print <<"EOM";
<p align="center">
アンケートにご協力いただきありがとうございました。<br>
<br>
<a href="./index.cgi">トップに戻る</a>
</p>
EOM
		&footer;
	} else {
		$P{'order_enquete'} = 1;
		&pfl_write($id);
		
		&header;
		print <<"EOM";
<p align="center">
アンケートにご協力いただきありがとうございました。<br>
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
