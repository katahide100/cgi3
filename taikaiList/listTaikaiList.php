<?php

// 関数群のファイル読み込み
require_once ('./taikaiListCommon.php');

// +++++++++ 大会結果一覧画面(管理用) +++++++++++ //

// 大会結果一覧取得
$arrTaikaiList = getTaikaiList();

if(is_null($arrTaikaiList) || count($arrTaikaiList) <= 0){

	echo '大会リストの取得ができませんでした。<br>';
// 	exit;
	
}else{
	usort($arrTaikaiList, function($a, $b) {
		return $a[1] < $b[1];
	});
}

$arrPost = isset($_POST)?$_POST:null;

if(!is_null($arrPost)){
	// 削除処理
	if(isset($arrPost['del_line']) && !empty($arrPost['del_line'])){

		// ここで削除処理
		delTaikai($arrPost['del_line']);
			
		// ページリロード
		header("Location: " . $_SERVER['PHP_SELF']);
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
<h1>大会結果登録機能</h1>

<table border="1">
<tr>
<th>大会名</th>
<th>日付</th>
<th>優勝者</th>
<th>一言</th>
<th>削除</th>
</tr>
<?php
foreach($arrTaikaiList as $key => $val){
?>
<tr>
<form action="" method="post" onSubmit="return check()">
<td width="150"><?php echo $val[0] ?></td>
<td><?php echo $val[1] ?></td>
<td><?php echo $val[2] ?></td>
<td width="200"><?php echo $val[5] ?></td>
<td>
<input type="hidden" name="del_line" value="<?php echo $val[0] ?>">
<input type="submit" value="削除">
</td>
</form>
</tr>
<?php } ?>

</table>
<br>

<input type="button" onclick="location.href='./editTaikaiList.php'" value="新規登録" />
</center>
</body>
</html>
