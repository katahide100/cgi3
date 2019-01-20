#!/usr/local/bin/perl

require "cust.cgi";
require "duel.pl";

&get_cookie;
$pc_chk = int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) if($pc_chk eq '');
&decode;
&decode2;
&pfl_read($id) if -e "${player_dir}/".$id.".cgi";
($win,$lose) = split(/-/,$P{'shohai'});
$win = 0 unless $win;
$lose = 0 unless $lose;
$name = $P{'name'};
&set_cookie if $F{'id'} ne '';
&entry if $F{'mode'} eq "entry";
&modify if $F{'mode'} eq "modify";
&regist if $F{'mode'} eq "regist";
&welcome;

sub welcome {
	open(DAT, "./index.dat");
	my($top_comment) = join('', <DAT>);
	close(DAT);
	my $tesst = "<p style=\"color:red\">※このゲームは最初にIDとパスワードを登録しないと遊べません。<br>　初めて遊ぶ方は、必ず登録フォームから『対戦CGIに登録』ボタンを押して登録してください。</p>" if !($c_id) || !($c_pass);
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
with(document);
function send(flag){
	if ('$ENV{'REMOTE_ADDR'}' == '123.254.57.186') {
		alert("管理人からメッセージがあるようです。");
		entrance.action = "happuppu.cgi";
	} else {
		entrance.action = (flag == "deck") ? "deck.cgi" : (flag == "group") ? "group.cgi" : (flag == "list") ? "list.cgi" : (flag == "nuisance") ? "nuisance.cgi" : "taisen.cgi";
	}

	entrance.submit();
}

// --></script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65518878-1', 'auto');
  ga('send', 'pageview');

</script>
<meta name="description" content="デュエルマスターズがウェブ上で他の人と対戦できる！ 発売されている全てのカードから自由自在にデッキを構築でき、一人での練習プレイ機能も完備。"/>
<meta name="keywords" content="デュエルマスターズ,対戦,カード,交流,CGI"/>
</head>
<body>
<div align="center">
EOM
	($sec,$min,$hour,$mday,$mon,$year) = localtime(time);
	$mon++;
	print"<h1>$title</h1>";
	if(($mon == 7) && ($mday == 30)) {
		print <<"EOM";
<table border="0" width="1260" cellspacing="0" cellpadding="10">
EOM
	} else {
		print <<"EOM";
<table border="0" width="1160" cellspacing="0" cellpadding="10">
EOM
	}
	print <<"EOM";
<tr><td style="border-style: none;vertical-align: top;">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 広告ユニット1 -->
<ins class="adsbygoogle"
     style="display:inline-block;width:160px;height:600px"
     data-ad-client="ca-pub-1974859203649104"
     data-ad-slot="1784652942"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td><td class="table">
<div align="center">
総数：<img src="dayx/dayx.cgi?gif" title="このページに来た総計人数"> 今日：<img src="dayx/dayx.cgi?today" title="今日の来た人の数"> 昨日：<img src="dayx/dayx.cgi?yes" title="昨日の来た人の数。"><br>
<hr>
<table border="0" cellspacing="0">
<tr valign="top"><td>
<form action="index.cgi" method="post" name="entrance">
<input type="hidden" name="mode" value="modify">
－ログインフォーム－<BR>
<table border="0" cellpadding="2">
<tr><th>ID</th><td>：<input type="text" name="id" value="$c_id" size="14"></td></tr>
<tr><th>パスワード</th><td>：<input type="password" name="pass" value="$c_pass" size="14"></td></tr>
</table>
<p><input type="submit" value="登録情報の変更"></p>
<p><input type="button" value="対戦画面へ移動" onClick="send('taisen');"></p>
<p><input type="button" value="デッキの構築" onClick="send('deck');"></p>
<p><input type="button" value="グループの編集" onClick="send('group');"></p>
<p><input type="button" value="リストの編集" onClick="send('list');"></p>
<p><input type="button" value="伝言板の過去ログ" onClick="send('log');"></p>
<p><input type="button" value="迷惑行為一覧" onClick="send('nuisance');"></p>
</form>
<hr>
<form action="index.cgi" method="post" name="register">
<input type="hidden" name="mode" value="entry">
－登録フォーム－<BR>
<table border="0" cellpadding="2">
<tr><th>ID</th><td>：<input type="text" name="id" value="" size="14"></td></tr>
<tr><th>パスワード</th><td>：<input type="password" name="pass" value="" size="14"></td></tr>
<tr><td colspan="2" align="center"></td></tr>
<tr><td colspan="2" align="center"><input type="checkbox" name="set" value="1"> 登録時にIDを自分で決める</td></tr>
</table>
<p><input type="submit" value="対戦CGIに登録"></p>
</form>
<hr>
</td><td>
EOM
	if(($mon == 12) && ($mday == 25)) {
		print <<"EOM";
<a href="./christmas.cgi">クリスマスの勲章が入手できるらしいですよ！！</a><hr>
EOM
	} elsif(($mon == 2) && ($mday == 14)) {
		print <<"EOM";
<a href="./valentine.cgi">今日はただの日</a><hr>
EOM
	} elsif(($mon == 4) && ($mday == 1)) {
		print <<"EOM";
<span style="color:#FF0000;font-size:36px;">おめでとうございます！！</span><br><br>
あなたは<span style="color:#888800">見事</span>に<span style="color:#008800"><b>管理陣営</b></span>の一人に<big>選ばれました！</big><br>
<b>管理権限</b>を授与する処理をするため、今すぐ下のリンクを<span style="color:#000088"><big>クリック</big></span>してください！！<br>
<span style="color:#FF0000">→</span><a href="./getadmin.cgi"><big><b>ココをクリック！！</b></big></a><span style="color:#FF0000">←</span><hr>
EOM
	}
	print <<"EOM";
$top_comment
<hr>
<table border="0" cellspacing="0" cellpadding="0">
<tr><th>■ 新機能に関する説明</th></tr>
<tr><td>　この対戦CGIでは、「禁止グループ」というものを設けています。<BR>
トップから「グループの編集」へ入り、<BR>
デッキの構築と同じような感覚でグループの作成を行います。<BR>
グループの枚数はデッキと違い、制限はありません。<BR>
１枚だけでも、１０枚でも、はたまた１００枚でも可能です。<BR>
グループの作成が完了したら、次は対戦画面で部屋を作成する時に、<BR>
作ったグループを選択して入室すれば、禁止グループの設定は完了です。<BR>
禁止グループで設定されたカードは、<BR>
自分も相手もそのデュエルで使うことはできません。(入室できません)</td></tr>
</table>
<hr>
<BR>
管理者 <A href="mailto:katahide100\@gmail.com">kat</A>　　共同制作者　ENTER　おんせん　げすと☆　人参　エイラ<br>
CGI提供 <A href="mailto:mewsyoui\@hotmail.com">メシス</A>
<hr>
<!--<a href="count/getaccess.cgi?mode=view" target="_blank">-->
<script language="javascript">
<!--
//ref = escape(document.referrer);
//if(ref != '') document.write('<img src="count/getaccess.cgi?r='+ref+'" border="0">');
//-->
</script><br>
<small>アクセスログ</small>
</a>
</div>
</td></tr>
</table>
</td><td style="border-style: none;vertical-align: top;">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 広告ユニット1 -->
<ins class="adsbygoogle"
     style="display:inline-block;width:160px;height:600px"
     data-ad-client="ca-pub-1974859203649104"
     data-ad-slot="1784652942"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td></tr>
</table>
EOM
	&footer2;
}

