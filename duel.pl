$ver = "8.0 EX";

$ENV{'TZ'} = "JST-9";
$times = time;
%locks = ();
$copyright = qq|<p>(c)Wizards of the Coast / Shogakukan / Mitsui-MP<br><a href="http://tsuru.pekori.to">つる＠帝国大劇場別館</a><br><a href="http://www.stannet.ne.jp/fb/">コピーデッキデータ提供：カードキングダム</a><br>Ver. $ver</p>|;

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
	<script type="text/javascript" src="$js/jquery-1.11.2.min.js"></script>
	<title>$title</title>
EOM
}

sub footer{
	print <<"EOM";
	</div>
	<div align="right">
EOM
	print &getcpu();
	print <<"EOM";
	</div>
</body>
</html>
EOM
	exit;
}

sub footer2 {
	print <<"EOM";
	<p>(c)Wizards of the Coast / Shogakukan / Mitsui-MP<br><a href="http://tsuru.pekori.to">つる＠帝国大劇場別館</a><br>Ver. $ver</p>
	<p><a href="javascript:history.back();">戻る</a></p>
	</div>
	<div align="right">
EOM
	print &getcpu();
	print <<"EOM";
	</div>
</body>
</html>
EOM
	exit;
}

sub getcpu {
    my($uti, $sti, $cuti, $csti) = times();
    $uti += $cuti;
    $sti += $csti;
    my($cpu) = $uti + $sti;

    $cpu = sprintf('%5.2f', $cpu);
    $uti = sprintf('%5.2f', $uti);
    $sti = sprintf('%5.2f', $sti);
    return "( CPU: $cpu User: $uti System: $sti )";
}

sub error {
	foreach $key(keys(%locks)){ unlink $locks{$key} if ((-e $locks{$key}) && ($locks{$key})); }

	&header;
	print <<"EOM";
</head>
<body>
	<div align="center">
	<h1>$title</h1>
	<hr>
	<h2>ERROR!</h2>
	<p><strong style="color:red">$_[0]</strong></p>
	<p><a href="./index.cgi">トップに戻る</a></p>
	<hr>
	$copyright
	<p><a href="javascript:history.back();">戻る</a></p>
EOM
	&footer;
}

