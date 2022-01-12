<?php

// 共通定数定義
define('NODE_SERVER_URL', 'https://manadream.net:1337');
define('CURRENT_HOST', (empty($_SERVER['HTTPS']) ? 'http://' : 'https://') . $_SERVER['HTTP_HOST'] . '/cgi3');
define('ADMIN_URL', CURRENT_HOST . '/admin');
define('ADMIN_ERROR_URL', ADMIN_URL . '/error.php');