#!/usr/local/bin/perl

require "cust.cgi";
require "action.pl";
require "duel.pl";
require "common.pl";

&decode;
&decode2;
&cardread if $F{'mode'} =~ /tourjoin|duel|cardview/;
&syu_read if $F{'mode'} !~ /form|regist|all/;
&cardread2 if $F{'mode'} !~ /form|regist|all|tourjoin|duel|cardview/;

@pfldata	= qw (dendou phase turn turn2 chudan chudan_flg end_flg trigger_flg skip_flg boru_cnt vor_cnt message dgroup duelid choose white black multi roomid start_date nid1 nnm1 nid2 nnm2 reverse_flg);
@pfldata2	= qw (lp side pn pass dnam usedeck date sur_flg drank ip janken tourtime);
@pflst		= qw (fld f_tap f_block f_drunk f_cloth shinka res syori btl vor syu_add shield magic res2);
@pflst2		= qw (deck hand boti gear psychic);
@phasestr	= qw (ターン開始フェイズ ドローフェイズ マナチャージフェイズ メインフェイズ アタックフェイズ);

@{$fw1[1]} = (280..319); @{$fw2[1]} = (240..279); @{$fw3[1]} = (200..239); @{$fw4[1]} = (160..199);
@{$fw1[2]} = (120..159); @{$fw2[2]} =  (80..119); @{$fw3[2]} =   (40..79); @{$fw4[2]} =    (0..39);

#&filelock($room);

if ($F{'mode'} eq "duel" && !($end_flg)) { &start; } else { &get_ini; }

&error("IDまたはパスワードが間違っています。入力し直してください。")
	if ($F{'mode'} ne "cardview" && $F{'mode'} ne "prof") && ($id eq $side[1] || $id eq $side[2]) && ($pass ne "" && (crypt($pass, $pass) ne $pass[1]) && (crypt($pass, $pass) ne $pass[2]));

if($side[1] eq $side[2]) {
	$u_side		= $turn2;
} else {
	$u_side		= $side[2] eq $id && $side[2] ? 2 : 1;
}
$u_side = (($u_side - 1) xor $reverse_flg) + 1;

$read_only	= 1 if $side[1] ne $id && $side[2] ne $id;
$u_side2	= 3 - $u_side;

&pfl_read($id) if (-e "player/".$id.".cgi" && $read_only);
$admin = (($P{'admin'} > 0) || ($P{'subadmin'} > 0)) ? 1 : 0;

#if ($F{'mode'} !~ /regist|drop|surrender|mess/ && -e "room/".$roomst.$room."_card.cgi") {
#	&read_cardfile;
#	&syu_read;
#}

&html			if !($F{'mode'}) || $F{'mode'} =~ /audience|duel/;
&regist($pn[$u_side], $F{'mess'}, "message$u_side")	if $F{'mode'} eq "regist" && !($read_only);
&regist($P{'name'},$F{'mess'},"admin")
					if $F{'mode'} eq "regist" && $read_only && (($P{'admin'} > 0) || ($P{'subadmin'} > 0));
&regist("", $F{'mess'}, "system")	if $F{'mode'} eq "regist2";
&access_chk();

&drop			if $F{'mode'} eq "drop";
&surrender		if $F{'mode'} eq "surrender" && !($end_flg);
&rcom			if $F{'mode'} eq "rcom";
&cardview		if $F{'mode'} eq "cardview";
&prof			if $F{'mode'} eq "prof";
unless ($chudan_flg) {
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
	&psychic		if $F{'mode'} eq "psychic";
	&psy_link		if $F{'mode'} eq "psy_link";
}
&block_flg			if $F{'mode'} eq "block_flg";
&shinka_sel			if $F{'mode'} eq "shinka_sel";
&c_shinka_sel		if $F{'mode'} eq "c_shinka_sel";
&vor_sel1			if $F{'mode'} eq "vor_sel";
&vor_sel2			if $F{'mode'} eq "vor_sel2";
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
&status				if $F{'mode'} eq "status";
&cardlist			if $F{'mode'} eq "cardlist" && $side[1] && $side[2] && !($end_flg) && !($read_only);
&mess				if $F{'mode'} eq "mess";

