sub act_cancel {
  &regist("null","$pn[$u_side]は行動をキャンセルした。");
  $chudan_flg = ""; $trigger_flg = ""; @syori = ();
  @btl = ();
  unshift(@{$deck[$u_side]}, @res, @res2);

  @res = ();
  @res2 = ();
  &control_chk;
}

sub drop_admit {
  if(!$end_flg) {
    &regist("null","$pn[$u_side]は$pn[$u_side2]に退室許可を出した。");
    $sur_flg[$u_side2] = 1;
  } else {
    &com_error("対戦していない状態では退室許可を出す必要はありません");
  }
}

sub drop_admit2 {
  if(!$end_flg) {
    &regist("null","$P{'name'}は$pn[$F{'tp'}]に退室許可を出した。");
    $sur_flg[$F{'tp'}] = 1;
  } else {
    &com_error("対戦していない状態では退室許可を出す必要はありません");
  }
}

sub kakunin {
  &regist("", "$pn[$u_side]は$pn[$u_side2]に確認を取った。", "system");
  unshift @syori, "s-$u_side2<>t-回答をしたら完了してください。<>m-kakunin_sel<>o-完了する";
}

sub kakunin_sel {
  shift @syori;
  &regist("", "$pn[$u_side]は回答を完了した。", "system");
}

sub rcom {
  &reverse_auth();
  &regist("", "操作権限を入れ替えました。", "system");
}

sub reverse_auth {
  $reverse_flg = 1 - $reverse_flg;
  $u_side = (($turn2 - 1) xor $reverse_flg) + 1;
  $u_side2 = 3 - $u_side;
}

sub janken {
  &regist("", "プレイヤー同士でジャンケンをする！", "system");
  unshift @syori, "t-ジャンケンの手を選んでください<>m-janken_sel<>o-決定";
  $chudan_flg = "1";
}

sub nuisance {
  &regist("null","$pn[$u_side]は荒らし報告を行った。");
# &regist("null","$pn[$u_side2]に退室許可が出された。");
# $sur_flg[$u_side2] = 1;

  my @nui_id = ();
  $nui_id[1] = $nid1;
  $nui_id[2] = $nid2;
  my @nui_name = ();
  $nui_name[1] = $nnm1;
  $nui_name[2] = $nnm2;

  my @numlogs = ();
  &filelock("${room}_log");
  open(DB,"room/".$roomst.$room."_log.cgi");
  while (<DB>) {
    my ($msgman,$msg,$msgmode) = split(/<>/,$_);
    $msg =~ s/<.*>//g;
    if(($msgmode eq "system") || ($msgmode eq "tap") || ($msgmode eq "message") || ($msgmode eq "message1") || ($msgmode eq "message2") || ($msgmode eq "admin")) {
      push(@numlogs, $_);
    }
  }
  close(DB);
  &fileunlock("${room}_log");

  &filelock("nuisance");
  open(IN,"nuisance/nui_list.dat");
  @nuis = <IN>;
  close(IN);
  my $n_new = int(shift(@nuis));
  my $flag = 0;
  foreach(@nuis) {
    my($n_num, $n_roomid, $n_user1id, $n_user1name, $n_user2id, $n_user2name, $n_comment, $n_time, $n_solve, $n_admcom) = split(/<>/, $_);
    if(($n_roomid eq $roomid) && ($n_user1id eq $nui_id[$u_side]) && ($n_user2id eq $nui_id[$u_side2])) {
      $_ = "$n_num<>$roomid<>$nui_id[$u_side]<>$nui_name[$u_side]<>$nui_id[$u_side2]<>$nui_name[$u_side2]<>$F{'nuicom'}<>" . time ."<>0<><>\n";
      $flag = 1;
      last;
    }
  }
  if(!$flag) {
    $n_new ++;
    unshift(@nuis, "$n_new<>$roomid<>$nui_id[$u_side]<>$nui_name[$u_side]<>$nui_id[$u_side2]<>$nui_name[$u_side2]<>$F{'nuicom'}<>" . time ."<>0<><>\n");
    unshift(@nuis, "$n_new\n");
  }

  open(OUT,">nuisance/log/${roomid}_log") || &error("ログファイルに書き込めません");
  print OUT @numlogs;
  close(OUT);
  open(OUT,">nuisance/nui_list.dat") || &error("報告リストファイルに書き込めません");
  print OUT @nuis;
  close(OUT);
  &fileunlock("nuisance");

  unless($end_flg) {

#   if(($room =~ /^t/) && ($date[$u_side] - $date[$u_side2] > 60 * 60 * 24)) {
    if(($room !~ /^t/) && ($date[$u_side] - $date[$u_side2] > $natime * 60)) {
      &s_mes("$natime分間行動がないため、$pn[$u_side2]さんを強制退室させます。");
      $timed_up = 1;
    }

    if($timed_up) {
      $sur_flg[$u_side] = 0;
      if(!$sur_flg[$u_side2] || $room =~ /^t/) {
        if($room !~ /^t/) {
          &s_mes("退室許可が出ていないので、$pn[$u_side2]は負けになります。");
        }
        $lp[$u_side] = 1;
        $lp[$u_side2] = 0;
        $sr[$u_side] = 0;
        $sr[$u_side2] = 1;
        &end_game;
      }
      if($room !~ /^t/) {
        &all_clr($u_side2);
        &deck_reload($u_side);
      }
    }
  }

}

#--------------------------------------------------------

sub draw {    # ドロー
# &com_error("先攻は１ターン目にドローすることはできません") if $turn == 1 && $phase == 1 && $u_side == $turn2;
# &com_error("$phasestr[$phase]にはドローはできません") if $phase == 2;
  &com_error("山札がないのでドローできません") if($#{$deck[$u_side]} < 0);
  &s_mes("$pn[$u_side]のドロー！");
  my $cardno = shift @{$deck[$u_side]};
  unshift @{$hand[$u_side]}, $cardno;
  if ($#{$deck[$u_side]} < 0) {
    &s_mes("$pn[$u_side]の山札が尽きた！");
    $lp[$u_side] = 0;
    &end_game;
  }
  if (&c_chk("光神龍スペル・デル・フィン", $u_side2) || &c_chk("魔流星アモン・ベルス", $u_side2) || &c_chk("鎧亜の邪聖ギル・ダグラス")) {
    &s_mes("《$c_name[$cardno]》を引いた。");
  } else {
    &e_mes("《$c_name[$cardno]》を引いた", $u_side);
  }
}

#--------------------------------------------------------

sub del_null {  # 指定配列の空きを消去
  local *arr = $_[0]; my $ind = $_[1];
  @{$arr[$ind]} = grep $_ ne "", @{$arr[$ind]};
}

sub shuffle { # 指定配列をランダムに並び替える
  local *arr = $_[0]; my $ind = $_[1]; my @out = ();
  push @out, splice @{$arr[$ind]}, rand @{$arr[$ind]}, 1 while @{$arr[$ind]};
  @{$arr[$ind]} = @out;
}

sub shuffle1 {
# &com_error("$phasestr[$phase]にはシャッフルはできません") if $phase =~ /[12]/;
  &shuffle(*deck, $u_side);
  &regist("", "$pn[$u_side]は山札をシャッフルした。", "system");
}

#--------------------------------------------------------

sub tap {   # タップ／アンタップ
# &com_error("$phasestr[$phase]にはタップ／アンタップはできません") if $phase =~ /[12]/;
  map { push @fsel, $1 if $_ =~ /^fsel(\d+)/ } keys(%F);
  map { $f_tap[$_] = $f_tap[$_] ? "" : "1";
      &t_mes(sprintf "$pn[$u_side]は%sを%sタップした。", &card_name_sub($_), $f_tap[$_] ? "" : "アン");
    } @fsel;
  undef @fsel;
}

#--------------------------------------------------------

sub battle {  # バトル可能かどうかのチェック
  &com_error("自分のターンではないので攻撃できません") if $u_side != $turn2;
# &com_error("バトルはバトルフェイズにしか行えません") if $phase != 4;
  &com_error("バトル処理中です") if $trigger_flg;
  &com_error("自分のバトルゾーンに攻撃できるクリーチャーがいません") unless grep $fld[$_] ne "" && !($f_tap[$_]), @{$fw1[$u_side]};
  @btl = ($u_side, $u_side2, undef, undef, "anonymous");
  $btl[8] = "1" if $F{'rush'};
  $chudan_flg = "1";
  unshift @syori, "t-攻撃するクリーチャーを選択してください<>m-battle_cre_chk<>o-決定";
}

sub battle_cre_chk {  # 攻撃するクリーチャーのチェック
  &com_error("攻撃するクリーチャーが指定されていません") if $F{'attack_from'} eq "";
  $btl[2] = $F{'attack_from'};
  $btl[6] = $F{"unblock$btl[2]"} ? "1" : undef;
  $btl[7] = $F{"double$btl[2]"} ? $F{"double$btl[2]"}: undef;
  &syori_clr;
  undef @unblock; undef @double;
  unless (grep $fld[$_] ne "", @{$fw1[$btl[1]]}) {
    $f_tap[$btl[2]] = "1";
    $btl[4] = "player";
    unless (&shield_chk($btl[1])) {
      &lemon_chk;
    } else {
      &s_mes(sprintf "%sはシールドへの攻撃を宣言した！", &card_name_sub($btl[2]));
      &attack_trigger;
    }
  } else {
    unshift @syori, "t-攻撃対象を選択してください<>m-taisyo_sel<>o-プレイヤー::クリーチャー";
  }
}

sub taisyo_sel {    # 攻撃対象の選択
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  $f_tap[$btl[2]] = "1";
  shift @syori;
  $btl[4] = $F{'run_select'} ? "player" : "creature";
  if ($F{'run_select'}) {
    &s_mes(sprintf "%sは%s攻撃を宣言した！", &card_name_sub($btl[2]), &shield_chk($btl[1]) ? "シールドへの" : "プレイヤーへの直接");
    &attack_trigger;
  } else {
    &syori_clr;
    unshift @syori, "t-攻撃対象のクリーチャーを選択してください<>m-attacked_cre_sel<>o-決定";
  }
}

sub attacked_cre_sel {  # 攻撃対象のクリーチャーを選択
  &com_error("攻撃対象のクリーチャーが選択されていません", $btl[0]) if $F{'attack_to'} eq "";
  $btl[3] = $F{'attack_to'};
  &syori_clr;
  &s_mes(sprintf "%sは%sへの攻撃を宣言した！", &card_name_sub($btl[2]), &card_name_sub($btl[3]));
  &attack_trigger;
}

sub attack_trigger {  # アタックトリガーの処理
  my $atk = $fld[$btl[2]];
  &s_mes("ターボラッシュ！") if $btl[8] && &k_chk($atk, 10);
  if ($c_name[$atk] eq "鎧亜の凄技ジョゼ・ウィルバート") {  # ジョゼ
    &s_mes("《$c_name[$atk]》の能力発動！　プレイヤー同士でジャンケンをする！");
    unshift @syori, "t-ジャンケンの手を選んでください<>m-janken_sel<>o-決定<>g-battle";
    $trigger_flg = "1";
  } elsif (&k_chk($atk, 19) && &tri_chk($atk, 2)) {     # メテオバーン
    if ($c_name[$atk] eq "超神星ペテルギウス・ファイナルキャノン" && 5 <= $shinka[$btl[2]] =~ tr/-/-/) {
      unshift @syori, "s-$btl[0]<>t-メガメテオバーン６を使いますか？<>m-meteo_sel<>o-使う::使わない<>g-battle";
      $trigger_flg = "1";
      @res = ($btl[2]);
    } elsif ($c_name[$atk] ne "超神星ペテルギウス・ファイナルキャノン" && $shinka[$btl[2]]) {
      unshift @syori, "s-$btl[0]<>t-メテオバーンを使いますか？<>m-meteo_sel<>o-使う::使わない<>g-battle";
      $trigger_flg = "1";
      @res = ($btl[2]);
    } else {
      &attacked_trigger;
    }
  } elsif ((&k_chk($atk, 10) && &tri_chk($atk, 2) && $btl[8])         # ターボラッシュでのアタックトリガー
    || (&k_chk($atk, 16) && &tri_chk($atk, 2) && 6 < &morph_chk($atk))    # メタモーフでのアタックトリガー
    || ($atk =~ /\-/ && ($atk =~ /1711|1837|1894|1962/))          # Ｇ・リンク中のアタックトリガー
    || (!(&k_chk($atk, 10)) && !(&k_chk($atk, 16)) && &tri_chk($atk, 2))  # 普通のアタックトリガー
    || ((&k_chk($atk, 4) || &c_chk("シータ・トゥレイト")) && (grep &tri_chk($fld[$_], 2) && &k_chk($fld[$_],4), @{$fw1[$u_side]}))
                                        # サバイバーのアタックトリガー
    ||  &c_chk("疾風の守護者スール・ミース")
    || (&c_chk("ムシャ・ルピア") && &card_name_sub($btl[2]) =~ /ボルメテウス・武者・ドラゴン/)
    || (&c_chk("衝撃のロウバンレイ") && &syu_chk($atk, 54, 61) && grep ($fld[$_] ne "" && $f_block[$_], @{$fw1[$btl[1]]}) > 0)
    || ((&c_chk("無双竜機ドルザーク") || &c_chk("緑神龍バルガザルムス")) && (&syu_chk($atk, 44, 50, 62, 66, 82, 83) || (&syu_chk($atk, 56) && $btl[9]) || &cloth_chk($atk, 1106, 2050) || &accel_chk2($btl[2], "武装兵ミステリアス", "開龍妖精フィーフィー")))
    || (&c_chk("悪魔聖霊アウゼス") && (&syu_chk($atk, 11, 41) || &accel_chk2($btl[2], "精撃の使徒アリッサ", "悪魔怪人デスブラッド")))
    || ((&syu_chk($atk, 50) || &cloth_chk($atk, 1106, 2050) || (&syu_chk($atk, 56) && $btl[9])) && !($c_evo[$atk]) && &cloth_chk($btl[2], 1299)) # プロミネンス・カタストロフィー
    || &cloth_chk($btl[2], 1166, 1170, 1171, 1172, 1230, 1296, 1297, 2050, 2121, 2145, 2184, 2185, 2201, 2220, 2237)  # クロスギアによるアタックトリガー
    || (&c_chk("黒龍王ダーク・ジオス") && &syu_chk($atk, 44, 50, 62, 66, 82, 83))
    || (&c_chk("封魔ガルプルス", 3) && &syu_chk($atk, 38))
    || &accel_chk2($btl[2], "戦技の化身", "風来の股旅ビワノシン", "大神秘ハルサ") # アクセルによるアタックトリガー
  ) {
    if (&c_chk("疾風の守護者スール・ミース")) {
      &s_mes("《疾風の守護者スール・ミース》の力で相手クリーチャーを１体タップできる！");
    } elsif (&c_chk("ムシャ・ルピア") && &card_name_sub($btl[2]) =~ /ボルメテウス・武者・ドラゴン/) {
      &s_mes("《ムシャ・ルピア》の力で《ボルメテウス・武者・ドラゴン》をサポート！　山札を１枚、シールドに加えることができる！");
    } elsif (&c_chk("衝撃のロウバンレイ") && &syu_chk($atk, 54, 61) && grep $fld[$_] ne "" && $f_block[$_], @{$fw1[$btl[1]]} > 0) {
      &s_mes("《衝撃のロウバンレイ》の能力発動！　相手のブロッカーを１体破壊！");
    } elsif (&syu_chk($atk, 44, 50, 62, 66, 82, 83) || (&syu_chk($atk, 56) && $btl[9]) || &cloth_chk($atk, 1106, 2050) || &accel_chk2($btl[2], "武装兵ミステリアス", "開龍妖精フィーフィー")) {
      if (&c_chk("無双竜機ドルザーク")) {
        &s_mes("《無双竜機ドルザーク》の能力発動！　相手クリーチャーを１体マナに送る！");
      } else {
        &s_mes(sprintf "%sの能力発動！", &card_name_sub($btl[2]));
      }
    } elsif (&c_chk("悪魔聖霊アウゼス") && (&syu_chk($atk, 11, 41) || &accel_chk2($btl[2], "精撃の使徒アリッサ", "悪魔怪人デスブラッド"))) {
      &s_mes("《悪魔聖霊アウゼス》の能力発動！　相手のタップされているクリーチャーを１体破壊！");
    } elsif (&c_chk("黒龍王ダーク・ジオス") && &syu_chk($atk, 44, 50, 62, 66, 82, 83)){
      &s_mes("《黒龍王ダーク・ジオス》の能力発動！　相手はクリーチャーを１体破壊しなければならない！");
    } elsif (&c_chk("封魔ガルプルス", 3) && &syu_chk($atk, 38)) {
      &s_mes("《封魔ガルプルス》の能力発動！　プレイヤーはお互いに手札を１枚捨てなければならない！");
    } elsif (&cloth_chk($btl[2], 1166, 1170, 1171, 1172, 1230, 1296, 1297, 1299, 2050, 2121, 2145, 2184, 2185, 2201, 2220)){
      &s_mes("クロスギアの効果発動！");
    } else {
      &s_mes("アタックトリガー発動！");
    }
    $chudan_flg = ""; $trigger_flg = "1";
    unshift @syori, "t-アタックトリガーの処理を終了しますか？<>m-attack_trigger_end<>o-終了する";
  } else {
    &attacked_trigger;
  }
}

sub attacked_trigger {
  if (&castle_chk($btl[1], 2267)) { # 超鯱城
    &s_mes("《超鯱城》の能力発動！　相手のパワー2000以下のクリーチャーをすべて破壊する！");
    unshift @syori, "s-$btl[1]<>t-《超鯱城》の能力の処理を終了しますか？<>m-attacked_sel<>o-終了する";
    $chudan_flg = $trigger_flg = "1";
  } elsif ((&ninja_chk($btl[1])) && !($btl[10])) {
    unshift @syori, "s-$btl[1]<>t-ニンジャ・ストライクを使いますか？<>m-ninja_sel<>o-使う::使わない<>g-attack<>p-1";
    $trigger_flg = $chudan_flg = "1";
  } elsif (&c_chk("ミラクル・ルンバ", $btl[1]) && $btl[4] eq "player") {
    &s_mes("《ミラクル・ルンバ》の能力発動！　自分のマナゾーンにない文明の数、マナゾーンのカードをタップしないと攻撃できない！");
    unshift @syori, "t-攻撃を続行しますか？<>m-runba_sel<>o-続行する::中止する";
    $chudan_flg = ""; $trigger_flg = "1";
  } elsif (&c_chk("紅玉の守護者リオ・レンティス", $btl[1])) {
    unshift @syori, "s-$btl[$btl[1]]<>t-《紅玉の守護者リオ・レンティス》の能力を使いますか？<>m-attacked_trigger_sel<>o-使う::使わない";
    $chudan_flg = $trigger_flg = "1";
  } elsif ((&c_chk("アクア・アンカー", $btl[1]) || (&c_chk("ドルンカ", $btl[1]) && &bun_chk($fld[$btl[2]], 2, 3))) && !($doru_flg)) {
    my $cre = &c_chk("アクア・アンカー", $btl[1]) ? "アクア・アンカー" : "ドルンカ";
    &s_mes("《$cre》の能力発動！");
    unshift @syori, "s-$btl[1]<>t-《$cre》の能力の処理を終了しますか？<>m-doru_end<>o-終了する";
    $chudan_flg = ""; $trigger_flg = "1";
    $chudan = "$cre";
  } elsif (&meteo_chk("聖帝ファルマハート", $btl[1]) || &meteo_chk("魔皇バルパス", 3)) {
    unshift @syori, sprintf"s-%s<>t-メテオバーンを使いますか？<>m-meteo_sel<>o-使う::使わない<>g-battle", &meteo_chk("魔皇バルパス", $btl[0]) ? $btl[0] : $btl[1];
    $chudan_flg = $trigger_flg = "1";
  } else {
    &s_mes("バトルチェック中…");
    unshift @syori, "s-$btl[1]<>t-バトルを続けますか？<>m-attacked_sel<>o-続ける";
    $chudan_flg = $trigger_flg = "1";
  }
}

sub castle_chk {  # 指定サイドに指定された城があるか否かのチェック
  my ($side, $castle) = @_;
  return grep $f_cloth[$_] =~ /$castle/ && $fld[$_] ne "", @{$fw3[$side]};
}

sub runba_sel {   # ミラクル・ルンバの処理
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    &s_mes("$pn[$btl[0]]はマナを支払い攻撃を続行！");
    $chudan_flg = "1"; $trigger_flg = "";
    &block_chk;
  } else {
    &s_mes("$pn[$btl[0]]は攻撃を中止した。");
    &battle_clr;
  }
}

sub block_chk {   # ブロック可能か否かのチェック
  shift @syori;
  $chudan_flg = $trigger_flg = $btl[10] = "";
  if ($btl[6]) {
    &s_mes("このクリーチャーはブロックできない！");
    &unblocked_trigger;
  } else {
    if (@res = grep $fld[$_] ne "" && $f_block[$_] && !($f_tap[$_]), @{$fw1[$btl[1]]}) {
      unshift @syori, "s-$btl[1]<>t-ブロックしますか？<>m-block_sel<>o-する::しない";
      $chudan_flg = $trigger_flg = "1";
    } else {
      &unblocked_trigger;
    }
  }
}

sub block_sel {   # ブロッカーの選択
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    &com_error("ブロッカーを指定してください", $btl[1]) if $F{'select'} eq "";
    $btl[3] = $F{'select'};
    $btl[4] = "creature";
    $f_tap[$btl[3]] = "1";
    &s_mes(sprintf "$pn[$btl[1]]は%sでブロック！", &card_name_sub($btl[3]));
    undef @res;
    &syori_clr;
    if (&tri_chk($fld[$btl[2]], 3)) {
      &s_mes("ブロックトリガー発動！");
      $chudan_flg = ""; $trigger_flg = "1";
      unshift @syori, "s-$btl[0]<>t-ブロックトリガーの処理を終了しますか？<>m-block_sel2<>o-終了する";
    } else {
      &blocked_trigger;
    }
  } else {
    &s_mes("$pn[$btl[1]]はブロックしなかった。");
    undef @res;
    &syori_clr;
    &unblocked_trigger;
  }
}

