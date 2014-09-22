<?php
$fp = fopen('t_name.txt', 'r');
$name = fgets($fp);
$fp_t=fopen('t_time.csv','r');
$line = fgets($fp_t);
$time = explode(',',$line);
$fp_s = fopen('t_syusai.txt', 'r');
$syusai = fgets($fp_s);
if(isset($_COOKIE['namae'])){
	$namae_c=$_COOKIE['namae'];
}
else{
	$namae_c="";
}
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="duel.css" media="all">
</head>
<body>
<center>
<br><br>
<table border="1" bgcolor="#b0c4de">
<tr>
<td>
<center>
<h1>登録画面</h1>
<br>
<h1><?php echo $name?></h1><br>
<br>
主催者：<?php echo $syusai?><br>
<br>
<form action="t_kakunin.php" method="post">
ユーザー名：<input type="text" name="namae" value="<?php echo $namae_c?>"><br>
<br>
希望時間帯（複数選択可）<br>
<?php
$c=0;
foreach($time as $value){
	if($value==""){
		break;
	}
	else{
	echo<<<EOF
	<input type="checkbox" name="time[{$c}]" value="{$value}">{$value}<br>
EOF;
	$c++;
	}
}
?>
<input type="submit" value="登録"><input type="button" value="戻る" onclick="location='sanka.php'">
</form>
</center>
</td>
</tr>
</table>
</center>
</body>
</html>