&act_cancel	if $F{'mode'} eq "cancel";
&drop_admit	if $F{'mode'} eq "dropadmit";
&drop_admit2	if $F{'mode'} eq "dropadmit2" && $read_only && (($P{'admin'} > 0) || ($P{'subadmin'} > 0));
&nuisance	if $F{'mode'} eq "nuisance";
&kakunin		if $F{'mode'} eq "kakunin";
&kakunin_sel		if $F{'mode'} eq "kakunin_sel";

&put_ini unless $read_only;

&fileunlock($room);

print "Content-type: text/html\n\n";
exit;

sub read_cardfile {
	open  DATA, "room/".$roomst.$room."_card.cgi" || &error("カードデータを読み込めません。");
	while(<DATA>){
		chomp;
		my @card = split /\t/;
		$cou = shift @card;
		($c_name[$cou], $c_bun[$cou], $c_syu[$cou], $c_pow[$cou], $c_mana[$cou], $c_evo[$cou], $c_kok[$cou], $c_tri[$cou]) = @card;
	}
	close DATA;
}

sub end_game {
	&end_game_sub;
	&html;
}

sub drop {
	if(!($read_only) && ($room !~ /^t/)){
		my $name = $pn[$u_side];
		&regist("","$nameさんが退室しました。(IP: $ENV{'REMOTE_ADDR'})", "system");
		$sur_flg[$u_side2] = 0;
		if((!($side[1]) || !($side[2])) || ($side[1] eq $side[2])){
			unlink("room/".$roomst.$room.'.cgi');
			unlink("room/".$roomst.$room."_log.cgi","room/".$roomst.$room.".cgi");
		} else {
			if(!($sur_flg[$u_side]) && !($end_flg)) {
				&regist("","退室許可が出ていないので、$nameは負けになります。", "system");
				$lp[$u_side] = 0;
				$lp[$u_side2] = 1;
				$sr[$u_side] = 1;
				$sr[$u_side2] = 0;
				&end_game_sub;
			}
			&all_clr($u_side);
			&deck_reload($u_side2);
			&put_ini;
		}
	}
	&fileunlock($room);
	exit;
}

sub surrender {
	&regist("","$pn[$u_side]さんが投了しました。", "system");
	$lp[$u_side] = 0;
	$sr[$u_side] = 1;
	$sr[$u_side2] = 0;
	&end_game;
}

sub deck_reload {
	my $sd = $_[0];
	&pfl_read($side[$sd]);
	my $use = $usedeck[$sd];
	@{$deck[$sd]} = split /,/, (split /-/, $P{"deck$use"})[1];
}

