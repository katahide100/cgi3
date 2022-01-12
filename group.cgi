#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

require 'cust.cgi';
require 'series.lib';
require 'duel.pl';

&decode;
&get_cookie;
$pc_chk = int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) . int(rand(10)) if($pc_chk eq '');
$F{'id'} = $c_id if(!$F{'id'});
$F{'pass'} = $c_pass if(!$F{'pass'});
&set_cookie;
if($F{'mode'} ne "cardview"){
	&decode2;
	&groupread;
	&pass_chk;
}
&cardread;
&syu_read;
&copy_run	if $F{'mode'} eq "groupcopy" && $F{'copy'} ne "";
&cardview	if $F{'mode'} eq "cardview";
&group_chg	if $F{'mode'} eq "group_chg";
&groupmake	if $F{'mode'} eq "groupmake";
&groupsave	if $F{'mode'} eq "groupsave";
&del_group	if $F{'mode'} eq "del_group";
&del_group2	if $F{'mode'} eq "del_group2";
&regist		if $F{'mode'} eq "regist";
&pickup;
&cardsort;
&groupsort;
&html;

sub group_chg{
	$P{'usegroup'} = $F{'usegroup'};
	$P{'pregroup'} = "" if $dnam[$F{'usegroup'}] ne "記録なし";
	$selstr4[$F{'usegroup'}] = " selected";
	&pfl_write($id);
	&groupread;
}

sub groupsave{
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
function sForm(F,C){
	save.mode.value = F;
	save.j.value = C;
	save.target = F == "cardview" ? "_blank" : "";
	save.submit();
}
// --></script>
</head>
<body>
<div align="center">
<table width="640" border="1" cellspacing="0" cellpadding="10" class="table">
<tr><td>
<p>※以下のグループをセーブします。グループに名前をつけてください。<br>
※グループは$maxgroup個までセーブすることができます。<br>
<font color="red">※既に$maxgroup個セーブされている場合、現在選択中のグループに新しいグループが上書きされます。</font></p>
<div align="center">
<form action="group.cgi" method="post" name="save">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode"value="regist">
	<input type="text" size="20" name="groupname">&nbsp;
	<input type="submit" value="決定">&nbsp;
	<input type="reset" value="クリア">
</form>
<br><br>
<table border="1" width="500">
<caption>グループ内容</caption>
<tr valign="top"><td width="250">
EOM
	my $count = 0;
	foreach my $card(@group){
		print "<a href=\"sForm('cardview',$card);\">$c_name[$card]</a><br>\n";
		print "</td><td>\n" if $count == 19;
		$count++;
	}
	print <<"EOM";
</td></tr></table>
<br><br>
<a href="javascript:document.save.mode.value = "";document.save.submit();">戻る</a>
</div>
</td></tr>
</table>
EOM
	&footer;
}

sub del_group	{
	&header;
	print <<"EOM";
<script type="text/javascript"><!--
function sForm(F,C){
	with(document.save){
		mode.value = F;
		j.value = C;
		target = F == "cardview" ? "_blank" : "";
		submit();
	}
}
// --></script>
</head>
<body>
<div align="center">
<table width="640" border="1" cellspacing="0" cellpadding="10" class="table">
<tr><td>
<p>※以下のデッキを消去します。<br>
<strong style="color: red;">※消去したデッキは復活させることができません！　しっかり確認してください。</strong></p>
<div align="center">
<table border="1" width="500">
<caption>デッキ内容</caption>
<tr valign="top"><td width="250">
EOM
	my $count = 0;
	foreach my $card(@group){
		print qq|<a href="sForm('cardview',$card);">$c_name[$card]</a><br>\n|;
		print qq|</td><td>\n| if $count == 19;
		$count++;
	}
	print <<"EOM";
</td></tr></table>
<br><br>
<form action="group.cgi" method="post" name="delete">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode"value="del_group2">
	<input type="submit" value="消去する" onclick="if(window.confirm('デッキを消去しますか？')){ sFlag('del_group2'); }">&nbsp;
</form>
<br><br>
<a href="javascript:save.mode.value='';save.submit();">戻る</a>
</div>
</td></tr>
</table>
EOM
	&footer;
}

