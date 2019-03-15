#!/usr/local/bin/perl

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
  &deckread;
  &pass_chk;
}
&cardread;
&syu_read;
&info_read;
&copy_run if $F{'mode'} eq "deckcopy" && $F{'copy'} ne "";
&cardview if $F{'mode'} eq "cardview";
&deckinv  if $F{'mode'} eq "deckinv";
&deck_chg if $F{'mode'} eq "deck_chg";
&deckmake if $F{'mode'} eq "deckmake";
&decksave if $F{'mode'} eq "decksave";
&del_deck if $F{'mode'} eq "del_deck";
&del_deck2  if $F{'mode'} eq "del_deck2";
&regist   if $F{'mode'} eq "regist";
&pickup;
&cardsort;
&decksort;
&html;

sub deck_chg {
  $P{'usedeck'} = $F{'usedeck'};
  $P{'predeck'} = "" if $dnam[$F{'usedeck'}] ne "記録なし";
  $P{'c_dname'} = $P{'url'} = "";
  $selstr4[$F{'usedeck'}] = " selected";
  &pfl_write($id);
  &deckread;
}

sub decksave {
  &header;
  &j_script;
  print "</head>\n";
  printf qq|<body%s>\n|, $P{'url'} ne "" ? " onload='var newWin = window.open(\"http://www.stannet.ne.jp/fb/dm/$P{'url'}\",\"new\",\"width=700\"); newWin.moveTo(screen.width-700,0);'" : "";
  print <<"EOM";
<div align="center">
<table width="640" border="1" cellspacing="0" cellpadding="10" class="table">
<tr><td>
<p>※以下のデッキをセーブします。デッキに名前をつけてください。<br>
※デッキは$maxdeck個までセーブすることができます。<br>
<font color="red">※既に$maxdeck個セーブされている場合、現在選択中のデッキに新しいデッキが上書きされます。</font></p>
EOM
if($P{'url'} ne ""){
  open(CHD,"deck.dat") || &error("コピーデッキデータの読み込みに失敗しました");
  while(<CHD>){
    chomp($chdst = $_);
    ($c_dname, $tmp, $url) = split(/-/,$chdst);
    last if $url eq $P{'url'};
  }
  close(CHD);
  $site = "http://www.stannet.ne.jp/fb/dm/" . $P{'url'};
  my @c_deck = split(/,/, $tmp);
  printf qq|<p>このデッキはカードキングダム提供の『$P{'c_dname'}』%s。<br>\n|, join(',', sort { $a <=> $b } @deck) eq join(',', sort { $a <=> $b } @c_deck) ? "です" : "から改造が加えてあります";
  print qq|<small>（注：デッキデータは初掲載時のものを使用しており、最新バージョンではありません）</small><br>\n|;
  printf qq|%sデッキの詳細な説明や遊び方が記された記事のページを<br>新しいウィンドウで開きましたので、必ずご一読ください。<br>\n|, join(',', sort { $a <=> $b } @deck) eq join(',', sort { $a <=> $b } @c_deck) ? "" : "ベースとなった";
  print qq|ウィンドウが開かない場合は、こちらのリンクをクリックすれば記事が開きます＞<a href="$site" target="_blank">Link</a></p>\n|;
  print qq|<p>また、<a href="http://www.stannet.ne.jp/fb/dm/" target="_blank">カードキングダムのサイト</a>にはサンプルデッキ以外にも数多くのデッキが掲載されておりますので、<br>よろしければご覧ください。</p>\n|;
}
my $deckname = $dnam[$F{'usedeck'}] if $dnam[$F{'usedeck'}] ne "記録なし";
$deckname = $P{'c_dname'} if $P{'c_dname'} ne "";
  print <<"EOM";
<div align="center">
<form action="deck.cgi" method="post" name="form">
  <input type="hidden" name="id" value="$id">
  <input type="hidden" name="pass" value="$pass">
  <input type="hidden" name="mode"value="regist">
  <input type="text" size="20" name="deckname" value="$deckname">&nbsp;
  <input type="submit" value="決定">&nbsp;
  <input type="reset" value="クリア">
</form>
<br><br>
<table border="1" width="500">
<caption>デッキ内容</caption>
<tr valign="top"><td width="250">
EOM
  my $count = 0;
  foreach my $card(@deck){
    $c_name[$card] = '不明なカード' if($c_name[$card] eq '');
    print qq|<a href="sForm('cardview',$card);">$c_name[$card]</a><br>\n|;
    print qq|</td><td>\n| if $count == 19;
    $count++;
  }
  print <<"EOM";
</tr>
<tr valign="top"><td colspan="2">
サイキック・クリーチャー
</td></tr>
<tr valign="top"><td width="250">
EOM
  my $count = 0;
  foreach my $card(@deckp){
    $c_name[$card] = '不明なカード' if($c_name[$card] eq '');
    print qq|<a href="sForm('cardview',$card);">$c_name[$card]</a><br>\n|;
    print qq|</td><td>\n| if $count == 19;
    $count++;
  }
  print <<"EOM";
</td></tr>
<tr valign="top"><td colspan="2">
GRクリーチャー
</td></tr>
<tr valign="top"><td width="250">
EOM
  my $count = 0;
  foreach my $card(@deckg){
    $c_name[$card] = '不明なカード' if($c_name[$card] eq '');
    print qq|<a href="sForm('cardview',$card);">$c_name[$card]</a><br>\n|;
    print qq|</td><td>\n| if $count == 19;
    $count++;
  }
  print <<"EOM";
</td></tr></table>
<br><br>
<a href="javascript:form.mode.value=''; form.submit();">戻る</a>
</div>
</td></tr>
</table>
  $copyright
EOM
  &footer;
}

sub del_deck  {
  &header;
  &j_script;
  print <<"EOM";
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
  foreach my $card(@deck){
    $c_name[$card] = '不明なカード' if($c_name[$card] eq '');
    print qq|<a href="sForm('cardview',$card);">$c_name[$card]</a><br>\n|;
    print qq|</td><td>\n| if $count == 19;
    $count++;
  }
  print <<"EOM";
</tr>
<tr valign="top"><td colspan="2">
サイキック・クリーチャー
</td></tr>
<tr valign="top"><td width="250">
EOM
  my $count = 0;
  foreach my $card(@deckp){
    $c_name[$card] = '不明なカード' if($c_name[$card] eq '');
    print qq|<a href="sForm('cardview',$card);">$c_name[$card]</a><br>\n|;
    print qq|</td><td>\n| if $count == 19;
    $count++;
  }
  print <<"EOM";
</td></tr></table>
<br><br>
<form action="deck.cgi" method="post" name="form">
  <input type="hidden" name="id" value="$id">
  <input type="hidden" name="pass" value="$pass">
  <input type="hidden" name="mode" value="">
  <input type="submit" value="消去する" onclick="if(window.confirm('デッキを消去しますか？')){ sForm('del_deck2'); }">&nbsp;
</form>
<br><br>
<a href="javascript:form.submit();">戻る</a>
</div>
</td></tr>
</table>
  $copyright
EOM
  &footer;
}

sub regist{
  return unless $id;
  $usedeck = $P{'usedeck'};
  $dcon = join(",",@deck);
  $dconp = join(",",@deckp);
  $dcong = join(",",@deckg);
  delete $P{'predeck'};
  delete $P{'predeckp'};
  delete $P{'predeckg'};
  my $cou = 0;
  $usedeck = 1 if(!$usedeck);
# foreach my $i(1..$maxdeck){
#   unless($P{"deck$i"}){
#     $dnam = ($F{'deckname'}) ? $F{'deckname'} : "デッキ".$i;
#     $dnam[$i] = $dnam;
#     $dcon[$i] = $dcon;
#     $P{"deck$i"} = "$dnam[$i]\-$dcon[$i]";
#     last;
#   }
#   $cou++;
# }
# if($cou == $maxdeck){
    $dnam = ($F{'deckname'}) ? $F{'deckname'} : "デッキ".$usedeck;
    $dnam[$usedeck] = $dnam;
    $dcon[$usedeck] = $dcon;
    $dconp[$usedeck] = $dconp;
    $dcong[$usedeck] = $dcong;
    $P{"deck$usedeck"}="$dnam[$usedeck]\-$dcon[$usedeck]\-$dconp[$usedeck]\-$dcong[$usedeck]";
# }
  $P{'c_dname'} = $P{'url'} = "";
  &pfl_write($id);
}

sub del_deck2 {
  return unless $id;
  $usedeck = $P{'usedeck'};
  delete $P{"deck$usedeck"};
  undef(@deck);
  &pfl_write($id);
  $dnam[$usedeck] = "記録なし";
}

