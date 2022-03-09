#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

use Net::SSLeay;
use LWP::UserAgent;
use HTTP::Request::Common;
use JSON;
use File::Copy;
use POSIX qw(strftime);

require "cust.cgi";
require "duel.pl";

&decode;
&get_cookie;
$pc_chk =
    int( rand(10) )
  . int( rand(10) )
  . int( rand(10) )
  . int( rand(10) )
  . int( rand(10) )
  . int( rand(10) )
  . int( rand(10) )
  . int( rand(10) )
  if ( $pc_chk eq '' );
$F{'id'}   = $c_id   if ( !$F{'id'} );
$F{'pass'} = $c_pass if ( !$F{'pass'} );
&set_cookie;

if ( $F{'mode'} ne "prof" ) {
	&decode2;
	&get_ini;
	( $win, $lose ) = split( /-/, $P{'shohai'} );
	$win          = 0 unless $win;
	$lose         = 0 unless $lose;
	$P{'channel'} = 1 unless ( $P{'channel'} );
}
$times = time;
( $sec, $min, $hour, $mday, $mon, $year ) = localtime(time);
$wdate = sprintf(
	"%04d/%02d/%02d %02d:%02d:%02d",
	$year + 1900,
	$mon + 1, $mday, $hour, $min, $sec
);
&prof     if $F{'mode'} eq "prof";
&write    if $F{'mode'} eq "write";
&detail   if $F{'mode'} eq "detail";
&tourrule if $F{'mode'} eq "tourrule";
&delete   if $F{'mode'} eq "delete";
&channel  if $F{'mode'} eq "channel";

if ( $P{'lobby'} == 1 ) {
	&room if $F{'mode'} eq "freeroom";
	&room if $F{'mode'} eq "tourroom";
	&chat
	  if $F{'mode'} eq "view"
		  || $F{'mode'} eq "write"
		  || $F{'mode'} eq "delete"
		  || $F{'mode'} eq "channel";
	&info if $F{'mode'} eq "info";
	&menu if $F{'mode'} eq "menu";
	&frame;
}
else {
	&view if $F{'mode'} eq "view";
	&html;
}

# 新モード

sub menu {
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		if(M == "duel") {
			entrance.duelpass.value = entrance["duelpass" + R].value;
			if(entrance.age.value == 0) {
				entrance.action = "duelold.cgi";
			} else {
				entrance.action = "duel.cgi";
			}
		} else if(M == "audience") {
			if(entrance.age.value == 0) {
				entrance.action = "duelold.cgi";
			} else {
				entrance.action = "duel.cgi";
			}
		} else if(M == "tourjoin") {
			entrance.action = "duelold.cgi";
		} else if(M == "tourcancel") {
			entrance.action = "duelold.cgi";
		} else if(M == "deck") {
			entrance.action = "deck.cgi";
		} else if(M == "group") {
			entrance.action = "group.cgi";
		} else if(M == "list") {
			entrance.action = "list.cgi";
		} else if(M == "nuisance") {
			entrance.action = "nuisance.cgi";
		} else if(M == "log") {
			entrance.action = "log.php";
		} else if(M == "index") {
			entrance.action = "index.cgi";
		} else {
			entrance.action = "taisen.cgi";
		}
		entrance.target = (M == "prof") ? "_blank" : (M == "tourrule") ? "_blank" : (M == "detail") ? "_blank" : (M == "freeroom") ? "main" : (M == "tourroom") ? "main" : (M == "info") ? "main" : "_top";
		entrance.submit();
	}
// --></script>
<script language="JavaScript">
<!--
vType   = ["visible","hidden"];
flag    = 0;		//　点滅フラグ
imgName = "myIMG";	//　点滅させる画像名
function iFlash()
{

	document.images[imgName].style.visibility = vType[flag ^= 1];
	setTimeout('iFlash()',800);
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
</head>
<body onLoad="setTimeout('iFlash()',800)">
<div align="center">
<form id="entrance" action="taisen.cgi" method="post" name="entrance" style="display: inline;">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
<div class="paging centered">
<ul>
<li><a href="javascript:sForm('freeroom', '', '');">フリールーム</a></li>
<li><a href="javascript:sForm('tourroom', '', '');">トーナメントルーム</a></li>
<li><a href="javascript:sForm('info', '', '');">お知らせ</a></li>
<li><a href="javascript:sForm('deck', '', '');">デッキ構築</a></li>
<li><a href="javascript:sForm('group', '', '');">グループ編集</a></li>
<li><a href="javascript:sForm('list', '', '');">リスト編集</a></li>
<li><a href="javascript:sForm('log', '', '');">過去ログ</a></li>
<li><a href="javascript:sForm('nuisance', '', '');">迷惑行為</a></li>
<li><a href="javascript:sForm('index', '', '');">トップへ戻る</a></li>
<li><a href="" onclick="window.open('donation/', '', 'width=700,height=500,scrollbers=yes');">寄付</a></li>
</ul>
</div>
</form>
</div>
</body>
</html>
EOM
	exit;
}

sub frame {
	&header;
	my ($roomtype) = ( $F{'mode'} eq 'tour' ) ? "tourroom" : "freeroom";
	print <<"EOM";
</head>
<frameset rows="64,*,240">
<frame src="taisen.cgi?mode=menu&id=$id&pass=$pass" name="menu" scrolling="no">
<frame src="taisen.cgi?mode=$roomtype&id=$id&pass=$pass" name="main" scrolling="yes">
<frame src="taisen.cgi?mode=view&id=$id&pass=$pass&line=30" name="chat" scrolling="yes">
</frameset>
<noframes>
<body>デュエルCGIはフレーム対応のブラウザでプレイしてください。</body>
</noframes>
</html>
EOM
	exit;
}

#-------------------------------------
# 対戦部屋一覧表示
#-------------------------------------
sub room {
	if ( mkdir( "./memlock", 0777 ) ) {
		open( MEM, "./member.dat" );
		@new_member = <MEM>;
		close(MEM);
		rmdir("./memlock");
	}
	else {
		my $locktime = ( stat "./memlock" )[9];
		rmdir("./memlock") if ( $locktime < time - 30 );
	}
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		if(M == "duel") {
			entrance.duelpass.value = entrance["duelpass" + R].value;
			if(entrance.age.value == 0) {
				entrance.action = "duelold.cgi";
			} else {
				entrance.action = "duel.cgi";
			}
		} else if(M == "audience") {
			if(entrance.age.value == 0) {
				entrance.action = "duelold.cgi";
			} else {
				entrance.action = "duel.cgi";
			}
		} else if(M == "tourjoin") {
			entrance.action = "duelold.cgi";
		} else if(M == "tourcancel") {
			entrance.action = "duelold.cgi";
		} else if(M == "deck") {
			entrance.action = "deck.cgi";
		} else if(M == "group") {
			entrance.action = "group.cgi";
		} else if(M == "list") {
			entrance.action = "list.cgi";
		} else if(M == "nuisance") {
			entrance.action = "nuisance.cgi";
		} else if(M == "log") {
			entrance.action = "log.php";
		} else if(M == "index") {
			entrance.action = "index.cgi";
		} else {
			entrance.action = "taisen.cgi";
		}
		entrance.target = (M == "prof") ? "_blank" : (M == "tourrule") ? "_blank" : (M == "detail") ? "_blank" : (M == "freeroom") ? "_self" : (M == "tourroom") ? "_self" : "_top";
		entrance.submit();
	}

	function textView(N) {
		if(document.getElementById(N).style.display == 'none') {
			document.getElementById(N).style.display = 'inline';
		} else {
			document.getElementById(N).style.display = 'none';
		}
	}

	function chooseView(N) {
		if(entrance.choose[N].value == 2) {
			entrance.duelid.disabled = true;
		} else {
			entrance.duelid.disabled = false;
		}
	}
	
	\$(function(\$) {
		
		var \$view = \$('#view'),
			\$name = \$('input[name="chatName"]'),
			\$data = \$('#chatData');
	
		/**
   		* データ取得
   		*/
  		function getData() {
    		\$.post('./chat/chat.php?mode=view', {}, function(data) {
      		\$view.html(data);
      		checkUpdate();
    		});
  		}
  
  		/**
   		* 更新チェック
   		*/
  		function checkUpdate() {
    		\$.post('./chat/chat.php?mode=check', {}, function(data) {
    		\$view.html(data);
    	  	//checkUpdate();
    		});
  		}
  		
  		\$("#chatAdd").click(function(){
  			\$.post('./chat/chat.php?mode=add', {data: \$data.val(),name: \$name.val()}, function(data) {
      		\$data.val('');
    		});
  		});
  
  		getData();
  		
  		
  		\$('#chatInputArea').hide();
  		\$("#dispChangeChat").click(function(){
  			if(\$('#chatInputArea').is(':hidden')) {
    			\$('#chatInputArea').show("slow");
  			}else{
  				\$('#chatInputArea').hide("slow");
  			}
    	});

		// 画面再描画
		refresh = () => {
			\$.ajax({
				type: "GET",
				url: location.href, // 取得先のURL
				dataType: 'html',
				success: function (data) {
					var html = jQuery.parseHTML(data);
					var roomList = \$(html).find('#room_list').html();
					var userList = \$(html).find('#user_list').html();
					\$('#room_list').html(roomList);
					\$('#user_list').html(userList);
				}
			});
		}

		// TODO 対戦部屋に入った瞬間にエミットで変更するようにしたい
		//setInterval(refresh, 10000);
  	});
    
    
// --></script>
</head>
<body>
<div align="center">
EOM
	if ( int( rand(12) ) == 0 ) {
		print
"<img src=\"./images/yukkuri_left_doremi.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/yukkuri_center.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/yukkuri_right_onpu.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	elsif ( int( rand(24) ) == 0 ) {
		print
"<img src=\"./images/cgi_logo_omote_v.gif\" width=\"480\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
	}
	elsif ( int( rand(12) ) == 0 ) {
		print
"<img src=\"./images/cgi_logo_omote_left.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_center_doremi.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_omote_right_n.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	elsif ( int( rand(36) ) == 0 ) {
		print
"<img src=\"./images/cgi_logo_tatae_onpu.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_tatae_word.gif\" width=\"416\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	elsif ( $F{'mode'} eq 'tour' ) {
		print
"<img src=\"./images/cgi_logo_ura_left.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_center.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_ura_right.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	else {
		print
"<img src=\"./images/cgi_logo_omote_left.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_center.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		if ( int( rand(8) ) == 0 ) {
			print
"<img src=\"./images/cgi_logo_omote_right_light.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		elsif ( int( rand(8) ) == 0 ) {
			print
"<img src=\"./images/cgi_logo_omote_right_d.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		elsif ( int( rand(4) ) == 0 ) {
			print
"<img src=\"./images/cgi_logo_omote_right_n.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		else {
			print
"<img src=\"./images/cgi_logo_omote_right.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		print "<br><br>\n";
	}
	print <<"EOM";