sub regist{
	return unless $id;
	$usegroup = $P{'usegroup'};
	$usegroup = 1 unless($usegroup);
	$dcon = join(",",@group);
	delete $P{'pregroup'};
#	my $cou = 0;
#	foreach my $i(1..$maxgroup){
#		unless($P{"group$i"}){
#			$dnam = ($F{'groupname'}) ? $F{'groupname'} : "デッキ".$i;
#			$dnam[$i] = $dnam;
#			$dcon[$i] = $dcon;
#			$P{"group$i"} = "$dnam[$i]\-$dcon[$i]";
#			last;
#		}
#		$cou++;
#	}
#	if($cou == $maxgroup){
		$dnam = ($F{'groupname'}) ? $F{'groupname'} : "グループ".$usegroup;
		$dnam =~ s/\-/－/g;
		$dnam[$usegroup] = $dnam;
		$dcon[$usegroup] = $dcon;
		$P{"group$usegroup"}="$dnam[$usegroup]\-$dcon[$usegroup]";
#	}
	&pfl_write($id);
}

sub del_group2	{
	return unless $id;
	$usegroup = $P{'usegroup'};
	delete $P{"group$usegroup"};
	undef(@group);
	&pfl_write($id);
	$dnam[$usegroup] = "記録なし";
}

sub groupmake{
	if($F{'text'}){
		undef(@group);
		@tmp = split(/\n/,$F{'text'});
		foreach my $card(@tmp){ $TX{$card}++ if $card; }
		foreach my $i(0..$#c_name){
			if($TX{$c_name[$i]}){
				$TXC{$c_name[$i]} = 1;
				for($j=0;$j<$TX{$c_name[$i]};$j++){ push(@group,$i); }
			}
		}
		foreach $key (keys(%TX)){ $overmsg.="<strong>$keyというカードは存在しません</strong><br>\n" unless $TXC{$key}; }
	}
	@group_new = @group;
	undef(@group);
	for($i=$#group_new;$i>-1;$i--){
		&add_card($group_new[$i],1) unless $F{'del'.$i};
	}
	@mai = grep(/^sel/,keys(%F));
	foreach $cardno(@mai){
		$kaisu = $F{$cardno};
		next if $kaisu =~ /\D/;
		$kaisu = 1 if $kaisu > 1;
		$cardno =~ s/^sel//;
		&add_card($cardno,$kaisu);
	}
	@group_stack = sort groupsort @group;
	@group = @group_stack;
	&put_ini;
}

sub copy_run{
	open(CHD,"group.dat") || &error("コピーグループデータの読み込みに失敗しました");
	my $cou = 1;
	while(<CHD>){
		chomp($chdst = $_);
		last if $cou == $F{'copy'};
		$cou++;
	}
	($dummy,$tmp) = split(/-/,$chdst);
	@group = split(/,/,$tmp);
	@group = sort groupsort @group;
	&put_ini;
}

sub add_card{
	my ($cardno,$kaisu) = @_; my $couno = $cardno;
	for(1 .. $kaisu){
		if($card_cou[$couno] < 1){
			unshift(@group,$cardno);
			$card_cou[$couno]++;
		}
	}
}

