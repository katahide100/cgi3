#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

require './cust.cgi';
require 'duel.pl';

&decode;
&get_cookie;

($sec,$min,$hour,$mday,$mon,$year) = localtime(time);

if(($mon + 1 == 12) && ($mday == 25)) {
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
★次のどれかに該当する方は是非この勲章をお受け取りください★<br>
<br>
<table>
<tbody>
<tr>
<td align="left">
┏━━━━━━━━━━━┓ <br>
┃　12月　December　　 　 　┃ <br>
┠───────────┨ <br>
┃　 　 　 　 　 　 　 1　 2　 3 .┃ <br>
┃　 4　 5　 6　 7　 8　 9 .10 .┃ <br>
┃ .11 .12 .13 .14 .15 .16 .17/V <br>
.そ .18 .19 .20 .21 .22 .23 .∑ <br>
　ﾚﾍ√＼ノZ∧ﾚﾍ√＼ノZ/ <br>
<br>
<br>
.: : : : : : : : :: :::: :: :: : :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::☆:::::::＋:::::::::::::: <br>
　　. . : : : ::::／⌒ヽ: ::: :: : :::: :: ::: ::: :::::::::::::::::::::::::..,,::。:+::::::::::::::::::::::: <br>
　　. .... ..::::/　　<｀O:: :: ::: :::::: :::::::::::: : :::::::::::::::::::+,::o;;::・;,::::::::::::::::::::: <br>
　　　　　⊂ﾆﾆﾆ⊃. . .: : : ::: : :: ::::::::: ::::::::::::::::..<;;::・,,::;ゞ;;o;*::.::::::::::: <br>
　　　 　/:彡ミ゛ヽ;）ー､. . .: : : :::::: ::::::::::::::::,,;;;<;+::;;;´;*::o*:,,;;ゞ;;:::::::: <br>
　　　 ./　/ヽ/ヽ、ヽ　 i. . .: : : :::::::: :::::::::::;;;*;;;〇;ゞ;*::;;:<;;;*;:;ゞ;;o; <br>
　　　/　/　｡ 　ヽ　ヽ　ｌ　　　:. :. .:: : :: ::<;;;;〇;ゞ;*::o,ゞ　;*;;;;*ゞ;*:o <br>
　￣（_,ノ ￣￣￣ヽ､_ノ￣￣ 　　　　;;;*;;;〇;ゞ;*::;;;;;*ゞ;*::o,　〇;;; ＊ <br>
　　　　　　　　　　　　　　　　　　　　　　　: : : : : :　llllllll　: : : : : : <br>
　　　　　　　　　　　　　　　　　　　　　　　　　　　田田田<br>
<br>
<br>
　　　／￣ヽ　　　　　l　　　　　　　　　　　　　　　お<br>
　　 , o　　　',　 はさ l　　　　　　　　 ＿　　　　　.は<br>
　　 ﾚ､ヮ __/　 ..じて l　　　　　　　／　　＼　　　 よ<br>
　　　　 /　ヽ　 めそ.l　　　　　　　{@　　@ i　　　 う<br>
　　　_/　　 l ヽ るろ l　　　　　　　} し_　　/<br>
　　　しl　　 i　ｉ かそl　　　　　　　 >　⊃ <　　　　今<br>
　　　　 l　　 ｰﾄ..　ろl　　　　　　　/ l　　　 ヽ 　　 日<br>
￣￣¨¨~~ ‐‐‐---─|　　　　　　/ /l　　 丶 .l　　 も<br>
　　　　　　　　　　　　|　　　　　 / / l　　　 }　l　 　い<br>
　　　　:☆::　　　　　 l　　　 ／ユ¨‐‐- ､_　 l　!:.　 い<br>
　　::彡彳*‡:*..　　　 l　_ ／　　　｀ ヽ__　 `-{し|:　天<br>
.:+彡*★:ミ:♪:ミ。:.,　l ／　　　　　　　　　｀ヽ　}／気<br>
.:彡'゜‡,※゜.ﾆｭ▲:ミ,::..l　　　　　　　　　　／ ／/　だ<br>
￣￣ ¨¨¨ー─‐‐--- ,,,,, ＿＿ ___＿_／ ／_/　　<br>
　　　　　　　　 ,..-´￣''ｰ,__　　　　　 ￣¨¨｀ ー──---<br>
　　　　　　 ／:::::::::::::::::::＞⌒ヽ<br>
　 　 　 　/:::::::::::::::::!:／ 弋__ノ<br>
　　　　/￣￣￣￣ヽ<br>
　　　　ゝ＿＿＿＿ﾉ<br>
　　　　／ﾉ(　_ノ　　＼　　<br>
　　　　|　⌒(（:;。:;）（;;ﾟ）<br>
　　　　.|　　　　 （__人__）　/⌒l　　　　　　　　　　　　　　 :☆:<br>
　　　 　|　　　　　｀ ⌒´ﾉ　|`'''|　　　　　　　　　　　　..::彡彳*‡:*..<br>
　　　　／ ⌒ヽ　　　　 }　 |　 |　　　　　　 　　　　.:+彡*★:ミ:♪:ミ。:.,<br>
　　 ／　 へ　　＼　　 }__/　/　　 　 　 　　　　　.:彡'゜‡,※゜.ﾆｭ▲:ミ,::..　ドシッ<br>
　／　／　|　　　　　 ノ 　 ノ　　　　　　　　　　.,;彡*;▲彡゜*★::.ﾄｰｲミ+:..<br>
( _ ノ　　　 |　　　　　 ＼´　　　　　　 ＿　　　..*彡゜◎.从♪.:ミ,☆,゜〓:ミ:,,<br>
　　　　　 　|　　　　　　　＼＿,, -‐ ''"　 ￣￣ﾞ''―---└'´￣｀ヽ.:.ミ.+:◎,ミ。:..<br>
　　　　　　 .|　　　　　　　　　　　　　　　　　　　　;,,,;,,,;,;,,＿＿＿ノ;,,,.<br>
　　　　　　　ヽ　　　　　　　　　　　＿,, -‐ ''"￣""”” ;■■■■;　　　ドシッ<br>
<br>
<br>
　　　　 ＿＿＿＿＿＿＿＿＿＿___<br>
　　　／|：： ┌──────┐ ：：|<br>
　　/.　 |：： ｜ 　　　　　　　　 ｜ ：：|<br>
　　|....　|：： ｜　　　　　　　　　｜ ：：|<br>
　　|....　|：： ｜　　　　　　　　　｜ ：：|<br>
　　|....　|：： └──────┘ ：：|<br>
　　＼_｜　　　 ┌────┐　　 .|　　　　 ∧∧<br>
　　　　 ￣￣￣￣￣￣￣￣￣￣￣　　 　 ( 　＿)　　　　俺が彼女がいないことで<br>
　　　　　　　　　　　　　／￣￣￣￣￣旦￣(_,　　 ）<br>
　　　　　　　　　　　 ／　　　　　　　　　　　　　＼ 　｀<br>
　　　　　　　　　　　|￣￣￣￣￣￣￣￣￣￣￣|、＿）<br>
　　　　　　　　　　　 ￣|￣|￣￣￣￣￣￣|￣|￣<br>
<br>
　　　　　|　　　　　　　　　　 .( (　|　|＼<br>
　　　　　| )　　　　　　　　　 　) ) |　|　.|<br>
　　　　　|＿＿＿＿＿＿＿＿(__|　.＼|　　　　　　　　俺の代わりにだれか一人、彼女を持てる<br>
　　　 ／― 　　∧ ∧　　――-＼≒<br>
　　／　　　 　 ( 　　　)　　　　　　　＼<br>
　　|￣￣￣￣￣￣￣￣￣￣￣￣￣ |<br>
　　|＿＿＿＿＿＿＿＿＿＿＿＿＿_|<br>
<br>
　　　∧∧<br>
　　（　 ･ω･）<br>
　 ＿|　⊃／(＿＿_<br>
／　└-(＿＿＿_／<br>
￣￣￣￣￣￣￣<br>
　　　　　　　　　　　　　　　　　　　　　　　　　　　　俺はそういうことに幸せを感じるんだ<br>
　 ＜⌒／ヽ-、_＿_<br>
／＜_/＿＿＿＿／<br>
<br>
<br>
　　　　　　　　 , -‐-､　　　　　　_　　　　　　　　　- ､<br>
　　　　　r‐ - '　　　 rヘ、　_／ ´/¨ヽ￣｀＼rく　　　しﾍ<br>
　　　{ _ ﾉ　　　　　 〈三　7／　　 |　　　　－くｿ　　　　　しｲ<br>
　　　 7　　　　　　　/｀7ｧ/　　/ /l　 　 ,、　　 ＼　　　　　く<br>
　　　 ﾚ{　,ｨ　r―- '　/l /　　 l　|-＼l　|-＼|　　 |ｰ､　ｒ、 r}<br>
　　　　 ∨ ﾍ{　　　 /　!ｌ|　　/ヘ!_　 ＼| _　l|　　∧　}ﾉ j丿<br>
　　　　 　 　 　 　 /　　vﾄ　 l　ｨ＝､　　 ｨ=､|　 /　l<br>
　　　　　　　　　 /}　　 /-＼l　　 　 　 '　　 j／　 {ヽ<br>
　　　　　　 　 　 |/ 　　 ＼_ ｀　　 r -- ┐　/　 　 ヽ|<br>
　　　　　　　　　　　　　　　-＼　　ヽ.__ノ ／<br>
　　　　　　　　　　　　 ／　　　|＞　. __／＼　　　　　　　　　　　　　　　　←婿<br>
　　　　 　 　 　 　 　 〈　　　　|j　　　|　　 　 〉<br>
　　　　　　　　　　　　 ＼　　 ∧　　卜　　 /<br>
　　　　　　　　　　　／￣ ＼ 　 lｰ　一l　 /￣＼<br>
　　　　 　 　 　 　 /　　　　| ＼ |ー‐一l / | l　　l<br>
　 　 　 　 　 　 　 |　　　　〈　　 |ヽ.　 /|'　 〉' 　 |<br>
</td>
</tr>
</tbody>
</table>
<br>
<!--やあ(´・ω・｀)管理人のメシスですよ。<br>
<br>
いや、まぁ別に何が言いたいってわけでもないけど。<br>
え？なんでわざわざこんなページ用意したかって？<br>
そりゃぁあれに決まってるっしょあれ。<br>
ほら12月25日。俗にいうクリスマスってやつ。<br>
<br>
いやークリスマスってめでたい日っすよねー。<br>
何がめでたいのか知らないけどめでたいっすよねーはぁーめでたいめでたい。<br>
<br>
町はもう電飾とか飾りまくりでも煌びやかなのな。<br>
男女のカップルが行き交って賑やかでとても楽しいですよね。<br>
<br>
まぁ、世間はそんなわけでクリスマスなわけで・・・<br>
で・・・<br>
世間はクリスマスなのに・・・<br>
クリスマスだというのに・・・ッ<br>
お前達はッ・・・<br>
対戦CGIかっ・・・！<br>
<br>
あ、いや、だからどうってわけじゃないっすよ。<br>
ほら、パソコンの前に座ってすごすのもいいっすよね！<br>
パソコンの世界だったらもうほんといろいろできるしさ！<br>
うん！現実なんかよりずっとよっぽどいいよね！ね！<br>
<br>
・・・<br>
<br>
ま、まぁ、現実世界でもほんとはみんなやるべきこと多いんですよね。<br>
それらよりも対戦CGIを優先してきてくれてるんですよね！<br>
決して彼女がいないだとか誰も誘ってくれる友達がいないだとか世間から隔離されてるだとか三次元を捨てただとかそんなんじゃないっすよね！<br>

とりあえずだな、そんな寂しくて切ないおまいらに漏れからのクリスマスプレゼントだ。<br>
この下にあるボタンを押してIDとパスワードを入力すると、特別な勲章を手に入れることができる。<br>
が、っここで注意してもらいたいのは勲章は一度入手すると二度と消せないということだ。<br>
何がいいたいかというとだな・・・<br>
<br>
クリスマスなのに対戦CGIに来ていたということがみんなにばれてしまうというわけだ・・・！<br>
その覚悟が出来ている人にだけ、是非とも入手してほしい。<br>
堂々と無い胸を張ってクリスマスに対戦CGIに来たことを誇れるデュエリストが・・・！<br>-->
<br>
<form action="christmas.cgi" name="send" method="post">
<table border="0" cellpadding="2">
<tr><th>ID</th><td>：<input type="text" name="id" value="$c_id" size="14"></td></tr>
<tr><th>パスワード</th><td>：<input type="password" name="pass" value="$c_pass" size="14"></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="クリスマスの勲章を受け取る"></td></tr>
</table>
</form>
<br>
<a href="./index.cgi">やっぱり帰る</a>
</p>
EOM
	&footer;
}

sub main {
	if($P{'order_christmas'} == 1) {
		&header;
		print <<"EOM";
<p align="center">
既にこの勲章は持っています。<br>
このいやしんぼめ！<br>
<BR>
<a href="./index.cgi">トップに戻る</a>
</p>
EOM
		&footer;
	} else {
		$P{'order_christmas'} = 1;
		&pfl_write($id);
		
		&header;
		print <<"EOM";
<p align="center">
さあ・・・これで君も孤高のデュエリストに仲間入りだ！<br>
よかったね！<br>
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
