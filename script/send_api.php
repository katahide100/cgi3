<?php

require_once '../config/define.php';

$post = $_POST;

$url = $post['url'];
 
// POST送信するデータ
$data = $post['data'];

// URL エンコード
$data = http_build_query($data, "", "&");

// 送信時のオプション
$options = array('http' => array(
    'method' => 'POST',
    'content' => $data,
));
 
// ストリームコンテキストを作成
$options = stream_context_create($options);
 
// file_get_contents
$contents = file_get_contents($url, false, $options);
 
// 出力
echo $contents;
?>