<form id="entrance" action="taisen.cgi" method="post" name="entrance" style="display: inline;">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
	<input type="hidden" name="duelpass" value="">
EOM
	&roomlist;
	print <<"EOM";
</form>
</div>
</body>
</html>
EOM
	exit;
}

sub chat {
	if ( mkdir( "./memlock", 0777 ) ) {
		open( MEM, "./member.dat" );
		@member = <MEM>;
		close(MEM);

		@new_member = ();
		for ( my ($i) = 0 ; $i <= $#member ; $i++ ) {
			my ( $mem_id, $mem_name, $mem_rank, $mem_comment, $mem_time,
				$mem_ip, $mem_channel )
			  = split( /<>/, $member[$i] );
			if ( ( $mem_id ne $F{'id'} ) && ( $mem_time > time - 300 ) ) {
				push( @new_member, $member[$i] );
			}
		}
		push( @new_member,
			    "$F{'id'}<>$P{'name'}<>$P{'drank'}<>$P{'comment'}<>" 
			  . time
			  . "<>$ENV{'REMOTE_ADDR'}<>$P{'channel'}<>\n" );
		open( MEM, "> ./member.dat" );
		print MEM @new_member;
		close(MEM);
		rmdir("./memlock");
	}
	else {
		my $locktime = ( stat "./memlock" )[9];
		rmdir("./memlock") if ( $locktime < time - 30 );
	}
	&read_log;
	shift(@lines);
	&header;
	print <<"EOM";
<script language="javascript">
<!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		entrance.target = (M == "prof") ? "_blank" : "_self";
		entrance.submit();
	}

	function autoDelete(N) {
		entrance.num.value = N;
		entrance.pass2.value = '${pass}';
		sForm('delete', '', '');
	}

	vType   = ["visible","hidden"];
	flag    = 0;		//　点滅フラグ
	imgName = "myIMG";	//　点滅させる画像名
	function iFlash()
	{
		document.images[imgName].style.visibility = vType[flag ^= 1];
		setTimeout('iFlash()',800);
	}

	/**** アクティブ判定処理 ****/

	var isActive = true; // 全体のアクティブフラグ
	var iframeIsActive = false; // iframeのアクティブフラグ
	var spIsActive = true; // スマホ対応用のアクティブフラグ

	// iframeからメッセージ受け取り
	\$(window).on('message', function(e){
		var data = e.originalEvent.data;
		if (data.isActive !== undefined) {
			iframeIsActive = data.isActive;
		}
	});

	\$('#chatFrame').focus();

	// 各フレームがアクティブかどうか
	parent.menu.window.onfocus = function () {
		isActive = true;
	};

	parent.main.window.onfocus = function () {
		isActive = true;
	};

	window.onfocus = function () {
		isActive = true;
	};

	// 各フレームが非アクティブかどうか
	parent.menu.window.onblur = function () {
		isActive = false;
	};

	parent.main.window.onblur = function () {
		isActive = false;
	};

	window.onblur = function () {
	 	isActive = false;
	};

	/**** スマホでホームボタン押下、ページ切り替えなどでもユーザーが消えるようにする対応 ***/

	var hidden, visibilityChange;

	if (typeof document.hidden !== "undefined") {
		hidden = "hidden";
		visibilityChange = "visibilitychange";
	} else if (typeof document.mozHidden !== "undefined") {
		hidden = "mozHidden";
		visibilityChange = "mozvisibilitychange";
	} else if (typeof document.msHidden !== "undefined") {
		hidden = "msHidden";
		visibilityChange = "msvisibilitychange";
	} else if (typeof document.webkitHidden !== "undefined") {
		hidden = "webkitHidden";
		visibilityChange = "webkitvisibilitychange";
	}
	document.addEventListener(visibilityChange, function(){
		// ページ非表示と表示時に呼ばれるため、表示から非表示になった時だけ呼ばれるように
		// document.hidden条件を追加
		if(document.hidden){
			spIsActive = false;
		} else {
			spIsActive = true;
		}
	}, false);

	window.addEventListener("pagehide", function(){
		spIsActive = false;
	}, false);

	window.addEventListener("pageshow", function(){
		spIsActive = true;
	}, false);

	// 一定間隔で、ユーザーが存在することをnodeに通知
	var interval = setInterval(function () {
		// 各フレーム、iframeいずれかがアクティブかつスマホ用フラグもアクティブの場合のみアクティブチェック
		if ((iframeIsActive || isActive) && spIsActive) {
			\$.ajax({
				url: '$hostName/cgi3/script/send_api.php',
				type:'POST',
				dataType: 'json',
				data : {url: '$chatNodeHost/userList', data: {user_id: "$id", user_name: "$P{'name'}", listFlg: 0}},
				timeout:7000,
			}).done(function(data) {
				console.log("ok");
			}).fail(function(XMLHttpRequest, textStatus, errorThrown) {
				console.log("参加ユーザーチェクエラー");
			})
		}
	 }, 5000);

// --></script>
</head>
<body onLoad="setTimeout('iFlash()',800); document.chatForm.submit();">
<div align="center">
<form id="entrance" action="taisen.cgi" method="post" name="entrance" style="display: inline;">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="subm" value="view">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
EOM
	&logview;
	print <<"EOM";
</form>

</div>
</body>
</html>
EOM
	exit;
}

sub info {
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	nowView = "mannerrule";
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		entrance.target = "_self";
		entrance.submit();
	}

	function textView(N) {
		if(document.getElementById(N).style.display == 'none') {
			document.getElementById(N).style.display = 'inline';
		} else {
			document.getElementById(N).style.display = 'none';
		}
	}
// --></script>
</head>
<body>
<div align="center">
<h1>$title</h1>
<table width="800" border="1" cellspacing="0" cellpadding="10" class="table"><tr><td>
EOM
	&explain;
	print <<"EOM";
</td></tr>
</table>
</div>
EOM
	&footer2;
}

# 旧モード

sub html {
	if ( mkdir( "./memlock", 0777 ) ) {
		open( MEM, "./member.dat" );
		@member = <MEM>;
		close(MEM);

		@new_member = ();
		for ( my ($i) = 0 ; $i <= $#member ; $i++ ) {
			my ( $mem_id, $mem_name, $mem_rank, $mem_comment, $mem_time,
				$mem_ip, $mem_channel )
			  = split( /<>/, $member[$i] );
			if ( ( $mem_id ne $F{'id'} ) && ( $mem_time > time - 300 ) ) {
				push( @new_member, $member[$i] );
			}
		}
		push( @new_member,
			    "$F{'id'}<>$P{'name'}<>$P{'drank'}<>$P{'comment'}<>" 
			  . time
			  . "<>$ENV{'REMOTE_ADDR'}<>$P{'channel'}<>\n" );
		open( MEM, "> ./member.dat" );
		print MEM @new_member;
		close(MEM);
		rmdir("./memlock");
	}
	else {
		my $locktime = ( stat "./memlock" )[9];
		rmdir("./memlock") if ( $locktime < time - 30 );
	}
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	nowView = "mannerrule";
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		if(M == "duel") {
			entrance.duelpass.value = entrance["duelpass" + R].value;
			if(entrance.age.value == 0) {
				entrance.action = "duelold.cgi";
			} else {
				entrance.action = "duel.cgi";
			}
		} else if(M == "audience") {
			if(entrance.age.value == 0) {
				entrance.action = "duelold.cgi";
			} else {
				entrance.action = "duel.cgi";
			}
		} else if(M == "tourjoin") {
			entrance.action = "duelold.cgi";
		} else if(M == "tourcancel") {
			entrance.action = "duelold.cgi";
		} else if(M == "deck") {
			entrance.action = "deck.cgi";
		} else if(M == "group") {
			entrance.action = "group.cgi";
		} else if(M == "list") {
			entrance.action = "list.cgi";
		} else if(M == "nuisance") {
			entrance.action = "nuisance.cgi";
		} else if(M == "log") {
			entrance.action = "log.php";
		} else if(M == "index") {
			entrance.action = "index.cgi";
		} else {
			entrance.action = "taisen.cgi";
		}
		entrance.target = (M == "prof") ? "_blank" : (M == "tourrule") ? "_blank" : (M == "detail") ? "_blank" : "_self";
		entrance.submit();
	}

	function textView(N) {
		if(document.getElementById(N).style.display == 'none') {
			document.getElementById(N).style.display = 'inline';
		} else {
			document.getElementById(N).style.display = 'none';
		}
	}
	
	function autoDelete(N) {
		entrance.num.value = N;
		entrance.pass2.value = '${pass}';
		sForm('delete', '', '');
	}
	
	function chooseView(N) {
		if(entrance.choose[N].value == 2) {
			entrance.duelid.disabled = true;
		} else {
			entrance.duelid.disabled = false;
		}
	}
// --></script>
</head>
<body>
<div align="center">
<!--<h1>$title</h1>-->
EOM
	if ( int( rand(12) ) == 0 ) {
		print
"<img src=\"./images/yukkuri_left_doremi.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/yukkuri_center.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/yukkuri_right_onpu.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	elsif ( int( rand(24) ) == 0 ) {
		print
"<img src=\"./images/cgi_logo_omote_v.gif\" width=\"480\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
	}
	elsif ( int( rand(12) ) == 0 ) {
		print
"<img src=\"./images/cgi_logo_omote_left.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_center_doremi.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_omote_right_n.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	elsif ( int( rand(36) ) == 0 ) {
		print
"<img src=\"./images/cgi_logo_tatae_onpu.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_tatae_word.gif\" width=\"416\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	elsif ( $F{'mode'} eq 'tour' ) {
		print
"<img src=\"./images/cgi_logo_ura_left.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_center.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_ura_right.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print "<br><br>\n";
	}
	else {
		print
"<img src=\"./images/cgi_logo_omote_left.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		print
"<img src=\"./images/cgi_logo_center.gif\" width=\"352\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		if ( int( rand(8) ) == 0 ) {
			print
"<img src=\"./images/cgi_logo_omote_right_light.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		elsif ( int( rand(8) ) == 0 ) {
			print
"<img src=\"./images/cgi_logo_omote_right_d.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		elsif ( int( rand(4) ) == 0 ) {
			print
"<img src=\"./images/cgi_logo_omote_right_n.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		else {
			print
"<img src=\"./images/cgi_logo_omote_right.gif\" width=\"64\" height=\"96\" alt=\"DMCGI ex\" title=\"$title\">";
		}
		print "<br><br>\n";
	}
	print <<"EOM";
