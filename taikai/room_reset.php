<?php

$dir="../room/";
$dirHandle = opendir ( $dir );
while ( false !== ( $fileName = readdir ( $dirHandle ) ) ) {
	if ( $fileName != "." && $fileName != ".." ) {
		unlink ( $dir.$fileName );
	}
}
closedir ( $dirHandle );

?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="duel.css" media="all">
</head>
<body>
<center>
<br>
<table border="1">
<tr>
<td>
<center>
対戦部屋のリセットが完了しました。<br>
<br>
<input type="button" value="管理画面に戻る" onclick="location='../admin.cgi'">
</center>
</td>
</tr>
</table>
</center>
</body>
</html>