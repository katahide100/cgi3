<?php

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
        }
    }
}

$common = new Common();