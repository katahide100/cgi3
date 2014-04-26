<?php
// 4.0.0-RC2 より前のバージョンでは、!== は存在しないことに注意しましょう

if ($handle = opendir('.')) {
    echo "ディレクトリ　ハンドル: $handle<br>\n";
    echo "ファイル名:<br>\n";

    /* ディレクトリをループする際の正しい方法です */
    while (false !== ($file = readdir($handle))) {
        echo "$file<br>\n";
    }
        closedir($handle);
}
?>
<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
</head>
<body>
<form action="dl.php" method="post">
ダウンロードするファイル名を入力してください。<br>
<input type="text" name="dl_file"><br>
<br>
<input type="submit" value="ダウンロード">
</form>
</body>
</html>