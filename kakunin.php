<?php
$name=$_POST['name'];
$time=$_POST['time'];
//null判定
$i=array("ユーザー名" => $name,"希望時間帯" => $time);
$b=0;
foreach($i as $key => $value){
	if($value==null){
		echo $key."を入力してください<br>";
		$b=true;
	}
}
//nullでなかった場合書き込み
if($b != true){
$fp = fopen("taikai.txt", "a");
fwrite($fp, $name."	".$time."\n");
fclose($fp);
}
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>確認</title>
</head>
<body>
<?php
if($b != true){
echo <<<EOF
<h1>確認画面</h1>
<br>
<br>
ユーザー名：{$name}<br>
希望時間：{$time}時<br>
<br>
<br>
以上の内容で登録しました。<br>
もし、時間を変更する場合は、もう一度送信してください。<br>
登録をやめたい場合は、ユーザー名の最初に※印を付けて送信してください。<br>
<br>
<input type="button" value="cgiに戻る" onclick="location='index.cgi'">
EOF;
}
else{
	echo <<<EOF
		<input type="button" value="戻る" onclick="location='taikai.html'">
EOF;
}
?>
</body>
</html>