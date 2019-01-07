#!/usr/local/bin/perl
BEGIN{open STDERR, '>./logs/error.log'};

require "cust.cgi";
require "action.pl";
require "duel.pl";
require "common.pl";

&decode;
&decode2 if $F{'mode'} ne "cardview";
&cardread if $F{'mode'} =~ /tourjoin|duel|cardview/;
&syu_read if $F{'mode'} !~ /form|regist|all/;
&cardread2 if $F{'mode'} !~ /form|regist|all|tourjoin|duel|cardview/;

$room = 't' if($F{'mode'} eq 'tourjoin' || $F{'mode'} eq "tourcancel");

@pfldata	= qw (dendou phase turn turn2 chudan chudan_flg end_flg trigger_flg skip_flg boru_cnt vor_cnt message dgroup duelid choose white black multi roomid start_date nid1 nnm1 nid2 nnm2 reverse_flg);
@pfldata2	= qw (lp side pn pass dnam usedeck date sur_flg drank ip janken tourtime);
@pflst		= qw (fld f_tap f_block f_drunk f_cloth shinka res syori btl vor syu_add shield magic res2);
@pflst2		= qw (deck hand boti gear psychic);
@phasestr	= qw (ターン開始フェイズ ドローフェイズ マナチャージフェイズ メインフェイズ アタックフェイズ);

@{$fw1[1]} = (280..319); @{$fw2[1]} = (240..279); @{$fw3[1]} = (200..239); @{$fw4[1]} = (160..199);
@{$fw1[2]} = (120..159); @{$fw2[2]} =  (80..119); @{$fw3[2]} =   (40..79); @{$fw4[2]} =    (0..39);

if ($F{'mode'} ne "cardview") {
	&filelock($room);
	if($F{'mode'} eq "duel" && !($end_flg)){ &start; } else { &get_ini; }
	if((($F{'mode'} eq "tourjoin") || ($F{'mode'} eq "tourcancel")) && !($end_flg)) { &start; }
	&error("IDまたはパスワードが間違っています。入力し直してください。") if ($id eq $side[1] || $id eq $side[2]) && (($pass ne "" && (crypt($pass, $pass) ne $pass[1]) && (crypt($pass, $pass) ne $pass[2]) && ($pass ne $admin)));

	if($side[1] eq $side[2]) {
		$u_side	= $turn2;
	} else {
		$u_side	= $side[2] eq $id && $side[2] ? 2 : 1;
	}
	$u_side = (($u_side - 1) xor $reverse_flg) + 1;
	$read_only = 1 if $side[1] ne $id && $side[2] ne $id;
	$u_side2 = 3 - $u_side;

	&pfl_read($id) if (-e $player_dir."/".$id.".cgi" && $read_only);
}

&frame				if !($F{'mode'}) || $F{'mode'} =~ /audience|duel/;
&form				if $F{'mode'} eq "form";
&sousa				if $F{'mode'} eq "sousa";
&ad                             if $F{'mode'} eq "ad";
&regist($pn[$u_side],$F{'mess'},"message$u_side")
					if $F{'mode'} eq "regist" && !($read_only);
&regist($P{'name'},$F{'mess'},"admin")
					if $F{'mode'} eq "regist" && $read_only && (($P{'admin'} > 0) || ($P{'subadmin'} > 0));
&access_chk();

&drop				if $F{'mode'} eq "drop";
&surrender			if $F{'mode'} eq "surrender" && !($end_flg);
#&restart			if $F{'mode'} eq "restart" && $end_flg;
&rcom				if $F{'mode'} eq "rcom";
&cardview			if $F{'mode'} eq "cardview";
&all				if $F{'mode'} eq "all";
unless($chudan_flg){
	&draw			if $F{'mode'} eq "draw";
	&shuffle1		if $F{'mode'} eq "shuffle";
	&battle			if $F{'mode'} eq "battle";
	&change_phase	if $F{'mode'} eq "phase";
	&tap			if $F{'mode'} eq "tap";
	&rand_tehuda	if $F{'mode'} eq "rand_tehuda";
	&mekuru			if $F{'mode'} eq "mekuru";
	&move			if $F{'mode'} eq "move";
	&break_btn		if $F{'mode'} eq "break";
	&cloth			if $F{'mode'} eq "cloth";
	&janken			if $F{'mode'} eq "janken";
	&gacha			if $F{'mode'} eq "gacha";
	&psychic			if $F{'mode'} eq "psychic";
	&psy_link			if $F{'mode'} eq "psy_link";
}
&block_flg			if $F{'mode'} eq "block_flg";
&shinka_sel			if $F{'mode'} eq "shinka_sel";
&b_shinka_sel		if $F{'mode'} eq "b_shinka_sel";
&c_shinka_sel		if $F{'mode'} eq "c_shinka_sel";
&add_up_card_sel	if $F{'mode'} eq "add_up_card_sel";
&vor_sel1			if $F{'mode'} eq "vor_sel";
&vor_sel2			if $F{'mode'} eq "vor_sel2";
&vor_sel1			if $F{'mode'} eq "b_vor_sel";
&vor_sel2			if $F{'mode'} eq "b_vor_sel2";
&glink_sel			if $F{'mode'} eq "glink_sel";
&glink_sel2			if $F{'mode'} eq "glink_sel2";
&return_sel			if $F{'mode'} eq "return_sel";
&battle_cre_chk		if $F{'mode'} eq "battle_cre_chk";
&taisyo_sel			if $F{'mode'} eq "taisyo_sel";
&attacked_cre_sel	if $F{'mode'} eq "attacked_cre_sel";
&block_sel			if $F{'mode'} eq "block_sel";
&block_trigger_end	if $F{'mode'} eq "block_trigger_end";
&battle_run			if $F{'mode'} eq "battle_sel";
&trap_sel			if $F{'mode'} eq "trap_sel";
&meji_sel			if $F{'mode'} eq "meji_sel";
&trigger_sel1		if $F{'mode'} eq "trigger_sel1";
&trigger_sel2		if $F{'mode'} eq "trigger_sel3";
&strike_sel			if $F{'mode'} eq "strike_sel1";
&strike_end			if $F{'mode'} eq "strike_end";
&arcadia_sel		if $F{'mode'} eq "arcadia_sel";
&runba_sel			if $F{'mode'} eq "runba_sel";
&ninja_sel			if $F{'mode'} eq "ninja_sel";
&ninja_end			if $F{'mode'} eq "ninja_end";
&mekuru_sel1		if $F{'mode'} eq "mekuru_sel1";
&mekuru_sel2		if $F{'mode'} =~ /mekuru_sel[23]/;
&mekuru_sel4		if $F{'mode'} =~ /mekuru_sel[45]/;
&mekuru_sel6		if $F{'mode'} eq "mekuru_sel6";
&mekuru_move1		if $F{'mode'} eq "mekuru_move1";
&mekuru_move2		if $F{'mode'} eq "mekuru_move2";
&changer_sel1		if $F{'mode'} eq "changer_sel1";
&changer_sel2		if $F{'mode'} eq "changer_sel2";
&meteo_sel			if $F{'mode'} eq "meteo_sel";
&meteo_end			if $F{'mode'} eq "meteo_end";
&dynamo_sel			if $F{'mode'} eq "dynamo_sel";
&cloth_sel1			if $F{'mode'} eq "cloth_sel";
&cloth_sel2			if $F{'mode'} eq "cloth_sel2";
&bikkuri_sel		if $F{'mode'} eq "bikkuri_sel";
&flip_sel			if $F{'mode'} eq "flip_sel";
&silent_sel			if $F{'mode'} eq "silent_sel";
&silent_sel2		if $F{'mode'} eq "silent_sel2";
&janken_sel			if $F{'mode'} eq "janken_sel";
&lemon_sel			if $F{'mode'} eq "lemon_sel";
&sforth_sel			if $F{'mode'} eq "sforth_sel";
&castle_sel			if $F{'mode'} eq "castle_sel";
&castle_trap		if $F{'mode'} eq "castle_trap";
&castle_trap_sel	if $F{'mode'} eq "castle_trap_sel";
&sel_end			if $F{'mode'} =~ /attack_trigger_end|block_sel2|meji_end|trigger_sel2|doru_end|arcadia_end|danrimos_end|last_attack|universe_attack/;
&block_chk			if $F{'mode'} eq "attacked_sel";
&taisyo_chk			if $F{'mode'} eq "blocked_sel";
&gabriela_sel		if $F{'mode'} eq "gabriela_sel";
&field				if $F{'mode'} eq "field";
&cardlist			if $F{'mode'} eq "cardlist" && $side[1] && $side[2] && !($end_flg) && !($read_only);
&mess				if $F{'mode'} eq "mess";

&act_cancel	if $F{'mode'} eq "cancel";
&drop_admit	if $F{'mode'} eq "dropadmit";
&drop_admit2	if $F{'mode'} eq "dropadmit2" && $read_only && (($P{'admin'} > 0) || ($P{'subadmin'} > 0));
&nuisance	if $F{'mode'} eq "nuisance";

&kakunin		if $F{'mode'} eq "kakunin";
&kakunin_sel		if $F{'mode'} eq "kakunin_sel";