sub unblocked_trigger {   # ブロックされなかった場合の処理
  if ($btl[4] eq "player" && (&tri_chk($fld[$btl[2]], 4) || &cloth_chk($btl[2], 1097, 1100) || &accel_chk2($btl[2], "ギガザンダ", "シンカイドウザン", "武装竜鬼バルガゼニガタ"))) {
    &s_mes(sprintf "%sの攻撃はブロックされなかった！", &card_name_sub($btl[2]));
    if (&c_chk("封魔バーガンティス", $btl[1]) && -1 < $#{$hand[$btl[1]]}) {
      &s_mes("《封魔バーガンティス》の能力発動！　$pn[$btl[1]]は手札をすべて捨てなければならない！");
      $chudan_flg = ""; $trigger_flg = "1";
      unshift @syori, "s-$btl[1]<>t-手札をすべて捨てましたか？<>m-bagantis_end<>o-捨てた";
    }
    &s_mes(sprintf "%sの特殊能力発動！", &tri_chk($fld[$btl[2]], 4) ? &card_name_sub($btl[2]) : $f_cloth[$btl[2]] =~ /1097/ ? "$c_name[1097]":"$c_name[1100]");
    if ($c_name[$fld[$btl[2]]] eq "聖剣炎獣バーレスク") {
      $skip_flg = "1";
      &s_mes("このターンの後、$pn[$btl[0]]のターンがもう一度行われる！");
      &taisyo_chk;
    } elsif ($c_name[$fld[$btl[2]]] eq "アクア・マスター") {
      unless (&shield_chk($btl[1])) {
        &s_mes("$pn[$btl[1]]のシールドが１枚もないので、シールドを表向きにできなかった。");
        &taisyo_chk;
      } else {
        $trigger_flg = "1";
        unshift @syori, "s-$btl[0]<>t-表向きにするシールドを選んでください<>m-block_trigger_end<>o-決定";
      }
    } else {
      $chudan_flg = ""; $trigger_flg = "1";
      unshift @syori, sprintf "s-$btl[0]<>t-%sの特殊能力の処理を終了しますか？<>m-block_trigger_end<>o-終了する",
        &tri_chk($fld[$btl[2]], 4) ? &card_name_sub($btl[2]) :
        &cloth_chk($btl[2], 1097) ? "グロリアス・ヘブンズアーム" : "タイフーン・バズーカ";
    }
  } else {
    &taisyo_chk;
  }
}

sub bagantis_end {      # 封魔バーガンティスの処理
  return if (!($F{'run_select'}) || !($btl[2]));
  &com_error("手札をすべて捨ててください", $btl[1]) if -1 < $#{$hand[$btl[1]]};
  &s_mes("$pn[$btl[1]]は封魔バーガンティスの能力の処理を終了した。");
  &syori_clr;
  $trigger_flg = ""; $chudan_flg = "1";
  &unblocked_trigger;
}

sub block_trigger_end {   # ブロックされなかったトリガー終了の処理
  return if (!($F{'run_select'}) || !($btl[2]));
  if (&card_name_sub($btl[2]) =~ /アクア・マスター/) {
    map { push @fsel, $1 if $_ =~ /^fsel(\d+)/ } keys(%F);
    &com_error(sprintf "表向きに%s", $#fsel < 0 ? "するシールドを選んでください" : "できるシールドは１枚だけです") if $#fsel != 0;
    my $fldno = $fsel[0];
    &which_side($fldno);
    &com_error(sprintf "表向きにできるのは%sシールドだけです", $area != 2 ? "" : "相手の") if $area != 2 || $l_side != $btl[1];
    $fld[$fldno] .= "-s";
    &s_mes("《アクア・マスター》の能力で相手のシールドを１枚、表向きにした！");
  }
  &s_mes(sprintf "$pn[$btl[0]]は%sの特殊能力の処理を終了した。", &card_name_sub($btl[2]));
  undef @fsel;
  &syori_clr;
  $chudan_flg = "1"; $trigger_flg = "";
  &taisyo_chk;
}

sub blocked_trigger {   # 相手がブロックした時のトリガー処理
  if (&ninja_chk($btl[0]) && !($btl[10])) {
    unshift @syori, "s-$btl[0]<>t-ニンジャ・ストライクを使いますか？<>m-ninja_sel<>o-使う::使わない<>g-block<>p-1";
    $chudan_flg = $trigger_flg = "1";
  } else {
    &taisyo_chk;
  }
}

sub taisyo_chk {  # 攻撃対象のチェック
  $trigger_flg = $chudan_flg = "";
  if ($btl[4] eq "creature") {
    &battle_run;
  } elsif (!(&shield_chk($btl[1]))) {
    &lemon_chk;
  } else {
    &break_chk;
    &s_mes("《封魔ダンリモス》の効果発動！") if &c_chk("封魔ダンリモス") && &syu_chk($btl[2], 38);
    unshift @syori, sprintf("s-$btl[0]<>t-%s", &c_chk("封魔ダンリモス") && &syu_chk($btl[2], 38) ? "封魔ダンリモスの処理を終了しますか？<>m-danrimos_end<>o-終了する" : "攻撃対象のシールドを選択してください<>m-battle_sel<>o-決定");
  }
}

sub battle_run {      # バトル実行
  if ($btl[4] eq "player") {
    &com_error("シールドが選択されていません", $btl[0]) if $F{'shield'} eq "";
    $btl[3] = $F{'shield'};
    foreach my $i (@{$fw1[$btl[1]]}) {
      if (&k_chk($fld[$i], 33) || ($c_name[$fld[$i]] eq "聖天使グライス・メジキューラ" && 0 < $#{$hand[$btl[1]]})) {
        $chudan = $i;
        $chudan_flg = $trigger_flg = "1";
        unshift @syori, sprintf "s-$btl[1]<>t-$c_name[$fld[$i]]の能力を使いますか？<>m-%s_sel<>o-使う::使わない",
          $c_name[$fld[$i]] eq "聖天使グライス・メジキューラ" ? "meji" : "trap";
        return;
      }
    }
    &shield_break;
  } else {
    if (&dynamo_chk) {
      unshift @syori, sprintf "s-$btl[1]<>t-ダイナモを使いますか？<>m-dynamo_sel<>o-使う::使わない";
      $chudan_flg = $trigger_flg = "1";
      return;
    }
    &s_mes(sprintf "バトル！　%s VS %s！", &card_name_sub($btl[2]), &card_name_sub($btl[3]));
    &battle_clr;
  }
}

sub trap_sel {        # シールド・セイバーの処理
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    $fldno = $chudan;
    &pick_card2;
    &s_mes("$pn[$btl[1]]は《$c_name[$cardno]》の能力を使った！");
    &s_mes("シールドのかわりに《$c_name[$cardno]》を墓地に送った。");
    unshift @{$boti[$btl[1]]}, $cardno;
    $btl[5]-- if $btl[5] != 40;
    $chudan = $trigger_flg = "";
    &syori_clr;
    &breaker;
  } else {
    $chudan = $trigger_flg = "";
    &syori_clr;
    &shield_break;
  }
}

sub meji_sel {        # グライス・メジキューラの処理
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  $chudan = "";
  if ($F{'run_select'}) {
    &s_mes("$pn[$btl[1]]は《聖天使グライス・メジキューラ》の能力を使った！");
    $chudan_flg = "";
    &syori_clr;
    unshift @syori, "s-$btl[1]<>t-手札を２枚捨ててください<>m-meji_end<>o-終了する";
  } else {
    &syori_clr;
    &shield_break;
  }
}

sub break_chk {       # シールドブレイク枚数の決定
  if ($btl[7] == 4) {
    my $crew = 0;
    if (&k_chk($fld[$btl[2]], 4)) {
      $crew = &c_chk("シータ・トゥレイト") ? grep $fld[$_] ne "", @{$fw1[$turn2]} : grep &k_chk($fld[$_], 4), @{$fw1[$turn2]};
    } elsif ($c_name[$fld[$btl[2]]] eq "超竜バハム") {
      $crew = grep &syu_chk($fld[$_], 56), @{$fw1[$turn2]};
    } elsif ($c_name[$fld[$btl[2]]] eq "アルティメット・ドラゴン") {
      $crew = grep &syu_chk($fld[$_], 44, 50, 62, 66, 82, 83), @{$fw1[$turn2]};
      foreach my $i(@{$fw1[$turn2]}){
        $crew++ if
           (&cloth_chk($i, 1106, 2050) && !(&syu_chk($fld[$i], 44, 50, 62, 66, 82, 83)))
        || &accel_chk2($i, "武装兵ミステリアス", "開龍妖精フィーフィー")
        || (&syu_chk($fld[$i], 56) && $btl[9]);
      }
    } elsif ($c_name[$fld[$btl[2]]] eq "超竜ザシャック") {
      $crew = grep &syu_chk($fld[$_], 50), @{$fw1[$turn2]};
      map { $crew++ if (&cloth_chk($_, 1106, 2050) && !(&syu_chk($fld[$_], 50))) || (&syu_chk($fld[$_], 56) && $btl[9]) } @{$fw1[$turn2]};
    } elsif ($c_name[$fld[$btl[2]]] eq "星鎧亜イカロス") {
      $crew = &rainbow_chk;
    } else {
      $crew = grep &syu_chk($fld[$_], $c_syu[$fld[$btl[2]]]), @{$fw1[$turn2]};
    }
    $btl[5] = $crew;
  } else {
    $btl[5] = $btl[7] == 5 ? 40 : $btl[7] == 0 ? 1 : $btl[7] == 1 ? 2 : $btl[7] == 2 ? 3 : 4;
  }
  $btl[5]++ if &cloth_chk($btl[2], 1106, 1171) && $btl[5] != 40;
}

sub shield_break {
  my $atk = $btl[2];
  &s_mes(sprintf "%sはシールドをブレイク！", $atk eq "anonymous" ? "$pn[$btl[0]]" : &card_name_sub($btl[2]));
  unless ($f_cloth[$btl[3]] =~ /^(2234|2236|2255)$/ && 1 < grep $fld[$_] ne "", @{$fw3[$btl[1]]}) {
    @shield = split /-/, $shinka[$btl[3]];
    unshift @shield, $fld[$btl[3]];
    shift @syori;
    $name = join "<br>", map { "《" . $c_name[$_] . "》"; } @shield;
    $fld[$btl[3]] = $shinka[$btl[3]] = "" if $c_name[$fld[$atk]] ne "陽炎の守護者ブルー・メルキス";
    $f_block[$btl[3]] = "";
    $btl[5]-- if $btl[5] != 40;
  }
  if (&k_chk($fld[$atk], 34)) {
    &s_mes("《$c_name[$fld[$atk]]》の力により、シールドは墓地へと送られる！");
    &s_mes("$pn[$btl[1]]の$nameを墓地に送った。");
    @{$boti[$btl[1]]} = (@shield, @{$boti[$btl[1]]});
    undef @shield;
    &breaker;
  } elsif (&accel_chk2($atk, "緑神龍ダグラドルグラン")) {
    &s_mes("《$c_name[$fld[$atk]]》のアクセル能力により、シールドはマナゾーンへと送られる！");
    while (@shield) {
      &fld_chk($btl[1]);
      &which_side($nf3);
      $fld[$nf3] = $_;
    }
    &s_mes("$pn[$btl[1]]の$nameをマナゾーンに送った。");
    &breaker;
  } elsif ($c_name[$fld[$atk]] eq "陽炎の守護者ブルー・メルキス") {
    &s_mes("《$c_name[$fld[$atk]]》の力により、ブレイクしたシールドが表向きになった！");
    $fld[$btl[3]] .= "-s";
    if (&s_tri_chk) {
      &s_mes("$pn[$btl[1]]のシールド・トリガーを$pn[$btl[0]]が発動させた！");
      &syori_clr;
      unshift @syori, "s-$btl[0]<>t-シールド・トリガーの処理を終了しますか？<>m-trigger_sel3<>o-終了する";
      $chudan_flg = "";
    } else {
      &breaker;
    }
  } elsif ($f_cloth[$btl[3]] =~ /^(2234|2236|2255)$/ && 1 < grep $fld[$_] ne "", @{$fw3[$btl[1]]}) {
    $chudan_flg = $trigger_flg = "1";
    unshift @syori, "s-$btl[1]<>t-城の退避能力を使いますか？<>m-castle_trap<>o-使う::使わない";
  } else {
    &s_mes("ブレイクされたシールドが$pn[$btl[1]]の手札となる！");
    &shield_break_sub($name, \@shield);
  }
}

sub shield_break_sub {
  my $name = $_[0]; my $shield = $_[1];
  &s_mes(sprintf "%sの能力発動！　ブレイクされたシールドは$nameだった！", &c_chk("光神龍スペル・デル・フィン") ? "光神龍スペル・デル・フィン" : "宣凶師ルベルス") if &c_chk("宣凶師ルベルス") || &c_chk("光神龍スペル・デル・フィン");
  $trigger_flg = $chudan_flg = "1";
  if (&c_chk("魔聖デス・アルカディア", $btl[1])) {
    $chudan = join "-", @$shield;
    unshift @syori, "s-$btl[1]<>t-魔聖デス・アルカディアの能力を使いますか？<>m-arcadia_sel<>o-使う::使わない";
  } elsif (&s_tri_chk) {
    unshift @syori, "s-$btl[1]<>t-シールド・トリガーを使いますか？<>m-trigger_sel1<>o-使う::使わない";
  } elsif (grep (&strike_chk($_, $btl[1]), @$shield)) {
    @res = grep &tri_chk($_, 6), @{$hand[$btl[1]]};
    unshift @syori, "s-$btl[1]<>t-ストライク・バックを使いますか？<>m-strike_sel1<>o-使う::使わない<>p-1";
  } else {
    @{$hand[$btl[1]]} = (@$shield, @{$hand[$btl[1]]});
    &e_mes("$nameを手に入れた", $btl[1]);
    unshift @syori, "s-$btl[1]<>t-バトルを続けますか？<>m-trigger_sel2<>o-続ける";
  }
  &s_mes("シールドチェック中・・・");
}

sub castle_trap {     # 城の退避能力を使うか否かの選択
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    $syori[0] = "s-$btl[1]<>t-かわりに手札に加えるシールドを選択してください<>m-castle_trap_sel<>o-決定";
  } else {
    $chudan = $trigger_flg = "";
    &syori_clr;
    &shield_break;
  }
}

sub castle_trap_sel {   # 城の退避能力の処理
  return if !($btl[2]) || !($F{'run_select'});
  &com_error("シールドが選択されていません", $btl[1]) if $F{'shield'} eq "";
  &com_error("ブレイクされるシールド以外を選んでください", $btl[1]) if $F{'shield'} == $btl[3];
  &s_mes("《$c_name[$f_cloth[$btl[3]]]》の退避能力発動！　ブレイクされるのとは別のシールドを手札に加える！");
  $btl[3] = $F{'shield'};
  @shield = split /-/, $shinka[$btl[3]];
  unshift @shield, $fld[$btl[3]];
  shift @syori;
  my $name = join "<br>", map { "《" . $c_name[$_] . "》"; } @shield;
  $fld[$btl[3]] = $shinka[$btl[3]] = $f_block[$btl[3]] = "";
  $btl[5]-- if $btl[5] != 40;
  &shield_break_sub($name, \@shield);
}

sub seiryu_chk {
  foreach my $magic (@magic) {
    my ($card, $side, $turn) = split /<>/, $magic;
    return 1 if $card eq "星龍の記憶" && $side == $btl[1];
  }
  return 0;
}

sub s_tri_chk {
  return grep (&tri_chk($_, 1), @shield) || &c_chk("星龍パーフェクト・アース", $btl[1]) || &seiryu_chk || (grep (&syu_chk($_, 0), @shield) && &c_chk("天雷龍姫エリザベス", $btl[1]));
}

sub arcadia_sel {
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    shift @syori;
    unshift @{$boti[$btl[1]]}, $chudan;
    &s_mes("$pn[$btl[1]]はシールドの《$c_name[$chudan]》を墓地に送った！");
    &s_mes("《魔聖デス・アルカディア》の能力発動！　相手のクリーチャーを１体破壊！");
    unshift @syori, "s-$btl[1]<>t-魔聖デス・アルカディアの能力の処理を終了しますか？<>m-arcadia_end<>o-終了する";
    $chudan = $chudan_flg = "";
  } else {
    shift @syori;
    if (&tri_chk($chudan, 1) || &strike_chk($chudan, $btl[1])) {
      $trigger_flg = "1";
      @res = grep &tri_chk($_, 6), @{$hand[$btl[1]]} unless &s_tri_chk;
      my $str = &s_tri_chk ? "s-$btl[1]<>t-シールド・トリガーを使いますか？<>m-trigger_sel1<>o-使う::使わない"
                 : "s-$btl[1]<>t-ストライク・バックを使いますか？<>m-strike_sel1<>o-使う::使わない<>p-1";
      unshift @syori, $str;
    } else {
      &pursue;
      &breaker;
    }
  }
}

sub janken {
  &s_mes("$pn[$u_side]は相手にジャンケン勝負を挑んだ！");
  unshift @syori, "s-$u_side<>t-ジャンケンの手を選んでください<>m-janken_sel<>o-決定";
  $chudan_flg = "1";
}

sub janken_sel  {
  return if !($F{'run_select'});
  &com_error("ジャンケンの手を選んでください") if $F{'janken'} eq "";
  $janken[$u_side] = $F{'janken'} if $janken[$u_side] eq "";
  if ($janken[$u_side2] ne "") {
    &s_mes("$pn[$u_side]は$janken[$u_side]、<br>$pn[$u_side2]は$janken[$u_side2]を出した！");
    if ($janken[$u_side] eq $janken[$u_side2]) {
      &s_mes("あいこだったのでもう一度！");
    } else {
      &syori_p_set;
      my $winner = ($janken[$u_side] eq "グー" && $janken[$u_side2] eq "チョキ")
            || ($janken[$u_side] eq "チョキ" && $janken[$u_side2] eq "パー")
            || ($janken[$u_side] eq "パー" && $janken[$u_side2] eq "グー") ? $u_side : $u_side2;
      &s_mes("$pn[$winner]の勝ち！");
      $trigger_flg = "";
      if ($S{'g'} eq "battle") {
        if ($btl[0] == $winner && $btl[4] eq "player" && $c_name[$fld[$btl[2]]] eq "鎧亜の凄技ジョゼ・ウィルバート") {
          &s_mes("鎧亜の凄技ジョゼ・ウィルバートはこのターン、Ｔ・ブレイカーとなった！");
          $btl[7] = 2;
        }
        &syori_clr;
        undef @janken;
        &attacked_trigger;
      } else {
        $chudan_flg = "";
        &syori_clr;
      }
    }
    undef @janken;
  }
}

sub strike_chk {  # ストライク・バックのチェック
  my ($side) = @_;
  @res = grep &tri_chk($_, 6) && &bun_chk($cno, $c_bun[$_]), (@{$hand[$side]});
}

sub ninja_chk {   # ニンジャ・ストライクのチェック
  my ($side) = $_[0];
  my $mana = &morph_chk($side);
  foreach my $card (@{$hand[$side]}) {
    push @res, $card if ($c_name[$card] =~ /轟火シシガミグレンオー/ && 7 < $mana)
     || ($c_name[$card] =~ /斬隠オロチ|威牙の幻ハンゾウ|光牙王機ゼロカゲ|怒流牙 サイゾウミスト/ && 6 < $mana)
     || ($c_name[$card] =~ /土隠の式神センブーン|怒流牙 佐助の超人|超越男/ && 4 < $mana)
     || ($c_name[$card] =~ /光牙忍ハヤブサマル|斬隠テンサイ・ジャニット|威牙忍ヤミノザンジ|威牙忍クロカゲ/ && 3 < $mana)
     || ($c_name[$card] =~ /土隠風の化身/ && 2 < $mana)
     || ($c_name[$card] =~ /威牙忍ヤミカゼ・ドラグーン/ && 1 < $mana)
     || ($c_name[$card] =~ /光牙忍ライデン/ && 0 < $mana)
  }
  return 1 if -1 < $#res;
  return 0;
}

sub ninja_sel {   # ニンジャ・ストライクの処理
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  if ($F{'run_select'}) {
    &com_error("出すクリーチャーを指定してください") if $F{'select'} eq "";
    $cardno = $F{'select'};
    foreach my $i(0..$#{$hand[$S{'s'}]}) {
      if ($hand[$S{'s'}][$i] == $cardno) { splice @{$hand[$S{'s'}]}, $i, 1; last; }
    }
    &s_mes("ニンジャ・ストライク！　$pn[$S{'s'}]は《$c_name[$cardno]》をバトルゾーンに出した！");
    &fld_chk($S{'s'});
    &put_battle_zone_sub;
    undef @res;
    $syori[0] = "s-$S{'s'}<>t-ニンジャ・ストライクの処理を終了しますか？<>m-ninja_end<>o-終了する<>g-$S{'g'}";
    $btl[10] = "1";
    $chudan_flg = ""; $trigger_flg = "1";
  } else {
    undef @res;
    $chudan_flg = $trigger_flg = "";
    $btl[10] = "1";
    if ($S{'g'} eq "attack") {
      &syori_clr;
      &attacked_trigger;
    } else {
      &syori_clr;
      &blocked_trigger;
    }
  }
}

sub ninja_end {
  return if !($F{'run_select'});
  &syori_p_set;
  &s_mes("$pn[$S{'s'}]はニンジャ・ストライクの処理を終了した。");
  $chudan_flg = "1"; $trigger_flg = "";
  if ($S{'g'} eq "attack") {
    &syori_clr;
    &attacked_trigger;
  } else {
    &syori_clr;
    &blocked_trigger;
  }
}

sub direct_atk {  # ダイレクトアタックの処理
  &s_mes(sprintf "%sの直接攻撃！", &card_name_sub($btl[2]));
  &s_mes("$pn[$btl[1]]に攻撃がヒットした！");
  $lp[$btl[1]] = 0;
  &end_game;
}

sub univ_atk {  # ユニバースの処理
  &s_mes(sprintf "%sの特殊効果発動！", &card_name_sub($btl[2]));
  &s_mes("$pn[$btl[1]]に効果がヒットした！");
  if ($turn < 3)
  {
    # 両者1ターン目のユニバースは負けにする。
    $lp[$btl[0]] = 0;
  }
  else
  {
    $lp[$btl[1]] = 0;
  }
  &end_game;
}