<table width="640" border="1" cellspacing="0" cellpadding="10" class="table"><tr><td>
<div style="width: 100%; height: 200px; overflow: scroll;">
EOM
	&explain;
	print <<"EOM";
</div>
<br>
<hr>
<form id="entrance" action="taisen.cgi" method="post" name="entrance" style="display: inline;">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
	<input type="hidden" name="duelpass" value="">
EOM
	&roomlist;
	if ($bbs) {
		&read_log;
		shift(@lines);
		print <<"EOM";
<hr width="640">
現在地: <select name="channel" onChange="sForm('channel', this.value)">
EOM
		for ( my ($i) = 1 ; $i <= 9 ; $i++ ) {
			my ($selected) = ( $i == $P{'channel'} ) ? " selected" : "";
			print "<option value=\"$i\"$selected>チャンネル $i</option>";
		}
		print <<"EOM";
</select>
<hr width="640">

<div class="menuArea2">
<div class="paging centered">
<ul>
<li><a href="javascript:sForm('freeroom', '', '');">フリールーム</a></li>
<li><a href="javascript:sForm('tourroom', '', '');">トーナメントルーム</a></li>
<li><a href="javascript:sForm('info', '', '');">お知らせ</a></li>
<li><a href="javascript:sForm('deck', '', '');">デッキ構築</a></li>
<li><a href="javascript:sForm('group', '', '');">グループ編集</a></li>
<li><a href="javascript:sForm('list', '', '');">リスト編集</a></li>
<li><a href="javascript:sForm('log', '', '');">過去ログ</a></li>
<li><a href="javascript:sForm('nuisance', '', '');">迷惑行為</a></li>
<li><a href="javascript:sForm('index', '', '');">トップへ戻る</a></li>
</ul>
</div>
</div>
<hr width="640">
<input type="hidden" name="subm" value="">
EOM
		&logview;
	}
	print <<"EOM";
</form>
EOM
	&footer2;
}

sub view {
	&read_log;
	shift(@lines);
	&header;
	print <<"EOM";
<script language="javascript">
<!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		if(M == "deck") {
			entrance.action = "deck.cgi";
		} else if(M == "group") {
			entrance.action = "group.cgi";
		} else if(M == "list") {
			entrance.action = "list.cgi";
		} else if(M == "nuisance") {
			entrance.action = "nuisance.cgi";
		} else if(M == "log") {
			entrance.action = "log.php";
		} else if(M == "index") {
			entrance.action = "index.cgi";
		} else {
			entrance.action = "taisen.cgi";
		}
		entrance.target = (M == "prof") ? "_blank" : "_self";
		entrance.submit();
	}
// --></script>
</head>
<body>

<div align="center">
<h1>$title</h1>
現在地: <select name="channel" onChange="sForm('channel', this.value)">
EOM
	for ( my ($i) = 1 ; $i <= 9 ; $i++ ) {
		my ($selected) = ( $i == $P{'channel'} ) ? " selected" : "";
		print "<option value=\"$i\"$selected>チャンネル $i</option>";
	}
	print <<"EOM";
</select>
<hr width="640">
<div class="paging centered">
<ul>
<li><a href="javascript:sForm('freeroom', '', '');">フリールーム</a></li>
<li><a href="javascript:sForm('tourroom', '', '');">トーナメントルーム</a></li>
<li><a href="javascript:sForm('info', '', '');">お知らせ</a></li>
<li><a href="javascript:sForm('deck', '', '');">デッキ構築</a></li>
<li><a href="javascript:sForm('group', '', '');">グループ編集</a></li>
<li><a href="javascript:sForm('list', '', '');">リスト編集</a></li>
<li><a href="javascript:sForm('log', '', '');">過去ログ</a></li>
<li><a href="javascript:sForm('nuisance', '', '');">迷惑行為</a></li>
<li><a href="javascript:sForm('index', '', '');">トップへ戻る</a></li>
</ul>
</div>

<hr width="640">
<form id="entrance" action="taisen.cgi" method="post" name="entrance" style="display: inline;">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="subm" value="view">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
EOM
	&logview;
	&footer2;
}

# 共通部分

sub roomlist {
	my $nextrank = "";
	$nextrank = " (next: " . ( $uppoint[ $P{'drank'} ] - $P{'dpoint'} ) . ")"
	  if ( $P{'drank'} < 25 );
	print <<"EOM";
<table border="0" cellpadding="3" cellspacing="0">
<tr><td class="adarea" style="vertical-align: top;">
EOM

my $randNum = int(rand 2);
# アドセンスがクリック済みの場合はアドセンスは表示しない
if ($adsenseActive == 0) {
	$randNum = 2;
}
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
	open(ADSFILE, "< data/ads.txt");
	
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
EOM
	$count = 1;
	while (my $ad = <ADSFILE>){
	  if ($count % 2 == 0) {
		chomp($ad);
		print "<div class='adblock'>$ad</div>";
	  }
	  $count++;
	}
	
	print "</div>";
}
        print <<"EOM";
</td><td width="640" bgcolor="#FFFFFF">
<div align="center" style="width: 600px; height: 200px; overflow: scroll;">
<table border="0" cellpadding="5">
<tr><th>ID</th><td>：$id</td></tr>
<tr><th>名前</th><td>：$P{'name'}</td></tr>
<tr><th>ランク</th><td>：$rankmark[$P{'drank'}]</td></tr>
<tr><th>ポイント</th><td>：$P{'dpoint'}$nextrank</td></tr>
<tr><th>成績</th><td>：$win勝　$lose敗</td></tr>
EOM
	if (
		( $F{'mode'} ne 'tourroom' )
		|| (   ( ( $T{'remain'} > 0 ) && ( $T{'accept'} == 0 ) )
			|| ( $T{'accept'} == 1 )
			|| ( !$T{'scale'} ) )
	  )
	{
		print <<"EOM";
<tr><th>使用デッキ</th><td>：
<select name="usedeck">
EOM
		map { print "<option value=\"$_\"$selstrd[$_]>$dnam[$_]</option>\n"; }
		  ( 1 .. $maxdeck );
		print <<"EOM";
</select></td></tr>
EOM
	}
	else {
		print <<"EOM";
<input type="hidden" name="usedeck" value="$P{'usedeck'}">
EOM
	}
	print <<"EOM";
<tr><th>モード</th><td>：
<select name="age">
<option value="0"$age_sel1>旧モード</option>
<option value="1"$age_sel2>新モード</option>
</select>
</td></tr>
EOM
	my $age_sel1 = !$P{'age'} ? ' selected' : '';
	my $age_sel2 = $P{'age'}  ? ' selected' : '';
	if ( $F{'mode'} ne 'tourroom' ) {
		print <<"EOM";
<tr><th>ルール</th><td>：


<select name="dendou">
<option value="0">殿堂なし</option>
<option value="1" selected>殿堂あり</option>
<option value="2">ＡＧ環境</option>
<option value="3">ＳＧＬ環境</option>
<option value="4">ゼロルール</option>
<option value="10">おやぢ電動</option>
<option value="11">CGIex公式</option>
<option value="12">殿堂禁止</option>
</select>
</td></tr>
<tr><th>使用禁止グループ</th><td>：
<select name="usegroup">
EOM
		print "<option value=\"0\">禁止しない</option>\n";
		map { print "<option value=\"$_\"$selstrg[$_]>$gnam[$_]</option>\n"; }
		  ( 1 .. $maxgroup );
		print <<"EOM";
</select></td></tr>
</td></tr>
<tr><th><select name="choose" onChange="chooseView(this.selectedIndex);">
<option value="0" selected>対戦者ID指定</option>
<option value="1">部屋パスワード</option>
<option value="2">友達のみ</option>
<option value="3">減算ポイント</option>
</select></th><td>：
<input type="text" name="duelid" size="10"></td></tr>
<tr><th>一言メッセージ</th><td>：
<input type="text" name="message" size="32"></td></tr>
EOM
	}
	else {
		print <<"EOM";
<input type="hidden" name="dendou" value="0">
<input type="hidden" name="usegroup" value="0">
<input type="hidden" name="choose" value="0">
<input type="hidden" name="duelid" value="">
<input type="hidden" name="message" value="">
EOM
	}
	print <<"EOM";
</table>
</div>
<hr>
<!--スクロール追加
<div align="center" style="width: 600px; height: 150px; overflow: scroll;">
<table border="0" cellpadding="5">
新規スクロール
</table>
</div>
<hr>
ここまで-->
<div align="center">
EOM
	if ($mente) {
		print <<"EOM";
<B>現在メンテナンス中です。<BR>
メンテナンスが終わるまで、入室は出来ません。</B>
<hr>
EOM
	}
	print <<"EOM";
<SCRIPT type="text/javascript"><!--
 myWeek=new Array("日","月","火","水","木","金","土");
function myFunc(){
  myDate=new Date();
  myMsg = myDate.getFullYear() + "年";
  myMsg += ( myDate.getMonth() + 1 ) + "月";
  myMsg += myDate.getDate() + "日";
  myMsg += "(" + myWeek[myDate.getDay()] +  "曜日)";
  myMsg += myDate.getHours() + "時";
  myMsg += myDate.getMinutes() + "分";
  myMsg += myDate.getSeconds() + "秒";
  document.getElementById("myIDdate").innerHTML = myMsg;
}

  setInterval( "myFunc()", 1000 );
// --></SCRIPT>

