<?php
$fp_t=fopen("taikai.csv","w");
fwrite($fp_t,"");
fclose($fp_t);
$fp = fopen("t_name.txt","w");
fwrite($fp,"");
fclose($fp);
$fp = fopen("t_time.csv","w");
fwrite($fp,"");
fclose($fp);
$fp_s = fopen("t_syusai.txt","w");
fwrite($fp_s,"");
fclose($fp_s);
if(isset($_COOKIE['meisyo'])){
	$meisyo_c=$_COOKIE['meisyo'];
}else{
	$meisyo_c="";
}
if(isset($_COOKIE['day'])){
	$day_c=$_COOKIE['day'];
}else{
	$day_c="";
}
if(isset($_COOKIE['syusai'])){
	$syusai_c=$_COOKIE['syusai'];
}else{
	$syusai_c="";
}
$fp_b=fopen("../setting.txt","w");
fwrite($fp_b,"bosyuu@@0");
fclose($fp_b);
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="duel.css" media="all">
</head>
<body>
<center>
<br>
<table border="1" bgcolor="#b0c4de">
<tr>
<td>
<center>
<br><b>大会管理画面</b><br>
<br>
<form action="t_kanri_kakunin.php" method="post">
大会名称<br>
<input type="text" name="meisyo" value="<?php echo $meisyo_c?>"><br>
ex) 第1回 対戦CGI ex 公式トーナメント<br>
<br>
開催日<br>
<input type="text" name="day" value="<?php echo $day_c?>" size="7"><br>
ex) 1/6<br>
<br>
主催者(主催する管理者のユーザー名)<br>
<input type="text" name="syusai" value="<?php echo $syusai_c?>"><br>
<br>
希望を取る時間<br>
<table border="1">
<tr>
<td>
<?php
$t_c=0;
for($t=6;$t <= 23;$t++){
	echo<<<EOF
	<input type="checkbox" name="time[{$t_c}]" value="{$t}時">{$t}時　
EOF;
	$t_c++;
	echo<<<EOF
	<input type="checkbox" name="time[{$t_c}]" value="{$t}時30分">{$t}時30分<br>
EOF;
	$t_c++;
}
?>
</td>
</tr>
</table>
<input type="submit" value="これで募集">
<input type="button" value="戻る" onclick="location='../admin.cgi'">
</form>
</center>
</td>
</tr>
</table>
</center>
</body>
</html>