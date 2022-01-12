#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

require './cust.cgi';
require 'duel.pl';

&decode;
&get_cookie;

if($F{'pass'} eq '') {
	&check;
} else {
	&set_cookie;
	&decode2;
	&get_ini;

	if($P{'admin'} > 0) {
		if($F{'mode'} eq 'logview')		{	&logview;	}
		elsif($F{'mode'} eq 'evaluate')		{	&evaluate;	}
		elsif($F{'mode'} eq 'solve')		{	&solve;		}
		elsif($F{'mode'} eq 'comment')		{	&comment;	}
		else					{	&main;		}
	} elsif($P{'subadmin'} > 0) {
		if($F{'mode'} eq 'logview')		{	&logview;	}
		elsif($F{'mode'} eq 'evaluate')		{	&evaluate;	}
		elsif($F{'mode'} eq 'solve')		{	&solve;		}
		elsif($F{'mode'} eq 'comment')		{	&comment;	}
		else					{	&main;		}
	} else {
		if($F{'mode'} eq 'logview')		{	&logview;	}
		else					{	&main;		}
	}


}

sub check {
	&header;
	print <<"EOM";
<form action="nuisance.cgi" name="send" method="post">
<input type="hidden" name="mode" value="login">
<table border="0" cellpadding="2">
<tr><th>ID</th><td>：<input type="text" name="id" value="$c_id" size="14"></td></tr>
<tr><th>パスワード</th><td>：<input type="password" name="pass" value="$c_pass" size="14"></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="迷惑リスト起動"></td></tr>
</table>
</form>
EOM
	&footer;
}

sub main {
	&filelock("nuisance");
	open(IN,"./nuisance/nui_list.dat");
	@nuis = <IN>;
	close(IN);
	my $n_new = int(shift(@nuis));
	my $cflag = 0;
	for(my($i) = 0; $i <= $#nuis; $i ++) {
		my($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom) = split(/<>/, $nuis[$i]);
		if($n_time < time - 60 * 60 * 24 * 7) {
			splice(@nuis, $i, 1);
			$c_flag = 1;
		}
	}
	if($c_flag == 1) {
		unshift(@nuis, "$n_new\n");
		open(OUT,"> ./nuisance/nui_list.dat");
		print OUT @nuis;
		close(OUT);
		shift(@nuis);
	}
	&fileunlock("nuisance");

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
<script type="text/javascript"><!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		if(M == "taisen") {
			entrance.action = "taisen.cgi";
		} else if(M == "deck") {
			entrance.action = "deck.cgi";
		} else if(M == "group") {
			entrance.action = "group.cgi";
		} else if(M == "list") {
			entrance.action = "list.cgi";
		} else if(M == "logview") {
			entrance.action = "nuisance.cgi";
			entrance.num.value = R;
		} else if(M == "prof") {
			entrance.action = "taisen.cgi";
			entrance.num.value = R;
		} else if(M == "log") {
			entrance.action = "log.php";
		} else if(M == "index") {
			entrance.action = "index.cgi";
		}

		entrance.target = (M == "prof") ? "_blank" : "_self";
		entrance.submit();
	}
// --></script>
</head>
<body>
	<div align="center">
		<h1>$title</h1>
<br>
<table border="1">
EOM
	foreach(@nuis) {
		my($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom) = split(/<>/, $_);
		my $slv = $n_solve == 1 ? '解決済み' : '未解決';
		my $bgc = $n_solve == 1 ? '#CCCCFF' : '#FFCCCC';
		my($sec,$min,$hour,$mday,$mon,$year) = localtime($n_time);
		$year += 1900;
		$mon ++;
		my $n_date = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		print <<"EOM";
<tr bgcolor="#FFFFFF">
<td width="80">解決</td>
<td width="120">報告者</td>
<td width="320">報告内容</td>
<td width="80">時間</td>
</tr>
<tr bgcolor="$bgc">
<td rowspan="2" width="80">$slv</td>
<td align="left" width="120">原告: <a href=\"javascript:sForm('prof','','${n_user1id}');\">${n_user1name}</a><BR>
被告: <a href="javascript:sForm('prof','','${n_user2id}');">${n_user2name}</a></td>
<td width="320">$n_comment</td>
<td width="80">$n_date</td>
</tr>
<tr bgcolor="#FFFFFF">
<td width="120">[<a href="javascript: sForm('logview', '$n_num');">部屋ログ</a>]</td>
<td colspan="2" width="400">$n_admcom</td>
</tr>
<tr>
<td colspan="4"><hr></td>
</tr>
EOM
		$cou ++;
	}
	print <<"EOM";