sub c_color{
	my $cno = $_[0];
	($bun,$bgc) = &bun_sub($cno);
	$syuzoku = &syu_sub($cno);
	if($bgc eq "rainbow"){
		$syuzoku =~ s/\//<br>/;
		my @bun = split(/\//,$bun);
		map {
			$c = $_ eq "光" ? "hikari": $_ eq "水" ? "mizu": $_ eq "闇" ? "yami": $_ eq "火" ? "hi" : $_ eq "自然" ? "sizen" : "zero";
			$_ = qq|<span class="$c">$_</span>|;
		} @bun;
		$bun = join("/",@bun);
	}
}

sub cardview {
	my $cou = $cou2 = 0;
	open KJT, "card2.txt" || &error("カード記述データを読み込めません。");
	my $lin = <KJT>;
	while(<KJT>){ chomp; $c_kijutu[$cou] = $_; $cou++; }
	close KJT;
	open KWD, "keyword.txt" || &error("キーワードデータを読み込めません。");
	while(<KWD>){
		chomp;
		($word, $tag) = split /\t/;
		$T{$word} = $tag;
	}
	close KWD;
	my $cno = $F{'j'};
	&c_color($cno);
	foreach my $word (keys %T) {
		my $link = qq|<a href="$keyword\#$T{$word}" class="jTip" id="$cou2" name="$word">$word</a>|;
		$c_kijutu[$cno] =~ s/$word/$link/gi;
		$cou2++;
	}
	&header;
	print qq|<script src="$js/jtip.js" type="text/javascript"></script>\n|;
	print qq|<link rel="stylesheet" href="$css/global.css" type="text/css">\n|;
	print qq|</head>\n|;
	print qq|<body>\n|;
	print qq|<div align="center">\n|;
	print qq|<table border="1" cellpadding="1" cellspacing="0" width="680" class="shield"><tr>\n|;
	print qq|<th width="24">Ｃ</th><th width="160">名前</th><th width="36">文明</th>\n|;
	print qq|<th width="48">パワー</th><th width="110">種族</th>| if 1 < $c_syu[$cno];
	print qq|<th>記述</th>\n</tr><tr class="$bgc">\n<td align="center">$c_mana[$cno]</td><td>$c_name[$cno]</td><td align="center">$bun</td>|;
	print qq|<td>$c_pow[$cno]</td><td>$syuzoku| if 1 < $c_syu[$cno];
	print qq|</td><td>$c_kijutu[$cno]</td>\n|;
	print qq|</tr></table>\n|;
        print <<"EOM";
<br>
EOM
my $randNum = int(rand 20);
if ($randNum == 1) {
        print <<"EOM";
ads
<!-- Research Artisan Pro Script Tag Start -->
<script type="text/javascript">
  var _Ra = {};
  _Ra.hId = '0';
  _Ra.uCd = '19070700007819331715';
  _Ra.exceptCrawler = true;
  (function() {var s=document.getElementsByTagName('script')[0],js=document.createElement('script');js.type='text/javascript';js.async='async';js.src='https://analyze.pro.research-artisan.com/track/script.php';s.parentNode.insertBefore(js,s);})();
</script>
<noscript><p><img src="https://analyze.pro.research-artisan.com/track/tracker.php?ucd=19070700007819331715&hid=0&guid=ON" alt="" width="1" height="1" /></p></noscript>
<!-- Research Artisan Pro Script Tag End   -->

<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 横長ビッグバナー -->
<ins class="adsbygoogle"
     style="display:inline-block;width:728px;height:90px"
     data-ad-client="ca-pub-1974859203649104"
     data-ad-slot="2205669784"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
EOM
}
	print qq|<p align="right"><a href="$keyword" target="_blank">キーワード一覧</a></p>\n|;
	&footer;
}

sub cardread{
	my $cou = 0;
	open(DATA,"card1.txt") || &error("カードデータを読み込めません。");
	my $lin = <DATA>;
	while(<DATA>){
		chomp;
		($c_name[$cou],$c_bun[$cou],$c_syu[$cou],$c_pow[$cou],$c_mana[$cou],$c_evo[$cou],$c_kok[$cou],$c_tri[$cou]) = split(/\t/);
		$cou++;
	}
	close(DATA);
}

sub cardread2{
	if(open(DATA,"room/duelist${room}_card.cgi")) {
		while(<DATA>){
			chomp;
			my($cou,$tc_name,$tc_bun,$tc_syu,$tc_pow,$tc_mana,$tc_evo,$tc_kok,$tc_tri) = split(/\t/);
			$c_name[$cou] = $tc_name;
			$c_bun[$cou] = $tc_bun;
			$c_syu[$cou] = $tc_syu;
			$c_pow[$cou] = $tc_pow;
			$c_mana[$cou] = $tc_mana;
			$c_evo[$cou] = $tc_evo;
			$c_kok[$cou] = $tc_kok;
			$c_tri[$cou] = $tc_tri;
		}
		close(DATA);
	} else {
		&cardread;
	}
}

sub syu_read {
	my $cou = 0;
	open(SYU,"syu.txt") || &error("種族データを読み込めません。");
	while(<SYU>){
		chomp;
		$syu[$cou] = $_;
		$cou++;
	}
	close(SYU);
}

sub syu_sub	{
	my $card = $_[0];
	my $syuzoku = "";
	if($c_syu[$card] =~ /,/){
		my @group = split(/,/, $c_syu[$card]);
		map { $_ = $syu[$_]; } @group;
		$syuzoku = join("\/",@group);
	} else { $syuzoku = $syu[$c_syu[$card]]; }
	return $syuzoku;
}

sub bun_sub	{
	my $card = $_[0];
	my ($bunmei, $style) = ();
	if($c_bun[$card] =~ /,/){
		$style = "rainbow";
		my @group = split(/,/, $c_bun[$card]);
		map { $_ = $_ == 0 ? "光": $_ == 1 ? "水": $_ == 2 ? "闇": $_ == 3 ? "火" : $_ == 4 ? "自然" :"ゼロ"; } @group;
		$bunmei = join("\/",@group);
	} else {
		$bunmei = $c_bun[$card] == 0 ? "光": $c_bun[$card] == 1 ? "水": $c_bun[$card] == 2 ? "闇": $c_bun[$card] == 3 ? "火" : $c_bun[$card] == 4 ? "自然" : "ゼロ" ;
		$style = $c_bun[$card] == 0 ? "hikari": $c_bun[$card] == 1 ? "mizu": $c_bun[$card] == 2 ? "yami": $c_bun[$card] == 3 ? "hi": $c_bun[$card] == 4 ? "sizen": "zero";
	}
	return ($bunmei, $style);
}

sub k_chk {
	my ($cre, $skill) = @_;
	foreach my $k(split /,/, $c_kok[$cre]){ return 1 if $k == $skill; }
	return 0;
}

sub pass_enc {
	crypt($_[0], $_[0]);
}

sub pass_chk{
	&error("IDまたはパスワードが間違っています。入力し直してください。") if ((crypt($pass, $pass) ne $P{'pass'}) && ($pass ne $admin));
}

sub filelock {
	if(-e "lock/$lockfile$_[0]"){
		$ftm = (stat("lock/$lockfile$_[0]"))[9];
		unlink "lock/$lockfile$_[0]" if $ftm < time-10;
	}
	for(1..5){
		if(-e "lock/$lockfile$_[0]"){
			sleep(1);
		} else {
			$locks{$_[0]} = "lock/$lockfile$_[0]";
			open(LOCK,">lock/$lockfile$_[0]");
			close(LOCK);
			return;
		}
	}
	&error("ファイルロック中です。$lockfile$_[0]"); 
}

sub fileunlock {
	$locks{$_[0]} = "";
	unlink "lock/$lockfile$_[0]" if -e "lock/$lockfile$_[0]";
}

sub pfl_read {
	my $id = $_[0];
	return if(!$id);
	&error("IDの形式が正しくありません。") if($id !~ /^[A-Z]{3}[0-9]{5}[am]{0,1}$/);
	&filelock("${id}_lock");
	undef(%P);
	chmod 0666, "${player_dir}/".$id.".cgi";
	open(PFL,"${player_dir}/".$id.".cgi") || &error("プレイヤーファイルが開けません");
	while(<PFL>){ chomp; ($key,$val) = split(/\t/); $P{$key} = $val; }
	close(PFL);
#	chmod 0000, "${player_dir}/".$id.".cgi";
	&fileunlock("${id}_lock");
}

sub pfl_write {
	my $id = $_[0];
	chmod 0666, "${player_dir}/".$id.".cgi";
	open(PFL,">${player_dir}/".$id.".cgi") || &error("書き込みエラーです。");
	foreach $key(keys(%P)){ print PFL "$key\t$P{$key}\n"; }
	close(PFL);
#	chmod 0000, "${player_dir}/".$id.".cgi";
}

sub prof {
	my $side = $F{'chara'};
	&error("対戦者のデータが見つかりません。") unless -e "${player_dir}/".$side.".cgi";
	chmod 0666, "${player_dir}/".$side.".cgi";
	open(PRF,"${player_dir}/".$side.".cgi") || &error("対戦者のファイルが開けません");
	while(<PRF>){ chomp; ($key,$val) = split(/\t/); $P2{$key} = $val; }
	close(PRF);
#	chmod 0000, "${player_dir}/".$side.".cgi";
	($win,$lose) = split(/-/,$P2{'shohai'});
	$win = 0 if !($win);
	$lose = 0 if !($lose);
	$use = $P2{'usedeck'};
	($deck,$dum) = split(/-/,$P2{"deck$use"});

	# ユーザー検索（node連携）
	my $url = $chatNodeHost . '/user/find?user_id=' . $P2{'id'};
	$request = POST( $url );

	# 送信
	my $ua = LWP::UserAgent->new(ssl_opts => { verify_hostname => 0 });
	my $res = $ua->request( $request );
	my $arrRes = decode_json($res->content);
	my $orica = 0;

	if ($res->is_success) {
		if (scalar @$arrRes > 0) {
			#ユーザーが存在した場合
			$orica = @$arrRes[0]->{orica};
		}
	}

	&header;
	print <<"EOM";
</head>
<body>
	<div align="center">
		<h1>$title</h1>
<table width="640" border="1" cellspacing="0" cellpadding="10" class="table"><tr><td align="center"> 
	<h2>対戦者データ</h2>
	<table border="0" cellpadding="5">
		<tr><th>ID</th><td align="left">：$P2{'id'}</td></tr>
		<tr><th>名　前</th><td align="left">：$P2{'name'}</td></tr>
		<tr><th>勝　敗</th><td align="left">：$win勝$lose敗</td></tr>
		<tr><th>ランク</th><td align="left">：$rankmark[$P2{'drank'}]</td></tr>
		<tr><th>ポイント</th><td align="left">：$P2{'dpoint'}</td></tr>
		<tr><th>オリカ作成権数</th><td align="left">：$orica</td></tr>
		<tr><th>コメント</th><td align="left">：$P2{'comment'}</td></tr>
		<tr><th>勝利数</th><td align="left">
EOM
print "光単： $P2{'light_win'}勝<br>\n" if($P2{'light_win'} > 0);
print "水単： $P2{'water_win'}勝<br>\n" if($P2{'water_win'} > 0);
print "闇単： $P2{'dark_win'}勝<br>\n" if($P2{'dark_win'} > 0);
print "火単： $P2{'fire_win'}勝<br>\n" if($P2{'fire_win'} > 0);
print "自然単： $P2{'nature_win'}勝<br>\n" if($P2{'nature_win'} > 0);
print "光/水： $P2{'lw_win'}勝<br>\n" if($P2{'lw_win'} > 0);
print "水/闇： $P2{'wd_win'}勝<br>\n" if($P2{'wd_win'} > 0);
print "闇/火： $P2{'df_win'}勝<br>\n" if($P2{'df_win'} > 0);
print "火/自然： $P2{'fn_win'}勝<br>\n" if($P2{'fn_win'} > 0);
print "自然/光： $P2{'nl_win'}勝<br>\n" if($P2{'nl_win'} > 0);
print "光/闇： $P2{'ld_win'}勝<br>\n" if($P2{'ld_win'} > 0);
print "水/火： $P2{'wf_win'}勝<br>\n" if($P2{'wf_win'} > 0);
print "闇/自然： $P2{'dn_win'}勝<br>\n" if($P2{'dn_win'} > 0);
print "火/光： $P2{'fl_win'}勝<br>\n" if($P2{'fl_win'} > 0);
print "自然/水： $P2{'nw_win'}勝<br>\n" if($P2{'nw_win'} > 0);
print "光/水/闇： $P2{'lwd_win'}勝<br>\n" if($P2{'lwd_win'} > 0);
print "水/火/光： $P2{'wfl_win'}勝<br>\n" if($P2{'wfl_win'} > 0);
print "自然/光/水： $P2{'nlw_win'}勝<br>\n" if($P2{'nlw_win'} > 0);
print "火/光/闇： $P2{'fld_win'}勝<br>\n" if($P2{'fld_win'} > 0);
print "光/闇/自然： $P2{'ldn_win'}勝<br>\n" if($P2{'ldn_win'} > 0);
print "火/自然/光： $P2{'fnl_win'}勝<br>\n" if($P2{'fnl_win'} > 0);
print "水/闇/火： $P2{'wdf_win'}勝<br>\n" if($P2{'wdf_win'} > 0);
print "水/闇/自然： $P2{'wdn_win'}勝<br>\n" if($P2{'wdn_win'} > 0);
print "自然/水/火： $P2{'nwf_win'}勝<br>\n" if($P2{'nwf_win'} > 0);
print "闇/火/自然： $P2{'dfn_win'}勝<br>\n" if($P2{'dfn_win'} > 0);
print "水/闇/火/自然： $P2{'nolight_win'}勝<br>\n" if($P2{'nolight_win'} > 0);
print "光/闇/火/自然： $P2{'nowater_win'}勝<br>\n" if($P2{'nowater_win'} > 0);
print "光/水/火/自然： $P2{'nodark_win'}勝<br>\n" if($P2{'nodark_win'} > 0);
print "光/水/闇/自然： $P2{'nofire_win'}勝<br>\n" if($P2{'nofire_win'} > 0);
print "光/水/闇/火： $P2{'nonature_win'}勝<br>\n" if($P2{'nonature_win'} > 0);
print "５色： $P2{'full_win'}勝<br>\n" if($P2{'full_win'} > 0);
	print <<"EOM";
</td></tr>
		<tr><th>勲章</th><td align="left">
EOM
	$order_flg = 0;
	foreach $order_name (@order_per) {
		if($P2{'order_' . $order_name}) {
			print "<img src=\"${symbol_dir}/symbol_${order_name}.png\" width=\"20\" height=\"20\" align=\"middle\"> 『$order_text{$order_name}』<br>\n";
			$order_flg = 1;
		}
	}
	unless($order_flg) {
		print "：獲得した勲章はありません。";
	}
	print <<"EOM";
</td></tr>
	</table>
	<br>
	<form name="white" action="list.cgi" method="post" style="display: inline;" onSubmit="if(!confirm('本当にホワイトリストに登録/除外しますか？')) return false;">
		<input type="hidden" name="id" value="$F{'id'}">
		<input type="hidden" name="pass" value="$F{'pass'}">
		<input type="hidden" name="mode" value="white">
		<input type="hidden" name="chara" value="$F{'chara'}">
		<input type="submit" value="ホワイトリストに登録/除外する">
	</form>
	<br><br>
	<form name="black" action="list.cgi" method="post" style="display: inline;" onSubmit="if(!confirm('本当にブラックリストに登録/除外しますか？')) return false;">
		<input type="hidden" name="id" value="$F{'id'}">
		<input type="hidden" name="pass" value="$F{'pass'}">
		<input type="hidden" name="mode" value="black">
		<input type="hidden" name="chara" value="$F{'chara'}">
		<input type="submit" value="ブラックリストに登録/除外する">
	</form>
</td></tr></table>
EOM
	&footer;
}

sub decode {
	if (length($ENV{'QUERY_STRING'}) > 0) {
		$INPUT = $ENV{'QUERY_STRING'};
	} elsif (length($ENV{'CONTENT_LENGTH'}) > 0) {
		read(STDIN,$INPUT,$ENV{'CONTENT_LENGTH'});
	} else {
		$INPUT .= $TMP[0] while $TMP[0] = <STDIN>;
	}
	$INPUT =~ s/\&+/\&/g;
	$INPUT =~ s/#.+//;
	@TMP = split('&',$INPUT);
	undef %F;
	foreach(@TMP){
		($key,$val) = split('=');
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
#		&jcode'convert(*val,'euc');
		$val =~ s/\015\012/\012/g;
		$val =~ s/\015/\012/g;
		$F{$key} = $val if $val ne "";
	}
}

sub log_read {	# 行区切りファイルからデータを読み込む
	return unless $_[0];
	open  IN, "$_[0]" or error("データファイルをオープンできません");
	my @lines = <IN>;
	close IN or error('データファイルをクローズできません');
	return @lines;
}

1;