sub lemon_chk {   # フルメタル・レモンのチェック
  if ((&c_chk("剛勇王機フルメタル・レモン", $btl[1]) && 9 < $#{$deck[$btl[1]]}) || &c_chk("光姫聖霊ガブリエラ", $btl[1])) {
    $chudan_flg = $trigger_flg = "1";
    unshift @syori, sprintf "s-$btl[1]<>t-《%s》の能力を使いますか？<>m-%s_sel<>o-使う::使わない",
      &c_chk("剛勇王機フルメタル・レモン", $btl[1]) && 9 < $#{$deck[$btl[1]]} ? "剛勇王機フルメタル・レモン" : "光姫聖霊ガブリエラ",
      &c_chk("剛勇王機フルメタル・レモン", $btl[1]) && 9 < $#{$deck[$btl[1]]} ? "lemon" : "gabriela";
  } else {
#   &direct_atk;
    &s_mes("$c_name[$fld[$btl[2]]]の直接攻撃！");
    unshift(@syori,"s-$btl[1]<>t-あなたの負けです。<>m-last_attack<>o-終了");
  }
}

sub lemon_sel {   # フルメタル・レモン効果実行の処理
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    unshift @{$boti[$btl[1]]}, splice @{$deck[$btl[1]]}, 0, 10;
    &s_mes("《剛勇王機フルメタル・レモン》の能力発動！");
    &s_mes("$pn[$btl[1]]は山札を10枚墓地に送った！");
    &s_mes("$pn[$btl[0]]の勝利は無効化された！");
  } else {
    if (&c_chk("光姫聖霊ガブリエラ", $btl[1])) {
      unshift @syori, sprintf "s-$btl[1]<>t-《光姫聖霊ガブリエラ》の能力を使いますか？<>m-gabriela_sel<>o-使う::使わない";
    } else {
#     &direct_atk;
      &s_mes("$c_name[$fld[$btl[2]]]の直接攻撃！");
      unshift(@syori,"s-$btl[1]<>t-あなたの負けです。<>m-last_attack<>o-終了");
    }
  }
}

sub gabriela_sel {    # 光姫聖霊ガブリエラ効果実行の処理
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    &s_mes("《光姫聖霊ガブリエラ》の能力発動！");
    $fldno = (grep $c_name[$fld[$_]] eq "光姫聖霊ガブリエラ", @{$fw1[$btl[1]]})[0];
    &pick_card2;
    unshift @{$boti[$btl[1]]}, $cardno;
    &s_mes("$pn[$btl[1]]は《光姫聖霊ガブリエラ》を墓地に送った！");
    &s_mes("$pn[$btl[0]]の勝利は無効化された！");
    &s_mes("《光姫聖霊ガブリエラ》の能力により、$pn[$btl[1]]は次のターンの終わりに敗北する！");
    unshift @magic, "光姫聖霊ガブリエラ<>$btl[1]";
    &battle_clr;
  } else {
#   &direct_atk;
    &s_mes("$c_name[$fld[$btl[2]]]の直接攻撃！");
    unshift(@syori,"s-$btl[1]<>t-あなたの負けです。<>m-last_attack<>o-終了");
  }
}

sub trigger_sel1 {  # シールド・トリガー使用の選択
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    &com_error("トリガーを使うカードが指定されていません") if $F{'select'} eq "";
    shift @syori;
    $cardno = splice @shield, $F{'select'}, 1;
    if (&syu_chk($cardno, 0)) {     # 呪文の場合
      &trigger_sel_sub;
      if (&meteo_chk("超神星マーキュリー・ギガブリザード", $btl[0])) {
        $trigger_flg = "1";
        unshift @syori, "s-$btl[0]<>t-メテオバーンを使いますか？<>m-meteo_sel<>o-使う::使わない<>g-merqury<>c-$c_name[$cardno]";
      } else {
        &magic("$c_name[$cardno]", $btl[1]);
      }
    } elsif (&syu_chk($cardno, 1)) {  # クロスギアの場合
      $s_cou = 0;
      &put_gear_chk($cardno, "tri");
      &put_card_dialog($cardno, "tri") if 0 < $s_cou;
    } else {              # クリーチャーの場合
      &put_cre_chk($cardno, "tri");
      if (-1 < $#res) {
        &put_card_dialog($cardno, "tri");
      } else {
        &trigger_sel_sub;
      }
    }
  } else {
    shift @syori;
    if (grep (&strike_chk($_, $btl[1]), @shield)) {
      shift @syori;
      @res = grep (&tri_chk($_, 6), @{$hand[$btl[1]]});
      unshift @syori, "s-$btl[1]<>t-ストライク・バックを使いますか？<>m-strike_sel1<>o-使う::使わない<>p-1";
    } else {
      &pursue;
      &breaker;
    }
  }
}

sub trigger_sel_sub {
  &fld_chk($btl[1]);
  $chudan = $trigger_flg = "";
  &s_mes(sprintf "シールド・トリガー%s！　$c_name[$cardno]%s！", &syu_chk($cardno, 0) ? "発動" : "クリーチャー", &syu_chk($cardno, 0) ? "" : "召喚");
  unshift @syori, "s-$btl[1]<>t-シールド・トリガーの処理を終了しますか？<>m-trigger_sel3<>o-終了する";
  &put_battle_zone_sub;
}

sub trigger_sel2 {
  return if !($F{'run_select'});
  &s_mes("$pn[$btl[1]]はシールド・トリガーの処理を終了した。");
  if ($#shield < 0) {
    &pursue_sub;
    &breaker;
  } else {
    shift @syori;
    $trigger_flg = $chudan_flg = "1";
    if (&s_tri_chk) {
      unshift @syori, "s-$btl[1]<>t-シールド・トリガーを使いますか？<>m-trigger_sel1<>o-使う::使わない";
    } elsif (grep (&strike_chk($_, $btl[1]), @shield)) {
      @res = grep (&tri_chk($_, 6), @{$hand[$btl[1]]});
      unshift @syori, "s-$btl[1]<>t-ストライク・バックを使いますか？<>m-strike_sel1<>o-使う::使わない<>p-1";
    } else {
      &pursue;
      &breaker;
    }
  }
}

sub strike_sel {
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    &com_error("捨てるカードを指定してください", $btl[1]) if $F{'select'} eq "";
    &com_error("使うカードを指定してください", $btl[1]) if $F{'select2'} eq "";
    $cno = splice @shield, $F{'select'}, 1;
    $cardno = $F{'select2'};
    foreach my $i(0..$#{$hand[$btl[1]]}) {
      if ($hand[$btl[1]][$i] == $cardno) { splice @{$hand[$btl[1]]}, $i, 1; last; }
    }
    unshift @{$boti[$btl[1]]}, $cno;
    &s_mes("$pn[$btl[1]]はシールドの《$c_name[$cno]》を墓地に送った！");
    &s_mes(sprintf "ストライク・バック%s", &syu_chk($cardno, 0) ? "超動！　$c_name[$cardno]！" : "クリーチャー！　《$c_name[$cardno]》召還！");
    $syori[0] = "s-$btl[1]<>t-ストライク・バックの処理を終了しますか？<>m-strike_end<>o-終了する";
    &fld_chk($btl[1]);
    &put_battle_zone_sub;
    undef @res;
    $chudan = $chudan_flg = "";
    $trigger_flg = "1";
  } else {
    &pursue;
    &breaker;
  }
}

sub strike_end {
  return if !($F{'run_select'});
  &s_mes("$pn[$btl[1]]はストライク・バックの処理を終了した。");
  if ($#shield < 0) {
    &pursue_sub;
    &breaker;
  } else {
    shift @syori;
    $trigger_flg = $chudan_flg = "1";
    if (grep (&strike_chk($_, $btl[1]), @shield)) {
      @res = grep (&tri_chk($_, 6), @{$hand[$btl[1]]});
      unshift @syori, "s-$btl[1]<>t-ストライク・バックを使いますか？<>m-strike_sel1<>o-使う::使わない<>p-1";
    } else {
      &pursue;
      &breaker;
    }
  }
}

sub pursue {
  my $name = join "", map { "《" . $c_name[$_] . "》"; } @shield;
  @{$hand[$btl[1]]} = (@shield, @{$hand[$btl[1]]});
  &e_mes("$nameを手に入れた", $btl[1]);
  &pursue_sub;
}

sub pursue_sub {
# &s_mes("$phasestr[$phase]続行！");
  &s_mes("ターン続行！");
  $chudan = $trigger_flg = "";
  &syori_clr;
  undef @res; undef @shield;
  $chudan_flg = "1";
}

sub breaker {
  if ($f_cloth[$btl[3]] ne "") {
    my $name = "";
    my @castle = split /-/, $f_cloth[$btl[3]];
    map { $name .= "《$c_name[$_]》" } @castle;
    &s_mes("シールドを要塞化していた城は墓地に送られる！");
    &s_mes("$pn[$btl[1]]の$nameを墓地に送った。");
    $f_cloth[$btl[3]] = "";
    @{$boti[$btl[1]]} = (@castle, @{$boti[$btl[1]]});
  }
  if (!(&shield_chk($btl[1])) || $btl[5] < 1) {
    &battle_clr;
  } else {
    &s_mes(sprintf "%s", $btl[7] == 5 ? "ワールドブレイカー！"
            : $btl[5] == 1 && &cloth_chk($btl[2], 1106, 1171) ? sprintf "%sの力で更にシールドを１枚ブレイク！", &cloth_chk($btl[2], 1106) ? "ファイナル・ドラグアーマー" : "バジュラズ・ソウル"
            : $btl[7] == 1 ? "ダブル・ブレイカー！"
            : $btl[7] == 2 ? "トリプル・ブレイカー！"
            : $btl[7] == 3 ? "クアトロ・ブレイカー！"
            : $c_name[$fld[$btl[2]]] eq "超竜バハム" ? "超竜バハムはドラゴノイドの数だけシールドを破壊する！"
            : "クルー・ブレイカー！"
        );
    unshift @syori, "s-$turn2<>t-攻撃対象のシールドを選択してください<>m-battle_sel<>o-決定";
  }
}

sub meteo_chk {
  my $cre = $_[0];
  my $side = $_[1] ? $_[1] : $u_side;
  my @field = $side == 3 ? (@{$fw1[1]}, @{$fw1[2]}) : (@{$fw1[$side]});
  @res = grep $c_name[$fld[$_]] eq $cre && $shinka[$_] ne "", @field;
  return 1 if -1 < $#res;
  return 0;
}

sub meteo_sel {
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  if ($F{'run_select'}) {
    if ($c_name[$fld[$btl[2]]] =~ /超神星ペテルギウス・ファイナルキャノン|超神星DEATH・ドラゲリオン/) {
      map { push @rsel, $1 if $_ =~ /^rsel(.+)/ } (keys(%F));
      &com_error("墓地に置くカードを６枚指定してください") if $#rsel != 5 && &card_name_sub($btl[2]) =~ /超神星ペテルギウス・ファイナルキャノン/;
      &com_error("墓地に置けるカードは３枚までです") if 2 < $#rsel && &card_name_sub($btl[2]) =~ /超神星DEATH・ドラゲリオン/;
      shift @syori;
      my @name = ();
      foreach $ssel(@rsel) {
        &pick_card3;
        push @name, "《$c_name[$cardno]》";
        unshift @{$boti[$S{'s'}]}, $cardno;
      }
      &del_move2;
      &s_mes(sprintf "$pn[$S{'s'}]は%sの進化元、%sを墓地に送った！", &card_name_sub($btl[2]), join "", @name);
    } else {
      &com_error("墓地に置くカードを指定してください") if $F{'select'} eq "";
      shift @syori;
      $ssel = $F{'select'};
      &pick_card3;
      &del_move2;
      unshift @{$boti[$S{'s'}]}, $cardno;
      &s_mes(sprintf "$pn[$S{'s'}]は%sの進化元、$c_name[$cardno]を墓地に送った！", &card_name_sub($btl[2]));
    }
    if ($c_name[$fld[$btl[2]]] eq "究極銀河ユニバース" && &syu_chk($cardno, 4)){
      unless (grep $_ ne "", (split /-/, $shinka[$btl[2]])) {
        &s_mes("《究極銀河ユニバース》の勝利条件が発動した！");
        unshift(@syori,"s-$btl[1]<>t-あなたの負けです。(両者1ターン目のユニバース効果では、使用した側が敗北します)<>m-universe_attack<>o-終了");
        undef @res;
        $chudan = $chudan_flg = "";
#       &end_game;
      }
    } else {
      &s_mes(sprintf "%s発動！", $c_name[$fld[$btl[2]]] eq "超神星ペテルギウス・ファイナルキャノン" ? "メガメテオバーン６" : "メテオバーン");
      unshift @syori, sprintf "s-$S{'s'}<>t-%sの処理を終了しますか？<>m-meteo_end<>o-終了する<>g-$S{'g'}", $c_name[$fld[$btl[2]]] eq "超神星ペテルギウス・ファイナルキャノン" ? "メガメテオバーン６" : "メテオバーン";
      undef @res;
      $chudan = $chudan_flg = "";
    }
  } else {
    undef @res; shift @syori;
    $trigger_flg = $chudan = "";
    if ($S{'g'} eq "battle") {
      $chudan_flg = "1";
      &attacked_trigger;
    } elsif ($S{'g'} eq "merqury") {
      &magic($S{'c'}, $u_side2);
    }
  }
}

sub meteo_end {
  return if !($F{'run_select'});
  &syori_p_set;
  &s_mes("$pn[$S{'s'}]はメテオバーンの処理を終了した。");
  &syori_clr;
  &attacked_trigger;
}

sub dynamo_sel {
  return if !($btl[2]) || (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    map { push @rsel, $1 if $_ =~ /^rsel(\d+)/ } (keys(%F));
    &com_error("ダイナモを使うクリーチャーが指定されていません") if $#rsel < 0;
    &s_mes("$pn[$btl[1]]はダイナモを使った！");
    foreach my $fno(@rsel) {
      next if $fno eq "";
      $f_tap[$fno] = "1";
      &s_mes(sprintf "%sのパワーと能力を%sにプラス！", &card_name_sub($fno), &card_name_sub($btl[3]));
    }
  }
  &s_mes(sprintf "バトル！　%s VS %s！", &card_name_sub($btl[2]), &card_name_sub($btl[3]));
  &battle_clr;
}

sub shield_chk {  # シールドの数を返す
  return grep $fld[$_] ne "", @{$fw3[$_[0]]};
}

sub morph_chk {   # 指定サイドのマナゾーンの数を返す
  return grep $fld[$_] ne "", @{$fw4[$_[0]]};
}

sub c_chk {     # 指定クリーチャーが指定サイドにいるかどうかを返す
  my $cre = $_[0];
  my $side = $_[1] ? $_[1] : $u_side;
  my @field = $side == 3 ? (@{$fw1[1]}, @{$fw1[2]}) : @{$fw1[$side]};
  return grep $c_name[$fld[$_]] eq $cre, @field;
}

sub tri_chk {   # 指定カードが指定トリガーを持つかどうかを返す
  my ($card, $chk) = @_;
  foreach my $cre (split /-/, $card) {
    foreach my $tri (split /,/, $c_tri[$cre]) { return 1 if $tri == $chk; }
  }
  return 0;
}

sub dynamo_chk {  # バトル可能なダイナモ持ちクリーチャーの配列を返す
  @res = grep &k_chk($fld[$_], 20) && $_ != $btl[3] && $f_tap[$_] ne "1", @{$fw1[$btl[1]]};
  return @res;
}

sub battle_clr {
  $chudan = $chudan_flg = $trigger_flg = "";
  undef @btl; undef @res; undef @res2; undef @syori; undef %F; undef %S;
}

sub syori_clr {
  shift @syori; undef %F; undef %S;
}

sub sel_end {
  return if !($F{'run_select'}) || !($btl[2]);
  my $mode = $F{'mode'};
  if ($mode =~ /doru_end|arcadia_end/) {
    &s_mes(sprintf "$pn[$btl[1]]は%sの能力の処理を終了した。", $mode eq "doru_end" ? "$chudan" : "魔聖デス・アルカディア");
  } elsif ($mode eq "meji_end") {
    &s_mes("$pn[$btl[1]]は手札を２枚捨ててシールドを守った！");
    $btl[5]-- if $btl[5] != 40;
  } elsif ($mode eq "last_attack") {
    &direct_atk;
  } elsif ($mode eq "universe_attack") {
    &univ_atk;
  } elsif ($mode !~ /trigger_sel2|danrimos_end/) {
    &s_mes(sprintf "%sは%s・トリガーの処理を終了した。",
      $mode eq "trigger_sel3" ? $pn[$btl[1]] : $pn[$btl[0]],
      $mode eq "attack_trigger_end" ? "アタック" : $mode eq "block_sel" ? "ブロック" : "シールド");
  }
  &pursue_sub;
  if ($mode eq "attack_trigger_end" || $mode eq "doru_end") {
    $doru_flg = "1" if $mode eq "doru_end";
    &attacked_trigger;
  } elsif ($mode eq "block_sel") {
    &blocked_trigger;
  } else {
    &breaker;
  }
}

#--------------------------------------------------------

sub break_btn {
  &com_error("自分のターンではないので、シールドをブレイクすることはできません") if $u_side != $turn2;
# &com_error("$phasestr[$phase]にシールドをブレイクすることはできません") if $phase =~ /[12]/;
  &com_error("バトル処理中にシールドをブレイクすることはできません") if $btl[0] ne "";
  @btl = ($u_side, $u_side2, "anonymous", undef, "player");
  &com_error("相手のシールドが１枚もないので、シールドをブレイクすることはできません") unless &shield_chk($u_side2);
  unshift @syori, "s-$btl[0]<>t-ブレイクするシールドを選択してください<>m-battle_sel<>o-決定";
}

#--------------------------------------------------------

sub change_phase {
  &com_error("自分のターンではないので、フェイズ移動はできません") if $u_side != $turn2;
  &com_error("バトル処理中にターンを終了させることはできません") if $btl[0] ne "";
# if ($phase != 4) {
#   $phase++;
# } else {
    map { $f_tap[$_] = "" } @{$fw3[$turn2]};
    &s_mes("$pn[$turn2]のターンを終了した。");
    foreach my $magic (@magic) {
      my ($card, $side, $t) = split /<>/, $magic;
      if (($card eq "光姫聖霊ガブリエラ" && $side == $turn2) || ($card eq "無双竜機ボルバルザーク" && $t == 2)) {
        &s_mes("《$card》の効果により、$pn[$turn2]はこのゲームに敗北する！");
        $lp[$turn2] = 0;
        &end_game;
      } elsif ($card eq "無双竜機ボルバルザーク" && $t == 1) {
        $turn++;
        $magic = $turn ? join "<>", ($card, $side, $t) : "";
      }
    }
    $turn++;
    $phase = 0;
    $turn2 = 3 - $turn2 if $skip_flg < 1;
    &s_mes(sprintf "$pn[$turn2]の%sターン！", 0 < $skip_flg ? "追加" : "");
    $skip_flg-- if 0 < $skip_flg;
    foreach my $magic (@magic) {
      my ($card, $side, $turn) = split /<>/, $magic;
      if ($card eq "星龍の記憶") {
        $turn--;
        $magic = $turn ? join "<>", ($card, $side, $turn) : "";
      }
    }

# フィールドの初期化
# --------------------------------------------------------------------------


    undef @f_drunk; undef @res; undef @syori; undef @syu_add;
    map { $f_tap[$_] = "" } (@{$fw3[1]}, @{$fw3[2]}); # めくったシールドの色を戻す
    unless (&c_chk("緑神龍クスダルフ", $turn2)) {   # マナゾーンのカードをアンタップ
      if (&c_chk("ガイアクラッシュ・クロウラー", 3)) {
        map { $f_tap[$_] = "" if !&syu_chk($fld[$_], 0) } @{$fw4[$turn2]};
      } else {
        map { $f_tap[$_] = "" } @{$fw4[$turn2]};
      }
    }
    foreach my $fldno (@{$fw1[$turn2]}) {       # バトルゾーンにあるカードをアンタップ
      next unless $f_tap[$fldno];
      if (&k_chk($fld[$fldno], 11)) {
        push @res, $fldno;
      } else {
        $f_tap[$fldno] = "" if $c_name[$fld[$fldno]] !~ /光器ドミニカ|ルナ・リボルバーホイール/ || !(&c_chk("ルナ・フォートレス", 3));
      }
    }

# --------------------------------------------------------------------------

    if (-1 < $#res) {
      unshift @syori, "s-$turn2<>t-サイレントスキルを使いますか？<>m-silent_sel<>o-使う::使わない";
      $chudan_flg = "1";
    } else {
      my $e_side = 3 - $turn2;
      if ((grep &tri_chk($fld[$_], 9)|| &tri_chk($fld[$_], 11), @{$fw1[$turn2]}) || (grep &tri_chk($fld[$_], 10), @{$fw1[$e_side]}) || &castle_chk($turn2, 2261)) {
        &s_mes(sprintf "%sドローする前にアンタップフェイズの処理を行う！", &castle_chk($turn2, 2261) ? "海底鬼面城の効果発動！　" : "クリーチャーの能力により、");
      } else {
        $phase = 1;
      }
    }
# }
# &s_mes("$pn[$turn2]の$phasestr[$phase]。");
# &s_mes("$pn[$turn2]のターン。");
}

sub silent_sel {
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    &com_error("サイレントスキルを使うクリーチャーを指定してください") if $F{'select'} eq "";
    &s_mes("$pn[$turn2]《は$c_name[$fld[$F{'select'}]]》のサイレントスキルを使った！");
    @res = grep $_ ne $F{'select'}, @res;
    unshift @syori, "s-$turn2<>t-サイレントスキルの処理を終了しますか？<>m-silent_sel2<>o-終了する";
  } else {
    map { $f_tap[$_] = "" } @res;
    undef @res; undef @syori;
    $phase = 1;
#   &s_mes("$pn[$turn2]の$phasestr[$phase]。");
  }
  $chudan_flg = "";
}

sub silent_sel2 {
  return if !($F{'run_select'});
  &s_mes("$pn[$turn2]はサイレントスキルの処理を終了した。");
  if (-1 < $#res) {
    &syori_clr;
    $chudan_flg = "1";
  } else {
    undef @syori;
    $chudan_flg = "";
    $phase = 1;
#   &s_mes("$pn[$turn2]の$phasestr[$phase]。");
  }
}



# 覚醒/解除
#--------------------------------------------------------

