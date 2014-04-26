<?php

if(empty($_POST['meisyo'])|| strlen($_POST['meisyo'])==0){
	echo "大会名を入力してください。<br>\n";
	echo "<br><br>ブラウザの戻るボタンで戻ってください。";
	exit;
}
if(empty($_POST['day'])|| strlen($_POST['day'])==0){
	echo "開催日を入力してください。<br>\n";
	echo "<br><br>ブラウザの戻るボタンで戻ってください。";
	exit;
}

if(empty($_POST['syusai'])|| strlen($_POST['syusai'])==0){
	echo "主催者名を入力してください。<br>\n";
	echo "<br><br>ブラウザの戻るボタンで戻ってください。";
	exit;
}

if(!isset($_POST['time']) || count($_POST['time'])==0){

	echo "希望時間を選択してください。<br>\n";
	echo "<br><br>ブラウザの戻るボタンで戻ってください。";
	exit;
}
setcookie("meisyo",$_POST['meisyo']);
setcookie("day",$_POST['day']);
setcookie("syusai",$_POST['syusai']);
$meisyo=htmlentities($_POST['meisyo'],ENT_QUOTES,'UTF-8');
$day=htmlentities($_POST['day'],ENT_QUOTES,'UTF-8');
$syusai=htmlentities($_POST['syusai'],ENT_QUOTES,'UTF-8');
$fp = fopen("t_name.txt", "w");
fwrite($fp, $meisyo."	".$day);
fclose($fp);
$fp_s = fopen("t_syusai.txt", "w");
fwrite($fp_s, $syusai);
fclose($fp_s);
$time=$_POST['time'];
foreach($time as $value){
$fp = fopen("t_time.csv", "a");
fwrite($fp, $value.",");
fclose($fp);
}
$fp_b=fopen("../setting.txt","w");
fwrite($fp_b,"bosyuu@@1");
fclose($fp_b);
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="duel.css" media="all">
</head>
<body>
<center>
<br><br>
<table border="1">
<tr>
<td>
<center>
<b>確認</b><br>
<br>
<?php
echo "大会名：".$meisyo."<br><br>";
echo "開催日：".$day."<br><br>";
echo "主催者：".$syusai."<br><br>";
echo "時間：<br>";
foreach($time as $value){
echo $value."<br>";
}
?>
<br>
<br>
以上の内容で募集しました。
<br>
<input type="button" value="管理画面に戻る" onclick="location='../admin.cgi'">
</center>
</td>
</tr>
</table>
</center>
</body>
</html>