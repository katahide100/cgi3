<?php
$fp=fopen("t_time.csv","r"); //管理人希望時間
$fp_t=fopen("taikai.csv","r"); //ユーザー希望時間
$fp_m=fopen("t_name.txt","r");
$fp_s=fopen("t_syusai.txt","r");
$line=fgets($fp);
$kibou=explode(',', $line);
$meisyo=fgets($fp_m);
$syusai=fgets($fp_s);
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
<?php
if(!empty($meisyo) || (isset($kibou[0]) && !empty($kibou[0]))){
?>
<?php echo $meisyo?><br>
<br>
主催者：<?php echo $syusai?><br>
<br>
参加希望者一覧<br>
<br>
<table border="1">
<tr>
<td><center>/</center></td>
<?php
foreach($kibou as $value){
	if(empty($value)){
	}else{
	echo "<td>".$value."</td>";
}
}
echo "</tr>";
while(!feof($fp_t)){
	$line4=fgets($fp_t);
	$user=explode(',', $line4);
	if(empty($user)){
	}else{
		echo "<tr><td>".$user[0]."</td>";
		foreach($kibou as $val){
			if(empty($val)){
			}else{
				echo "<td>";
				$a=0;
				foreach($user as $usrval){
					if($usrval == $val){
						echo "<center>○</center>";
						$a=1;
					}
				}
				if($a==0){
					echo"　";
				}
				echo "</td>";
			}
		}
		echo "</tr>";
	}
}
fclose($fp);
fclose($fp_m);
fclose($fp_t);
?>
</tr>
</table>
<input type="button" value="参加を希望する" onclick="location='t_touroku.php'">
<?php
}else{
	echo "現在大会参加希望の募集はしておりません";
}
?>
</center>
</td>
</tr>
</table>
</center>
</body>
</html>