sub deckmake{
  local (%psy_top, %psy_back, %psy_super, %psy_cell);
  eval (join "", (log_read("psychic.txt")));

  if($F{'text'}){
    undef(@deck);
    @tmp = split(/\n/,$F{'text'});
    foreach my $card(@tmp){ $TX{$card}++ if $card; }
    foreach my $i(0..$#c_name){
      if($TX{$c_name[$i]}){
        $TXC{$c_name[$i]} = 1;
        for($j=0;$j<$TX{$c_name[$i]};$j++){ push(@deck,$i); }
      }
    }
    undef(@deckp);
    @tmp = split(/\n/,$F{'textp'});
    foreach my $card(@tmp){ $TX{$card}++ if $card; }
    foreach my $i(0..$#c_name){
      if($TX{$c_name[$i]}){
        $TXC{$c_name[$i]} = 1;
        for($j=0;$j<$TX{$c_name[$i]};$j++){ push(@deckp,$i); }
      }
    }
    undef(@deckg);
    @tmp = split(/\n/,$F{'textg'});
    foreach my $card(@tmp){ $TX{$card}++ if $card; }
    foreach my $i(0..$#c_name){
      if($TX{$c_name[$i]}){
        $TXC{$c_name[$i]} = 1;
        for($j=0;$j<$TX{$c_name[$i]};$j++){ push(@deckg,$i); }
      }
    }
    foreach $key (keys(%TX)){ $overmsg.="<strong>$keyというカードは存在しません</strong><br>\n" unless $TXC{$key}; }
  }

  @deck_new = @deck;
  undef(@deck);
  for($i=$#deck_new;$i>-1;$i--){
    &add_card($deck_new[$i],1) unless $F{'del'.$i};
  }

  @deckp_new = @deckp;
  undef(@deckp);
  for($i=$#deckp_new;$i>-1;$i--){
    &add_card($deckp_new[$i],1) unless $F{'delp'.$i};
  }

  @deckg_new = @deckg;
  undef(@deckg);
  for($i=$#deckg_new;$i>-1;$i--){
    &add_card($deckg_new[$i],1) unless $F{'delg'.$i};
  }

  @mai = grep(/^sel/,keys(%F));
  foreach $cardno(@mai){
    $kaisu = $F{$cardno};
    next if $kaisu =~ /\D/;
    $kaisu = 4 if $kaisu > 4;
    $cardno =~ s/^sel//;
    &add_card($cardno,$kaisu);
  }

  @deck_stack = sort decksort @deck;
  @deck = @deck_stack;
  @deckp_stack = sort decksort @deckp;
  @deckp = @deckp_stack;
  @deckg_stack = sort decksort @deckg;
  @deckg = @deckg_stack;

  &put_ini;
}

sub copy_run {
  open(CHD,"deck.dat") || &error("コピーデッキデータの読み込みに失敗しました");
  my $cou = 1;
  while(<CHD>){
    chomp($chdst = $_);
    last if $cou == $F{'copy'};
    $cou++;
  }
  close(CHD);
  ($c_dname,$tmp,$url,$ptmp) = split(/-/,$chdst);
  @deck = split(/,/,$tmp);
  @deck = sort decksort @deck;
  if (defined($ptmp)) {
    @deckp = split(/,/,$ptmp);
    @deckp = sort decksort @deckp;
  } else {
    @deckp = ();
  }
  #($c_dname,$tmp,$url) = split(/-/,$chdst);
  #@deck = split(/,/,$tmp);
  #@deck = sort decksort @deck;
  #@deckp = ();
  $P{'c_dname'} = $c_dname;
  $P{'url'} = $url;
  &put_ini;
}

# カードを一覧に追加
sub add_card{
  my ($cardno,$kaisu) = @_;

  my($couno);
  if ($psy_super{$cardno}) {
    $couno = $psy_super{$cardno};
  } elsif ($psy_back{$cardno}) {
    $couno = [ $psy_back{$cardno} ];
  } else {
    $couno = [ $cardno ];
  }

  foreach my $cardnum (@$couno) {
    for(1 .. $kaisu){
      if($card_cou[$cardnum] < 4){
         if (syu_chk($cardnum, 145) || syu_chk($cardnum, 150) || syu_chk($cardnum, 103) || syu_chk($cardnum, 119) || syu_chk($cardnum, 151) || syu_chk($cardnum, 185) || syu_chk($cardnum, 186)) {
          # サイキックの場合
          unshift(@deckp,$cardnum);
        } elsif (syu_chk($cardnum, 222)) {
          if($card_cou[$cardnum] < 2){
            # GRの場合
            unshift(@deckg,$cardnum);
          } else {
            $overmsg .= "<strong>GRゾーンに入れられるカードは１種類2枚までです</strong><br>\n";
          }
        } else {
          # 通常
          unshift(@deck,$cardnum);
        }
        $card_cou[$cardnum]++;
      } else {
        $overmsg .= "<strong>デッキに入れられるカードは１種類４枚までです</strong><br>\n";
      }
    }
  }
}

sub pickup{
  $F{'series'} = 0 unless $F{'series'};
  $F{'kind'} = 0 unless $F{'kind'};
  if($F{'sstr'} || $F{'sstr2'}){
    $F{'series'} = 9999;
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
  } elsif ($F{'series'} ne "9999") {
    @disp = @{$ser[$F{'series'}]};
  } else {
    foreach my $i(0 .. $#c_name){
      $disp[$i] = $i if $c_name[$i] ne "";
    }
  }
  @d_tmp = ();
  if($F{'kind'} != 0){
    foreach my $i(@disp){
      $c_kind = (&syu_chk($i, 96)) ? 3 : (&syu_chk($i, 1)) ? 2 : (&syu_chk($i, 0)) ? 1 : 0;
      if ($F{'kind'} == 1){ push(@d_tmp,$i) if !($c_kind); }
      elsif ($F{'kind'} == 2){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 0); }
      elsif ($F{'kind'} == 3){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 1); }
      elsif ($F{'kind'} == 4){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 2); }
      elsif ($F{'kind'} == 5){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 3); }
      elsif ($F{'kind'} == 6){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 4); }
      elsif ($F{'kind'} == 28){ push(@d_tmp,$i) if (!($c_kind) && $c_bun[$i] == 5); }
      elsif ($F{'kind'} == 7){ push(@d_tmp,$i) if (!($c_kind) && &k_chk($i,12)); }
      elsif ($F{'kind'} == 8){ push(@d_tmp,$i) if $c_kind == 1; }
      elsif ($F{'kind'} == 9){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 0; }
      elsif ($F{'kind'} == 10){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 1; }
      elsif ($F{'kind'} == 11){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 2; }
      elsif ($F{'kind'} == 12){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 3; }
      elsif ($F{'kind'} == 13){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 4; }
      elsif ($F{'kind'} == 29){ push(@d_tmp,$i) if $c_kind == 1 && $c_bun[$i] == 5; }
      elsif ($F{'kind'} == 14){ push(@d_tmp,$i) if $c_kind == 1 && &k_chk($i,12); }
      elsif ($F{'kind'} == 15){ push(@d_tmp,$i) if $c_kind == 2; }
      elsif ($F{'kind'} == 16){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 0; }
      elsif ($F{'kind'} == 17){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 1; }
      elsif ($F{'kind'} == 18){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 2; }
      elsif ($F{'kind'} == 19){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 3; }
      elsif ($F{'kind'} == 20){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 4; }
      elsif ($F{'kind'} == 30){ push(@d_tmp,$i) if $c_kind == 2 && $c_bun[$i] == 5; }
      elsif ($F{'kind'} == 21){ push(@d_tmp,$i) if $c_kind == 2 && &k_chk($i,12); }
      elsif ($F{'kind'} == 22) { push @d_tmp, $i if $c_kind == 3; }
      elsif ($F{'kind'} == 23) { push @d_tmp, $i if $c_kind == 3 && $c_bun[$i] == 0; }
      elsif ($F{'kind'} == 24) { push @d_tmp, $i if $c_kind == 3 && $c_bun[$i] == 1; }
      elsif ($F{'kind'} == 25) { push @d_tmp, $i if $c_kind == 3 && $c_bun[$i] == 2; }
      elsif ($F{'kind'} == 26) { push @d_tmp, $i if $c_kind == 3 && $c_bun[$i] == 3; }
      elsif ($F{'kind'} == 27) { push @d_tmp, $i if $c_kind == 3 && $c_bun[$i] == 4; }
      elsif ($F{'kind'} == 31) { push @d_tmp, $i if $c_kind == 3 && $c_bun[$i] == 5; }
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
      elsif ($F{'skill'} == 30) { push @d_tmp, $i if &k_chk($i, 32); }
    }
    @disp = @d_tmp;
  }
  $selstr[$F{'series'}] = $selstr2[$F{'kind'}] = $selstr3[$F{'skill'}] = $selstr4[$P{'usedeck'}] = " selected";
}

