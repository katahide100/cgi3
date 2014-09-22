<?php

/**
* ファイルアップロード用関数
*
*/
function fileUpload($fileName,$getFiles){

	// 同じ名前のファイルがあるかチェック(新規のみ)
	if(!file_exists("../symbols/" . 'symbol_'.$fileName.'.png')){
	
		// ファイルがサーバに一時アップロード済みか確認。
		if (is_uploaded_file($getFiles["upfile"]["tmp_name"])) {

			// ファイルアップロード処理(ファイル移動)
			if (move_uploaded_file($getFiles["upfile"]["tmp_name"], "../symbols/" . 'symbol_'.$fileName.'.png')) {
				chmod("../symbols/" . 'symbol_'.$fileName.'.png', 0777);
	    		echo "../symbols/" . 'symbol_'.$fileName.'.png' . "をアップロードしました。<br>";
	    		return true;
			} else {
	    		echo "ファイルをアップロードできません。<br>";
	    		return false;
			}
		} else {
			echo "ファイルが選択されていません。<br>";
			return false;
		}
	}else{
		echo "同じ名前の勲章が存在します。別の名前を付けてください。<br>";
		return false;
	}
}

/**
* ファイル削除用関数
*
*/
function fileDelete($fileName){

	// 同じ名前のファイルがあるかチェック(新規のみ)
	if(file_exists("../symbols/" . 'symbol_'.$fileName.'.png')){
	
		// 削除実行
		unlink("../symbols/" . 'symbol_'.$fileName.'.png');
		
	}else{
		return false;
	}
}

/**
* バリデーション処理
*
*/
function validate($arrParam,$getFiles){

	$arrChkParam = $arrParam;
	$errMessage  = '';
	
	// 勲章名のバリデーション ================
	
	// 必須入力チェック
	if(!isset($arrChkParam['title']) || is_null($arrChkParam['title'])
		 || $arrChkParam['title'] == ''){
    	$errMessage .= "勲章名は必須項目です。<br>";
	}else{
	
		// 半角英字チェック
		if(!preg_match("/^[a-z]+$/", $arrChkParam['title'])){
    		$errMessage .= "勲章名はすべて半角英字の小文字で入力してください。<br>";
		}
	
	}
	
	// 禁止文字バリデーション
	if(ereg("[_=;.\"\'&]",  $arrChkParam['title'])){
		$errMessage .= "勲章名に禁止文字が含まれています。<br>";	
	}
	
	// 説明のバリデーション ================
	
	// 必須入力チェック
	if(!isset($arrChkParam['setumei']) || is_null($arrChkParam['setumei'])
		 || $arrChkParam['setumei'] == ''){
    	$errMessage .= "説明は必須項目です。<br>";
	}
	
	// 禁止文字バリデーション
	if(ereg("[<>_=;.\"\'&]",  $arrChkParam['setumei'])){
		$errMessage .= "説明に禁止文字が含まれています。<br>";	
	}
	
	// 画像ファイルのバリデーション ================
	
	// 必須入力チェック
	if(!isset($getFiles['upfile']['name']) || is_null($getFiles['upfile']['name'])
		 || $getFiles['upfile']['name'] == ''){
    	$errMessage .= "画像ファイルは必須項目です。<br>";
	}
	
	// pingファイルかチェック
	$arrFileNm = explode('.',$getFiles['upfile']['name']);
	if($arrFileNm[1] != 'png'){
		$errMessage .= "画像は拡張子をpngにしてください。<br>";
	}
	
	if($errMessage != ''){
		echo $errMessage;
		return false;
	}else{
		return true;
	}
}

/**
* ファイル書き込み処理
* 説明：csvファイル書き込み後、本番に書き込む
*
*/
function writeProc($arrParam){

	$arrWriteParam = $arrParam;   // csvに追加（更新）するパラメータ
	$strCsvData    = '';          // csvに書き込むテキスト
	
	if(is_null($arrWriteParam) || $arrWriteParam == array()){
		echo "エラーが発生しました。<br>";
		return false;
	}
	
	// csvテキスト作成処理 =============================
	
	// csvファイル読み込み
	$fp = fopen("./kunsyo.csv","r");
	
	// 一行ごとに処理
	while($line = fgets($fp)){
		$data = explode(',',$line);
		if(!is_null($data) && count($data) > 0){
		
			// TODO 同じ勲章名がないかチェック(新規のみ)
			// 更新の場合は同じ勲章名と入れ替える必要あり
			if($data[0] == $arrWriteParam['title']){
				echo "同じ勲章名が存在します。別の名前で登録してください。<br>";
				return false;
			}
			
			// 出力用パラメータにセット
			$strCsvData .= $data[0].','.$data[1].','.$data[2]."\n";
		}
	}
	
	// TODO 追加する勲章をパラメータにセット(新規のみ)
	$strCsvData .= $arrWriteParam['title'].','.$arrWriteParam['setumei'].','.$arrWriteParam['symbol']."\n";
	
	// csvファイルクローズ
	fclose($fp);
	$fp = null;
	
	// csv書き込み処理(共通) =========================
	
	if($strCsvData != ''){
		// 追記モード
		$fp = fopen("./kunsyo.csv", 'ab');
	
		// ファイルを排他ロックする
		flock($fp, LOCK_EX);

		// ファイルの中身を空にする
		ftruncate($fp, 0);

		// データをファイルに書き込む
		$writeResult = fwrite($fp, $strCsvData);
	
		fclose($fp);

		if($writeResult == false){
			echo "csvへの書き込みに失敗しました。<br>";
			return false;
		}else{
			echo "csvへの書き込みに成功しました。<br>";
			return true;
		}
	}
}

/**
* 登録済み勲章リスト取得処理
* 説明：
*
*/
function getSymbolList(){

	$arrSymbolList = array();          // 勲章リスト
		
	// 勲章リスト作成処理 =============================
	
	// csvファイル読み込み
	$fp = fopen("./kunsyo.csv","r");
	
	// 一行ごとに処理
	while($line = fgets($fp)){
		$data = explode(',',$line);
		if(!is_null($data) && count($data) > 0){
			$arrSymbolList[] = $data;
		}
	}
		
	// csvファイルクローズ
	fclose($fp);
	$fp = null;
	
	return $arrSymbolList;
}

/**
* 勲章削除処理
* 説明：
*
*/
function delSymbol($symbolNm){

	// csvテキスト削除処理 =============================
	
	// csvファイル読み込み
	$fp = fopen("./kunsyo.csv","r");
	
	// 一行ごとに処理
	while($line = fgets($fp)){
		$data = explode(',',$line);
		if(!is_null($data) && count($data) > 0){
		
			// 削除する勲章名と違う場合のみ変数に格納
			if($data[0] != $symbolNm){
				$strCsvData .= $data[0].','.$data[1].','.$data[2]."\n";
			}
			
		}
	}
	
	// csvファイルクローズ
	fclose($fp);
	$fp = null;
	
	// ファイル削除処理実行
	fileDelete($symbolNm);
	
	// csv書き込み処理(共通) =========================
	
	if($strCsvData != ''){
		// 追記モード
		$fp = fopen("./kunsyo.csv", 'ab');
	
		// ファイルを排他ロックする
		flock($fp, LOCK_EX);

		// ファイルの中身を空にする
		ftruncate($fp, 0);

		// データをファイルに書き込む
		$writeResult = fwrite($fp, $strCsvData);
	
		fclose($fp);

		if($writeResult == false){
			echo "削除に失敗しました。<br>";
			return false;
		}else{
			echo "削除に成功しました。<br>";
			return true;
		}
	}
}
?>