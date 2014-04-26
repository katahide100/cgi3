<?php

// 関数群のファイル読み込み
require_once ('./editSymbolCommon.php');

// +++++++++ 勲章登録画面 +++++++++++ //

if(isset($_POST) && !is_null($_POST) && count($_POST) > 0){

	$getParam = $_POST;
	$getFiles = $_FILES;
	
	// 入力内容バリデーションチェック
	$result = validate($getParam,$getFiles);
	
	// 勲章画像アップロード
	if($result){
		$fupResult = fileupload($getParam['title'],$getFiles);
		
		// csvファイル書き込み
		if($fupResult){
			writeProc($getParam);
		}
	}
	
}

?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="../css/duel.css" media="all">
</head>
<body>
<form action="" method="post" enctype="multipart/form-data">

<br>
<center>
<h1>勲章登録機能</h1>
<table border="1">
<tr>
<td>
<br>
勲章英語名(半角英字)：<br>
<input type='text' name='title' value='' size="12" maxlength="12"><br>
※最大12文字。全角文字、半角数字、半角記号などは使えません。<br>
<br>
説明（例：～である証）：<br>
<input type='text' name='setumei' value='' size="30" maxlength="200"><br>
※最大200文字。一部半角記号などは使えません。<br>
<br>
種別：
<select name='symbol'>
    <option value='★'>イベント系
    <option value='□'>幾度も勝利
    <option value='■'>数多くの勝利
    <option value='◆'>特別賞(パワーの低いもののみなど）
    <option value='▲'>エキスパート系
    <option value='☆'>管理、権限系
</select>
<br>
<br>
画像ファイル：<br>
<input type="file" name="upfile" size="30" /><br>
※拡張子は.pngにしてください。<br>
<br>
<center>
<input type="submit" value="登録" />
<input type="button" onclick="location.href='./listSymbol.php'" value="一覧画面" />
</center>
</td>
</tr>
</table>
</center>
</form>
</body>
</html>