</table>
<hr>
<form action="nuisance.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
	<input type="hidden" name="num" value="">
</form>
<a href="javascript:sForm('', '', '');">更新する</a>&nbsp;&nbsp;
<a href="javascript:sForm('taisen', '', '');">対戦する</a>&nbsp;&nbsp;
<a href="javascript:sForm('deck', '', '');">デッキ構築</a>&nbsp;&nbsp;
<a href="javascript:sForm('group', '', '');">グループ編集</a>&nbsp;&nbsp;
<a href="javascript:sForm('list', '', '');">リスト編集</a>&nbsp;&nbsp;
<a href="javascript:sForm('log', '', '');">過去ログ</a>&nbsp;&nbsp;
<a href="javascript:sForm('index', '', '');">トップへ戻る</a>
EOM
	if($P{'admin'} > 0) {

	} elsif($P{'subadmin'} > 0) {

	}
	&footer;
}

sub logview {
	&filelock("nuisance");
	open(IN,"nuisance/nui_list.dat");
	@nuis = <IN>;
	close(IN);
	my $n_new = int(shift(@nuis));
	my $flag = 0;
	my($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom);
	foreach(@nuis) {
		($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom) = split(/<>/, $_);
		if($n_num == $F{'num'}) {
			$flag = 1;
			last;
		}
	}
	if($flag == 1) {
		my($sec,$min,$hour,$mday,$mon,$year) = localtime($n_time);
		$year += 1900;
		$mon ++;
		my $n_date = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
		open(IN,"nuisance/log/${n_roomid}_log");
		@numlogs = <IN>;
		close(IN);
		&fileunlock("nuisance");

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
	<script type="text/javascript"><!--
		with(document);
		function sForm(M,R,C) {
			entrance.mode.value = M;
			entrance.room.value = R;
			entrance.chara.value = C;
			if(M == "taisen") {
				entrance.action = "taisen.cgi";
			} else if(M == "deck") {
				entrance.action = "deck.cgi";
			} else if(M == "group") {
				entrance.action = "group.cgi";
			} else if(M == "list") {
				entrance.action = "list.cgi";
			} else if(M == "index") {
				entrance.action = "index.cgi";
			}
			entrance.target = (M == "prof") ? "_blank" : "_self";
			entrance.submit();
		}
	// --></script>
	</head>
	<body>
		<div align="center">
			<h1>$title</h1>
	<br>
	<table border="1">
EOM
		my $slv = $n_solve == 1 ? '解決済み' : '未解決';
		my $bgc = $n_solve == 1 ? '#CCCCFF' : '#FFCCCC';
		print <<"EOM";
	<tr bgcolor="#FFFFFF">
	<td>解決</td>
	<td>報告者</td>
	<td>報告内容</td>
	<td>時間</td>
	</tr>
	<tr bgcolor="$bgc">
	<td rowspan="2">$slv</td>
	<td align="left">原告: <a href=\"javascript:sForm('prof','','${n_user1id}');\">${n_user1name}</a><BR>
	被告: <a href=\"javascript:sForm('prof','','${n_user2id}');\">${n_user2name}</a></td>
	<td>$n_comment</td>
	<td>$n_date</td>
	</tr>
	<tr>
	<td colspan="4" bgcolor="#FFFFFF">$n_admcom</td>
	</tr>
	</table>
	<hr>
	<form action="nuisance.cgi" method="post" name="entrance">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="">
		<input type="hidden" name="room" value="">
		<input type="hidden" name="chara" value="">
	</form>
	<a href="javascript:sForm('');">迷惑リストに戻る</a>&nbsp;&nbsp;
	<a href="javascript:sForm('taisen');">対戦する</a>&nbsp;&nbsp;
	<a href="javascript:sForm('deck');">デッキ構築</a>&nbsp;&nbsp;
	<a href="javascript:sForm('group');">グループ編集</a>&nbsp;&nbsp;
	<a href="javascript:sForm('list');">リスト編集</a>&nbsp;&nbsp;
	<a href="javascript:sForm('index');">トップへ戻る</a>
EOM
		if(($P{'admin'} > 0) || ($P{'subadmin'} > 0)) {
			print <<"EOM";
	<hr>
	<form action="nuisance.cgi" method="post" name="evaluate" onSubmit="if(!confirm('本当に評価しますか？')) return false;">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="evaluate">
		<input type="hidden" name="num" value="$F{'num'}">
		評価対象: <select name="target">
			<option value="${n_user1id}" selected>${n_user1id}/${n_user1name}</option>
			<option value="${n_user2id}">${n_user2id}/${n_user2name}</option>
		</select>
		評価ポイント: <select name="point">
			<option value="5">＋５</option>
			<option value="4">＋４</option>
			<option value="3">＋３</option>
			<option value="2">＋２</option>
			<option value="1">＋１</option>
			<option value="0">±０</option>
			<option value="-1">－１</option>
			<option value="-2">－２</option>
			<option value="-3">－３</option>
			<option value="-4">－４</option>
			<option value="-5">－５</option>
		</select>
		<input type="submit" value="評価する">
	</form>
	<hr>
	<form action="nuisance.cgi" method="post" name="comment" onSubmit="if(!confirm('本当にコメントしますか？')) return false;">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="comment">
		<input type="hidden" name="num" value="$F{'num'}">
		コメント: <input type="input" name="comment" size="64" value="">
		<input type="submit" value="コメントする">
	</form>
	<hr>
	<form action="nuisance.cgi" method="post" name="evaluate" onSubmit="if(!confirm('本当に解決しますか？')) return false;">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="solve">
		<input type="hidden" name="num" value="$F{'num'}">
EOM
			if($n_solve == 1) {
			print <<"EOM";
		<input type="submit" value="未解決にする">
EOM
			} else {
			print <<"EOM";
		<input type="submit" value="解決にする">
EOM
			}
			print <<"EOM";
	</form>
EOM
		}
		print <<"EOM";
	<hr>
	<table border="1">
	<tr bgcolor="#FFFFFF">
	<td>
EOM
		foreach (@numlogs) {
			my ($msgman,$msg,$msgmode) = split(/<>/,$_);
			if($msgmode eq "system") {
				print qq|<span class="system">$msg</span><br>|;
			} elsif($msgmode eq "message") {
				print qq|<span class="message">$msgman ＞ $msg</span><br>|;
			} elsif($msgmode eq "message1") {
				print qq|<span class="message1">$msgman ＞ $msg</span><br>|;
			} elsif($msgmode eq "message2") {
				print qq|<span class="message2">$msgman ＞ $msg</span><br>|;
			} elsif($msgmode eq "tap") {
				print qq|<span class="taped">$msg</span><br>|;
			} elsif($msgmode eq "admin") {
				print qq|<span class="admin">$msgman ＞ $msg</span><br>|;
			}
		}
		print <<"EOM";
	</td>
	</tr>
	</table>
EOM
		&footer;
	} else {
		&error("データファイルが見つかりません。");
	}
}

