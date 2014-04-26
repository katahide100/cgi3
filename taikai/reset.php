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
<br>
<table border="1">
<tr>
<td>
<center>
<br>
全ての登録情報をリセットしました。<br>
<br>
<input type="button" value="戻る" onclick="location='../admin.cgi'">
</center>
</td>
</tr>
</table>
</center>
</body>
</html>