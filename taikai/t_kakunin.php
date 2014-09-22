<?php
	header('Content-type: text/html; charset=UTF-8');
	if(empty($_POST['namae']) || strlen($_POST['namae'])==0){
		echo "エラー<br>ユーザー名を入力してください。<br>\n";
		echo "<br><br>ブラウザの戻るボタンで戻ってください。";
		exit;
	}
	/* TODO 登録できないエラーを回避（後で修正する）
	
	if(empty($_POST['time']) || strlen($_POST['time'])==0){
		echo "エラー<br>希望時間を選択してください。<br>\n";
		echo "<br><br>ブラウザの戻るボタンで戻ってください。";
		exit;
	}*/
	setcookie("namae",$_POST['namae']);
	$namae=htmlentities($_POST['namae'],ENT_QUOTES,'UTF-8');
	$time=$_POST['time'];
	$fp=fopen("taikai.csv","a");
	fwrite($fp,$namae.",");
	fclose($fp);
	$fp_t=fopen("taikai.csv","a");
	foreach($time as $value){
		fwrite($fp_t,$value.",");
	}
	fwrite($fp_t,"\n");
	fclose($fp_t);

?>
<html>
	<head>
		<link rel="stylesheet" type="text/css" href="duel.css" media="all">
	</head>
	<body>
	<center>
	<br><br>
	<table border="1">
	<tr>
	<td>
	<center>
	<h1>登録完了</h1>
	<br>
	ユーザー名：<?php echo $namae?><br>
	<br>
	希望時間：
	<?php
		foreach($time as $value){
			echo $value.",";
		}
	?>
	<br><br>
	以上の内容で登録しました。<br>
	ご協力ありがとうございました。
	<br>
	<input type="button" value="戻る" onclick="location='sanka.php'">
	</center>
	</td>
	</tr>
	</table>
	</center>
	</body>
	</html>