sub psychic {
	#com_error("$phasestr[$G{'phase'}]には覚醒/解除はできません") if $G{'phase'} =~ /[12]/;

	map { push @fsel, $1 if $_ =~ /^fsel(\d+)/ } keys(%F);

	my (%psy_top, %psy_back, %psy_super, %psy_cell);
	eval (join "", (log_read("psychic.txt")));

	my %count;
	map {
		my ($fldno) = $_;
		my ($cardno, $side, $area) = ($fldno =~ /\-/) ? look_god($fldno) : look_fld($fldno);
		if ($psy_top{$cardno} || $psy_back{$cardno}) {
			my ($reversedno) = ($psy_top{$cardno}) ? $psy_top{$cardno} : $psy_back{$cardno};
			s_mes(sprintf "$pn[$side]の%sを%sに裏返した", "《$c_name[$cardno]》", "《$c_name[$reversedno]》");
			# ゴッドの場合
			if ($fldno =~ /\-/) {
				my ($fldno, $godno) = split (/\-/, $fldno);
				my @card = split (/\-/, $fld[$fldno]);
				if ($card[$godno] ne "") {
					$card[$godno] = $reversedno;
				}
				$fld[$fldno] = join ("-", @card);
				$f_drunk[$fldno] = "";
			# それ以外
			} else {
				$fld[$fldno] = $reversedno;
				$f_drunk[$fldno] = "";
			}
		} elsif ($psy_super{$cardno}) {
			my (@cells) = @{$psy_super{$cardno}};
			$fld[$fldno] = shift(@cells);
			$f_drunk[$fldno] = "";
			my ($splitednames) = "《$c_name[$fld[$fldno]]》";
			map {
				my ($fno) = fld_chk($side);
				$fld[$fno] = $_;
				$f_drunk[$fno] = "";
				$splitednames .= "《$c_name[$_]》";
			} @cells;
			s_mes(sprintf "$pn[$side]の%sをリンク解除！ %sに分割された", "《$c_name[$cardno]》", $splitednames);
		} else {
			e_mes(sprintf ("%sを裏返すことはできません", "《$c_name[$cardno]》"), $u_side);
		}
#		open (FILE, ">> debug.txt");
#		print FILE "$_\n";
#		close (FILE);
	} (grep !$count{$_}++, @fsel);

	undef @fsel;
}

sub psy_link {
	#com_error("$phasestr[$G{'phase'}]には覚醒リンクはできません")		if $G{'phase'} =~ /[12]/;

	  map { push @fsel, $1 if $_ =~ /^fsel(\d+)/ } keys(%F);

	my (%psy_top, %psy_back, %psy_super, %psy_cell);
	eval (join "", (log_read("psychic.txt")));

	my %count;
	my $sp;
	my %chk;
	my $l_side;
	map {
		my ($fldno) = $_;
		my ($cardno, $side, $area) = ($fldno =~ /\-/) ? look_god($fldno) : look_fld($fldno);
		if ($psy_cell{$cardno}) {
			if ($sp) {
				com_error("同じ名前のカードが2枚以上選ばれています") if ($chk{$cardno});
				com_error("相手の場と自分の場のクリーチャーで覚醒リンクさせることはできません") if ($l_side != $side);
				com_error("正しいリンク元の組み合わせを選んでください") unless (grep ($_ eq $cardno, @{$sp}));
			} else {
				$sp = $psy_super{$psy_cell{$cardno}};
				$l_side = $side;
			}
			$chk{$cardno}++;
		} else {
			com_error("逆面がサイキック・セルでないクリーチャーは選択できません");
		}
	} (grep !$count{$_}++, @fsel);

	if ($sp) {
		map {
			com_error("カードの組み合わせが足りていません") unless ($chk{$_});
		} @{$sp};

		my ($cardnames) = "";
		my ($basefldno) = -1;
		my ($reversedname) = "";
		%count = {};
		map {
			my ($fldno) = $_;
			my ($cardno, $side, $area) = ($fldno =~ /\-/) ? look_god($fldno) : look_fld($fldno);

			if ($basefldno < 0) {
				$basefldno = $fldno;
				$fld[$fldno] = $psy_cell{$cardno};
				$reversedname = $c_name[$psy_cell{$cardno}];
				$f_drunk[$fldno] = "";
			} else {
				$fld[$fldno] = "";
				$f_cloth[$basefldno] = ($f_cloth[$basefldno]) ? $f_cloth[$basefldno] . "-" . $f_cloth[$fldno] : $f_cloth[$fldno];
				$f_cloth[$fldno] = "";
				$f_evo[$basefldno] = ($f_evo[$basefldno]) ? $f_evo[$basefldno] . "-" . $f_evo[$fldno] : $f_evo[$fldno];
				$f_evo[$fldno] = "";
				sforth_sub($side, $fldno);
			}
			$cardnames .= "《$c_name[$cardno]》";
		} (grep !$count{$_}++, @fsel);

		s_mes(sprintf "$pn[$l_side]の%sを覚醒リンク！　%s爆誕！", $cardnames, "《$reversedname》");
	}

	undef @fsel;
}

#--------------------------------------------------------

sub rand_tehuda {
# &com_error("$phasestr[$phase]に相手の手札を捨てることはできません") if $phase =~ /[12]/;
  &del_null(*hand, $u_side2);
  if ($#{$hand[$u_side2]} < 0) {
    &s_mes("$pn[$u_side]は$pn[$u_side2]の手札を捨てようとした。");
    &s_mes("しかし$pn[$u_side2]は手札を持っていなかった。");
  } else {
    $cardno = splice @{$hand[$u_side2]}, int(rand(sprintf "%d", $#{$hand[$u_side2]} + 1)), 1;
    &s_mes("$pn[$u_side]は$pn[$u_side2]の《$c_name[$cardno]》を捨てた。");
    if ($u_side == $turn2 && &k_chk($cardno, 29)) {
      &s_mes("《$c_name[$cardno]》の能力発動！　墓地に置くかわりにバトルゾーンに出る！");
      &fld_chk($u_side2);
      &put_battle_zone_sub;
    } else {
      unshift @{$boti[$u_side2]}, $cardno;
    }
  }
}

#--------------------------------------------------------

sub mekuru {
# &com_error("$phasestr[$phase]にカードをめくることはできません") if $phase =~ /[12]/;
  $chudan_flg = $trigger_flg = "1";
  if ($F{'marea'} == 3) {
    &s_mes("$pn[$u_side]は相手の山札の一番上をめくって見た。");
    &e_mes("相手の山札の一番上のカードは《$c_name[$deck[$u_side2][0]]》だった", $u_side);
    unshift @syori, "s-$u_side<>t-カードを山札の一番下に戻しますか？<>m-mekuru_sel6<>o-はい::いいえ";
  } else {
    unshift @syori, sprintf "s-$u_side<>t-%s<>m-mekuru_sel%s<>o-%s%s",
      $F{'marea'} == 0 ? "めくるシールドを選んでください" : $F{'marea'} == 1 ? "山札をめくってください" : "山札を何枚めくりますか？",
      $F{'marea'} == 0 ? "1" : $F{'marea'} == 1 && $F{'impulse'} ? "5" : $F{'marea'} == 1 ? "4" : $F{'impulse'} ? "3" : "2",
      $F{'marea'} == 1 ? "めくる::終了する" : "決定",
      $F{'secret'} ? "<>p-secret" : "";
  }
}

sub mekuru_sel1 { # 指定シールドをめくる
  map { push @fsel, $1 if $_ =~ /^fsel(\d+)/ } keys(%F);
  &com_error("めくるシールドを選んでください") if $#fsel < 0;
  foreach my $fldno (@fsel) {
    &which_side($fldno);
    next if $area != 2 || $fld[$fldno] =~ /\-s$/ || $fld[$fldno] eq "";
    my @shield = split /-/, $shinka[$fldno];
    unshift @shield, $fld[$fldno];
    my $name = join "<br>", map { "《" . $c_name[$_] . "》"; } @shield;
    my $cou = $fldno - $fw3[$l_side][0] + 1;
    $f_tap[$fldno] = "1";
    &s_mes(sprintf "$pn[$u_side]は%sシールド$couをめくって見た。", $l_side == $u_side ? "自分の" : "相手の");
    &e_mes("シールド$couのカードは$nameだった", $u_side);
    undef @shield;
  }
  undef @fsel;
  &syori_clr;
  $chudan_flg = $trigger_flg = "";
}

sub mekuru_sel2 { # 枚数を指定してめくる
  my $k = $F{'maisu'};
  my $name = "";
  for (1..$k) { push @res2, shift @{$deck[$u_side]}; }
  @res2 = reverse @res2;
  &s_mes("$pn[$u_side]は山札のカードを$k枚めくった。");
  if ($F{'mode'} eq "mekuru_sel2") {
    map { $name .= "《$c_name[$_]》<br>" } @res2;
    if ($F{'secret'}) {
      &e_mes("めくったカードは<br>$nameだった", $u_side);
    } else {
      &s_mes("めくったカードは<br>$nameだった");
    }
  }
  $syori[0] = sprintf "s-$u_side<>t-カードを%s%s",
    $F{'mode'} eq "mekuru_sel2" ? "移動してください<>m-mekuru_move1<>o-手札に加える::墓地に送る"
                  : "戻す順番を決めてください<>m-mekuru_move2<>o-山札の下へ戻す::山札の上へ戻す",
    $F{'secret'} ? "<>p-secret" : "";
}

sub mekuru_sel4 { # １枚ずつめくる
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    my $cno = shift @{$deck[$u_side]};
    push @res2, $cno;
    &s_mes("$pn[$u_side]は山札からカードを１枚めくった。");
    &s_mes("$pn[$u_side]がめくったカードは《$c_name[$cno]》だった。");
  } else {
    $syori[0] = sprintf "s-$u_side<>t-カードを%s",
      $F{'mode'} eq "mekuru_sel4" ? "移動してください<>m-mekuru_move1<>o-バトルゾーンに出す::墓地に送る<>p-one"
                    : "戻す順番を決めてください<>m-mekuru_move2<>o-山札の下へ戻す::山札の上へ戻す";
  }
}

sub mekuru_sel6 { # 相手の山札をめくった後一番下に戻す。
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    push @{$deck[$u_side2]}, shift @{$deck[$u_side2]};
    &s_mes("$pn[$u_side]はめくったカードを山札の一番下に戻した。");
  }
  &syori_clr;
  $chudan_flg = $trigger_flg = "";
}

sub mekuru_move1 {  # １枚ずつめくった後、バトルゾーンに出す
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  map { push @rsel, $1 if $_ =~ /^rsel(\d+)/ } (keys(%F));
  &com_error("一度にバトルゾーンに出せるカードは１枚だけです") if 0 < $#rsel && $F{'run_select'} && $S{'p'} eq "one";
  foreach my $rsel(@rsel) {
    next if $res2[$rsel] eq "";
    $cardno = $res2[$rsel];
    $res2[$rsel] = "";
    if ($S{'p'} eq "one" && $F{'run_select'}) {
      if (&syu_chk($cardno, 1)) {
        &put_gear_chk($cardno);
      } elsif (&syu_chk($cardno, 96)) {
        @res = &shield_chk($u_side);
      } elsif (!(&syu_chk($cardno, 0))) {
        &put_cre_chk($cardno);
      }
      if (0 < $s_cou || -1 < $#res) {
        &put_card_dialog($cardno, "mekuru");
        &put_ini;
        exit;
      } else {
        &fld_chk($u_side);
        &s_mes("$pn[$u_side]は《$c_name[$cardno]》をバトルゾーンに出した。");
        if (&syu_chk($cardno, 1)) {
          unshift @{$gear[$u_side]}, $cardno;
        } else {
          &put_battle_zone_sub;
        }
      }
    } else {
      local (*arr) = $F{'run_select'} ? *hand : *boti;
      unshift @{$arr[$u_side]}, $cardno;
      &s_mes(sprintf "$pn[$u_side]は《$c_name[$cardno]》を%s。", $F{'run_select'} ? "手札に加えた" : "墓地に送った");
    }
  }
  @res2 = grep $_ ne "", @res2;
  if ($#res2 < 0) {
    undef @rsel;
    &syori_clr;
    $chudan_flg = $trigger_flg = "";
  }
}

sub mekuru_move2 {
  &unique;
  &s_mes(sprintf "$pn[$u_side]はカードを山札の%sに戻した。", $F{'run_select'} ? "下" : "上") if $F{'secret'};
  my @arr_stack = ();
  foreach my $rsel (@rsel) {
    my $rsel2 = substr $rsel, 4;
    my $cno = $res2[$rsel2];
    $res2[$rsel2] = "";
    if ($F{$rsel} == 0) {
      unshift @{$hand[$u_side]}, $cno;
      if ($F{'secret'}) {
        &e_mes("《$c_name[$cno]》を手札に加えた", $u_side);
      } else {
        &s_mes("《$c_name[$cno]》を手札に加えた。");
      }
    } elsif ($F{$rsel} == 1) {
      unshift @{$boti[$u_side]}, $cno;
      &s_mes("《$c_name[$cno]》を墓地に送った。");
    } else {
      $m_name .= "《$c_name[$cno]》<br>";
      push @arr_stack, $cno;
    }
  }
  @{$deck[$u_side]} = $F{'run_select'} ? (@{$deck[$u_side]}, @arr_stack) : (@arr_stack, @{$deck[$u_side]});
  &regist("", sprintf("%s$m_nameを山札の%sに戻した%s",
    $F{'secret'} ? "（" : "",
    $F{'run_select'} ? "下" : "上",
    $F{'secret'} ? "）" : "。"),
    sprintf "%s", $F{'secret'} ? "secret$u_side" : "system"
  ) if $m_name ne "";
  &syori_clr;
  $chudan_flg = $trigger_flg = "";
}

sub unique {  # 順番の重複をチェック
  while (($key, $val) = each(%F)) {
    push @value, $val if $key =~ /^rsel/ && 1 < $val;
  }
  my @unique = grep !$count{$_}++, @value;
  &com_error("順番が重なっているカードがあります。もう一度順番を決めてください") if $#unique < $#value;
  @rsel = sort { $F{$a} cmp $F{$b} } (grep /^rsel/, keys(%F));
}

#--------------------------------------------------------