sub evaluate {
	&filelock("nuisance");
	open(IN,"nuisance/nui_list.dat");
	@nuis = <IN>;
	close(IN);
	&filelock("$F{'target'}_lock");
	chmod 0666, "${player_dir}/".$F{'target'}.".cgi";
	open(PFL,"${player_dir}/".$F{'target'}.".cgi") || &error("プレイヤーファイルが開けません");
	while(<PFL>){ chomp; ($key,$val) = split(/\t/); $TP{$key} = $val; }
	close(PFL);
	my $n_new = int(shift(@nuis));
	my $flag = 0;
	my($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom);
	foreach(@nuis) {
		($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom) = split(/<>/, $_);
		@n_admcoms = split(/<br>/, $n_admcom);
		if($n_num == $F{'num'}) {
			$flag = 1;
			unshift(@n_admcoms, "<a href=\"javascript:sForm('prof','','$id');\">$P{'name'}</a>は<a href=\"javascript:sForm('prof','','$F{'target'}');\">$TP{'name'}</a>に$F{'point'}の評価を加えた。");
			$n_admcom = join("<br>", @n_admcoms);
			$_ = "$n_num<>$n_roomid<>$n_user1id<>$n_user1name<>$n_user2id<>$n_user2name<>$n_comment<>$n_time<>$n_solve<>$n_admcom<>\n";
			last;
		}
	}
	if($flag == 1) {
		unshift(@nuis, "$n_new\n");
		open(OUT,">nuisance/nui_list.dat");
		print OUT @nuis;
		close(OUT);
		&fileunlock("nuisance");
		$TP{'evpoint'} += $F{'point'};
		$TP{'evtime'} = time;
		open(PFL,">${player_dir}/".$F{'target'}.".cgi") || &error("書き込みエラーです。");
		foreach $key(keys(%TP)){ print PFL "$key\t$TP{$key}\n"; }
		close(PFL);
		&fileunlock("${id}_lock");
		&logview();
	} else {
		&fileunlock("nuisance");
		&fileunlock("${id}_lock");
		&error("データファイルが見つかりません。");
	}
}

