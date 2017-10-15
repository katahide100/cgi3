<?php
require_once './config/define.php';
require_once './config/common.php';
?>
<html>
<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<meta http-equiv="Pragma" content="no-cache">
	<link rel="stylesheet" href="./css/duel.css" type="text/css">
	<script type="text/javascript" src="./js/jquery-1.11.2.min.js"></script>
	<title>デュエル・マスターズ対戦CGI ex</title>
<script type="text/javascript"><!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		if(M == "deck") {
			entrance.action = "deck.cgi";
		} else if(M == "taisen") {
			entrance.action = "taisen.cgi";
		} else if(M == "prof") {
			entrance.action = "taisen.cgi";
		} else if(M == "group") {
			entrance.action = "group.cgi";
		} else if(M == "list") {
			entrance.action = "list.cgi";
		} else if(M == "nuisance") {
			entrance.action = "nuisance.cgi";
		} else if(M == "log") {
			entrance.action = "log-old.cgi";
		} else if(M == "index") {
			entrance.action = "index.cgi";
		} else {
			entrance.action = "log.php";
		}
		entrance.target = (M == "prof") ? "_blank" : "_self";
		entrance.submit();
	}
// --></script>
</head>
<body onLoad="document.chatForm.submit();">

<div align="center">
<h1>デュエル・マスターズ対戦CGI ex</h1>
<div class="paging centered">
<ul>
<li><a href="javascript:sForm('taisen', '', '');">対戦する</a></li>
<li><a href="javascript:sForm('info', '', '');">お知らせ</a></li>
<li><a href="javascript:sForm('deck', '', '');">デッキ構築</a></li>
<li><a href="javascript:sForm('group', '', '');">グループ編集</a></li>
<li><a href="javascript:sForm('list', '', '');">リスト編集</a></li>
<li><a href="javascript:sForm('nuisance', '', '');">迷惑行為</a></li>
<li><a href="javascript:sForm('log', '', '');">旧チャットログ</a></li>
<li><a href="javascript:sForm('index', '', '');">トップへ戻る</a></li>
</ul>
</div>
<form action="log.php" method="post" name="entrance" style="display: inline;">
	<input type="hidden" name="id" value="<?php echo $common->loginId ?>">
	<input type="hidden" name="pass" value="<?php echo $common->loginPass ?>">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
</form>
<hr width="640">

<table width="700" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
<tr><td>
<table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
<tr><td>
<form action="<?php echo CHAT_SERVER_URL ?>/processChat" method="post" target="chatFrame" name="chatForm">
  <input name="username" type="hidden" value="<?php echo $common->loginId ?>"/>
  <input name="password" type="hidden" value="<?php echo $common->loginPass ?>"/>
  <input name="url" type="hidden" value="/chatLogCgi"/>
</form>
<iframe name="chatFrame" width="100%" height="465" scrolling="no" frameborder="0"></iframe>
</td></tr>
</table>
</td></tr>
</table>

</div>
	</div>
	<div align="right">
( CPU:  0.01 User:  0.00 System:  0.01 )	</div>
</body>
</html>