sub move {
  local ($parea = $F{'parea'}, $varea = $F{'varea'}, $vside = (($u_side - 1) xor $F{'vside'}) + 1);
  local *zone = $parea == 2 ? *boti : $parea == 3 ? *hand : ($parea == 4 || $parea == 5) ? *deck : $parea == 9 ? *psychic : "";
  local *arr = $varea == 2 ? *deck : $varea == 1 ? *boti : $varea == 0 ? *hand : *psychic;
# &com_error("$phasestr[$phase]にカードを移動することはできません") if $phase == 1;
# &com_error("$phasestr[$phase]にはマナゾーン以外にカードを移動することはできません") if $phase == 2 && $parea != 0;
  &com_error("フォームから多重送信されたため、二度目以降の処理を中断しました") if(($multi eq $F{'random'}) && ($F{'random'} ne ''));
  $multi = $F{'random'};

  map { push @{$1}, $2 if $_ =~ /(^.?sel)(.+)/ } keys(%F);
  &com_error("場に出ているカードとそれ以外のカードを同時に移動させることはできません") if (-1 < $#sel || $F{'decktop'}) && (-1 < $#fsel || -1 < $#ssel || -1 < $#gsel || -1 < $#csel);
  &com_error("山札の一番上や一番下とそれ以外のカードを同時に移動させることはできません") if -1 < $#sel && $F{'decktop'};
  &com_error("移動させるカードを指定してください") if $#sel < 0 && $#fsel < 0 && $#ssel < 0 && $#gsel < 0 && $#csel < 0 && !($F{'decktop'});

  # 強制的に上に置く
  if ( $parea == 10 ) {

    if (-1 < $#sel || $F{'decktop'}) {  # 手札、墓地、山札からバトルゾーンへ
      &com_error("一度にバトルゾーンに出せるカードは１枚ずつです") if 0 < $#sel;
      &com_error("相手のカードを場に出すことはできません") if $vside == $u_side2;
      if ($F{'decktop'}) {
        #デッキのカード選択の場合
        if ($F{'under'} == 1) {
          $cardno = $deck[$vside][$#{$deck[$vside]}]; # デッキの一番下
        } else {
          $cardno = $deck[$vside][0]; # デッキの１番上（0番目）
        }
      } else {
        # デッキ以外の場合
        $cardno = $arr[$vside][$sel[0]];
      }
      return if $cardno eq ""; #未選択の場合はリターン
      $s_cou = 0;
      &fld_chk($u_side);
      if (&syu_chk($cardno, 1)) { # クロスギア
        &put_gear_chk($cardno);
      } elsif (&syu_chk($cardno, 96)) { # 城
        @res = &shield_chk($u_side);
      } elsif (!(&syu_chk($cardno, 0))) { # 呪文以外
        &put_cre_chk2($cardno);
      }
      if ($F{'decktop'}) {
        if ($F{'under'} == 1) {
          $deck[$u_side][$#{$deck[$u_side]}] = "";
        } else {
          $deck[$u_side][0] = "";
        }
      } else {
        $arr[$u_side][$sel[0]] = "";
      }
      #&s_mes("$s_cou");
      #&s_mes("$#res");
      if (0 < $s_cou || -1 < $#res) {
        &put_card_dialog2($cardno, sprintf("%d", $F{'decktop'} ? 2 : $varea));
      } else {
        &com_error("自分のシールドが無いので城をバトルゾーンに出すことはできません") if &syu_chk($cardno, 96);
        if ($F{'decktop'}) {
          if ($F{'under'} == 1) {
            &s_mes("$pn[$u_side]は山札の一番下のカードをバトルゾーンに出した。");
          } else {
            &s_mes("$pn[$u_side]は山札の一番上のカードをバトルゾーンに出した。");
          }
        }

        &s_mes(sprintf "$pn[$u_side]%s《$c_name[$cardno]》%s！",
          "は",
          "をバトルゾーンに出した");
        if (&syu_chk($cardno, 1)) {
          unshift @{$gear[$u_side]}, $cardno;
        } else {
          &put_battle_zone_sub;
        }
        &del_move;
      }
    } else {              # フィールドからバトルゾーンへ
      &com_error("バトルゾーンからバトルゾーンに移動させることはできません") if -1 < $#gsel || -1 < $#csel;
      &com_error("一度にバトルゾーンに移動できるカードは１枚ずつです") if 0 < $#ssel || 0 < $#fsel;
      if (-1 < $#fsel) {
        $fldno = $fsel[0];
        &which_side($fldno);
        &com_error("バトルゾーンからバトルゾーンに移動させることはできません") if $area < 2;
        &pick_card2;
      } else {
        $ssel = $ssel[0];
        &pick_card3;
      }
      &put_cre_chk2($cardno);
      if (-1 < $#res) {
        &put_card_dialog2($cardno, sprintf("%s", -1 < $#fsel ? "fld$fldno" : "shinka$ssel"));
      } else {
        &fld_chk($l_side);
        &p_mess;
        &put_battle_zone_sub;
      }
    }

  } elsif ( $parea == 9 ) {# 超次元ゾーンへ

    if ( $F{'decktop'} ) {
      $cardno = ${$deck[$u_side]}[0];
      com_error("サイキック・クリーチャー以外のカードを超次元ゾーンに移動することはできません")  unless (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186));
      $cardno = shift @{$deck[$u_side]};
      move_sub($cardno, $u_side);
    } else {
      if (@sel) {
        foreach my $sel (@sel) {
          $cardno = ${ $varea == 0 ? $hand[$vside] : $varea == 1 ? $boti[$vside] : $varea == 2 ? $deck[$vside] : $varea == 3 ? $psychic[$vside] : $hand[$vside] }[$sel];
          com_error("サイキック・クリーチャー以外のカードを超次元ゾーンに移動することはできません")  unless (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186));
        }
        foreach my $sel (@sel) {
          $cardno = pick_card($sel);
          move_sub($cardno, $vside);
        }
      } else {
        foreach my $evono (@ssel) {
          my($cardno, $l_side, $area) = look_evo($evono);
          com_error("サイキック・クリーチャー以外のカードを超次元ゾーンに移動することはできません")  unless (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186));
          com_error("サイキック・クリーチャー以外のカードを超次元ゾーンに移動することはできません")  unless (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186));
        }
        foreach my $fldno (@fsel) {
          my($cardno, $l_side, $area) = look_fld($fldno);
          com_error("サイキック・クリーチャー以外のカードを超次元ゾーンに移動することはできません")  unless (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186));
        }
        foreach my $gsel (@gsel) {
          my($cardno, $l_side, $area) = look_gene($gsel);
          com_error("サイキック・クリーチャー以外のカードを超次元ゾーンに移動することはできません")  unless (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186));
        }
        foreach my $csel (@csel) {
          my($cardno, $l_side, $area) = look_cloth($csel);
          com_error("サイキック・クリーチャー以外のカードを超次元ゾーンに移動することはできません")  unless (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186));
        }

        foreach my $evono (@ssel) {
          move_sub(pick_evo($evono));
        }
        foreach my $fldno (@fsel) {
          move_sub(pick_fld($fldno));
        }
        foreach my $gsel (@gsel) {
          move_sub(pick_gene($gsel));
        }
        foreach my $csel (@csel) {
          move_sub(pick_cloth($csel));
        }
      }

    }
    &del_move;
  } elsif (6 < $parea) { # 進化獣もしくはシールドの下
    @res = $parea == 7 ? grep $c_evo[$fld[$_]] ne "", @{$fw1[$u_side]} : grep $fld[$_] ne "", @{$fw3[$u_side]};
    &com_error(sprintf "自分の%sが１%sもないので移動できません", $parea == 7 ? "進化クリーチャー" : "シールド", $parea == 7 ? "体" : "枚") if $#res < 0;
    &com_error("フィールドのクリーチャー以外を直接移動させる処理はまだできていません。ごめんなさいm(__)m") if -1 < $#ssel || -1 < $#gsel || -1 < $#csel;
    $chudan = "";
    if ($F{'decktop'}) {
      if ($F{'under'} == 1) {
        $chudan = pop @{$deck[$u_side]};
      } else {
        $chudan = shift @{$deck[$u_side]};
      }
    } elsif (-1 < $#sel) {
      &com_error(sprintf "相手のカードを%sの下に移動させることはできません", $parea == 7 ? "進化クリーチャー" : "シールド") if $vside == $u_side2;
      foreach my $sel(@sel) {
        next if &syu_chk($arr[$vside][$sel], 0, 1) && $parea == 7;
        &pick_card1($sel);
        $chudan .= $chudan ne "" ? "-$cardno" : $cardno;
      }
    } else {
      foreach $fldno(@fsel) {
        &which_side($fldno);
        next if $l_side != $u_side || ($area == 1 && $parea == 7) || $fld[$fldno] eq "";
        $chudan .= $chudan ne "" ? "-$fldno" : $fldno;
      }
    }
    $chudan_flg = "1";
    unshift @syori, sprintf "s-$u_side<>t-カードを下に置きたい%sを選んでください<>m-changer_sel1<>a-%s<>o-決定::やめる%s",
                $parea == 7 ? "進化クリーチャー" : "シールド",
                $F{'decktop'} ? "deck" : -1 < $#sel ? "$varea" : "field",
                $parea == 7 ? "" : "<>p-shield";
    undef @res if $parea == 8;
  } elsif ($parea == 1) {
    if (-1 < $#sel || $F{'decktop'}) {  # 手札、墓地、山札からバトルゾーンへ
      &com_error("一度にバトルゾーンに出せるカードは１枚ずつです") if 0 < $#sel;
      &com_error("相手のカードを場に出すことはできません") if $vside == $u_side2;
      if ($F{'decktop'}) {
        if ($F{'under'} == 1) {
          $cardno = $deck[$vside][$#{$deck[$vside]}];
        } else {
          $cardno = $deck[$vside][0];
        }
      } else {
        $cardno = $arr[$vside][$sel[0]];
      }
      return if $cardno eq "";
      $s_cou = 0;
      &fld_chk($u_side);
      if (&syu_chk($cardno, 1)) {
        &put_gear_chk($cardno);
      } elsif (&syu_chk($cardno, 96)) {
        @res = &shield_chk($u_side);
      } elsif (!(&syu_chk($cardno, 0))) {
        &put_cre_chk($cardno);
      }
      if ($F{'decktop'}) {
        if ($F{'under'} == 1) {
          $deck[$u_side][$#{$deck[$u_side]}] = "";
        } else {
          $deck[$u_side][0] = "";
        }
      } else {
        $arr[$u_side][$sel[0]] = "";
      }
      if (0 < $s_cou || -1 < $#res) {
        &put_card_dialog($cardno, sprintf("%d", $F{'decktop'} ? 2 : $varea));
      } else {
        &com_error("自分のシールドが無いので城をバトルゾーンに出すことはできません") if &syu_chk($cardno, 96);
        if ($F{'decktop'}) {
          if ($F{'under'} == 1) {
            &s_mes("$pn[$u_side]は山札の一番下のカードをバトルゾーンに出した。");
          } else {
            &s_mes("$pn[$u_side]は山札の一番上のカードをバトルゾーンに出した。");
          }
        }

        &s_mes(sprintf "$pn[$u_side]%s《$c_name[$cardno]》%s！",
          &syu_chk($cardno, 1) ? "はクロスギア、" : &syu_chk($cardno, 0) ? "の" : "は",
          &syu_chk($cardno, 1) ? "をジェネレート" : &syu_chk($cardno, 0) ? "、超動" : "を召喚");
        if (&syu_chk($cardno, 1)) {
          unshift @{$gear[$u_side]}, $cardno;
        } else {
          &put_battle_zone_sub;
        }
        &del_move;
      }
    } else {              # フィールドからバトルゾーンへ
      &com_error("バトルゾーンからバトルゾーンに移動させることはできません") if -1 < $#gsel || -1 < $#csel;
      &com_error("一度にバトルゾーンに移動できるカードは１枚ずつです") if 0 < $#ssel || 0 < $#fsel;
      if (-1 < $#fsel) {
        $fldno = $fsel[0];
        &which_side($fldno);
        &com_error("バトルゾーンからバトルゾーンに移動させることはできません") if $area < 2;
        &pick_card2;
      } else {
        $ssel = $ssel[0];
        &pick_card3;
      }
      &put_cre_chk($cardno);
      if (-1 < $#res) {
        &put_card_dialog($cardno, sprintf("%s", -1 < $#fsel ? "fld$fldno" : "shinka$ssel"));
      } else {
        &fld_chk($l_side);
        &p_mess;
        &put_battle_zone_sub;
      }
    }
  } elsif ($parea =~ /[06]/) {
    if (-1 < $#sel || $F{'decktop'}) {  # 手札、墓地、山札からマナゾーン、シールドへ
      &com_error("相手のカードを場に出すことはできません") if $vside == $u_side2;
      local $e_side = 3 - $u_side;
      if ($F{'decktop'}) {
        if ($F{'under'} == 1) {
          $cardno = pop @{$deck[$u_side]};
        } else {
          $cardno = shift @{$deck[$u_side]};
        }
        &put_card_sub;
      } else {
        foreach my $sel(@sel) {
          &pick_card1($sel);
          &put_card_sub;
        }
      }
      &del_move;
    } else {              # フィールドからマナゾーン、シールドへ
      foreach $ssel(@ssel) {
        &pick_card3;
        &put_card2_sub;
      }
      foreach $fldno(@fsel) {
        &which_side($fldno);
        next if ($area < 2 && $parea == 1) || ($area == 3 && $parea == 0) || ($area == 2 && $parea == 6);
        &pick_card2;
        &put_card2_sub;
      }
      foreach $gsel(@gsel) {
        next if $parea == 1;
        &pick_card5;
        &put_card2_sub;
      }
      &del_move3;
      foreach $csel(@csel) {
        next if $parea == 1;
        &pick_card6;
        &put_card2_sub;
      }
      &del_move4;
    }
  } elsif (-1 < $#sel || $F{'decktop'}) { # 手札、墓地、山札から手札、墓地、山札へ
    &com_error("墓地にあるカードを墓地に送ることはできません") if !($F{'decktop'}) && $varea == 1 && $parea == 2;
    &com_error("手札のカードを手札に入れることはできません") if !($F{'decktop'}) && $varea == 0 && $parea == 3;
    &com_error("山札のカードを山札の上に戻すことはできません") if ($varea == 2 || $F{'decktop'}) && $parea == 4;
    if ($F{'decktop'}) {
      if ($F{'under'} == 1) {
        $cardno = pop @{$deck[$u_side]};
      } else {
        $cardno = shift @{$deck[$u_side]};
      }
      &move_sub($u_side);
    } else {
      foreach my $sel(@sel) {
        &pick_card1($sel);
        &move_sub($vside);
      }
    }
    &del_move;
  } elsif (-1 < $#gsel) {         # ジェネレートしたクロスギアを手札、墓地、山札へ
    foreach $gsel(@gsel) {
      &pick_card5;
      &move_sub($l_side);
    }
    &del_move3;
  } elsif (-1 < $#fsel && -1 < $#ssel && $parea == 4) { # 進化と進化元を同時に山札の一番上へ
    &return_deck3;
  } else {
    &move2;
  }
  undef @sel; undef @fsel; undef @ssel; undef @gsel; undef @csel;
}

sub put_card_sub {
  &fld_chk($u_side);
  my $fno = $parea == 0 ? $nf3 : $nf2;
  &s_mes(sprintf "$pn[$u_side]は%s%sを%sに%s",
  $F{'decktop'} ? ($F{'under'} == 1) ? "山札の一番下の" : "山札の一番上の" : "",
  $parea == 0 && $F{'decktop'} ? "カード、《$c_name[$cardno]》" : $parea == 0 ? "《$c_name[$cardno]》" : "カード",
  $parea == 0 ? "マナゾーン" : "シールド",
  $parea == 0 ? "出した。" : "セット！");
  if (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186))  {
    s_mes("《$c_name[$cardno]》は超次元ゾーンに送られた。");
    push (@{$psychic[$u_side]}, $cardno);
  } else {
    $f_tap[$fno] = &k_chk($cardno, 12) || &c_chk("停滞の影タイム・トリッパー", $e_side) ? "1" : "0" if $parea == 0;
    $fld[$fno] = $cardno;
  }
}

sub put_battle_zone_sub {
  my $fno = !(&syu_chk($cardno, 0)) ? $nf0 : $nf1;
  $fno = $nf1 if (&syu_chk($cardno, 96)); # 城用独自処理、本家実装で削除行
  $fld[$fno] = $cardno;
  $f_drunk[$fno] = &k_chk($cardno, 6) || &syu_chk($cardno, 0, 1) ? "" : "1";
  $f_drunk[$fno] = "" if (&syu_chk($cardno, 96)); # 城用独自処理、本家実装で削除行
  $chudan_flg = "";
  &put_battle_zone_koka($cardno, $fno);
}

sub put_battle_zone_koka {
  my ($cardno, $fno) = @_;
  $chudan_flg = $chudan = "";
  &which_side($fno);
  my $e_side = 3 - $l_side;
  if (&syu_chk($cardno, 0)) {
    if (&k_chk($cardno, 14)) {
      my $cou = grep $_ == $cardno, (@{$boti[1]}, @{$boti[2]});
      &s_mes("クローン呪文！　墓地に置かれた$cou枚分、効果が増幅する！") if $cou != 0;
    }
    if (&meteo_chk("超神星マーキュリー・ギガブリザード", $e_side)) {
      unshift @syori, "s-$e_side<>t-メテオバーンを使いますか？<>m-meteo_sel<>o-使う::使わない<>g-merqury<>c-$c_name[$cardno]";
    } else {
      &magic("$c_name[$cardno]", $l_side);
    }
  } else {
    if ($c_name[$cardno] eq "無双竜機ボルバルザーク" && !(&c_chk("無双竜機ボルバルザーク", $l_side))) {
      &s_mes("《$c_name[$cardno]》の効果発動！");
      if ($l_side == $turn2) {
        &s_mes("このターンの後、$pn[$l_side]のターンがもう一度行われる！");
        $skip_flg = 1;
      }
      &s_mes(sprintf "%s次のターンが終わった時、$pn[$l_side]はこのゲームに敗北する！", $l_side == $turn2 ? "そして" : "");
#     $boru_cnt = 1;
      unshift @magic, "無双竜機ボルバルザーク<>$l_side<>1";
    } elsif ($c_name[$cardno] =~ /処罰の精霊ウラルス|捜索甲冑ゴロンガー/) {
      if (grep $fld[$_] ne "", (@{$fw3[1]}, @{$fw3[2]})) {
        $chudan = $cardno;
        $chudan_flg = "1";
        unshift @syori, "s-$l_side<>t-表向きにするシールドを選んでください<>m-flip_sel<>o-決定::終了";
      }
    } elsif ($c_name[$cardno] =~ /蒼黒の知将ディアブロスト|金色の精霊クロスヘイム|天雷の龍聖ロレンツオ４世/) {
      &block_flg;
      &s_mes(sprintf "《$c_name[$cardno]》の能力で、%sの%sクリーチャーはすべてブロッカーとなった！",
        $c_name[$cardno] eq "蒼黒の知将ディアブロスト" ? "$pn[$e_side]" : "$pn[$l_side]",
        $c_name[$cardno] eq "蒼黒の知将ディアブロスト" ? "" : $c_name[$cardno] eq "金色の精霊クロスヘイム" ? "多色" :"ナイト・");
    } elsif (&k_chk($cardno, 28) && &shield_chk($l_side)) {
      $chudan_flg = $trigger_flg = "1";
      $chudan = $fno;
      unshift @syori, "s-$l_side<>t-シールド・フォースのシールドを選んでください<>m-sforth_sel<>o-決定";
    }
    &set_block($fno, $cardno);
    $f_tap[$fno] = "1" if $c_name[$cardno] =~ /光器ドミニカ|緊縛の影バインド・シャドウ/
              || &c_chk("聖霊王エルフェウス", $e_side)
              || (&c_chk("霊騎ラファーム", $e_side) && &bun_chk($cardno, 3, 4))
              || (&c_chk("緊縛の影バインド・シャドウ", 3) && &bun_chk($cardno, 2));
  }
}

sub sforth_sel {  # シールドフォースのシールドを選択
  return if !($F{'run_select'});
  &com_error("シールドを指定してください") if $F{'select'} eq "";
  &syori_p_set;
  my $fno = $F{'select'};
  my $cou = $fno - $fw3[$S{'s'}][0] + 1;
  $f_block[$fno] .= $f_block[$fno] eq "" ? "$chudan" : "-$chudan";
  &s_mes(sprintf "%sはシールド$couを指定してシールド・フォースを発動させた！", &card_name_sub($chudan));
  &syori_clr;
  $chudan = $chudan_flg = $trigger_flg = "";
}

sub move2 {     # フィールドから手札、墓地、山札へ移動
  foreach $csel (@csel) { # クロス中のクロスギア
    &pick_card6;
    &move_sub($l_side);
  }
  &del_move4;
  foreach $ssel (@ssel) { # 進化獣
    &pick_card3;
    &move_sub($l_side);
  }
  &del_move2;
  foreach $fldno(@fsel) { # フィールド
    if ($fldno =~ /\-/) {
      &pick_god($fldno);
    } else {
      &pick_card2;
    }
    &move_sub($l_side);
  }
  &del_move5;
  undef @fsel; undef @ssel; undef @csel;
}

sub move_sub {
  my $side = $_[0];
  &p_mess;
  if ((syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186)) && ($parea != 9)) {
    s_mes("《$c_name[$cardno]》は超次元ゾーンに送られた。");
    push (@{$psychic[$side]}, $cardno);
  } else {
    if ($parea == 5) {
      push @{$deck[$side]}, $cardno;
    } else {
      unshift @{$zone[$side]}, $cardno;
    }
  }
}

sub pick_card1 {
  my $sel = $_[0];
  $cardno = $arr[$vside][$sel];
  next if $cardno eq "";
  $arr[$vside][$sel] = "";
}

sub pick_card2 {
  next if $fld[$fldno] eq "";
  $cardno = $fld[$fldno];
  $cardno =~ s/\-s$// if $cardno =~ /\-s$/;
  $fld[$fldno] = $f_tap[$fldno] = $f_block[$fldno] = $f_drunk[$fldno] = "";
  &which_side($fldno);
  &shinka_sub($fldno);
  &cloth_sub($fldno);
  &sforth_sub($fldno);
}

sub pick_card4 { # 今のところ墓地進化に使用
  next if $boti[$u_side][$fldno] eq "";
  $cardno = $boti[$u_side][$fldno];
  $cardno =~ s/\-s$// if $cardno =~ /\-s$/;
  &which_side($fldno, 'boti');
  &shinka_sub3($fldno);
  &cloth_sub($fldno);
  &sforth_sub($fldno);
}

sub pick_god {
  my ($fldno, $gno) = split /-/, $_[0];
  my @card = split /-/, $fld[$fldno];
  next if $card[$gno] eq "";
  $cardno = $card[$gno];
  $card[$gno] = "";
  $fld[$fldno] = join "-", @card;
  &which_side($fldno);
}



sub pick_card {	# 手札、墓地、山札、超次元からカードを取り出す
	my $arr = $varea == 0 ? $hand[$vside] : $varea == 1 ? $boti[$vside] : $varea == 2 ? $deck[$vside] : $varea == 3 ? $psychic[$vside] : $hand[$vside];
	next if ${$arr}[$_[0]] eq "";
	my $cardno = ${$arr}[$_[0]];
	${$arr}[$_[0]] = "";
	return $cardno
}

sub pick_fld {	# フィールドからカードを取り出す
	my $fldno = $_[0];
	next if $fld[$fldno] eq "";
	$cardno = $fld[$fldno];
	$cardno =~ s/\-s$// if $cardno =~ /\-s$/;
	$fld[$fldno] = $f_tap[$fldno] = $f_block[$fldno] = $f_drunk[$fldno] = "";
	which_side($fldno);
	shinka_sub($fldno);
	cloth_sub($l_side, $fldno);
	sforth_sub($l_side, $fldno);
	return $l_side
}

sub pick_god {		# ゴッドの片方を取り出す
	my ($fldno, $godno) = split /-/, $_[0];
	my @card = split /-/, $fld[$fldno];
	next if $card[$godno] eq "";
	$cardno = $card[$godno];
	$card[$godno] = "";
	$fld[$fldno] = join "-", @card;
	which_side($fldno);
	return $l_side
}

sub pick_evo {		# 進化元を取り出す
	my ($fldno, $evono) = split /-/, $_[0];
	my @shinka = split /-/, $f_evo[$fldno];
	next if $shinka[$evono] eq "";
	$cardno = $shinka[$evono];
	$shinka[$evono] = "";
	$f_evo[$fldno] = join "-", @shinka;
	which_side($fldno);
	return $l_side
}

sub pick_gene {		# ジェネレート中のクロスギアを取り出す
	my ($l_side, $gearno, $evono) = split /-/, $_[0];
	my @s_gear = split /:/, $gear[$l_side][$gearno] if $evono ne "";
	$cardno = $evono eq "" ? $gear[$l_side][$gearno] : $s_gear[$evono];
	next if $cardno eq "";
	($evono eq "" ? $gear[$l_side][$gearno] : $s_gear[$evono]) = "";
	$gear[$l_side][$gearno] = join ":", @s_gear if $evono ne "";
	return $l_side;
}

sub pick_cloth {	# クロス中のクロスギアもしくは城を取り出す
	my ($fldno, $clothno, $evono) = split /-/, $_[0];
	my @c_gear = split /-/, $f_cloth[$fldno];
	my @e_gear = split /:/, $c_gear[$clothno] if $evono ne "";
	$cardno = $evono eq "" ? $c_gear[$clothno] : $e_gear[$evono];
	next if $cardno eq "";
	($evono eq "" ? $c_gear[$clothno] : $e_gear[$evono]) = "";
	$c_gear[$clothno] = join ":", @e_gear if $evono ne "";
	$f_cloth[$fldno] = join "-", @c_gear;
	which_side($fldno);
	return $l_side
}

sub look_card {	# 手札、墓地、山札、超次元からカードを取り出す
	my $arr = $varea == 0 ? $hand[$vside] : $varea == 1 ? $boti[$vside] : $varea == 2 ? $deck[$vside] : $varea == 3 ? $psychic[$vside] : $hand[$vside];
	next if ${$arr}[$_[0]] eq "";
	my $cardno = ${$arr}[$_[0]];
	return $cardno
}

sub look_fld {	# フィールドからカードを取り出す
	my $fldno = $_[0];
	next if $fld[$fldno] eq "";
	my $cardno = $fld[$fldno];
	which_side($fldno);
	return ($cardno, $l_side, $area)
}

sub look_god {		# ゴッドの片方を取り出す
	my ($fldno, $godno) = split /-/, $_[0];
	my @card = split /-/, $fld[$fldno];
	next if $card[$godno] eq "";
	my $cardno = $card[$godno];
	which_side($fldno);
	return ($cardno, $l_side, $area)
}

sub look_evo {		# 進化元を取り出す
	my ($fldno, $evono) = split /-/, $_[0];
	my @shinka = split /-/, $f_evo[$fldno];
	next if $shinka[$evono] eq "";
	my $cardno = $shinka[$evono];
	which_side($fldno);
	return ($cardno, $l_side, $area)
}

sub look_gene {		# ジェネレート中のクロスギアを取り出す
	my ($l_side, $gearno, $evono) = split /-/, $_[0];
	my @s_gear = split /:/, $gear[$l_side][$gearno] if $evono ne "";
	my $cardno = $evono eq "" ? $gear[$l_side][$gearno] : $s_gear[$evono];
	next if $cardno eq "";
	return ($cardno, $l_side, "gene");
}

sub look_cloth {	# クロス中のクロスギアもしくは城を取り出す
	my ($fldno, $clothno, $evono) = split /-/, $_[0];
	my @c_gear = split /-/, $f_cloth[$fldno];
	my @e_gear = split /:/, $c_gear[$clothno] if $evono ne "";
	my $cardno = $evono eq "" ? $c_gear[$clothno] : $e_gear[$evono];
	next if $cardno eq "";
	which_side($fldno);
	return ($cardno, $l_side, $area)
}

sub shinka_sub {
  my $fldno = $_[0];
  if ($shinka[$fldno] ne "") {
    my @evo = split /-/, $shinka[$fldno];
    $fld[$fldno] = pop @evo;
    &set_block($fldno, $fld[$fldno]);
    $shinka[$fldno] = join "-", @evo;
    undef @evo;
  }
}

sub add_up_card_sub {
  $fno = $F{'select'};
  my $cno = $fld[$fno];
  $shinka[$fno] .= $shinka[$fno] eq "" ? "$cno" : "-$cno";
  $f_block[$fno] = $f_drunk[$fno] = "";
  $fld[$fno] = $chudan;
}

sub shinka_sub2 {
  $fno = $F{'select'};
  my $cno = $fld[$fno];
  $shinka[$fno] .= $shinka[$fno] eq "" ? "$cno" : "-$cno";
  $f_block[$fno] = $f_drunk[$fno] = "";
  $fld[$fno] = $chudan;
}

sub shinka_sub3 { # 今のところ墓地進化に使用
  my $fldno = $_[0];
  # 墓地から進化元カード削除
  $boti[$u_side][$fldno] = "";
  if ($shinka[$fldno] ne "") {
    my @evo = split /-/, $shinka[$fldno];
    $fld[$fldno] = pop @evo;
    &set_block($fldno, $fld[$fldno]);
    $shinka[$fldno] = join "-", @evo;
    undef @evo;
  }
}

sub mana_shinka_sub {
  $fldno = $F{'select'};
  &pick_card2;
  &fld_chk($l_side);
  $fno = $nf0;
  $shinka[$fno] .= "$cardno";
  $f_block[$fno] = $f_drunk[$fno] = "";
  $fld[$fno] = $chudan;
}

# 墓地進化処理関数
sub boti_shinka_sub {
  $fldno = $F{'select'};
  &pick_card4;
  &fld_chk($u_side);
  $fno = $nf0;
  $shinka[$fno] .= "$cardno";
  $f_block[$fno] = $f_drunk[$fno] = "";
  $fld[$fno] = $chudan;
}

sub pick_card3 {
  ($fldno, $sno) = split /-/, $ssel;
  my @evo = split /-/, $shinka[$fldno];
  next if $evo[$sno] eq "";
  $cardno = $evo[$sno];
  $evo[$sno] = "";
  $shinka[$fldno] = join "-", @evo;
  &which_side($fldno);
}

sub pick_card5 {
  ($l_side, $gno, $sno) = split /-/, $gsel;
  my @s_gear = split /:/, $gear[$l_side][$gno] if $sno ne "";
  $cardno = $sno eq "" ? $gear[$l_side][$gno] : $s_gear[$sno];
  next if $cardno eq "";
  ($sno eq "" ? $gear[$l_side][$gno] : $s_gear[$sno]) = "";
  $gear[$l_side][$gno] = join ":", @s_gear if $sno ne "";
}

sub pick_card6 {
  my ($fno, $cno, $sno) = split /-/, $csel;
  my @c_gear = split /_/, $f_cloth[$fno];
  my @s_gear = split /:/, $c_gear[$cno] if $sno ne "";
  $cardno = $sno eq "" ? $c_gear[$cno] : $s_gear[$sno];
  next if $cardno eq "";
  ($sno eq "" ? $c_gear[$cno] : $s_gear[$sno]) = "";
  $c_gear[$cno] = join ":", @s_gear if $sno ne "";
  $f_cloth[$fno] = join "_", @c_gear;
  &which_side($fno);
}

sub sforth_sub {  # シールドフォースを持つクリーチャーが場を離れた時の処理
  my $fldno = $_[0];
  foreach my $i (@{$fw3[$l_side]}) {
    next if $f_block[$i] eq "";
    my @forth = split /-/, $f_block[$i];
    @forth = grep $_ != $fldno, @forth;
    $f_block[$i] = join "-", @forth;
  }
}

sub p_mess {
  my $p_mess = "";
  if (!($l_side)) {
    $p_mess = "$pn[$u_side]は";
    $p_mess .= "$pn[$vside]の" if $vside != $u_side;
  } else {
    $p_mess = $l_side == $u_side ? "$pn[$u_side]は" : "$pn[$l_side]の";
  }
  $p_mess .= $area == 2 ? "シールドを"
       : $area ne "" ? sprintf "%sを", "《$c_name[$cardno]》"
       : $F{'decktop'} ? sprintf "山札の一番%sのカード%sを", $F{'under'} == 1 ? "下" : "上", $parea != 3 ? "、《$c_name[$cardno]》" : ""
       : $varea == 0 ? sprintf "%s%sを", $vside != $u_side ? "手札から、" : "", 3 < $parea && $vside == $u_side ? "カード" : "《$c_name[$cardno]》"
       : $varea == 1 ? "墓地から、《$c_name[$cardno]》を"
       : $varea == 3 ? "超次元ゾーンから、《$c_name[$cardno]》を"
       : $vside == $u_side && $parea == 3 && ($F{'show'}) ? "山札のカードを"
       : "山札から、《$c_name[$cardno]》を";
  $p_mess .= $parea == 1 && &syu_chk($cardno, 1) ? "ジェネレートした。"
       : $parea == 0 || $parea == 1 || $parea == 6 ? sprintf "%sに移動した。", $parea == 0 ? "マナゾーン" : $parea == 1 ? "バトルゾーン" : "シールド"
       : $parea == 2 ? "墓地に送った。"
       : $parea == 9 ? "超次元ゾーンに送った。"
       : $parea == 3 ? sprintf "手札に%s。", @sel > 0 || $F{'decktop'} ? "加えた" : "戻した"
       : sprintf "山札の%sに戻した。", $parea == 4 ? "上" : "下";
  &s_mes("$p_mess");
}

sub magic {
  my ($card, $side) = @_;
  $btl[9] = 1 if $card eq "レジェンド・アタッカー";
  if ($card eq "ビックリ・イリュージョン") {
    unshift @syori, "s-$side<>t-追加する種族を選んでください<>m-bikkuri_sel<>o-決定";
    $chudan_flg = $trigger_flg = "1";
  } elsif ($card eq "冥界の手") {
#   my @out = @shield = ();
#   foreach my $i(@{$fw3[$u_side]}){
#     push @shield, $fld[$i] if $fld[$i] ne "";
#     $fld[$i] = "";
#   }
#   push @out, splice @shield, rand @shield, 1 while @shield;
#   map { $_ =~ s/\-s$// if $_ =~ /\-s$/ } @out;
#   my $count = 0;
#   while (@out) {
#     $fld[$fw3[$u_side][$count]] = shift @out;
#     $count++;
#   }
#   &shuffle(*fw3, $side);
#   &del_null(*fw3, $side);
#   &s_mes("$pn[$side]は自分のシールドをシャッフルした！");
  } elsif ($card eq "ザ・ユニバース・ゲート") {
    &s_mes("$pn[$side]は山札を３枚めくった！");
    &s_mes("めくったカードは《$c_name[$deck[$side][0]]》《$c_name[$deck[$side][1]]》《$c_name[$deck[$side][2]]》だった！");
    $skip_flg = grep &syu_chk($_, 4), (@{$deck[$side]}[0..2]);
    &s_mes("$pn[$side]のターンがあと$skip_flg回行われる！") if 0 < $skip_flg;
  } elsif ($card eq "星龍の記憶") {
    &s_mes("$pn[$side]のシールドはすべてシールド・トリガーを得た！");
    unshift @magic, sprintf "$card<>$side<>%d", $side == $turn2 ? 3 : 2;
  }
}

sub del_move {  # 手札、山札、墓地の不要なスペースを削除
  &del_null(sprintf("%s", $varea == 0 ? *hand : $varea == 1 ? *boti : $varea == 2 ? *deck : *psychic), $vside);
}

sub del_move2 { # 進化クリーチャーの不要なスペースを削除
  foreach my $i (@{$fw1[1]}, @{$fw1[2]}) {
    $shinka[$i] = join "-", grep $_ ne "", (split /-/, $shinka[$i]) if $shinka[$i] ne "";
  }
}

sub del_move3 { # ジェネレート中のクロスギアの不要なスペースを削除
  foreach my $i(1..2) {
    @{$gear[$i]} = &del_gear_sub(\@{$gear[$i]});
  }
}

sub del_move4 { # クロスしたクロスギアの不要なスペースを削除
  foreach my $i(@{$fw1[1]}, @{$fw1[2]}) {
    next if $f_cloth[$i] eq "";
    my @c_gear = split /_/, $f_cloth[$i];
    $f_cloth[$i] = join "_", &del_gear_sub(\@c_gear);
  }
}

sub del_gear_sub {
  my $cloth = $_[0]; my @arr = @$cloth;
  foreach my $gear (@arr) {
    $gear = join ":", grep $_ ne "", (split /:/, $gear) if $gear ne "";
  }
  return grep $_ ne "", @arr;
}

sub del_move5 { # ゴッドの不要なスペースを削除
  foreach my $i(@{$fw1[1]}, @{$fw1[2]}) {
    $fld[$i] = join "-", grep $_ ne "", (split /-/, $fld[$i]) if $fld[$i] =~ /\-/;
  }
}

#--------------------------------------------------------

sub return_deck3 {
  my @value = my @evo = ();
  map { push @value, (split /-/, $_)[0];
      push @evo, (split /-/, $_)[1] } @ssel;
  my @unique = grep !$count{$_}++, @value;
  &com_error("複数のフィールドの進化カードを同時に山札に戻すことはできません") if 0 < $#unique;
  foreach $fldno (@fsel) {
    next if $fld[$fldno] eq "";
    $cardno = $fld[$fldno];
    $f_tap[$fldno] = $f_block[$fldno] = $f_drunk[$fldno] = $fld[$fldno] = "";
    &which_side($fldno);
    if ($fldno == $value[0]) {
      my @shinka = split /-/, $shinka[$fldno];
      map { push @res2, splice(@shinka, $_, 1) if $shinka[$_] ne "" } @evo;
      push @res2, $cardno;
      $cardno = "";
      $chudan = $l_side;
      &del_move2;
    } else {
      &move_sub($l_side);
      &shinka_sub($fldno);
    }
    &cloth_sub($fldno);
  }
  if (0 < @res2) {
    unshift @syori, "s-$l_side<>t-山札に戻す順番を選んでください<>m-return_sel<>o-決定<>p-1";
    $chudan_flg = "1";
  }
}

sub return_sel {
  &unique;
  my @arr_stack = @m_name = ();
  foreach my $rsel (@rsel) {
    my $rsel2 = substr $rsel, 4;
    my $cno = $res2[$rsel2];
    $res2[$rsel2] = "";
    push @m_name, "《$c_name[$cno]》";
    push @arr_stack, $cno;
  }
  $m_name = join "<br>", @m_name;
  @{$deck[$u_side]} = (@arr_stack, @{$deck[$u_side]});
  &s_mes("$m_nameを山札の上に戻した。");
  &syori_clr;
  undef @arr_stack; undef @m_name;
  $chudan_flg = "";
}

#--------------------------------------------------------

sub changer_sel1 {
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  if ($F{'run_select'}) {
    &com_error(sprintf "%sが指定されていません", $S{'p'} eq "shield" ? "シールド" : "進化クリーチャー") if $F{'select'} eq "";
    shift @syori;
    my $fno = $F{'select'};
    my @card = ();
    if ($S{'a'} eq "field") {
      foreach $fldno (split /-/, $chudan) {
        next if $fldno == $fno;
        &pick_card2;
        push @card, $cardno;
      }
      @card = (@card, split /-/, $shinka[$fno]) if $shinka[$fno] ne "";
    } else {
      $chudan .= "-$shinka[$fno]" if $shinka[$fno] ne "";
      @card = split /-/, $chudan;
    }
    if ($S{'p'} eq "shield") {
      my $name = join "", map { "《" . $c_name[$_] . "》"; } @card if $S{'a'} eq "field";
      &s_mes(sprintf "$pn[$u_side]は%s%sをシールドの下に置いた。",
        $S{'a'} eq "field" ? "" : $S{'a'} eq "0" ? "手札から" : $S{'a'} eq "1" ? "墓地から" : "山札から",
        $S{'a'} eq "field" ? "$name" : "カード"
      );
      for (my ($i) = 0; $i < scalar @card; $i++) {
        if (&syu_chk($card[$i], 145) || &syu_chk($card[$i], 150) || &syu_chk($card[$i], 103) || &syu_chk($card[$i], 119) || &syu_chk($card[$i], 151) || &syu_chk($card[$i], 185) || &syu_chk($card[$i], 186)) {
          s_mes("《$c_name[$card[$i]]》は超次元ゾーンに送られた。");
          push (@{$psychic[$u_side]}, splice (@card, $i, 1));
          $i--;
        }
      }
      $shinka[$fno] = join "-", @card;
      $chudan = $chudan_flg = "";
      undef @card;
    } else {
      $chudan = $fno;
      @res2 = @card;
      unshift @syori, "s-$u_side<>t-カードを置く順番を選んでください<>m-changer_sel2<>o-決定";
    }
  } else {
    &e_mes("カードの移動をキャンセルしました", $u_side);
    if ($S{'a'} ne "field") {
      local *arr = $S{'a'} == 0 ? *hand : $S{'a'} == 1 ? *boti : *deck;
      map { unshift @{$arr[$u_side]}, $_ } (split /-/, $chudan);
    }
    shift @syori; undef @res2; $chudan = $chudan_flg = $trigger_flg = "";
  }
}


sub changer_sel2 {
  &unique;
  my @arr_stack = ();
  foreach my $rsel (@rsel) {
    my $rsel2 = substr $rsel, 4;
    my $cno = $res2[$rsel2];
    $res2[$rsel2] = "";
    $m_name .= "《$c_name[$cno]》<br>";
    push @arr_stack, $cno;
  }
  @arr_stack = reverse @arr_stack;
  $shinka[$chudan] = join "-", @arr_stack;
  &s_mes("$pn[$u_side]は$m_nameを《$c_name[$fld[$chudan]]》の下に置いた。");
  &syori_clr;
  $chudan_flg = $trigger_flg = "";
}

#--------------------------------------------------------

sub put_gear_chk {
  local $cno = $_[0];
  if ($_[1] eq "tri" && &tri_chk($cno, 1)) { # トリガーかつクロスギアＸの場合
    @res = grep $fld[$_] ne "", @{$fw1[$btl[1]]};
    if ($#res < 0) {
      unshift @{$gear[$btl[1]]}, $cno;
      &e_mes("クリーチャーがいないのでクロスギアをジェネレートします", $btl[1]);
      &s_mes("シールド・トリガー、クロスギアＸ！　《$c_name[$cno]》をジェネレートした！");
      &pursue_sub;
      &breaker;
    } else {
      &put_card_dialog($cno, "tri");
    }
  } elsif ($_[1] eq "tri" && $c_evo[$cno] != 1 && &s_tri_chk) { # トリガーの場合
    unshift @{$gear[$btl[1]]}, $cno;
    &s_mes("シールド・トリガー、超動！　《$c_name[$cno]》をジェネレートした！");
    &pursue_sub;
    &breaker;
  } elsif ($c_evo[$cno] == 1) { # 進化クロスギアの場合
    local @rnb = split /,/, $c_bun[$cno];
    map { &put_gear_chk_sub(split /_/, $f_cloth[$_]) if $f_cloth[$_] } @{$fw1[$u_side]};
    &put_gear_chk_sub(@{$gear[$u_side]});
    &com_error("進化できるクロスギアがバトルゾーンにありません") if $s_cou < 1;
  }
}

sub put_gear_chk_sub {
  my @gear = @_;
  foreach my $gear(@gear) {
    next unless $gear;
    $gear = (split /:/, $gear)[-1] if $gear =~ /:/;
    if ($c_name[$cno] eq "龍刃 ヤマト・スピリット") {
      $s_cou++ if &syu_chk($gear, 88) || $c_name[$gear] eq "レオパルド・グローリーソード";
    } else {
      $s_cou++ if &bun_chk2($gear, \@rnb) || $c_name[$gear] eq "レオパルド・グローリーソード";
    }
  }
}

sub put_cre_chk {
  my $cno = $_[0];
  if ($c_evo[$cno] ne "") {   # 進化クリーチャーの処理
    if ($c_evo[$cno]>=8 && $c_evo[$cno] < 11) {  # マナ進化
      my @bun = (split /,/, $c_bun[$cno]);
      foreach my $i(@{$fw4[$u_side]}){
        next if $fld[$i] eq "";
        push @res, $i if &bun_chk2($fld[$i], \@bun) && !(&syu_chk($fld[$i], 0, 1));
      }
    }elsif ($c_evo[$cno]==11) {  # 墓地進化
      my @bun = (split /,/, $c_bun[$cno]);
      foreach (0..$#{$boti[$u_side]}){
        push @res, $_ if &bun_chk2($boti[$u_side][$_], \@bun) && !(&syu_chk($boti[$u_side][$_], 0, 1));
      }
    }elsif ($c_evo[$cno]>=12) {  # 墓地進化V・GV
      my @bun = (split /,/, $c_bun[$cno]);
      my @vor = $c_name[$cno] eq "火之鳥カイザー・アイニー" ? (59)
            : $c_name[$cno] eq "超神龍ハカイシ・ハカイ" ? (44)
            : (-1);
      foreach (0..$#{$boti[$u_side]}){
        if ($vor[0] != -1) {
          push @res, $_ if &syu_chk2($boti[$u_side][$_], \@vor);
        } else {
          push @res, $_ if &bun_chk2($boti[$u_side][$_], \@bun) && !(&syu_chk($boti[$u_side][$_], 0, 1));
        }
      }
    } elsif (4 <= $c_evo[$cno]) {
      if ($c_name[$cno] eq "ＪＫ神星シャバダバドゥー") {
        @res = grep $fld[$_] ne "", @{$fw1[$u_side]};
      } elsif ($c_name[$cno] eq "双流星キリン・レガシー") {
        @res = &rainbow_chk;
      } elsif ($c_evo[$cno] == 4) { # ギャラクシーボルテックス
        @vor = $c_name[$cno] eq "超神星ヴィーナス・ラ・セイントマザー" ? (12, 23, 9)
           : $c_name[$cno] eq "超神星マーキュリー・ギガブリザード" ? (23, 38, 35)
           : $c_name[$cno] eq "超神星プルート・デスブリンガー" ? (42, 38, 54)
           : $c_name[$cno] eq "超神星マーズ・ディザスター" ? (54, 72, 58)
           : $c_name[$cno] eq "超神星ジュピター・キングエンパイア" ? (72, 9, 78)
           : $c_name[$cno] eq "超神星ライラ・ボルストーム" ? (44, 50, 66)
           : $c_name[$cno] eq "超神星ネプチューン・シュトローム" ? (38, 41, 11)
           : $c_name[$cno] eq "超神星ペテルギウス・ファイナルキャノン" ? (23, 38, 83)
           : $c_name[$cno] eq "超神星アポロヌス・ドラゲリオン" ? (44, 50, 62, 66, 82, 83)
           : $c_name[$cno] eq "超神星ウラヌス・ナインテイル" ? (3)
           : $c_name[$cno] eq "超神星ビッグバン・アナスタシス" ? (9, 72, 23)
           : $c_name[$cno] eq "超神星ブラックホール・サナトス" ? (38, 54, 31, 61)
#          : $c_name[$cno] eq "竜魔神王バルカディア・NEX" ? (11,41,50)
           : (50, 54, 61);
        &shinka_chk(@vor);
      } elsif ($c_evo[$cno] == 7) { # 文明進化Ｖ
        @vor = $c_name[$cno] eq "鋼流星ペングカイザー" ? (0, 1)
           : $c_name[$cno] eq "魔流星アモン・ベルス" ? (1, 2)
           : ($c_name[$cno] eq "闘流星ナイトスクリーマー" || $c_name[$cno] eq "暗黒凰ゼロ・フェニックス") ? (2, 3)
           : $c_name[$cno] eq "幻流星ミスター・イソップ" ? (3, 4)
           : $c_name[$cno] eq "龍炎凰インフィニティ・フェニックス" ? (3)
           : (4, 0);
        &shinka_chk2(@vor);
      } else {            # 通常の進化Ｖ
        @vor = $c_name[$cno] eq "光彗星アステロイド・マイン" ? (9, 81, 82)
           : $c_name[$cno] eq "氷彗星アステロイド・レイザ" ? (23, 80, 83)
           : $c_name[$cno] eq "闇彗星アステロイド・ゲルーム" ? (38, 31, 44)
           : $c_name[$cno] eq "炎彗星アステロイド・ガウス" ? (54, 61, 50)
           : $c_name[$cno] eq "地彗星アステロイド・ガイア" ? (72, 74, 66)
           : $c_name[$cno] eq "光彗星アステロイド・ルクサス" ? (44, 50, 62, 66, 82, 83, 59, 54)
           : $c_name[$cno] eq "英霊王スターマン" ? (20, 28)
           : $c_name[$cno] eq "蛇魂王ナーガ" ? (33, 37)
           : $c_name[$cno] eq "暗黒王デス・フェニックス" ? (44, 59)
           : $c_name[$cno] eq "太陽王ソウル・フェニックス" ? (59, 66)
           : $c_name[$cno] eq "聖獣王ペガサス" ? (76, 11)
           : $c_name[$cno] eq "超聖竜ボルフェウス・ヘヴン" ? (11, 50)
           : $c_name[$cno] eq "龍炎鳳エターナル・フェニックス" ? (59, 50)
           : $c_name[$cno] eq "星狼凰マスター・オブ・デスティニー" ? (88, 89)
           : $c_name[$cno] eq "戦極竜ヴァルキリアス・ムサシ" ? (88)
           : $c_name[$cno] eq "暗黒皇グレイテスト・シーザー" ? (44, 50, 62, 66, 82, 83, 89)
           : $c_name[$cno] eq "超聖竜シデン・ギャラクシー" ? (11, 44, 50, 62, 66, 82, 83)
           : (88);
        &shinka_chk(@vor);
      }
    } else {
      if ($c_name[$cno] eq "伝説のサンテ・ガト・デ・パコ") {
        &shinka_chk(72);
      } elsif ($c_name[$cno] eq "大邪眼バルクライ王") {
        &shinka_chk(40);
      } elsif (&syu_chk($cno, 2) && &c_chk("シータ・トゥレイト")) {
        @res = grep $fld[$_] ne "", @{$fw1[$u_side]};
      } elsif ($c_evo[$cno] == 3) { # ドラゴン進化
        my @evo = $c_name[$cno] eq "超竜騎神ボルガウルジャック" ? (44, 50, 62, 66, 82, 83, 54) : (44, 50, 62, 66, 82, 83);
        &shinka_chk(@evo);
      } elsif ($c_evo[$cno] == 2) { # 多色進化
        @res = &rainbow_chk;
      } elsif (&syu_chk($cno, 88)) {  # サムライ進化
        &shinka_chk(88);
      } elsif (&syu_chk($cno, 89)) {  # ナイト進化
        &shinka_chk(89);
      } else {
        &shinka_chk(split /,/, $c_syu[$cno]);
      }
    }
    undef %tmp;
    @res = grep !$tmp{$_}++, @res;
    if ((($c_evo[$cno] == 4 || $c_evo[$cno] == 10 || $c_evo[$cno] == 13 ) && $#res < 2) || ((4 < $c_evo[$cno] && $c_evo[$cno] != 8 && $c_evo[$cno] != 11) && $#res < 1) || $#res < 0) {
      undef @res;
      undef @vor if 0 < $#res;
      my $str = $#res < 0 && $c_evo[$cno] !~ /4|5|6|7|9|10|12|13/ ? sprintf "進化できるクリーチャーが%sにいません", $c_evo[$cno] < 8 ? "バトルゾーン" : $c_evo[$cno] == 8 ? "マナゾーン" : "墓地" : sprintf "%sボルテックスに必要なクリーチャーが揃っていません", $c_evo[$cno] == 4 || $c_evo[$cno] == 10 || $c_evo[$cno] == 13 ? "ギャラクシー・" : "";
      if ($_[1] eq "tri") {
        &e_mes("$str", $btl[1]);
        &e_mes("シールドを手札に戻します", $btl[1]);
        &pursue;
        &breaker;
      } else {
        &com_error("$str");
      }
    }
  } elsif (&syu_chk($cno, 84)) {  # ゴッド
    if ($c_name[$cno] =~ /天神|海神|黒神|炎神|地神/) {
      foreach my $i (@{$fw1[$u_side]}) {
        push @res, $i if ($c_name[$cno] eq "黒神ダーク・インドラ" && $fld[$i] =~ /^1963|1966$/)
                || ($c_name[$cno] eq "炎神フレイム・アゴン" && $fld[$i] =~ /^1964|1962$/)
                || ($c_name[$cno] eq "地神エメラルド・ファラオ" && $fld[$i] =~ /^1965|1963$/)
                || ($c_name[$cno] eq "天神シャイン・バルキリー" && $fld[$i] =~ /^1966|1964$/)
                || ($c_name[$cno] eq "海神ブルー・ポセイドン" && $fld[$i] =~ /^1962|1965$/);
      }
    } else {
      @god = $c_name[$cno] eq "G・A・ペガサス" ? ("1713")
         :$c_name[$cno] eq "G・E・レオパルド" ? ("1709")
         :$c_name[$cno] eq "竜極神ゲキ" ? ("1712")
         :$c_name[$cno] eq "竜極神メツ" ? ("1711")
         :$c_name[$cno] eq "金剛神ガナストラ" ? ("1723")
         :$c_name[$cno] eq "修羅王ガラサラマ" ? ("1721")
         :$c_name[$cno] eq "邪道神キキ" ? ("1729")
         :$c_name[$cno] eq "外道神カイカイ" ? ("1724")
         :$c_name[$cno] eq "千刃の武象ギリトラワンガ" ? ("1766")
         :$c_name[$cno] eq "千呪の魔象ギリメノアイル" ? ("1763")
         :$c_name[$cno] eq "炎武神バルザック" ? ("1822")
         :$c_name[$cno] eq "地武神オルメガス" ? ("1821")
         :$c_name[$cno] eq "界神オットー" ? ("1850")
         :$c_name[$cno] eq "罪神イザナ" ? ("1846")
         :$c_name[$cno] eq "幻神ドッコイ" ? ("1837")
         :$c_name[$cno] eq "罰神オルフェ" ? ("1839")
         :$c_name[$cno] eq "封神ゴート" ? ("1849")
         :$c_name[$cno] eq "闘神タウロス" ? ("1842")
         :$c_name[$cno] eq "雷神リキ" ? ("1848")
         :$c_name[$cno] eq "霊神ゴウ" ? ("1847")
         :$c_name[$cno] eq "戦神アロロ" ? ("1851")
         :$c_name[$cno] eq "回神パロロ" ? ("1843")
         :$c_name[$cno] eq "究極神アク" ? ("1899")
         :$c_name[$cno] eq "超絶神ゼン" ? ("1894")
         :$c_name[$cno] eq "極上神プロディジー" ? ("1910", "1906")
         :$c_name[$cno] eq "崇高神ケミカル" ? ("1911", "1904")
         :$c_name[$cno] eq "至高神オービタル" ? ("1911", "1904")
         :$c_name[$cno] eq "無上神アンダーワールド" ? ("1910", "1906")
         :$c_name[$cno] eq "龍神ヘヴィ" ? ("1953", "1954", "1953-1954")
         :$c_name[$cno] eq "破壊神デス" ? ("1952", "1954", "1952-1954")
         :$c_name[$cno] eq "龍神メタル" ? ("1952", "1953", "1952-1953")
         :$c_name[$cno] eq "朱雀神ガリョウ" ? ("2029")
         :$c_name[$cno] eq "白虎神テンセイ" ? ("2030")
         :$c_name[$cno] eq "魔光神ルドヴィカ２世" ? ("2032")
         :$c_name[$cno] eq "神帝ヴィシュ" ? ("2450", "2382", "2643","2367-2450","2367-2382","2367-2643","2367-2382-2450","2367-2450-2643")
         :$c_name[$cno] eq "神帝アナ" ? ("2367","2410", "2642","2367-2450","2410-2450","2450-2642","2367-2450-2642","2367-2410-2450")
         :$c_name[$cno] eq "神帝マニ" ? ("2450", "2382", "2643","2367-2450","2367-2382","2367-2643","2367-2382-2450","2367-2450-2643")
         :$c_name[$cno] eq "神帝スヴァ" ? ("2367","2410", "2642","2367-2450","2410-2450","2450-2642","2367-2450-2642","2367-2410-2450")
         :$c_name[$cno] eq "神帝ムーラ" ? ("2410", "2642", "2367","2382-2410","2410-2643","2382-2642","2642-2643","2367-2382","2367-2643","2367-2382-2410","2367-2382-2642","2367-2410-2643","2367-2642-2643")
         :$c_name[$cno] eq "神帝アージュ" ? ("2382", "2643", "2450","2382-2410","2382-2642","2410-2643","2642-2643","2410-2450","2450-2642","2382-2410-2450","2410-2450-2643","2382-2450-2642","2450-2642-2643")
         :$c_name[$cno] eq "神王タイタス" ? ("2621","2875","2621-2875","2621-2873-2875")
         :$c_name[$cno] eq "イズモ" ? ("3968","3969","3978","3979","4007","4008","4009","4010","4026","4027","4048","4049" , "4302","4281","4127","4183","4304","4280","4128","4184","3968-3969","3968-3979","3968-4007","3968-4009","3968-4026","3968-4048","3968-4304","3968-4280","3968-4128","3968-4184","3978-3969","3978-3979","3978-4007","3978-4009","3978-4026","3978-4048","3978-4304","3978-4280","3978-4128","3978-4184","4008-3969","4008-3979","4008-4007","4008-4009","4008-4026","4008-4048","4008-4304","4008-4280","4008-4128","4008-4184","4010-3969","4010-3979","4010-4007","4010-4009","4010-4026","4010-4048","4010-4304","4010-4280","4010-4128","4010-4184","4027-3969","4027-3979","4027-4007","4027-4009","4027-4026","4027-4048","4027-4304","4027-4280","4027-4128","4027-4184","4049-3969","4049-3979","4049-4007","4049-4009","4049-4026","4049-4048","4049-4304","4049-4280","4049-4128","4049-4184","4302-3969","4302-3979","4302-4007","4302-4009","4302-4026","4302-4048","4302-4304","4302-4280","4302-4128","4302-4184","4281-3969","4281")
         :$c_name[$cno] eq "神人類 ヨミ" ? ("3968","3969","3978","3979","4007","4008","4009","4010","4026","4027","4048","4049")
         :$c_name[$cno] eq "悪魔右神ダフトパンク" ? ("3969","3979","4007","4009","4026","3956","4011","4048")
         :$c_name[$cno] eq "爆裂右神ストロークス" ? ("3969","3979","4007","4009","4026","3956","4011","4048")
         :$c_name[$cno] eq "戦攻右神マッシヴ・アタック" ? ("3969","3979","4007","4009","4026","3956","4011","4048")
         :$c_name[$cno] eq "霊騎右神ニルヴァーナ" ? ("3969","3979","4007","4009","4026","3956","4011","4048")
         :$c_name[$cno] eq "双天右神クラフト・ヴェルク" ? ("3969","3979","4007","4009","4026","3956","4011","4048")
         :$c_name[$cno] eq "聖霊左神ジャスティス" ? ("3956","3968","3978","4008","4010","4027","4011","4049")
         :$c_name[$cno] eq "封魔左神リバティーンズ" ? ("3956","3968","3978","4008","4010","4027","4011","4049")
         :$c_name[$cno] eq "妖精左神パールジャム" ? ("3956","3968","3978","4008","4010","4027","4011","4049")
         :$c_name[$cno] eq "夢幻左神スクエア・プッシャー" ? ("3956","3968","3978","4008","4010","4027","4011","4049")
         :$c_name[$cno] eq "双魔左神ディーヴォ" ? ("3956","3968","3978","4008","4010","4027","4011","4049")
         :$c_name[$cno] eq "真滅右神ブラ―" ? ("3969","3979","4007","4009","4026","3956","4011","4048")
         :$c_name[$cno] eq "龍機左神オアシス" ? ("3956","3968","3978","4008","4010","4027","4011","4049")
         :$c_name[$cno] eq "神王リア" ? ("2873","2603","2603-2873","2603-2873-2875")
         :$c_name[$cno] eq "名も無き神人類" ? ("1709","1711","1712","1713","1721","1723","1724","1729","1763","1766","1821","1822","1837","1839","1842","1846","1847","1848","1850","1851","1894","1899","1904","1906","1911","1952","1953","1954","1962","1963","1964")
         :$c_name[$cno] eq "神王オセロー" ? ("2621","2875","2621-2875","2603-2621-2875")
         :$c_name[$cno] eq "神王マクベス" ? ("2873","2603","2603-2873","2621-2603-2873")
         :("2031");
      foreach my $i (@{$fw1[$u_side]}) {
        next if $fld[$i] eq "";
        map { push @res, $i if $fld[$i] eq $_ } @god;
      }
    }
    undef @res if $#res < 0;
  }
}

sub put_cre_chk2 { # 強制的に上に置く場合に使用
  my $cno = $_[0];
  map { push @res, $_} @{$fw1[$u_side]};
}

sub put_card_dialog {
  my ($cno, $process) = @_;
  my $str = &syu_chk($cno, 84) ? "Ｇ・リンクしますか？<>m-glink_sel<>o-する::しない"
      : &syu_chk($cno, 96) ? "要塞化するシールドを選択してください<>m-castle_sel<>o-決定::やめる"
      : &syu_chk($cno, 1) && !($c_evo[$cno]) ? "クロスさせるクリーチャーを選択してください<>m-cloth_sel2<>o-決定::やめる"
      : sprintf "%s%sを選んでください<>m-%s_sel<>o-決定::やめる",
        3 < $c_evo[$cno] && $c_evo[$cno] != 8 && $c_evo[$cno] != 11 ? "一番下の" : "進化させる",
        &syu_chk($cno, 1) ? "クロスギア" : "クリーチャー",
        &syu_chk($cno, 1) && $c_evo[$cno] != 11 ? "c_shinka" : 3 < $c_evo[$cno] && $c_evo[$cno] != 8 ? $c_evo[$cno] == 11 ? "b_shinka" : 12 <= $c_evo[$cno] ?"b_vor" : "vor" : "shinka";
  unshift @syori, sprintf "s-%d<>t-$str<>a-%s%s",
        $process eq "tri" ? $btl[1] : $u_side,
        $process eq "tri" ? "tri" : $F{'decktop'} ? "decktop" : $process ne "" ? "$process" : "",
        $process eq "tri" ? "<>p-tri" : "";
  $chudan_flg = "1";
  $chudan = $cno;
  $vor_cnt = 0 if 3 < $c_evo[$cno];
  undef @res if &syu_chk($cno, 96);
}

sub put_card_dialog2 { # 強制的に置く場合に使用
  my ($cno, $process) = @_;
  my $str = sprintf "%s%sを選んでください<>m-%s_sel<>o-決定::やめる",
        "下になる",
        "クリーチャー",
        "add_up_card";
  unshift @syori, sprintf "s-%d<>t-$str<>a-%s%s",
        $process eq "tri" ? $btl[1] : $u_side,
        $process eq "tri" ? "tri" : $F{'decktop'} ? "decktop" : $process ne "" ? "$process" : "",
        $process eq "tri" ? "<>p-tri" : "";
  $chudan_flg = "1";
  $chudan = $cno;
  $vor_cnt = 0 if 3 < $c_evo[$cno];
  undef @res if &syu_chk($cno, 96);
}

sub rainbow_chk { # 多色クリーチャーの配列を返す
  return (grep &k_chk($fld[$_], 12)
         || $fld[$_] =~ /\-/  # リンク中のゴッド
         || (&c_chk("染空の守護者エルス・エリクシオン") && $c_bun[$fld[$_]] =~ /[14]/)
         || (&c_chk("ペイント・フラッペ") && $c_bun[$fld[$_]] =~ /[20]/)
         || (&c_chk("黒染妃ゼノビア") && $c_bun[$fld[$_]] =~ /[31]/)
         || (&c_chk("染風の宮司カーズ") && $c_bun[$fld[$_]] =~ /[42]/)
         || (&c_chk("幻染妖精リリアン") && $c_bun[$fld[$_]] =~ /[03]/), @{$fw1[$u_side]});
}

sub bikkuri_sel { # ビックリ・イリュージョン
  return if !($F{'run_select'});
  &com_error("追加する種族を指定してください") if $F{'add'} eq "";
  push @syu_add, $F{'add'};
  &s_mes("$pn[$u_side]のクリーチャーに種族：$syu[$F{'add'}]が追加された！");
  $chudan_flg = $trigger_flg = "";
  &syori_clr;
}

sub shinka_chk {  # 進化（種族）元クリーチャーのチェック
  my @evo = @_;
  map { push @res, $_ if &syu_chk2($fld[$_], \@evo) || ($c_name[$fld[$_]] eq "式神イノセント" && 6 < &morph_chk($u_side)) || $c_name[$fld[$_]] =~ /無垢|無頼剣兵ドラグイノセント/ || &cloth_chk($_, 1302) } @{$fw1[$u_side]};
  &armored_chk if grep $_ == 50, @evo;
  &accel_chk("開龍妖精フィーフィー")  if grep $_ == 66, @evo;
  &accel_chk("武装兵ミステリアス")  if grep $_ == 62, @evo;
  &accel_chk("精撃の使徒アリッサ")  if grep $_ == 11, @evo;
  &accel_chk("悪魔怪人デスブラッド")  if grep $_ == 41, @evo;
}

sub shinka_chk3 {  # 墓地進化（種族）元クリーチャーのチェック TODO 本当はこれでチェックしたい
  my @evo = @_;
  map { push @res, $_ if &syu_chk2($boti[$u_side][$_], \@evo) } 0..$#{$boti[$u_side]};
}

sub shinka_chk2 { # 進化（文明）元クリーチャーのチェック
  my @bun = @_; my @evo = ();
  foreach my $bun(@bun) {
    my @bun2 = ($bun);
    map { push @evo, $_ if $fld[$_] ne "" && &bun_chk2($fld[$_], \@bun2) } @{$fw1[$u_side]};
    if ($#evo < 0) {
      undef @res; undef @vor;
      &com_error("ボルテックス進化に必要なクリーチャーが揃っていません");
    }
    @res = (@res, @evo);
    undef @evo;
  }
}

sub shinka_chk4 { # 墓地進化（文明）元クリーチャーのチェック TODO 本当はこれでチェックしたい
  my @bun = @_; my @evo = ();
  foreach my $bun(@bun) {
    my @bun2 = ($bun);
    map { push @evo, $_ if $boti[$u_side][$_] ne "" && &bun_chk2($boti[$u_side][$_], \@bun2) } 0..$#{$boti[$u_side]};
    if ($#evo < 0) {
      undef @res; undef @vor;
      &com_error("ボルテックス進化に必要なクリーチャーが揃っていません");
    }
    @res = (@res, @evo);
    undef @evo;
  }
}

sub accel_chk {   # 自分のバトルゾーンにアクセル状態の指定クリーチャーがいるかどうか
  my $card = $_[0];
  map { push @res, $_ if $f_cloth[$_] ne "" && $c_name[$fld[$_]] eq $card } @{$fw1[$u_side]};
}

sub accel_chk2 {  #
  my $fno = shift; my @cre = @_;
  return 0 if $f_cloth[$fno] eq "";
  return grep $c_name[$fld[$fno]] eq $_, @cre;
}

sub armored_chk {
  map { push @res, $_ if (!(&syu_chk($fld[$_], 50)) && &cloth_chk($_, 1106, 2050)) || (&syu_chk($fld[$_], 56) && $btl[9]) } @{$fw1[$u_side]};
}

sub syu_chk {
  my $card = shift; my @syu = @_;
  &syu_chk2($card, \@syu);
}

sub syu_chk2 {
  my ($card, $syu) = @_; my @vals = ();
  map { push @vals, split /,/, $c_syu[$_] } (split /\-/, $card);
  @vals = (@vals, @syu_add) if $F{'mode'} ne "meteo_sel";
  push @vals, 41 if &c_chk("封魔の戦慄ジュマゾール", $u_side) && $c_syu[$card] =~ /38/;
  @vals = (@vals, 66, 82) if &c_chk("無双龍聖ジオ・マスターチャ", $u_side) && (4 <= $c_mana[$card] || $card =~ /\-/);
  @vals = (@vals, 50, 66, 88) if &c_chk("武装竜鬼ジオゴクトラ", $u_side) && (4 <= $c_mana[$card] || $card =~ /\-/);
  undef %E;
  map { $E{$_} = 1 } @$syu;
  return grep $E{$_}, @vals;
}

sub bun_chk {
  my $card = shift; my @bun = @_;
  &bun_chk2($card, \@bun);
}

sub bun_chk2 {
  my ($card, $bun) = @_; my @vals = ();
  map {
    push @vals, split /,/, $c_bun[$_];
    push @vals, 0 if &c_chk("染空の守護者エルス・エリクシオン") && $c_bun[$_] =~ /[14]/;
    push @vals, 1 if &c_chk("ペイント・フラッペ") && $c_bun[$_] =~ /[20]/;
    push @vals, 2 if &c_chk("黒染妃ゼノビア") && $c_bun[$_] =~ /[31]/;
    push @vals, 3 if &c_chk("染風の宮司カーズ") && $c_bun[$_] =~ /[42]/;
    push @vals, 4 if &c_chk("幻染妖精リリアン") && $c_bun[$_] =~ /[03]/;
  } (split /\-/, $card);
  undef %E;
  map { $E{$_} = 1 } @$bun;
  return grep $E{$_}, @vals;
}

sub cloth_chk { # 指定フィールドのクリーチャーが指定したクロスギア（複数種類可能）をクロスしているかどうかのチェック
  my $fno = shift; my @gear = @_;
  foreach my $c_gear(split /_/, $f_cloth[$fno]) {
    $c_gear = (split /:/, $c_gear)[-1] if $c_gear =~ /:/; # 進化クロスギアの場合
    foreach my $s_gear(@gear) {
      return 1 if $c_gear == $s_gear;
    }
  }
  return 0;
}

sub put_card2_sub {
  &fld_chk($l_side);
  &p_mess;
  my $fno = $parea == 0 ? $nf3 : $nf2;
  my $e_side = $l_side ? 3 - $l_side : 3 - $u_side;
  if (syu_chk($cardno, 145) || syu_chk($cardno, 150) || syu_chk($cardno, 103) || syu_chk($cardno, 119) || syu_chk($cardno, 151) || syu_chk($cardno, 185) || syu_chk($cardno, 186)) {
    s_mes("《$c_name[$cardno]》は超次元ゾーンに送られた。");
    push (@{$psychic[$side]}, $cardno);
  } else {
    $f_tap[$fno] = &k_chk($cardno, 12) || &c_chk("停滞の影タイム・トリッパー", $e_side) ? "1" : "0" if $parea == 0;
    $fld[$fno] = $cardno;
  }
}

sub cloth_sub {
  my $fno = $_[0];
  if ($fld[$fno] eq "" && $f_cloth[$fno] ne "") {
    push @{$gear[$l_side]}, (split /_/, $f_cloth[$fno]);
    $f_cloth[$fno] = "";
  }
}

sub flip_sel {  # シールドを表向きにする
  return if (!($F{'run_select'}) && !($F{'not_select'}));
  if ($F{'run_select'}) {
    map { push @fsel, $1 if $_ =~ /^fsel(\d+)/ } (keys(%F));
    &com_error("表向きにするシールドが選ばれていません") if @fsel < 1;
    map {
      &which_side($_);
      $fld[$_] .= "-s" if $area == 2 || $fld[$_] ne ""
    } @fsel;
    &s_mes("《$c_name[$chudan]》の能力でシールドを表向きにした！");
    undef @fsel;
  } else {
    $chudan = $chudan_flg = "";
    @syori = ();
  }
}

sub cloth {
# &com_error("$phasestr[$phase]にはクロスはできません") if $phase =~ /[12]/;
  &com_error("自分のバトルフィールドにクロスギアがありません") if $#{$gear[$u_side]} < 0 && !(grep $f_cloth[$_] ne "", @{$fw1[$u_side]});
  &com_error("自分のバトルゾ?ンにクリーチャーがいません") unless grep $fld[$_] ne "", @{$fw1[$u_side]};
  unshift @syori, "s-$u_side<>t-クロスギアを選択してください<>m-cloth_sel<>o-決定::やめる";
  $chudan_flg = "1";
}

sub cloth_sel1 {
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'not_select'}) {
    &e_mes("クロスギアの選択をキャンセルしました", $u_side);
    shift @syori;
    $chudan_flg = "";
  } else {
    map { push @{$1}, $2 if $_ =~ /(^.?sel)(.+)/ } keys(%F);
#   foreach $key (keys(%F)) { push @{$1}, $2 if $key =~ /(gsel|csel)(.+)/ }
    &com_error("クロスギアが指定されていません") if $#gsel < 0 && $#csel < 0;
    &com_error("複数のクロスギアを一度にクロスすることはできません") if $#gsel == 0 && $#csel == 0;
    if ($gsel[0] ne "") {
      my ($side, $gno, $dummy) = split /-/, $gsel[0];
      $cardno = splice @{$gear[$side]}, $gno, 1;
    } else {
      my ($fno, $cno, $dummy) = split /-/, $csel[0];
      my @c_gear = split /_/, $f_cloth[$fno];
      $cardno = splice @c_gear, $cno, 1;
      $f_cloth[$fno] = join "_", @c_gear;
      &which_side($fno);
    }
    $chudan = $cardno;
    $syori[0] = sprintf "s-$u_side<>t-クロスさせるクリーチャーを選択してください<>m-cloth_sel2<>o-決定::やめる<>g-%s", $gsel[0] ne "" ? "g" : $csel[0];
    undef @gsel; undef @csel;
  }
}

