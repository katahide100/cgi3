<?php

$post = $_POST;

$url = $post['url'];
 
// POST送信するデータ
$data = $post['data'];

// URL エンコード
$data = http_build_query($data, "", "&");

$header = array(
  "Content-Type: application/x-www-form-urlencoded",
  "Content-Length: ".strlen($data)
);

// 送信時のオプション
$options = array('http' => [
    'method' => 'POST',
    'content' => $data,
    'header' => implode("\r\n", $header),
  ],
  'ssl' => [
    'verify_peer' => false,
    'verify_peer_name' => false
  ]
);
 
// ストリームコンテキストを作成
$options = stream_context_create($options);
 
// file_get_contents
$contents = file_get_contents($url, false, $options);
 
// 出力
echo $contents;
?>
