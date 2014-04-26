sub alluc {
&lock;
open(UCN,"$multif$userc") or &error("óòópé“èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉãÅF${multif}${userc} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@uc = <UCN>;
close(UCN);
&unlock;
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>Ç›ÇÒÇ»ÇÃèëÇ´çûÇ›âÒêî Å| ${title}</title>
</head>
<body>
<div align="center">
<font size="$tsize" color="$tcolor">Ç›ÇÒÇ»ÇÃèëÇ´çûÇ›âÒêî</font>
<hr>
Ç›ÇÒÇ»ÇÃèëÇ´çûÇ›âÒêîÇ≈Ç∑ÅB<br>
è„à 100à Ç‹Ç≈Ç™ÅAï\\é¶Ç≥ÇÍÇ‹Ç∑ÅB
<hr>
<table summary="ï\\" border="0" cellspacing="16" cellpadding="4" style="background-color:#ffffff;">
<tr><td>
<table summary="ï\\" border="0" cellspacing="4" cellpadding="0" style="background-color:#ffffff;">
<tr><td>Ç®ñºëO</td><td>âÒêî</td><td>ç≈èIèëÇ´çûÇ›éûçè</td><td>ID</td></tr>
END
$rankc = 0;
foreach $tmpuc (@uc) {
$rankc++;
($ucid,$ucname,$uccount,$uctimev,$uctimes) = split(/<>/,$tmpuc);
$ucidv = substr($ucid, -10, 10);
print"<tr><td>${rankc}. <b>$ucname</b>Ç≥ÇÒ</td><td><b>$uccount</b>âÒ</td><td>$uctimev</td><td>$ucidv</td></tr>\n";
last if($rankc >= 100);
}
print<<END;
</table>
</td></tr>
</table><br>
<a href="$script?id=$Fm{'id'}">åfé¶î¬Ç÷ñﬂÇÈ</a>
</div>
END
&footer;
print<<END;
</body>
</html>
END
}

sub numbers {
@result = ();
$vrc = 0;
$Fm{'page'} = int($Fm{'page'});
$hit = 0;
if($Fm{'n'} ne '') {
&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
&unlock;
($n1,$n2) = split(/\-/,$Fm{'n'});
$n2 = $n1 if($n2 eq '');
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount) = split(/\,/,$lhost);
if($lrno ne '') {
$vrc++;
} else {
$vrc = 1;
}
if($Fm{'t'} ne '') {
if((($lno eq $Fm{'t'}) && ($n1 <= $vrc) && ($n2 >= $vrc)) || (($lrno eq $Fm{'t'}) && ($n1 <= $vrc) && ($n2 >= $vrc))) {
push(@result,$tmplog) if((($Fm{'page'} * $sonep) <= $hit) && (($Fm{'page'} * $sonep) + $sonep > $hit));
$hit++;
}
} else {
if(($lno >= $n1) && ($lno <= $n2)) {
push(@result,$tmplog) if((($Fm{'page'} * $sonep) <= $hit) && (($Fm{'page'} * $sonep) + $sonep > $hit));
$hit++;
}
}



}

print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ãLéñåüçı Å| ${title}</title>
</head>
<body>
[<a href="$script?id=$Fm{'id'}">åfé¶î¬Ç…ñﬂÇÈ</a>]<br><br>
END
if(@result > 0) {
print<<END;
åüçıåãâ ÅF<b>$hit</b>åèÇ™ÅAHitÇµÇ‹ÇµÇΩÅB<br>
END
$tmpp = $Fm{'page'} - 1;
if($Fm{'page'} > 0) { print"<a href=\"$script?id=$Fm{'id'}&amp;mode=numbers&amp;n=$Fm{'n'}&amp;t=$Fm{'t'}&amp;page=$tmpp\">Å©ëOÇÃÉyÅ[ÉW</a> "; } else { print"Å©ëOÇÃÉyÅ[ÉW "; }
for($i=0;$i<=int($hit / 10);$i++) {
if($i eq $Fm{'page'}) {
print"[<b>$i</b>] ";
} else {
print"[<a href=\"$script?id=$Fm{'id'}&amp;mode=numbers&amp;n=$Fm{'n'}&amp;t=$Fm{'t'}&amp;page=${i}\">${i}</a>] ";
}
}
$tmpp = $Fm{'page'} + 1;
if(($Fm{'page'} * $sonep) + $sonep < $hit) { print"<a href=\"$script?id=$Fm{'id'}&amp;mode=numbers&amp;n=$Fm{'n'}&amp;t=$Fm{'t'}&amp;page=$tmpp\">éüÇÃÉyÅ[ÉWÅ®</a>"; } else { print"éüÇÃÉyÅ[ÉWÅ®"; }
}
print<<END;
<hr>
<div align="center">
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
END
if(@result > 0) {

foreach $tmplog (@result) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount) = split(/\,/,$lhost);
$lid = substr($lpass, -10, 10);
&jumper;
&quotation;
$ltitle = "[No.${lrno}Ç÷ÇÃï‘êMãLéñÇ≈Ç∑] " . $ltitle if($lrno ne '');
$printicon = ($licon ne '') ? "<img src=\"${imgdir}$licon\" alt=\"$licon\">" : '';
if($lcount ne '') { $ucview = ($ucon == 1) ? " (èëÇ´çûÇ› <b>${lcount}</b>âÒ)" : ''; } else { $ucview = ''; }
print<<END;
<b>$ltitle</b> ìäçeé“ÅF<b>$lname</b>Ç≥ÇÒ${ucview} - <small>$ltime</small> <font color="#888800" size="-1">No.$lno</font> <small>ID: $lid</small>
<table summary="ï\\" border="0" cellspacing="16" cellpadding="0">
<tr><td>$printicon</td><td><font color="$lcolor">
$lcomment
<!-- IP:${raddr} HOST:${rhost} -->
</font></td></tr>
</table>
<hr>
END
}
} else {
print"Ç®íTÇµÇÃãLéñÇÕë∂ç›ÇµÇ‹ÇπÇÒÅB<br>Ç∑Ç≈Ç…çÌèúÇ≥ÇÍÇΩÇ©ÅAãLéñNo.Çä‘à·Ç¡ÇΩâ¬î\\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB\n";
}
print<<END;
</td></table>
</body>
</html>
END
} else {
&pagemove("$script");
}
}

