<?php
		/*
			*プログラム名：野球ゲームプログラムStep9
			*説明：正解数がユニークであるかどうかの表示を止め、ユニークになった時のみ正解数を表示する。
			*作成者：片岡 秀昌
			*作成日：2013年5月16日
		*/
	$number=$_POST['number'];	//入力数値を受け取る。

	if(!ereg("^[0-9]{3}$",$number)){	//3桁の数字でなかった場合、エラーメッセージを設定。
		 $msg="⇒エラー！！3桁の数字ではありません。<br>\n";
	}else{
		for($i=0;$i<3;$i++){	//3桁の入力値を1桁ずつに分解し、配列に格納。
			$one_num[]=substr($number,$i,1);
		}
		if($one_num[0]==$one_num[1]){	//重複判定。
			$msg ="⇒ユニークではありません。<br>\n";
		}elseif($one_num[0]==$one_num[2]){
			$msg ="⇒ユニークではありません。<br>\n";
		}elseif($one_num[1]==$one_num[2]){
			$msg ="⇒ユニークではありません。<br>\n";
		}else{
			$msg = "⇒ユニークです。<br>\n";
		}
	}
	$k=0;
	while($k==0){	//重複がなくなるまで（$kが0の間は)ループさせる。
		for($j=0;$j<3;$j++){	//3つのランダムな数字を配列に格納。
			$rand[$j]=rand(0,9);
		}
		if($rand[0]==$rand[1]){	//正解数の重複判定。
		}elseif($rand[0]==$rand[2]){
		}elseif($rand[1]==$rand[2]){
		}else{
			$k=1;
		}
	}
	$ans_num=$rand[0].$rand[1].$rand[2]."<br>\n";	//3つの数字を連結。
?>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	</head>
	<body>
		<b>野球プログラム</b><br>
		<br>
		<form action="" method="post">
			3桁の数字を入力してください。：<input type="text" name="number" value="<?=$number?>"><br>
			<input type="submit" value="結果表示">
		</form>
		入力値：<?=$number?><br>
		<?=$msg?>
		正解数：<?=$ans_num?>
	</body>
</html>