<?php
if(empty($_POST['dl_file']) || strlen($_POST['dl_file'])==0){

}else{
	$dfile=$_POST['dl_file'];
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename='.$dfile);
header('Content-Length: '.filesize($dfile));
readfile($dfile);
}
?>
