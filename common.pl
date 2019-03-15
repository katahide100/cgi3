sub access_chk {	# 強制退室チェック
	$timed_up = 0;
	if(($side[1] && $date[$u_side2] && $natime) && $side[2] && !($read_only)){
		if(!(&control_chk()) || (&control_chk() && $F{'mode'} ne "field") || ($room =~ /^t/)) {
			$tourtime[$u_side] += $times - $date[$u_side] unless (&control_chk());
			$date[$u_side] = $times;
		}

		# 強制退室処理
		if(($room =~ /^t/) && ($times - $start_date > 60 * 60 * 24)) {
			&s_mes("規定時刻になったため、デュエルを終了します！");

			if($tourtime[$u_side] < $tourtime[$u_side2]) {
				&s_mes("待ち時間が少なかったため、$pn[$u_side]さんは敗北になります。");
				$lp[$u_side] = 0;
				$lp[$u_side2] = 1;
				$sr[$u_side] = 1;
				$sr[$u_side2] = 0;
				&end_game;
			} elsif($tourtime[$u_side] > $tourtime[$u_side2]) {
				&s_mes("待ち時間が少なかったため、$pn[$u_side2]さんは敗北になります。");
				$lp[$u_side] = 1;
				$lp[$u_side2] = 0;
				$sr[$u_side] = 0;
				$sr[$u_side2] = 1;
				&end_game;
			}
		}
	} elsif((!$side[1] || !$side[2]) && !($read_only)) {
		$tourtime[$u_side] += $times - $date[$u_side];
		$date[$u_side] = $times;
	}
}

sub deny {			# 禁止ID、プロクシのチェック
	map { &error("あなたのIDは対戦を禁止されています") if $id =~ /^$_/ } @deny_id;
	if ($deny_proxy) {
		while (my ($envkey, $envvalue) = each(%ENV)) {
			&error("プロクシ経由での対戦は禁止されてます") if $envkey =~ /proxy/i || $envvalue =~ /proxy/i;
		}
	}
}

sub all_clr {
	my $sd = $_[0] ? $_[0] : "";
	undef @hand; undef @boti; undef @deck; undef @gear; undef @psychic; undef @gr;
	undef @fld; undef @f_tap; undef @f_block; undef @f_drunk; undef @f_cloth; undef @shinka; undef @res; undef @res2; undef @syori; undef @vor; undef @syu_add; undef @magic;
	&battle_clr;
	$lp[$sd] = $side[$sd] = $pn[$sd] = $pass[$sd] = $dnam[$sd] = $usedeck[$sd] = $date[$sd] = "" if $sd ne "";
#	$phase = $turn = $turn2 = $skip_flg = $boru_cnt = $vor_cnt = $end_flg = $janken[1] = $janken[2] = "";
	$phase = $turn = $turn2 = $skip_flg = $boru_cnt = $vor_cnt = $janken[1] = $janken[2] = "";
}

