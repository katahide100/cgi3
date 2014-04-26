<?php
chmod("../tour/part.dat", 0755); 
chmod("../tour", 0755); // 8 進数; 正しいモードの値
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
<br>
※この画面は、大会を開催後に、最終処理をするための画面です。<br>
<br>
パーミッションの変更が完了しました。<br>
大会は開催されます。<br>
<br>
<input type="button" value="管理画面に戻る" onclick="location='../admin.cgi'">
</center>
</td>
</tr>
</table>
</center>
</body>
</html>