<?php

date_default_timezone_set('Asia/Tokyo');

// データを書き込むファイル
define('DATA_FILE', './data/data');
define('LOG_EXT', '.log');

/**
 * データを取得
 */
function getData() {
	return file_get_contents(DATA_FILE.'0'.LOG_EXT);
}

/**
 * 更新チェック
 *
 * 対象データに変化が無ければループし続ける。
 * 変化が有れば新しいデータ追加した全てのデータを返す。
 */
function getUpdatedData() {
	$data = getData();
	$temp = $data;
// 	while ($temp === $data) {
// 		$temp = getData();
// 		sleep(1);
// 	}
	return $temp;
}

/**
 * データ追加
 *
 * 新しいデータを追加して全てのデータを返す。
 */
function pushData($name, $data) {
	if (!empty($data)) {
		$data = $name.'  > '.str_replace(array("\n", "\r"), PHP_EOL, $data)
		. ' (' . date("Y/m/d H:i:s") . ') - ' . $_SERVER["REMOTE_ADDR"] . PHP_EOL
		. '-------------------------------------------------------' . PHP_EOL;
		$contentTemp=file(DATA_FILE.LOG_EXT);
		array_unshift($contentTemp, $data);
		file_put_contents(DATA_FILE.LOG_EXT, $contentTemp, LOCK_EX);
		$content = array_chunk($contentTemp, 40);
		
		foreach($content as $key => $val){
			$strWrite = implode($val);
			file_put_contents(DATA_FILE.$key.LOG_EXT, $strWrite, LOCK_EX);
		}
	}
	
	return getData();
}

if (isset($_GET['mode'])) {
	// モードの振り分け
	switch ($_GET['mode']) {
		// データを取得
		case 'view':
			$data = getData();
			break;

			// 更新チェック
		case 'check':
			$data = getUpdatedData();
			break;

			// データを保存
		case 'add':
			$data = pushData($_POST['name'], $_POST['data']);
			break;
	}
	
	// 結果を表示
	echo nl2br(htmlspecialchars($data, ENT_QUOTES));
}



function debug($message){
	ob_start();
	var_dump($message);
	$result =ob_get_contents();
	ob_end_clean();
	
	$fp = fopen("../log/debug.log", "a+" );
	fputs($fp, $result);
	fclose( $fp );
}
?>