sub pickup{
	$F{'series'} = 0 unless $F{'series'};
	$F{'kind'} = 0 unless $F{'kind'};
	if($F{'sstr'} || $F{'sstr2'}){
		$F{'series'} = 99;
		$F{'kind'} = $cou = 0;
		undef(@disp);
		if($F{'sstr'}){
			$F{'sstr'} =~ s/　/ /g;
			my @word = split(/\s+/, $F{'sstr'});
			foreach my $key (@word) {
				foreach my $card (0 .. $#c_name){
					if ($c_name[$card] =~ /$key/){ $disp[$cou] = $card; $cou++; }
				}
			}
		}
		if($F{'sstr2'}){
			$F{'sstr2'} =~ s/　/ /g;
			my @word2 = split(/\s+/, $F{'sstr2'});
			foreach my $key2 (@word2) {
				foreach my $card (0 .. $#c_syu){
					if (&syu_sub($card) =~ /$key2/){ $disp[$cou] = $card; $cou++; }
				}
			}
		}
		my %tmp;
		@disp = grep(!$tmp{$_}++,@disp);
		$overmsg = "<strong>条件に合うカードはありません</strong><br><br>\n" if $#disp < 0;
	} elsif ($F{'series'} ne "99") {
		@disp = @{$ser[$F{'series'}]};
	} else {
		foreach my $i(0 .. $#c_name){
			$disp[$i] = $i if $c_name[$i] ne "";
		}
	}
	@d_tmp = ();
	if($F{'kind'} != 0){
		foreach my $i(@disp){
			$c_kind = $c_syu[$i] == 1 ? 2 : $c_syu[$i] == 0 ? 1 : 0;
			if($F{'kind'} == 1){ push(@d_tmp,$i) if !($c_kind); }
			elsif($F{'kind'} == 2){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 0); }
			elsif($F{'kind'} == 3){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 1); }
			elsif($F{'kind'} == 4){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 2); }
			elsif($F{'kind'} == 5){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 3); }
			elsif($F{'kind'} == 6){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 4); }
			elsif($F{'kind'} == 7){ push(@d_tmp,$i) if (!($c_kind) && &k_chk($c_kok[$i],12)); }
			elsif($F{'kind'} == 8){ push(@d_tmp,$i) if $c_kind == 1; }
			elsif($F{'kind'} == 9){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 0; }
			elsif($F{'kind'} == 10){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 1; }
			elsif($F{'kind'} == 11){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 2; }
			elsif($F{'kind'} == 12){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 3; }
			elsif($F{'kind'} == 13){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 4; }
			elsif($F{'kind'} == 14){ push(@d_tmp,$i) if $c_kind == 1 && &k_chk($c_kok[$i],12); }
			elsif($F{'kind'} == 15){ push(@d_tmp,$i) if $c_kind == 2; }
			elsif($F{'kind'} == 16){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 0; }
			elsif($F{'kind'} == 17){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 1; }
			elsif($F{'kind'} == 18){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 2; }
			elsif($F{'kind'} == 19){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 3; }
			elsif($F{'kind'} == 20){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 4; }
			elsif($F{'kind'} == 21){ push(@d_tmp,$i) if $c_kind == 2 && &k_chk($c_kok[$i],12); }
		}
		@disp = @d_tmp;
	}
	@d_tmp = ();
	if($F{'skill'} != 0){
		foreach my $i(@disp){
			   if ($F{'skill'} ==  1) { push @d_tmp, $i if $c_evo[$i] && $c_evo[$i] < 8; }
			elsif ($F{'skill'} ==  2) { push @d_tmp, $i if 8 <= $c_evo[$i]; }
			elsif ($F{'skill'} ==  3) { push @d_tmp, $i if &k_chk($i, 1); }
			elsif ($F{'skill'} ==  4) { push @d_tmp, $i if &k_chk($i, 3); }
			elsif ($F{'skill'} ==  5) { push @d_tmp, $i if &k_chk($i, 5); }
			elsif ($F{'skill'} ==  6) { push @d_tmp, $i if &k_chk($i, 8); }
			elsif ($F{'skill'} ==  7) { push @d_tmp, $i if &k_chk($i, 9); }
			elsif ($F{'skill'} ==  8) { push @d_tmp, $i if &k_chk($i, 4); }
			elsif ($F{'skill'} ==  9) { push @d_tmp, $i if &k_chk($i, 6); }
			elsif ($F{'skill'} == 10) { push @d_tmp, $i if &k_chk($i, 10); }
			elsif ($F{'skill'} == 11) { push @d_tmp, $i if &k_chk($i, 11); }
			elsif ($F{'skill'} == 12) { push @d_tmp, $i if &k_chk($i, 13); }
			elsif ($F{'skill'} == 13) { push @d_tmp, $i if &k_chk($i, 15); }
			elsif ($F{'skill'} == 14) { push @d_tmp, $i if &k_chk($i, 17); }
			elsif ($F{'skill'} == 15) { push @d_tmp, $i if &k_chk($i, 18); }
			elsif ($F{'skill'} == 16) { push @d_tmp, $i if &k_chk($i, 19); }
			elsif ($F{'skill'} == 17) { push @d_tmp, $i if &k_chk($i, 20); }
			elsif ($F{'skill'} == 18) { push @d_tmp, $i if &k_chk($i, 22); }
			elsif ($F{'skill'} == 19) { push @d_tmp, $i if &k_chk($i, 23); }
			elsif ($F{'skill'} == 20) { push @d_tmp, $i if &k_chk($i, 27); }
			elsif ($F{'skill'} == 21) { push @d_tmp, $i if &k_chk($i, 25); }
			elsif ($F{'skill'} == 22) { push @d_tmp, $i if &k_chk($i, 26); }
			elsif ($F{'skill'} == 23) { push @d_tmp, $i if &k_chk($i, 28); }
			elsif ($F{'skill'} == 24) { push @d_tmp, $i if $c_tri[$i] == 1; }
			elsif ($F{'skill'} == 25) { push @d_tmp, $i if $c_tri[$i] == 6; }
			elsif ($F{'skill'} == 26) { push @d_tmp, $i if &k_chk($i, 7); }
			elsif ($F{'skill'} == 27) { push @d_tmp, $i if &k_chk($i, 16); }
			elsif ($F{'skill'} == 28) { push @d_tmp, $i if &k_chk($i, 21); }
			elsif ($F{'skill'} == 29) { push @d_tmp, $i if &k_chk($i, 30); }
			elsif ($F{'skill'} == 30) { push @d_tmp, $i if &k_chk($i, 31); }
			elsif ($F{'skill'} == 31) { push @d_tmp, $i if &k_chk($i, 32); }
			elsif ($F{'skill'} == 32) { push @d_tmp, $i if &k_chk($i, 33); }
			elsif ($F{'skill'} == 33) { push @d_tmp, $i if &k_chk($i, 34); }
		}
		@disp = @d_tmp;
	}
	$selstr[$F{'series'}] = $selstr2[$F{'kind'}] = $selstr3[$F{'skill'}] = $selstr4[$P{'usedeck'}] = " selected";
}

