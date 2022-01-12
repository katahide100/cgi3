#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

require 'cust.cgi';
require 'duel.pl';

&decode;
&get_cookie;
$F{'id'} = $c_id if(!$F{'id'});
$F{'pass'} = $c_pass if(!$F{'pass'});
&set_cookie;

&decode2;
&pfl_read($id);
&pass_chk;

&html;

sub html{
	chmod 0666, "log/lognumber.dat";
	open(NUM,"log/lognumber.dat") || &error("ログ番号記録ファイルが開けません。"); 
	$lognumber = <NUM>;
	close(NUM);

	$F{'room'} = $lognumber unless($F{'room'});
	open(LOG,"log/msglog$F{'room'}.dat"); 
	@lines = reverse(<LOG>);
	close(LOG);

	&header;
	print <<"EOM";
<script type="text/javascript"><!--
	with(document);
	function sForm(M,R,C) {
		entrance.mode.value = M;
		entrance.room.value = R;
		entrance.chara.value = C;
		if(M == "deck") {
			entrance.action = "deck.cgi";
		} else if(M == "taisen") {
			entrance.action = "taisen.cgi";
		} else if(M == "prof") {
			entrance.action = "taisen.cgi";
		} else if(M == "group") {
			entrance.action = "group.cgi";
		} else if(M == "list") {
			entrance.action = "list.cgi";
		} else if(M == "nuisance") {
			entrance.action = "nuisance.cgi";
		} else if(M == "log") {
			entrance.action = "log.php";
		} else if(M == "log-old") {
			entrance.action = "log-old.cgi";
		} else if(M == "index") {
			entrance.action = "index.cgi";
		} else {
			entrance.action = "log.php";
		}
		entrance.target = (M == "prof") ? "_blank" : "_self";
		entrance.submit();
	}
// --></script>
</head>
<body>
<div align="center">
<h1>$title</h1>
<a href="javascript:sForm('taisen', '', '');">対戦画面</a>&nbsp;&nbsp;
<a href="javascript:sForm('deck', '', '');">デッキ構築</a>&nbsp;&nbsp;
<a href="javascript:sForm('group', '', '');">グループ編集</a>&nbsp;&nbsp;
<a href="javascript:sForm('list', '', '');">リスト編集</a>&nbsp;&nbsp;
<a href="javascript:sForm('nuisance', '', '');">迷惑行為</a>&nbsp;&nbsp;
<a href="javascript:sForm('index', '', '');">トップへ戻る</a>
<hr width="640">
EOM
	for(my($i) = $lognumber; $i >= 1; $i--) {
		if($F{'room'} != $i) {
			print "[<a href=\"javascript:sForm('log-old', '$i', '');\">$i</a>] ";
		} else {
			print "[<b>$i</b>] ";
		}
	}
	print <<"EOM";
<hr width="640">
<form action="log-old.cgi" method="post" name="entrance" style="display: inline;">
	<input type="hidden" name="id" value="$id">
	<input type="hidden" name="pass" value="$pass">
	<input type="hidden" name="mode" value="">
	<input type="hidden" name="room" value="">
	<input type="hidden" name="chara" value="">
<table width="800" border="0" cellpadding="3" cellspacing="0" bgcolor="#FFFFFF">
<tr><td>
<table width="100%" border="0" cellpadding="1" cellspacing="0" bgcolor="#FFFFFF">
EOM
	my($cnt) = 0;
	my(@black) = split(/\,/, $P{'blacklist'});
	foreach(@lines){
		my($num,$wdate,$lid,$name,$com,$pass,$ip,$order,$pcchk,$white,$black,$channel) = split(/<>/);
		my($symbol) = "";
		next if(grep(/^$lid$/, @black));
		if($black ne '') {
			next if(grep(/^$P{'id'}$/, split(/\,/, $black)));
		}
		if($channel eq '') {
			$com = "<font color=\"#004488\">$com</font>";
		}
		my($vnum) = ($channel eq '') ? "[$num]" : "[$num]:$channel";
#		my($id) = $1 if($name =~ /\<A\ href\=\"javascript\:sForm\(\'prof\'\, \'\'\,\ \'(.*?)\'\)\;\"\>.*?\<\/A\>/);
		print <<"EOM";
<tr valign="top">
<td nowrap>$vnum&nbsp;<A href=\"javascript:sForm('prof', '', '$lid');\">$name</A>&nbsp;</td>
<td nowrap>&gt;&nbsp;</td>
<td>$com<small> ($wdate) - $ip</small></td>
</tr>
<tr><td colspan="3"><hr size="1" color="#000000"></td></tr>
EOM
		$cnt ++;
	}
	print <<"EOM";
</table>
</td></tr>
</table>

	</form>
</div>
EOM
	&footer;
}

sub set_cookie{ 
	($sec,$min,$hour,$mday,$mon,$year) = gmtime(time + 30*24*60*60);
	$gdate = sprintf("%02d\-%s\-%04d %02d:%02d:%02d", $mday, ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mon], $year + 1900, $hour, $min, $sec);
	$cook = "id:$F{'id'},pass:$F{'pass'}";
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
}

sub decode2 {
	$id = $F{'id'};
	$pass = $F{'pass'}; $pass =~ s/\.//g; $pass =~ s/\///g;
	&error("IDが入力されていません") unless $id;
	&error("パスワードが入力されていません。") unless $pass;
}