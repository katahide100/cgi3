<?php
 
header('Content-Type: text/html; charset=UTF-8');

class insertCard_model{
	private $name;
	private $civilization;
	private $kind;
	private $power;
	private $cost;
	private $evolution;
	private $effect;
	private $trigger;
	private $str;
	private $execute;
	private $errMsg;
	private $user;
	
	public function __construct(){
		$this->init();
	}
	
	public function init(){
		$this->name         = "";	//カード名(必須)
		$this->civilization = "";	//文明(必須)
		$this->kind         = "";	//種族(必須)
		$this->power        = "";	//パワー
		$this->cost         = "";	//コスト(必須)
		$this->evolution    = "";	//進化
		$this->effect       = "";	//効果
		$this->trigger      = "";	//トリガー
		$this->str          = "";	//能力（文章）
		$this->execute      = "";	//遷移チェック用
		$this->errMsg       = "";	//エラー表示用
		$this->user			= "";	//使用ユーザー
	}

	function getName(){
		return $this->name;
	}
	
	function getCivilization(){
		return $this->civilization;
	}
	
	function getKind(){
		return $this->kind;
	}
	
	function getPower(){
		return $this->power;
	}
	
	function getCost(){
		return $this->cost;
	}
	
	function getEvolution(){
		return $this->evolution;
	}
	
	function getEffect(){
		return $this->effect;
	}
	
	function getTrigger(){
		return $this->trigger;
	}
	
	function getExecute(){
		return $this->execute;
	}
	
	function getErrMsg(){
		return $this->errMsg;
	}
	
	function getStr(){
		return $this->str;
	}
	
	function getUser(){
		return $this->user;
	}
//===============値取得関数===================

	function getForm(){
		if(isset($_POST['name'])){
			$this->name = $_POST['name'];
		}
		
		if(isset($_POST['civilization'])){
			$this->civilization = $_POST['civilization'];
		}
		
		if(isset($_POST['kind'])){
			$this->kind = $_POST['kind'];
		}
		
		if(isset($_POST['power'])){
			$this->power = $_POST['power'];
		}
		
		if(isset($_POST['cost'])){
			$this->cost = $_POST['cost'];
		}
		
		if(isset($_POST['evolution'])){
			$this->evolution = $_POST['evolution'];
		}
		
		if(isset($_POST['effect'])){
			$this->effect = $_POST['effect'];
		}
		
		if(isset($_POST['trigger'])){
			$this->trigger = $_POST['trigger'];
		}
		
		if(isset($_POST['execute'])){
			$this->execute = $_POST['execute'];
		}
		
		if(isset($_POST['str'])){
			$this->str = $_POST['str'];
		}
		
		if(isset($_POST['user'])){
			$this->user = $_POST['user'];
		}
	}
	
//=============メイン処理関数=================

	function processing(){
			
	//-------登録ボタンからの遷移の場合-------------
		
		if($this->execute == "登録"){
			
			/*----各エラーチェック----*/
			
			if(empty($this->name)){
				$this->errMsg .= "カード名を入力してください。<br>\n";
			}elseif(substr($this->name,0,3) != "★"){
				$this->errMsg .= "カード名は★で囲ってください。<br>\n";
			}
			
			if(strlen($this->civilization) == 0){
				$this->errMsg .= "文明を入力してください。<br>\n";
			}elseif(!preg_match("/^[0-9,]+$/",$this->civilization)){
				$this->errMsg .= "文明は半角数字で入力してください。<br>\n";
			}
			
			if(strlen($this->kind) == 0){
				$this->errMsg .= "種族を入力してください。<br>\n";
			}elseif(!preg_match("/^[0-9,]+$/",$this->kind)){
				$this->errMsg .= "種族は半角数字で入力してください。<br>\n";
			}
			
			if(strlen($this->power)){
				if(!preg_match("/^[0-9+]+$/",$this->power)){
					$this->errMsg .= "パワーは半角数字で入力してください。<br>\n";
				}
			}
			
			if(strlen($this->cost) == 0){
				$this->errMsg .= "コストを入力してください。<br>\n";
			}elseif(!preg_match("/^[0-9]+$/",$this->cost)){
				$this->errMsg .= "コストは半角数字で入力してください。<br>\n";
			}
			
			if(strlen($this->evolution)){
				if(!preg_match("/^[0-9,]+$/",$this->evolution)){
					$this->errMsg .= "進化は半角数字で入力してください。<br>\n";
				}
			}
			
			if(strlen($this->effect)){
				if(!preg_match("/^[0-9,]+$/",$this->effect)){
					$this->errMsg .= "効果は半角数字で入力してください。<br>\n";
				}
			}
			
			if(strlen($this->trigger)){
				if(!preg_match("/^[0-9,]+$/",$this->trigger)){
					$this->errMsg .= "トリガーは半角数字で入力してください。<br>\n";
				}
			}
			
			//オリジナルでは必要ない
			//if(empty($this->str)){
			//	$this->str = "\n";
			//}
			
			if(empty($this->user)){
				$this->errMsg .= "使用ユーザーを入力してください。<br>\n";
			}
			
			
			//エラーがなかった場合
			$result = "";
			if($this->errMsg == ""){
				if($this->user == "全員"){
					$cgiMsg = "★cgi専用カード<br/>";
				}else{
					$cgiMsg = "★cgi個人専用カード－このカードはユーザー【{$this->user}】しか使う事が出来ない。<br/>";
				}
				$this->str = $cgiMsg.$this->str;
				$result .= "\n".$this->name."	";
				$result .= $this->civilization."	";
				$result .= $this->kind."	";
				$result .= $this->power."	";
				$result .= $this->cost."	";
				$result .= $this->evolution."	";
				$result .= $this->effect."	";
				$result .= $this->trigger;
				
				//card1への書き込み処理
				$fp = fopen("../../card1.txt","a") or die("カードリストが開けませんでした。");
				fwrite($fp,$result);
				fclose($fp);
				
				//card2への書き込み処理
				$fp = fopen("../../card2.txt","a") or die("カードリスト（能力）が開けませんでした。");
				fwrite($fp,"\n".$this->str);
				fclose($fp);
					
				$this->execute = "success";
			}
		}
	}
}


?>