sub k_chk {
	my ($c_kok,$skill) = @_;
	@kouka = split(/,/,$c_kok);
	foreach my $kouka(@kouka){
		return 1 if $kouka == $skill;
	}
	return 0;
}

sub html{
	if($copy){
		open(IN,"group.dat") || &error("コピーグループデータの読み込みに失敗しました");
		@data = <IN>;
		close(IN);
	}
	&header;
	$viewst = $F{'view'} ? qq|<a href="javascript:groupV();">通常表示</a>| : qq|<a href="javascript:groupV('text');">テキスト表示</a>|;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
function sForm(F,C){
	with(group){
		mode.value = F;
		j.value = C;
		action = F == "taisen" ? "taisen.cgi" : F == "deck" ? "deck.cgi" : F == "list" ? "list.cgi" : F == "nuisance" ? "nuisance.cgi" : "group.cgi";
		target = F == "cardview" ? "_blank" : "";
		submit();
	}
}
function chkCB(){
	with(group){
		if(allchk.checked == true){
			for(i=0;i<elements.length;i++){
				if(elements["del"+i]){ elements["del"+i].checked = true; }
			}
		} else if (allchk.checked == false) {
			for(i=0;i<elements.length;i++){
				if(elements["del"+i]){ elements["del"+i].checked = false; }
			}
		}
	}
}

function groupV(t) {
	document.view.view.value = t;
	document.view.submit();
}
// --></script>
</head>
<body>
<div align="center">
	$overmsg
	<form name="view" action="group.cgi" method="post">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="view" value="">
	</form>
	<form name="group" action="group.cgi" method="post">
		<input type="hidden" name="id" value="$id">
		<input type="hidden" name="pass" value="$pass">
		<input type="hidden" name="mode" value="">
		<input type="hidden" name="j" value="">
EOM
	print q|<input type="hidden" name="view" value="text">| if $F{'view'} eq "text";
	print <<"EOM";
		<p class="search">
		拡張パック：
		<select name="series">
			<option value="0"$selstr[0]>第１弾</option>
			<option value="1"$selstr[1]>第２弾</option>
			<option value="2"$selstr[2]>第３弾</option>
			<option value="3"$selstr[3]>第４弾</option>
			<option value="4"$selstr[4]>第５弾</option>
			<optgroup label="闘魂編">
				<option value="5"$selstr[5]>第１弾</option>
				<option value="6"$selstr[6]>第２弾</option>
				<option value="7"$selstr[7]>第３弾</option>
				<option value="8"$selstr[8]>第４弾</option>
			</optgroup>
			<optgroup label="聖拳編">
				<option value="9"$selstr[9]>第１弾</option>
				<option value="10"$selstr[10]>第２弾</option>
				<option value="11"$selstr[11]>第３弾</option>
				<option value="12"$selstr[12]>第４弾</option>
			</optgroup>
			<optgroup label="転生編">
				<option value="13"$selstr[13]>第１弾</option>
				<option value="14"$selstr[14]>第２弾</option>
				<option value="15"$selstr[15]>第３弾</option>
				<option value="16"$selstr[16]>第４弾</option>
			</optgroup>
			<optgroup label="不死鳥編">
				<option value="18"$selstr[18]>第１弾</option>
				<option value="19"$selstr[19]>第２弾</option>
				<option value="20"$selstr[20]>第３弾</option>
				<option value="21"$selstr[21]>第４弾</option>
				<option value="22"$selstr[22]>第５弾</option>
			</optgroup>
			<optgroup label="極神編">
				<option value="23"$selstr[23]>第１弾</option>
				<option value="24"$selstr[24]>第２弾</option>
				<option value="25"$selstr[25]>第３弾</option>
				<option value="26"$selstr[26]>第４弾</option>
			</optgroup>
			<optgroup label="戦国編">
				<option value="27"$selstr[27]>第１弾</option>
			</optgroup>
			<option value="51"$selstr[51]>双龍パック</option>
			<option value="17"$selstr[17]>BCパック</option>
			<option value="52"$selstr[52]>CDパック</option>
			<option value="53"$selstr[53]>CDパック2</option>
			<option value="54"$selstr[54]>CDパック3</option>
			<option value="55"$selstr[55]>ゼロデュエル</option>
			<option value="98"$selstr[98]>プロモ</option>
			<option value="99"$selstr[99]>全部</option>
		</select>
		カード種別：
		<select name="kind">
			<option value="0"$selstr2[0]>全部</option>
			<optgroup label="クリーチャー">
				<option value="1"$selstr2[1]>全文明</option>
				<option value="2"$selstr2[2]>光</option>
				<option value="3"$selstr2[3]>水</option>
				<option value="4"$selstr2[4]>闇</option>
				<option value="5"$selstr2[5]>火</option>
				<option value="6"$selstr2[6]>自然</option>
				<option value="7"$selstr2[7]>レインボー</option>
			</optgroup>
			<optgroup label="呪文">
				<option value="8"$selstr2[8]>全文明</option>
				<option value="9"$selstr2[9]>光</option>
				<option value="10"$selstr2[10]>水</option>
				<option value="11"$selstr2[11]>闇</option>
				<option value="12"$selstr2[12]>火</option>
				<option value="13"$selstr2[13]>自然</option>
				<option value="14"$selstr2[14]>レインボー</option>
			</optgroup>
			<optgroup label="クロスギア">
				<option value="15"$selstr2[15]>全文明</option>
				<option value="16"$selstr2[16]>光</option>
				<option value="17"$selstr2[17]>水</option>
				<option value="18"$selstr2[18]>闇</option>
				<option value="19"$selstr2[19]>火</option>
				<option value="20"$selstr2[20]>自然</option>
				<option value="21"$selstr2[21]>レインボー</option>
			</optgroup>
		</select>
		能力：
		<select name="skill">
			<option value="0"$selstr3[0]>&nbsp;</option>
			<option value="1"$selstr3[1]>進化</option>
			<option value="2"$selstr3[2]>マナ進化</option>
			<option value="3"$selstr3[3]>ブロッカー</option>
			<option value="4"$selstr3[4]>Ｗ・ブレイカー</option>
			<option value="5"$selstr3[5]>Ｔ・ブレイカー</option>
			<option value="6"$selstr3[6]>クルー・ブレイカー</option>
			<option value="7"$selstr3[7]>スレイヤー</option>
			<option value="8"$selstr3[8]>サバイバー</option>
			<option value="9"$selstr3[9]>スピードアタッカー</option>
			<option value="10"$selstr3[10]>ターボラッシュ</option>
 			<option value="11"$selstr3[11]>サイレントスキル</option>
			<option value="12"$selstr3[12]>ウェーブストライカー</option>
 			<option value="13"$selstr3[13]>シンパシー</option>
			<option value="14"$selstr3[14]>アクセル</option>
			<option value="15"$selstr3[15]>Ｇ・ゼロ</option>
			<option value="16"$selstr3[16]>メテオバーン</option>
			<option value="17"$selstr3[17]>ダイナモ</option>
			<option value="18"$selstr3[18]>フォートＥ</option>
			<option value="19"$selstr3[19]>スリリング・スリー</option>
			<option value="20"$selstr3[20]>Ｏ・ドライブ</option>
			<option value="21"$selstr3[21]>侍流ジェネレート</option>
			<option value="22"$selstr3[22]>シールド・プラス</option>
			<option value="23"$selstr3[23]>シールド・フォース</option>
			<option value="24"$selstr3[24]>Ｓ・トリガー</option>
			<option value="25"$selstr3[25]>Ｓ・バック</option>
			<option value="26"$selstr3[26]>チャージャー</option>
			<option value="27"$selstr3[27]>メタモーフ</option>
			<option value="28"$selstr3[28]>サイクロン</option>
			<option value="29"$selstr3[29]>ナイト・マジック</option>
			<option value="30"$selstr3[30]>ニンジャ・ストライク</option>
			<option value="31"$selstr3[31]>Q・ブレイカー</option>
			<option value="32"$selstr3[32]>シールド・セイバー</option>
			<option value="33"$selstr3[33]>シールド焼却</option>
		</select><br>
		カード名検索：<input type="text" name="sstr" size="24" value="$F{'sstr'}">&nbsp;&nbsp;
		種族名検索：<input type="text" name="sstr2" size="24" value="$F{'sstr2'}">&nbsp;&nbsp;
		<input type="button" value="検索" onclick="sForm();">
	</p>
	<table border="4" cellpadding="5" class="table"><tr valign="top">
		<td colspan="2" align="center">
			<p><a href="./etc/help.html#group" target="_blank">説明</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('taisen');">対戦する</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('deck');">デッキ構築</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('list');">リスト構築</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('log');">過去ログ</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('nuisance');">迷惑行為</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="index.cgi">戻る</a>&nbsp;&nbsp;&nbsp;&nbsp;$viewst
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<select name="usegroup">
EOM
	map { print qq|<option value="$_"$selstr4[$_]>$dnam[$_]</option>\n| } (1..$maxgroup);
	print <<"EOM";
			</select>
&nbsp;<input type="button" value="グループ選択" onclick="sForm('group_chg');"></p>
<p>
<input type="button" value="グループ組替" onclick="sForm('groupmake');">&nbsp;&nbsp;&nbsp;&nbsp;
<input type="button" value="グループセーブ" onclick="sForm('groupsave');">&nbsp;&nbsp;&nbsp;&nbsp;
EOM
	if($copy && @data > 0){
		my $no = 1;
		print qq|<select name="copy">\n|;
		print qq|<option value="0">&nbsp;</option>\n|;
		foreach (@data){
			($cnam,$dummy) = split(/-/);
			print qq|<option value="$no">$cnam</option>\n|;
			$no++;
	 	}
		print "</select>&nbsp;\n";
		print qq|<input type="button" value="コピー" onclick="sForm('groupcopy');">\n|;
	 }
	print <<"EOM";
&nbsp;&nbsp;&nbsp;&nbsp;<input type="button" value="グループ消去" onclick="sForm('del_group');">
</p>
</td></tr>
	<tr valign="top">
	<td width="400">
EOM
	print qq|<input type="hidden" name="view" value="text">| if $F{'view'} eq "text";
	&view_list(0) if @sort_res > 0;
	&view_list(1) if @sort_res2 > 0;
	&view_list(2) if @sort_res3 > 0;
	print "　</td><td>\n";
	if(@group == 0){ @main_group = @main_num = (); $groupcou = 0; }
	else{
		$count = 0;
		foreach $card(@group){
			push(@main_group,$card);
			push(@main_num,$count);
			$count++;
		}
		$groupcou = $#main_group+1;
	}
	if ($F{'view'} eq "text"){ &groupview_text; } else { &groupview; }
	print <<"EOM";
	</td></tr>
	</table>
	</form>
EOM
	&footer;
}