<!--<p>現在時刻：$wdate　<strong><a href="$help#taisen" target="_blank">対戦での注意</a></strong></p>-->
<p>現在時刻：<span id="myIDdate">表示中</span>　<strong><a href="$help#taisen" target="_blank">対戦での注意</a></strong></p>
EOM
	if ( $F{'mode'} eq 'tourroom' ) {
		undef(%T);
		&filelock("tr");
		open( TRT, "tour/part.dat" )
		  || &error("大会データが開けません");
		while (<TRT>) { chomp; ( $key, $val ) = split(/\t/); $T{$key} = $val; }
		close(TRT);
		&fileunlock("tr");
		print "<p>$T{'title'}</p>\n" if ( $T{'scale'} );
		print <<"EOM";
<table border="0" cellspacing="0" cellpadding="0"><tr align="center" valign="middle">
<tr>
<td>
EOM

		if ( !$T{'scale'} ) {
			print <<"EOM";
現在、対戦CGI ex 公式トーナメントは開催されておりません。
EOM
		}
		elsif ( ( $T{'remain'} > 0 ) && ( $T{'accept'} == 0 ) ) {
			if ( $T{'tpass'} ne '' ) {
				print <<"EOM";
参加パスワード: <input type="text" size="16" name="tpass" value=""><BR>
<BR>
EOM
			}
			print <<"EOM";
<input type="button" value="大会に参加 (後 $T{'remain'}人)" onClick="if(confirm('大会に参加します')) sForm('tourjoin', '', '');"><BR>
<BR>
<input type="button" value="大会の登録を取り消し" onClick="if(confirm('登録を取り消します')) sForm('tourcancel', '', '');"><BR>
<BR>
<A href="javascript:sForm('tourrule', '', '');">この大会の詳細情報</A>
EOM
		}
		elsif ( $T{'accept'} == 1 ) {
			if ( $T{'tpass'} ne '' ) {
				print <<"EOM";
参加パスワード: <input type="text" size="16" name="tpass" value=""><BR>
<BR>
EOM
			}
			print <<"EOM";
<input type="button" value="大会に参加 (現在 $T{'number'}人)" onClick="if(confirm('大会に参加します')) sForm('tourjoin', '', '');"><BR>
<BR>
<input type="button" value="大会の登録を取り消し" onClick="if(confirm('登録を取り消します')) sForm('tourcancel', '', '');"><BR>
<BR>
<A href="javascript:sForm('tourrule', '', '');">この大会の詳細情報</A>
EOM
		}
		else {
			for ( my ($i) = 0 ; $i < 2**$T{'scale'} ; $i++ ) {
				print "["
				  . $T{ "p" . ( $i + 1 ) . "id" } . "/"
				  . $T{ "p" . ( $i + 1 ) . "name" }
				  . "]<BR>\n";
				print "<BR>\n" if ( $i < 2**$T{'scale'} - 1 );
			}
			print <<"EOM";
<BR>
</td>
<td>
EOM
			for ( my ($i) = 0 ; $i < $T{'scale'} ; $i++ ) {
				for ( my ($j) = 0 ; $j < 2**( $T{'scale'} - $i - 1 ) ; $j++ ) {
					my $rn = &room_num( $i, $T{'scale'} ) + $j + 1;
					my $ln = ( $rn - 1 ) * 2;
					for ( my ($k) = 0 ; $k < 2**$i - 1 ; $k++ ) {
						print "<BR>\n";
					}
					if ( &line_chk( $ln + 1, $T{'scale'} ) ) {
						print "━┓<BR>\n";
					}
					else {
						print "<FONT color=\"#C0C0C0\">─┐</FONT><BR>\n";
					}
					for ( my ($k) = 0 ; $k < 2**$i - 1 ; $k++ ) {
						if ( &line_chk( $ln + 1, $T{'scale'} ) ) {
							print "&nbsp;&nbsp;&nbsp;┃<BR>\n";
						}
						else {
							print
"&nbsp;&nbsp;&nbsp;<FONT color=\"#C0C0C0\">│</FONT><BR>\n";
						}
					}
					print
"&nbsp;&nbsp;&nbsp;<A href=\"javascript:sForm('audience','t${rn}','');\">";
					if (   ( &line_chk( $ln + 1, $T{'scale'} ) )
						|| ( &line_chk( $ln + 2, $T{'scale'} ) ) )
					{
						print "■";
					}
					else {
						print "□";
					}
					print "</A><BR>\n";
					for ( my ($k) = 0 ; $k < 2**$i - 1 ; $k++ ) {
						if ( &line_chk( $ln + 2, $T{'scale'} ) ) {
							print "&nbsp;&nbsp;&nbsp;┃<BR>\n";
						}
						else {
							print
"&nbsp;&nbsp;&nbsp;<FONT color=\"#C0C0C0\">│</FONT><BR>\n";
						}
					}
					if ( &line_chk( $ln + 2, $T{'scale'} ) ) {
						print "━┛<BR>\n";
					}
					else {
						print "<FONT color=\"#C0C0C0\">─┘</FONT><BR>\n";
					}
					for ( my ($k) = 0 ; $k < 2**$i - 1 ; $k++ ) {
						print "<BR>\n";
					}
					print "<BR>\n" if ( $j < 2**( $T{'scale'} - $i - 1 ) - 1 );
				}
				print "<BR>\n";
				print "</td><td>\n";
			}
			for ( my ($i) = 1 ; $i < 2**$T{'scale'} ; $i++ ) {
				print "<BR>\n";
			}
			my $rn = &room_num( $T{'scale'}, $T{'scale'} ) + 1;
			my $ln = ( $rn - 1 ) * 2;
			if ( &line_chk( $ln + 1, $T{'scale'} ) ) {
				print "━";
			}
			else {
				print "<FONT color=\"#C0C0C0\">─</FONT>";
			}
			print "<A href=\"javascript:sForm('audience','t${rn}');\">";
			if (   ( &line_chk( $ln + 1, $T{'scale'} ) )
				|| ( &line_chk( $ln + 2, $T{'scale'} ) ) )
			{
				print "■";
			}
			else {
				print "□";
			}
			print "</A>";
			if ( &line_chk( $ln + 2, $T{'scale'} ) ) {
				print "━";
			}
			else {
				print "<FONT color=\"#C0C0C0\">─</FONT>";
			}
			print "<BR>\n";
			for ( my ($i) = 1 ; $i < 2**$T{'scale'} + 1 ; $i++ ) {
				if ( $i == 2 ) {
					print "<A href=\"javascript:sForm('audience','t"
					  . ( 2**$T{'scale'} * 2 )
					  . "', '');\">";
					if ( $T{'third'} ) {
						print "■";
					}
					else {
						print "□";
					}
					print "</A>\n";
				}
				print "<BR>\n";
			}
			print <<"EOM";
</td>
<td>
EOM
			for ( my ($i) = 0 ; $i < $T{'scale'} ; $i++ ) {
				for ( my ($j) = 0 ; $j < 2**$i ; $j++ ) {
					my $rn =
					  &room_num( $T{'scale'} - $i - 1, $T{'scale'} ) +
					  &room_rev( $T{'scale'} - $i, $T{'scale'} ) +
					  $j + 2;
					my $ln = ( $rn - 1 ) * 2;
					for (
						my ($k) = 0 ;
						$k < 2**( $T{'scale'} - $i - 1 ) - 1 ;
						$k++
					  )
					{
						print "<BR>\n";
					}
					if ( &line_chk( $ln + 1, $T{'scale'} ) ) {
						print "┏━<BR>\n";
					}
					else {
						print "<FONT color=\"#C0C0C0\">┌─</FONT><BR>\n";
					}
					for (
						my ($k) = 0 ;
						$k < 2**( $T{'scale'} - $i - 1 ) - 1 ;
						$k++
					  )
					{
						if ( &line_chk( $ln + 1, $T{'scale'} ) ) {
							print "┃&nbsp;&nbsp;&nbsp;<BR>\n";
						}
						else {
							print
"<FONT color=\"#C0C0C0\">│</FONT>&nbsp;&nbsp;&nbsp;<BR>\n";
						}
					}
					print
					  "<A href=\"javascript:sForm('audience','t${rn}','');\">";
					if (   ( &line_chk( $ln + 1, $T{'scale'} ) )
						|| ( &line_chk( $ln + 2, $T{'scale'} ) ) )
					{
						print "■";
					}
					else {
						print "□";
					}
					print "</A>&nbsp;&nbsp;&nbsp;<BR>\n";
					for (
						my ($k) = 0 ;
						$k < 2**( $T{'scale'} - $i - 1 ) - 1 ;
						$k++
					  )
					{
						if ( &line_chk( $ln + 2, $T{'scale'} ) ) {
							print "┃&nbsp;&nbsp;&nbsp;<BR>\n";
						}
						else {
							print
"<FONT color=\"#C0C0C0\">│</FONT>&nbsp;&nbsp;&nbsp;<BR>\n";
						}
					}
					if ( &line_chk( $ln + 2, $T{'scale'} ) ) {
						print "┗━<BR>\n";
					}
					else {
						print "<FONT color=\"#C0C0C0\">└─</FONT><BR>\n";
					}
					for (
						my ($k) = 0 ;
						$k < 2**( $T{'scale'} - $i - 1 ) - 1 ;
						$k++
					  )
					{
						print "<BR>\n";
					}
					print "<BR>\n" if ( $j < 2**$i - 1 );
				}
				print "<BR>\n";
				print "</td><td>\n";
			}
			print <<"EOM";
<td>
EOM
			for ( my ($i) = 2**$T{'scale'} ; $i < 2**$T{'scale'} * 2 ; $i++ ) {
				print "["
				  . $T{ "p" . ( $i + 1 ) . "id" } . "/"
				  . $T{ "p" . ( $i + 1 ) . "name" }
				  . "]<BR>\n";
				print "<BR>\n" if ( $i < 2**$T{'scale'} * 2 - 1 );
			}
		}
		print <<"EOM";
<BR>
</td>
</tr>
</table>
EOM

	}
	else {
		print <<"EOM";
<div id="room_list" style="text-align:left;">
EOM
		for my $i ( 1 .. $heyakazu ) {
			$notflg = 0;
			undef(%G);
			$gfn = "${room_dir}/" . $roomst . $i . '.cgi';
			my $exist   = 0;
			my $success = 1;
			my $maxdate = 0;
			if ( -e $gfn ) {
				open( IN, $gfn ) || ( $success = 0 );
				while (<IN>) {
					chomp;
					( $key, $val ) = split(/\t/);
					$G{$key} = $val;
				}
				close(IN);
				$maxdate =
				  ( $G{'date1'} > $G{'date2'} ) ? $G{'date1'} : $G{'date2'};
			}
			my ( $sec, $min, $hour, $mday, $mon, $year ) = localtime($maxdate);
			my $vdate = sprintf( "%02d:%02d", $hour, $min );

			if ( $success == 0 ) {
				if ( grep( /^$i$/, @beginner ) ) {
					print
"<div style=\"border: solid 1px; background-color: #b0ffb0;\">\n";
					print
"<strong style=\"margin: 5;\">部屋 $i</strong>[練習用]";
				}
				else {
					print "<div style=\"border: solid 1px;\">\n";
					print "<strong style=\"margin: 5;\">部屋 $i</strong>";
				}
				print
"部屋データを開けませんでした。<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">\n";
				$exist = 0;
			}
			elsif (
				(
					   ( $times - $maxdate > $natime * 60 )
					&& ( ($maxdate) || ( $G{'end_flg'} ) )
				)
				|| !( -e $gfn )
			  )
			{
				if ( grep( /^$i$/, @beginner ) ) {
					print
"<div style=\"border: solid 1px; background-color: #b0ffb0;\">\n";
					print
"<strong style=\"margin: 5;\">部屋 $i</strong>[練習用]";
				}
				else {
					print "<div style=\"border: solid 1px;\">\n";
					print "<strong style=\"margin: 5;\">部屋 $i</strong>";
				}
				print
"<label style=\"background-color:#C0C0C0;border-radius: 6px;padding: 3px;\">空室</label><input type=\"hidden\" name=\"duelpass${i}\" value=\"\">\n";
				copy "${room_dir}/" . $roomst . $i . '_log.cgi', "room_old/" . $roomst . $i . "_" . strftime("%Y%m%d%H%M%S", localtime(time)) . "_log.cgi";
				unlink(
					"${room_dir}/" . $roomst . $i . '.cgi',
					"${room_dir}/" . $roomst . $i . '_log.cgi',
					"${room_dir}/" . $roomst . $i . '_card.cgi'
				);
				$exist = 0;
			}
			else {
				$exist = 1;
				my ($dendou_cau) = (
					( $G{'dendou'} == 0 )
					  && ( ( !( $G{'side1'} ) && $G{'side2'} )
						|| ( !( $G{'side2'} ) && $G{'side1'} ) )
				) ? " background-image: url('$image/caution.gif');" : "";
				if (
					(
						   !$G{'side1'}
						|| !$G{'side2'}
						|| $G{'side1'} eq $G{'side2'}
					)
					&& (   ( $G{'side1'} eq $G{'duelid'} )
						|| ( $G{'side2'} eq $G{'duelid'} ) )
					&& ( $G{'duelid'} ne '' )
					&& ( $G{'choose'} == 0 )
				  )
				{
					print
"<div style=\"border: solid 1px; background-color: #b0ffff;\">\n";
					print
"<strong style=\"margin: 5;\">部屋 $i</strong>[一人練習用]";
				}
				elsif ( grep( /^$i$/, @beginner ) ) {
					print
"<div style=\"border: solid 1px; background-color: #b0ffb0;$dendou_cau\">\n";
					print
"<strong style=\"margin: 5;\">部屋 $i</strong>[練習用]";
				}
				else {
					print "<div style=\"border: solid 1px; $dendou_cau\">\n";
					print "<strong style=\"margin: 5;\">部屋 $i</strong>";
				}
				if ( $G{'end_flg'} ) {
					$notflg = 1;
					print
"対戦終了<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">";

#				print "<a href=\"javascript:sForm('prof','','$G{'side1'}');\">$G{'pn1'}</a><small>[$G{'side1'}]</small>VS<a href=\"javascript:sForm('prof','','$G{'side2'}');\">$G{'pn2'}</a><small>[$G{'side2'}]</small>\n";
				}
				elsif (( !( $G{'side1'} ) && $G{'side2'} )
					|| ( !( $G{'side2'} ) && $G{'side1'} ) )
				{
					print "対戦待ち";
					printf
"<a href=\"javascript:sForm('prof',$i,'%s');\">%s</a><small>[%s]</small>\n",
					  !( $G{'side1'} ) ? "$G{'side2'}" : "$G{'side1'}",
					  !( $G{'side1'} ) ? $G{'pn2'}     : $G{'pn1'},
					  !( $G{'side1'} ) ? $G{'side2'}   : $G{'side1'};
					printf $G{'dendou'} == 12 ? "殿堂禁止"
					  : $G{'dendou'} == 11 ? "CGIex公式"
					  : $G{'dendou'} == 10 ? "おやぢ環境"
					  : $G{'dendou'} == 4  ? "ゼロデュエル"
					  : $G{'dendou'} == 3  ? "SGL環境"
					  : $G{'dendou'} == 2  ? "AG環境"
					  : $G{'dendou'} == 1  ? "殿堂あり"
					  :   "<font color=\"#FF0000\">殿堂なし</font>";
					if ( $G{'dgroup'} eq '' ) {
						print "禁止なし";
					}
					else {
						print
"禁止あり （<A href=\"javascript:sForm('detail', $i, '');\">詳細</A>）";
					}
					print "\n";
					if ( $G{'choose'} == 1 ) {
						printf "パス指定：%s\n",
						  $G{'duelid'} eq ''
						  ? "なし<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">"
						  : "<input type=\"text\" size=\"8\" name=\"duelpass${i}\" value=\"\">";
					}
					elsif ( ( $G{'choose'} == 2 ) && ( $G{'white'} ne '' ) ) {
						printf
"友達のみ<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">\n";
						$notflg = 1
						  unless (
							grep( /^$id$/, split( /\,/, $G{'white'} ) ) );
					}
					elsif ( $G{'choose'} == 3 ) {
						printf "減算ポイント：$G{'duelid'}p以下\n";
					}
					else {
						if (
							(
								   ( $G{'side1'} eq $G{'duelid'} )
								|| ( $G{'side2'} eq $G{'duelid'} )
							)
							&& ( $G{'duelid'} ne '' )
						  )
						{
							print
"<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">\n";
						}
						else {
							printf "対戦者指定：%s\n",
							  $G{'duelid'} eq ''
							  ? "なし<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">"
							  : "$G{'duelid'}<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">";
						}
						$notflg = 1
						  if ( $G{'duelid'} ne $id && $G{'duelid'} ne '' );
					}
					print "\n";
					printf "一言：%s\n",
					  $G{'message'} eq '' ? "なし" : $G{'message'};
				}
				else {
					$notflg = 1;
					print
"対戦中<input type=\"hidden\" name=\"duelpass${i}\" value=\"\">\n";
					print
"<a href=\"javascript:sForm('prof','','$G{'side1'}');\">$G{'pn1'}</a><small>[$G{'side1'}]</small>VS<a href=\"javascript:sForm('prof','','$G{'side2'}');\">$G{'pn2'}</a><small>[$G{'side2'}]</small>\n";
				}
				# 最終チェックはなくても良さげなので外してみる
				# print "最終チェック：$vdate\n";
				print
"<a href=\"javascript:sForm('audience',$i,'')\">様子を見る</a>\n";
			}
			if (
				( $G{'dendou'} == 0 )
				&& (   ( !( $G{'side1'} ) && $G{'side2'} )
					|| ( !( $G{'side2'} ) && $G{'side1'} ) )
			  )
			{
				print
"<input type=\"button\" value=\"入室\" onclick=\"if(confirm('この部屋は殿堂ルールがなしに設定されています。')) sForm('duel',$i,$exist);\">\n"
				  if !($notflg) && ( !($mente) || ( $P{'admin'} > 0 ) );
			}
			else {
				print
"<input type=\"button\" value=\"入室\" onclick=\"sForm('duel',$i,$exist);\">\n"
				  if !($notflg) && ( !($mente) || ( $P{'admin'} > 0 ) );
			}
			print "</div>\n";
			# print "</tr><tr align=\"center\" valign=\"top\">"
			#   if ( $i - 1 ) % 5 == 4;
		}
		print <<"EOM";
</div>
EOM
	}
	if ( ( $P{'admin'} > 0 ) || ( $P{'subadmin'} > 0 ) ) {
		$admin_flg = 1;
	}
	print <<"EOM";
