#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

require "cust.cgi";
require "duel.pl";

&cardread;
&inforead;

@cardlist = (0 .. $#c_name);

&header;
print <<"EOM";
</head>
<body>
<div align="center">
<h1>$title</h1>
<table border="1" width="600" cellspacing="0" cellpadding="10">
<tr><td class="table"> 
<p>この対戦ＣＧＩで、ここ一週間の人気カード情報です。<br>
上位100位までを表示しています。</p>
<div align="center">
<table border="0" cellpadding="4" cellspacing="0">
<tr bgcolor="#c0c0c0"><td>順位</td><td>カード名</td><td>累計</td><td>今日</td><td>1日前</td><td>2日前</td><td>3日前</td><td>4日前</td><td>5日前</td><td>6日前</td></tr>
EOM
@cardlist = sort s_pop @cardlist;
my($order) = 1;
my($last_pop) = $c_pop[$cardlist[0]];
my($cnt) = 0;
foreach(@cardlist) {
	last if($c_pop[$_] == 0);
	if($last_pop > $c_pop[$_]) {
		$order ++;
		$last_pop = $c_pop[$_];
		last if($order > 100);
	}
	
	$vday0 = ($pop_day[$_][0] == 0) ? "<font color=\"#888888\">0</font>" : $pop_day[$_][0];
	$vday1 = ($pop_day[$_][1] == 0) ? "<font color=\"#888888\">0</font>" : $pop_day[$_][1];
	$vday2 = ($pop_day[$_][2] == 0) ? "<font color=\"#888888\">0</font>" : $pop_day[$_][2];
	$vday3 = ($pop_day[$_][3] == 0) ? "<font color=\"#888888\">0</font>" : $pop_day[$_][3];
	$vday4 = ($pop_day[$_][4] == 0) ? "<font color=\"#888888\">0</font>" : $pop_day[$_][4];
	$vday5 = ($pop_day[$_][5] == 0) ? "<font color=\"#888888\">0</font>" : $pop_day[$_][5];
	$vday6 = ($pop_day[$_][6] == 0) ? "<font color=\"#888888\">0</font>" : $pop_day[$_][6];
	$bgc = ($cnt % 2 == 0) ? "#c0ffc0" : "#c0c0c0";
	print <<"EOM";
	<tr bgcolor="$bgc"><td>$order</td><td>$c_name[$_]</td><td>$c_pop[$_]</td><td>$vday0</td><td>$vday1</td><td>$vday2</td><td>$vday3</td><td>$vday4</td><td>$vday5</td><td>$vday6</td></tr>
EOM
	$cnt ++;
}
print <<"EOM";
</table><br>
<p><a href="index.cgi">戻る</a></p>
</div>
</td></tr>
</table>
EOM
&footer;

sub s_pop { $c_pop[$b] <=> $c_pop[$a]; }

sub inforead {
	@pop_day = ();
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
}