sub solve {
	&filelock("nuisance");
	open(IN,"nuisance/nui_list.dat");
	@nuis = <IN>;
	close(IN);
	my $n_new = int(shift(@nuis));
	my $flag = 0;
	my($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom);
	foreach(@nuis) {
		($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom) = split(/<>/, $_);
		@n_admcoms = split(/<br>/, $n_admcom);
		if($n_num == $F{'num'}) {
			$flag = 1;
			$n_solve = 1 - $n_solve;
			unshift(@n_admcoms, "<a href=\"javascript:sForm('prof','','$id');\">$P{'name'}</a>はこの報告を" . (($n_solve == 1) ? "解決" : "未解決") . "にした。");
			$n_admcom = join("<br>", @n_admcoms);
			$_ = "$n_num<>$n_roomid<>$n_user1id<>$n_user1name<>$n_user2id<>$n_user2name<>$n_comment<>$n_time<>$n_solve<>$n_admcom<>\n";
			last;
		}
	}
	if($flag == 1) {
		unshift(@nuis, "$n_new\n");
		open(OUT,">nuisance/nui_list.dat");
		print OUT @nuis;
		close(OUT);
		&fileunlock("nuisance");
		&logview();
	} else {
		&fileunlock("nuisance");
		&error("データファイルが見つかりません。");
	}
}

sub comment {
	&filelock("nuisance");
	open(IN,"nuisance/nui_list.dat");
	@nuis = <IN>;
	close(IN);
	my $n_new = int(shift(@nuis));
	my $flag = 0;
	my($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom);
	foreach(@nuis) {
		($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom) = split(/<>/, $_);
		@n_admcoms = split(/<br>/, $n_admcom);
		if($n_num == $F{'num'}) {
			$flag = 1;
			unshift(@n_admcoms, "<a href=\"javascript:sForm('prof','','$id');\">$P{'name'}</a> ＞ $F{'comment'}");
			$n_admcom = join("<br>", @n_admcoms);
			$_ = "$n_num<>$n_roomid<>$n_user1id<>$n_user1name<>$n_user2id<>$n_user2name<>$n_comment<>$n_time<>$n_solve<>$n_admcom<>\n";
			last;
		}
	}
	if($flag == 1) {
		unshift(@nuis, "$n_new\n");
		open(OUT,">nuisance/nui_list.dat");
		print OUT @nuis;
		close(OUT);
		&fileunlock("nuisance");
		&logview();
	} else {
		&fileunlock("nuisance");
		&error("データファイルが見つかりません。");
	}
}

sub get_ini {
	&error("プレイヤーファイルがありません。<br>IDを設定しなおしてください。") if !(-e "${player_dir}/".$id.".cgi");
	&pfl_read($id) if -e "${player_dir}/".$id.".cgi";
	&pass_chk if($pass ne $admin);
}

sub pfl_read {
	my $id = $_[0];
	undef(%P);
	chmod 0666, "${player_dir}/".$id.".cgi";
	open(PFL,"${player_dir}/".$id.".cgi") || &error("プレイヤーファイルが開けません");
	while(<PFL>){ chomp; ($key,$val) = split(/\t/); $P{$key} = $val; }
	close(PFL);
#	chmod 0000, "${player_dir}/".$id.".cgi";
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
	<link rel="stylesheet" href="$css" type="text/css">
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