<hr>
<div class="dispChangeChat">
	<a id="dispChangeChat">入力する</a>
</div>
<div id="chatInputArea">
  <input type="hidden" name="chatName" value="$P{'name'}" />
  <textarea cols="40" rows="3" id="chatData" /></textarea><br>
  <input id="chatAdd" type="button" value="書き込み" />
  <input type="button" onClick="javascript:sForm('freeroom', '', '');" value="更新する">
  <div style="width:75%;font-size: 11px;">
  <br><b><font color=#ff0000>// 共有掲示板、チャットに関する注意事項 //</font><br>
<font color=blue>管理人及び副管理人が以下の行為に該当すると判断した場合、<font color=#ff0000>即刻アカウント規制</font>及び<font color=#ff0000>投稿の削除</font>をさせていただく場合がございますので、ご了承ください。<br></font>
・誹謗中傷・公序良俗に反する言動・暴言などの書き込み<br>
・不要な連投 ※対戦募集コメントなども含む（他の方の投稿が流れてしまうため、どうしても必要な場合は複数回投稿せずに1度の書き込みにまとめるようお願いいたします）。<br>
・共有掲示板及びチャットの1chでデュエル・マスターズおよび当サイトと関係のない個人的な会話を延々と続けるなど(関係のない会話がしたい場合はチャットの1ch以外でお願いいたします)。<br></b>
  </div>
</div>
  <div align="center" style="width: 500px; height: 180px; overflow: scroll;">
  <dl>
  <dd id="view">ここにデータ</dd>
  </dl>
  </div>

<hr>
<a href="./etc/help.html#kyoyu" class="jTip" id="100" name="共有掲示板" target="_brank">共有掲示板について</a>
</div>
</td><td class="adarea" style="vertical-align: top;">
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
	open(ADSFILE, "< data/ads.txt");
	
    print <<'EOM';
        <script>
		$(document).ready(function(){
		  $('.ad-scroll2').slick({
		  	draggable: true,
		    autoplay: true,
		    vertical: true,
		    slidesToShow: 6,
		    autoplaySpeed:10000,
		  });
		});
		</script>
		
		<div class="ad-scroll2" style="display:inline-block;width:160px;">
EOM
	$count = 1;
	while (my $ad = <ADSFILE>){
	  if ($count % 2 != 0) {
		chomp($ad);
		print "<div class='adblock'>$ad</div>";
	  }
	  $count++;
	}
	
	print "</div>";
}
        print <<"EOM";
</td></tr></table>
<hr width="640">
EOM
	if ( $F{'mode'} eq 'tourroom' ) {
		print
"<a href=\"javascript:sForm('tourroom', '', '');\">更新する</a>&nbsp;&nbsp;\n";
		print
"<a href=\"javascript:sForm('freeroom', '', '');\">フリールーム</a>&nbsp;&nbsp;\n";
		print
"　　<input type=\"button\" value=\"大会結果\" onclick=\"window.open(\'taikaiList/taikaiList.php\', \'\', \'width=800,height=600\');\">&nbsp;&nbsp;\n";
	}
	else {
		print
"<a href=\"javascript:sForm('freeroom', '', '');\">更新する</a>&nbsp;&nbsp;\n";
		print
"<a href=\"javascript:sForm('tourroom', '', '');\">トーナメントルーム</a>&nbsp;&nbsp;\n";
	}
	print <<"EOM";
