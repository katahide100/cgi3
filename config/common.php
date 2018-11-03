<?php
require_once 'define.php';

class Common {
    // 共通クラス

    public $loginId = ''; // ログインユーザーのID
    public $loginPass = ''; // ログインユーザーのパスワード

    function __construct() {
        $this->getAuth();
    }

    // ログイン情報取得
    private function getAuth() {
        $arrCookie = explode(',', $_COOKIE['duel']);
        foreach ($arrCookie as $cookie) {
            $pair = explode(':', $cookie);
            if ($pair[0] == 'id') {
                $this->loginId = $pair[1];
            }
            if ($pair[0] == 'pass') {
                $this->loginPass = $pair[1];
            }
            if ($pair[0] == 'name') {
                $this->loginName = $pair[1];
            }
        }
    }

    public function getUser() {
        $id = $this->loginId;
        $curl = curl_init();

        curl_setopt($curl, CURLOPT_URL, NODE_SERVER_URL.'/user/find?user_id=' . $id);
        curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'GET');
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); // 証明書の検証を行わない
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);  // curl_execの結果を文字列で返す

        $response = curl_exec($curl);
        $result = json_decode($response, true);

        curl_close($curl);

        return $result[0];
    }
}

$common = new Common();