sub view_list{
	my $label = $_[0];
	if($label == 0){
		print <<"EOM";
<big>クリーチャー</big>
	　<select name="sortkey">
		<option value="0"$selstr6[0]>文明順</option>
		<option value="1"$selstr6[1]>マナコスト順</option>
		<option value="2"$selstr6[2]>パワー順</option>
		<option value="3"$selstr6[3]>種族順</option>
		<option value="4"$selstr6[4]>名前順</option>
	</select>
　<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
		map { &print_card($_) } @sort_res;
		print "</table>\n";
	} elsif($label == 1) {
		print <<"EOM";
<big>呪文</big>
　<select name="sortkey2">
	<option value="0"$selstr7[0]>文明順</option>
	<option value="1"$selstr7[1]>マナコスト順</option>
	<option value="2"$selstr7[2]>名前順</option>
</select>
　<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
		map { &print_card($_) } @sort_res2;
		print "</table>\n";
	} else {
		print <<"EOM";
<big>クロスギア</big>　
<select name="sortkey3">
	<option value="0"$selstr8[0]>文明順</option>
	<option value="1"$selstr8[1]>マナコスト順</option>
	<option value="2"$selstr8[2]>名前順</option>
</select>　
<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
		map { &print_card($_) } @sort_res3;
		print "</table>\n";
	}
}