<hr width="640">
<select id="user_list" size="7" onChange="document.entrance.viewid.value = this.value;" style="width:600px;">
<option value="" selected>－ 参加者一覧 －</option>
EOM
	for ( my ($i) = 0 ; $i <= $#new_member ; $i++ ) {
		my ( $mem_id, $mem_name, $mem_rank, $mem_comment, $mem_time, $mem_ip,
			$mem_channel )
		  = split( /<>/, $new_member[$i] );
		my ( $mem_sec, $mem_min, $mem_hour, $mem_mday, $mem_mon, $mem_year ) =
		  localtime($mem_time);
		$mem_wdate = sprintf( "%02d:%02d:%02d", $mem_hour, $mem_min, $mem_sec );
		print
"<option value=\"$mem_id\">$mem_channel : \[$mem_id\/$mem_name \($rankmark[$mem_rank]\)\] : $mem_comment ($mem_wdate)<\/option>\n";
	}
	print <<"EOM";
</select><br>
ID: <input type="text" name="viewid" size="16">&nbsp;のデータを&nbsp;<input type="button" value="見る" onClick="javascript:sForm('prof', '', document.entrance.viewid.value);">
</td></tr>
</table>
EOM
}

sub logview {
	$F{'line'} = 30 unless ( $F{'line'} );
	$F{'area'} = 1  unless ( $F{'area'} );
	my ($linesel10)  = ( $F{'line'} == 10 )  ? " selected" : "";
	my ($linesel20)  = ( $F{'line'} == 20 )  ? " selected" : "";
	my ($linesel30)  = ( $F{'line'} == 30 )  ? " selected" : "";
	my ($linesel50)  = ( $F{'line'} == 50 )  ? " selected" : "";
	my ($linesel100) = ( $F{'line'} == 100 ) ? " selected" : "";
	my ($areasel0)   = ( $F{'area'} == 0 )   ? " selected" : "";
	my ($areasel1)   = ( $F{'area'} == 1 )   ? " selected" : "";
	my ($areasel2)   = ( $F{'area'} == 2 )   ? " selected" : "";
	print <<"EOM";
<table border="0" width="720" cellpadding="3" cellspacing="0">
<tr><td align="center">
<input type="button" value="覚醒可能クリーチャー一覧" onclick="window.open('psychic_list.html', '', 'width=400,height=500,scrollbers=yes');">

<input type="button" value="大会参加希望登録" onclick="window.open('taikai/sanka.php', '', 'width=800,height=600');">
<input type="hidden" name="num">
<input type="hidden" name="pass2">
<input type="hidden" name="subm" value="$F{'mode'}">
</form>
EOM
	&bosyuu();
	print <<"EOM";
<br>
</td></tr>
<tr><td align="center">
<table width="90%" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
<tr><td>
<form action="$chatNodeHost/processChat" method="post" target="chatFrame" name="chatForm">
  <input name="username" type="hidden" value="$id"/>
  <input name="password" type="hidden" value="$pass"/>
  <input name="url" type="hidden" value="/lobbyCgi"/>
<iframe id="chatFrame" name="chatFrame" width="100%" height="465" scrolling="no"
 frameborder="0"></iframe>
</td></tr>
</table>
</td></tr>
</table>

EOM
}