sub search {
if($Fm{'key'} ne '') {

&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
&unlock;
$Fm{'page'} = int($Fm{'page'});
$hit = 0;
if($Fm{'key'} ne '') {
@key = split(/(?:\ |Å@)/,$Fm{'key'});
foreach $tmplog (@log) {
$findflag = ($Fm{'sm'} eq '1') ? 1 : 0;

foreach $key (@key) {
$tmp2log = unpack('H*',$tmplog);
$tmpkey = unpack('H*',$key);
if($Fm{'sm'} eq '1') {
$findflag = 0 if($tmp2log !~ /$tmpkey/);
} else {
$findflag = 1 if($tmp2log =~ /$tmpkey/);
}
}
if($findflag == 1) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);

if((($Fm{'page'} * $sonep) <= $hit) && (($Fm{'page'} * $sonep) + $sonep > $hit)) {
$ltitle = "[No.${lrno}Ç÷ÇÃï‘êMãLéñÇ≈Ç∑] " . $ltitle if($lrno ne '');
$lid = substr($lpass, -10, 10);
&jumper;
&quotation;
$printicon = ($licon ne '') ? "<img src=\"${imgdir}$licon\" alt=\"$licon\">" : '';
if($lcount ne '') { $ucview = ($ucon == 1) ? " (èëÇ´çûÇ› <b>${lcount}</b>âÒ)" : ''; } else { $ucview = ''; }
$print .= <<END;
<b>$ltitle</b> ìäçeé“ÅF<b>$lname</b>Ç≥ÇÒ${ucview} - <small>$ltime</small> <font color="#888800" size="-1">No.$lno</font> <small>ID: $lid</small>
<table summary="ï\\" border="0" cellspacing="16" cellpadding="0">
<tr><td>$printicon</td><td><font color="$lcolor">
$lcomment
<!-- IP:${raddr} HOST:${rhost} -->
</font></td></tr>
</table>
<hr>
END
}
$hit++;
}
}
}

}
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ãLéñåüçı Å| ${title}</title>
</head>
<body>
[<a href="$script?id=$Fm{'id'}">åfé¶î¬Ç…ñﬂÇÈ</a>]
<div align="center"><font size="6" color="#0000ff">ãLéñåüçı</font></div>
<form action="$script" method="GET" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="search">
<blockquote>
ÅEåüçıÉLÅ[ÉèÅ[ÉhÇÕÅAãÛîíÇ≈ãÊêÿÇÈÇ±Ç∆Ç≈ÅAï°êîéwíËÇ∑ÇÈÇ±Ç∆Ç™Ç≈Ç´Ç‹Ç∑ÅB<br>

<br>
<input type="text" size="30" name="key" value="$Fm{'key'}">
<select name="sm">
END
if($Fm{'sm'} ne '1') { print'<option value="0" selected>OR</option>'; } else { print'<option value="0">OR</option>'; }
if($Fm{'sm'} eq '1') { print'<option value="1" selected>AND</option>'; } else { print'<option value="1">AND</option>'; }
print<<END;

</select>
<input type="submit" value="åüçı">
</blockquote>
</form>
END
if($Fm{'key'} ne '') {
print<<END;
åüçıåãâ ÅF<b>$hit</b>åèÇ™ÅAHitÇµÇ‹ÇµÇΩÅB<br>
END
$codekey = $Fm{'key'};
$codekey =~ s/(\W)/'%'.unpack("H2", $1)/ego;
$tmpp = $Fm{'page'} - 1;
if($Fm{'page'} > 0) { print"<a href=\"$script?id=$Fm{'id'}&amp;mode=search&amp;key=$codekey&amp;sm=$Fm{'sm'}&amp;page=$tmpp\">Å©ëOÇÃÉyÅ[ÉW</a> "; } else { print"Å©ëOÇÃÉyÅ[ÉW "; }
for($i=0;$i<=int($hit / 10);$i++) {
if($i eq $Fm{'page'}) {
print"[<b>$i</b>] ";
} else {
print"[<a href=\"$script?id=$Fm{'id'}&amp;mode=search&amp;key=$codekey&amp;sm=$Fm{'sm'}&amp;page=${i}\">${i}</a>] ";
}
}
$tmpp = $Fm{'page'} + 1;
if(($Fm{'page'} * $sonep) + $sonep < $hit) { print"<a href=\"$script?id=$Fm{'id'}&amp;mode=search&amp;key=$codekey&amp;sm=$Fm{'sm'}&amp;page=$tmpp\">éüÇÃÉyÅ[ÉWÅ®</a>"; } else { print"éüÇÃÉyÅ[ÉWÅ®"; }
}
print<<END;
<hr>
<div align="center">
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
$print
</td></table>
</div>
<br><br>
<a href="$script?id=$Fm{'id'}">ñﬂÇÈ</a>
END
&footer;
print<<END;
</body>
</html>
END
}

sub iconlist {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ÉAÉCÉRÉìàÍóó Å| ${title}</title>
</head>
<body>
<div align="center">
<font size="$tsize" color="$tcolor">ÉAÉCÉRÉìàÍóó</font>
<table summary="ï\\" border="1" cellspacing="16" cellpadding="4" style="background-color:#ffffff;">
END
$iconcount = 0;
foreach $tmpicon (@icon) {
($tmpiconaddr,$tmpiconname) = split(/\,/,$tmpicon);
if(($tmpiconaddr eq '') || ($tmpiconaddr eq 'special')) {
next;
} else {
if($icon ne '') { $selected = ($icon eq $iconcount) ? ' selected' : ''; } else { $selected = ($iconcount == 0) ? ' selected' : ''; }
print"<tr>\n" if($iconcount % 5 == 0);
print"<td align=\"center\" valign=\"center\"><img src=\"${imgdir}${tmpiconaddr}\" alt=\"$tmpiconaddr\"><br><b>${tmpiconname}</b></td>\n";
print"</tr>" if($iconcount % 5 == 4);
$iconcount++;
}
}
for($i=0;$i<5 - ($iconcount % 5);$i++) {
print"<td></td>\n";
}
print"</tr>" if($iconcount % 5 != 4);
print<<END;
</table><br>
<a href="$script?id=$Fm{'id'}">åfé¶î¬Ç÷ñﬂÇÈ</a>
</div>
END
&footer;
print<<END;
</body>
</html>
END
}

sub agreement {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>åfé¶î¬óòópãKñÒ Å| ${title}</title>
</head>
<body>
${agmcom}
<hr>
END
if(($cflag ne 'ok') && ($queson != 0)) {
print<<END;
åfé¶î¬óòópãKñÒÇ…<br><br>
<button onClick="location.href = '${script}?mode=question';">ìØà”Ç∑ÇÈ</button> <button onClick="location.href = '$backpa';" onKeyPress="">ìØà”ÇµÇ»Ç¢</button>
<hr>
<a href="$backpa">${backpn}Ç÷ñﬂÇÈ</a>
END
} else {
print<<END;
<a href="$script?id=$Fm{'id'}">åfé¶î¬Ç÷ñﬂÇÈ</a>
END
}
print<<END;
END
&footer;
print<<END;
</body>
</html>
END
}

sub question {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>óòópãKñÒéøñ‚ Å| ${title}</title>
</head>
<body>
óòópãKñÒÇ…ä÷Ç∑ÇÈÅAä»íPÇ»ñ‚ëËÇ≈Ç∑ÅB<br>
ëSñ‚ê≥âÇ∑ÇÍÇŒÅAÇnÇjÇ≈Ç∑ÅB<br><br>
<form action="$script" method="POST" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="cookie">
<table summary="ï\\" border="1" cellspacing="0" cellpadding="0">
END
$count = 0;
foreach $ques (@ques) {
$tc = $count + 1;
$qnum = 1;
@candq = split(/<>/,$cand[$count]);
$candc = @cand;
print"<TR><TD colspan=\"3\">Q${tc}. $ques</TD>\n";
print"<TR>\n";
foreach $cand (@candq) {
print"<TD align=\"left\" valign=\"top\">${qnum}. <input type=\"radio\" name=\"q${count}\" value=\"$qnum\"><br>${cand}</TD>\n";
$qnum++;
}
print"<TR><TD colspan=\"3\"><hr></TD>\n";
$count++;
}
print<<END;
</TABLE>
<br>
<input type="submit" value="âÒìö">
</form>
<hr>
<a href="$script?id=$Fm{'id'}">óòópãKñÒÇ÷ñﬂÇÈ</a>
END
&footer;
print<<END;
</body>
</html>
END
}

sub setcookie {
$count = 0; $misst = 0;
foreach $answ (@answ) {
if($answ ne $Fm{"q${count}"}) {
$misst = 1;
last;
}
$count++;
}
if($misst == 1) {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ä‘à·Ç¢ Å| ${title}</title>
</head>
<body>
âÒìöÇ™ÅAä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB<br>
Ç‡Ç§àÍìxÅAóòópãKñÒÇÇµÇ¡Ç©ÇËÇ∆ì«Ç›íºÇµÇƒÅAçƒíßêÌÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br><br>
<a href="$script?id=$Fm{'id'}">óòópãKñÒÇ÷</a>
END
&footer;
print<<END;
</body>
</html>
END
} else {
&sendcookie;
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ê≥â Å| ${title}</title>
</head>
<body>
ëSñ‚ê≥âÇ≈Ç∑ÅB<br>
Ç≈ÇÕÅAåfé¶î¬Ç÷ÉåÉbÉcÉSÅ[Ç≈Ç∑Å`ÅB<br><br>
<a href="$script?id=$Fm{'id'}">åfé¶î¬Ç÷</a>
END
&footer;
print<<END;
</body>
</html>
END
}
}

sub check {
$uri = $Fm{'uri'};
$uri = $1 if($ENV{'QUERY_STRING'} =~ /uri\=(.*)/);
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ÉWÉÉÉìÉv Å| ${title}</title>
</head>
<body>
<div align="center">
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
<a href="$uri">$uri</a><br><br>
è„ãLÇÃÉTÉCÉgÇ÷ÉäÉìÉNÇµÇÊÇ§Ç∆ÇµÇƒÇ¢Ç‹Ç∑ÅB<br>
îOÇÃÇΩÇﬂÅA<a href="http://www.jah.ne.jp/~fild/cgi-bin/LBCC/lbcc.cgi?$uri" target="_blank">ÉuÉâÉNÉâÉ`ÉFÉbÉJÅ[</a>Ç≈í≤Ç◊ÇΩÇËÅA<br>
<a href="view-source:$uri">É\\Å[ÉXÇå©ÇÈ</a>Ç±Ç∆ÇÇ∑ÇÈÇÃÇÅAÇ®Ç∑Ç∑ÇﬂÇµÇ‹Ç∑ÅB<br>
</td></table>
</div>
<br>
<a href="$script?id=$Fm{'id'}">ñﬂÇÈ</a>
END
&footer;
print<<END;
</body>
</html>
END
}

1;