sub print_card {
	local $j = $_[0];
	print "<tr><td>";
	&print_line;
	print qq|</td><td align="right" nowrap>×&nbsp;<input type="checkbox" name="sel$j" value="1"></td></tr>\n|;
}

sub print_line{
	my $syu = &syu_sub($j);
	my $bun = (&bun_sub($j))[0];
	print qq|<a href="javascript:sForm('cardview',$j);">$c_name[$j]</a>/$bun/$c_mana[$j]|;
	printf  "%s%s", 1 < $c_syu[$j] ? "/$c_pow[$j]/$syu" : "", $c_evo[$j] == 7 ? "/GV進化"  : $c_evo[$j] == 5 ? "/Ｖ進化" : ($c_evo[$j]) && $c_evo[$j] != 2 ? "/進化" : "";
}

sub s_name { $c_name[$a] cmp $c_name[$b]; }
sub s_syuzoku { &syu_sub($a) cmp &syu_sub($b); }
sub s_bunmei {
	$bunmeia = (&bun_sub($a))[1] eq "hikari" ? 1 : (&bun_sub($a))[1] eq "mizu" ? 2 : (&bun_sub($a))[1] eq "yami" ? 3 : (&bun_sub($a))[1] eq "hi" ? 4 : (&bun_sub($a))[1] eq "sizen" ? 5 : 6;
	$bunmeib = (&bun_sub($b))[1] eq "hikari" ? 1 : (&bun_sub($b))[1] eq "mizu" ? 2 : (&bun_sub($b))[1] eq "yami" ? 3 : (&bun_sub($b))[1] eq "hi" ? 4 : (&bun_sub($b))[1] eq "sizen" ? 5 : 6;
	$bunmeia <=> $bunmeib;
}
sub s_power { $c_pow[$a] <=> $c_pow[$b]; }
sub s_mana { $c_mana[$a] <=> $c_mana[$b]; }

