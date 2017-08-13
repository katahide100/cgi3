<?php
    $param = $_POST;

    $tmpPath = "../../tmp/help/contents.txt";

    // ファイル書き込み確認
    if (is_writable($tmpPath)) {
        if (!$handle = fopen($tmpPath, 'w')) {
            $message = "一時ファイルが開けませんでした。";
            exit;
        }

        if (fwrite($handle, $param['contents']) === FALSE) {
            $message = "一時ファイルの書き込みに失敗しました。";
            exit;
        }

        $message = "一時ファイル登録完了しました。";

        fclose($handle);
    } else {
        $message = "一時ファイル作成の権限がありませんでした。";
    }

    $templatePath = "template.txt";
    $templateFile = file_get_contents($templatePath);

    $html = str_replace("{{CONTENTS}}", $param['contents'], $templateFile);

    $path = "../../etc/help.html";

    $message = '';

    // ファイル書き込み確認
    if (is_writable($path)) {
        if (!$handle = fopen($path, 'w')) {
            $message = "ファイルが開けませんでした。";
            exit;
        }

        if (fwrite($handle, $html) === FALSE) {
            $message = "ファイルの書き込みに失敗しました。";
            exit;
        }

        $message = "登録完了しました。";

        fclose($handle);
    } else {
        $message = "作成の権限がありませんでした。";
    }
?>

<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>ヘルプ編集</title>
<link rel="stylesheet" type="text/css" href="../../css/duel.css" media="all">
</head>
<body>
    <?php echo $message ?><br>
    <input type="button" value="戻る" onclick="location='index.php'">
</body>
</html>