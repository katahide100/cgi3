<?php

// 関数群のファイル読み込み
require_once ('./editSymbolCommon.php');

// +++++++++ 勲章一覧画面 +++++++++++ //

// 勲章一覧取得
$arrSymbolList = getSymbolList();

if(is_null($arrSymbolList) || count($arrSymbolList) <= 0){

	echo '勲章リストの取得ができませんでした。<br>';
	exit;
	
}

$arrPost = isset($_POST)?$_POST:null;

if(!is_null($arrPost)){
	// 削除処理
	foreach($arrPost as $key => $val){
		if(mb_substr($key, 0, 4) == 'del_'){
			// ここで削除処理
			delSymbol(mb_substr($key, 4));
			
			// ページリロード
			header("Location: " . $_SERVER['PHP_SELF']);
			
		}
	}
}

?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="../css/duel.css" media="all">
<script type="text/javascript"> 
<!-- 

function check(){

	if(window.confirm('削除してよろしいですか？')){ // 確認ダイアログを表示

		return true; // 「OK」時は送信を実行

	}
	else{ // 「キャンセル」時の処理

		// window.alert('キャンセルされました'); // 警告ダイアログを表示
		return false; // 送信を中止

	}

}
// -->
</script>
</head>
<body>
<center>
<h1>勲章登録機能</h1>
<form action="" method="post" onSubmit="return check()">
※ここで表示されている勲章は、カード登録機能のセーブをすることで、本登録されます。<br>
<table border="1">
<tr>
<th>連番</th>
<th>英語名</th>
<th>説明</th>
<th>マーク</th>
<th>削除</th>
</tr>
<?php
foreach($arrSymbolList as $key => $val){
?>
<tr>
<td><?php echo $key + 1 ?></td>
<td><?php echo $val[0] ?></td>
<td><?php echo $val[1] ?></td>
<td><?php echo $val[2] ?></td>
<td>
<input type="submit" name="del_<?php echo $val[0] ?>" value="削除">
</td>
</tr>
<?php } ?>

</table>
<br>
</form>
<input type="button" onclick="location.href='./editSymbol.php'" value="新規登録" />
</center>
</body>
</html>