sub cardsort{
	my ($cou,$cou2,$cou3) = 0;
	foreach my $i(@disp){
		if($c_syu[$i] == 1){ $sort_src3[$cou3] = $i; $cou3++; }
		elsif($c_syu[$i] == 0){ $sort_src2[$cou2] = $i; $cou2++; }
		else{ $sort_src[$cou] = $i; $cou++; }
	}
	@sort_res = $F{'sortkey'} == 0 ? sort s_bunmei @sort_src : $F{'sortkey'} == 1 ? sort s_mana @sort_src : $F{'sortkey'} == 2 ? sort s_power @sort_src : $F{'sortkey'} == 3 ? sort s_syuzoku @sort_src : sort s_name @sort_src;
	@sort_res2 = $F{'sortkey2'} == 0 ? sort s_bunmei @sort_src2 : $F{'sortkey2'} == 1 ? sort s_mana @sort_src2 : sort s_name @sort_src2;
	@sort_res3 = $F{'sortkey3'} == 0 ? sort s_bunmei @sort_src3 : $F{'sortkey3'} == 1 ? sort s_mana @sort_src3 : sort s_name @sort_src3;
	$selstr6[$F{'sortkey'}] = $selstr7[$F{'sortkey2'}] = " selected";
}

sub groupsort{
	$lva = $c_syu[$a] == 1 ? 2 : $c_syu[$a] == 0 ? 1 : 0;
	$lvb = $c_syu[$b] == 1 ? 2 : $c_syu[$a] == 0 ? 1 : 0;
	$lva <=> $lvb || &s_bunmei || &s_mana || &s_power || &s_name;
}