sub html {
	&fileunlock($room);
	&header;
	my $str = " checked=checked" if $F{'ninja'} ne "";
	print <<"EOM";
	<link rel="stylesheet" href="$css/thickbox.css" type="text/css">
	<script type="text/javascript" src="$js/jquery.js"></script>
	<script type="text/javascript" src="$js/form.js"></script>
	<script type="text/javascript" src="$js/thickbox.js"></script>
<script><!--
	var u_side = "$u_side", u_side2 = "$u_side2", read_only = "$read_only", pn = "$pn[$u_side]", admin = "$admin"; end_flg = "0"; side1 = "$side[1]"; side2 = "$side[2]";
// --></script>
<script type="text/javascript" src="$js/duel.js"></script>
</head>
<body id="duelfld">
<form action="duel.cgi" method="post" name="duel" id="duel" onsubmit="sendData('regist'); return false;">
	<input type="hidden" name="room" id="room" value="$room">
	<input type="hidden" name="id" id="id" value="$id">
	<input type="hidden" name="pass" id="pass" value="$pass">
	<input type="hidden" name="mode" id="mode" value="regist">
	<table width="100%" border="0" cellpadding="10" cellspacing="0">
	<tr>
		<td class="header" colspan="1"><strong>$title</strong></td>
		<td align="right" class="header" colspan="2">
			<input type="button" value="投了" id="surrender" onclick="if(window.confirm('投了しますか？')){sendData('surrender');}">
			<input type="button" value="退室" onclick="if(window.confirm('退室しますか？')){sendData('drop');}">
			<input type="button" value="一言更新" id="roommsg" onclick="if(window.confirm('この部屋の一言メッセージを現在の発言内容に更新しますか？')){sendData('roommsg');}">
			<input type="button" value="退室許可" id="dropadmit" onclick="if(window.confirm('対戦相手に退室許可を出しますか？')){sendData('dropadmit');}">
			<img src="$image/book_open.png" width="16" height="16" alt="説明"><a href="help/help.html#duel" target="_blank">説明</a>
		</td>
	</tr>
	<tr valign="top">
		<td width="180" align="center">
			<table width="180" cellpadding="5" cellspacing="0" border="1" class="table">
			<tr><td id="status"></td></tr>
			<tbody id="kansen" style="display:none;">
EOM
	if((($P{'admin'} > 0) || ($P{'subadmin'} > 0)) && ($read_only)) {
		print <<"EOM";
			<tr><td>
			<select name="tp">
			<option value="$u_side" selected>$pn[$u_side]</option>
			<option value="$u_side2">$pn[$u_side2]</option>
			</select> に <input type="button" value="退室許可" onClick="if(confirm('本当に退室許可を出しますか？')) {sendData('dropadmit2');}">
			</tr>
EOM
	}
	$kansen = $kansen[int(rand($#kansen))];
	print <<"EOM";
			<tr><td><img src="$image/$kansen" width="180" alt="観戦中"></td></tr>
			</tbody>
			<tbody id="console">
EOM
	if($side[1] eq $side[2]) {
		print <<"EOM";
			<tr><td align="center">
				<input type="button" value="操作権限の入れ替え" id="rcom" onclick="if(window.confirm('操作権限を入れ替えますか？\\n\\nこのコマンドは一人対戦用です。\\n実行すると、相手の画面を操作するようになります。')){sendData('rcom');}">
			</td></tr>
EOM
	}
	print <<"EOM";
			<tr><td align="center">
					<input type="button" value="ドロー" onclick="if(window.confirm('ドローしますか？')){sendData('draw');}">
					<input type="button" value="シャッフル" onclick="if(window.confirm('シャッフルしますか？')){sendData('shuffle');}">
			</td></tr>
			<tr><td align="center">
				<input type="button" value="ターン終了" id="phase" onclick="if(window.confirm('ターン終了しますか？')){sendData('phase');}">
			</td></tr>
			<tr><td align="center">
				<input type="button" value="アタック" onclick="if(window.confirm('アタックしますか？')){sendData('battle');}">&nbsp;<input type="checkbox" name="rush" value="on">ターボラッシュ
				<input type="button" value="シールドブレイク" onclick="if(window.confirm('シールドブレイクしますか？')){sendData('break');}">
			</td></tr>
			<tr align="center"><td>
				<input type="button" value="行動をキャンセル" onclick="if(window.confirm('本当に行動をキャンセルしますか？\\nこの行動は、基本的にバグで何も出来なくなった状態からの\\n脱出に使われます。')) {sendData('cancel');}">
			</td></tr>
			<tr><td align="center">
				<input type="button" value="タップ／アンタップ" onclick="if(window.confirm('本当にタップ／アンタップしますか？\\nこの行動は、バトルゾーンにあるクリーチャーだけでなく、\\nマナゾーンにあるカードをタップ／アンタップする場合にも使います。')) {sendData('tap');}">
			</td></tr>
			<tr><td align="center">
				<input type="button" value="相手の手札を見ずに捨てる" onclick="if(window.confirm('相手の手札を見ずに捨てますか？')){sendData('rand_tehuda');}">
			</td></tr>
			<tr><td align="center">
				<select name="marea">
					<option value="0">シールドを</option>
					<option value="1">山札を１枚ずつ</option>
					<option value="2">枚数を指定して</option>
					<option value="3">相手の山札の上を</option>
				</select>
				<input type="button" value="めくる" onclick="if(window.confirm('めくりますか？')){sendData('mekuru');}"><br>
				<input type="checkbox" name="impulse" value="on">めくった後、山札に戻す<br>
				<input type="checkbox" name="secret" value="on">自分だけが見る
			</td></tr>
			<tr><td align="center">
				<input type="button" value="クロス" onclick="if(window.confirm('クロスしますか？')){sendData('cloth');}">
			</td></tr>
			<tr><td align="center">
				<input type="button" value="ジャンケン" onclick="if(window.confirm('本当にジャンケンしますか？')) {sendData('janken');}">
			</td></tr>
			<tr><td align="center">
				<input type="button" value="覚醒／解除" onclick="if(window.confirm('本当に覚醒／解除しますか？')) {sendData('psychic');}">
			</td></tr>
			<tr><td align="center">
				<input type="button" value="覚醒リンク" onclick="if(window.confirm('本当に覚醒リンクしますか？')) {sendData('psy_link');}">
			</td></tr>
EOM
	if($room =~ /^t/) {
		print <<"EOM";
			<tr><td align="center">
				<input type="button" value="相手に確認を取る" onclick="if(confirm('本当に相手に確認を取りますか？')) {sendData('kakunin');}">
			</td></tr>
EOM
	}
	print <<"EOM";
			<tr><td align="center">
				<input type="checkbox" name="decktop" value="on">山札の<select name="under"><option value="0" selected>一番上</option><option value="1">一番下</option></select>のカードを<br>
				<input type="checkbox" name="show" value="on">相手に見せないで<br>
				<select name="parea">
					<option value="0">マナゾーンへ</option>
					<option value="1">バトルゾーンへ</option>
					<option value="2">墓地へ</option>
					<option value="3">手札へ</option>
					<option value="4">山札の上へ</option>
					<option value="5">山札の下へ</option>
					<option value="6">シールドへ</option>
					<option value="7">進化獣の下へ</option>
					<option value="8">シールドの下へ</option>
					<option value="9">超次元ゾーンへ</option>
				</select>
				<input type="button" value="移動" onclick="if(window.confirm('移動しますか？')){sendData('move');}">
			</td></tr>
			<tr><td align="center">
				カードの移動(内容は上と同じです)<br>
				<input type="button" value="マナへ" onclick="if(window.confirm('本当にマナゾーンへカードを移動しますか？')) {document.duel.parea.selectedIndex=0;sendData('move');}">
				<input type="button" value="バトルゾーンへ" onclick="if(window.confirm('本当にバトルゾーンへ移動しますか？')) {document.duel.parea.selectedIndex=1;sendData('move');}"><br>
				<input type="button" value="手札へ" onclick="if(window.confirm('本当に手札へ移動しますか？')) {document.duel.parea.selectedIndex=3;sendData('move');}">
				<input type="button" value="墓地へ" onclick="if(window.confirm('本当に墓地へ移動しますか？')) {document.duel.parea.selectedIndex=2;sendData('move');}">
				<input type="button" value="シールドへ" onclick="if(window.confirm('本当にシールドへ移動しますか？')) {document.duel.parea.selectedIndex=6;sendData('move');}"><br>
				<input type="button" value="山札の上へ" onclick="if(window.confirm('本当に山札の上へ移動しますか？')) {document.duel.parea.selectedIndex=4;sendData('move');}">
				<input type="button" value="山札の下へ" onclick="if(window.confirm('本当に山札の下へ移動しますか？')) {document.duel.parea.selectedIndex=5;sendData('move');}">
				<input type="button" value="進化獣の下へ" onclick="if(window.confirm('本当に進化獣の下へ移動しますか？')) {document.duel.parea.selectedIndex=7;sendData('move');}"><br>
				<input type="button" value="シールドの下へ" onclick="if(window.confirm('本当にシールドの下へ移動しますか？')) {document.duel.parea.selectedIndex=8;sendData('move');}">
				<input type="button" value="超次元ゾーンへ" onclick="if(window.confirm('本当に超次元ゾーンへ移動しますか？')) {document.duel.parea.selectedIndex=9;sendData('move');}">
			</td></tr>
			<tr><td>
				<p align="center">
					<select name="vside">
						<option value="0" selected>自分</option>
						<option value="1">相手</option>
					</select>
					<select name="varea">
						<option value="0" selected>手札</option>
						<option value="1">墓地</option>
						<option value="2">山札</option>
						<option value="3">次元</option>
					</select>
					<input type="button" value="切替" onclick="if(window.confirm('切り替えますか？')){sendData('cardlist'); showAlert();}">
				</p>
				<div id="cardList"></div>
			</td>
			</tr>
			</tbody>
			</table>
		</td>
		<td align="center" id="field">
		</td>
		<td width="200">
			<div class="message" id="messageLog"></div>
			<div id="messagefield">
				<label>メッセージ入力：</label><br>
				<input name="mess" id="mess" type="text" tabindex="1" class="mess"><br>
				更新秒数 
				<select name="load">
					<option value="10">10</option>
					<option value="15">15</option>
					<option value="30" selected>30</option>
					<option value="45">45</option>
					<option value="60">60</option>
					<option value="100">100</option>
				</select>
				<input type="button" value="発言" onclick="sendData('regist');">
				<br>
				<a href="./etc/help.html#kyoyu" class="jTip" id="100" name="共有掲示板" target="_brank">共有掲示板について</a>
				<table width="200" border="1" cellpadding="1" cellspacing="0" bgcolor="#FFFFFF">
				<tr><td>
				<div align="center" style="width: 200px; height: 400px; overflow: scroll;">
<table border="0" cellpadding="5">
<script>BbsPath='http://duel.wktk.so/cgi3/bbs-u3/';</script><div id="BbsScript"><a href="http://web-sozai.seesaa.net/">ページ埋め込み型掲示板</a></div><script src="http://duel.wktk.so/cgi3/bbs-u3/bbs.js" type="text/javascript" charset="utf-8" async="async" defer="defer"></script>
</table>
</div>
</td>
</tr>
</table>
			</div>
		</td>
	</tr>
	</table>
</form>
</body>
</html>
EOM
	exit;
}

sub field {
	for my $i(1..2){
		&del_null(*hand, $i);
		&del_null(*deck, $i);
		&del_null(*boti, $i);
		&del_null(*gear, $i);
		&del_null(*psychic, $i);
	}
#	print "Content-Type: text/html; charset=UTF-8\n\n";
	print "Content-Type: text/html\n\n";
	print qq|<table border="0" cellpadding="0" cellspacing="20">\n<tr align="center"><td colspan="2">\n|;
	&view_field($u_side2, 3);
	print qq|</td></tr>\n<tr align="center"><td colspan="2">\n|;
	&view_field($u_side2, 2);
	print "</td></tr>\n";
	&view_gear($u_side2) if -1 < $#{$gear[$u_side2]};
	print qq|<tr align="center"><td>\n|;
	&view_field($u_side2, 1);
	print "</td><td>\n";
	&view_field($u_side2, 0);
	print "</td></tr>\n</table>\n";
	&field_sel;
	print qq|<table border="0" cellpadding="0" cellspacing="20">\n<tr align="center"><td>\n|;
	&view_field($u_side, 0);
	print "</td><td>\n";
	&view_field($u_side, 1);
	print qq|</td></tr>\n<tr align="center"><td colspan="2">\n|;
	&view_field($u_side, 2);
	print "</td></tr>\n";
	&view_gear($u_side) if -1 < $#{$gear[$u_side]};
	print qq|<tr align="center"><td colspan="2">\n|;
	&view_field($u_side, 3);
	print "</td></tr>\n</table>\n";
	&put_ini unless $read_only;
	undef %F; undef %S;
	&fileunlock($room);
	exit;
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
		next if $gear[$gside][$i] eq "";
		print "<td>";
		if ($gear[$gside][$i] =~ /:/) {
			my @s_gear = split /:/, $gear[$gside][$i];
			print q|<table border="0">|;
			for my $j(0..$#s_gear-1){
				next if $s_gear[$j] eq "";
				print "<tr>\n<td>";
				print qq|<input type="checkbox" name="gsel$gside-$i-$j" value="on"></td>\n<td>| if $S{'m'} !~ /c_shinka_sel|cloth_sel/ && &control_chk;
				print "$c_name[$s_gear[$j]]";
				print "</td>\n</tr>";
			}
			print "</table>\n";
			&view_gear_sub($gside, $s_gear[-1], $gside.'-'.$i.'-'.$#s_gear, "gsel");
		} else {
			&view_gear_sub($gside, $gear[$gside][$i], $gside.'-'.$i, "gsel");
		}
		print "</td>\n";
		print "</tr><tr>\n" if $cou % 5 == 4;
		$cou++;
	}
	print "</tr></table>\n";
	print "</td></tr>\n";
}

sub view_gear_sub {
	my ($side, $cno, $k, $str, $flg) = @_;
	if ($str eq "gsel") {
		&view_card($cno,1);
	} else {
		print "<tr>\n<td>";
	}
	if ($S{'m'} eq "c_shinka_sel") {
		printf qq|<input type="radio" name="$str$k" value="on">%s|, $str eq "csel" ? "</td>\n<td>" : "" if $side == $u_side && (&bun_chk($cno, (split /,/, $c_bun[$chudan])) || $c_name[$cno] eq "レオパルド・グローリーソード");
	} elsif ($S{'m'} eq "cloth_sel") {
		printf qq|<input type="radio" name="$str$k" value="on">%s|, $str eq "csel" ? "</td>\n<td>" : "" if $side == $u_side;
	} elsif (&control_chk) {
		printf qq|<input type="checkbox" name="$str$k" value="on">%s|, $str eq "csel" ? "</td>\n<td>" : "";
	}
	if ($str eq "csel" && $flg == 1) {
		print "$c_name[$cno]";
	} elsif ($str eq "csel") {
		&view_card($cno, 4);
	}
	print "</td>\n</tr>" if $str eq "csel";
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
					printf qq|<input type="checkbox" name="csel%s" value="on"></td>\n<td>|, $fno.'-'.$i if (&control_chk && $phase !~ /1|2/) && !($syori[0]);
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


sub status {
	for my $i(1..2){
		$deckno[$i] = @{$deck[$i]};
		$handno[$i] = @{$hand[$i]};
		$botino[$i] = @{$boti[$i]};
		$psychicno[$i] = @{$psychic[$i]};
	}
#	print "Content-Type: text/html; charset=UTF-8\n\n";
	print "Content-Type: text/html\n\n";
	if ($side[1] && $side[2] && !($end_flg) && !($read_only)){
		print qq|ターン：$turn<br>\n|;
		print qq|$pn[$turn2]のターン<br>\n|;
		print qq|【山札】$pn[$u_side]：$deckno[$u_side]／$pn[$u_side2]：$deckno[$u_side2]<br>\n|;
		if (&c_chk("ラグーン・マーメイド", 3)) {
			print qq|【山札の１枚目】<br>\n|;
			print qq|$pn[$u_side]：$c_name[$deck[$u_side][0]]<br>\n|;
			print qq|$pn[$u_side2]：$c_name[$deck[$u_side2][0]]<br>\n|;
		}
		print qq|【手札】$pn[$u_side]：$handno[$u_side]／$pn[$u_side2]：$handno[$u_side2]<br>\n|;
		print qq|【墓地】$pn[$u_side]：$botino[$u_side]／$pn[$u_side2]：$botino[$u_side2]<br>\n|;
		print qq|【次元】$pn[$u_side]：$psychicno[$u_side]／$pn[$u_side2]：$psychicno[$u_side2]<br>\n|;
	}
	my($sec,$min,$hour,$mday,$mon,$year) = localtime($date[$u_side]);
	my $dat1 = sprintf("%02d:%02d",$hour,$min);
	my($vsec,$vmin,$vhour,$vmday,$vmon,$vyear) = localtime($date[$u_side2]);
	my $dat2 = sprintf("%02d:%02d",$vhour,$vmin);
	print qq|【最終アクセス】<br>\n|;
	print qq|<a href="javascript:tb_show('','taisen.cgi?&amp;mode=prof&amp;chara=$side[$u_side]&amp;keepThis=true&amp;TB_iframe=true')">$pn[$u_side]</a>\[$side[$u_side]\]：$dat1<br>\n| if $side[$u_side];
	print qq|<a href="javascript:tb_show('','taisen.cgi?&amp;mode=prof&amp;chara=$side[$u_side2]&amp;keepThis=true&amp;TB_iframe=true')">$pn[$u_side2]</a>\[$side[$u_side2]\]：$dat2\n| if $side[$u_side2];
	print qq|<script>\n|;
	if (!$read_only && (!($side[1]) || !($side[2])) && !$end_flg) {
		print qq|\$("#roommsg").show();|;
	} else {
		print qq|\$("#roommsg").hide();|;
	}
	if ($read_only || !($side[1]) || !($side[2]) || $end_flg) {
		print qq|\$("#console, #surrender, #dropadmit").hide(); \$("#kansen").show(); side1 = "$side[1]"; side2 = "$side[2]";\n|;
	} else {
		print qq|\$("#console, #surrender, #dropadmit").show(); \$("#kansen").hide(); side1 = "$side[1]"; side2 = "$side[2]";\n|;

#		if ($phase == 4 && $turn2 == $u_side) {
#			print qq|\$("#phase").val("ターン終了");\n|;
#		} else {
#			print qq|\$("#phase").val("次のフェイズへ");\n|;
#		}
		print  qq|var \$target = \$("option", "select[name=parea]");\n|;
		printf qq|var \$opt = \$target.get()[%d];\n|, $phase == 2 ? 0 : 1;
		print  qq|\$opt.selected = true;\n|;
	}
	print "end_flg = \"" . ($end_flg ? "1" : "0") . "\";\n";
	print "u_side = \"$u_side\"; u_side2 = \"$u_side2\";\n";
	print qq|\$("#messagefield").hide();\n| if $read_only && !$admin;
	print qq|</script>\n|;
	&fileunlock($room);
	exit;
}

sub cardlist {
	my $vside = (($u_side - 1) xor $F{'vside'}) + 1;
	my $varea = $F{'varea'} || 0;
	&regist("","$pn[$u_side]は相手の手札を見た！", "system") if $varea == 0 && $vside eq $u_side2;
	&regist("",sprintf ("$pn[$u_side]は%sの山札を見た！", $vside == $u_side2 ? "相手" : "自分"), "system") if $varea == 2;
	&regist("",sprintf ("$pn[$u_side]は%sのGRゾーンを見た！", $vside == $u_side2 ? "相手" : "自分"), "system") if $varea == 4;
	&del_null(sprintf("%s", $varea == 0 ? *hand : $varea == 1 ? *boti : $varea == 2 ? *deck : *psychic), $vside);
	my @tmp = $varea == 0 ? @{$hand[$vside]} : $varea == 1 ? @{$boti[$vside]} : @{$deck[$vside]};
	print "Content-Type: text/html; charset=UTF-8\n\n";
	printf "%s$pn[$vside]の%s%s\n", $#tmp < 0 ? "" : "<strong>", $varea == 0 ? "手札": $varea == 1 ? "墓地": $varea == 2 ? "山札" : "超次元ゾーン", $#tmp < 0 ? "は０です":"</strong>";
	if (0 <= $#tmp) {
		my $cou = 0;
		foreach my $cno(@tmp) {
			my $bun = join "", map { $_ = sprintf qq|<span class="%s">$_</span>|, $_ eq "光" ? "hikari": $_ eq "水" ? "mizu": $_ eq "闇" ? "yami": $_ eq "火" ? "hi" : $_ eq "自然" ? "sizen" : "zero"; } (split /\//, (&bun_sub($cno))[0]);
			print  qq| <br><input type="checkbox" name="sel$cou" value="$cno">\n|;
			printf qq| $bun　<a href="#" onclick="tb_show('','duel.cgi?&amp;mode=cardview&amp;j=$cno&amp;room=$room&amp;keepThis=true&amp;TB_iframe=true&amp;height=300&amp;width=700'); return false;">$c_name[$cno]</a>/$c_mana[$cno]%s\n|, $c_evo[$cno] == 4 ? "/進化GV" : 4 < $c_evo[$cno] ? "/進化Ｖ" : $c_evo[$cno] ? "/進化" : "";
			$cou++;
	        }
	}
	&fileunlock($room);
	exit;
}

sub mess {
	open DB, "room/".$roomst.$room."_log.cgi";
	my $cou = 0;
	my $pstr = "";
	while (<DB>) {
		my ($msgman, $msg, $status) = split /<>/, $_;
		if ($status =~ /secret/) {
			next if substr($status, -1, 1) != $u_side || $read_only;
			$pstr .= qq|<span class="secret">$msg</span><br>\n|;
			$msg = "";
		}
		$pstr .= $status eq "system" ? qq|<span class="system">$msg</span><br>|
		       : $status eq "tap" ? qq|<span class="taped">$msg</span><br>|
		       : $status eq "admin" ? qq|<span class="admin">$msgman ＞ $msg</span><br>|
		       : $status eq "message" ? qq|<span class="message">$msgman ＞ $msg</span><br>|
		       : $status eq "message1" ? qq|<span class="message1">$msgman ＞ $msg</span><br>|
		       : $status eq "message2" ? qq|<span class="message2">$msgman ＞ $msg</span><br>|
		       : qq|<span class="system">$msg</span><br>| if $msg;
		$cou++;
	}
	close DB;
#	print "Content-Type: text/html; charset=UTF-8\n\n";
	print "Content-Type: text/html\n\n";
	print "$pstr";
	&fileunlock($room);
	exit;
}

sub view_card {
	local ($cno, $area) = @_;
	&c_color($cno);
	if ($area == 2 && $fld[$fno] !~ /\-s$/) { &view_card2; } else { &view_card1; }
}

sub view_card1 {
	my $tmpst = $area == 0 && $phase !~ [12] && $v_side == $u_side && !($chudan_flg) && !($read_only)
		? sprintf qq|<input type="checkbox" name="block$fno" id="block$fno" value="on"%s onclick="stopBubble(event);sendData('block_flg', this);">ブロッカー\n|, $f_block[$fno] ? " checked" : ""
		: $area == 0 && $f_block[$fno] ? "ブロッカー\n" : "";
	printf qq|<div class="$bgc"%s>\n|, $area =~ /[03]/ ? qq| id="fsel$fno" onclick="sendData('tap', this);"| : "";
	print qq|$c_mana[$cno]/\n| if $area < 2;
	print qq|<a href="#" onclick="stopBubble(event);tb_show('','duel.cgi?&amp;mode=cardview&amp;j=$cno&amp;room=$room&amp;keepThis=true&amp;TB_iframe=true&amp;height=300&amp;width=700')">$c_name[$cno]</a>\n|;
	print qq|<span class="center">$c_pow[$cno]</span>\n| if $area == 0;
	print qq|<span class="center">$syuzoku</span>\n| if $area =~ /[03]/;
	print qq|<span class="center">$tmpst</span>\n| if $tmpst ne "";
	print qq|<span class="center">$bun</span>\n| if $bgc eq "rainbow";
	print "</div>\n";
}

sub view_card2 {
	print qq|<div class="shield">\n|;
	printf "%d\n", $fno - $fw3[$v_side][0] + 1;
	print  "</div>\n";
}

sub view_god {
	my ($fno, $area) = @_;
	my @god = split /-/, $fld[$fno];
	print qq|<table border="1" cellpadding="0" class="god">\n|;
	print qq|<tr>\n|;
	foreach my $i (0 .. $#god) {
		print "<td>\n";
		&view_card($god[$i], $area);
		printf qq|<input type="checkbox" name="fsel%s" value="on">\n|, $fno.'-'.$i if (&control_chk && $phase !~ /1|2/) && !($v_side == $u_side && (&ex_chk($fno, \@{$fw1[$u_side]})) && !($f_tap[$fno]) && $btl[4] eq "anonymous") && !($syori[0]);
		print "</td>\n";
	}
	print "</tr>\n";
	print "</table>\n";
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
	my @butstr = split /::/, $S{'o'};
	print <<"EOM";
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
					my $cno = $S{'p'} ? $res : $fld[$res];
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
	print qq|<input type="button" value="$butstr[0]" name="$S{'m'}" id="run_select" onclick="sendData('$S{m}',this);">|;
	print qq|　<input type="button" value="$butstr[1]" name="$S{'m'}" id="not_select" onclick="sendData('$S{m}',this); return false;">| if $butstr[1];
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
	return 0 if $read_only || !($side[1]) || !($side[2]);
	&syori_p_set;
	return 0 if ($S{'s'} ne "" ? $S{'s'} : $turn2) ne $u_side;
	return 1;
}

sub syori_p_set {
	return if $syori[0] eq "";
	undef %S;
	map { $S{$1} = $2 if $_ =~ /(.)-(.+)/ } split /<>/, $syori[0];
}

sub regist {
	my ($msgman, $msg, $status) = @_;
	unless($msg) {
		&fileunlock($room);
		exit;
	}
#	my $lfh = &filelock($room) || &error("ファイルロック中です。");
	open  IN, "room/".$roomst.$room."_log.cgi";
	@lines = <IN>;
	close IN;
	unshift @lines, "$msgman<>$msg<>$status<>\n";
	open  OUT, ">room/".$roomst.$room."_log.cgi" || &error("ログファイルに書き込めません");
	print OUT @lines;
	close OUT;
#	&fileunlock($lfh);
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
	$room = $F{'room'};
	($id = $F{'id'}) =~ s/\.|\///g;
	($pass = $F{'pass'}) =~ s/\.|\///g;
	&error("IDが入力されていません。") if !($id) && ($F{'mode'} !~ /cardview|prof/);
	&error("パスワードが入力されていません。") if !($pass) && ($F{'mode'} !~ /cardview|prof/);
	if ($F{'mess'}) {
		$F{'mess'} =~ s/</&lt\;/g;
		$F{'mess'} =~ s/>/&gt\;/g;
	}
}