sub entry{
	if($F{'set'}) {
		&error("IDの形式が正しくありません。<BR>半角英字の大文字３つ、数字５つにしてください。<BR>例：ABC012345") unless($F{'id'} =~ /^[A-Z]{3}[0-9]{5}$/);
		&error("そのIDは既に存在します。<BR>別のIDにしてください。") if((-e "${player_dir}/".$id.".cgi") || (-e "${player_dir}/".$id."a.cgi") || (-e "${player_dir}/".$id."m.cgi"));
	} else {
		$id = &make_id;
	}

	$msg = "※上記のIDで新しくプレイヤーファイルを作成します。名前とパスワードを設定してください。<br>";
	&header;
	print <<"EOM";
</head>
<body>
<div align="center">
<h1>$title</h1>
<table border="1" width="600" cellspacing="0" cellpadding="10" class="table"><tr><td>
<form action="index.cgi" method="post">
<input type="hidden" name="mode" value="regist">
<input type="hidden" name="id" value="${id}">
<p>$msg
※IDは変更することができませんので、忘れないようにしてください。<br>
※パスワードは半角英数（a～z、A～Z、0～9）8文字以内で入力してください。<br>
※メッセージは対戦者データ画面で表示されます。改行しないで入力してください。<br>
※メッセージにタグを使うことはできません。<br>
<table border="0" cellpadding="2" align="center">
<tr><th>ID</th><td align="left">：${id}</td></tr>
<tr><th>名前</th><td align="left">：<input type="text" name="name" value="" size="14"></td></tr>
<tr><th>パスワード</th><td align="left">：<input type="password" name="pass" value="$pass" size="14"></td></tr>
<tr><th valign="top">パスワード確認</th><td valign="top" align="left">：<input type="password" name="pass2" size="14"><br>　確認のため、もう一度同じパスワードを入力してください。</td></tr>
<tr><th>モード選択</th><td align="left">：<select name="age"><option value="1" selected>新モード</option><option value="0">旧モード</option></select></td></tr>
<tr><th>ロビー選択</th><td align="left">：<select name="lobby"><option value="1" selected>新モード</option><option value="0">旧モード</option></select></td></tr>
<tr><th>伝言板番号</th><td align="left">：<select name="channel">
EOM
	for (my($i) = 1; $i <= 9; $i++) {
		my($selected) = ($i == 1) ? " selected" : "";
		print "<option value=\"$i\"$selected>チャンネル $i</option>";
	}
	print <<"EOM";
</select></td></tr>
<tr><th>メッセージ</th><td align="left">：<input type="text" name="comment" value="" size="50"></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="登録">
</td></tr>
</table>
</form>
</td></tr></table>
EOM
	&footer2;
}

