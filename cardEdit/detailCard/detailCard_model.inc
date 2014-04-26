<?php 

header('Content-Type: text/html; charset=UTF-8');

class detailCard_model{
	private $num;
	private $lines;	//カード情報(配列)
	private $str;	//かーどのうりょく(文章）(配列)
	
	public function __construct(){
		$this->init();
	}
	
	public function init(){
		$this->num = "";
		$this->lines = array();
		$this->str = "";
	}
	
	public function getNum(){
		return $this->num;
	}
	
	public function getLines(){
		return $this->lines;
	}
	
	public function getStr(){
		return $this->str;
	}
	
	public function getForm(){
		if(isset($_GET['num'])){
			$this->num = $_GET['num'];
		}
	}
	
	public function processing(){
		
		//ファイルの行数を取得
		//$lineNum = sizeof(file("../../card1.txt"));
		//echo $lineNum;
		
		//カードデータを一行ごとに配列に格納
		$lines = file("../../card1.txt");
		$str = file("../../card2.txt");
		//タブごとに列分けする
		$row = explode("\t",$lines[$this->num]);
		$this->lines = $row;
		$this->str = $str[$this->num];
	}
}

?>