sub cloth_sel2 {
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'not_select'}) {
    &syori_p_set;
    if ($S{'g'} eq "g") {
      unshift @{$gear[$u_side]}, $chudan;
    } else {
      my ($fno, $k) = split /\-/, $S{'g'};
      $f_cloth[$fno] .= $f_cloth[$fno] eq "" ? "$chudan" : "_$chudan";
    }
    &e_mes("クロスをキャンセルしました", $u_side);
  } else {
    map { push @fsel, $1 if $_ =~ /^fsel(\d+)/ } keys(%F);
    &com_error("クロスさせるクリーチャーが指定されていません") if $#fsel < 0;
    my $fno = $fsel[0];
    &which_side($fno);
    &com_error("自分のクリーチャーにしかクロスできません") if $l_side != $u_side;
    $f_cloth[$fno] .= $f_cloth[$fno] eq "" ? "$chudan" : "_$chudan";
    $chudan = (split /:/, $chudan)[-1] if $chudan =~ /:/;
    &s_mes("シールド・トリガー、超動！") if $S{'p'} eq "tri";
    &s_mes(sprintf "クロス、《$c_name[$chudan]》！　$pn[$u_side]の%sを超強化！", &card_name_sub($fno));
  }
  shift @syori;
  unshift @syori, "s-$btl[1]<>t-シールド・トリガーの処理を終了しますか？<>m-trigger_sel3<>o-終了する" if $S{'p'} eq "tri";
  $chudan = $chudan_flg = $trigger_flg = "";
  undef %F; undef %S; undef @fsel; undef @res;
}

