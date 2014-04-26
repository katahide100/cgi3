<?php

// 関数群のファイル読み込み
require_once ('./taikaiListCommon.php');

// +++++++++ 大会リスト作成画面 +++++++++++ //

// 初期値投入
$arrDefaultParam = getDefaultParam();


if(isset($_POST) && !is_null($_POST) && count($_POST) > 0){

	$getParam = $_POST;
	
	// 入力内容バリデーションチェック
	$result = validate($getParam);
	
	// csv書き込み
	if($result){
		
		// csvファイル書き込み
		writeProc($getParam);
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
<h1>大会結果登録機能</h1>
<table border="1">
<tr>
<td>
<br>
大会名：<br>
<input type='text' name='taikaiTitle' value="<?php echo $arrDefaultParam['taikaiTitle'];?>" size="30" maxlength="100"><br>
※最大100文字。一部半角記号などは使えません。<br>
<br>
開催日：<br>
<input type='text' name='kaisaiDate' value=<?php echo $arrDefaultParam['kaisaiDate'];?> size="14" maxlength="15"><br>
年、月、日を"/"区切りで入力<br>
<br>
優勝者名：<br>
<?php if(is_array($arrDefaultParam['arrUser'])){ ?>
<select name='winUser'>
<?php foreach($arrDefaultParam['arrUser'] as $key => $val){
		if($key == $arrDefaultParam['winUid']){?>
			<option value=<?php echo $key;?> selected><?php echo $val;?>
		<?php }else{ ?>
			<option value=<?php echo $key;?>><?php echo $val;?>
		<?php } ?>
<?php } ?>
</select>
<?php }else{ ?>
	<input type='text' name='winUserNm' value="" size="30" maxlength="100"><br>
	※最大100文字。一部半角記号などは使えません。<br>
<?php } ?>
<br>
<?php if(is_array($arrDefaultParam['arrUser'])){ ?>
<br>
優勝者デッキ登録：<br>
<input type='radio' name='regDeck' value='0' checked='checked'>登録しない　<input type='radio' name='regDeck' value='1'>登録する<br>
<br>
デッキ名：<br>
<input type='text' name='deckName' value='' size="30" maxlength="100"><br>
※最大100文字。一部半角記号などは使えません。<br>
<br>
<?php }else{ ?>
<input type='hidden' name='regDeck' value='0'>
<?php } ?>
ひとこと：<br>
<input type='text' name='comment' value='' size="30" maxlength="200"><br>
※優勝者からひと言など(何でもいい)。<br>
※最大200文字。一部半角記号などは使えません。<br>

<center>
<br>
<input type="submit" value="登録" />
<input type="button" onclick="location.href='./listTaikaiList.php'" value="一覧画面" />
</center>
</td>
</tr>
</table>
</center>
</form>
</body>
</html>