sub modify{
	&error("IDが間違っています。") if(!-e "${player_dir}/".$id.".cgi");
	&pfl_read($id);
	&pass_chk;

	$msg = "※現在設定されているパスワード、名前、もしくはメッセージを変更します。<br>";
	if($P{'age'} == 1) {
		$agesel0 = "";
		$agesel1 = " selected";
	} else {
		$agesel0 = " selected";
		$agesel1 = "";
	}
	if($P{'lobby'} == 1) {
		$lobbysel0 = "";
		$lobbysel1 = " selected";
	} else {
		$lobbysel0 = " selected";
		$lobbysel1 = "";
	}
	&header;
	print <<"EOM";
</head>
<body>
<div align="center">
<h1>$title</h1>
<table border="1" width="600" cellspacing="0" cellpadding="10" class="table"><tr><td> 
<form action="index.cgi" method="post">
<input type="hidden" name="mode" value="regist">
<input type="hidden" name="id" value="$id">
<p>$msg</p>
<table border="0" cellpadding="2" align="center">
<input type="hidden" name="cpass" value="$pass">
<tr><th>ID</th><td align="left">：$id</td></tr>
<tr><th>名前</th><td align="left">：<input type="text" name="name" value="$name" size="14"></td></tr>
<tr><th>パスワード</th><td align="left">：<input type="password" name="pass" value="$pass" size="14"></td></tr>
<tr><th valign="top" align="left">パスワード確認</th><td valign="top" align="left">：<input type="password" name="pass2" size="14"><br>　確認のため、もう一度同じパスワードを入力してください。</td></tr>
<tr><th>モード選択</th><td align="left">：<select name="age"><option value="1"$agesel1>新モード</option><option value="0"$agesel0>旧モード</option></select></td></tr>
<tr><th>ロビー選択</th><td align="left">：<select name="lobby"><option value="1"$lobbysel1>新モード</option><option value="0"$lobbysel0>旧モード</option></select></td></tr>
<tr><th>伝言板番号</th><td align="left">：<select name="channel">
EOM
	for (my($i) = 1; $i <= 9; $i++) {
		my($selected) = ($i == $P{'channel'}) ? " selected" : "";
		print "<option value=\"$i\"$selected>チャンネル $i</option>";
	}
	print <<"EOM";
</select></td></tr>
<tr><th>メッセージ</th><td align="left">：<input type="text" name="comment" value="$P{'comment'}" size="50"></td></tr>
<tr><th>勲章選択</th><td align="left">
EOM
	print "<input type=\"radio\" name=\"order\" value=\"\"";
	print " checked" if($P{'order'} eq '');
	print "> 勲章なし<br>\n";
	foreach $order_name (@order_per) {
		if($P{'order_' . $order_name}) {
			print "<input type=\"radio\" name=\"order\" value=\"$order_name\"";
			print " checked" if($P{'order'} eq $order_name);
			print "> <img src=\"${symbol_dir}/symbol_${order_name}.png\" width=\"20\" height=\"20\" align=\"middle\"> 『$order_text{$order_name}』<br>\n";
		}
	}
	print <<"EOM";
</td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="変更">
</td></tr>
</table>
</form>
</td></tr></table>
EOM
	&footer2;
}

