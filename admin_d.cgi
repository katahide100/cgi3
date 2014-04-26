#!/usr/local/bin/perl

require './cust.cgi';
#require 'http://mesis.twimpt.com/dm/cust.cgi';
require 'duel.pl';
#require 'http://mesis.twimpt.com/dm/duel.pl';

&decode;
&get_cookie;

@alpha = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z');

if($F{'pass'} eq '') {
	&check;
} else {
	&set_cookie;
	&decode2;
	&get_ini;

	#if($P{'admin'} == 0) {
	if($P{'admin'} > 0) {
		if($F{'mode'} eq 'access')		{	&access;	}
		elsif($F{'mode'} eq 'ipban')		{	&ipban;		}
		elsif($F{'mode'} eq 'filelist')		{	&filelist;		}
		elsif($F{'mode'} eq 'fileedit')		{	&fileedit;		}
		elsif($F{'mode'} eq 'filewrite')	{	&filewrite;		}
		elsif($F{'mode'} eq 'filedelete')	{	&filedelete;		}
		elsif($F{'mode'} eq 'logedit')		{	&logedit;		}
		elsif($F{'mode'} eq 'logdelete')	{	&logdelete;		}
		elsif($F{'mode'} eq 'listmake')		{	&listmake;		}
		elsif($F{'mode'} eq 'logview')		{	&logview;		}
		elsif($F{'mode'} eq 'logwrite')		{	&logwrite;		}
		elsif($F{'mode'} eq 'tourmake')		{	&tourmake;		}
		elsif($F{'mode'} eq 'tourwrite')	{	&tourwrite;		}
		elsif($F{'mode'} eq 'tourdelete')	{	&tourdelete;		}
		elsif($F{'mode'} eq 'tourtime')		{	&tourtime;		}
		else					{	&main;		}
	#} elsif($P{'subadmin'} == 0) {
	} elsif($P{'subadmin'} > 0) {
		if($F{'mode'} eq 'logedit')		{	&logedit;		}
		elsif($F{'mode'} eq 'logdelete')	{	&logdelete;		}
		elsif($F{'mode'} eq 'logview')		{	&logview;		}
		elsif($F{'mode'} eq 'logwrite')		{	&logwrite;		}
		else					{	&main;		}
	} else {
		&error("管理者以外は入れません。");
	}

}

sub check {
	&header;
	print <<"EOM";
<form action="admin.cgi" name="send" method="post">
<input type="hidden" name="mode" value="login">
<table border="0" cellpadding="2">
<tr><th>ID</th><td>：<input type="text" name="id" value="$c_id" size="14"></td></tr>
<tr><th>パスワード</th><td>：<input type="password" name="pass" value="$c_pass" size="14"></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="管理者ツール起動"></td></tr>
</table>
</form>
EOM
	&footer;
}