sub explain {
	print <<"EOM";
<ul>
<li><strong>遊ぶ前に「対戦での注意」を読んでください。</strong></li>
<li>サーバーに負荷がかかるので、ボタンを短い間隔で連打しないでください。</li>
<li>途中で落ちた場合、５分以内なら「様子を見る」から入ればゲームに復帰できます。</li>
<li><strong style="color:red;">$natime分間アクセスがない場合、アクセスがない側の負けになります。</strong></li>
</ul>
<HR>
<b><a href="javascript:textView('oldatt');">過去のお知らせ</a></b><br>
<div id="oldatt" style="display:none;">
<table border="0">
<tr><td align="left">
<b><a href="javascript:textView('pakurio');">パクリオの効果について</a></b><br>
<div id="pakurio" style="display:none;">
<table border="0">
<tr><td align="left">
この対戦CGIでは、相手の手札から直接、<br>
場にカードを出すことができないため、<br>
パクリオの効果を、操作側から実行することができません。<br>
なので、パクリオを使用する際には、相手の手札を見た後、<br>
シールドに送るカード名を相手に伝え、<br>
相手側でシールドへの移動を行ってもらってください。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('touryou');">投了時のポイントについて</a></b><br>
<div id="touryou" style="display:none;">
<table border="0">
<tr><td align="left">
対戦終了後に入るポイントは、勝者側に８０Ｐ、敗者側に４０Ｐを基本として、<br>
減算カードによって相対的に変動します。
</td></tr>
</table>
</div>
<BR>
<b><a href="javascript:textView('kakusa');">ランクの格差によるポイントの増減について</a></b><br>
<div id="kakusa" style="display:none;">
<table border="0">
<tr><td align="left">
当ＣＧＩで導入されているランク制度はただのお飾りですが、<br>
対戦者の同士のランクの格差によって得られるポイントに差をつけてみました。<br>
ランクの高い人と低い人が闘った場合、対戦終了後のポイントは<br>
低い方が多く、高い方は少なくなるようにしました。<br>
差分はランク分で、例えばＺ（26）の人とＡ（1）の人が闘った場合、<br>
Ｚの人には-25Ｐ、Ａの人には+25Ｐされるようになりました。<br>
つまり、強い人が弱い人を相手にしても、あまり意味がないってことですね。<br>
ちなみに、ポイントをハチャメチャに集めると得られる勲章があるとかないとか。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('bakkutoriga');">S・トリガーとS・バックが被った際の処理方法</a></b><br>
<div id="bakkutoriga" style="display:none;">
<table border="0">
<tr><td align="left">
この対戦CGIでは、ブレイクされたシールドがS・トリガーだった場合、<br>
手札にS・バックカードがあっても、S・バックを発動させることが出来ません。<br>
なので、もしもS・トリガーではなくS・バックを使用したい場合は、<br>
一旦S・トリガーを発動させて、そのS・トリガーの処理中にS・トリガーを墓地に置き、<br>
S・バックカードを手札から出してください。<br>
後は通常通りS・バックの操作を行い、トリガー処理を終了すれば完了です。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('kunsyou');">収得した勲章の表示方法</a></b><br>
<div id="kunsyou" style="display:none;">
<table border="0">
<tr><td align="left">
このページの下にある伝言板に書き込んだ時、<br>
収得した勲章を１つ表示させることができますが、<br>
表示させるためには勲章を収得した後、<br>
トップページから登録情報の変更に行って、<br>
表示させる勲章を選ぶ必要があります。<br>
ちなみ、収得した勲章が１つも無い場合は、<br>
当然表示させることができません。<br>
また、２つ以上の勲章を同時に表示させることできませんので、<br>
予めご了承ください。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('tansyoku');">単色デッキ等の勝利数について</a></b><br>
<div id="tansyoku" style="display:none;">
<table border="0">
<tr><td align="left">
単色デッキや５色デッキを使い続けて勝利を重ねると、<br>
それぞれに応じた勲章がもらえますが、<br>
これらは全て15ターン以上をかけての勝利が条件となります。<br>
14ターン以内での勝利は入手ポイント補正もかかりますので、<br>
一般に速攻と呼ばれるデッキタイプは損をする形となっています。<br>
また、カードパワーの低いカードを多く入れることによって手に入る勲章や、<br>
ハイランダー、フルレインボーデッキの勲章も同様となっています。<br>
(※14ターン＝１プレイヤー7ターン)
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('feizu');">フェイズについて</a></b><br>
<div id="feizu" style="display:none;">
<table border="0">
<tr><td align="left">
当CGIでは、ドローフェイズやマナチャージフェイズといった<BR>
一連の流れが存在しません。<BR>
これは、フェイズの移行についての手間を省くためで、<BR>
ドロー→フェイズ移行→マナチャージ→フェイズ移行・・・と続く流れを、<BR>
ドロー→マナチャージ→召還や呪文→バトル→ターン終了と、<BR>
少ない操作でターンを終わらせられるようになります。<BR>
他の対戦CGIを使っていた方々にとっては使いづらいかもしれませんが、<BR>
慣れるとスピーディにデュエルが進みます。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('kanrinin');">デュエル中の管理者発言について</a></b><br>
<div id="kanrinin" style="display:none;">
<table border="0">
<tr><td align="left">
デュエルをしている時、突如ログに対戦者以外の発言が<BR>
出ることがありますが、これは何らかの問題が起きた時、<BR>
物事を解決するために管理者から行われるものです。<BR>
普通にしている限りでは管理者は何もしませんが、<BR>
発言がある時には何某かの問題があるということですので、<BR>
もしも管理者からの発言があった際には、その言う事に従うようにしてください。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('sasou');">人をデュエルに誘う際の諸注意</a></b><br>
<div id="sasou" style="display:none;">
<table border="0">
<tr><td align="left">
この対戦待ちページに居る人をデュエルに誘う場合、<BR>
一度呼んだ人と違う人とデュエルしたい場合、<BR>
また、何らかの理由でデュエルが出来なくなった場合には、<BR>
キャンセルする旨を書き込むようにしてください。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('oyadi');">おやぢ電動ルールについて</a></b><br>
<div id="oyadi" style="display:none;">
<table border="0">
<tr><td align="left">
おやぢ電動ルールとは、某所のオフ会で採用された殿堂ルールで、<BR>
通常のプレミアム殿堂・殿堂カードに加え、以下のカードが追加されています。<BR>
<BR>
・プレミアム殿堂入りカード<BR>
&nbsp;&nbsp;&nbsp;ロスト・チャージャー<BR>
&nbsp;&nbsp;&nbsp;ヘル・スラッシュ<BR>
&nbsp;&nbsp;&nbsp;フューチャー・スラッシュ<BR>
&nbsp;&nbsp;&nbsp;ボルメテウス・ホワイト・ドラゴン<BR>
&nbsp;&nbsp;&nbsp;ボルメテウス・サファイア・ドラゴン<BR>
&nbsp;&nbsp;&nbsp;呪紋の化身 <BR>
&nbsp;&nbsp;&nbsp;闘匠メサイヤ<BR>
&nbsp;&nbsp;&nbsp;無双恐皇ガラムタ<BR>
&nbsp;&nbsp;&nbsp;霊騎ガリウム<BR>
&nbsp;&nbsp;&nbsp;陽炎の守護者ブルー・メルキス<BR>
&nbsp;&nbsp;&nbsp;封魔ダンリモス<BR>
&nbsp;&nbsp;&nbsp;覇竜凰ドルザバード<BR>
&nbsp;&nbsp;&nbsp;緑神龍ダグラドルグラン<BR>
<BR>
・殿堂入りカード<BR>
&nbsp;&nbsp;&nbsp;バジュラズ・ソウル<BR>
&nbsp;&nbsp;&nbsp;パシフィック・チャンピオン<BR>
&nbsp;&nbsp;&nbsp;凶星王ダーク・ヒドラ<BR>
&nbsp;&nbsp;&nbsp;魂と記憶の盾<BR>
&nbsp;&nbsp;&nbsp;母なる大地<BR>
&nbsp;&nbsp;&nbsp;転生プログラム<BR>
&nbsp;&nbsp;&nbsp;凶戦士ブレイズ・クロー<BR>
&nbsp;&nbsp;&nbsp;火炎流星弾<BR>
&nbsp;&nbsp;&nbsp;タイラーのライター<BR>
&nbsp;&nbsp;&nbsp;炎舞闘士サピエント・アーク
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('shinkasyoumetsu');">進化クリーチャーが消滅する</a></b><br>
<div id="shinkasyoumetsu" style="display:none;">
<table border="0">
<tr><td align="left">
クリーチャーを進化させた際、まれに進化クリーチャーが消滅することがあります。<BR>
この際、一度マナゾーン等からクリーチャーを場に出すことで再度出現することがあります。<BR>
その後、一度その進化クリーチャーを手札に戻し、マナゾーン等から出したクリーチャーを元の場所に戻した後、<BR>
戻した進化クリーチャーをもう一度出すことで解決できる場合があります。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('kyousei');">5分間無アクセスによる強制退室について</a></b><br>
<div id="kyousei" style="display:none;">
<table border="0">
<tr><td align="left">
DM対戦CGIでは5分間アクセスがないと強制的に退室される機能がありますが、<br>
5分間、相手を束縛する行為は重いものとして、<br>
当CGIでは退室だけでなく、同時に敗北にもなるようになっています。<br>
しかし、それでも5分間アクセスをしない人が数多くいるため、<br>
強制退室による敗北ではポイントの上下が更に激しくなるようにしました。<br>
具体的に、デュエルに勝った側には80P、負けた側には40P入っていたポイントを、<br>
強制退室で勝った側には120P、負けた側には0Pになるようにしました。<br>
急用などで抜けないといけなくなった場合は、速やかに投了するようにしてください。<br>
また、相手の了承を得ずに長時間放置することは、マナー違反にあたり、処罰されます。<br>
</td></tr>
</table>
</div>
</td></tr>
</table>
</div>

<br>
<b><a href="javascript:textView('mannerrule');">このCGIで制定されているルールについて</a></b><br>
<div id="mannerrule" style="display:inline;">
<table border="0">
<tr><td align="left">
トップにリンクが貼ってありますが、いまいち読んでいる人が少ないようなのでこの場で告知しておきます。<br>
<a href="http://s2.whss.biz/~corile/dm/etc/help3.html" target="_blank">対戦時などのマナー</a>に定義されているルールを破った場合、対戦中の試合の強制敗北、<br>
状況如何ではアクセス規制などの処置をとらせていただきます。<br>
「読んでいなかった」などの言い訳は通用しませんので、ご一読いただくようお願いします。<br>
<br>
(以下、4月10日追記)<br>
また、当ＣＧＩにおいては対戦開始時に挨拶(「よろしくお願いします」等)を行うことが<br>
暗黙の了解的な位置づけで執り行われているようですが、<br>
これについて、管理者個人としては挨拶を強制させるような意思はもっておりません。<br>
ゆえに、ルールとして挨拶を必ず行わなければならないようなものを制定する気はありませんが、<br>
<b>挨拶ひとつもできないような人が、まともであるとは思えない</b>といったように捉えられることを否むことはできません。<br>
対戦ＣＧＩは相手の顔や表情が見えなくはあれど、対戦相手は人間です。<br>
そこからコミュニケーションを省くことは決してできず、意思が充分に伝わらなければ争いが起こることは必至です。<br>
無用なトラブルを避けるためにも、形式的ながら対戦開始時の挨拶は心がけるようお願い申し上げます。<br>
<br>
なお、挨拶をしなかったという事だけで一方的に腹を立て、無断退室や不当な退室許可要求などをすることは<br>
ルール違反として処罰いたしますので、その点も留意していただくようお願いします。<br>
<br>
また、挨拶をしないこと自体、ルール上に置いては問題はありません。<br>
そのため、それを理由にした迷惑報告は受け付けていませんのでご留意ください。<br>
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('mudan');">無断投了と無断退室について</a></b><br>
<div id="mudan" style="display:none;">
<table border="0">
<tr><td align="left">
投了はゲームとしてユーザーに与えられている権利です。<br>
それを断る権利は相手には一切存在しませんし、<br>
むしろそれを却下することはルール違反として罰せられます。<br>
それゆえ、相手に確認を求める必要はありません。<br>
<br>
ただし、退室に関しては相手の前から去るということです。<br>
現実で考えてみればわかりますが、相手の目の前で急に背を向けて<br>
立ち去るということは、実に非常識な行いです。<br>
一見、投了と退室は二つで一つのようですが、実際は似て非なるものです。<br>
<br>
ちなみに、無断退室をすると、投了によって敗北した時よりも<br>
ポイント減算及び相手へのポイント加算は激しいものになります。<br>
無断退室に遭ったら、むしろラッキー程度に思っていただけるとありがたいです。<br>
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('dendoulist');">2008年6月29日時点での殿堂入り</a></b><br>
<div id="dendoulist" style="display:none;">
<table border="0">
<tr><td align="left">
■ プレミアム殿堂入りカード (デッキに入れることができない)<br>
・ヘル・スラッシュ<br>
・ロスト・チャージャー<br>
・無双竜機ボルバルザーク<br>
・炎槍と水剣の裁<br>
・フューチャー・スラッシュ<br>
・アクア・パトロール<br>
・ボルメテウス・サファイア・ドラゴン<br>
<br>
■ 殿堂入りカード (デッキに1枚のみ入れることができる)<br>
・サイバー・ブレイン<br>
・ディープ・オペレーション<br>
・ストリーミング・シェイパー<br>
・エメラル<br>
・アストラル・リーフ<br>
・アクアン<br>
・スケルトン・バイス<br>
・予言者マリエル<br>
・クローン・バイス<br>
・アクア・ハルカス<br>
・呪紋の化身<br>
・母なる大地<br>
・魂と記憶の盾<br>
・パシフィック・チャンピオン<br>
・インフェルノ・ゲート<br>
・インフィニティ・ドラゴン<br>
・超竜バジュラ<br>
<br>
■ プレミアム殿堂コンビカード (これらの組み合わせをデッキに入れることができない)<br>
・龍仙ロマネスク＋母なる大地<br>
・龍仙ロマネスク＋母なる紋章<br>
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('cantshinka');">対応していない進化について</a></b><br>
<div id="cantshinka" style="display:none;">
<table border="0">
<tr><td align="left">
マナ進化クリーチャーや、一部の進化クリーチャーに関して、対応していないものが存在していない。<br>
その場合、普通にバトルゾーンへ出そうとしても、条件が整っていないとしてエラーが返されますが、<br>
場に出したい対象のカードを一度マナゾーンに置いた後、そのカードにチェックを入れ、<br>
メニューから「バトルゾーンへ」を行うことへ場に出すことができます。
</td></tr>
</table>
</div>
<br>
<b><a href="javascript:textView('bagu');">現在確認されているバグ</a></b><br>
<div id="bagu" style="display:inline;">
<table border="0">
<tr><td align="left">
最新弾のカードデータを適用しましたが、本体の更新はまだですので、<BR>
新しく追加されたカードの効果が発揮されないことや、<BR>
新しく追加されたカードでゴッド・リンクが出来ないなどの報告はご遠慮いただくようお願いします。<BR>
最新弾のカードに関するバグをご報告いただいても、仕様であるとしか言いようがありません。
</td></tr>
</table>
</div>
EOM
}

sub channel {
	&error("伝言板番号の値が正しくありません。")
	  unless ( $F{'room'} >= 1 && $F{'room'} <= 9 );
	$P{'channel'} = $F{'room'};
	&pfl_write( $P{'id'} );
	$F{'mode'} = $F{'subm'};
}

sub room_num {
	my $n = $_[0];
	my $m = $_[1];
	my $r = 0;
	for ( my $i = 0 ; $i < $n ; $i++ ) {
		$r += 2**$m / ( 2**$i );
	}
	return $r;
}

sub room_rev {
	my $n = $_[0];
	my $m = $_[1];
	my $r = 0;
	for ( my $i = 0 ; $i < $m - $n ; $i++ ) {
		$r += 2**$i;
	}
	return $r;
}

sub ret_phase {
	my ($n) = $_[0];
	my ($m) = $_[1];
	my ($t) = 0;
	for ( my ($i) = 0 ; $i < $m ; $i++ ) {
		$t += 2**( $m - $i );
		return $i if ( $n <= $t );
	}
	return $m;
}

sub line_chk {
	my ($n) = $_[0];
	my ($m) = $_[1];
	my ($f) = &ret_phase( int( ( $n + 1 ) / 2 ), $m );
	for ( my ($i) = 0 ; $i < 2**$f ; $i++ ) {
		my ($t) = ( $n - &room_num( $f, $m ) * 2 - 1 ) * 2**$f + 1 + $i;
		return 1 if ( $T{"p${t}win"} > $f );
	}
	return 0;
}

sub get_ini {
	&error(
"プレイヤーファイルがありません。<br>IDを設定しなおしてください。"
	) if !( -e "${player_dir}/" . $id . ".cgi" ) && $pass ne $admin;
	&pfl_read($id) if -e "${player_dir}/" . $id . ".cgi";
	&pass_chk if $pass ne $admin;
	

	# ユーザー検索（node連携）
	my $url = $chatNodeHost . '/user/find?user_id='.$id;
	$request = POST( $url );
	
	# 送信
	my $ua = LWP::UserAgent->new(ssl_opts => { verify_hostname => 0 });
	my $res = $ua->request( $request );
	
	my $arrRes = decode_json($res->content);
	my $auth = 0;
	if ($P{'admin'} > 0) {
		$auth = $P{'admin'};
	}
	if ($res->is_success) {
		if (scalar @$arrRes > 0) {
			#ユーザーが存在したら更新（node連携）
			my $url = $chatNodeHost . '/user/update/' . @$arrRes[0]->{id} . '?password=' . $pass . '&username=' . $P{'name'} . '&auth=' . $auth;
			$request = POST( $url );

			# 送信
			my $ua = LWP::UserAgent->new(ssl_opts => { verify_hostname => 0 });
			my $res = $ua->request( $request );
# 			&error(
# $res->base
# 	)
		} else {
			#存在しなかったら登録（node連携）
			my $url = $chatNodeHost . '/user/create?user_id=' . $id . '&password=' . $pass . '&username=' . $P{'name'};
			$request = POST( $url );

			# 送信
			my $ua = LWP::UserAgent->new(ssl_opts => { verify_hostname => 0 });
			my $res = $ua->request( $request );

			# &error(
			# 	$res
			# 		);
		}
	}

	for my $i ( 1 .. $maxdeck ) {
		unless ( $P{"deck$i"} ) { $dnam[$i] = "記録なし"; next; }
		else { ( $dnam[$i], $dum ) = split( /-/, $P{"deck$i"} ); }
	}
	$selstrd[ $P{'usedeck'} ] = " selected" if $P{'usedeck'};
	for my $i ( 1 .. $maxgroup ) {
		unless ( $P{"group$i"} ) { $gnam[$i] = "記録なし"; next; }
		else { ( $gnam[$i], $gum ) = split( /-/, $P{"group$i"} ); }
	}
	$selstrg[ $P{'usegroup'} ] = " selected" if $P{'usegroup'};
}