sub groupview_text {
	print "　グループ枚数?$groupcou枚<br><br>\n";
	print q|<textarea cols="30" rows="70" name="text">|;
	map { print "$c_name[$_]\n" } @main_group if $groupcou != 0;
	print "\n</textarea>\n";
}

sub groupview {
	print "　グループ枚数　現在$groupcou枚\n";
	print qq|　　<small><input type="checkbox" name="allchk" onclick="chkCB();" class="none">全チェック</small><br><br>\n|;
	if($groupcou != 0){
		foreach my $i(0 .. $#main_group){
			$j = $main_group[$i];
			print qq|<input type="checkbox" name="del$main_num[$i]" class="none">\n|;
			&print_line;
			print "<br>\n";
		}
	}
}

sub put_ini{
	return unless $id;
	$P{'pregroup'} = join(",",@group);
	&pfl_write($id);
}

sub groupread{
	return unless -e "${player_dir}/".$id.".cgi";
	&pfl_read($id);
	my $cou = 0;
	foreach my $i(1 .. $maxgroup){
		if(!($P{"group$i"})){ $dnam[$i] = "記録なし"; @{$group[$i]} = (); next; }
		else{
			($dnam[$i],$dcon[$i]) = split(/-/,$P{"group$i"});
			$cou = $i;
		}
	}
	$P{'usegroup'} = $cou if $cou && !($P{'usegroup'});
	@group = $P{'pregroup'} ? split(/,/,$P{'pregroup'}) : $P{'usegroup'} ? split(/,/,$dcon[$P{'usegroup'}]) : ();
}

sub set_cookie{ 
	($sec,$min,$hour,$mday,$mon,$year) = gmtime(time + 30*24*60*60);
	$gdate = sprintf("%02d\-%s\-%04d %02d:%02d:%02d", $mday, ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mon], $year + 1900, $hour, $min, $sec);
	$cook = "id:$F{'id'},pass:$F{'pass'},pc:$pc_chk";
	print "Set-Cookie: duel=$cook; expires=$gdate GMT\n";
}

sub get_cookie{
	$cookies = $ENV{'HTTP_COOKIE'};
	@pairs = split(/;/,$cookies);
	foreach $pair(@pairs){
		($name,$value) = split(/=/,$pair);
		$name =~ s/ //g;
		$D{$name} = $value;
	}
	@pairs = split(/,/,$D{'duel'});
	foreach $pair(@pairs){
		($name,$value) = split(/:/,$pair);
		$C{$name} = $value;
	}
	$c_id = $C{'id'};
	$c_pass = $C{'pass'};
	$pc_chk = $C{'pc'};
}

sub decode2 {
	$id = $F{'id'};
	$pass = $F{'pass'}; $pass =~ s/\.//g; $pass =~ s/\///g;
	&error("IDが入力されていません") unless $id;
	&error("パスワードが入力されていません。") unless $pass;
}