&room_msg	if $F{'mode'} eq "roommsg";
&tourstart	if $F{'mode'} eq "tourstart";
&tourreset	if $F{'mode'} eq "tourreset";

if(!($F{'mode'}) || $F{'mode'} ne "regist"){ &field; } else { &all; }

&fileunlock($room);

sub ad {
  &header;
  print <<"EOM";
<script>
setTimeout("location.reload()",180000);
</script>
</head>
<body>
<div style="width: 160px; font-size: 11px; color: blue;background-color: #c2d3e1">運営継続のため     
、たまにクリックして頂けると幸いです。</div>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 広告ユニット1 -->
<ins class="adsbygoogle"
     style="display:inline-block;width:160px;height:600px"
     data-ad-client="ca-pub-1974859203649104"
     data-ad-slot="1784652942"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</body></html>
EOM
&fileunlock($room);
exit;
}

sub sousa {
	&header;
	my $vside = (($u_side - 1) xor $F{'vside'}) + 1;
	my $varea = $F{'varea'} ? $F{'varea'} : 0;
	$selstr[$vside] = $selstr2[$varea] = " selected";
	for my $i(1..2){
		$deckno[$i] = @{$deck[$i]};
		$handno[$i] = @{$hand[$i]};
		$botino[$i] = @{$boti[$i]};
		$psychicno[$i] = @{$psychic[$i]};
	}
	my($sec,$min,$hour,$mday,$mon,$year) = localtime($date[$u_side]);
	my $dat1 = sprintf("%02d:%02d",$hour,$min);
	my($vsec,$vmin,$vhour,$vmday,$vmon,$vyear) = localtime($date[$u_side2]);
	my $dat2 = sprintf("%02d:%02d",$vhour,$vmin);
#	my $pstr = $phase =~ /3|4/ ? " selected" : "";
	my $pstr = " selected";
	my $random = crypt(int(rand(100000000)), int(rand(100)));
	unless($read_only){
		print <<"EOM";
<script type="text/javascript">
<!--
	with(document);
	function Tap(){
		parent.field.fields.mode.value = "tap";
		\$.post("duelold.cgi", \$(parent.field.fields).serialize(), function(data){
			window.parent.s.emit("action", {mode:"tap",room:"$room"});
        });
	}
	function Cmd(f){
		parent.field.fields.mode.value = f;
		\$.post("duelold.cgi", \$(parent.field.fields).serialize(), function(data){
			window.parent.s.emit("action", {mode:f,room:"$room"});
        });
	}
	function sForm(f) {
		card.mode.value = f;
		card.target = (f == "sousa") ? "_self" : "field";
		\$.post("duelold.cgi", \$("[name=card]").serialize(), function(data){
			window.parent.s.emit("action", {mode:f,room:"$room"});
        });
	}
	function Move(parea){
		str = 'duelold.cgi?room=$room&id=$id&pass=$pass&load=$load&log=$log&mode=move&vside=$F{'vside'}&varea=$varea&parea=' + parea + '&random=$random';
		str += (card.decktop.checked) ? "&decktop=on" : "&decktop=";
		str += (card.show.checked) ? "&show=on" : "&show=";
		str += "&under=" + card.under[card.under.selectedIndex].value;
		for(i=0;i<card.elements.length;i++){
			if(card.elements["sel"+ i] && card.elements["sel"+ i].checked){ str += "&sel" + i + "=on"; }
		}
		var F = parent.field.fields;
		for(i=0;i<F.elements.length;i++){
			if (F.elements[i].checked && F.elements[i].name.match(/^.?sel/)){ str += "&" + F.elements[i].name + "=on"; }
		}
		\$.post(str, \$("[name=card]").serialize(), function(data){
			window.parent.s.emit("action", {mode:'move',room:"$room"});
        });

	}
	(function() {
    	// form が submit されたとき(攻撃、ブレイク時の処理などで使用)
	    var form = \$(parent.field.fields);
	    form.on('click', 'input[type=submit]', function(event) {
	    	// submit処理をキャンセル
	    	event.preventDefault();

	    	// postデータにsubmitタグのnameとvalueを追加する
	    	var postData = \$(parent.field.fields).serialize() + '&' + \$(this).attr('name') + '=' + \$(this).val();
		    \$.post("duelold.cgi", postData, function(data){
				window.parent.s.emit("action", {mode:parent.field.fields.mode.value,room:"$room"});
	        });
	        // 自動で submit されないように処理を止める
	        return false;
	    });
	})();

// -->
</script>
EOM
	}
my($side1_mark) = $sur_flg[$u_side] == 1 ? " <font title=\"退室許可証\">☆</font>" : "";
my($side2_mark) = $sur_flg[$u_side2] == 1 ? " <font title=\"退室許可証\">☆</font>" : "";
	print <<"EOM";
</head>
<body>
<table width="180" cellpadding="5" cellspacing="0" border="1" align="center" class="table">
<tr><td>
ターン：$turn<br>
<!--$pn[$turn2]の$phasestr[$phase]<br>-->
【山札】$pn[$u_side]：$deckno[$u_side]／$pn[$u_side2]：$deckno[$u_side2]<br>
EOM
if (&c_chk("ラグーン・マーメイド",3)) {
	print qq|【山札の１枚目】<br>\n|;
	print qq|$pn[$u_side]：$c_name[$deck[$u_side][0]]<br>\n|;
	print qq|$pn[$u_side2]：$c_name[$deck[$u_side2][0]]<br>\n|;
}
	print <<"EOM";
【手札】$pn[$u_side]：$handno[$u_side]／$pn[$u_side2]：$handno[$u_side2]<br>
【墓地】$pn[$u_side]：$botino[$u_side]／$pn[$u_side2]：$botino[$u_side2]<br>
【次元】$pn[$u_side]：$psychicno[$u_side]／$pn[$u_side2]：$psychicno[$u_side2]<br>
【最終アクセス】<br>
$pn[$u_side]\[$side[$u_side]\]：$dat1$side1_mark<br>
$pn[$u_side2]\[$side[$u_side2]\]：$dat2$side2_mark
</td></tr>
EOM
	if($read_only || $end_flg || !($side[1]) || !($side[2])){
		if(($P{'admin'} > 0) || ($P{'subadmin'} > 0)) {
			print <<"EOM";
<tr><td><form action="duelold.cgi" method="post" name="admin" target="field" style="display:inline;">
	<input type="hidden" name="room" value="$room">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="dropadmit2">
<select name="tp">
<option value="$u_side" selected>$pn[$u_side]</option>
<option value="$u_side2">$pn[$u_side2]</option>
</select> に <input type="submit" value="退室許可" onClick="if(confirm('本当に退室許可を出しますか？')) { this.disabled = true; document.admin.submit(); } else { return false; }">
</form>
</tr>
EOM
		}
		$kansen = $kansen[int(rand($#kansen))];
		print qq|<tr><td><img src="$image/$kansen" width="180" alt="観戦中"></td>|;
	} else {
#		my $bstr = $phase == 4 && $u_side == $turn2 ? "ターン終了" : "次のフェイズへ";
#		my $bstri = $phase == 4 && $u_side == $turn2 ? "ターンを終了" : "次のフェイズへ移行";
		my $bstr = "ターンの終了";
		my $bstri = "ターンを終了";
		print <<"EOM";
<form action="duelold.cgi" method="post" name="card">
	<input type="hidden" name="room" value="$room">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="load" value="$load">
	<input type="hidden" name="log" value="$log">
EOM
	if($side[1] eq $side[2]) {
		print <<"EOM";
<tr><td align="center">
	<input type="button" value="操作権限の入れ替え" onclick="if(confirm('操作権限を入れ替えますか？\\n\\nこのコマンドは一人対戦用です。\\n実行すると、相手の画面を操作するようになります。')) { this.disabled = true; sForm('rcom'); } return false;">
</td></tr>
EOM
	}
		print <<"EOM";
<tr><td align="center">
	<input type="button" value="ドロー" onclick="if(confirm('本当にドローしますか？')) { this.disabled = true; sForm('draw'); } return false;">
	<input type="button" value="シャッフル" onclick="if(confirm('本当にシャッフルしますか？')) { this.disabled = true; sForm('shuffle'); } return false;">
</td></tr>
<tr><td align="center">
	<input type="button" value="$bstr" onclick="if(confirm('本当に$bstriしますか？')) { this.disabled = true; sForm('phase'); } return false;">
</td></tr>
<tr><td align="center">
	<table border="0">
		<tr align="center"><td>
			<input type="button" value="クリーチャーで攻撃" onclick="if(confirm('本当にクリーチャーで攻撃しますか？\\nこの行動は、クリーチャーへの攻撃だけでなく、\\n相手プレイヤーのシールドをブレイクするのにも使います。')) { this.disabled = true; sForm('battle'); } return false;"><br>
			&nbsp;<label><input type="checkbox" name="rush" value="on" class="none">ターボラッシュ</label>
		</td></tr>
		<tr align="center"><td>
			<input type="button" value="特殊能力でシールド破壊" onclick="if(confirm('本当に特殊能力でシールドを破壊しますか？\\nこの行動は、サイレントスキルなどの\\nバトル以外でのシールドブレイクでのみ、使います。')) { this.disabled = true; sForm('break'); } return false;">
		</td></tr>
		<tr align="center"><td>
			<input type="button" value="行動をキャンセル" onclick="if(confirm('本当に行動をキャンセルしますか？\\nこの行動は、基本的にバグで何も出来なくなった状態からの\\n脱出に使われます。\\nバグる恐れがあるため、「やめる」ボタンが出ている場合は、\\nそちらでキャンセル処理をするようお願い致します。')) { this.disabled = true; sForm('cancel'); } return false;">
		</td></tr>
	</table>
</td></tr>
<tr><td align="center">
	<input type="button" value="タップ／アンタップ" onclick="if(confirm('本当にタップ／アンタップしますか？\\nこの行動は、バトルゾーンにあるクリーチャーだけでなく、\\nマナゾーンにあるカードをタップ／アンタップする場合にも使います。')) { this.disabled = true; Tap(); } return false;">
</td></tr>
<tr><td align="center">
	<input type="button" value="相手の手札を見ずに捨てる" onclick="if(confirm('本当に相手の手札を見ずに捨てますか？')) { this.disabled = true; sForm('rand_tehuda'); } return false;">
</td></tr>
<tr><td align="center">
	<select name="marea">
		<option value="0">シールドを</option>
		<option value="1">山札を１枚ずつ</option>
		<option value="2">枚数を指定して</option>
		<option value="3">相手の山札の上を</option>
	</select>
	<input type="button" value="めくる" onclick="if(confirm('本当にめくりますか？')) { this.disabled = true; sForm('mekuru'); } return false;"><br>
	<label><input type="checkbox" name="impulse" value="on" class="none">めくった後、山札に戻す</label><br>
	<label><input type="checkbox" name="secret" value="on" class="none">自分だけが見る</label>
</td></tr>
<tr><td align="center">
	<input type="button" value="クロス" onclick="if(confirm('本当にクロスしますか？')) { this.disabled = true; sForm('cloth'); } return false;">
</td></tr>
<tr><td align="center">
	<input type="button" value="覚醒／解除" onclick="if(confirm('本当に覚醒／解除しますか？')) { this.disabled = true; Cmd('psychic'); } return false;">
</td></tr>
<tr><td align="center">
	<input type="button" value="覚醒リンク" onclick="if(confirm('本当に覚醒リンクしますか？')) { this.disabled = true; Cmd('psy_link'); } return false;">
</td></tr>
<tr><td align="center">
	<input type="button" value="ジャンケン" onclick="if(confirm('本当にジャンケンしますか？')) { this.disabled = true; sForm('janken'); } return false;">
</td></tr>
<tr><td align="center">
<input type="button" value="ガチャを回す" onclick="if(confirm('本当にガチャを回しますか？')) { this.disabled = true; sForm('gacha'); } return false;">
</td></tr>
EOM
		if($room =~ /^t/) {
			print <<"EOM";
<tr><td align="center">
	<input type="button" value="相手に確認を取る" onclick="if(confirm('本当に相手に確認を取りますか？')) { this.disabled = true; sForm('kakunin'); } return false;">
</td></tr>
EOM
		}
		print <<"EOM";
<tr><td align="center">
	<label><input type="checkbox" name="decktop" value="on" class="none">山札の</label><select name="under"><option value="0" selected>一番上</option><option value="1">一番下</option></select>のカードを<br>
	<label><input type="checkbox" name="show" value="on" class="none">相手に見せないで</label><br>
	<select name="parea">
		<option value="0">マナゾーンへ</option>
		<option value="1"$pstr>バトルゾーンへ</option>
		<option value="2">墓地へ</option>
		<option value="3">手札へ</option>
		<option value="4">山札の上へ</option>
		<option value="5">山札の下へ</option>
		<option value="6">シールドへ</option>
		<option value="7">進化獣の下へ</option>
		<option value="8">カードの下へ</option>
		<option value="9">超次元ゾーンへ</option>
		<option value="10">強制的にクリーチャーの上へ</option>
	</select>
	<input type="button" value="移動" onclick="if(confirm('本当にカードを移動しますか？')) { this.disabled = true; Move(document.card.parea.value); } return false;">
</td></tr>
<tr><td align="center">
	カードの移動(内容は上と同じです)<br>
	<input type="button" value="マナへ" onclick="if(confirm('本当にマナゾーンへカードを移動しますか？')) { this.disabled = true; Move('0'); } return false;">
	<input type="button" value="バトルゾーンへ" onclick="if(confirm('本当にバトルゾーンへ移動しますか？')) { this.disabled = true; Move('1'); } return false;"><br>
	<input type="button" value="手札へ" onclick="if(confirm('本当に手札へ移動しますか？')) { this.disabled = true; Move('3'); } return false;">
	<input type="button" value="墓地へ" onclick="if(confirm('本当に墓地へ移動しますか？')) { this.disabled = true; Move('2'); } return false;">
	<input type="button" value="シールドへ" onclick="if(confirm('本当にシールドへ移動しますか？')) { this.disabled = true; Move('6'); } return false;"><br>
	<input type="button" value="山札の上へ" onclick="if(confirm('本当に山札の上へ移動しますか？')) { this.disabled = true; Move('4'); } return false;">
	<input type="button" value="山札の下へ" onclick="if(confirm('本当に山札の下へ移動しますか？')) { this.disabled = true; Move('5'); } return false;">
	<input type="button" value="進化獣の下へ" onclick="if(confirm('本当に進化獣の下へ移動しますか？')) { this.disabled = true; Move('7'); } return false;"><br>
	<input type="button" value="カードの下へ" onclick="if(confirm('本当にカードの下へ移動しますか？')) { this.disabled = true; Move('8'); } return false;">
	<input type="button" value="超次元ゾーンへ" onclick="if(confirm('本当に超次元ゾーンへ移動しますか？')) { this.disabled = true; Move('9'); } return false;">
	<input type="button" value="強制的にクリーチャーの上へ" onclick="if(confirm('本当にクリーチャーの上へ移動しますか？\\nシステム的に対応していない場合のみこのボタンを使用してください。\\n（通常の進化などはバトルゾーンへボタンをご利用ください。）')) { this.disabled = true; Move('10'); } return false;"><br>
</td></tr>
<tr><td>
	<p align="center">
	<select name="vside" onchange="if(!confirm('本当に手札表示を切り替えますか？')) return false;">
	<option value="0"$selstr[$u_side]>自分</option>
	<option value="1"$selstr[$u_side2]>相手</option>
	</select>
	<select name="varea" onchange="if(!confirm('本当に手札表示を切り替えますか？')) return false;">
	<option value="0"$selstr2[0]>手札</option>
	<option value="1"$selstr2[1]>墓地</option>
EOM
		print qq|<option value="2"$selstr2[2]>山札</option>\n| unless &c_chk("巡霊者メスタポ",3);
		print qq|<option value="3"$selstr2[3]>次元</option>\n|;
		print qq|</select>\n|;
		print qq|<input type="button" value="切替" onclick="sForm('sousa'); return false;">\n|;
		print qq|</p>\n|;
		&regist("","$pn[$u_side]は相手の手札を見た！") if $varea == 0 && $vside eq $u_side2;
		&regist("",sprintf "$pn[$u_side]は%sの山札を見た！", $vside == $u_side2 ? "相手" : "自分") if $varea == 2;
		&del_null(sprintf(%s,$varea == 0 ? *hand : $varea == 1 ? *boti : $varea == 2 ? *deck : *psychic),$vside);
		my @tmp = $varea == 0 ? @{$hand[$vside]} : $varea == 1 ? @{$boti[$vside]} : $varea == 2 ? @{$deck[$vside]} : @{$psychic[$vside]};
		printf "%s$pn[$vside]の%s%s\n",$#tmp < 0 ? "" : "<strong>", $varea == 0 ? "手札": $varea == 1 ? "墓地": $varea == 2 ? "山札" : "超次元ゾーン", $#tmp < 0 ? "は０です":"</strong>";
		if(0 <= $#tmp){
			my $cou = 0;
			foreach my $cno(@tmp){
				my $bun = (&bun_sub($cno))[0];
				print  qq| <br><input type="checkbox" name="sel$cou" value="$cno" class="none">\n|;
				printf qq| $bun　<a href="javascript:parent.cView($cno);">$c_name[$cno]</a>/$c_mana[$cno]%s\n|, $c_evo[$cno] =~ /1|2|3/ ? "/進化" : $c_evo[$cno] =~ /5|6|7/ ? "/進化Ｖ" : $c_evo[$cno] == 4 ? "/進化GV" : "";
				$cou++;
			}
		}
		print "</td>";
	}
	print qq|</tr>\n|;
	print qq|</form>\n| unless $read_only || $end_flg || !($side[1]) || !($side[2]);
	print qq|</table>\n|;
	print qq|</body>\n</html>\n|;
	&fileunlock($room);
	exit;
}

sub end_game{
	&end_game_sub;
}

sub drop {
	if(!($read_only) && ($room !~ /^t/)){
		my $name = $pn[$u_side];
		&regist("","$nameさんが退室しました。(IP: $ENV{'REMOTE_ADDR'})", "system");
		$sur_flg[$u_side2] = 0;
		if((!($side[1]) || !($side[2])) || ($side[1] eq $side[2])){
			unlink("room/".$roomst.$room.".cgi");
			unlink("room/".$roomst.$room."_log.cgi","room/".$roomst.$room."_card.cgi");
		} else {
			if(!($sur_flg[$u_side]) && !($end_flg)) {
				&regist("","退室許可が出ていないので、$nameは負けになります。", "system");
				$lp[$u_side] = 0;
				$lp[$u_side2] = 1;
				$sr[$u_side] = 1;
				$sr[$u_side2] = 0;
				&end_game;
			}
			&all_clr($u_side);
			&deck_reload($u_side2);
		}
	}
	&thanks;
}

sub surrender {
	&regist("","$pn[$u_side]さんが投了しました。", "system");
	$lp[$u_side] = 0;
	$sr[$u_side] = 1;
	$sr[$u_side2] = 0;
	&end_game;
	&form;
}

sub thanks{
	&fileunlock($room);
	&header;
	print <<"EOM";
</head>
<body>
<div align="center">
<h3>ご利用ありがとうございました</h3>
<form name="send" action="taisen.cgi" method="POST" target="_top">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="pass" value="$pass">
EOM
	if($room =~ /^t/) {
		print "<input type=\"hidden\" name=\"mode\" value=\"tour\">\n";
	} else {
		print "<input type=\"hidden\" name=\"mode\" value=\"\">\n";
	}
print <<"EOM";
[<a href="javascript:document.send.submit();">戻る</a>]</p>
</form>
EOM
	&fileunlock($room);
	&footer;
}

sub deck_reload {
	my $sd = $_[0];
	&pfl_read($side[$sd]);
	my $use = $usedeck[$sd];
	($dnam,$dcon) = split(/-/,$P{"deck$use"});
	@{$deck[$sd]} = split(/,/,$dcon);
	&put_ini;
}

sub frame {
	&fileunlock($room);
	&header;
	print <<"EOM";
<script src="$hostName:$nodePort/socket.io/socket.io.js"></script>
<script type="text/javascript"><!--
var s = io.connect('$hostName:$nodePort');
   s.on("action", function (data) {
           if (data.room == "$room") {
                   parent.sousa.card.mode.value = 'field';
                   parent.sousa.card.target = "field";
                   parent.sousa.card.submit();
           }
});
with(document);
function cView(c){
	vWin = window.open("duelold.cgi?mode=cardview&j=" + c,"view","width=720,height=300,resizable=yes,scrollbars=yes");
}
// --></script>
</head>
<frameset cols="220,*,180">
<frameset rows="*,200">
<frame src="duelold.cgi?mode=sousa&id=$id&pass=$pass&room=$room" name="sousa">
<frame src="duelold.cgi?mode=all&id=$id&pass=$pass&room=$room" name="message">
</frameset>
<frameset rows="100,*">
<frame src="duelold.cgi?mode=form&id=$id&pass=$pass&room=$room" name="form">
<frame src="duelold.cgi?mode=field&id=$id&pass=$pass&room=$room" name="field">
</frameset>
<frameset rows="*">
<frame src="duelold.cgi?mode=ad&id=$id&pass=$pass&room=$room" name="ad">
</frameset>
<noframes>
<body>デュエルCGIはフレーム対応のブラウザでプレイしてください。</body>
</noframes>
</frameset>
</html>
EOM
	exit;
}

sub form {
	&fileunlock($room);
	&header;
	$str = !($read_only) && (!($side[1]) || !($side[2])) ? "相手が来るのを待っています。落ちるときは「退室」を押してください" : "<strong>$title</strong>";
	print <<"EOM";
<script type="text/javascript"><!--
with(document);
function autoclear() {
	send.mess.value = "";
	send.mess.focus();
}
function sFlag(flag) {
	send.mode.value = flag;
	send.target = ((flag == "regist") || (flag == "nuisance")) ? "message" : (flag == "field") ? "field" : (flag == "dropadmit") ? "message" : (flag == "roommsg") ? "message" : "_self";
	send.submit();
//	if((flag != "field") && (flag != "dropadmit")){ setTimeout('autoclear()',10); }
	send.target = "message";
	send.mode.value = "regist";
}
// --></script>
</head>
<body>
<div align="center">
<form action="duelold.cgi" method="post" name="send" target="message" onsubmit="setTimeout('autoclear()',10);">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="room" value="$room">
	<input type="hidden" name="mode" value="regist">
<table border="0" cellpadding="2" cellspacing="0" align="center">
<tr><td colspan="2">　$str</td></tr>
<tr>
EOM
	if(!($read_only) || (($P{'admin'} > 0) || ($P{'subadmin'} > 0))){
		print "<td colspan=\"2\">\n";
		print "<input type=\"text\" size=\"60\" name=\"mess\">　\n";
#		print "<input type=\"button\" value=\"発言\" onclick=\"sFlag('regist');\">\n";
		print "<input type=\"submit\" value=\"発言\">\n";
		print "<input type=\"reset\" value=\"クリア\">\n";
		print "</td></tr>\n";
		print "<tr>\n";
	}
	print <<"EOM";
<td>&nbsp;&nbsp;ログ行数
<select name="log">
	<option value="10">10</option>
	<option value="20">20</option>
	<option value="30">30</option>
	<option value="9999" selected>ALL</option>
</select>
&nbsp;&nbsp;更新秒数
<select name="load">
	<option value="20">20</option>
	<option value="30" selected>30</option>
	<option value="45">45</option>
	<option value="60">60</option>
	<option value="100">100</option>
</select>
&nbsp;<input type="button" value="更新" onclick="sFlag('field');">
</td>
<td align="right">
EOM
	print "<input type=\"button\" value=\"投了\" onclick=\"if(window.confirm('投了しますか？')){ sFlag('surrender'); }\">\n" if !($read_only) && !($end_flg) && $side[1] && $side[2];
	print "&nbsp;&nbsp;<input type=\"button\" value=\"退室\" onclick=\"if(window.confirm('退室しますか？')){ sFlag('drop'); }\">\n";
	unless($read_only) {
		unless($side[1] && $side[2]) {
			print "&nbsp;&nbsp;<input type=\"button\" value=\"一言更新\" onclick=\"if(window.confirm('この部屋の一言メッセージを現在の発言内容に更新しますか？')){ sFlag('roommsg'); setTimeout('autoclear()',10); }\">\n";
		} else {
			print "&nbsp;&nbsp;<input type=\"button\" value=\"退室許可\" onclick=\"if(window.confirm('対戦相手に退室許可を出しますか？')){ sFlag('dropadmit'); }\">\n";
		}
	}
	print "&nbsp;&nbsp;<a href=\"$help#duel\" target=\"_blank\">説明</a>&nbsp;&nbsp;\n";
	print "</td>\n";
	if($side[1] && $side[2] && !$read_only) {
		print "</tr>\n<tr><td colspan=\"2\"><hr></td>";
		print "</tr>\n<tr><td colspan=\"2\">報告内容: <input size=\"64\" name=\"nuicom\" type=\"text\" value=\"\"> <input type=\"button\" value=\"迷惑報告\" onclick=\"if(window.confirm('この対戦内容を迷惑行為として報告しますか？')){ sFlag('nuisance'); }\"></td>\n";
	    }
	print "</tr></table>\n";
	print "</form>\n";
	&fileunlock($room);
	&footer;
}

sub field {
	&pfl_read($id) if -e "${player_dir}/" . $id . ".cgi";
	for my $i(1..2){
		&del_null(*hand,$i);
		&del_null(*deck,$i);
		&del_null(*boti,$i);
		&del_null(*gear,$i);
		&del_null(*psychic,$i);
	}
	&header;
	print <<"EOM";
	<meta http-equiv="Refresh" content="$load;URL=duelold.cgi?mode=field&id=$id&pass=$pass&room=$room&load=$load&log=$log">
<script type="text/javascript"><!--
with(document);
parent.message.location.href = "duelold.cgi?mode=all&id=$id&pass=$pass&room=$room";
function Tap(){
	fields.mode.value = "tap";
	fields.submit();
}
function Load() {
	str = 'duelold.cgi?id=$id&pass=$pass&room=$room&load=$load&log=$log&mode=';
	if(parent.sousa.card){
		var F = parent.sousa.card;
		if(!parent.flag){
			parent.form.location.href = str + 'form';
			parent.flag = "true";
		}
		parent.sousa.location.href = str + 'sousa&vside=' + F.vside.value + '&varea=' + F.varea.value;
	} else {
		parent.sousa.location.href = str + 'sousa';
	}
}
function bFlag(c){
	fields.mode.value= 'block_flg';
	fields.submit();
}

\$(function(\$) {

		var \$view = \$('#view'),
			\$name = \$('input[name="chatName"]'),
			\$data = \$('#chatData');

		/**
   		* データ取得
   		*/
  		function getData() {
    		\$.post('./chat/chat.php?mode=view', {}, function(data) {
      		\$view.html(data);
      		checkUpdate();
    		});
  		}

  		/**
   		* 更新チェック
   		*/
  		function checkUpdate() {
    		\$.post('./chat/chat.php?mode=check', {}, function(data) {
    		\$view.html(data);
    	  	//checkUpdate();
    		});
  		}

  		\$("#chatAdd").click(function(){
  			\$.post('./chat/chat.php?mode=add', {data: \$data.val(),name: \$name.val()}, function(data) {
      		\$data.val('');
    		});
  		});

  		getData();

  		\$('#chatInputArea').hide();

  		\$("#dispChangeChat").click(function(){
  			if(\$('#chatInputArea').is(':hidden')) {
    			\$('#chatInputArea').show("slow");
  			}else{
  				\$('#chatInputArea').hide("slow");
  			}
    	});
  	});

// --></script>
</head>
<body onload="Load();">
<div align="center">
<form name="fields" method="post" action="duelold.cgi">
	<input type="hidden" name="room" value="$room">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="load" value="$load">
	<input type="hidden" name="log" value="$log">
EOM
	print qq|<input type="hidden" name="mode" value="field">\n| if $syori[0] eq "";
	print qq|<table border="0" cellpadding="10"><tr align="center"><td colspan="2">\n|;
	&view_field($u_side2,3);
	print qq|</td></tr>\n<tr align="center"><td colspan="2">\n|;
	&view_field($u_side2,2);
	print "</td></tr>\n";
	&view_gear($u_side2) if -1 < $#{$gear[$u_side2]};
	print qq|<tr align="center"><td>\n|;
	&view_field($u_side2,1);
	print "</td><td>\n";
	&view_field($u_side2,0);
	print "</td></tr>\n</table>\n";
	print "<hr>\n";
	&field_sel;
	print qq|<table border="0" cellpadding="10">\n<tr align="center"><td>\n|;
	&view_field($u_side,0);
	print "</td><td>\n";
	&view_field($u_side,1);
	print qq|</td></tr>\n<tr align="center"><td colspan="2">\n|;
	&view_field($u_side,2);
	print "</td></tr>\n";
	&view_gear($u_side) if -1 < $#{$gear[$u_side]};
	print qq|<tr align="center"><td colspan="2">\n|;
	&view_field($u_side,3);
	if(!$read_only) {
		print qq|</td></tr>\n|;
		print qq|<tr align="center"><td colspan="2">\n|;
		print qq|<input type="button" value="タップ／アンタップ" onclick="if(confirm('本当にタップ／アンタップしますか？\\nこの行動は、バトルゾーンにあるクリーチャーだけでなく、\\nマナゾーンにあるカードをタップ／アンタップする場合にも使います。')) { this.disabled = true; Tap(); }">\n|;
            }

    print qq|\n<tr><td colspan=\"2\"><table width="400" border="1" cellpadding="3" cellspacing="0" bgcolor="#FFFFFF">
				<tr><td>
				<hr>
				<center>
				<div class=\"dispChangeChat\">
	<a id=\"dispChangeChat\">入力する</a>
</div>
<div id="chatInputArea">

  <input type=\"hidden\" name=\"chatName\" value=\"$P{"name"}\" />
  <br><textarea cols=\"40\" rows=\"3\" id=\"chatData\" /></textarea><br>
  <input id=\"chatAdd\" type=\"button\" value=\"書き込み\" />
  <input type=\"button\" onClick=\"javascript:sForm('freeroom', '', '');\" value=\"更新する\">
</center>
</div>
  <div align=\"center\" style=\"width: 500px; height: 180px; overflow: scroll;\">
  <dl>
  <dd id=\"view\">ここにデータ</dd>
  </dl>
  </div>
<hr></td>
</tr></table><br></td></tr>\n|;
    print qq|<tr><td colspan=\"2\"><a href="./etc/help.html#kyoyu" class="jTip" id="100" name="共有掲示板" target="_brank">共有掲示板について</a></td></tr>\n|;
	print qq|</td></tr>\n</table>\n</form>\n|;
	if(!($read_only) || ((($P{'admin'} > 0) || ($P{'subadmin'} > 0)) && $F{'mode'} eq 'dropadmit2')){
		&put_ini;
	}
	&fileunlock($room);
	&footer;
}

sub view_field {
	local ($v_side, $area) = @_;
	print qq|<table border="1" cellspacing="0" class="table">\n|;
	print qq|<tr align="center">\n|;
	if ($area == 0) {
		foreach my $i(@{$fw1[$v_side]}) {
			&view_field_sub($i);
			if ($i%4 == 3) {
				if ($i <= (grep $fld[$_] ne "", @{$fw1[$v_side]})[-1]) { print qq|</tr><tr align="center">\n|; } else { last; }
			}
		}
	} elsif ($area == 1) {
		foreach my $i(@{$fw2[$v_side]}) {
			&view_field_sub($i);
			if ($i < (grep $fld[$_] ne "", @{$fw2[$v_side]})[-1]) { print qq|</tr><tr align="center">\n|; } else { last; }
		}
	} elsif ($area == 2) {
		foreach my $i(@{$fw3[$v_side]}) {
			&view_field_sub($i);
			if ($i%5 == 4) {
				if ($i < (grep $fld[$_] ne "", @{$fw3[$v_side]})[-1]) { print qq|</tr><tr align="center">\n|; } else { last; }
			}
		}
	} else {
		foreach my $i(@{$fw4[$v_side]}) {
			&view_field_sub($i);
			if ($i%5 == 4) {
				if ($i <= (grep($fld[$_] ne "", @{$fw4[$v_side]}))[-1]) { print qq|</tr><tr align="center">\n|; } else { last; }
			}
		}
	}
	print "</tr></table>\n";
}

sub view_gear {
	my $gside = $_[0];
	print qq|<tr align="center"><td colspan="2">\n|;
	print qq|<table border="1" cellspacing="0" class="table">\n|;
	print qq|<tr align="center">\n|;
	my $cou = 0;
	foreach my $i(0..$#{$gear[$gside]}){
		print "<td>";
		next if $gear[$gside][$i] eq "";
		if($gear[$gside][$i] =~ /:/){
			my @s_gear = split(/:/,$gear[$gside][$i]);
			print q|<table border="0">|;
			for my $j(0..$#s_gear-1){
				next if $s_gear[$j] eq "";
				my $k = $gside.'-'.$i.'-'.$j;
				print "<tr>\n<td>";
				print qq|<input type="checkbox" name="gsel$k" value="on" class="none"></td>\n<td>| if $S{'m'} !~ /c_shinka_sel|cloth_sel/ && &control_chk;
				print "$c_name[$s_gear[$j]]";
				print "</td>\n</tr>";
			}
			print "</table>\n";
			$k = $gside.'-'.$i.'-'.$#s_gear;
			&view_gear_sub($gside,$s_gear[-1],$k);
		} else {
			my $k = $gside.'-'.$i;
			&view_gear_sub($gside,$gear[$gside][$i],$k);
		}
		print "</td>\n";
		print "</tr><tr>\n" if $cou % 5 == 4 && $i != $#{$gear[$gside]};
		$cou++;
	}
	print "</tr></table>\n";
	print "</td></tr>\n";
}

sub view_gear_sub {
	my ($gside,$cno,$k) = @_;
	&view_card($cno,1);
	if($S{'m'} eq "c_shinka_sel") {
		if($gside == $u_side) {
			my @rnb = split(/,/,$c_bun[$chudan]);
			print qq|<input type="radio" name="gsel$k" value="on" class="none">\n| if $c_bun[$cno] =~ /$rnb[0]|$rnb[1]/ || $c_name[$cno] eq "レオパルド・グローリーソード";
		}
	} elsif ($S{'m'} eq "cloth_sel") {
		print qq|<input type="radio" name="gsel$k" value="on" class="none">\n| if $gside == $u_side;
	} elsif (&control_chk) {
		print qq|<input type="checkbox" name="gsel$k" value="on" class="none">\n|;
	}
}

sub view_gear_sub2 {
	my ($v_side,$cno,$k,$flg) = @_;
	print "<tr>\n<td>";
	if($S{'m'} eq "c_shinka_sel") {
		if($v_side == $u_side) {
			my @rnb = split(/,/,$c_bun[$chudan]);
			print qq|<input type="radio" name="csel$k" value="on" class="none">\n| if $c_bun[$cno] =~ /$rnb[0]|$rnb[1]/ || $c_name[$cno] eq "レオパルド・グローリーソード";
		}
	} elsif ($S{'m'} eq "cloth_sel") {
		print qq|<input type="radio" name="csel$k" value="on" class="none"></td>\n<td>| if $v_side == $u_side;
	} elsif (&control_chk) {
		print qq|<input type="checkbox" name="csel$k" value="on" class="none"></td>\n<td>|;
	}
	if($flg){
		print "$c_name[$cno]";
	} else {
		&view_card($cno, 4);
	}
	print "</td>\n<tr>";
}

sub view_field_sub {
	local ($fno) = $_[0];
	if ($fld[$fno] eq "") {
		print q|<td><span class="table">＿＿＿＿＿</span>|;
	} else {
		my $cno = $fld[$fno];
		$cno =~ s/\-s$// if $cno =~ /\-s$/;
		printf "<td%s>\n", $f_tap[$fno] ? ' class="tap"' : "";
		if ($f_cloth[$fno] ne "") {
			if ($area == 2) {		# 城
				my @castle = split /-/, $f_cloth[$fno];
				print qq|<table border="0">|;
				foreach my $i (0 .. $#castle) {
					print "<tr>\n<td>";
					printf qq|<input type="checkbox" name="csel%s" value="on"></td>\n<td>|, $fno.'-'.$i if (&control_chk) && !($syori[0]);
					&view_card($castle[$i], 4);
					print "</td>\n</tr>";
				}
				print qq|</table>\n|;
			} else {				# クロスギア
				my @cloth = split /_/, $f_cloth[$fno];
				for my $i(0 .. $#cloth){
					next if $cloth[$i] eq "";
					print qq|<table border="0">|;
					if ($cloth[$i] =~ /:/) {
						my @s_cloth = split /:/, $cloth[$i];
						for my $j (0 .. $#s_cloth) {
							next if $s_cloth[$j] eq "";
							$flg = $j == $#s_cloth ? 0 : 1;
							&view_gear_sub($v_side, $s_cloth[$j], $fno.'-'.$i.'-'.$j, "csel", $flg);
						}
					} else {
						&view_gear_sub($v_side, $cloth[$i], $fno.'-'.$i, "csel");
					}
					print "</table>";
				}
			}
		}
		if ($shinka[$fno] ne "") {
			@{$shinka[$fno]} = split /-/, $shinka[$fno];
			print qq|<table cellpadding="0" cellspacing="0" width="96%" align="center">| if $area == 2;
			foreach my $i(0..$#{$shinka[$fno]}){
				next if $shinka[$fno][$i] eq "";
				print  qq|<tr>| if $area == 2;
				printf qq|%s<input type="checkbox" name="ssel$fno-$i" value="on">%s|, $area == 2 ? "<td>" : "", $area == 2 ? "</td>" : "", if &control_chk;
				print  qq|<td width="99%">| if $area == 2;
				if ($area == 2) {
					print qq|<div class="p_shield"></div>|;
				} else {
					print "$c_name[$shinka[$fno][$i]]<br>\n";
				}
				print qq|</td></tr>| if $area == 2;
			}
			print qq|</table>| if $area == 2;
		}
		print "召喚酔い<br>\n" if $f_drunk[$fno] && !(&k_chk($cno, 6)) && !(&cloth_chk($fno, 1105));
		if ($cno =~ /\-/) {
			&view_god($fno, $area) if $area == 0;
		} else {
			&view_card($cno, $area);
		}
		&view_fldbutton($area) if &control_chk;
		map { print "$c_name[$fld[$_]]<br>\n" } (split /-/, $f_block[$fno]) if $f_block[$fno] ne "" && $area == 2;
	}
	print "</td>\n";
}

sub view_card {
	local ($cno, $area) = @_;
	&c_color($cno);
	if($area == 0){ &view_card1; }
	elsif($area == 1){ &view_card2; }
	elsif($area == 2 && !($fld[$fno] =~ /\-s$/)){ &view_card4; }
	else{ &view_card3; }
}

#sub view_card1 {
#	my $tmpst = !($chudan_flg) && !($read_only) ?
#		sprintf qq|<input type="checkbox" name="block$fno"%s onclick="bFlag();" class="none">ブロッカー\n|,
#			$f_block[$fno] ? " checked" : ""
#		: $f_block[$fno] ? "ブロッカー\n" : "";
#	print qq|<table border="1" cellpadding="0" class="$bgc">\n|;
#	print qq|<tr><td>$c_mana[$cno]/</td><td><a href="javascript:parent.cView($cno);">$c_name[$cno]</a></td></tr>\n|;
#	print qq|<tr><td align="center" colspan="2">$c_pow[$cno]</td></tr>\n|;
#	print qq|<tr><td align="center" colspan="2">$syuzoku</td></tr>\n|;
#	print qq|<tr><td align="center" colspan="2">$tmpst</td></tr>\n| if $tmpst ne "";
#	print qq|<tr><td align="center" colspan="2">$bun</td></tr>\n| if $bgc eq "rainbow";
#	print "</table>\n";
#}

sub view_card1 {
	my $tmpst = $area == 0 && $v_side == $u_side && !($chudan_flg) && !($read_only)
		? sprintf qq|<input type="checkbox" name="block$fno"%s onclick="bFlag();" class="none">ブロッカー\n|, $f_block[$fno] ? " checked" : ""
		: $area == 0 && $f_block[$fno] ? "ブロッカー\n" : "";
	printf qq|<div class="$bgc"%s>\n|, $area =~ /0|3/ ? qq| id="fsel$fno" onclick="sendData('tap', this);"| : "";
	print qq|$c_mana[$cno]/\n| if $area < 2;
	print qq|<a href="javascript:parent.cView($cno);">$c_name[$cno]</a>\n|;
	print qq|<span class="center">$c_pow[$cno]</span>\n| if $area == 0;
	print qq|<span class="center">$syuzoku</span>\n| if $area =~ /0|3/;
	print qq|<span class="center">$tmpst</span>\n| if $tmpst ne "";
	print qq|<span class="center">$bun</span>\n| if $bgc eq "rainbow";
	print "</div>\n";
}

sub view_card2 {
	print qq|<div class="$bgc"%s>\n|;
	print qq|<span class="center">$c_mana[$cno]/|;
	print qq|<a href="javascript:parent.cView($cno);">$c_name[$cno]</a></span>\n|;
	print qq|<span class="center">$bun</span>\n| if $bgc eq "rainbow";
	print "</div>\n";
}

sub view_card3 {
	print qq|<div class="$bgc"%s>\n|;
	print qq|<span class="center"><a href="javascript:parent.cView($cno);">$c_name[$cno]</a></span>\n|;
	print qq|<span class="center">$syuzoku</span>\n| if $area == 3;
	print qq|<span class="center">$bun</span>\n| if $bgc eq "rainbow";
	print "</div>\n";
}

sub view_card4 {
	my $cou = $fno - $fw3[$v_side][0] + 1;
	print qq|<table border="1" cellpadding="0" cellspacing="0" class="shield"><tr>\n|;
	print qq|<td align="center" valign="bottom"><br>$cou<br><span class="shield">＿＿＿＿＿</span></td>\n|;
	print "</tr></table>\n";
}

sub view_god {
	my ($fno, $area) = @_;
	my @god = split /-/, $fld[$fno];
	print qq|<table border="1" cellpadding="0" class="god">\n|;
	print qq|<tr>\n|;
	foreach my $i (0 .. $#god) {
		print "<td>\n";
		&view_card($god[$i], $area);
		printf qq|<input type="checkbox" name="fsel%s" value="on">\n|, $fno.'-'.$i if (&control_chk) && !($v_side == $u_side && $fw1[$u_side][0] <= $fno && $fno <= $fw1[$u_side][-1] && !($f_tap[$fno]) && $btl[4] eq "anonymous") && !($syori[0]);
		print "</td>\n";
	}
	print "</tr>\n";
	print "</table>\n";
}

sub all{
	&filelock("${room}_log");
	open(DB,"room/".$roomst.$room."_log.cgi");
	my $cou = 0;
	while (<DB>) {
		last if $log <= $cou;
		my ($msgman,$msg,$msgmode) = split(/<>/,$_);
		if(($msgmode eq "secret1") || ($msgmode eq "secret2")){
			next if (($msgmode eq "secret1") && ($u_side != 1)) || (($msgmode eq "secret2") && ($u_side != 2)) || $read_only;
			$pstr .= qq|&nbsp;<span class="secret">$msg</span><br>\n|;
			$msg = "";
		} elsif($msgmode eq "system") {
			$pstr .= qq|&nbsp;<span class="system">$msg</span><br>|;
		} elsif($msgmode eq "message") {
			$pstr .= qq|&nbsp;<span class="message">$msgman ＞ $msg</span><br>|;
		} elsif($msgmode eq "message1") {
			$pstr .= qq|&nbsp;<span class="message1">$msgman ＞ $msg</span><br>|;
		} elsif($msgmode eq "message2") {
			$pstr .= qq|&nbsp;<span class="message2">$msgman ＞ $msg</span><br>|;
		} elsif($msgmode eq "tap") {
			$pstr .= qq|&nbsp;<span class="taped">$msg</span><br>|;
		} elsif($msgmode eq "admin") {
			$pstr .= qq|&nbsp;<span class="admin">$msgman ＞ $msg</span><br>|;
		}
		$cou++;
	}
	close(DB);
	&fileunlock("${room}_log");
	&header;
	print <<"EOM";
</head>
<body>
<div align="left">
<table border="0" cellspacing="0" cellpadding="5" width="95%" class="table"><tr><td>
&nbsp;&nbsp;&nbsp;&nbsp;[<A href="./duelold.cgi?mode=all&id=$id&pass=$pass&room=$room">最新のログ</A>]<BR>
$pstr
</td></tr></table>
EOM
	undef(%F); undef(%S);
	&fileunlock($room);
	&footer;
}

sub field_sel{
	return if $syori[0] eq "" || ($S{'m'} ne "janken_sel" && !(&control_chk)) || ($S{'m'} eq "janken_sel" && $janken[$u_side] ne "");
	if ($S{'m'} eq "mekuru_move1") {
		@res2 = grep $_ ne "", @res2;
		if ($#res2 < 0) {
			&syori_clr;
			$chudan_flg = "";
			return;
		}
	}
	&syori_p_set;
	my @butstr = split(/::/,$S{'o'});
	print <<"EOM";
<input type="hidden" name="mode" value="$S{'m'}">
<table border="0" class="shield" cellpadding="5">
<tr align="center"><td>$S{'t'}</td></tr>
EOM
	unless($S{'m'} =~ /battle_sel|mekuru_sel1/){
		print qq|<tr align="center"><td>\n|;
		if ($S{'m'} eq "bikkuri_sel") {					# ビックリ・イリュージョン
			print qq|<select name="add">\n|;
			map { print qq|<option value="$_">$syu[$_]</option>\n|; } (2 .. $#syu);
			print "</select>\n";
		} elsif ($S{'m'} eq "janken_sel") {				# ジャンケン
			print qq|<input type="radio" name="janken" value="グー"> グー\n|;
			print qq|<input type="radio" name="janken" value="チョキ"> チョキ\n|;
			print qq|<input type="radio" name="janken" value="パー"> パー\n|;
		} elsif($S{'m'} =~ /mekuru_sel2|mekuru_sel3/){	# 枚数を指定してめくる
			print qq|<input type="hidden" name="secret" value="on">\n| if $S{'p'} eq "secret";
			print qq|<input type="text" size="20" name="maisu">枚\n|;
		} elsif ($S{'m'} =~ /mekuru_move1|mekuru_move2|mekuru_sel4|mekuru_sel5|changer_sel2|return_sel/) {
														# 順番を指定
			print qq|<input type="hidden" name="secret" value="on">\n| if $S{'p'} eq "secret";
			print qq|<table><tr>\n|;
			my $cou = 0;
			foreach my $cno (@res2) {
				next if $cno eq "";
				print q|<td align="center">|;
				&view_card($cno, sprintf(%d, !(&syu_chk($cno, 0)) && !(&syu_chk($cno, 1)) ? 1 : 0));
				if($S{'m'} eq "mekuru_move1"){
					print qq|<input type="checkbox" name="rsel$cou" value="$cno">\n|;
				} elsif($S{'m'} =~ /mekuru_move2|changer_sel2|return_sel/) {
					print qq|<select name="rsel$cou">\n|;
					print qq|<option value="0">手札へ</option>\n| if $S{'m'} eq "mekuru_move2";
					print qq|<option value="1">墓地へ</option>\n| if $S{'m'} eq "mekuru_move2";
					print qq|<option value="2">1番上</option>\n|;
					foreach my $i (2..$#res2+1){
						printf qq|<option value="%s">$i番目</option>\n|, $i + 1;
					}
					print "</select>\n";
				}
				print "</td>\n";
				print "</tr><tr>\n" if $cou%5 == 4;
				$cou++;
			}
			print "</tr></table>\n";
		} else {
			my $cou = 0;
			if ($S{'m'} =~ /trigger_sel1|strike_sel1/) {
				print qq|<table><tr>\n|;
				foreach my $i(0..$#shield) {
					next if $shield[$i] eq "";
					my $cno = $shield[$i];
					print qq|<td align="center">|;
					&view_card($cno, sprintf(%d, !(&syu_chk($cno, 0, 1)) ? 1 : 0));
					print qq|<input type="radio" name="select" value="$i">\n|
						if ($S{'m'} eq "trigger_sel1" && &s_tri_chk) || ($S{'m'} eq "strike_sel1" && &strike_chk($cno, $btl[1]));
#						if ($S{'m'} eq "trigger_sel1" && (&tri_chk($cno, 1) || &c_chk("星龍パーフェクト・アース", $btl[1]))) || &seiryu_chk || ($S{'m'} eq "strike_sel1" && &strike_chk($cno, $btl[1]));
					print "</td>\n";
					print "</tr><tr>\n" if $cou%5 == 4;
					$cou++;
				}
				print "</tr></table>\n";
			} elsif ($S{'m'} =~ /cloth_sel2|c_shinka_sel|arcadia_sel/) {
				my $cno = $chudan !~ /:/ ? $chudan : (split /:/, $chudan)[-1];	# $chudanに保存されたカードを表示
				&view_card($cno, sprintf(%d, !(&syu_chk($cno, 0)) && !(&syu_chk($cno, 1)) ? 1 : 0));
			}
			if ($S{'m'} eq "strike_sel1") {	# ストライク・バックの場合に分割ラインを表示
				print qq|</td></tr>\n|;
				print qq|<tr align="center"><td><hr></td></tr>\n|;
				print qq|<tr align="center"><td>\n|;
			}
			print qq|<table><tr>\n|;
			my $cou = 0;
			foreach $res(@res) {
				if ($S{'m'} eq "meteo_sel") {	# メテオバーンで捨てるカードを選択
					my @shinka = split /-/, $shinka[$res];
					foreach my $i(0..$#shinka) {
						next if $shinka[$i] eq "";
						my $k = $res.'-'.$i;
						my $cno = $shinka[$i];
						print qq|<td align="center">|;
						&view_card($cno, sprintf(%d, !(&syu_chk($cno, 0, 1)) ? 1 : 0));
						printf qq|<input type="%s" name="%s" value="$k">\n|,
							$c_name[$fld[$res]] =~ /超神星ペテルギウス・ファイナルキャノン|超神星DEATH・ドラゲリオン/ ? "checkbox" : "radio",
							$c_name[$fld[$res]] =~ /超神星ペテルギウス・ファイナルキャノン|超神星DEATH・ドラゲリオン/ ? "rsel$k" : "select";
						print "</td>\n";
						print "</tr><tr>\n" if $cou%5 == 4;
						$cou++;
					}
				} elsif ($S{'m'} !~ /cloth_sel2|c_shinka_sel/) {
					my $cno = $S{'p'} ? $res : $S{'m'} eq 'b_shinka_sel' || $S{'m'} eq 'b_vor_sel' || $S{'m'} eq 'b_vor_sel2' ? $boti[$u_side][$res] : $fld[$res];
					next if $cno eq "";
					print q|<td align="center">|;
					if ($cno =~ /\-/) { &view_god($res, 0); } else { &view_card($cno, sprintf %d, !(&syu_chk($cno, 0)) && !(&syu_chk($cno, 1)) ? 1 : 0); }
					printf qq|<input type="%s" name="%s" value="$res">\n|,
						$S{'m'} eq "dynamo_sel" ? "checkbox" : "radio",
						$S{'m'} eq "dynamo_sel" ? "rsel$res" : $S{'m'} eq "strike_sel1" ? "select2" : "select";
					print "</td>\n";
					print "</tr><tr>\n" if $cou%5 == 4;
					$cou++;
				}
			}
			print "</tr></table>\n";
		}
		print "</td></tr>\n";
	}
	print qq|<tr><td align="center">\n|;
	print qq|<input type="submit" value="$butstr[0]" name="run_select">|;
	print qq|　<input type="submit" value="$butstr[1]" name="not_select">| if $butstr[1];
	print "\n</td></tr>\n</table>\n";
}

sub niheya_chk {
	foreach my $i (1 .. $heyakazu) {
		next if $i == $room;
		undef %N;
		open  IN, "room/".$roomst.$i.'.cgi';
		while(<IN>){ chomp; ($key, $val) = split /\t/; $N{$key} = $val; }
		close IN;
		&error("部屋番号$iを先に終わらせてください") if $N{'side1'} eq $id || $N{'side2'} eq $id;
	}
}

sub control_chk {
	return 0 if ($read_only || !($side[1]) || !($side[2]));
	&syori_p_set;
	my $c_side = $S{'s'} ne "" ? $S{'s'} : $turn2;
	return 0 if $c_side ne $u_side;
	return 1;
}

sub syori_p_set {
	undef(%S);
	return if $syori[0] eq "";
	my @tmp = split(/<>/,$syori[0]);
	map { $S{$1} = $2 if $_ =~ /(.)-(.+)/ } @tmp;
}

sub regist {
	my ($msgman,$msg,$msgmode) = @_;
	return if($msg eq '');
	$msgmode = "system" if($msgmode eq '');
	&filelock("${room}_log");
	open(IN,"room/".$roomst.$room."_log.cgi");
	my @lines = <IN>;
	close(IN);
	$msg =~ s/Bold\((.*?)\)/\<b\>$1\<\/b\>/g;
	$msg =~ s/Italic\((.*?)\)/\<i\>$1\<\/i\>/g;
	$msg =~ s/Underline\((.*?)\)/\<u\>$1\<\/u\>/g;
	$msg =~ s/Strike\((.*?)\)/\<s\>$1\<\/s\>/g;
	$msg =~ s/\\\(/\(/g;
	$msg =~ s/\\\)/\)/g;
	unshift(@lines,"$msgman<>$msg<>$msgmode<>\n");
	open(OUT,">room/".$roomst.$room."_log.cgi") || &error("ログファイルに書き込めません");
	print OUT @lines;
	close(OUT);
	&fileunlock("${room}_log");
}

sub put_ini{
	my $putst = "";
	foreach my $data(@pfldata){
		$evalst = '$val=$'.$data;
		eval($evalst);
		$putst .= "$data\t$val\n" if $val ne "";
	}
	foreach my $datb(@pfldata2){
		foreach my $i(1..2){
			$evalst = '$val=$'.$datb.'['.$i.']';
			eval($evalst);
			$putst .= "$datb$i\t$val\n" if $val ne "";
		}
	}
	foreach my $lsta(@pflst){
		$evalst = '$val=join(",",@'.$lsta.')';
		eval($evalst);
		$putst .= "$lsta\t$val\n" if $val !~ /^,*$/;
	}
	foreach my $lstb(@pflst2){
		foreach my $i(1..2){
			$evalst = '$val=join(",",@{$'.$lstb.'['.$i.']})';
			eval($evalst);
			$putst .= "$lstb$i\t$val\n" if $val !~ /^,*$/;
		}
	}
	open(PFL,">room/".$roomst.$room.'.cgi') || &error("Write Error");
	print PFL $putst;
	close(PFL);
}

sub get_ini{
	return unless -e "room/".$roomst.$room.'.cgi';
	open(PFL,"room/".$roomst.$room.'.cgi') || &error("データファイルが開けません");
	my(@tmppfl) = <PFL>;
	&error("データファイルが壊れているか、読み込みに失敗した可能性があります。") if($#tmppfl < 0);
	foreach(@tmppfl){ chomp; ($key,$val) = split(/\t/); $G{$key} = $val; }
	close(PFL);
	foreach my $data(@pfldata){
		$evalst = '$'.$data.' = $G{"'.$data.'"}';
		eval($evalst);
	}
	foreach my $datb(@pfldata2){
		foreach my $i(1..2){
			$evalst = '$'.$datb.'['.$i.'] = $G{"'.$datb.$i.'"}';
			eval($evalst);
		}
	}
	foreach my $lsta(@pflst){
		$evalst='@'.$lsta.' = split(/,/,$G{"'.$lsta.'"})';
		eval($evalst);
	}
	foreach $lstb(@pflst2){
		foreach my $i(1..2){
			$evalst = '@{$'.$lstb.'['.$i.']} = split(/,/,$G{"'.$lstb.$i.'"})';
			eval($evalst);
		}
	}
}

sub decode2 {
	$id = $F{'id'};
	$id =~ s/\.|\///g;
	$pass = $F{'pass'};
	$pass =~ s/\.|\///g;
	$room = $F{'room'};
	$load = $F{'load'} ? $F{'load'} : 30;
	$log = $F{'log'} ? $F{'log'} : "9999";
	&error("IDが入力されていません") unless $id;
	&error("パスワードが入力されていません。") unless $pass;
	if($F{'mess'}) {
		$F{'mess'} =~ s/</&lt\;/g;
		$F{'mess'} =~ s/>/&gt\;/g;
	}
	$random = $F{'random'};
}

#---admin.cgiからのジャンプ処理---#

sub tourreset {
	if($P{'admin'} > 0) {
		&cardread;
		%T = ();
		chmod 0666, "./tour/part.dat";
		open(TRT, "./tour/part.dat");
		while(<TRT>){ chop; ($KEY,$VAL) = split(/\t/); $T{$KEY} = $VAL; }
		close(TRT);
		%NT = ();
		$NT{'scale'} = $T{'scale'};
		$NT{'remain'} = $T{'remain'};
		$NT{'p_fame'} = $T{'p_fame'};
		$NT{'fame'} = $T{'fame'};
		$NT{'type'} = $T{'type'};
		$NT{'date'} = $times;
		for(my($i) = 1; $i <= 2 ** $T{'scale'}; $i ++) {
			$room = "t${i}";
			for(my($j) = 1; $j <= 2; $j ++) {
				my($pnum) = ($i - 1) * 2 + $j;
				@arr_deck = split(/-/, $T{"p${pnum}deck"});
				@{$deck[$j]} = split(/\,/, $arr_deck[0]);
				@{$psychic[$j]} = split(/\,/, $arr_deck[1]);
				#@{$deck[$j]} = split(/\,/, $T{"p${pnum}deck"});
				&shuffle(*deck,$j);
				$side[$j] = $T{"p${pnum}id"};
				$pass[$j] = $T{"p${pnum}pass"};
				$pn[$j] = $T{"p${pnum}name"};

				$NT{"p${pnum}id"} = $T{"p${pnum}id"};
				$NT{"p${pnum}pass"} = $T{"p${pnum}pass"};
				$NT{"p${pnum}name"} = $T{"p${pnum}name"};
				$NT{"p${pnum}deck"} = $T{"p${pnum}deck"};
				$NT{"p${pnum}win"} = 0;
				$sur_flg[$j] = 0;
				if($j == 1) { &put_ini; } else { &start2; }
			}
		}
		chmod 0666, "./tour/part.dat";
		open(TRT, "> ./tour/part.dat");
		foreach $key(keys(%NT)){ print TRT "$key\t$NT{$key}\n"; }
		close(TRT);
		print "Location: ./admin.cgi?id=$F{'id'}&pass=$F{'pass'}\n\n";
	} else {
		print "Location: ./index.cgi\n\n";
	}
}

sub tourstart {
	if($P{'admin'} > 0) {
		&cardread;
		%T = ();
		chmod 0666, "./tour/part.dat";
		open(TRT, "./tour/part.dat");
		while(<TRT>){ chop; ($KEY,$VAL) = split(/\t/); $T{$KEY} = $VAL; }
		close(TRT);
		%PR = ();
		chmod 0666, "./tour/priority.dat";
		open(PRT, "./tour/priority.dat");
		while(<PRT>){ chop; ($KEY,$VAL) = split(/\t/); $PR{$KEY} = $VAL; }
		close(PRT);
		%NT = ();
		$NT{'scale'} = $T{'scale'};
		$NT{'remain'} = $T{'remain'};
		$NT{'p_fame'} = $T{'p_fame'};
		$NT{'fame'} = $T{'fame'};
		$NT{'type'} = $T{'type'};
		$NT{'date'} = $times;
		if($T{'accept'} == 1) {
			$T{'remain'} = 0;
			# 全体をシャッフル
			my(@num) = &num_shuf(1 .. $T{'number'});
			# 優先権の高い人を上に持ってくる
			@num = reverse sort { $PR{$T{"p${a}id"}} <=> $PR{$T{"p${b}id"}} } @num;
			# 当選者をシャッフル
			my(@win) = &num_shuf(1 .. (2 ** $T{'scale'} * 2));

			for(my($i) = 1; $i <= 2 ** $T{'scale'}; $i ++) {
				$room = "t${i}";
				for(my($j) = 1; $j <= 2; $j ++) {
					my($pnum) = ($i - 1) * 2 + $j;
					@arr_deck = split(/-/, $T{"p$num[$win[$pnum]]deck"});
					#@{$deck[$j]} = split(/\,/, $T{"p$num[$win[$pnum]]deck"});
					@{$deck[$j]} = split(/\,/, $arr_deck[0]);
					@{$psychic[$j]} = split(/\,/, $arr_deck[1]);
					&shuffle(*deck,$j);
					$side[$j] = $T{"p$num[$win[$pnum]]id"};
					$pass[$j] = $T{"p$num[$win[$pnum]]pass"};
					$pn[$j] = $T{"p$num[$win[$pnum]]name"};
					$date[$j] = $times;

					$NT{"p${pnum}id"} = $T{"p$num[$win[$pnum]]id"};
					$NT{"p${pnum}pass"} = $T{"p$num[$win[$pnum]]pass"};
					$NT{"p${pnum}name"} = $T{"p$num[$win[$pnum]]name"};
					$NT{"p${pnum}deck"} = $T{"p$num[$win[$pnum]]deck"};
					$NT{"p${pnum}win"} = $T{"p$num[$win[$pnum]]win"};

					$PR{$T{"p$num[$win[$pnum]]id"}} --;
					delete($PR{$T{"p$num[$win[$pnum]]id"}}) if($PR{$T{"p$num[$win[$pnum]]id"}} == 0);
					$sur_flg[$j] = 0;
					if($j == 1) { &put_ini; } else { &start2; }
				}
			}
			for(my($i) = 2 ** $T{'scale'} + 1; $i <= $T{'number'}; $i ++) {
				for(my($j) = 1; $j <= 2; $j ++) {
					my($pnum) = ($i - 1) * 2 + $j;
					$PR{$T{"p$num[$pnum]id"}} ++;
				}
			}

			$T{'accept'} = 0;
			chmod 0666, "./tour/part.dat";
			open(TRT, "> ./tour/part.dat");
			foreach $key(keys(%NT)){ print TRT "$key\t$NT{$key}\n"; }
			close(TRT);
			chmod 0666, "./tour/priority.dat";
			open(PRT, "> ./tour/priority.dat");
			foreach $key(keys(%PR)){ print PRT "$key\t$PR{$key}\n"; }
			close(PRT);
		}
		print "Location: ./admin.cgi?id=$F{'id'}&pass=$F{'pass'}\n\n";
	} else {
		print "Location: ./index.cgi\n\n";
	}
}