sub main {
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
		if((M == "tourreset") || (M == "tourstart")) {
			entrance.action = "duelold.cgi";
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
管理お疲れ様です。<BR>
何をするか、下のメニューから選んでください。<BR><BR>


EOM
	#if($P{'admin'} == 0) {
	if($P{'admin'} > 0) {
		print <<"EOM";
[<A href="javascript:if(confirm('ユーザーデータを編集します')) sForm('filelist');">ユーザーデータの編集</A>]<BR><BR>
[<A href="javascript:if(confirm('アクセス規制IPのリストを編集します')) sForm('access');">アクセス規制ＩＰの変更</A>]<BR><BR>
[<A href="javascript:if(confirm('ユーザーリストを再構築します。\\n再構築には、しばらく時間がかかります')) sForm('listmake');">ユーザーリストの再構築</A>]<BR><BR>
[<A href="javascript:if(confirm('伝言板のログを削除します')) sForm('logedit');">伝言板のログを削除する</A>]<BR><BR>
[<A href="javascript:if(confirm('全ての部屋のログを見ます')) sForm('logview');">全ての部屋のログを見る</A>]<BR><BR>
[<A href="javascript:if(confirm('CGI公式トーナメントを開催します')) sForm('tourmake');">CGI公式トーナメントの開催</A>]<BR><BR>
[<A href="javascript:if(confirm('トーナメントを開催した後に、\\nここで最終処理を行います。\\n（これをやらないと開催されません。）')) location.href='taikai/parmission.php';">トーナメント開催の最終処理</A>]<BR><BR>
[<A href="javascript:if(confirm('CGI公式トーナメントを終了します')) sForm('tourdelete');">CGI公式トーナメントの終了</A>]<BR><BR>
[<A href="javascript:if(confirm('トーナメントの募集を開始します。\\nOKを選択すると前回のデータがリセットされ、新しく募集します。')) location.href='taikai/t_kanri_open.html';">CGI公式トーナメントの募集</A>]<BR><BR>
[<A href="javascript:if(confirm('トーナメントの募集をリセットします。')) location.href='taikai/reset.php';">CGI公式トーナメントの募集をリセット</A>]<BR><BR>
[<A href="javascript:if(confirm('開催パターンが抽選である\\nCGI公式トーナメントの受付を終了し、\\nデュエルを開始します。')) sForm('tourstart');">CGI公式トーナメントの抽選実行</A>]<BR><BR>
[<A href="javascript:if(confirm('CGI公式トーナメントを、\\n1回戦の組み合わせを変更せずにリセットします。\\n組み合わせをそのままに\\n最初からやり直すコマンドです。')) sForm('tourreset');">CGI公式トーナメントのリセット</A>]<BR><BR>
<!--[<A href="javascript:if(confirm('大会部屋の最終アクセス時間を再設定します')) sForm('tourtime');">大会部屋時間の再設定</A>]<BR><BR>-->
[<A href="javascript:if(confirm('対戦部屋がエラーで使えない場合はここでリセットできます。')) location.href='taikai/room_reset.php';">対戦部屋のリセット(部屋がエラーで使えなくなった場合に使用)</A>]<BR><BR>
[<A href="javascript:if(confirm('オリジナルカードを登録します。')) location.href='cardEdit/listCard/listCard.php';">オリジナルカード登録</A>]<BR><BR>
[<A href="javascript:if(confirm('メインページに戻ります')) sForm('index');">メインページへ戻る</A>]<BR><BR>
<B>－メモ－</B><BR>
パスワードを　aaMwrmlI6E95E　に設定すると、<BR>
パスワード：a　でアクセスできるようになります。<BR><BR>
掲示板の管理モードのパスワードは、xxxxxxxx　です。<BR>
荒らしが出現した際、管理モードに入り、対処を行ってください。<BR><BR>
EOM
	#} elsif($P{'subadmin'} == 0) {
	} elsif($P{'subadmin'} > 0) {
		print <<"EOM";
[<A href="javascript:if(confirm('伝言板のログを削除します')) sForm('logedit');">伝言板のログを削除する</A>]<BR><BR>
[<A href="javascript:if(confirm('全ての部屋のログを見ます')) sForm('logview');">全ての部屋のログを見る</A>]<BR><BR>
[<A href="javascript:if(confirm('メインページに戻ります')) sForm('index');">メインページへ戻る</A>]<BR><BR>
EOM
	}
	&footer;
}

sub access {
	&header;
	print <<"EOM";
排除するIPアドレスを、改行区切りで書いていってください。<BR>
制限する時、IPの途中までを対象にすれば、少しの変動では抜けられなくなります。<BR>
例えば、127.0.0.1を制限したい場合、127.0.0と書くのがベストです。<BR>
<form action="admin.cgi" name="send" method="post">
<input type="hidden" name="mode" value="ipban">
<input type="hidden" name="id" value="$F{'id'}">
<input type="hidden" name="pass" value="$F{'pass'}">
<table border="0" cellpadding="2">
<tr><td colspan="2" align="center"><textarea name="denyip" cols="50" rows="10">
EOM
	foreach $denyip (@denyip) {
		print "$denyip\n";
	}
	print <<"EOM";
</textarea></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="リストの上書き"></td></tr>
</table>
</form>
<A href="./admin.cgi?id=$F{'id'}&pass=$F{'pass'}">やめて戻る</A>
EOM
	&footer;
}

sub ipban {
	open(DNY, "> ./denyip.dat");
	print DNY $F{'denyip'};
	close(DNY);
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
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
アクセス規制ＩＰリストの更新が完了しました。<BR>
<BR>
<A href="javascript:sForm();">戻る</A>
EOM
	&footer;
}

sub filelist {
	opendir(DIR, "${player_dir}");
	my(@file_list) = sort readdir(DIR);
	closedir(DIR);
	#chmod(0666, "http://mesis.twimpt.com/dm//userlist.dat");
	chmod(0666, "./userlist.dat");
	open(USR, "./userlist.dat");
	#open(USR, "http://mesis.twimpt.com/dm//userlist.dat");
	@userlist = <USR>;
	close(USR);
#	chmod(0000, "./userlist.dat");

	$usercnt = $#userlist + 1;

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
		entrance.alpha.value = R;
		entrance.file.value = C;
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="alpha" value="">
	<input type="hidden" name="file" value="">
	<input type="hidden" name="name" value="">
編集するファイルを、選んでください。<BR>
ユーザーのファイルは、ID_pflです。<BR><BR>
<table border="0" cellpadding="2">
<tr><th>アルファベットから検索</th>
EOM
print "<td align=\"left\">：";
	foreach $alpha_s (@alpha) {
		print "[<A href=\"javascript:sForm('filelist', '$alpha_s');\">$alpha_s</A>] ";
	}
print "</td></tr>";
print <<"EOM";
<tr><th>ユーザーリストから検索</th>
EOM
print "<td align=\"left\">：";
	$count = 0;
	foreach $userdata (@userlist) {
		if($count % 100 == 0) {
			print "[<A href=\"javascript:sForm('filelist', '". ($count / 100) ."');\">". ($count + 1) . " ～ " . ($count + 100) . "</A>] ";
		}
		$count ++;
	}
print "総数：$usercnt</td></tr>";
print <<"EOM";
<tr><th>名前で検索</th><td align="left">：<INPUT type="text" size="20" name="search" value="$F{'name'}">&nbsp;<INPUT type="button" value="検索" onClick="document.entrance.name.value = document.entrance.search.value; sForm('filelist');"></td></tr>
</form>
<BR>
<table border="0" cellpadding="2">
EOM
	if($F{'name'} ne '') {
		print "<tr><td>ファイル名</td><td>ID</td><td>名前</td><td>コメント</td><td>オプション</td></tr>\n";
		foreach $userdata (@userlist) {
			my($l_id, $l_name, $l_com) = split(/\t/, $userdata);
			print "<tr><td>[<A href=\"javascript:sForm('fileedit', '', '${l_id}_pfl');\">${l_id}_pfl</A>]</td><td>$l_id</td><td>$l_name</td><td>$l_com</td><td>[<A href=\"javascript:if(confirm('本当に削除しますか？')) sForm('filedelete', '', '${l_id}_pfl');\">削除</A>]</td></tr>\n" if($l_name =~ /$F{'name'}/);
		}
	} elsif($F{'alpha'} =~ /^[0-9]*$/) {
		$F{'alpha'} = '0' if($F{'alpha'} eq '');
		$for_start = $F{'alpha'} * 100;
		$for_end = $for_start + 100;
		$for_end = $#userlist + 1 if($for_end > $#userlist + 1);
		print "<tr><td>ファイル名</td><td>ID</td><td>名前</td><td>コメント</td></tr>\n";
		for(my($i) = $for_start; $i < $for_end; $i ++) {
			my($l_id, $l_name, $l_com) = split(/\t/, $userlist[$i]);
			print "<tr><td>[<A href=\"javascript:sForm('fileedit', '', '${l_id}_pfl');\">${l_id}_pfl</A>]</td><td>$l_id</td><td>$l_name</td><td>$l_com</td><td>[<A href=\"javascript:if(confirm('本当に削除しますか？')) sForm('filedelete', '', '${l_id}_pfl');\">削除</A>]</td></tr>\n";
		}
	} else {
		$F{'alpha'} = 'a' if($F{'alpha'} eq '');
		print "<tr><td>ファイル名</td></tr>\n";
		foreach $file (@file_list) {
			next if(($file eq '.') || ($file eq '..') || ($file !~ /^$F{'alpha'}/i));
			print "<tr><td>[<A href=\"javascript:sForm('fileedit', '', '$file');\">$file</A>]</td><td>[<A href=\"javascript:if(confirm('本当に削除しますか？')) sForm('filedelete', '', '$file');\">削除</A>]</td></tr>\n";
		}
	}
	print <<"EOM";
</table>
<BR><BR><A href="javascript:sForm();">やめて戻る</A>
EOM
	&footer;
}

sub fileedit {
	%TP = ();
	chmod 0666, "${player_dir}/".$F{'file'};
	open(PFL, "${player_dir}/$F{'file'}");
	while(<PFL>){ chop; ($KEY,$VAL) = split(/\t/); $TP{$KEY} = $VAL; }
	close(PFL);
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
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
<form action="admin.cgi" name="send" method="post">
<input type="hidden" name="mode" value="filewrite">
<input type="hidden" name="id" value="$F{'id'}">
<input type="hidden" name="pass" value="$F{'pass'}">
<input type="hidden" name="file" value="$F{'file'}">
<table border="0" cellpadding="2">
<tr><th>ファイル名</th><td colspan="2" align="left">：$F{'file'}</td></tr>
EOM
foreach $key (keys(%TP)) {
    print "<tr><th>${key}</th><td align=\"left\">：<input type=\"text\" name=\"${key}_hash\" value=\"$TP{$key}\" size=\"50\"></td><td>この要素を消去&nbsp;<input type=\"checkbox\" name=\"${key}_hash_delete\" value=\"1\"></td></tr>\n";
}
	print <<"EOM";
<tr><th><input type="text" name="new_key_tmp" value="" size="10"></th><td colspan="2" align="left">：<input type="text" name="new_hash_tmp" value="" size="50"></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="編集完了"></td></tr>
</table>
</form>
<A href="javascript:sForm();">やめて戻る</A>
EOM
	&footer;
}

sub filewrite {
	%TP = ();
	chmod 0666, "${player_dir}/".$F{'file'};
	open(PFL, "${player_dir}/$F{'file'}");
	while(<PFL>){ chop; ($KEY,$VAL) = split(/\t/); $TP{$KEY} = $VAL; }
	close(PFL);
	foreach $key (keys(%F)) {
		if($key =~ /(.*?)\_hash$/) {
			$key_name = $1;
			$TP{$key_name} = $F{$key};
			delete($TP{$key_name}) if($F{$key.'_delete'});
		}
	}
	$TP{$F{'new_key_tmp'}} = $F{'new_hash_tmp'}	if($F{'new_key_tmp'} ne '');
	open(PFL, "> ${player_dir}/$F{'file'}");
	foreach $key(keys(%TP)){ print PFL "$key\t$TP{$key}\n"; }
	close(PFL);
	chmod 0000, "${player_dir}/".$F{'file'};
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
		entrance.file.value = R;
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="file" value="">
</form>
編集が完了しました。<BR><BR>
[<A href="javascript:sForm('fileedit', '$F{'file'}');">引き続き編集する</A>]<BR><BR>
[<A href="javascript:sForm('filelist');">リストに戻る</A>]<BR><BR>
[<A href="javascript:sForm();">メニューに戻る</A>]
EOM
	&footer;
}

sub filedelete {
	chmod 0666, "${player_dir}/".$F{'file'};
	unlink "${player_dir}/".$F{'file'};
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
		entrance.file.value = R;
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="file" value="">
</form>
削除が完了しました。<BR><BR>
[<A href="javascript:sForm('filelist');">リストに戻る</A>]<BR><BR>
[<A href="javascript:sForm();">メニューに戻る</A>]
EOM
	&footer;
}

sub listmake {
	opendir(DIR, "${player_dir}") || &error("ディレクトリを開けませんでした");
	my(@file_list) = sort readdir(DIR);
	closedir(DIR);

	$finish = 0;

	chmod(0666, "./userlist.dat");
	open(USR, "< ./userlist.dat") || &error("読み込めませんでした");
	@userlist = <USR>;
	close(USR);
	@userlist = () if($F{'process'} == 0);
	for ($i = $F{'process'} * 200; $i < min($F{'process'} * 200 + 200, $#file_list + 1); $i ++) {
		next if($file_list[$i] !~ /\.cgi$/);
		%TP = ();
		chmod 0666, "${player_dir}/".$file_list[$i];
		open(PFL, "${player_dir}/$file_list[$i]");
		while(<PFL>){ chop; ($KEY,$VAL) = split(/\t/); $TP{$KEY} = $VAL; }
		close(PFL);
#		$TP{'white'} = $TP{'whitelist'};
#		delete $TP{'whitelist'};
#		$TP{'black'} = $TP{'blacklist'};
#		delete $TP{'blacklist'};
#		open(PFL, "> ${player_dir}/$file_list[$i]");
#		foreach $key(keys(%TP)){ print PFL "$key\t$TP{$key}\n"; }
#		close(PFL);
#		chmod 0000, "${player_dir}/".$file_list[$i];
		push(@userlist, "$TP{'id'}\t$TP{'name'}\t$TP{'comment'}\n");
	}
	open(USR, "> ./userlist.dat") || &error("書き込めませんでした");
	print USR @userlist;
	close(USR);
#	chmod(0000, "./userlist.dat");

	$number = $F{'process'} + 1;

	$finish = 1 if($F{'process'} * 200 + 200 >= $#file_list + 1);

	$remainder = "あと " . (int($#file_list / 200) - $number) . "回";

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
	function sForm(M) {
		entrance.mode.value = M;
		if(M == "index") {
			entrance.action = "index.cgi";
		}
		entrance.target = (M == "prof") ? "_blank" : "_self";
		entrance.submit();
	}
// --></script>
</head>
EOM
	if($finish) {
		print <<"EOM";
<body>
	<div align="center">
		<h1>$title</h1>
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
リストの再構築が完了しました。<BR><BR>
[<A href="javascript:sForm();">メニューに戻る</A>]
EOM
	} else {
		print <<"EOM";
<body onLoad="sForm('listmake');">
	<div align="center">
		<h1>$title</h1>
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="listmake">
	<input type="hidden" name="process" value="$number">
</form>
次の段階へ進みます。<BR>
しばらくお待ちください・・・。<BR>
($remainder)<BR><BR>
[<A href="javascript:sForm();">中断</A>]
EOM
	}

	&footer;

}

sub logview {
	&header;
	$F{'cou'} = 10 if(!$F{'cou'});
	print <<"EOM";
<table border="0" cellpadding="2">
EOM
	for($i = 1; $i <= $heyakazu; $i ++) {
		print "<tr>" if(($i - 1) % 3 == 0);
		print "<td>部屋番号$i<BR>\n<textarea cols=\"80\" rows=\"12\" wrap=\"off\">\n";
		chmod("${room_dir}/".$roomst.$i."_log.cgi", 0666);
		open(DB,"${room_dir}/".$roomst.$i."_log.cgi");
		my $cou = 0;
		while (<DB>) {
			last if $cou >= $F{'cou'};
			my ($msgman,$msg,$msgmode) = split(/<>/,$_);
			$msg =~ s/<.*>//g;
			if($msgmode eq "system") {
				print "$msg\n";
			} elsif(($msgmode eq "message1") || ($msgmode eq "message2") || ($msgmode eq "admin")) {
				print $msgman eq "null" ? "$msg\n" : "$msgman ＞ $msg\n";
			}
			$cou++;
		}
		close(DB);
		chmod("${room_dir}/".$roomst.$i."_log.cgi", 0000);
		print "</textarea></td>\n";
		print "</tr>\n" if(($i - 1) % 3 == 2);
	}
	print <<"EOM";
<form action="admin.cgi" method="post" name="reload">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="logview">
<tr><td colspan="3" align="center">表示数 <input type="text" size="5" name="cou" value="$F{'cou'}"> 行で <input type="submit" value="リロード"></td></tr>
</form>
<hr>
<form action="admin.cgi" method="post" name="entrance" onSubmit="if(!confirm('本当に全部屋に向けて発言しますか？')) return false;">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="logwrite">
<tr><td colspan="3" align="center">メッセージ <input type="text" size="30" name="msg" value=""> で、全部屋に <input type="submit" value="発言"></td></tr>
</form>
</table>
<A href="./admin.cgi?id=$F{'id'}&pass=$F{'pass'}">やめて戻る</A>
EOM
	&footer;
}

sub logwrite {
	for($room = 1; $room <= $heyakazu; $room ++) {
		chmod("${room_dir}/".$roomst.$room."_log.cgi", 0666);
		if(open(DB,"${room_dir}/".$roomst.$room."_log.cgi")) {
			@lines = <DB>;
			close(DB);
			&regist($P{'name'},$F{'msg'},"admin");
		}
		chmod("${room_dir}/".$roomst.$room."_log.cgi", 0000);
	}
	&logview;
}

sub tourmake {
	&cardread;
	%T = ();
	chmod 0666, "./tour/part.dat";
	open(TRT, "./tour/part.dat");
	while(<TRT>){ chop; ($KEY,$VAL) = split(/\t/); $T{$KEY} = $VAL; }
	close(TRT);
	@p_fame = split(/\,/, $T{'p_fame'});
	@fame = split(/\,/, $T{'fame'});
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
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
<form action="admin.cgi" name="send" method="post">
<input type="hidden" name="mode" value="tourwrite">
<input type="hidden" name="id" value="$F{'id'}">
<input type="hidden" name="pass" value="$F{'pass'}">
<table border="0" cellpadding="2" width="320">
<tr><td>大会名称: <input type="text" size="64" name="title" value="$T{'title'}"><BR>
例: 第1回 対戦CGI ex 公式トーナメント</td></tr>
<tr><td><hr></td></tr>
<tr><td>参加人数: <select name="scale">
EOM
	for(my($i) = 1; $i <= 5; $i ++) {
		print "<option value=\"$i\"";
		print " selected" if($i == 3);
		print ">";
		print 2 ** $i * 2;
		print "人</option>\n";
	}
	print <<"EOM";
</select></td></tr>
<tr><td><hr></td></tr>
<tr><td>基本殿堂: <select name="dendou">
<option value="0">殿堂なし</option>
<option value="1" selected>殿堂あり</option>
<option value="2">ＡＧ環境</option>
<option value="3">ＳＧＬ環境</option>
<option value="4">ゼロルール</option>
<option value="10">おやぢ電動</option>
<option value="11">CGIex公式</option>
<option value="12">殿堂禁止</option>
</select></td></tr>
<tr><td><hr></td></tr>
<tr><td>追加Ｐ殿堂入りカード<BR>
<TEXTAREA name="p_fame" style="width: 240px; height: 80px;">
EOM
	foreach $card (@p_fame) {
		print "$c_name[$card]\n";
	}
	print <<"EOM";
</TEXTAREA></td></tr>
<tr><td><hr></td></tr>
<tr><td>追加殿堂入りカード<BR>
<TEXTAREA name="fame" style="width: 240px; height: 80px;">
EOM
	foreach $card (@fame) {
		print "$c_name[$card]\n";
	}
	print <<"EOM";
</TEXTAREA></td></tr>
<tr><td><hr></td></tr>
<tr><td>ポイント制限: <select name="point">
<option value="-1">制限なし</option>
<option value="0">0p</option>
<option value="5">5p以下</option>
<option value="10">10p以下</option>
<option value="15">15p以下</option>
<option value="20">20p以下</option>
<option value="25" selected>25p以下</option>
<option value="30">30p以下</option>
<option value="35">35p以下</option>
<option value="40">40p以下</option>
<option value="45">45p以下</option>
<option value="50">50p以下</option>
</select></td></tr>
<tr><td><hr></td></tr>
<tr><td>参加受付モード: <select name="accept">
<option value="0" selected>先着モード</option>
<option value="1">抽選モード</option>
</select></td></tr>
<tr><td><hr></td></tr>
<tr><td>開催形式: <select name="type">
<option value="0" selected>公式トーナメント</option>
<option value="1">通常トーナメント</option>
<option value="2">練習トーナメント</option>
</select></td></tr>
<tr><td><hr></td></tr>
<tr><td>パスワード制限: <input type="text" size="16" name="tpass" value="$T{'tpass'}"><br>(未入力で制限なし)</td></tr>
<tr><td><hr></td></tr>
<tr><td><input type="submit" value="大会を開催する"></td></tr>
</table>
</form>
<A href="javascript:sForm();">やめて戻る</A>
EOM
	&footer;
}

sub tourwrite {
	&cardread;
	&error("パスワードは8文字以内にしてください。") if(length($F{'tpass'}) > 8);
	&error("パスワードには半角英数字のみが使用可能です。") if(($duelid ne '') && ($F{'tpass'} !~ /^[A-Za-z0-9]*$/));
	%T = ();
	@p_fame = ();
	@fame = ();
	if($F{'p_fame'}){
		%TX = ();
		%TXC = ();
		@tmp = split(/\n/,$F{'p_fame'});
		foreach my $card(@tmp){ $TX{$card}++ if $card; }
		foreach my $i(0..$#c_name){
			if($TX{$c_name[$i]}){
				$TXC{$c_name[$i]} = 1;
				push(@p_fame, $i);
			}
		}
		foreach $key (keys(%TX)){ $errormsg .= "Ｐ殿堂: <strong>$keyというカードは存在しません</strong><br>\n" unless $TXC{$key}; }
	}
	if($F{'fame'}){
		%TX = ();
		%TXC = ();
		@tmp = split(/\n/,$F{'fame'});
		foreach my $card(@tmp){ $TX{$card}++ if $card; }
		foreach my $i(0..$#c_name){
			if($TX{$c_name[$i]}){
				$TXC{$c_name[$i]} = 1;
				push(@fame, $i);
			}
		}
		foreach $key (keys(%TX)){ $errormsg .= "殿堂: <strong>$keyというカードは存在しません</strong><br>\n" unless $TXC{$key}; }
	}
	$T{'point'} = int($F{'point'});
	$T{'scale'} = $F{'scale'};
	$T{'number'} = 0;
	$T{'remain'} = ($F{'accept'} == 0) ? 2 ** $F{'scale'} * 2 : 0;
	$T{'third'} = 0;
	$T{'dendou'} = $F{'dendou'};
	$T{'accept'} = $F{'accept'};
	$T{'title'} = $F{'title'};
	$T{'tpass'} = $F{'tpass'};
	$T{'type'} = $F{'type'};
	$T{'p_fame'} = join(',', @p_fame);
	$T{'fame'} = join(',', @fame);;
	&filelock("tr");
	for(my($i) = 1; $i <= 2 ** $T{'scale'} * 2; $i ++) {
		chmod (0666, "./${room_dir}/duelistt${i}.cgi", "./${room_dir}/duelistt${i}_log.cgi", "./${room_dir}/duelistt${i}_time1.cgi", "./${room_dir}/duelistt${i}_time2.cgi", "./${room_dir}/duelistt${i}_card.cgi");
		unlink("./${room_dir}/duelistt${i}.cgi", "./${room_dir}/duelistt${i}_log.cgi", "./${room_dir}/duelistt${i}_time1.cgi", "./${room_dir}/duelistt${i}_time2.cgi", "./${room_dir}/duelistt${i}_card.cgi");
	}
	chmod 0666, "./tour/part.dat";
	open(TRT, "> ./tour/part.dat");
	foreach $key(keys(%T)){ print TRT "$key\t$T{$key}\n"; }
	close(TRT);
	&fileunlock("tr");
	chmod 0000, "./tour/part.dat";
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
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
${errormsg}<BR>
大会の開催準備をしました。<BR><BR>
[<A href="javascript:sForm();">メニューに戻る</A>]
EOM
	&footer;
}

sub tourdelete {
	%T = ();
	chmod 0666, "./tour/part.dat";
	open(TRT, "./tour/part.dat");
	while(<TRT>){ chop; ($KEY,$VAL) = split(/\t/); $T{$KEY} = $VAL; }
	close(TRT);
	for(my($i) = 1; $i <= 2 ** $T{'scale'}; $i ++) {
		unlink("./${room_dir}/duelistt${i}.cgi", "./${room_dir}/duelistt${i}_log.cgi", "./${room_dir}/duelistt${i}_time1.cgi", "./${room_dir}/duelistt${i}_time2.cgi", "./${room_dir}/duelistt${i}_card.cgi");
	}
	$T{'scale'} = 0;
	$T{'remain'} = 0;
	$T{'third'} = 0;
	$T{'debug'} = 0;
	&filelock("tr");
	chmod 0666, "./tour/part.dat";
	open(TRT, "> ./tour/part.dat");
	foreach $key(keys(%T)){ print TRT "$key\t$T{$key}\n"; }
	close(TRT);
	&fileunlock("tr");
	chmod 0000, "./tour/part.dat";
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
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
大会を終了をしました。<BR><BR>
[<A href="javascript:sForm();">メニューに戻る</A>]
EOM
	&footer;
}

sub tourtime {
	&filelock("tr");
	open(TRT,"tour/part.dat") || &error("大会データが開けません");
	while(<TRT>){ chomp; ($key,$val) = split(/\t/); $T{$key} = $val; }
	close(TRT);
	&fileunlock("tr");

	for(my($i) = 1; $i <= 2 ** $T{'scale'} * 2; $i ++) {
		open(PFL,"${room_dir}/".$roomst."t".$i.'.cgi') || &error("データファイルが開けません");
		my(@tmppfl) = <PFL>;
		&error("データファイルが壊れているか、読み込みに失敗した可能性があります。") if($#tmppfl < 0);
		foreach(@tmppfl){ chomp; ($key,$val) = split(/\t/); $G{$key} = $val; }
		close(PFL);
		for(my($j) = 1; $j <= 2; $j ++) {
			$G{'date'.$j} = $times;
			$G{'tourtime'.$j} = 0;
		}
		open(PFL,"> ${room_dir}/".$roomst."t".$i.'.cgi') || &error("データファイルが開けません");
		foreach $key(keys(%G)){ print PFL "$key\t$G{$key}\n"; }
		close(PFL);
	}
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
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
大会部屋の最終アクセス時間を再設定しました。<BR><BR>
[<A href="javascript:sForm();">メニューに戻る</A>]
EOM
	&footer;
}

sub regist {
	my ($msgman,$msg,$msgmode) = @_;
	&filelock;
	open(IN,"${room_dir}/".$roomst.$room."_log.cgi");
	@lines = <IN>;
	close(IN);
	unshift(@lines,"$msgman<>$msg<>$msgmode<>\n") if($msg ne "");
	open(OUT,">${room_dir}/".$roomst.$room."_log.cgi") || &error("ログファイルに書き込めません");
	print OUT @lines;
	close(OUT);
	&fileunlock;
}

sub logedit {
	chmod 0666, "word.dat";
	open(WORD,"word.dat") || &error("伝言ファイルが開けません。");
	@lines = <WORD>;
	close(WORD);

	&header;
	print <<"EOM";
<p align="center">
<form action="admin.cgi" name="send" method="post">
<input type="hidden" name="mode" value="logdelete">
<input type="hidden" name="id" value="$F{'id'}">
<input type="hidden" name="pass" value="$F{'pass'}">
<table border="0" width="800" cellpadding="3" cellspacing="0" bgcolor="#FFFFFF">
<tr><td>
<table width="100%" border="0" cellpadding="0" cellspacing="0">
EOM
	shift(@lines);
	foreach(@lines){
		my($num,$wdate,$id,$name,$com,$pass,$ip,$order) = split(/<>/);
		my($symbol) = "";
		if($order ne '') {
			$symbol = "<font color=\"$order_color{$order}\">$order_symbol{$order}</font>";
		}
		print <<"EOM";
<tr valign="top">
<td nowrap><input type="checkbox" name="dnum_$num" value="1"></td>
<td nowrap>[$num]&nbsp;$name&nbsp;$symbol</td>
<td nowrap>&gt;&nbsp;</td>
<td>$com<small> ($wdate) - $ip</small></td>
</tr>
<tr><td colspan="4"><hr size="1" color="#000000"></td></tr>
EOM
	}
	print <<"EOM";
<tr><td colspan="4" align="center"><input type="submit" value="選択した記事を削除する"></td></tr>
</table>
</td></tr>
</table>
</form>
</p>
<A href="./admin.cgi?id=$F{'id'}&pass=$F{'pass'}">やめて戻る</A>
EOM
	&footer;
}

sub logdelete {
	chmod 0666, "word.dat";
	open(WORD,"word.dat") || &error("伝言ファイルが開けません。");
	@lines = <WORD>;
	close(WORD);
	my($top_data) = shift(@lines);
	foreach(@lines){
		my($num,$wdate,$id,$name,$com,$pass,$ip,$order) = split(/<>/);
		$_ = '' if($F{"dnum_$num"});
	}
	unshift(@lines, $top_data);
	chmod 0666, "word.dat";
	open(OUT,">word.dat") || &error("伝言ファイルに書きこめません。");
	print OUT @lines;
	close(OUT);

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
		if(M == "index") {
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
<form action="admin.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
伝言板の記事を削除しました。<BR><BR>
[<A href="javascript:sForm();">メニューに戻る</A>]
EOM
	&footer;
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