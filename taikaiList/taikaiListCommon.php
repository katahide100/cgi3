<?php
// 大会リスト用共通関数群

/**
* 初期表示用パラメータ取得関数
* 説明：登録画面の、デフォルト値を取得する
*
*/
function getDefaultParam(){

	$taikaiTitle = '';                  // 大会名
	$winUser     = '';                  // 優勝者名
	$winDeck     = '';                  // 優勝者デッキ
	$kaisaiDate  = '';                  // 開催日
	$arrUser     = '';                  // 参加ユーザー一覧
	
	// 初期表示用パラメータ取得処理 =============================
	
	// 大会datファイル読み込み
	$line = file("../tour/part.dat");
	
	// 一行ごとに処理
	foreach($line as $key => $val){
		// タブ区切り
		$arrData = split("\t", $val);
		
		// 大会名取得
		if($arrData[0] == 'title'){
			$taikaiTitle = str_replace("\n","",$arrData[1]);
		}
		
		// 優勝者id取得
		if(preg_match("/p(.*)win/", $arrData[0])){
			if(isset($tmpPoint) && $arrData[1] > $tmpPoint){
				$tmpPoint = $arrData[1];
				$tmpUid = str_replace("\n","",str_replace("win","",$arrData[0]));
			}elseif(!isset($tmpPoint)){
				$tmpPoint = $arrData[1];
				$tmpUid = str_replace("\n","",str_replace("win","",$arrData[0]));
			}
		}
		
		// 参加ユーザー一覧
		if(preg_match("/p(.*)name/", $arrData[0])){
			$arrUser[str_replace("name","",$arrData[0])] = str_replace("\n","",$arrData[1]);
		}
	}
	
	// 優勝者名、優勝者デック取得
	foreach($line as $key2 => $val2){
		// タブ区切り
		$arrData = split("\t", $val2);
		
		if($arrData[0] == $tmpUid.'name'){
			$winUser = str_replace("\n","",$arrData[1]);
		}
		if($arrData[0] == $tmpUid.'deck'){
			$winDeck = str_replace("\n","",$arrData[1]);
		}
	}
	
	// 現在月日取得
	$kaisaiDate = date("Y/m/d");
	
	// 値詰め替え
	$arrRtnParam['taikaiTitle'] = $taikaiTitle;
	$arrRtnParam['winUid']      = $tmpUid;
	$arrRtnParam['winUser']     = $winUser;
	//  デックは登録時に判定、取得することにする
	//$arrRtnParam['winDeck']   = $winDeck;
	$arrRtnParam['kaisaiDate']  = $kaisaiDate;
	$arrRtnParam['arrUser']     = $arrUser;
	
	
	return $arrRtnParam;
}

