<?php 

header('Content-Type: text/html; charset=UTF-8');

class listCard_model{
	private $listCard;
	
	function __construct(){
		$this->init();
	}
	
	function init(){
		$this->listCard = array();
	}
	
	function getListCard(){
		return $this->listCard;
	}
	
	function processing(){
		
		//カードデータを一行ごとに配列に格納
		$lines = file("../../card1.txt");
		$str = file("../../card2.txt");
		
		//一行ごとの処理
		for($i=0;$i<count($lines);$i++){
			
			//タブごとに列分けする
			$row = explode("\t",$lines[$i]);
			
			//能力(文章）を$rowの最後に追加する
			array_push($row, $str[$i]);
			
			//表示用変数に格納する
			$this->listCard[] = $row;
		}
	}
}

?>