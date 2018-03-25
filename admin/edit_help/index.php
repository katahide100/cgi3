<?php
    $file = file_get_contents("../../tmp/help/contents.txt");
?>

<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>ヘルプ編集</title>
<link rel="stylesheet" type="text/css" href="../../css/duel.css" media="all">
</head>
<body align="center">
    <h1>ヘルプ編集画面</h1>
    <br>
    <br>
<form action="complete.php" method="POST">
    <input type="submit" value="登録"><br><br>

<textarea name="contents" class="ckeditor"><?php echo $file; ?></textarea>

</form>
<script src="../../ckeditor/ckeditor.js"></script>
</body>
</html>