sub block_flg {
#	map { $f_block[$_] = "" } (@{$fw1[1]}, @{$fw1[2]});
	map { $flg = $_; $_ =~ s/^block//; $f_block[$_] = $F{$flg} eq "on" ? "1" : ""; } grep /^block/, keys(%F);
	map { $f_block[$_] = "1" } @{$fw1[2]} if &c_chk("蒼黒の知将ディアブロスト", 1);
	map { $f_block[$_] = "1" } @{$fw1[1]} if &c_chk("蒼黒の知将ディアブロスト", 2);
	map { $f_block[$_] = "1" if (&k_chk($fld[$_], 12) && &c_chk("金色の精霊クロスヘイム", 1)) || (&syu_chk($fld[$_], 89) && &c_chk("天雷の龍聖ロレンツオ４世", 1)) } @{$fw1[1]} if &c_chk("金色の精霊クロスヘイム", 1) || &c_chk("天雷の龍聖ロレンツオ４世", 1);
	map { $f_block[$_] = "1" if (&k_chk($fld[$_], 12) && &c_chk("金色の精霊クロスヘイム", 2)) || (&syu_chk($fld[$_], 89) && &c_chk("天雷の龍聖ロレンツオ４世", 2)) } @{$fw1[2]} if &c_chk("金色の精霊クロスヘイム", 2) || &c_chk("天雷の龍聖ロレンツオ４世", 2);
}

sub start {
	&deny;
	my $cf = 0;
	my $mn = 0;
	if($F{'mode'} eq 'duel') {
		$room = int($room);
		&error("不正な部屋番号です") unless(($room > 0) && ($room <= $heyakazu));
		&get_ini;
		&error("使用中 $pn[1] VS $pn[2]") if ($side[1]) && ($side[2]);
		$dendou = $F{'dendou'} if !($side[1]) && !($side[2]);
		$roomid = &make_id() if !($side[1]) && !($side[2]);
		$duelid = $F{'duelid'} if !($side[1]) && !($side[2]);
		$choose = $F{'choose'} if !($side[1]) && !($side[2]);
		&error("一言メッセージが長すぎます。50字以内にしてください") if length($F{'message'}) > 150;
		$message = $F{'message'} if !($side[1]) && !($side[2]);
		unless(grep(/^$room$/, @beginner) && ($id eq $duelid) && ($choose == 0)) {
			&error("同じID同士の対戦はできません") if ($side[1] && $id eq $side[1] && !($side[2])) || ($side[2] && $id eq $side[2] && !($side[1]));
			&error("同じIPアドレス同士の対戦はできません") if (($ip[1] && $ENV{'REMOTE_ADDR'} eq $ip[1] && !($side[2]) || ($ip[2] && $ENV{'REMOTE_ADDR'} eq $ip[2] && !($side[1]))) && ($ENV{'REMOTE_ADDR'} ne '127.0.0.1'));
		}
		$u_side = !($side[1]) ? 1 : 2;
		&niheya_chk;
	} else {
		%T = ();
		&filelock("tr");
		chmod 0666, "./tour/part.dat";
		open(TRT, "./tour/part.dat");
		while(<TRT>){ chop; ($KEY,$VAL) = split(/\t/); $T{$KEY} = $VAL; }
		close(TRT);
#		chmod 0000, "./tour/part.dat";
		&error("申し訳ありませんが、この大会は既に満員です") if(($T{'remain'} <= 0) && ($T{'accept'} == 0));
		&error("この大会に参加するには、指定されたパスワードが必要です") if(($T{'tpass'} ne '') && ($F{'tpass'} eq ''));
		&error("参加するためのパスワードが間違っています") if(($T{'tpass'} ne '') && ($F{'tpass'} ne $T{'tpass'}));
		my($tl) = 0;
		$dendou = $T{'dendou'} if !($side[1]) && !($side[2]);
		if($T{'accept'} == 1) {
			$tl = $T{'number'};
		} else {
			$tl = 2 ** $T{'scale'} * 2 - $T{'remain'};
		}
		for(my($i) = 1; $i <= $tl; $i ++) {
			if($id eq $T{"p${i}id"}) {
				$cf = $i;
				last;
			}
		}
		if($cf > 0) {
			$mn = $cf;
		} elsif($T{'accept'} == 1) {
			$mn = $T{'number'} + 1;
		} else {
			$mn = 2 ** $T{'scale'} * 2 - $T{'remain'} + 1;
		}
	}
	&pfl_read($id);
	&pass_chk;
	&error("あなたのIDは対戦規制をかけられています。<BR>悪いことをした覚えがないのにこのエラーが出た場合は、<BR>管理者まで連絡してください。") if($P{"deny"});
	my $use = $F{'usedeck'};
	&error("デッキを読み込むことができません。選択し直してください。") if !($P{"deck$use"});
	($dummy,$dcond,$dcondp,$dcondg) = split(/-/,$P{"deck$use"});
	my @odeck = split(/,/,$dcond);
	&error("デッキが40枚になっていません。デッキを作り直してください。") if $#odeck != 39;

	foreach my $card (@odeck) {
		&error("対応していないカードが入っています。デッキを作り直してください") if($card > $#c_name);
	}

	my @odeckp = split(/,/,$dcondp);
	&error("超次元カードが15枚以上入っています。デッキを作り直してください。") if $#odeckp > 14;

	my @odeckg = split(/,/,$dcondg);
	&error("GRカードが0枚もしくは12枚ではありません。デッキを作り直してください。$#odeckg") if($#odeckg != -1 && $#odeckg != 11);

	foreach my $card (@odeckp) {
		&error("対応していないカードが入っています。デッキを作り直してください") if($card > $#c_name);
	}

	foreach my $card (@odeckg) {
		&error("対応していないカードが入っています。デッキを作り直してください") if($card > $#c_name);
	}

	if($F{'mode'} eq 'duel') {
		$black = $P{'black'} if !($side[1]) && !($side[2]);
		$white = $P{'white'} if !($side[1]) && !($side[2]);
		if (($side[1]) || ($side[2])) {
			if ($P{'black'} ne '') {
				my(@b_list_my) = split(/\,/, $P{'black'});
				&error("自分のブラックリストに載っている相手とは対戦できません") if(grep(/^$side[1]$/, @b_list_my) || grep(/^$side[2]$/, @b_list_my));
			}
			if ($black ne '') {
				my(@b_list_room) = split(/\,/, $black);
				&error("自分のIDが相手のブラックリストに入っているため対戦できません") if(grep(/^$id$/, @b_list_room));
			}
			if(($choose == 2) && ($white ne '')) {
				my(@w_list) = split(/\,/, $white);
				&error("自分のIDが相手のホワイトリストに登録されていないため対戦できません") unless(grep(/^$id$/, @w_list));
			}
		}
		if($choose == 1) {
			&error("パスワードは8文字以内にしてください。") if((length($F{'duelid'}) > 8) && !($side[1]) && !($side[2]));
			&error("パスワードには半角英数字のみが使用可能です。") if(($duelid ne '') && ($F{'duelid'} !~ /^[A-Za-z0-9]*$/) && !($side[1]) && !($side[2]));
			&error("パスワードが異なっています。入室できません。") if (($duelid ne '') && ($duelid ne $F{'duelpass'}) && (($side[1]) || ($side[2])));
		} elsif($choose == 3) {
			&error("減算ポイントが指定されていません。") if ($duelid eq '');
			$minuscard = 0;
			foreach my $i(0 .. $#odeck){
				if(grep(/^$odeck[$i]$/,@minus10)) {
					$minuscard += 10;
				} elsif(grep(/^$odeck[$i]$/,@minus5)) {
					$minuscard += 5;
				} elsif(grep(/^$odeck[$i]$/,@minus3)) {
					$minuscard += 3;
				} elsif(grep(/^$odeck[$i]$/,@minus1)) {
					$minuscard += 1;
				} elsif(grep(/^$odeck[$i]$/,@plus1)) {
					$minuscard -= 1;
				}
			}
			$minuscard = 0 if($minuscard < 0);
			&error("減算ポイントが ${duelid}pを超えています。デッキを作り直してください<BR><BR>(現在のポイント： $minuscard)") if ($minuscard > $duelid);
		} else {
			unless(grep(/^$room$/, @beginner)) {
				&error("練習部屋以外で対戦者IDを自身のIDに設定することはできません。") if(($F{'duelid'} eq $id) && !($side[1]) && !($side[2]));
			}
			open(LOG,">>tmperrorlog.dat");
			print LOG "$id > $F{'duelid'}\n";
			close(LOG);
			&error("対戦者IDの形式が正しくありません。<BR>半角英字の大文字３つ、数字５つにしてください。<BR>例：ABC01234<BR><BR><font color=\"red\">入力されたID：$F{'duelid'}</font>") if(($duelid ne '') && ($F{'duelid'} !~ /^[A-Z]{3}[0-9]{5}[am]{0,1}$/) && !($side[1]) && !($side[2]));
			&error("対戦者が予約された部屋です。入室できません。") if (($duelid ne '') && ($duelid ne $id) && (($side[1]) || ($side[2])));
		}
		&error("先に部屋へ入った人が居ます。入室をやり直してください。") if ((($side[1]) || ($side[2])) && ($F{'chara'} == 0));

		if (!($side[1]) && !($side[2])) {
			if($F{'usegroup'} > 0) {
				$tempg = $P{"group$F{'usegroup'}"};
				($dummy,$dgroup) = split(/-/,$tempg);
			} else {
				$dgroup = "";
			}
			$P{'usegroup'} = $F{'usegroup'};
		}
	}

	if (($dendou == 1) || ($dendou == 4)) {
		undef(%CHK);
		undef(%CMB);
		if($dendou == 4) {
			my(%odeck_hash) = ();
			foreach my $card (@odeck) {
				$odeck_hash{$card} ++;
			}
			my(@zerodeck_list) = ();
			for(my($i) = 0; $i <= $#zerodeck; $i ++) {
				foreach my $card (@{$zerodeck[$i]}) {
					$zerodeck_list[$i]{$card} ++;
				}
			}
			my($zero_flag) = 0;
			for(my($i) = 0; $i <= $#zerodeck; $i ++) {
				my($zero_diff) = 0;
				foreach my $card (keys(%odeck_hash)) {
					$zero_diff += $odeck_hash{$card} - $zerodeck_list[$i]{$card};
				}
				if($zero_diff <= 10) {
					$zero_flag = 1;
					last;
				}
			}
			&error("ゼロデッキ対象外です") if($zero_flag == 0);
		}
		foreach my $card(@odeck){
			if(grep(/^$card$/,@premium)){
				$buffer .= "<FONT color=\"red\">$c_name[$card]</FONT><BR>";
				$red_flag = 1;
			} elsif(grep(/^$card$/,@dendou)){
				$CHK{$card}++;
				if ($CHK{$card} > 1) {
					&error("殿堂入りカードが２枚以上入っています。デッキを作り直してください。");
					$buffer .= "<FONT color=\"brown\">$c_name[$card]</FONT><BR>";
				} else {
					$buffer .= "<FONT color=\"brown\">$c_name[$card]</FONT><BR>";
				}
			} else {
				$buffer .= "<FONT color=\"black\">$c_name[$card]</FONT><BR>";
			}
			foreach(@combi) {
				for(my($i) = 0; $i <= 1; $i ++) {
					if($card == ${$_}[$i]) {
						$CMB{$card}++;
						&error("プレミアム殿堂コンビ入りカードが入っています。デッキを作り直してください。") if($CMB{${$_}[1 - $i]} > 0);
#						last;
					}
				}
			}
		}
		$buffer = "プレミアム殿堂入りカードが入っています。デッキを作り直してください。<BR>$buffer" if($red_flag);
		$buffer = "殿堂入りカードが２枚以上入っています。デッキを作り直してください。<BR>$buffer" if($yellow_flag);
		&error($buffer) if($red_flag || $yellow_flag);
	} elsif ($dendou == 10) {
		undef(%CHK);
		my $red_flag = 0;
		my $yellow_flag = 0;
		my $cnt = 0;
		my $buffer = '<BR>';
		foreach my $card(@odeck){
			if(grep(/^$card$/, 770, 1334, 1456, 441, 1237, 531, 1076, 1404, 1156, 959, 758, 661, 474, 910, 1127)) {
				$buffer .= "<FONT color=\"red\">$c_name[$card]</FONT><BR>";
				$red_flag = 1;
			} elsif(grep(/^$card$/, 118, 174, 191, 232, 256, 260, 474, 602, 661, 770, 986, 931, 670, 57, 1046, 816, 778, 476, 785, 838, 1171)) {
				$CHK{$card}++;
				if ($CHK{$card} > 1) {
					$buffer .= "<FONT color=\"brown\">$c_name[$card]</FONT><BR>";
					$yellow_flag = 1;
				} else {
					$buffer .= "<FONT color=\"brown\">$c_name[$card]</FONT><BR>";
				}
			} else {
				$buffer .= "<FONT color=\"black\">$c_name[$card]</FONT><BR>";
			}
			$cnt ++;
		}
		$buffer = "プレミアム電動入りカードが入っています。デッキを作り直してください。<BR>$buffer" if($red_flag);
		$buffer = "電動入りカードが２枚以上入っています。デッキを作り直してください。<BR>$buffer" if($yellow_flag);
		&error($buffer) if($red_flag || $yellow_flag);
	} elsif ($dendou == 11) {
		undef(%CHK);
		my $red_flag = 0;
		my $yellow_flag = 0;
		my $cnt = 0;
		my $buffer = '<BR>';
		foreach my $card(@odeck){
			if(grep(/^$card$/, 770,1237,661,474,910,548,931,57,1045,1046,430,1601,884,1068,1470,531,168,924,1171,1127)) {
				$buffer .= "<FONT color=\"red\">$c_name[$card]</FONT><BR>";
				$red_flag = 1;
			} elsif(grep(/^$card$/, @dendou, 1576,1437,1350,1598,442,1407,838)) {
				$CHK{$card}++;
				if ($CHK{$card} > 1) {
					$buffer .= "<FONT color=\"red\">$c_name[$card]</FONT><BR>";
					$yellow_flag = 1;
				} else {
					$buffer .= "<FONT color=\"brown\">$c_name[$card]</FONT><BR>";
				}
			} else {
				$buffer .= "<FONT color=\"black\">$c_name[$card]</FONT><BR>";
			}
			$cnt ++;
		}
		$buffer = "プレミアム殿堂入りカードが入っています。デッキを作り直してください。<BR>$buffer" if($red_flag);
		$buffer = "殿堂入りカードが２枚以上入っています。デッキを作り直してください。<BR>$buffer" if($yellow_flag);
		&error($buffer) if($red_flag || $yellow_flag);
	} elsif ($dendou == 2 || $dendou == 3) {
		my @sgl = ();
		require "series.lib";
		undef %exists;
		if($dendou == 2) {
			foreach (@{$ser[100]}) { $exists{$_} = 1; }
		} elsif($dendou == 3) {
			foreach (@{$ser[101]}) { $exists{$_} = 1; }
		}
		my $ngflag = 0;
		my @nglist = ();
		foreach my $card(@odeck){
			if($exists{$card}) {
				push(@nglist, 0);
			} else {
				push(@nglist, 1);
				$ngflag = 1;
			}
		}
		if($ngflag) {
			my $buffer = "";
			my $i = 0;
			foreach my $card(@odeck){
				if($nglist[$i]) {
					$buffer .= "<FONT color=\"red\">$c_name[$card]</FONT><BR>\n";
				} else {
					$buffer .= "$c_name[$card]<BR>\n";
				}
				$buffer .= "</TD><TD>\n" if($i == 19);
				$i ++;
			}
			if($dendou == 2) {
			&error(<<"EOM");
ＡＧ環境非対応のカードが入っています。デッキを作り直してください。<BR>
<BR>
<TABLE border="1">
<TR><TD>
$buffer
</TD></TR>
</TABLE>
EOM
			} elsif($dendou == 3) {
			&error(<<"EOM");
ＳＧＬ環境非対応のカードが入っています。デッキを作り直してください。<BR>
<BR>
<TABLE border="1">
<TR><TD>
$buffer
</TD></TR>
</TABLE>
EOM
			}
		}
	}
	if($F{'mode'} eq 'tourjoin') {
		@p_fame = split(/\,/, $T{'p_fame'});
		@fame = split(/\,/, $T{'fame'});
		$dendou = 0;
		foreach my $card(@odeck){
			foreach my $p_fame(@p_fame){
				if ($card == $p_fame) {
				&error("$T{'title'} 追加Ｐ殿堂入りカードが入っています。デッキを作り直してください。");
				}
			}
		}
		my %spc = ();
		foreach my $card(@odeck){
			foreach my $fame(@fame){
				if ($card == $fame) {
					$spc{$card} ++;
					&error("$T{'title'} 追加殿堂入りカードが２枚以上入っています。デッキを作り直してください。") if $spc{$card} > 1;
				}
			}
		}

		$minuscard = 0;
		foreach my $i(0 .. $#odeck){
			if(grep(/^$odeck[$i]$/,@minus10)) {
				$minuscard += 10;
			} elsif(grep(/^$odeck[$i]$/,@minus5)) {
				$minuscard += 5;
			} elsif(grep(/^$odeck[$i]$/,@minus3)) {
				$minuscard += 3;
			} elsif(grep(/^$odeck[$i]$/,@minus1)) {
				$minuscard += 1;
			} elsif(grep(/^$odeck[$i]$/,@plus1)) {
				$minuscard -= 1;
			}
		}
		$minuscard = 0 if($minuscard < 0);
		&error("減算ポイントが$T{'point'}pを超えています。デッキを作り直してください<BR><BR>(現在のポイント： $minuscard)") if ($minuscard > $T{'point'} && $T{'point'} >= 0);
	}

	if($F{'mode'} eq 'duel') {
		foreach my $card(@odeck){
			if($dgroup ne '') {
				if(grep(/^$card$/,split(/,/,$dgroup))){
					&error("使用禁止に設定されているカードが含まれています。デッキを作り直してください。");
				}
			}
		}

		@{$deck[$u_side]} = @odeck;
		@{$psychic[$u_side]} = @odeckp;
		@{$gr[$u_side]} = @odeckg;
		&shuffle(*deck,$u_side);
		&shuffle(*gr,$u_side);
		$side[$u_side] = $id;
		$ip[$u_side] = $ENV{'REMOTE_ADDR'};
		$pn[$u_side] = $P{'name'};
		$pass[$u_side] = $P{'pass'};
		if($u_side == 1) {
			$nid1 = $side[$u_side];
			$nnm1 = $pn[$u_side];
		} elsif($u_side == 2) {
			$nid2 = $side[$u_side];
			$nnm2 = $pn[$u_side];
		}
#		$dnam[$u_side] = $dnam;
		$drank[$u_side] = $P{'drank'};
		$date[$u_side] = $times;
		$sur_flg[$u_side] = 0;
		$P{'usedeck'} = $usedeck[$u_side] = $use;
		&s_mes("$pn[$u_side]さんが入室しました。(IP: $ENV{'REMOTE_ADDR'})");
	#	&filelock;
		$P{'age'} = $F{'age'};
		&pfl_write($id);
	#	&fileunlock;
		if(!($side[1]) || !($side[2])){
			&put_ini;
			if(grep(/^$room$/, @beginner) && ($id eq $duelid) && ($choose == 0)) {
				print "Content-type: text/html\n\n";
				print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
	"http://www.w3.org/TR/REC-html40/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<meta http-equiv="Pragma" content="no-cache">
	<link rel="stylesheet" href="$css/duel.css" type="text/css">
	<title>$title</title>
<script type="text/javascript"><!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.submit();
	}
// --></script>
</head>
<body>
	<div align="center">
		<h1>$title</h1>
<form action="taisen.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
入室処理は正常に完了しました。<BR>
引き続き、相手用のデッキを選んで再び入室してください。<BR>
<BR>
[<A href="javascript:sForm('');">戻る</A>]
EOM
				&fileunlock($room);
				&footer;
			}
		} else {
			&start2;
		}
	} else {
		if($F{'mode'} eq 'tourcancel') {
			if($cf > 0) {
				my($tmpnum) = 0;
				if($T{'accept'} == 1) {
					$tmpnum = $T{'number'};
				} else {
					$tmpnum = 2 ** $T{'scale'} * 2 - $T{'remain'};
				}
				for(my($i) = 1; $i <= $tmpnum; $i ++) {
					if($cf < $i) {
						$j = $i - 1;
						$T{"p${j}id"} = $T{"p${i}id"};
						$T{"p${j}pass"} = $T{"p${i}pass"};
						$T{"p${j}name"} = $T{"p${i}name"};
						$T{"p${j}deck"} = $T{"p${i}deck"};
						$T{"p${j}win"} = $T{"p${i}win"};
					}
				}
				delete($T{"p${tmpnum}id"});
				delete($T{"p${tmpnum}pass"});
				delete($T{"p${tmpnum}name"});
				delete($T{"p${tmpnum}deck"});
				delete($T{"p${tmpnum}win"});
				if($T{'accept'} == 0) {
					$T{'remain'} ++;
				} else {
					$T{'number'} --;
				}
				chmod 0666, "./tour/part.dat";
				open(TRT, "> ./tour/part.dat");
				foreach $key(keys(%T)){ print TRT "$key\t$T{$key}\n"; }
				close(TRT);
			}
		} else {
			$P{'usedeck'} = $usedeck[$u_side] = $use;
			$T{"p${mn}id"} = $id;
			$T{"p${mn}pass"} = $P{'pass'};
			$T{"p${mn}name"} = $P{'name'};
			if(defined(@odeckp) && defined(@odeckg)){
				$T{"p${mn}deck"} = join(',', @odeck).'-'.join(',', @odeckp).'-'.join(',', @odeckg);
			} elsif (defined(@odeckp)){
				$T{"p${mn}deck"} = join(',', @odeck).'-'.join(',', @odeckp);
			}else{
				$T{"p${mn}deck"} = join(',', @odeck);
			}
			$T{"p${mn}win"} = 0;
			if($cf == 0) {
				if($T{'accept'} == 0) {
					$T{'remain'} --;
				} else {
					$T{'number'} ++;
				}
			}

			%NT = ();
			$NT{'scale'} = $T{'scale'};
			$NT{'remain'} = $T{'remain'};
			$NT{'p_fame'} = $T{'p_fame'};
			$NT{'fame'} = $T{'fame'};
			$NT{'title'} = $T{'title'};
			$NT{'tpass'} = $T{'tpass'};
			$NT{'type'} = $T{'type'};
			if(($T{'remain'} <= 0) && ($T{'accept'} == 0)) {
				my(@num) = &num_shuf(1 .. 2 ** $T{'scale'} * 2);
				unshift(@num, 0);
				for(my($i) = 1; $i <= 2 ** $T{'scale'}; $i ++) {
					$room = "t${i}";
					for(my($j) = 1; $j <= 2; $j ++) {
						my($pnum) = ($i - 1) * 2 + $j;
						@arr_deck = split(/-/, $T{"p$num[$pnum]deck"});
						@{$deck[$j]} = split(/\,/, $arr_deck[0]);
						@{$psychic[$j]} = split(/\,/, $arr_deck[1]);
						@{$gr[$j]} = split(/\,/, $arr_deck[2]);
						#@{$deck[$j]} = split(/\,/, $T{"p$num[$pnum]deck"});
						&shuffle(*deck,$j);
						&shuffle(*gr,$j);
						$side[$j] = $T{"p$num[$pnum]id"};
						$pass[$j] = $T{"p$num[$pnum]pass"};
						$pn[$j] = $T{"p$num[$pnum]name"};

						$NT{"p${pnum}id"} = $T{"p$num[$pnum]id"};
						$NT{"p${pnum}pass"} = $T{"p$num[$pnum]pass"};
						$NT{"p${pnum}name"} = $T{"p$num[$pnum]name"};
						$NT{"p${pnum}deck"} = $T{"p$num[$pnum]deck"};
						$NT{"p${pnum}win"} = $T{"p$num[$pnum]win"};
						$sur_flg[$j] = 0;
						if($j == 1) { &put_ini; } else { &start2; }
					}
				}
				chmod 0666, "./tour/part.dat";
				open(TRT, "> ./tour/part.dat");
				foreach $key(keys(%NT)){ print TRT "$key\t$NT{$key}\n"; }
				close(TRT);
	#			chmod 0000, "./tour/part.dat";
			} else {
				chmod 0666, "./tour/part.dat";
				open(TRT, "> ./tour/part.dat");
				foreach $key(keys(%T)){ print TRT "$key\t$T{$key}\n"; }
				close(TRT);
	#			chmod 0000, "./tour/part.dat";
			}
		}
		&fileunlock("tr");
		print "Content-type: text/html\n\n";
		print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
	"http://www.w3.org/TR/REC-html40/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<meta http-equiv="Pragma" content="no-cache">
	<link rel="stylesheet" href="$css/duel.css" type="text/css">
	<title>$title</title>
<script type="text/javascript"><!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.submit();
	}
// --></script>
</head>
<body>
	<div align="center">
		<h1>$title</h1>
<form action="taisen.cgi" method="post" name="entrance">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
</form>
EOM
#&error($cf) if($cf > 0);
		if($F{'mode'} eq 'tourcancel') {
			print <<"EOM";
$T{'title'}への登録を取り消しました。<BR><BR>
EOM
		} elsif($cf > 0) {
			print <<"EOM";
$T{'title'}の登録情報の変更が完了しました。<BR><BR>
EOM
		} else {
			print <<"EOM";
$T{'title'}への登録が完了しました。<BR>
大会で使われるデッキは、登録時に選択したデッキです。<BR>
後で変更する場合は、デッキを選択し直して再度登録ボタンを押せば完了されます。<BR>
<BR>
EOM
		}
		print <<"EOM";
[<A href="javascript:sForm('tour');">戻る</A>]
EOM
		&fileunlock($room);
		&footer;
	}
}

sub start2{
	$phase = $turn = $lp[1] = $lp[2] = 1;
	$turn2 = int(rand(2))+1;
	$message = "";

	if($T{'date'}) {
		$start_date = $T{'date'};
	} else {
		$start_date = $times;
	}

	#my @c_data = ();
	#my $cou = 0;
	#my %chk = ();
	#for my $i(1..2){
	#	foreach (@{$deck[$i]}) {
	#		if(!$chk{$_}) {
	#			$c_data[$cou] = "$_\t$c_name[$_]\t$c_bun[$_]\t$c_syu[$_]\t$c_pow[$_]\t$c_mana[$_]\t$c_evo[$_]\t$c_kok[$_]\t$c_tri[$_]\n";
	#			$chk{$_} ++;
	#			$cou ++;
	#		}
	#	}
	#}


	my (@new, %tmp, $lfh, $lin, $data, $out);
	my $cou = 0;
	my @card = grep (!$tmp{$_}++, (@{$deck[1]}, @{$deck[2]}, @{$psychic[1]}, @{$psychic[2]}, @{$gr[1]}, @{$gr[2]}));

	my (%psy_top, %psy_back, %psy_super, %psy_cell);
	eval (join "", (log_read("psychic.txt")));

	my %psychic_back;
	foreach my $cardno (@card) {
		if ($psy_top{$cardno}) {
			$psychic_back{$psy_top{$cardno}} = 1;
		} elsif ($psy_cell{$cardno}) {
			$psychic_back{$psy_cell{$cardno}} = 1;
		}
	}
	foreach my $cardno (keys %psychic_back) {
		push (@card, $cardno);
	}

	foreach (@card) {
		if(!$chk{$_}) {
			$c_data[$cou] = "$_\t$c_name[$_]\t$c_bun[$_]\t$c_syu[$_]\t$c_pow[$_]\t$c_mana[$_]\t$c_evo[$_]\t$c_kok[$_]\t$c_tri[$_]\n";
			$chk{$_} ++;
			$cou ++;
		}
	}

	open(DRC,"> room/duelist${room}_card.cgi") || &error("カードデータを書き込めませんでした");
	foreach (@c_data){ print DRC $_; }
	close(DRC);
	chmod 0666, "room/duelist${room}_card.cgi";

	for my $i(1..2){
		@{$hand[$i]} = ();
		&shuffle(*deck,$i);
		&shuffle(*gr,$i);
		for (my $j=$fw3[$i][0]; $j<$fw3[$i][5]; $j++) {
			$fld[$j] = shift(@{$deck[$i]});
			push(@{$hand[$i]}, shift(@{$deck[$i]}));
		}
	}
	if($room =~ /^t/) {
		&s_mes("$T{'title'}、開始！");
	} else {
		&s_mes("デュエル開始！");
	}
	&s_mes("$pn[$turn2]のターン！");
#	&s_mes("$pn[$turn2]の$phasestr[$phase]。");
	&put_ini;
}

sub end_game_sub {
	undef(%T);
	if($room =~ /^t/) {
		&filelock("tr");
		open(TRT,"tour/part.dat") || &error("大会データが開けません");
		while(<TRT>){ chomp; ($key,$val) = split(/\t/); $T{$key} = $val; }
		close(TRT);
	}
	@p_field1 = ();
	@p_mana1 = ();
	@p_shield1 = ();
	@p_field2 = ();
	@p_mana2 = ();
	@p_shield2 = ();

	for($i = 0; $i <= $#fld; $i ++) {
		if($fld[$i] ne '') {
			if($i < 40) {
				push(@p_mana2, $fld[$i]);
			} elsif(($i >= 40) && ($i < 80)) {
				push(@p_shield2, $fld[$i]);
			} elsif(($i >= 80) && ($i < 160)) {
				push(@p_field2, $fld[$i]);
				if($shinka[$i] ne '') {
					foreach(split(/\-/, $shinka[$i])) {
						push(@p_field2, $_);
					}
				}
				if($f_cloth[$i] ne '') {
					foreach(split(/\-/, $f_cloth[$i])) {
						push(@p_field2, $_);
					}
				}
			} elsif(($i >= 160) && ($i < 200)) {
				push(@p_mana1, $fld[$i]);
			} elsif(($i >= 200) && ($i < 240)) {
				push(@p_shield1, $fld[$i]);
			} elsif(($i >= 240) && ($i < 320)) {
				push(@p_field1, $fld[$i]);
				if($shinka[$i] ne '') {
					foreach(split(/\-/, $shinka[$i])) {
						push(@p_field1, $_);
					}
				}
				if($f_cloth[$i] ne '') {
					foreach(split(/\-/, $f_cloth[$i])) {
						push(@p_field1, $_);
					}
				}
			}
		}
	}

	@p_all1 = ();
	@p_all2 = ();
	for($i = 0; $i <= $#p_field1; $i ++) { push(@p_all1, $p_field1[$i]); }
	for($i = 0; $i <= $#p_mana1; $i ++) { push(@p_all1, $p_mana1[$i]); }
	for($i = 0; $i <= $#p_shield1; $i ++) { push(@p_all1, $p_shield1[$i]); }
	for($i = 0; $i <= $#{$hand[1]}; $i ++) { push(@p_all1, $hand[1][$i]); }
	for($i = 0; $i <= $#{$boti[1]}; $i ++) { push(@p_all1, $boti[1][$i]); }
	for($i = 0; $i <= $#{$deck[1]}; $i ++) { push(@p_all1, $deck[1][$i]); }
	for($i = 0; $i <= $#{$gear[1]}; $i ++) { push(@p_all1, $gear[1][$i]); }
	for($i = 0; $i <= $#{$psychic[1]}; $i ++) { push(@p_all1, $psychic[1][$i]); }
	for($i = 0; $i <= $#{$gr[1]}; $i ++) { push(@p_all1, $gr[1][$i]); }
	for($i = 0; $i <= $#p_field2; $i ++) { push(@p_all2, $p_field2[$i]); }
	for($i = 0; $i <= $#p_mana2; $i ++) { push(@p_all2, $p_mana2[$i]); }
	for($i = 0; $i <= $#p_shield2; $i ++) { push(@p_all2, $p_shield2[$i]); }
	for($i = 0; $i <= $#{$hand[2]}; $i ++) { push(@p_all2, $hand[2][$i]); }
	for($i = 0; $i <= $#{$boti[2]}; $i ++) { push(@p_all2, $boti[2][$i]); }
	for($i = 0; $i <= $#{$deck[2]}; $i ++) { push(@p_all2, $deck[2][$i]); }
	for($i = 0; $i <= $#{$gear[2]}; $i ++) { push(@p_all2, $gear[2][$i]); }
	for($i = 0; $i <= $#{$psychic[2]}; $i ++) { push(@p_all2, $psychic[2][$i]); }
	for($i = 0; $i <= $#{$gr[2]}; $i ++) { push(@p_all2, $gr[2][$i]); }


#	$shieldpoint1 = ($#p_shield1 + 1) * 5 if($sr[1] == 0);
#	$shieldpoint2 = ($#p_shield2 + 1) * 5 if($sr[2] == 0);

	$minuscard1 = 0;
	$minuscard2 = 0;

	for($i = 0; $i <= $#p_all1; $i ++) {
		if(grep(/^$p_all1[$i]$/,@minus10)) {
			$minuscard1 += 10;
		} elsif(grep(/^$p_all1[$i]$/,@minus5)) {
			$minuscard1 += 5;
		} elsif(grep(/^$p_all1[$i]$/,@minus3)) {
			$minuscard1 += 3;
		} elsif(grep(/^$p_all1[$i]$/,@minus1)) {
			$minuscard1 += 1;
		} elsif(grep(/^$p_all1[$i]$/,@plus1)) {
			$minuscard1 -= 1;
		}
	}
	$minuscard1 = 0 if($minuscard1 < 0);
	for($i = 0; $i <= $#p_all2; $i ++) {
		if(grep(/^$p_all2[$i]$/,@minus10)) {
			$minuscard2 += 10;
		} elsif(grep(/^$p_all2[$i]$/,@minus5)) {
			$minuscard2 += 5;
		} elsif(grep(/^$p_all2[$i]$/,@minus3)) {
			$minuscard2 += 3;
		} elsif(grep(/^$p_all2[$i]$/,@minus1)) {
			$minuscard2 += 1;
		} elsif(grep(/^$p_all2[$i]$/,@plus1)) {
			$minuscard2 -= 1;
		}
	}
	$minuscard2 = 0 if($minuscard2 < 0);

	$rankpoint1 = $drank[1] - $drank[2];
	$rankpoint2 = $drank[2] - $drank[1];

	$winer = $lp[1] == 0 ? 2 : 1;
	&s_mes("$pn[$winer]の勝ち！");
	if(($T{'type'} == 2) && ($room =~ /^t/)) {
		&s_mes("練習対戦なので、勝敗数とポイントは記録されません。");
	} elsif(grep(/^$room$/,@beginner)) {
		&s_mes("練習対戦なので、勝敗数とポイントは記録されません。");
	} elsif((($sr[$u_side] == 1) || ($sr[$u_side2] == 1)) && ($turn <= 2)) {
		&s_mes("2ターン以内の投了・無断退室では勝敗数とポイントは記録されません。");
	} else {
		my(@pop_day) = ();
		my($cnt) = 0;
		&filelock("pop");
		open(POP,"./popular.dat") || &error("使用カード記録データが開けません");
		$pop_date = <POP>;
		chomp($pop_date);
		while(<POP>){ chomp; @{$pop_day[$cnt]} = split(/,/); $cnt ++; }
		close(POP);

		my($sec,$min,$hour,$mday,$mon,$year) = localtime($times);
		my($psec,$pmin,$phour,$pmday,$pmon,$pyear) = localtime($pop_date);
		if(($year != $pyear) || ($mon != $pmon) || ($mday != $pmday)) {
			foreach(@pop_day) {
				while($#{$_} < 7) { push(@{$_}, "0"); }
				while($#{$_} >= 7) { pop(@{$_}); }
				unshift(@{$_}, "0");
			}
		}

		for($i = 0; $i <= $#p_all1; $i ++) {
			$pop_day[$p_all1[$i]][0] ++;
		}
		for($i = 0; $i <= $#p_all2; $i ++) {
			$pop_day[$p_all2[$i]][0] ++;
		}

		open(POP,"> ./popular.dat") || &error("使用カード記録データが開けません");
		print POP $times . "\n";
		foreach(@pop_day) {
			print POP join(',', @{$_}) . "\n";
		}
		close(POP);
		&fileunlock("pop");
		map { &put_shohai($side[$_],$_); } (1..2);
	}
	my $last_turn = $turn;
	&all_clr;
	if($room =~ /^t(.*)/) {
		my $rn = $1;
		my $tphase = &ret_phase($rn, $T{'scale'}) + 1;
		my $th_chk = 0;
		if($tphase == $T{'scale'}) {
			$th_chk = 1;
		}
		my $win_num = &id_to_num($side[$winer]);
		if($rn < 2 ** $T{'scale'} * 2) {
			$T{"p${win_num}win"} ++;
		} else {
			$T{'third'} = 1;
		}
		if($T{'type'} != 2) {
			&filelock("$side[$winer]_lock");
			&filelock("$side[3 - $winer]_lock");
			undef(%WP);
			chmod 0666, "${player_dir}/".$side[$winer].".cgi";
			open(PFL,"${player_dir}/".$side[$winer].".cgi") || &error("プレイヤーファイルが開けません");
			while(<PFL>){ chomp; ($key,$val) = split(/\t/); $WP{$key} = $val; }
			close(PFL);
			chmod 0000, "${player_dir}/".$side[$winer].".cgi";
			undef(%LP);
			chmod 0666, "${player_dir}/".$side[3 - $winer].".cgi";
			open(PFL,"${player_dir}/".$side[3 - $winer].".cgi") || &error("プレイヤーファイルが開けません");
			while(<PFL>){ chomp; ($key,$val) = split(/\t/); $LP{$key} = $val; }
			close(PFL);
			chmod 0000, "${player_dir}/".$side[3 - $winer].".cgi";

			if($T{'type'} == 0) {
				if($rn == 2 ** $T{'scale'} * 2) {
					if(!$WP{'order_tt'}) {
						$WP{'order_tt'} = 1;
						&s_mes("$pn[$winer]に、$order_text{'tt'}が贈られました。");
					}
				} elsif($tphase - 1 == $T{'scale'}) {
					if(!$LP{'order_ts'}) {
						$LP{'order_ts'} = 1;
						&s_mes($pn[3 - $winer]."に、$order_text{'ts'}が贈られました。");
					}
					if(!$WP{'order_tf'}) {
						$WP{'order_tf'} = 1;
						&s_mes("$pn[$winer]に、$order_text{'tf'}が贈られました。");
					}
				}
			}
			&s_mes("一度退室しないと、再度対戦することはできません。");
			chmod 0666, "${player_dir}/".$side[$winer].".cgi";
			open(PFL,"> ${player_dir}/".$side[$winer].".cgi") || &error("プレイヤーファイルが開けません");
			foreach $key(keys(%WP)){ print PFL "$key\t$WP{$key}\n"; }
			close(PFL);
			chmod 0000, "${player_dir}/".$side[$winer].".cgi";
			chmod 0666, "${player_dir}/".$side[3 - $winer].".cgi";
			open(PFL,"> ${player_dir}/".$side[3 - $winer].".cgi") || &error("プレイヤーファイルが開けません");
			foreach $key(keys(%LP)){ print PFL "$key\t$LP{$key}\n"; }
			close(PFL);
			chmod 0000, "${player_dir}/".$side[3 - $winer].".cgi";
			&fileunlock("$side[$winer]_lock");
			&fileunlock("$side[3 - $winer]_lock");
		}

		for(my($thr) = 0; $thr <= $th_chk; $thr ++) {
			if($rn < 2 ** $T{'scale'} * 2 - 1) {
				my $nr = 0;
				my $nr_side = ($rn + 1) % 2 + 1;
				my $pnum = 0;
				if($thr) {
					$nr = 2 ** $T{'scale'} * 2;
					$pnum = &id_to_num($side[3 - $winer]);
				} else {
					$nr = &room_num($tphase, $T{'scale'}) + int((($rn - &room_num($tphase - 1, $T{'scale'})) + 1) / 2);
#					&s_mes("nextroom: &room_num($tphase, $T{'scale'}) + int(($rn - &room_num($tphase - 1, $T{'scale'}) + 1) / 2) : " . &room_num($tphase, $T{'scale'}));
					$pnum = &id_to_num($side[$winer]);
				}

				%TG = ();
				&filelock("t$nr");
				open(PFL,"${room_dir}/".$roomst."t".$nr.'.cgi');
				foreach(<PFL>){ chomp; ($key,$val) = split(/\t/); $TG{$key} = $val; }
				close(PFL);

				$TG{"deck${nr_side}"} = $T{"p${pnum}deck"};
				$TG{"side${nr_side}"} = $T{"p${pnum}id"};
				$TG{"pass${nr_side}"} = $T{"p${pnum}pass"};
				$TG{"pn${nr_side}"} = $T{"p${pnum}name"};
				$TG{"sur_flg${nr_side}"} = 0;
				$TG{"date${nr_side}"} = $times;
				$TG{"tourtime${nr_side}"} = 0;

				if($TG{'side1'} && $TG{'side2'}) {
					$TG{"phase"} = $TG{"turn"} = $TG{"lp1"} = $TG{"lp2"} = 1;
					if($T{'date'}) {
						$TG{"start_date"} = $T{'date'} + $tphase * 60 * 60 * 24;
					} else {
						$TG{"start_date"} = $times;
					}
					@nr_field = ();

					@{$nr_deck[1]} = &num_shuf(split(/\,/, $TG{"deck1"}));
					@{$nr_deck[2]} = &num_shuf(split(/\,/, $TG{"deck2"}));
					@{$nr_hand[1]} = ();
					@{$nr_hand[2]} = ();

					for(my($i) = 1; $i <= 2; $i ++) {
						for(my($j) = 0; $j < 5; $j ++) {
							$nr_field[40 + $j + 160 * (2 - $i)] = shift(@{$nr_deck[$i]});
						}
						for(my($j) = 0; $j < 5; $j ++) {
							unshift(@{$nr_hand[$i]}, shift(@{$nr_deck[$i]}));
						}
					}

					$TG{"fld"} = join(',', @nr_field);
					$TG{"deck1"} = join(',', @{$nr_deck[1]});
					$TG{"deck2"} = join(',', @{$nr_deck[2]});
					$TG{"hand1"} = join(',', @{$nr_hand[1]});
					$TG{"hand2"} = join(',', @{$nr_hand[2]});
					$TG{"date1"} = $times;
					$TG{"date2"} = $times;

					$TG{"turn2"} = int(rand(2))+1;
					open(IN,"${room_dir}/".$roomst."t".$nr."_log.cgi");
					my @nr_lines = <IN>;
					close(IN);
					if($thr) {
						unshift(@nr_lines,"null<>３位決定デュエル開始！<>system<>\n");
					} elsif($tphase == $T{'scale'}) {
						unshift(@nr_lines,"null<>決勝デュエル開始！<>system<>\n");
					} elsif($tphase == $T{'scale'} - 1) {
						unshift(@nr_lines,"null<>準決勝デュエル開始！<>system<>\n");
					} else {
						unshift(@nr_lines,"null<>デュエル開始！<>system<>\n");
					}
					unshift(@nr_lines,"null<>".$TG{"pn$TG{'turn2'}"}."のターン！<>system<>\n");
#					unshift(@nr_lines,"null<>".$TG{"pn$TG{'turn2'}"}."の$phasestr[$TG{'phase'}]。<>\n");

					open(OUT,">${room_dir}/".$roomst."t".$nr."_log.cgi") || &error("ログファイルに書き込めません");
					print OUT @nr_lines;
					close(OUT);

					&fileunlock("t${nr}_log");
				}
				open(PFL, "> ${room_dir}/".$roomst."t".$nr.'.cgi');
				foreach $key(keys(%TG)){ print PFL "$key\t$TG{$key}\n"; }
				close(PFL);
				&fileunlock("t$nr");
			}
		}
		chmod 0666, "./tour/part.dat";
		open(TRT, "> ./tour/part.dat");
		foreach $key(keys(%T)){ print TRT "$key\t$T{$key}\n"; }
		close(TRT);
#		chmod 0000, "./tour/part.dat";
		&fileunlock("tr");
	}
	$end_flg = "1";
	&put_ini;
}

sub put_shohai{
	my ($id,$tsno) = @_;
	&pfl_read($id);
	$shohai = $P{'shohai'};
	$dpoint = $P{'dpoint'};
	$drank = $P{'drank'};
	($win,$lose) = split(/-/,$shohai);
	if($winer == $tsno){ $win++; }
	else{ $lose++; }
	$shohai = "$win-$lose";

	if($room =~ /^t(.*)/) {
		my $rn = $1;
		my $tphase = &ret_phase($rn, $T{'scale'});
		$tphase -- if($rn == 2 ** $T{'scale'} * 2);
		if($tphase == 5) {
			if($winer == $tsno) { $getpoint = 1000; }
			else		    { $getpoint = 500; }
		} elsif($tphase == 4) {
			if($winer == $tsno) { $getpoint = 500; }
			else		    { $getpoint = 250; }
		} elsif($tphase == 3) {
			if($winer == $tsno) { $getpoint = 300; }
			else		    { $getpoint = 150; }
		} elsif($tphase == 2) {
			if($winer == $tsno) { $getpoint = 200; }
			else		    { $getpoint = 100; }
		} elsif($tphase == 1) {
			if($winer == $tsno) { $getpoint = 150; }
			else		    { $getpoint = 75; }
		} elsif($tphase == 0) {
			if($winer == $tsno) { $getpoint = 100; }
			else		    { $getpoint = 50; }
		} else {
			if($winer == $tsno) { $getpoint = 500; }
			else		    { $getpoint = 250; }
		}
	} else {
		if($winer == $tsno) {
			if($timed_up == 1) {
				$getpoint = 160;
			} else {
				$getpoint = 80;
				if($turn < 13) {
					$getpoint -= 20;
				}
			}
		} else {
			if($timed_up == 1) {
				$getpoint = -40;
			} else {
				$getpoint = 40;
				if($turn < 13) {
					$getpoint += 20;
				}
			}
		}
	}
	if($tsno == 1) {
		$getpoint += $shieldpoint1;
		$getpoint -= $shieldpoint2;
		$getpoint -= $minuscard1;
		$getpoint += $minuscard2;
		$getpoint -= $rankpoint1;
	} else {
		$getpoint += $shieldpoint2;
		$getpoint -= $shieldpoint1;
		$getpoint -= $minuscard2;
		$getpoint += $minuscard1;
		$getpoint -= $rankpoint2;
	}

	$drank = 0;
	$dpoint += $getpoint;
	$dpoint = 0 if($dpoint < 0);
	for($i = 0; $i <= $#uppoint; $i ++) {
		if($dpoint < $uppoint[$i]) {
			last;
		} else {
			$drank ++;
		}
	}
	if($winer == $tsno) {
		if($tsno == 1) {
			@winerdeck = @p_all1;
		} else {
			@winerdeck = @p_all2;
		}
		my $weak_point = 0;
		my $fire_point = 0;
		my $nature_point = 0;
		my $light_point = 0;
		my $water_point = 0;
		my $dark_point = 0;
		my %deckcnt = ();
		my $hirander = 1;
		my $all_rainbow = 1;
		foreach $wdeck (@winerdeck) {
			if(grep(/^$wdeck$/,@plus1)) {
				$weak_point ++;
			}
			$fire_point ++ if($c_bun[$wdeck] =~ /3/);
			$nature_point ++ if($c_bun[$wdeck] =~ /4/);
			$light_point ++ if($c_bun[$wdeck] =~ /0/);
			$water_point ++ if($c_bun[$wdeck] =~ /1/);
			$dark_point ++ if($c_bun[$wdeck] =~ /2/);
			$deckcnt{$wdeck} ++;
			$hirander = 0 if($deckcnt{$wdeck} > 1);
			$all_rainbow = 0 if(($c_bun[$wdeck] eq '0') || ($c_bun[$wdeck] eq '1') || ($c_bun[$wdeck] eq '2') || ($c_bun[$wdeck] eq '3') || ($c_bun[$wdeck] eq '4'));
		}
		if($turn >= 13) {
			if(!$P{'order_weak'}) {
				if($weak_point >= 8) {
					$P{'order_weak'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'weak'}が贈られました。");
				}
			}
			if(!$P{'order_long'}) {
				if($turn >= 40) {
					$P{'order_long'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'long'}が贈られました。");
				}
			}
			if(!$P{'order_hirand'}) {
				if($hirander) {
					$P{'order_hirand'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'hirand'}が贈られました。");
				}
			}
			if(!$P{'order_rainbow'}) {
				if($all_rainbow) {
					$P{'order_rainbow'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'rainbow'}が贈られました。");
				}
			}
			if(($fire_point == 40) && ($nature_point == 0) && ($light_point == 0) && ($water_point == 0) && ($dark_point == 0)) {
				$P{'fire_win'} ++;
				if((!$P{'order_fire'}) && ($P{'fire_win'} >= 10)) {
					$P{'order_fire'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'fire'}が贈られました。");
				} elsif((!$P{'order_highfire'}) && ($P{'fire_win'} >= 30)) {
					$P{'order_highfire'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'highfire'}が贈られました。");
				}
			}
			if(($fire_point == 0) && ($nature_point == 40) && ($light_point == 0) && ($water_point == 0) && ($dark_point == 0)) {
				$P{'nature_win'} ++;
				if((!$P{'order_nature'}) && ($P{'nature_win'} >= 10)) {
					$P{'order_nature'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'nature'}が贈られました。");
				} elsif((!$P{'order_highnature'}) && ($P{'nature_win'} >= 30)) {
					$P{'order_highnature'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'highnature'}が贈られました。");
				}
			}
			if(($fire_point == 0) && ($nature_point == 0) && ($light_point == 40) && ($water_point == 0) && ($dark_point == 0)) {
				$P{'light_win'} ++;
				if((!$P{'order_light'}) && ($P{'light_win'} >= 10)) {
					$P{'order_light'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'light'}が贈られました。");
				} elsif((!$P{'order_highlight'}) && ($P{'light_win'} >= 30)) {
					$P{'order_highlight'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'highlight'}が贈られました。");
				}
			}
			if(($fire_point == 0) && ($nature_point == 0) && ($light_point == 0) && ($water_point == 40) && ($dark_point == 0)) {
				$P{'water_win'} ++;
				if((!$P{'order_water'}) && ($P{'water_win'} >= 10)) {
					$P{'order_water'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'water'}が贈られました。");
				} elsif((!$P{'order_highwater'}) && ($P{'water_win'} >= 30)) {
					$P{'order_highwater'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'highwater'}が贈られました。");
				}
			}
			if(($fire_point == 0) && ($nature_point == 0) && ($light_point == 0) && ($water_point == 0) && ($dark_point == 40)) {
				$P{'dark_win'} ++;
				if((!$P{'order_dark'}) && ($P{'dark_win'} >= 10)) {
					$P{'order_dark'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'dark'}が贈られました。");
				} elsif((!$P{'order_highdark'}) && ($P{'dark_win'} >= 30)) {
					$P{'order_highdark'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'highdark'}が贈られました。");
				}
			}

			my $exist_color_d = 12;
			my $exist_color_t = 8;

			my %deck_color = (
			'lw' => [$exist_color_d, $exist_color_d, 0, 0, 0],
			'wd' => [0, $exist_color_d, $exist_color_d, 0, 0],
			'df' => [0, 0, $exist_color_d, $exist_color_d, 0],
			'fn' => [0, 0, 0, $exist_color_d, $exist_color_d],
			'nl' => [$exist_color_d, 0, 0, 0, $exist_color_d],
			'ld' => [$exist_color_d, 0, $exist_color_d, 0, 0],
			'wf' => [0, $exist_color_d, 0, $exist_color_d, 0],
			'dn' => [0, 0, $exist_color_d, 0, $exist_color_d],
			'fl' => [$exist_color_d, 0, 0, $exist_color_d, 0],
			'nw' => [0, $exist_color_d, 0, 0, $exist_color_d],
			'lwd' => [$exist_color_t, $exist_color_t, $exist_color_t, 0, 0],
			'wfl' => [$exist_color_t, $exist_color_t, 0, $exist_color_t, 0],
			'nlw' => [$exist_color_t, $exist_color_t, 0, 0, $exist_color_t],
			'fld' => [$exist_color_t, 0, $exist_color_t, $exist_color_t, 0],
			'ldn' => [$exist_color_t, 0, $exist_color_t, 0, $exist_color_t],
			'fnl' => [$exist_color_t, 0, 0, $exist_color_t, $exist_color_t],
			'wdf' => [0, $exist_color_t, $exist_color_t, $exist_color_t, 0],
			'wdn' => [0, $exist_color_t, $exist_color_t, 0, $exist_color_t],
			'nwf' => [0, $exist_color_t, 0, $exist_color_t, $exist_color_t],
			'dfn' => [0, 0, $exist_color_t, $exist_color_t, $exist_color_t],
			'nolight' => [0, $exist_color_t, $exist_color_t, $exist_color_t, $exist_color_t],
			'nowater' => [$exist_color_t, 0, $exist_color_t, $exist_color_t, $exist_color_t],
			'nodark' => [$exist_color_t, $exist_color_t, 0, $exist_color_t, $exist_color_t],
			'nofire' => [$exist_color_t, $exist_color_t, $exist_color_t, 0, $exist_color_t],
			'nonature' => [$exist_color_t, $exist_color_t, $exist_color_t, $exist_color_t, 0]
			);
			foreach $key (keys(%deck_color)) {
				if(
				((($light_point == 0) && (!$deck_color{$key}[0])) || (($light_point >= $deck_color{$key}[0]) && ($deck_color{$key}[0]))) &&
				((($water_point == 0) && (!$deck_color{$key}[1])) || (($water_point >= $deck_color{$key}[1]) && ($deck_color{$key}[1]))) &&
				((($dark_point == 0) && (!$deck_color{$key}[2])) || (($dark_point >= $deck_color{$key}[2]) && ($deck_color{$key}[2]))) &&
				((($fire_point == 0) && (!$deck_color{$key}[3])) || (($fire_point >= $deck_color{$key}[3]) && ($deck_color{$key}[3]))) &&
				((($nature_point == 0) && (!$deck_color{$key}[4])) || (($nature_point >= $deck_color{$key}[4]) && ($deck_color{$key}[4])))
				) {
					$P{$key . '_win'} ++;
					if((!$P{'order_' . $key}) && ($P{$key . '_win'} >= 10)) {
						$P{'order_' . $key} = 1;
						&s_mes("$pn[$tsno]に、$order_text{$key}が贈られました。");
					} elsif((!$P{'order_high' . $key}) && ($P{$key . '_win'} >= 30)) {
						$P{'order_high' . $key} = 1;
						&s_mes("$pn[$tsno]に、$order_text{'high' . $key}が贈られました。");
					}
				}
			}

			if(($fire_point >= 5) && ($nature_point >= 5) && ($light_point >= 5) && ($water_point >= 5) && ($dark_point >= 5)) {
				$P{'full_win'} ++;
				if((!$P{'order_full'}) && ($P{'full_win'} >= 10)) {
					$P{'order_full'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'full'}が贈られました。");
				} elsif((!$P{'order_highfull'}) && ($P{'full_win'} >= 30)) {
					$P{'order_highfull'} = 1;
					&s_mes("$pn[$tsno]に、$order_text{'highfull'}が贈られました。");
				}
			}
		} else {
			&s_mes("12ターン以内での勝利では、単色デッキ等の勝利数は増えません。");
		}
	}
	if(!$P{'order_ex'}) {
		if($dpoint >= 20000) {
			$P{'order_ex'} = 1;
			&s_mes("$pn[$tsno]に、$order_text{'ex'}が贈られました。");
		}
	} elsif(!$P{'order_sp'}) {
		if($dpoint >= 30000) {
			$P{'order_sp'} = 1;
			&s_mes("$pn[$tsno]に、$order_text{'sp'}が贈られました。");
		}
	} elsif(!$P{'order_dm'}) {
		if($dpoint >= 50000) {
			$P{'order_dm'} = 1;
			&s_mes("$pn[$tsno]に、$order_text{'dm'}が贈られました。");
		}
	}

	$P{'shohai'} = $shohai;
	$P{'dpoint'} = $dpoint;
	$P{'drank'} = $drank;
	$P{'usedeck'} = $usedeck[$tsno];
	$P{'dendou'} = $dendou;

	if($P{'evtime'} < $times - 60 * 60 * 24 * 7) {
		$P{'evpoint'} = 0;
		$P{'evtime'} = 0;
	}

#	&filelock;
	&pfl_write($id);
#	&fileunlock;
#&s_mes("デバッグ出力：（s1:$shieldpoint1;s2:$shieldpoint2;m1:$minuscard1;m2:$minuscard2;r:$rankpoint1;）");
	if($getpoint > 0) {
		&s_mes("$pn[$tsno]は <B>${getpoint}P</B>手に入れた！");
	} elsif($getpoint < 0) {
		&s_mes("$pn[$tsno]は <B>${getpoint}P</B>失ってしまった・・・");
	} else {
		&s_mes("$pn[$tsno]は ポイントが 変わらなかった。");
	}
}

sub room_num {
	my $n = $_[0];
	my $m = $_[1];
	my $r = 0;
	for (my $i = 0; $i < $n; $i ++) {
		$r += 2 ** $m / (2 ** $i);
	}
	return $r;
}

sub ret_phase {
	my($n) = $_[0];
	my($m) = $_[1];
	my($t) = 0;
	for(my($i) = 0; $i < $m; $i ++) {
		$t += 2 ** ($m - $i);
		return $i if($n <= $t);
	}
	return $m;
}

sub id_to_num {
	my $n = $_[0];
	for (my($i) = 1; $i <= 2 ** $T{'scale'} * 2; $i ++) {
		return $i if($n eq $T{"p${i}id"});
	}
	return 0;
}

sub num_shuf {
    my @list = @_;

    for my $i (0 .. $#list) {
        my $rand = int(rand(@list));
        my $tmp = $list[$i];
        $list[$i] = $list[$rand];
        $list[$rand] = $tmp;
    }
    return @list;
}


sub make_id {
	my @alphabet = ('A'..'Z');
	$m_id = "";
	for(0..2){ my $random = int(rand(26)); $m_id .= $alphabet[$random]; }
	my $m_id2 = int(rand(99999))+1;
	$m_id .= sprintf("%05d",$m_id2);
	return $m_id;
}

1;