sub detail {
	&cardread;
	$gfn = "${room_dir}/" . $roomst . $F{'room'} . '.cgi';
	open( IN, $gfn );
	while (<IN>) { chomp; ( $key, $val ) = split(/\t/); $G{$key} = $val; }
	close(IN);
	&header;
	print <<"EOM";
</head>
<body>
	<div align="center">
		<h1>$title</h1>
<table width="640" border="1" cellspacing="0" cellpadding="10" class="table"><tr><td align="center"> 
	<h2>禁止カードリスト</h2>
	<table border="0" cellpadding="5">
		<tr><td>
EOM
	foreach $dg ( split( /\,/, $G{'dgroup'} ) ) {
		print "$c_name[$dg]<BR>\n";
	}
	print <<"EOM";
		</td></tr>
	</table>
</td></tr></table>
EOM
	&footer;
}

sub tourrule {
	&cardread;
	%T = ();
	&filelock("tr");
	chmod 0666, "./tour/part.dat";
	open( TRT, "./tour/part.dat" );
	while (<TRT>) { chop; ( $KEY, $VAL ) = split(/\t/); $T{$KEY} = $VAL; }
	close(TRT);
	&fileunlock("tr");
	&header;
	print <<"EOM";
</head>
<body>
	<div align="center">
		<h1>$title</h1>
<table width="640" border="1" cellspacing="0" cellpadding="10" class="table"><tr><td align="center">
	<h3>募集人数</h3>
EOM
	print 2**$T{'scale'} * 2 . "人\n";
	print <<"EOM";
	<h3>ポイント制限</h3>
EOM

	if ( $T{'point'} >= 0 ) {
		print "$T{'point'}p以下\n";
	}
	else {
		print "制限なし\n";
	}
	print <<"EOM";
	<h3>Ｐ殿堂入りカード</h3>
	<table border="0" cellpadding="5">
		<tr><td>
EOM
	foreach $p_fame ( split( /\,/, $T{'p_fame'} ) ) {
		print "$c_name[$p_fame]<BR>\n";
	}
	print <<"EOM";
		</td></tr>
	</table>
	<h3>殿堂入りカード</h3>
	<table border="0" cellpadding="5">
		<tr><td>
EOM
	foreach $fame ( split( /\,/, $T{'fame'} ) ) {
		print "$c_name[$fame]<BR>\n";
	}
	print <<"EOM";
		</td></tr>
	</table>
</td></tr></table>
EOM
	&footer;
}

sub write {
	&error("現在、あなたの書き込みは禁止されています。")
	  if $P{'deny'};
	&error("伝言板番号の値が正しくありません。")
	  unless ( $P{'channel'} >= 1 && $P{'channel'} <= 9 );
	&error("伝言を入力してください。")
	  if $F{'comment'} eq "" || $F{'comment'} eq "伝言をどうぞ";
	$F{'comment'} =~ s/</&lt\;/g;
	$F{'comment'} =~ s/>/&gt\;/g;
	$F{'comment'} =~ s/Bold\((.*?)\)/\<b\>$1\<\/b\>/g;
	$F{'comment'} =~ s/Italic\((.*?)\)/\<i\>$1\<\/i\>/g;
	$F{'comment'} =~ s/Underline\((.*?)\)/\<u\>$1\<\/u\>/g;
	$F{'comment'} =~ s/Strike\((.*?)\)/\<s\>$1\<\/s\>/g;
	$F{'comment'} =~
	  s/Invisible\((.*?)\)/\<font color=\"\#FFFFFF\"\>$1\<\/font\>/g;
	$F{'comment'} =~ s/\\\(/\(/g;
	$F{'comment'} =~ s/\\\)/\)/g;
	&error("伝言が長すぎます。") if length( $F{'comment'} ) > $leng;
	&filelock("msg");
	&read_log;

	chmod 0666, "log/lognumber.dat";
	open( NUM, "log/lognumber.dat" )
	  || &error("ログ番号記録ファイルが開けません。");
	$lognumber = <NUM>;
	close(NUM);

	my $top = shift(@lines);
	( $no, $time2, $lid ) = split( /<>/, $top );
	$no++;
	&error("$ptime秒間は連続投稿ができません。")
	  if ( ( $times - $time2 < $ptime ) && ( $P{'id'} eq $lid ) );
	local @new = ();
	local @old = ();
	foreach my $i ( 0 .. $#lines ) {
		push( @new, $lines[$i] ) if $i < $maxview;
		push( @old, $lines[$i] ) if $i >= $maxview;
	}
	my $pw    = &pass_enc( $F{'pass'} );
	my $order = "";
	$order = $P{'order'} if ( $P{"order_$P{'order'}"} );
	$wchan = ( $F{'area'} == 1 ) ? $P{'channel'} : "";
	$wlist = ( $F{'area'} == 2 ) ? $P{'white'}   : "";

	unshift( @new,
"$no<>$wdate<>$P{'id'}<>$P{'name'}<>$F{'comment'}<>$pw<>$ENV{'REMOTE_ADDR'}<>$order<>$pc_chk<>$wlist<>$P{'black'}<>$wchan<>\n"
	);
	unshift( @new, "$no<>$times<>$P{'id'}\n" );
	&write_log;

	foreach (@old) {
		my (
			$num, $wdate, $lid,   $name,  $com,   $pass,
			$ip,  $order, $pcchk, $white, $black, $channel
		) = split(/<>/);
		$_ = '' if ( $white ne '' );
	}

	open( LOG, ">>log/msglog${lognumber}.dat" );
	print LOG @old;
	close(LOG);
	my ($fsize) = -s "log/msglog${lognumber}.dat";
	if ( $fsize >= 50000 ) {
		$lognumber++;
		open( NUM, ">log/lognumber.dat" )
		  || &error("ログ番号記録ファイルが開けません。");
		print NUM $lognumber;
		close(NUM);
	}

	&fileunlock("msg");
	$F{'mode'}    = $F{'subm'};
	$F{'comment'} = '';
}

sub delete {
	&error("削除する伝言の番号を入力してください")
	  unless $F{'num'};
	&read_log;
	my $top = shift(@lines);
	local @new = ();
	foreach (@lines) {
		( $no, $dum, $dum, $dum, $dum, $pw ) = split(/<>/);
		if ( $F{'num'} == $no ) {
			&error("削除する伝言のパスワードが違います。")
			  if crypt( $F{'pass2'}, $F{'pass2'} ) ne $pw
				  && ( ( $P{'admin'} <= 0 ) && ( $P{'subadmin'} <= 0 ) );
		}
		else { push( @new, $_ ); }
	}
	unshift( @new, $top );
	&filelock("msg");
	&write_log;
	&fileunlock("msg");
	$F{'mode'} = $F{'subm'};
}

sub read_log {
	chmod 0666, "word.dat";
	open( WORD, "word.dat" )
	  || &error("伝言ファイルが開けません。");
	@lines = <WORD>;
	close(WORD);

	#	chmod 0000, "word.dat";
}

sub write_log {
	chmod 0666, "word.dat";
	open( OUT, ">word.dat" )
	  || &error("伝言ファイルに書きこめません。");
	print OUT @new;
	close(OUT);

	#	chmod 0000, "word.dat";
}

sub set_cookie {
	my ( $sec, $min, $hour, $mday, $mon, $year ) =
	  gmtime( time + 30 * 24 * 60 * 60 );
	$gdate = sprintf(
		"%02d\-%s\-%04d %02d:%02d:%02d",
		$mday,
		(
			'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
			'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
		  )[$mon],
		$year + 1900,
		$hour, $min, $sec
	);
	$cook = "id:$F{'id'},pass:$F{'pass'},pc:$pc_chk";
	print "Set-Cookie: duel=$cook; expires=$gdate GMT\n";
}

sub get_cookie {
	$cookies = $ENV{'HTTP_COOKIE'};
	@pairs = split( /;/, $cookies );
	foreach $pair (@pairs) {
		( $name, $value ) = split( /=/, $pair );
		$name =~ s/ //g;
		$D{$name} = $value;
	}
	@pairs = split( /,/, $D{'duel'} );
	foreach $pair (@pairs) {
		( $name, $value ) = split( /:/, $pair );
		$C{$name} = $value;
	}
	$c_id   = $C{'id'};
	$c_pass = $C{'pass'};
	$pc_chk = $C{'pc'};
}

sub decode2 {
	$id   = $F{'id'};
	$pass = $F{'pass'};
	$pass =~ s/\.//g;
	$pass =~ s/\///g;
	&error("IDが入力されていません")                 unless $id;
	&error("パスワードが入力されていません。") unless $pass;
}

sub bosyuu {

	open( IN, "setting.txt" );
	@aaa = <IN>;
	close(IN);
	foreach $bbb (@aaa) {

		my @ccc = split( /@@/, $bbb );

		if ( $ccc[0] == 'bosyuu' and $ccc[1] == '1' ) {
			print <<"EOM";

<img src="./tnm.png" width="60" height="30" name="myIMG"><br>

EOM
		}
	}
}

sub kaisai {

	open( IN, "setting.txt" );
	@aaa = <IN>;
	close(IN);
	foreach $bbb (@aaa) {

		my @ccc = split( /@@/, $bbb );

		if ( ( $ccc[1] != "kaisai" ) && ( $ccc[1] == '1' ) ) {
			print <<"EOM";

<img src="./kaisai.png" width="60" height="17" name="myIMG"><br>

EOM
		}
	}
}