sub del_file{
	chdir("tmp");
	@files = glob("*_pfl");
	if($max_file <= $#files){
		while(@files){
			my $file = shift @files;
			my $date = (-M $file);
			unlink($file) if $date >= $del_day;
		}
	}
	chdir("/");
}

sub regist{
	if((-e "${player_dir}/".$id.".cgi") || (-e "${player_dir}/".$id."a.cgi") || (-e "${player_dir}/".$id."m.cgi")) {
		&pfl_read($id);
		$pass = $F{'cpass'};
		&pass_chk;
		$pass = $F{'pass'};
	} else {
		&error("IDの形式が正しくありません。<BR>半角英字の大文字３つ、数字５つにしてください。<BR>例：ABC012345") if($F{'id'} !~ /^[A-Z]{3}[0-9]{5}$/);
	}
	@lobby = ('旧モード', '新モード');
	&error("名前を入力してください。") unless $F{'name'};
	&error("名前は１０文字以内にしてください。") if length($F{'name'})>30;
	&error("メッセージは５０文字以内にしてください。") if length($F{'comment'})>=150;
	&error("パスワードを入力してください。") unless $F{'pass'};
	&error("パスワードは英数字で設定してください。") if $F{'pass'} =~ /\W/;
	&error("パスワードは８文字以内にしてください。") if length($F{'pass'})>8;
	&error("確認の為パスワードは２回入力してください。") unless $F{'pass2'};
	&error("伝言板番号の値が正しくありません。") unless ($F{'channel'} >= 1 && $F{'channel'} <= 9);
	&error("パスワードが正しく入力されていません。") if $F{'pass'} ne $F{'pass2'};
	&error("不正な勲章選択です。") if(!($P{"order_$F{'order'}"}) && ($F{'order'} ne ''));
	$P{'name'} = $F{'name'}; $P{'pass'} = &pass_enc($F{'pass'}); $P{'id'} = $F{'id'};$P{'comment'} = $F{'comment'};$P{'order'} = $F{'order'};$P{'age'} = $F{'age'};$P{'lobby'} = $F{'lobby'};$P{'channel'} = $F{'channel'};
	&pfl_write($P{'id'});
	&del_file if $max_file;
	&header;
	print <<"EOM";
</head>
<body>
<div align="center">
<h1>$title</h1>
<table border="1" width="600" cellspacing="0" cellpadding="10">
<tr><td class="table"> 
<p>以下の設定で登録しました。<br>IDおよびパスワードは、メモするなどして、忘れないようにしてください。</p>
<div align="center">
<table border="0" cellpadding="2">
<tr><th>ID</th><td>：$P{'id'}</td></tr>
<tr><th>名前</th><td>：$P{'name'}</td></tr>
<tr><th>パスワード</th><td>：$F{'pass'}</td></tr>
<tr><th>ロビー選択</th><td>：$lobby[$F{'lobby'}]</td></tr>
<tr><th>メッセージ</th><td>：$P{'comment'}</td></tr>
</table>
<p><a href="index.cgi">戻る</a></p>
</div>
</td></tr>
</table>
EOM
	&footer;
}

sub make_id{
	my @alphabet = ('A'..'Z');
	$m_id = "";
	for(0..2){ my $random = int(rand(26)); $m_id .= $alphabet[$random]; }
	my $m_id2 = int(rand(99999))+1;
	$m_id .= sprintf("%05d",$m_id2);
	if((-r "${player_dir}/".$m_id.".cgi") || (-r "${player_dir}/".$m_id."a.cgi")){ &make_id; } else { return $m_id; }
}

sub set_cookie{
	($sec,$min,$hour,$mday,$mon,$year) = localtime(time + 30*24*60*60);
	$gdate = sprintf("%02d\-%s\-%04d %02d:%02d:%02d", $mday, ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mon], $year + 1900, $hour, $min, $sec);
	$cook = "id:$F{'id'},pass:$F{'pass'},pc:$pc_chk";
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
	$pc_chk = $C{'pc'};
}

sub decode2 {
	$id = $F{'id'} if $F{'id'};
	$name = $F{'name'} if $F{'name'}; $name =~ s/\.//g; $name =~ s/\///g;
	$pass = $F{'pass'} if $F{'pass'}; $pass =~ s/\.//g; $pass =~ s/\///g;
}
