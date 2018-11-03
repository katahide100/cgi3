<?php
   require_once '../../config/common.php';

   $id = $common->loginId;
   $curl = curl_init();

   curl_setopt($curl, CURLOPT_URL, NODE_SERVER_URL.'/user/find?user_id=' . $id);
   curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'GET');
   curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); // 証明書の検証を行わない
   curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);  // curl_execの結果を文字列で返す

   $response = curl_exec($curl);
   $result = json_decode($response, true);

   curl_close($curl);

   if ($result[0]['auth'] != 1) {
        // 認証エラー
        header('Location: ' . ADMIN_ERROR_URL . '?msg=権限がありません');
   }