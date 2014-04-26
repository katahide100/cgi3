<?php 

header('Content-Type: text/html; charset=UTF-8');

class deleteCard_model{
	private $num;
	private $execute;
	
	public function __construct(){
		$this->init();
	}
	
	public function init(){
		$this->num = "";
		$this->execute = "";
	}
	
	public function getNum(){
		return $this->num;
	}
	
	public function getExecute(){
		return $this->execute;
	}
	
	public function getForm(){
		if(isset($_GET['num'])){
			$this->num = $_GET['num'];
		}
		
		if(isset($_GET['execute'])){
			$this->execute = $_GET['execute'];
		}
	}
		
	public function processing(){
		if($this->execute == "削除"){

			//カードデータを一行ごとに配列に格納
			$lines = file("../../card1.txt");
			$str = file("../../card2.txt");
			
			$lines[$this->num] = "\n";
			$str[$this->num] = "\n";
			
			//カードデータの書き換え
			$fp = fopen("../../card1.txt","w");
			foreach($lines as $key => $val){
				fwrite($fp,$lines[$key]);
			}
			fclose($fp);
			
			$fp = fopen("../../card2.txt","w");
			foreach($str as $key => $val){
				fwrite($fp,$str[$key]);
			}
			fclose($fp);
		}
	}
}

?>