<?php

// 関数群のファイル読み込み
require_once ('./taikaiListCommon.php');

// +++++++++ 大会結果一覧画面 +++++++++++ //

// 大会結果一覧取得
$arrTaikaiList = getTaikaiList();

if(is_null($arrTaikaiList) || count($arrTaikaiList) <= 0){

	echo '大会リストの取得ができませんでした。<br>';
	exit;
	
}else{
	usort($arrTaikaiList, function($a, $b) {
		return $a[1] < $b[1];
	});
}


?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="../css/duel.css" media="all">

</head>
<body>
<center>
<h1>大会結果</h1>
<form action="" method="post" onSubmit="return check()">

<table border="1">
<tr>
<th>大会名</th>
<th>日付</th>
<th>優勝者</th>
<th>一言</th>
</tr>
<?php
foreach($arrTaikaiList as $key => $val){
?>
<tr>
<td width="150"><?php echo $val[0] ?></td>
<td><?php echo $val[1] ?></td>
<td><?php echo $val[2] ?></td>
<td width="200"><?php echo $val[5] ?></td>
</tr>
<?php } ?>

</table>
<br>
</form>
</center>
</body>
</html>