sub fld_chk {
  my $side = $_[0];
  $nf0 = $nf1 = $nf2 = $nf3 = -1;
  foreach my $i (@{$fw1[$side]}) { if ($fld[$i] eq "") { $nf0 = $i; last; } }
  foreach my $i (@{$fw2[$side]}) { if ($fld[$i] eq "") { $nf1 = $i; last; } }
  foreach my $i (@{$fw3[$side]}) { if ($fld[$i] eq "") { $nf2 = $i; last; } }
  foreach my $i (@{$fw4[$side]}) { if ($fld[$i] eq "") { $nf3 = $i; last; } }
}

sub b_shinka_sel {
	&shinka_sel;
}

sub shinka_sel {
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  if ($F{'run_select'}) {
    &s_mes("シールド・トリガー、超動！") if $S{'p'} eq "tri";
    &s_mes(sprintf "%sの進化クリーチャー・《$c_name[$chudan]》降臨！", $S{'p'} eq "tri" ? "$pn[$btl[1]]" : "$pn[$u_side]");
    if ($c_evo[$chudan] == 8) { &mana_shinka_sub; } elsif ($c_evo[$chudan] == 11) { &boti_shinka_sub; } else { &shinka_sub2; }
    shift @syori;
    if ($S{'p'} eq "tri") {
      unshift @syori, "s-$btl[1]<>t-シールド・トリガーの処理を終了しますか？<>m-trigger_sel3<>o-終了する";
      $trigger_flg = "1";
    }
    $chudan_flg = "";
    &put_battle_zone_koka($chudan, $fno);
  } else {
    &e_mes("進化をキャンセルしました", $u_side);
    if ($S{'p'} eq "tri") {
      &pursue;
      &breaker;
    } elsif ($S{'a'} =~ /^fld/) {
      ($fldno = $S{'a'}) =~ s/fld//;
      $fld[$fldno] = $chudan;
    } elsif ($S{'a'} =~ /^shinka/) {
      ($ssel = $S{'a'}) =~ s/shinka//;
      ($fldno, $sno) = split /-/, $ssel;
      my @evo = split /-/, $shinka[$fldno];
      $evo[$sno] = $chudan;
      $shinka[$fldno] = join "-", @evo;
    } else {
      local *arr = $S{'a'} eq "0" ? *hand : $S{'a'} eq "1" ? *boti : *deck;
      unshift @{$arr[$u_side]}, $chudan;
    }
    shift @syori;
    $chudan = $chudan_flg = "";
  }
  undef @res; undef %S; undef %F;
}