sub html{
  if($copy){
    open(IN,"deck.dat") || &error("コピーデッキデータの読み込みに失敗しました");
    @data = <IN>;
    close(IN);
  }
  &header;
  &j_script;
  $viewst = $F{'view'} ? qq|<a href="javascript:deckV();">通常表示</a>| : qq|<a href="javascript:deckV('text');">テキスト表示</a>|;
  print <<"EOM";
<script type="text/javascript"><!--
function chkCB(){
  with(document.form){
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


	function chkCBp() {
		with (document.form) {
			if (allchkp.checked == true) {
				for (i = 0; i < elements.length; i++) {
					if (elements["delp" + i]) {
						elements["delp" + i].checked = true;
					}
				}
			} else if (allchkp.checked == false) {
				for (i = 0; i < elements.length; i++) {
					if (elements["delp" + i]) {
						elements["delp" + i].checked = false;
					}
				}
			}
		}
	}

  function chkCBg() {
    with (document.form) {
      if (allchkg.checked == true) {
        for (i = 0; i < elements.length; i++) {
          if (elements["delg" + i]) {
            elements["delg" + i].checked = true;
          }
        }
      } else if (allchkg.checked == false) {
        for (i = 0; i < elements.length; i++) {
          if (elements["delg" + i]) {
            elements["delg" + i].checked = false;
          }
        }
      }
    }
  }

	function deckV(t) {
		document.view.view.value = t;
		document.view.submit();
	}
// -->
</script>
</head>
<body>
<div align="center">
  $overmsg
  <form name="view" action="deck.cgi" method="get">
    <input type="hidden" name="id" value="$id">
    <input type="hidden" name="pass" value="$pass">
    <input type="hidden" name="view" value="">
  </form>
  <form name="form" action="deck.cgi" method="post">
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
        <option value="9999"selected$selstr[9999]>全種</option>

        <optgroup label = "基本編">
            <option value="109" $selstr[109]>第１弾</option>
            <option value="1" $selstr[1]>第２弾</option>
            <option value="2" $selstr[2]>第３弾</option>
            <option value="3" $selstr[3]>第４弾</option>
            <option value="4" $selstr[4]>第５弾</option>
        <optgroup label = "闘魂編">
            <option value="5" $selstr[5]>第１弾</option>
            <option value="6" $selstr[6]>第２弾</option>
            <option value="7" $selstr[7]>第３弾</option>
            <option value="8" $selstr[8]>第４弾</option>
        <optgroup label = "聖拳編">
            <option value="9" $selstr[9]>第１弾</option>
            <option value="10" $selstr[10]>第２弾</option>
            <option value="11" $selstr[11]>第３弾</option>
            <option value="12" $selstr[12]>第４弾</option>
        <optgroup label = "転生編">
            <option value="13" $selstr[13]>第１弾</option>
            <option value="14" $selstr[14]>第２弾</option>
            <option value="15" $selstr[15]>第３弾</option>
            <option value="16" $selstr[16]>第４弾</option>
        <optgroup label = "不死鳥編">
            <option value="18" $selstr[18]>第１弾</option>
            <option value="19" $selstr[19]>第２弾</option>
            <option value="20" $selstr[20]>第３弾</option>
            <option value="21" $selstr[21]>第４弾</option>
            <option value="22" $selstr[22]>第５弾</option>
        <optgroup label = "極神編">
            <option value="23" $selstr[23]>第１弾</option>
            <option value="24" $selstr[24]>第２弾</option>
            <option value="25" $selstr[25]>第３弾</option>
            <option value="26" $selstr[26]>第４弾</option>
        <optgroup label = "戦国編">
            <option value="27" $selstr[27]>第１弾</option>
            <option value="28" $selstr[28]>第２弾</option>
            <option value="29" $selstr[29]>第３弾</option>
            <option value="30" $selstr[30]>第４弾</option>
        <optgroup label = "神化編">
            <option value="31" $selstr[31]>第１弾</option>
            <option value="35" $selstr[35]>第２弾</option>
            <option value="36" $selstr[36]>第４弾</option>
            <option value="38" $selstr[38]>第３弾</option>
        <optgroup label = "覚醒編">
            <option value="45" $selstr[45]>第１弾</option>
            <option value="46" $selstr[46]>第２弾</option>
            <option value="47" $selstr[47]>第３弾</option>
            <option value="48" $selstr[48]>第４弾</option>
        <optgroup label = "エピソード１">
            <option value="42" $selstr[42]>ファースト・コンタクト</option>
            <option value="43" $selstr[43]>ダークサイド</option>
            <option value="44" $selstr[44]>ガイアール・ビクトリー</option>
            <option value="49" $selstr[49]>ライジング・ホープ</option>
        <optgroup label = "エピソード2">
            <option value="32" $selstr[32]>ホワイト・ゼニス・パック</option>
            <option value="33" $selstr[33]>ブラック・ボックス・パック</option>
            <option value="34" $selstr[34]>グレイト・ミラクル</option>
            <option value="37" $selstr[37]>ゴールデン・エイジ</option>
            <option value="39" $selstr[39]>ビクトリー・ラッシュ</option>
            <option value="40" $selstr[40]>ゴールデン・ドラゴン</option>
            <option value="41" $selstr[41]>大決戦オールスター１２</option>
            <option value="79" $selstr[79]>激熱！ガチンコBEST</option>
            <option value="80" $selstr[80]></option>
        <optgroup label = "エピソード３">
            <option value="70" $selstr[70]>レイジＶＳゴッド</option>
            <option value="81" $selstr[81]>最強戦略パーフェクト12</option>
            <option value="95" $selstr[95]>デッド&ビート</option>
            <option value="98" $selstr[98]>ウルトラＶマスター</option>
            <option value="102" $selstr[102]>オメガ∞マックス</option>
        <optgroup label = "ドラゴン・サーガ">
            <option value="108" $selstr[108]>龍解ガイギンガ</option>
            <option value="111" $selstr[111]>暴龍ガイグレン</option>
            <option value="112" $selstr[112]>双剣オウギンガ</option>
            <option value="113" $selstr[113]>超戦ガイネクスト×極</option>
            <option value="114" $selstr[114]>超戦ガイネクスト×真</option>
            <option value="122" $selstr[122]>龍の祭典！魂ドラゴンフェス！！</option>
        <optgroup label = "革命編">
            <option value="115" $selstr[115]>燃えろドギラゴン!!</option>
            <option value="116" $selstr[116]>時よ止まれミラダンテ!!</option>
            <option value="117" $selstr[117]>禁断のドキンダムX</option>
            <option value="118" $selstr[118]>正体判明のギュウジン丸!!</option>
        <optgroup label = "革命ファイナル">
            <option value="119" $selstr[119]>ハムカツ団とドギラゴン剣</option>
            <option value="120" $selstr[120]>世界は0だ!! ブラックアウト!!</option>
            <option value="121" $selstr[121]>ドギラゴールデンvsドルマゲドンX</option>
            <option value="123" $selstr[123]>ファイナル・メモリアル・パック ~E1・E2・E3編~</option>
            <option value="124" $selstr[124]>ファイナル・メモリアル・パック ~DS・Rev・RevF編~</option>
        <optgroup label = "デュエル・マスターズ">
            <option value="132" $selstr[132]>クロニクル・レガシー・デッキ 風雲!!怒流牙忍法帖</option>
            <option value="126" $selstr[126]>Newヒーローデッキ ジョーのジョーカーズ</option>
            <option value="127" $selstr[127]>Newヒーローデッキ キラのラビリンス</option>
            <option value="128" $selstr[128]>Newヒーローデッキ ボルツのB・A・D</option>
            <option value="136" $selstr[136]>超メガ盛りプレミアム7デッキ　キラめけ正義！！DG超動</option>
            <option value="130" $selstr[130]>ステキ！カンペキ！！ ジョーデッキーBOX</option>
            <option value="131" $selstr[131]>クロニクル・レガシー・デッキ アルカディアス鎮魂歌</option>
            <option value="135" $selstr[135]>超メガ盛りプレミアム7デッキ　集結！！炎のJ･O･Eカーズ</option>
            <option value="134" $selstr[134]>ゴールデン・ベスト</option>
            <option value="125" $selstr[125]>新1弾 ジョーカーズ参上！！</option>
            <option value="129" $selstr[129]>新2弾 マジでB・A・Dなラビリンス！！</option>
            <option value="133" $selstr[133]>新3弾 気分 JOE×2 メラ冒険↑↑</option>
            <option value="137" $selstr[137]>新4弾 誕ジョー↑マスター・ドラゴン↑↑ ～正義ノ裁キ～</option>
            <option value="138" $selstr[138]>新4弾 誕ジョー↑ マスター・ドルスザク↑↑ ～無月の魔凰～</option>
        <optgroup label = "双極篇">
            <option value="139" $selstr[139]>ジョーカーズ・弾銃炸裂・スタートデッキ</option>
            <option value="140" $selstr[140]>オウ禍武斗・マッハ炸裂・スタートデッキ</option>
            <option value="142" $selstr[142]>ドルスザク・無月炸裂・スタートデッキ</option>
            <option value="147" $selstr[147]>煌世の剣・Z炸裂・スタートデッキ</option>
            <option value="145" $selstr[145]>クロニクル・レガシー・デッキ2018 究極のバルガ龍幻郷</option>
            <option value="146" $selstr[146]>クロニクル・レガシー・デッキ2018 至高のゼニス頂神殿</option>
            <option value="154" $selstr[154]>超誕!!ツインヒーローデッキ80 聖剣神話†カリバーサーガ</option>
            <option value="153" $selstr[153]>超誕!!ツインヒーローデッキ80 Jの超機兵ジョーカーズデラックス</option>
            <option value="152" $selstr[152]>超誕!!ツインヒーローデッキ80 卍獄の虚無月ムーンレスムーン</option>
            <option value="151" $selstr[151]>超誕!!ツインヒーローデッキ80 自然大暴走ファイナルハザード </option>
            <option value="141" $selstr[141]>第1弾　豪快！！ジョラゴンGoFight！！</option>
            <option value="143" $selstr[143]>第2弾　逆襲のギャラクシー 卍・獄・殺！！</option>
            <option value="148" $selstr[148]>第3弾 †ギラギラ†煌世主と終葬のＱＸ！！</option>
            <option value="155" $selstr[155]>第4弾 超決戦!バラギアラ!!無敵オラオラ輪廻∞</option>
            <option value="144" $selstr[144]>デュエマクエスト・パック～伝説の最強戦略12～</option>
            <option value="150" $selstr[150]>ペリッ！！スペシャルだらけのミステリーパック</option>
            <option value="156" $selstr[156]>夢の最＆強!!ツインパクト超No.1パック</option>
        <optgroup label = "超天篇">
            <option value="158" $selstr[158]>超GRスタートデッキ ジョーのガチャメカ・ワンダフォー</option>
            <option value="159" $selstr[159]>超GRスタートデッキ キャップのオレガ・オーラ・デリート</option>
            <option value="157" $selstr[157]>第1弾 新世界ガチ誕!! 超GRとオレガ・オーラ!!</option>
        <optgroup label = "デッキビルダー">
            <option value="88" $selstr[88]>デッキビルダーDX　ハンター・エディション</option>
            <option value="89" $selstr[89]>デッキビルダーDX　エイリアンエディション</option>
            <option value="90" $selstr[90]>デッキビルダー鬼DX　ガンバ！勝太編</option>
            <option value="91" $selstr[91]>デッキビルダー鬼DX　キラリ！レオ編</option>
        <optgroup label = "フルホイルパック">
            <option value="73" $selstr[73]>リバイバル・ヒーロー　ザ・ハンター</option>
            <option value="74" $selstr[74]>リバイバル・ヒーロー　ザ・エイリアン</option>
            <option value="97" $selstr[97]>仁義なきロワイヤル</option>
        <optgroup label = "超王道戦略ファンタジスタ12">
            <option value="107" $selstr[107]>ドラゴン・サーガ　超王道戦略ファンタジスタ12</option>
        <optgroup label = "ヒーローズ・ビクトリー・パック">
            <option value="75" $selstr[75]>大乱闘！ヒーローズ・ビクトリー・パック　燃えるド根性大作戦</option>
            <option value="76" $selstr[76]>大乱闘！ヒーローズ・ビクトリー・パック　咆えろ野生の大作戦</option>
        <optgroup label = "ドラマティック・ウォーズ">
            <option value="77" $selstr[77]> ドラゴン＆ファイアー</option>
            <option value="78" $selstr[78]>エンジェル＆デーモン</option>
        <optgroup label = "ビギニング・ドラゴン・デッキ">
            <option value="103" $selstr[103]>熱血の戦闘龍</option>
            <option value="104" $selstr[104]>正義の天聖龍</option>
            <option value="105" $selstr[105]>神秘の結晶龍</option>
        <optgroup label = "デッキ収録カード（再録なし）">
            <option value="55" $selstr[55]>スーパーデッキ ゼロ</option>
            <option value="83" $selstr[83]>スタートダッシュ　火＆自然編</option>
            <option value="84" $selstr[84]>スタートダッシュスタートダッシュ　水＆闇編</option>
            <option value="85" $selstr[85]>炎のキズナXX</option>
            <option value="86" $selstr[86]>ストロング・メタル　爆裂ダッシュ</option>
            <option value="87" $selstr[87]>ストロング・メタル　最強国技</option>
            <option value="92" $selstr[92]>禁断の変形デッキ オラクルの書</option>
            <option value="93" $selstr[93]>禁断の変形デッキ アウトレイジの書</option>
            <option value="96" $selstr[96]>スーパーデッキMAX「カツキングと伝説の秘宝」 </option>
            <option value="100" $selstr[100]>スーパーデッキOMG「逆襲のイズモと聖邪神の秘宝」</option>
            <option value="67" $selstr[67]>ザ・ゴッド・キングダム</option>
            <option value="66" $selstr[66]>マッド・ロック・チェスター</option>
            <option value="56" $selstr[56]>スーパーデッキ クロス</option>
            <option value="58" $selstr[58]>変形デッキセット　DX鬼ドラゴン</option>
            <option value="59" $selstr[59]>変形デッキセット　DX鬼エンジェル</option>
            <option value="60" $selstr[60]>ライジング・ダッシュデッキ　反撃ブロック！</option>
            <option value="61" $selstr[61]>エントリーパック・ゼロ　パーフェクト・エンジェル</option>
            <option value="62" $selstr[62]>1stデッキ　アウトレイジ・ダッシュ</option>
            <option value="63" $selstr[63]>1stデッキ　オラクル・ダッシュ</option>
            <option value="64" $selstr[64]>ルナティック・ゴッド</option>
            <option value="65" $selstr[65]>ウルトラ・NEX</option>
            <option value="101" $selstr[101]>ザ・サムライ・レジェンド</option>
        <optgroup label = "再録パック">
            <option value="17" $selstr[17]>ベストチャレンジャー</option>
            <option value="51" $selstr[51]>双龍パック</option>
            <option value="52" $selstr[52]>コロコロドリーム</option>
            <option value="53" $selstr[53]>コロコロドリーム2</option>
            <option value="54" $selstr[54]>コロコロドリーム3</option>
            <option value="57" $selstr[57]>ヒーローズクロス</option>
            <option value="106" $selstr[106]>キング・オブ・デュエルロード ストロング7</option>
        <optgroup label = "特別なカード">
            <option value="71" $selstr[71]>推進会拡張パック第一弾</option>
            <option value="72" $selstr[72]>大会優勝者用オリジナルカード</option>
            <option value="82" $selstr[82]>プロモーションカード2013</option>
            <option value="94" $selstr[94]>アゲアゲVS(アゲインスト)パック</option>
            <option value="99" $selstr[99]>プロモーションカード2014</option>
        <optgroup label = "CGI限定オリジナルカード">
            <option value="149" $selstr[149]>2018年　オリカ募集　推進パック第４弾</option>

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
        <option value="28"$selstr2[6]>ゼロ</option>
        <option value="7"$selstr2[7]>レインボー</option>
      </optgroup>
      <optgroup label="呪文">
        <option value="8"$selstr2[8]>全文明</option>
        <option value="9"$selstr2[9]>光</option>
        <option value="10"$selstr2[10]>水</option>
        <option value="11"$selstr2[11]>闇</option>
        <option value="12"$selstr2[12]>火</option>
        <option value="13"$selstr2[13]>自然</option>
        <option value="29"$selstr2[13]>ゼロ</option>
        <option value="14"$selstr2[14]>レインボー</option>
      </optgroup>
      <optgroup label="クロスギア">
        <option value="15"$selstr2[15]>全文明</option>
        <option value="16"$selstr2[16]>光</option>
        <option value="17"$selstr2[17]>水</option>
        <option value="18"$selstr2[18]>闇</option>
        <option value="19"$selstr2[19]>火</option>
        <option value="20"$selstr2[20]>自然</option>
        <option value="30"$selstr2[20]>ゼロ</option>
        <option value="21"$selstr2[21]>レインボー</option>
      </optgroup>
      <optgroup label="城">
        <option value="22"$selstr2[22]>全文明</option>
        <option value="23"$selstr2[23]>光</option>
        <option value="24"$selstr2[24]>水</option>
        <option value="25"$selstr2[25]>闇</option>
        <option value="26"$selstr2[26]>火</option>
        <option value="27"$selstr2[27]>自然</option>
        <option value="31"$selstr2[27]>ゼロ</option>
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
      <option value="30"$selstr3[30]>Ｑ・ブレイカー</option>
    </select><br>
    カード名検索：<input type="text" name="sstr" size="24" value="$F{'sstr'}">&nbsp;&nbsp;
    種族名検索：<input type="text" name="sstr2" size="24" value="$F{'sstr2'}">&nbsp;&nbsp;
    <input type="button" value="検索" onclick="sForm();">
  </p>
  <table border="4" cellpadding="5" class="table"><tr valign="top">
    <td colspan="2" align="center">
      <!--<p><a href="javascript:sForm('deckinv');">デッキ調査</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="./etc/help.html#deck" target="_blank">説明</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('taisen');">対戦する</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('group');">グループ編集</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('list');">リスト編集</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('log');">過去ログ</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:sForm('nuisance');">迷惑行為</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="index.cgi">戻る</a>&nbsp;&nbsp;&nbsp;&nbsp;$viewst-->

	<div class="paging centered" style="padding-bottom: 5px;">
	<ul>
	<li><a href="javascript:sForm('deckinv');">デッキ調査</a></li>
	<li><a href="./etc/help.html#deck" target="_blank">説明</a></li>
	<li><a href="javascript:sForm('taisen');">対戦する</a></li>
	<li><a href="javascript:sForm('group');">グループ編集</a></li>
	<li><a href="javascript:sForm('list');">リスト編集</a></li>
	<li><a href="javascript:sForm('log');">過去ログ</a></li>
	<li><a href="javascript:sForm('nuisance');">迷惑行為</a></li>
	<li>$viewst</li>
	</ul>
	</div>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <select name="usedeck">
EOM
  map { print qq|<option value="$_"$selstr4[$_]>$dnam[$_]</option>\n| } (1..$maxdeck);
  print <<"EOM";
      </select>
&nbsp;<input type="button" value="デッキ選択" onclick="sForm('deck_chg');"></p>
<p>
<input type="button" value="デッキ組替" onclick="sForm('deckmake');">&nbsp;&nbsp;&nbsp;&nbsp;
<input type="button" value="デッキセーブ" onclick="sForm('decksave');">&nbsp;&nbsp;&nbsp;&nbsp;
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
    print qq|<input type="button" value="コピー" onclick="sForm('deckcopy');">\n|;
   }
  print <<"EOM";
&nbsp;&nbsp;&nbsp;&nbsp;<input type="button" value="デッキ消去" onclick="sForm('del_deck');">
</p>
</td></tr>
  <tr valign="top">
  <td width="400">
EOM
  print qq|<input type="hidden" name="view" value="text">| if $F{'view'} eq "text";
  &view_list(0) if @sort_res1 > 0;
  &view_list(1) if @sort_res2 > 0;
  &view_list(2) if @sort_res3 > 0;
  &view_list(3) if @sort_res4 > 0;
  &view_list(4) if @sort_res5 > 0;
  print "　</td><td>\n";
  if(@deck == 0){ @main_deck = @main_num = (); $deckcou = 0; }
  else{
    $count = 0;
    foreach $card(@deck){
      push(@main_deck,$card);
      push(@main_num,$count);
      $count++;
    }
    $deckcou = $#main_deck+1;
  }
  if ($F{'view'} eq "text"){ &deckview_text; } else { &deckview; }
  print "<hr />サイキック・クリーチャー<br />";
  if(@deckp == 0){ @main_deck_psychic = @mainp_num = (); $deckpcou = 0; }
  else{
    $countp = 0;
    foreach $card(@deckp){
      push(@main_deck_psychic,$card);
      push(@mainp_num,$countp);
      $countp++;
    }
    $deckpcou = $#main_deck_psychic+1;
  }
  if ($F{'view'} eq "text"){ &deckpview_text; } else { &deckpview; }
  print "<hr />GRクリーチャー<br />";
  if(@deckg == 0){ @main_deck_gr = @maing_num = (); $deckgcou = 0; }
  else{
    $countg = 0;
    foreach $card(@deckg){
      push(@main_deck_gr,$card);
      push(@maing_num,$countg);
      $countg++;
    }
    $deckgcou = $#main_deck_gr+1;
  }
  if ($F{'view'} eq "text"){ &deckgview_text; } else { &deckgview; }
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
  　<select name="sortkey1">
    <option value="0"$selstr6[0]>文明順</option>
    <option value="1"$selstr6[1]>マナコスト順</option>
    <option value="2"$selstr6[2]>パワー順</option>
    <option value="3"$selstr6[3]>種族順</option>
    <option value="4"$selstr6[4]>名前順</option>
    <option value="5"$selstr6[5]>人気順</option>
  </select>
　<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
    map { &print_card($_) } @sort_res1;
    print "</table>\n";
  } elsif($label == 1) {
    print <<"EOM";
<big>呪文</big>
　<select name="sortkey2">
  <option value="0"$selstr7[0]>文明順</option>
  <option value="1"$selstr7[1]>マナコスト順</option>
  <option value="2"$selstr7[2]>名前順</option>
  <option value="3"$selstr7[3]>人気順</option>
</select>
　<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
    map { &print_card($_) } @sort_res2;
    print "</table>\n";
  } elsif($label == 3) {
    print <<"EOM";
<big>城</big>
　<select name="sortkey2">
  <option value="0"$selstr7[0]>文明順</option>
  <option value="1"$selstr7[1]>マナコスト順</option>
  <option value="2"$selstr7[2]>名前順</option>
  <option value="3"$selstr7[3]>人気順</option>
</select>
　<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
    map { &print_card($_) } @sort_res4;
    print "</table>\n";
  } elsif($label == 4) {
    print <<"EOM";
<big>サイキック・クリーチャー</big>
　<select name="sortkey2">
  <option value="0"$selstr7[0]>文明順</option>
  <option value="1"$selstr7[1]>マナコスト順</option>
  <option value="2"$selstr7[2]>名前順</option>
  <option value="3"$selstr7[3]>人気順</option>
</select>
　<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
    map { &print_card($_) } @sort_res5;
    print "</table>\n";
  } else {
    print <<"EOM";
<big>クロスギア</big>　
<select name="sortkey3">
  <option value="0"$selstr8[0]>文明順</option>
  <option value="1"$selstr8[1]>マナコスト順</option>
  <option value="2"$selstr8[2]>名前順</option>
  <option value="3"$selstr8[3]>人気順</option>
</select>　
<input type="button" value="並び替え" onclick="sForm();">
<br><br>
<table border="0" width="100%">
EOM
    map { &print_card($_) } @sort_res3;
    print "</table>\n";
  }
}

