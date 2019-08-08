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
<table border="0" width="1260" cellspacing="0" cellpadding="10" id="index">
EOM
	} else {
		print <<"EOM";
<table border="0" width="1160" cellspacing="0" cellpadding="10" id="index">
EOM
	}
	print <<"EOM";
<tr><td style="border-style: none;vertical-align: top; width: 160px;" class="adarea">
EOM
my $randNum = int(rand 20);
if ($randNum == 1) {
        print <<"EOM";
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
<!-- 広告ユニット1 -->
<ins class="adsbygoogle"
     style="display:inline-block;width:160px;height:600px"
     data-ad-client="ca-pub-1974859203649104"
     data-ad-slot="1784652942"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
EOM
} else {
        print <<'EOM';
        <script>
		$(document).ready(function(){
		  $('.ad-scroll1').slick({
		  	draggable: true,
		    autoplay: true,
		    vertical: true,
		    slidesToShow: 6,
		    autoplaySpeed:10000,
		  });
		});
		</script>
		
		<div class="ad-scroll1" style="display:inline-block;width:160px;">
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810618157&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810618157"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810618157_8fdfe707ed0a4629ae914d693f4e1661.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810618157&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810895107&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810895107"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810895107.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810895107&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810896777&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810896777"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810896777.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810896777&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810139126&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810139126"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810139126_39c3e88e8e8f489c93f0a75363860a03.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810139126&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810114567&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810114567"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810114567_50c27e52edd84aaca5e7b9c34a9712b8.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810114567&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810139119&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810139119"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810139119_bac5e22af62b4b14a739ee90bc6ddfa3.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810139119&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810964384&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810964384"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810964384.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810964384&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810863342&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810863342"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810863342.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810863342&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810131526&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810131526"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810131526_6617fc8b9f9e4286a4abd85b3276995b.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810131526&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810872566&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810872566"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810872566.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810872566&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810114543&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810114543"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810114543_bb0361f226df4ae89734453bfefa4d1a.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810114543&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810618751&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810618751"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810618751_e4b5544580354aa986f3d525981a96be.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810618751&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810139102&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810139102"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810139102_ef272ae18fd84a7cb5072f708b7beb21.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810139102&type=2&subid=0" ></div>
EOM
}
	print <<"EOM";
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
</td><td style="border-style: none;vertical-align: top; width: 160px;" class="adarea">
EOM
if ($randNum == 1) {
        print <<"EOM";
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 広告ユニット1 -->
<ins class="adsbygoogle"
     style="display:inline-block;width:160px;height:600px"
     data-ad-client="ca-pub-1974859203649104"
     data-ad-slot="1784652942"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
EOM
} else {
        print <<'EOM';
        <script>
		$(document).ready(function(){
		  $('.ad-scroll1').slick({
		  	draggable: true,
		    autoplay: true,
		    vertical: true,
		    slidesToShow: 6,
		    autoplaySpeed:10000,
		  });
		});
		</script>
		
		<div class="ad-scroll1" style="display:inline-block;width:160px;">
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810894827&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810894827"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810894827.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810894827&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810894858&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810894858"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810894858.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810894858&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810618768&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810618768"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810618768_42f314ab51334e9d8859686c0a27d0e4.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810618768&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810132721&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810132721"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810132721_464887a358004465a9de096b6021ea3a.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810132721&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810131540&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810131540"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810131540_57c5b11d52e341808cc16e087e491c91.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810131540&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810114642&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810114642"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810114642_9d50d326bd49448d9ce10b5c1a2deba6.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810114642&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810131533&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810131533"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810131533_981db18cd1d94f53853753e456cfcdfc.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810131533&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810894865&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810894865"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810894865.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810894865&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810131496&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810131496"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810131496_a1a7f38f8ad949c98f75019bb53e37ba.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810131496&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810618133&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810618133"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810618133_4786713fb8d3446cbf9fab4a1613b6bf.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810618133&type=2&subid=0" ></div>
<div><a target='new' href="https://linksynergy.jrs5.com/link?id=MbBo1cILGsc&offerid=328106.4904810114666&type=2&murl=https%3A%2F%2Ftakaratomymall.jp%2Fshop%2Fg%2Fg4904810114666"><IMG border=0 src="https://dmwysfovhyfx3.cloudfront.net/img/goods/5/4904810114666_67427a902c42456fb193cd3209e86937.jpg" ></a><IMG border=0 width=1 height=1 src="https://ad.linksynergy.com/fs-bin/show?id=MbBo1cILGsc&bids=328106.4904810114666&type=2&subid=0" ></div>
EOM
}
	print <<"EOM";
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
