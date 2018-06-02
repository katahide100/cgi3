<?php
    require_once '../admin.php';

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // ユーザー検索
        if ($_POST["type"] == 'search'){
            
            $id = $_POST["user_id"];
            $curl = curl_init();
            $return = [];
            $error = '';

            curl_setopt($curl, CURLOPT_URL, NODE_SERVER_URL.'/user/find?user_id=' . $id);
            curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'GET');
            curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); // 証明書の検証を行わない
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);  // curl_execの結果を文字列で返す

            $response = curl_exec($curl);
            $result = json_decode($response, true);

            curl_close($curl);

            if(count($result) < 1) {
                $error = 'ユーザー情報が取得できませんでした。';
            }

            if (!empty($error)) {
                $return = ['error' => $error];
            } else {
                $return = $result[0];
            }
            header('Content-Type: application/json; charset=utf-8');
            echo json_encode($return, JSON_UNESCAPED_UNICODE);
            exit;
        }

        // ユーザー更新
        if ($_POST["type"] == 'update'){
            
            $recId = $_POST["record_id"];
            $orica = $_POST["orica"];
            $curl = curl_init();
            $return = [];
            $error = '';
            $data = [
                'orica' => $orica
            ];

            curl_setopt($curl, CURLOPT_URL, NODE_SERVER_URL . '/user/update/' . $recId);
            curl_setopt($curl,CURLOPT_POST, TRUE);
            curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
            curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); // 証明書の検証を行わない
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);  // curl_execの結果を文字列で返す

            $response = curl_exec($curl);
            $result = json_decode($response, true);

            curl_close($curl);

            if($result['status'] !== null && $result['details'] !== null) {
                $error = $result['details'];
            }
            
            if (!empty($error)) {
                $return = ['error' => $error];
            } else {
                $return = $result;
            }
            header('Content-Type: application/json; charset=utf-8');
            echo json_encode($return, JSON_UNESCAPED_UNICODE);
            exit;
        }
    }
?>

<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>ユーザー編集</title>
<link rel="stylesheet" type="text/css" href="<?=CURRENT_HOST ?>/css/duel.css" media="all">
<script type="text/javascript" src="<?=CURRENT_HOST ?>/js/jquery-1.11.2.min.js"></script>


<script type="text/javascript">
    $(function(){
        $('#update_btn').hide();

        // Ajax button click
        $('#user_id').on('change',function(){
            $('#msg').html("");
            $.ajax({
                url:'',
                type:'POST',
                data:{
                    'type':'search',
                    'user_id':$('#user_id').val(),
                }
            })
            // Ajaxリクエストが成功した時発動
            .done( (data) => {
                if (data.error !== undefined && data.error != '') {
                    $('#msg').html(data.error + "<br>");
                    $('#update_btn').hide();
                } else {
                    var orica = 0;
                    if (data.orica > 0) {
                        orica = data.orica;
                    }
                    $('#orica').val(orica);
                    $('#record_id').val(data.id);
                    $('#update_btn').show();
                }
            })
            // Ajaxリクエストが失敗した時発動
            .fail( (data) => {
                $('#msg').html("通信エラー<br>");
                $('#update_btn').hide();
            });
        });

        // Ajax button click
        $('#update_btn').on('click',function(){
            $('#msg').html("");
            $.ajax({
                url:'',
                type:'POST',
                data:{
                    'type':'update',
                    'record_id':$('#record_id').val(),
                    'orica':$('#orica').val(),
                }
            })
            // Ajaxリクエストが成功した時発動
            .done( (data) => {
                
                if (data.error !== undefined && data.error != '') {
                    $('#msg').html(data.error + "<br>");
                } else {
                    $('#msg').html("登録が成功しました。<br>");
                }
            })
            // Ajaxリクエストが失敗した時発動
            .fail( (data) => {
                $('#msg').html("通信エラー<br>");
            });
        });
    });

</script>

</head>
<body align="center">
    <h1>ユーザー編集画面</h1>
    <br>
    <br>
<form action="" method="POST">
    ユーザーID：<input type="text" name="user_id" id="user_id" value=""><br><br>
    オリカ券：<input type="text" name="orica" id="orica" value=""><br><br>
    <input type="hidden" name="record_id" id="record_id" value="">
    <font color="red" id="msg"></font>
    <input type="button" id="update_btn" value="登録"><br><br>
</form>
</body>
</html>