sub deckinv {
  if($#deck == 0){ @main_deck = @main_num = (); $deckcou = 0; }
  else{
    $count = 0;
    foreach(@deck){
      push(@main_deck,$_); push(@main_num,$count);
      $count++;
    }
    $deckcou = $#main_deck+1;
  }
my(@bunmei_c) = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
my(@mana_c) = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
my($creater_c) = 0;
my($shinka_c) = 0;
my($jumon_c) = 0;
my($cross_c) = 0;
  &header;
  print<<"EOM";
</head>
<body>
<div align="center">
  　デッキ枚数　現在$deckcou枚
EOM
  if($deckcou != 0){
    foreach my $i(0 .. $#main_deck){
      if($c_bun[$main_deck[$i]] eq '0') {
        $bunmei_c[0]++;
      } elsif($c_bun[$main_deck[$i]] eq '1') {
        $bunmei_c[1]++;
      } elsif($c_bun[$main_deck[$i]] eq '2') {
        $bunmei_c[2]++;
      } elsif($c_bun[$main_deck[$i]] eq '3') {
        $bunmei_c[3]++;
      } elsif($c_bun[$main_deck[$i]] eq '4') {
        $bunmei_c[4]++;
      } elsif($c_bun[$main_deck[$i]] eq '0,1') {
        $bunmei_c[5]++;
      } elsif($c_bun[$main_deck[$i]] eq '0,2') {
        $bunmei_c[6]++;
      } elsif($c_bun[$main_deck[$i]] eq '3,0') {
        $bunmei_c[7]++;
      } elsif($c_bun[$main_deck[$i]] eq '1,2') {
        $bunmei_c[8]++;
      } elsif($c_bun[$main_deck[$i]] eq '1,3') {
        $bunmei_c[9]++;
      } elsif($c_bun[$main_deck[$i]] eq '4,1') {
        $bunmei_c[10]++;
      } elsif($c_bun[$main_deck[$i]] eq '2,3') {
        $bunmei_c[11]++;
      } elsif($c_bun[$main_deck[$i]] eq '2,4') {
        $bunmei_c[12]++;
      } elsif($c_bun[$main_deck[$i]] eq '3,4') {
        $bunmei_c[13]++;
      } elsif($c_bun[$main_deck[$i]] eq '4,0') {
        $bunmei_c[14]++;
      } elsif($c_bun[$main_deck[$i]] eq '0,1,2') {
        $bunmei_c[15]++;
      } elsif($c_bun[$main_deck[$i]] eq '1,3,0') {
        $bunmei_c[16]++;
      } elsif($c_bun[$main_deck[$i]] eq '4,0,1') {
        $bunmei_c[17]++;
      } elsif($c_bun[$main_deck[$i]] eq '3,0,2') {
        $bunmei_c[18]++;
      } elsif($c_bun[$main_deck[$i]] eq '0,2,4') {
        $bunmei_c[19]++;
      } elsif($c_bun[$main_deck[$i]] eq '3,4,0') {
        $bunmei_c[20]++;
      } elsif($c_bun[$main_deck[$i]] eq '1,2,3') {
        $bunmei_c[21]++;
      } elsif($c_bun[$main_deck[$i]] eq '1,2,4') {
        $bunmei_c[22]++;
      } elsif($c_bun[$main_deck[$i]] eq '4,1,3') {
        $bunmei_c[23]++;
      } elsif($c_bun[$main_deck[$i]] eq '2,3,4') {
        $bunmei_c[24]++;
      } elsif($c_bun[$main_deck[$i]] eq '0,1,2,3,4') {
        $bunmei_c[25]++;
      } elsif($c_bun[$main_deck[$i]] eq '5') {
        $bunmei_c[26]++;
      }



      $mana_c[$c_mana[$main_deck[$i]]]++;
      if(($c_syu[$main_deck[$i]] eq '1') || ($c_syu[$main_deck[$i]] eq '1,88')) {
        $cross_c++;
      } elsif(($c_syu[$main_deck[$i]] eq '0') || ($c_syu[$main_deck[$i]] eq '0,89')) {
        $jumon_c++;
      } elsif(($c_evo[$main_deck[$i]] == 1) || ($c_evo[$main_deck[$i]] == 3) || ($c_evo[$main_deck[$i]] == 4) || ($c_evo[$main_deck[$i]] == 5) || ($c_evo[$main_deck[$i]] == 7)) {
        $shinka_c++;
      } else {
        $creater_c++;
      }
      if(grep(/^$main_deck[$i]$/,@minus10)) {
        $minuscard += 10;
      } elsif(grep(/^$main_deck[$i]$/,@minus5)) {
        $minuscard += 5;
      } elsif(grep(/^$main_deck[$i]$/,@minus3)) {
        $minuscard += 3;
      } elsif(grep(/^$main_deck[$i]$/,@minus1)) {
        $minuscard += 1;
      } elsif(grep(/^$main_deck[$i]$/,@plus1)) {
        $minuscard -= 1;
      }
    }
    $minuscard = 0 if($minuscard < 0);

    my($hikari_bunmei) = $bunmei_c[0] + $bunmei_c[5] + $bunmei_c[6] + $bunmei_c[7] + $bunmei_c[14] + $bunmei_c[15] + $bunmei_c[16] + $bunmei_c[17] + $bunmei_c[18] + $bunmei_c[19] + $bunmei_c[20] + $bunmei_c[25];
    my($mizu_bunmei) = $bunmei_c[1] + $bunmei_c[5] + $bunmei_c[8] + $bunmei_c[9] + $bunmei_c[10] + $bunmei_c[15] + $bunmei_c[16] + $bunmei_c[17] + $bunmei_c[21] + $bunmei_c[22] + $bunmei_c[23] + $bunmei_c[25];
    my($yami_bunmei) = $bunmei_c[2] + $bunmei_c[6] + $bunmei_c[8] + $bunmei_c[11] + $bunmei_c[12] + $bunmei_c[15] + $bunmei_c[18] + $bunmei_c[19] + $bunmei_c[21] + $bunmei_c[22] + $bunmei_c[24] + $bunmei_c[25];
    my($hi_bunmei) = $bunmei_c[3] + $bunmei_c[7] + $bunmei_c[9] + $bunmei_c[11] + $bunmei_c[13] + $bunmei_c[16] + $bunmei_c[18] + $bunmei_c[20] + $bunmei_c[21] + $bunmei_c[23] + $bunmei_c[24] + $bunmei_c[25];
    my($sizen_bunmei) = $bunmei_c[4] + $bunmei_c[10] + $bunmei_c[12] + $bunmei_c[13] + $bunmei_c[14] + $bunmei_c[17] + $bunmei_c[19] + $bunmei_c[20] + $bunmei_c[22] + $bunmei_c[23] + $bunmei_c[24] + $bunmei_c[25];
    my($zero_bunmei) = $bunmei_c[26];


    my($creater_l) = $creater_c * 12;
    my($shinka_l) = $shinka_c * 12;
    my($jumon_l) = $jumon_c * 12;
    my($cross_l) = $cross_c * 12;
    my($hikari_l,$mizu_l,$yami_l,$hi_l,$sizen_l,$zero_l) = ($hikari_bunmei*12,$mizu_bunmei*12,$yami_bunmei*12,$hi_bunmei*12,$sizen_bunmei*12,$zero_bunmei*12);
    my(@bunmei_l) = ($bunmei_c[0]*12,$bunmei_c[1]*12,$bunmei_c[2]*12,$bunmei_c[3]*12,$bunmei_c[4]*12,$bunmei_c[5]*12,$bunmei_c[6]*12,$bunmei_c[7]*12,$bunmei_c[8]*12,$bunmei_c[9]*12,$bunmei_c[10]*12,$bunmei_c[11]*12,$bunmei_c[12]*12,$bunmei_c[13]*12,$bunmei_c[14]*12,$bunmei_c[15]*12,$bunmei_c[16]*12,$bunmei_c[17]*12,$bunmei_c[18]*12,$bunmei_c[19]*12,$bunmei_c[20]*12,$bunmei_c[21]*12,$bunmei_c[22]*12,$bunmei_c[23]*12,$bunmei_c[24]*12,$bunmei_c[25]*12);
    my(@mana_l) = ($mana_c[0]*12,$mana_c[1]*12,$mana_c[2]*12,$mana_c[3]*12,$mana_c[4]*12,$mana_c[5]*12,$mana_c[6]*12,$mana_c[7]*12,$mana_c[8]*12,$mana_c[9]*12,$mana_c[10]*12,$mana_c[11]*12,$mana_c[12]*12,$mana_c[13]*12,$mana_c[14]*12);

    my($minus_l) = $minuscard * 4;
    print<<"EOM";
<table border="1" cellpadding="1" cellspacing="0" width="680" class="table">
<tr><th width="100">クリーチャー</th><td width="40">${creater_c}枚</td><td align="left"><div style="background-color:#888888;width:${creater_l}px;"></div></td></tr>
<tr><th width="100">進化クリーチャー</th><td width="40">${shinka_c}枚</td><td align="left"><div style="background-color:#888888;width:${shinka_l}px;"></div></td></tr>
<tr><th width="100">呪文</th><td width="40">${jumon_c}枚</td><td align="left"><div style="background-color:#888888;width:${jumon_l}px;"></div></td></tr>
<tr><th width="100">クロスギア</th><td width="40">${cross_c}枚</td><td align="left"><div style="background-color:#888888;width:${cross_l}px;"></div></td></tr>
<tr><th width="100">減算ポイント</th><td width="40">${minuscard}Ｐ</td><td align="left"><div style="background-color:#888888;width:${minus_l}px;"></div></td></tr>
</table>
<br><br>
<table border="1" cellpadding="1" cellspacing="0" width="680" class="table">
<tr><th width="100">マナコスト１</th><td width="40">$mana_c[1]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[1]px;"></div></td></tr>
<tr><th width="100">マナコスト２</th><td width="40">$mana_c[2]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[2]px;"></div></td></tr>
<tr><th width="100">マナコスト３</th><td width="40">$mana_c[3]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[3]px;"></div></td></tr>
<tr><th width="100">マナコスト４</th><td width="40">$mana_c[4]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[4]px;"></div></td></tr>
<tr><th width="100">マナコスト５</th><td width="40">$mana_c[5]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[5]px;"></div></td></tr>
<tr><th width="100">マナコスト６</th><td width="40">$mana_c[6]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[6]px;"></div></td></tr>
<tr><th width="100">マナコスト７</th><td width="40">$mana_c[7]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[7]px;"></div></td></tr>
<tr><th width="100">マナコスト８</th><td width="40">$mana_c[8]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[8]px;"></div></td></tr>
<tr><th width="100">マナコスト９</th><td width="40">$mana_c[9]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[9]px;"></div></td></tr>
<tr><th width="100">マナコスト１０</th><td width="40">$mana_c[10]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[10]px;"></div></td></tr>
<tr><th width="100">マナコスト１１</th><td width="40">$mana_c[11]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[11]px;"></div></td></tr>
<tr><th width="100">マナコスト１２</th><td width="40">$mana_c[12]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[12]px;"></div></td></tr>
<tr><th width="100">マナコスト１３</th><td width="40">$mana_c[13]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[13]px;"></div></td></tr>
<tr><th width="100">マナコスト１４</th><td width="40">$mana_c[14]枚</td><td align="left"><div style="background-color:#888888;width:$mana_l[14]px;"></div></td></tr>
</table>
<br><br>
<table border="1" cellpadding="1" cellspacing="0" width="680" class="table">
<tr><th width="100">光総合</th><td width="40">${hikari_bunmei}枚</td><td align="left"><div style="background-color:#888888;width:${hikari_l}px;"></div></td></tr>
<tr><th width="100">水総合</th><td width="40">${mizu_bunmei}枚</td><td align="left"><div style="background-color:#888888;width:${mizu_l}px;"></div></td></tr>
<tr><th width="100">闇総合</th><td width="40">${yami_bunmei}枚</td><td align="left"><div style="background-color:#888888;width:${yami_l}px;"></div></td></tr>
<tr><th width="100">火総合</th><td width="40">${hi_bunmei}枚</td><td align="left"><div style="background-color:#888888;width:${hi_l}px;"></div></td></tr>
<tr><th width="100">自然総合</th><td width="40">${sizen_bunmei}枚</td><td align="left"><div style="background-color:#888888;width:${sizen_l}px;"></div></td></tr>
<tr><th width="100">ゼロ総合</th><td width="40">${zero_bunmei}枚</td><td align="left"><div style="background-color:#888888;width:${zero_l}px;"></div></td></tr>
</table>
<br><br>
<table border="1" cellpadding="1" cellspacing="0" width="680" class="table">
<tr><th width="100">光</th><td width="40">$bunmei_c[0]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[0]px;"></div></td></tr>
<tr><th width="100">水</th><td width="40">$bunmei_c[1]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[1]px;"></div></td></tr>
<tr><th width="100">闇</th><td width="40">$bunmei_c[2]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[2]px;"></div></td></tr>
<tr><th width="100">火</th><td width="40">$bunmei_c[3]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[3]px;"></div></td></tr>
<tr><th width="100">自然</th><td width="40">$bunmei_c[4]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[4]px;"></div></td></tr>
<tr><th width="100">光/水</th><td width="40">$bunmei_c[5]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[5]px;"></div></td></tr>
<tr><th width="100">光/闇</th><td width="40">$bunmei_c[6]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[6]px;"></div></td></tr>
<tr><th width="100">火/光</th><td width="40">$bunmei_c[7]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[7]px;"></div></td></tr>
<tr><th width="100">水/闇</th><td width="40">$bunmei_c[8]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[8]px;"></div></td></tr>
<tr><th width="100">水/火</th><td width="40">$bunmei_c[9]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[9]px;"></div></td></tr>
<tr><th width="100">自然/水</th><td width="40">$bunmei_c[10]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[10]px;"></div></td></tr>
<tr><th width="100">闇/火</th><td width="40">$bunmei_c[11]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[11]px;"></div></td></tr>
<tr><th width="100">闇/自然</th><td width="40">$bunmei_c[12]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[12]px;"></div></td></tr>
<tr><th width="100">火/自然</th><td width="40">$bunmei_c[13]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[13]px;"></div></td></tr>
<tr><th width="100">自然/光</th><td width="40">$bunmei_c[14]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[14]px;"></div></td></tr>
<tr><th width="100">光/水/闇</th><td width="40">$bunmei_c[15]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[15]px;"></div></td></tr>
<tr><th width="100">水/火/光</th><td width="40">$bunmei_c[16]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[16]px;"></div></td></tr>
<tr><th width="100">自然/光/水</th><td width="40">$bunmei_c[17]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[17]px;"></div></td></tr>
<tr><th width="100">火/光/闇</th><td width="40">$bunmei_c[18]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[18]px;"></div></td></tr>
<tr><th width="100">光/闇/自然</th><td width="40">$bunmei_c[19]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[19]px;"></div></td></tr>
<tr><th width="100">火/自然/光</th><td width="40">$bunmei_c[20]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[20]px;"></div></td></tr>
<tr><th width="100">水/闇/火</th><td width="40">$bunmei_c[21]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[21]px;"></div></td></tr>
<tr><th width="100">水/闇/自然</th><td width="40">$bunmei_c[22]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[22]px;"></div></td></tr>
<tr><th width="100">自然/水/火</th><td width="40">$bunmei_c[23]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[23]px;"></div></td></tr>
<tr><th width="100">闇/火/自然</th><td width="40">$bunmei_c[24]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[24]px;"></div></td></tr>
<tr><th width="100">光/水/闇/火/自然</th><td width="40">$bunmei_c[25]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[25]px;"></div></td></tr>
<tr><th width="100">ゼロ</th><td width="40">$bunmei_c[26]枚</td><td align="left"><div style="background-color:#888888;width:$bunmei_l[26]px;"></div></td></tr>
</table>
<br><br>
<table border="1" cellpadding="1" cellspacing="0" width="680" class="table">
<tr><td>
EOM
    foreach my $i(0 .. $#main_deck){
      $j=$main_deck[$i];
      &print_line;
      printf "%s", $c_point[$j] > 0 ? " (<font color=\"#000088\">+$c_point[$j]</font>P)" : $c_point[$j] < 0 ? " (<font color=\"#880000\">$c_point[$j]</font>P)" : "";
      print "<br>\n";
    }
  }
print<<"EOM";
</td></tr>
</table>
EOM
  &footer;
}

sub print_card {
  local $j = $_[0];
  print "<tr><td>";
  &print_line;
  my $pop_v = ($c_pop[$j] == 0) ? "<font color=\"#888888\">0</font>" : "$c_pop[$j]";
  printf "%s", $c_dendou[$j] == 1 ? " (<font color=\"#ff0000\">Ｐ殿堂</font>)" : $c_dendou[$j] == 2 ? " (<font color=\"#880000\">殿堂</font>)" : $c_dendou[$j] == 3 ? " (<font color=\"#888800\">コンビ</font>)" : "";
  printf "%s", $c_point[$j] > 0 ? " (<font color=\"#000088\">+$c_point[$j]</font>P)" : $c_point[$j] < 0 ? " (<font color=\"#880000\">$c_point[$j]</font>P)" : "";
  print qq|</td><td align="right" nowrap>[ $pop_v ] ×&nbsp;<input type="text" size="2" name="sel$j"></td></tr>\n|;
}

sub print_line{
  my $syu = &syu_sub($j);
  my $bun = (&bun_sub($j))[0];
  $c_name[$j] = '不明なカード' if($c_name[$j] eq '');
  print qq|<a href="javascript:sForm('cardview',$j);">$c_name[$j]</a>/$bun/$c_mana[$j]|;
  printf  "%s%s", !(&syu_chk($j, 0)) && !(&syu_chk($j, 1)) && !(&syu_chk($j, 96)) ? "/$c_pow[$j]/$syu" : "", $c_evo[$j] == 4 ? "/進化GV" : 7 < $c_evo[$j] ? "/マナ進化" : 4 < $c_evo[$j] ? "/進化Ｖ" : $c_evo[$j] ? "/進化" : "";
}

sub s_name { $c_name[$a] cmp $c_name[$b]; }
sub s_syuzoku { &syu_sub($a) cmp &syu_sub($b); }
sub s_bunmei {
  $bunmeia = (&bun_sub($a))[1] eq "hikari" ? 1 : (&bun_sub($a))[1] eq "mizu" ? 2 : (&bun_sub($a))[1] eq "yami" ? 3 : (&bun_sub($a))[1] eq "hi" ? 4 : (&bun_sub($a))[1] eq "sizen" ? 5 : (&bun_sub($a))[1] eq "zero" ? 6 : 7;
  $bunmeib = (&bun_sub($b))[1] eq "hikari" ? 1 : (&bun_sub($b))[1] eq "mizu" ? 2 : (&bun_sub($b))[1] eq "yami" ? 3 : (&bun_sub($b))[1] eq "hi" ? 4 : (&bun_sub($b))[1] eq "sizen" ? 5 : (&bun_sub($b))[1] eq "zero" ? 6 : 7;
  $bunmeia <=> $bunmeib;
}
sub s_power { $c_pow[$a] <=> $c_pow[$b]; }
sub s_mana { $c_mana[$a] <=> $c_mana[$b]; }
sub s_pop { $c_pop[$b] <=> $c_pop[$a]; }

sub cardsort {
  foreach my $i (@disp) {
    if (&syu_chk($i, 96)) { push @sort_src4, $i; }
    elsif (&syu_chk($i, 1)) { push @sort_src3, $i; }
    elsif (&syu_chk($i, 0)) { push @sort_src2, $i; }
    elsif (&syu_chk($i, 145) || &syu_chk($i, 150) || &syu_chk($i, 103) || &syu_chk($i, 119) || &syu_chk($i, 151) || &syu_chk($i, 185) || &syu_chk($i, 186)) { push @sort_src5, $i; }
    else { push @sort_src1, $i; }
  }
  @sort_res1 = $F{'sortkey1'} == 0 ? sort s_bunmei @sort_src1 : $F{'sortkey1'} == 1 ? sort s_mana @sort_src1: $F{'sortkey1'} == 2 ? sort s_power @sort_src1 : $F{'sortkey1'} == 3 ? sort s_syuzoku @sort_src1 : sort s_name @sort_src1;
  @sort_res2 = $F{'sortkey2'} == 0 ? sort s_bunmei @sort_src2 : $F{'sortkey2'} == 1 ? sort s_mana @sort_src2 : sort s_name @sort_src2;
  @sort_res3 = $F{'sortkey3'} == 0 ? sort s_bunmei @sort_src3 : $F{'sortkey3'} == 1 ? sort s_mana @sort_src3 : sort s_name @sort_src3;
  @sort_res4 = $F{'sortkey4'} == 0 ? sort s_bunmei @sort_src4 : $F{'sortkey4'} == 1 ? sort s_mana @sort_src4 : sort s_name @sort_src4;
  @sort_res5 = $F{'sortkey5'} == 0 ? sort s_bunmei @sort_src5 : $F{'sortkey5'} == 1 ? sort s_mana @sort_src5 : sort s_name @sort_src5;
  $selstr6[$F{'sortkey1'}] = $selstr7[$F{'sortkey2'}] = $selstr8[$F{'sortkey3'}] = $selstr9[$F{'sortkey4'}] = $selstr10[$F{'sortkey5'}] = " selected";
}

sub decksort{
  $lva = $c_syu[$a] == 1 ? 2 : $c_syu[$a] == 0 ? 1 : 0;
  $lvb = $c_syu[$b] == 1 ? 2 : $c_syu[$a] == 0 ? 1 : 0;
  $lva <=> $lvb || &s_bunmei || &s_mana || &s_power || &s_name;
}

sub deckview_text {
  print "　デッキ枚数-$deckcou枚<br><br>\n";
  print q|<textarea cols="30" rows="70" name="text">|;
  map { $c_name[$_] = '不明なカード' if($c_name[$_] eq ''); print "$c_name[$_]\n" } @main_deck if $deckcou != 0;
  print "\n</textarea>\n";
}

sub deckview {
  print "　デッキ枚数　現在$deckcou枚\n";
  print qq|　　<small><label><input type="checkbox" name="allchk" onclick="chkCB();" class="none">全チェック</label></small><br><br>\n|;
  if($deckcou != 0){
    foreach my $i(0 .. $#main_deck){
      $j = $main_deck[$i];
      print qq|<input type="checkbox" name="del$main_num[$i]" class="none">\n|;
      &print_line;
      print "<br>\n";
    }
  }
}

sub deckpview_text {
  print "　デッキ枚数-$deckpcou枚<br><br>\n";
  print q|<textarea cols="30" rows="70" name="text">|;
  map { $c_name[$_] = '不明なカード' if($c_name[$_] eq ''); print "$c_name[$_]\n" } @main_deck_psychic if $deckpcou != 0;
  print "\n</textarea>\n";
}

# GRクリーチャー一覧表示（テキスト形式）
sub deckgview_text {
  print "　デッキ枚数-$deckgcou枚<br><br>\n";
  print q|<textarea cols="30" rows="70" name="text">|;
  map { $c_name[$_] = '不明なカード' if($c_name[$_] eq ''); print "$c_name[$_]\n" } @main_deck_gr if $deckgcou != 0;
  print "\n</textarea>\n";
}

sub deckpview {
  print "　デッキ枚数　現在$deckpcou枚\n";
  print qq|　　<small><label><input type="checkbox" name="allchkp" onclick="chkCBp();" class="none">全チェック</label></small><br><br>\n|;
  if($deckpcou != 0){
    foreach my $i(0 .. $#main_deck_psychic){
      $j = $main_deck_psychic[$i];
      print qq|<input type="checkbox" name="delp$mainp_num[$i]" class="none">\n|;
      &print_line;
      print "<br>\n";
    }
  }
}

# GRクリーチャー一覧表示
sub deckgview {
  print "　デッキ枚数　現在$deckgcou枚\n";
  print qq|　　<small><label><input type="checkbox" name="allchkg" onclick="chkCBg();" class="none">全チェック</label></small><br><br>\n|;
  if($deckgcou != 0){
    foreach my $i(0 .. $#main_deck_gr){
      $j = $main_deck_gr[$i];
      print qq|<input type="checkbox" name="delg$maing_num[$i]" class="none">\n|;
      &print_line;
      print "<br>\n";
    }
  }
}

sub syu_chk {
  my ($card, $syu) = @_;
  return grep $_ == $syu, (split /,/, $c_syu[$card]);
}

sub put_ini{
  return unless $id;
  $P{'predeck'} = join(",",@deck);
  $P{'predeckp'} = join(",",@deckp);
  $P{'predeckg'} = join(",",@deckg);
  &pfl_write($id);
}

sub deckread{
  return unless -e "${player_dir}/".$id.".cgi";
  &pfl_read($id);
  my $cou = 0;
  foreach my $i(1 .. $maxdeck){
    if(!($P{"deck$i"})){ $dnam[$i] = "記録なし"; @{$deck[$i]} = (); @{$deckp[$i]} = (); @{$deckg[$i]} = (); next; }
    else{
      # プレイヤーデータから-区切りで各種類のカード番号取得
      ($dnam[$i],$dcon[$i],$dconp[$i],$dcong[$i]) = split(/-/,$P{"deck$i"});
      $cou = $i;
    }
  }
  # 使用デッキ取得
  $P{'usedeck'} = $cou if $cou && !($P{'usedeck'});
  # 通常
  @deck = $P{'predeck'} ? split(/,/,$P{'predeck'}) : $P{'usedeck'} ? split(/,/,$dcon[$P{'usedeck'}]) : ();
  # サイキック
  @deckp = $P{'predeckp'} ? split(/,/,$P{'predeckp'}) : $P{'usedeck'} ? split(/,/,$dconp[$P{'usedeck'}]) : ();
  # GR
  @deckg = $P{'predeckg'} ? split(/,/,$P{'predeckg'}) : $P{'usedeck'} ? split(/,/,$dcong[$P{'usedeck'}]) : ();
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

sub j_script {
  print <<"EOM";
<script type="text/javascript"><!--
function sForm(F,C){
  with(document.form){
    mode.value = F;
    j.value = C;
    action = F == "taisen" ? "taisen.cgi" : F == "group" ? "group.cgi" : F == "list" ? "list.cgi" : F == "nuisance" ? "nuisance.cgi" : "deck.cgi";
    target = F == "cardview" ? "_blank" : "";
    submit();
  }
}
// --></script>
EOM
}

sub info_read {
  my(@pop_day) = ();
  my($cnt) = 0;
  &filelock("pop");
  open(POP,"./popular.dat") || &error("使用カード記録データが開けません");
  $pop_date = <POP>;
  chomp($pop_date);
  while(<POP>){ chomp; @{$pop_day[$cnt]} = split(/,/); $cnt ++; }
  close(POP);
  &fileunlock("pop");

  @c_pop = ();
  for(my($i) = 0; $i <= $#pop_day; $i ++) {
    foreach(@{$pop_day[$i]}) {
      $c_pop[$i] += $_;
    }
  }

  @c_dendou = ();

  for(my($i) = 0; $i <= $#premium; $i ++) {
    $c_dendou[$premium[$i]] = 1;
  }
  for(my($i) = 0; $i <= $#dendou; $i ++) {
    $c_dendou[$dendou[$i]] = 2;
  }
  for(my($i) = 0; $i <= $#combi; $i ++) {
    $c_dendou[$combi[$i][0]] = 3;
    $c_dendou[$combi[$i][1]] = 3;
  }

  @c_point = ();
  for(my($i) = 0; $i <= $#minus10; $i ++) {
    $c_point[$minus10[$i]] -= 10;
  }
  for(my($i) = 0; $i <= $#minus5; $i ++) {
    $c_point[$minus5[$i]] -= 5;
  }
  for(my($i) = 0; $i <= $#minus3; $i ++) {
    $c_point[$minus3[$i]] -= 3;
  }
  for(my($i) = 0; $i <= $#minus1; $i ++) {
    $c_point[$minus1[$i]] -= 1;
  }
  for(my($i) = 0; $i <= $#plus1; $i ++) {
    $c_point[$plus1[$i]] += 1;
  }
}