/**
* バリデーション処理
*
*/
function validate($arrParam){

	$arrChkParam = $arrParam;
	$errMessage  = '';
	
	// 大会名のバリデーション ================
	
	// 必須入力チェック
	if(!isset($arrChkParam['taikaiTitle']) || is_null($arrChkParam['taikaiTitle'])
		 || $arrChkParam['taikaiTitle'] == ''){
    	$errMessage .= "大会名は必須項目です。<br>";
	}
	
	// 禁止文字バリデーション
	if(ereg("[_=;.\"\'&]",  $arrChkParam['taikaiTitle'])){
		$errMessage .= "大会名に禁止文字が含まれています。<br>";	
	}
	
	// 開催日のバリデーション ================
	
	// 必須入力チェック
	if(!isset($arrChkParam['kaisaiDate']) || is_null($arrChkParam['kaisaiDate'])
		 || $arrChkParam['kaisaiDate'] == ''){
    	$errMessage .= "開催日は必須項目です。<br>";
	}
	
	if(!strptime($arrChkParam['kaisaiDate'], '%Y/%m/%d')){
 		$errMessage .= "開催日を正しく入力してください。<br>";
	}
	
	// 優勝者のバリデーション ================
	
	if(!isset($arrChkParam['winUserNm'])){
		// 必須入力チェック
		if(!isset($arrChkParam['winUser']) || is_null($arrChkParam['winUser'])
			 || $arrChkParam['winUser'] == ''){
	    	$errMessage .= "優勝者は必須項目です。<br>";
		}else{
		
			// 半角英字チェック
			if(!preg_match("/^[a-zA-Z0-9]+$/", $arrChkParam['winUser'])){
	    		$errMessage .= "優勝者は半角英字の小文字で入力してください。<br>";
			}
		
		}
	}else{
		// 必須入力チェック
		if(!isset($arrChkParam['winUserNm']) || is_null($arrChkParam['winUserNm'])
			 || $arrChkParam['winUserNm'] == ''){
	    	$errMessage .= "優勝者は必須項目です。<br>";
		}
		
		// 禁止文字バリデーション
		if(ereg("[_=;.\"\'&]",  $arrChkParam['winUserNm'])){
			$errMessage .= "優勝者に禁止文字が含まれています。<br>";	
		}
		
	}
	
	// デッキ登録のバリデーション ================
	
	// もしデッキ登録するにチェックが入っていた場合
	if($arrChkParam['regDeck'] == '1'){
		// 必須入力チェック
		if(!isset($arrChkParam['deckName']) || is_null($arrChkParam['deckName'])
			 || $arrChkParam['deckName'] == ''){
    		$errMessage .= "デッキ名は必須項目です。<br>";
		}else{
			// 禁止文字バリデーション
			if(ereg("[_=;.\"\'&]",  $arrChkParam['deckName'])){
				$errMessage .= "デッキ名に禁止文字が含まれています。<br>";	
			}
		}
	}
	
	// 一言のバリデーション ================
	
	// 禁止文字バリデーション
	if(ereg("[_=;.\"\'&]",  $arrChkParam['comment'])){
		$errMessage .= "ひとことに禁止文字が含まれています。<br>";	
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
	$fp = fopen("./taikaiList.csv","r");
	
	// 一行ごとに処理
	while($line = fgets($fp)){
		$data = explode(',',$line);
		if(!is_null($data) && count($data) > 0){
		
			// TODO 同じ大会名がないかチェック(新規のみ)
			// 更新の場合は同じ大会名と入れ替える必要あり
			if($data[0] == $arrWriteParam['taikaiTitle']){
				echo "同じ大会名が存在します。別の名前で登録してください。<br>";
				return false;
			}
			
			// 出力用パラメータにセット
			$strCsvData .= $data[0].','.$data[1].','.$data[2].','.$data[3].','.$data[4].','.$data[5]."\n";
		}
	}
	
	// 大会datファイル読み込み
	$line = file("../tour/part.dat");
	
	// 優勝者名、優勝者デック取得
	if(isset($arrWriteParam['winUserNm'])){
		$winUser  = $arrWriteParam['winUserNm'];
		$winDeck  = '';
		$winDeckP = '';
	}else{
		if($line != array() && $line != null){
			foreach($line as $key => $val){
				// タブ区切り
				$arrData = split("\t", $val);
				
				if($arrData[0] == $arrWriteParam['winUser'].'name'){
					$winUser = str_replace("\n","",$arrData[1]);
				}
				if($arrData[0] == $arrWriteParam['winUser'].'deck'){
					$arrDeck  = explode('-',str_replace("\n","",$arrData[1]));
					$winDeck  = $arrDeck[0];
					$winDeckP = $arrDeck[1];
				}
			}
		}
	}
	
	// TODO 追加する大会をパラメータにセット(新規のみ)
	$strCsvData .= $arrWriteParam['taikaiTitle'].','.$arrWriteParam['kaisaiDate'].','.$winUser.','.$arrWriteParam['regDeck'].','.$arrWriteParam['deckName'].','.$arrWriteParam['comment']."\n";
	
	// csvファイルクローズ
	fclose($fp);
	$fp = null;
	
	// csv書き込み処理(共通) =========================
	
	if($strCsvData != ''){
		
		// 追記モード
		$fp = fopen("./taikaiList.csv", 'ab');
	
		// ファイルを排他ロックする
		flock($fp, LOCK_EX);

		// ファイルの中身を空にする
		ftruncate($fp, 0);

		// データをファイルに書き込む
		$writeResult = fwrite($fp, $strCsvData);
	
		fclose($fp);

		// デッキ登録処理 =================================

		if($arrWriteParam['regDeck'] == '1' && isset($winDeck) && $winDeck != ''){
		
			$strDatData = '';
			
			// デッキdatファイル読み込み
			$line = file("../deck.dat");
			
			// 一行ごとに処理
			foreach($line as $key => $val){
				$strDatData .= $val;
			}
			
			$no     = mb_strrpos($strDatData,'/dm');
			$arrRen = explode(".",mb_substr($strDatData,$no + 3));
			$renNo  = $arrRen[0];
			$nextRenNo = $renNo + 1;
			
			// 追加するデックを作成
			$strDatData .= $arrWriteParam['deckName'].'-'.$winDeck.'-100/dm'.$nextRenNo.'.html'.'-'.$winDeckP."\n";
			
			// 追記モード
			$fpd = fopen("../deck.dat", 'ab');
		
			// ファイルを排他ロックする
			flock($fpd, LOCK_EX);

			// ファイルの中身を空にする
			ftruncate($fpd, 0);

			// データをファイルに書き込む
			$writeDatResult = fwrite($fpd, $strDatData);
		
			fclose($fpd);
		}

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
* 登録済み大会結果リスト取得処理
* 説明：
*
*/
function getTaikaiList(){

	$arrTaikaiList = array();          // 大会結果リスト
		
	// 大会結果リスト作成処理 =============================
	
	// csvファイル読み込み
	$fp = fopen("./taikaiList.csv","r");
	
	// 一行ごとに処理
	while($line = fgets($fp)){
		$data = explode(',',$line);
		if(!is_null($data) && count($data) > 0){
			$arrTaikaiList[] = $data;
		}
	}
		
	// csvファイルクローズ
	fclose($fp);
	$fp = null;
	
	return $arrTaikaiList;
}

/**
* 勲章削除処理
* 説明：
*
*/
function delTaikai($taikaiNm){

	// csvテキスト削除処理 =============================
	
	// csvファイル読み込み
	$fp = fopen("./taikaiList.csv","r");
	
	$strCsvData = '';
	
	// 一行ごとに処理
	while($line = fgets($fp)){
		$data = explode(',',$line);
		if(!is_null($data) && count($data) > 0){
		
			// 削除する大会名と違う場合のみ変数に格納
			if($data[0] != $taikaiNm){
				$strCsvData .= $data[0].','.$data[1].','.$data[2].','.$data[3].','.$data[4].','.$data[5]."\n";
			}
			
		}
	}
	
	// csvファイルクローズ
	fclose($fp);
	$fp = null;
	
	// csv書き込み処理(共通) =========================
	
	if($strCsvData !== null){
		// 追記モード
		$fp = fopen("./taikaiList.csv", 'ab');
	
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