sub add_up_card_sel {
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  if ($F{'run_select'}) {
    &s_mes(sprintf "%sは《$c_name[$chudan]》を出した！", "$pn[$u_side]");
    &add_up_card_sub;
    shift @syori;
    $chudan_flg = "";
    #&put_battle_zone_koka($chudan, $fno);
  } else {
    &e_mes("カードの移動をキャンセルしました", $u_side);
    if ($S{'p'} eq "tri") {
      &pursue;
      &breaker;
    } elsif ($S{'a'} =~ /^fld/) {
      ($fldno = $S{'a'}) =~ s/fld//;
      $fld[$fldno] = $chudan;
    } elsif ($S{'a'} =~ /^shinka/) {
      ($ssel = $S{'a'}) =~ s/shinka//;
      ($fldno, $sno) = split /-/, $ssel;
      my @evo = split /-/, $shinka[$fldno];
      $evo[$sno] = $chudan;
      $shinka[$fldno] = join "-", @evo;
    } else {
      local *arr = $S{'a'} eq "0" ? *hand : $S{'a'} eq "1" ? *boti : *deck;
      unshift @{$arr[$u_side]}, $chudan;
    }
    shift @syori;
    $chudan = $chudan_flg = "";
  }
  undef @res; undef %S; undef %F;
}

sub c_shinka_sel {
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  if ($F{'run_select'}) {
    my @evo = grep /^gsel|^csel/, keys(%F);
    &com_error("進化させるクロスギアが指定されていません") if $#evo < 0;
    my $gsel = substr $evo[0], 4;
    my ($side, $gno) = split /-/, $gsel;
    if ($evo[0] =~ /^gsel/) {
      $gear[$side][$gno] .= ":$chudan";
    } else {
      my @cloth = split /_/, $f_cloth[$side];
      $cloth[$gno] .= ":$chudan";
      $f_cloth[$side] = join "_", @cloth;
      &which_side($side);
    }
    &s_mes("シールド・トリガー、超動！") if $S{'p'} eq "tri";
    &s_mes("進化クロスギア！　《$c_name[$chudan]》発動！");
  } else {
    if ($S{'p'} eq "tri") {
      &pursue;
      &breaker;
    } else {
      &e_mes("進化をキャンセルしました", $u_side);
      local *arr = $S{'a'} == 0 ? *hand : $S{'a'} == 1 ? *boti : *deck;
      unshift @{$arr[$u_side]}, $chudan;
    }
  }
  shift @syori;
  unshift @syori, "s-$btl[1]<>t-シールド・トリガーの処理を終了しますか？<>m-trigger_sel3<>o-終了する" if $S{'p'} eq "tri";
  undef @res; undef %F; undef %S;
  $chudan = $chudan_flg = $trigger_flg = "";
}

sub vor_sel1 {
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    &vor_sub1;
    &syori_p_set;
    $syori[0] = sprintf "s-$u_side<>t-%s体目のクリーチャーを選んでください<>m-%s%s<>a-$S{'a'}<>o-決定::やめる",
      $vor_cnt == 2 ? "三" : "二",
      12 <= $c_evo[$chudan] ? "b_vor_sel" : "vor_sel",
      ($c_evo[$chudan] == 4 || $c_evo[$chudan] == 10 || $c_evo[$chudan] == 13) && $vor_cnt == 1 ? "" : 2;
  } else {
    &vor_cancel;
  }
}

sub vor_sel2 {
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    if (12 <= $c_evo[$chudan]) { &boti_vor_sub2; } elsif (9 <= $c_evo[$chudan]) { &mana_vor_sub2; } else { &vor_sub2; }
    &s_mes(sprintf "超進化！　$pn[$u_side]の%s《$c_name[$chudan]》光臨！", ($c_evo[$chudan] == 4 || $c_evo[$chudan] == 10 || $c_evo[$chudan] == 13) ? "ギャラクシー・ボルテックス" : "ボルテックスクリーチャー");
    @res = @vor = (); $chudan = $chudan_flg = $vor_cnt = "";
    &syori_clr;
  } else {
    &vor_cancel;
  }
}

sub vor_sub1 {
  &com_error(sprintf "%d体目のクリーチャーが指定されていません", $vor_cnt + 1) if $F{'select'} eq "";
  push @vor, $F{'select'};
  $vor_cnt++;
  @res = grep $_ ne $F{'select'}, @res;
  if ($c_evo[$chudan] == 5) {
    my $evo = &syu_chk($fld[$vor[2]], $vor[0]) ? $vor[1] : $vor[0];
    @res = grep &syu_chk($fld[$_], $evo) || $c_name[$fld[$_]] =~ /無垢|無頼剣兵ドラグイノセント/ || ($c_name[$fld[$_]] eq "式神イノセント" && 6 < &morph_chk($u_side)) || &cloth_chk($_, 1302), @res;
  }
}

sub vor_sub2 {
  &com_error(sprintf "%s体目のクリーチャーが指定されていません", $vor_cnt == 2 ? "三" : "二") if $F{'select'} eq "";
  my $fldno = $c_evo[$chudan] == 4 ? $vor[-2] : $vor[-1];
  my $fno = $F{'select'};
  my $cno = $fld[$fno];
  $shinka[$fldno] .= $shinka[$fldno] ne "" ? "-$fld[$fldno]" : $fld[$fldno];
  if ($c_evo[$chudan] == 4) {
    $shinka[$fldno] .= "-$shinka[$vor[-1]]" if $shinka[$vor[-1]] ne "";
    $shinka[$fldno] .= "-$fld[$vor[-1]]";
    $f_cloth[$fldno] .= "_$f_cloth[$vor[-1]]" if $f_cloth[$vor[-1]] ne "";
  }
  $shinka[$fldno] .= "-$shinka[$fno]" if $shinka[$fno] ne "";
  $shinka[$fldno] .= "-$cno";
  $f_cloth[$fldno] .= "_$f_cloth[$fno]" if $f_cloth[$fno] ne "";
  $f_tap[$fldno] = ($f_tap[$fldno] eq "1" || $f_tap[$fno] eq "1" || $f_tap[$vor[-1]] eq "1") ? "1" : "";
  $fld[$fldno] = $fld[$fno] = $f_block[$fldno] = $f_block[$fno] = $f_drunk[$fldno] = $f_drunk[$fno] = $shinka[$fno] = $f_cloth[$fno] = $f_tap[$fno] = "";
  $fld[$vor[-1]] = $f_block[$vor[-1]] = $f_drunk[$vor[-1]] = $f_cloth[$vor[-1]] = $f_tap[$vor[-1]] = $shinka[$vor[-1]] = "" if $c_evo[$chudan] == 4;
  $fld[$fldno] = $chudan;
  &set_block($fno, $chudan);
}

sub mana_vor_sub2 {
  &com_error("2体目のクリーチャーが指定されていません") if $F{'select'} eq "";
  my $m_evo = "";
  if ($c_evo[$chudan] == 10) {
    for my $i (-2..-1) {
      $fldno = $vor[$i];
      &pick_card2;
      $m_evo .= $m_evo eq "" ? "$cardno" : "-$cardno";
    }
  } else {
    $fldno = $vor[-1];
    &pick_card2;
    $m_evo .= $m_evo eq "" ? "$cardno" : "-$cardno";
  }
  $fldno = $F{'select'};
  &pick_card2;
  $m_evo .= $m_evo eq "" ? "$cardno" : "-$cardno";
  &fld_chk($l_side);
  my $fno = $nf0;
  $shinka[$fno] = $m_evo;
  $fld[$fno] = $chudan;
  &set_block($fno, $chudan);
}

# 墓地進化ボルテックス処理
sub boti_vor_sub2 {
  &com_error("2体目のクリーチャーが指定されていません") if $F{'select'} eq "";
  my $m_evo = "";
  if ($c_evo[$chudan] == 13) {
    for my $i (-2..-1) {
      $fldno = $vor[$i];
      &pick_card4;
      $m_evo .= $m_evo eq "" ? "$cardno" : "-$cardno";
    }
  } else {
    $fldno = $vor[-1];
    &pick_card4;
    $m_evo .= $m_evo eq "" ? "$cardno" : "-$cardno";
  }
  $fldno = $F{'select'};
  &pick_card4;
  $m_evo .= $m_evo eq "" ? "$cardno" : "-$cardno";
  &fld_chk($l_side);
  my $fno = $nf0;
  $shinka[$fno] = $m_evo;
  $fld[$fno] = $chudan;
  &set_block($fno, $chudan);
}

sub vor_cancel {
  &syori_p_set;
  &e_mes("ボルテックス進化をキャンセルしました", $u_side);
  local *arr = $S{'a'} == 0 ? *hand : $S{'a'} == 1 ? *boti : *deck;
  unshift @{$arr[$u_side]}, $chudan;
  shift @syori; undef @vor; undef @res;
  $chudan = $chudan_flg = $vor_cnt = "";
}

sub glink_sel { # 通常のゴッドリンク
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    &com_error("Ｇ・リンクするクリーチャーが指定されていません") if $F{'select'} eq "";
    my $fno = $F{'select'};
    my $god1 = &card_name_sub($fno);
    if ($c_name[$chudan] =~ /天神|海神|黒神|炎神|地神/) {
      if (($c_name[$chudan] eq "黒神ダーク・インドラ" && $fld[$fno] =~ /1966$/ && $fld[$fno] =~ /^1963/)
          || ($c_name[$chudan] eq "炎神フレイム・アゴン" && $fld[$fno] =~ /1962$/ && $fld[$fno] =~ /^1964/)
          || ($c_name[$chudan] eq "地神エメラルド・ファラオ" && $fld[$fno] =~ /1963$/ && $fld[$fno] =~ /^1965/)
          || ($c_name[$chudan] eq "天神シャイン・バルキリー" && $fld[$fno] =~ /1964$/ && $fld[$fno] =~ /^1966/)
          || ($c_name[$chudan] eq "海神ブルー・ポセイドン" && $fld[$fno] =~ /1965$/ && $fld[$fno] =~ /^1962/)) {
        $syori[0] = "s-$u_side<>t-どちら側にリンクしますか？<>m-glink_sel2<>o-左::右<>g-$fno";
        return;
      } else {
        $fld[$fno] =
          (($c_name[$chudan] eq "黒神ダーク・インドラ" && $fld[$fno] =~ /1966$/)
            || ($c_name[$chudan] eq "炎神フレイム・アゴン" && $fld[$fno] =~ /1962$/)
            || ($c_name[$chudan] eq "地神エメラルド・ファラオ" && $fld[$fno] =~ /1963$/)
            || ($c_name[$chudan] eq "天神シャイン・バルキリー" && $fld[$fno] =~ /1964$/)
            || ($c_name[$chudan] eq "海神ブルー・ポセイドン" && $fld[$fno] =~ /1965$/))
          ? $fld[$fno] . '-' . $chudan : $chudan . '-' . $fld[$fno];
      }
    } else {
      my @god = split /-/, $fld[$fno];
      push @god, $chudan;
      @god = sort @god;
      @god = reverse @god if $fld[$fno] == 1713 || $fld[$fno] == 1904;
      $fld[$fno] = join "-", @god;
      &set_block($fno, $chudan);
    }
    $f_drunk[$fno] = "";
    &s_mes("$pn[$u_side]は《$c_name[$chudan]》を$god1にＧ・リンクした。");
    &s_mes(sprintf "神降臨！　%s！", &card_name_sub($fno));
  } else {
    &syori_p_set;
    $cardno = $chudan;
    &s_mes(sprintf "$pn[$u_side]は%sカードをバトルゾーンに出した。", $S{'a'} eq "decktop" ? "山札の" : "");
    &s_mes("$pn[$u_side]は$c_name[$cardno]を召喚！");
    &fld_chk($u_side);
    &put_battle_zone_sub;
  }
  &syori_clr; undef @res;
  $chudan = $chudan_flg = "";
}

sub glink_sel2 {  # 左右両方にゴッドリンク可能な場合
  return if !($F{'run_select'}) && !($F{'not_select'});
  &syori_p_set;
  my $fno = $S{'g'};
  my $god1 = &card_name_sub($fno);
  $fld[$fno] = ($F{'run_select'}) ? $chudan . '-' . $fld[$fno] : $fld[$fno] . '-' . $chudan;
  &s_mes("$pn[$u_side]は《$c_name[$chudan]》を$god1にＧ・リンクした。");
  &s_mes(sprintf "神降臨！　%s！", &card_name_sub($fno));
  &syori_clr;
  undef @res;
  $chudan = $chudan_flg = "";
}

sub set_block {   # ブロッカーフラグを立てる
  my ($fldno, $cardno) = @_;
  &which_side($fldno);
  my $e_side = 3 - $l_side;
  $f_block[$fldno] = &k_chk($cardno, 1)
          || &c_chk("蒼黒の知将ディアブロスト", $e_side)
          || (&c_chk("金色の精霊クロスヘイム") && &k_chk($cardno, 12))
          || (&c_chk("天雷の龍聖ロレンツオ４世") && &syu_chk($cardno, 89))
          || &castle_chk($l_side, 2258) ? "1" : "";
}

sub castle_sel {  # 城
  return if !($F{'run_select'}) && !($F{'not_select'});
  if ($F{'run_select'}) {
    &com_error("シールドを指定してください") if $F{'select'} eq "";
    &syori_p_set;
    my $fno = $F{'select'};
    $f_cloth[$fno] .= $f_cloth[$fno] eq "" ? "$chudan" : "-$chudan";
    &s_mes("城発動！　$pn[$u_side]のシールドを《$c_name[$chudan]》で要塞化！");
  } else {
    &e_mes("シールドの要塞化をキャンセルしました", $u_side);
    if ($S{'p'} eq "tri") {
      &pursue;
      &breaker;
    } else {
      local *arr = $S{'a'} eq "0" ? *hand : $S{'a'} eq "1" ? *boti : *deck;
      unshift @{$arr[$u_side]}, $chudan;
    }
  }
  &syori_clr;
  $chudan = $chudan_flg =  $trigger_flg = "";
}

sub which_side {
  my $fno = $_[0];
  if    ($_[1] eq 'boti') { $l_side = $u_side; $area = ""; }
  elsif (&ex_chk($fno, \@{$fw1[$u_side]}))  { $l_side = $u_side; $area = 0; }
  elsif (&ex_chk($fno, \@{$fw2[$u_side]}))  { $l_side = $u_side; $area = 1; }
  elsif (&ex_chk($fno, \@{$fw3[$u_side]}))  { $l_side = $u_side; $area = 2; }
  elsif (&ex_chk($fno, \@{$fw4[$u_side]}))  { $l_side = $u_side; $area = 3; }
  elsif (&ex_chk($fno, \@{$fw1[$u_side2]})) { $l_side = $u_side2; $area = 0; }
  elsif (&ex_chk($fno, \@{$fw2[$u_side2]})) { $l_side = $u_side2; $area = 1; }
  elsif (&ex_chk($fno, \@{$fw3[$u_side2]})) { $l_side = $u_side2; $area = 2; }
  elsif (&ex_chk($fno, \@{$fw4[$u_side2]})) { $l_side = $u_side2; $area = 3; }
}

sub com_error { # エラーメッセージ
  my $side = $_[1] ? $_[1] : $u_side;
  &regist("", "（$_[0]）", "secret$side");
  &field;
}

sub card_name_sub {
  my @name = map { "《" . $c_name[$_] . "》"; } (split /-/, $fld[$_[0]]);
  push @name, "ボルメテウス・武者・ドラゴン" if &cloth_chk($_[0], 2050) || $c_name[$fld[$_[0]]] eq "ボルメテウス・剣誠・ドラゴン";
  return join "", @name;
}

sub ex_chk {  # 指定番号がリスト内に含まれるか否かのチェック
  my ($ex, $list) = @_;
  undef $read;
  grep vec($read, $_, 1) = 1, @$list;
  return vec($read, $ex, 1);
}

sub s_mes {
  &regist("", "$_[0]", "system");
}

sub e_mes {
  &regist("", "（$_[0]）", "secret$_[1]");
}

sub t_mes {
  &regist("", "$_[0]", "tap");
}

#--------------------------------------------------------

sub view_fldbutton {
# return if $phase =~ /[12]/;
  &syori_p_set;
  if ($v_side == $u_side && &ex_chk($fno, \@{$fw1[$u_side]}) && !($f_tap[$fno]) && $btl[4] eq "anonymous") {
    undef @sstr;
    (($fno == $btl[2] && $btl[7] ne "") ? $sstr[$btl[7]] : &k_chk($fld[$fno], 3) ? $sstr[1] : &k_chk($fld[$fno], 5) ? $sstr[2] : &k_chk($fld[$fno], 7) ? $sstr[4] : $sstr[0]) = " selected";
    printf qq|<input type="radio" name="attack_from" value="$fno"%s><br>\n|, $fno == $btl[2] ? " checked" : "";
    printf qq|<input type="checkbox" name="unblock$fno" value="on"%s>ブロック不可<br>\n|, &k_chk($fld[$fno], 2) ? " checked" : "";
    print <<"EOM";
<select name="double$fno">
  <option value="0"$sstr[0]></option>
  <option value="1"$sstr[1]>Ｗ・ブレイカー</option>
  <option value="2"$sstr[2]>Ｔ・ブレイカー</option>
  <option value="3"$sstr[3]>Ｑ・ブレイカー</option>
  <option value="4"$sstr[4]>クルー・ブレイカー</option>
  <option value="5"$sstr[5]>ワールドブレイカー</option>
</select>
EOM
  } elsif (!($trigger_flg) && 0 < $#btl && $v_side != $u_side) {  # バトル中かつトリガーフラグが立っておらず、相手のフィールド
    printf qq|<input type="%s" name="%s" value="$fno"><br>|,
      (&ex_chk($fno, \@{$fw1[$u_side2]}) && $btl[4] eq "creature") || (&ex_chk($fno, \@{$fw3[$u_side2]}) && $btl[4] eq "player") ? "radio": "checkbox",
      (&ex_chk($fno, \@{$fw1[$u_side2]}) && $btl[4] eq "creature") ? "attack_to" : &ex_chk($fno, \@{$fw3[$u_side2]}) && $btl[4] eq "player" ? "shield" : "fsel$fno";
  } elsif ($S{'m'} eq "castle_trap_sel" && &ex_chk($fno, \@{$fw3[$btl[1]]})) {  # バトル中かつトリガーフラグが立っておらず、相手のフィールド
    print  qq|<input type="radio" name="shield" value="$fno"><br>|;
  } elsif ($S{'m'} eq "cloth_sel2" && &ex_chk($fno, \@{$fw1[$u_side]})) { # クロスするクリーチャーを選択する時
    print  qq|<input type="radio" name="fsel$fno" value="on"><br>|;
  } elsif ($S{'m'} =~ /sforth_sel|castle_sel/ && &ex_chk($fno, \@{$fw3[$u_side]})) {  # シールド・フォースおよび城のシールドを選択する時
    print  qq|<input type="radio" name="select" value="$fno"><br>|;
  } elsif ($fld[$fno] !~ /\-/) {  # シールドもしくはリンクしていないクリーチャー
    printf qq|<div onmouseover="this.style.backgroundColor='yellow'" onmouseout="this.style.backgroundColor=''"><label style="display: block; width:100%;height:100%;"><input type="%s" name="%s" value="$fno"><br></label></div>|,
      $S{'m'} eq "changer_sel1" && $S{'p'} eq "shield" && $v_side == $u_side ? "radio" : "checkbox",
      $S{'m'} eq "changer_sel1" && $S{'p'} eq "shield" && $v_side == $u_side ? "select" : "fsel$fno";
  }
}

1;
