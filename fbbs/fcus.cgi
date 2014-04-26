sub custom {
if($Fm{'pass'} ne '') {
&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
&unlock;

$adminflag = 0;
foreach $adpass (@adpass) {
if($Fm{'pass'} eq $adpass) {
$adminflag = 1;
last;
}

}
$tmppass = $Fm{'pass'};
$cpass = crypt($Fm{'pass'},$crp);
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ãLéñï“èWÅEçÌèúÉtÉHÅ[ÉÄ Å| ${title}</title>
</head>
<body>
END
if(($Fm{'dmode'} eq 'edit') || ($Fm{'dmode'} eq 'delete')) {
$find = 0;
$print = '';
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
$ecomment = $lcomment;
$cpass = $lpass if(($adminflag == 1) && ($lno eq $Fm{'no'}));
$plpass = $lpass if($lrno ne '');

if(($lno eq $Fm{'no'}) && ($lpass ne $cpass)) { $find = 2; last; }
elsif((($lno eq $Fm{'no'}) && ($lpass eq $cpass))	||
(($lno eq $Fm{'no'}) && ($adminflag == 1)))		{
&jumper;
&quotation;
$print .= <<END;
<hr><b>$ltitle</b> ìäçeé“ÅF<b>$lname</b>Ç≥ÇÒ - <small>$ltime</small> <font color="#888800" size="-1">No.$lno</font>
<blockquote><font color="$lcolor">$lcomment</font></blockquote>
END
$find = 1;
last;
}
}
if($find == 1) {
if($Fm{'dmode'} eq 'edit') {
print"<small>ãLéñNo.$Fm{'no'} ÇÃï“èWÉtÉHÅ[ÉÄÇ≈Ç∑ÅB[<a href=\"$script?id=$Fm{'id'}\" onClick=\"if(!confirm('ï“èWÇé~ÇﬂÇƒñﬂÇËÇ‹Ç∑Ç©ÅH')) return false;\" onKeyPress=\"\">ñﬂÇÈ</a>]</small><br><br>\n";
} elsif($Fm{'dmode'} eq 'delete') {
print"<small>ãLéñNo.$Fm{'no'} ÇÃçÌèúÉtÉHÅ[ÉÄÇ≈Ç∑ÅB[<a href=\"$script?id=$Fm{'id'}\" onClick=\"if(!confirm('çÌèúÇé~ÇﬂÇƒñﬂÇËÇ‹Ç∑Ç©ÅH')) return false;\" onKeyPress=\"\">ñﬂÇÈ</a>]</small><br><br>\n";
}
print<<END;
<div align="center">
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
$print
<hr></td></table><br>
END
$Fm{'pass'} = $tmppass if($adminflag == 1);
$ecomment =~ s/<font style\=\"color\:\#000000\;background\-color\:\#000000\;\">(.*?)<\/font>/\&lt\;\&gt\;\1\&lt\;\/\&gt\;/g;
$ecomment =~ s/<br>/\n/g;

foreach $oktag (@oktag) {
	$ecomment =~ s/<${oktag}>(.*?)<\/${oktag}>/\&lt\;${oktag}\&gt\;\1\&lt\;\/${oktag}\&gt\;/g;
}
if($Fm{'dmode'} eq 'edit') {
print<<END;
<br>
<blockquote>
END
if($upbbs == 1) {
print<<END;
<form action="$script" method="POST" ENCTYPE="multipart/form-data" style="display:inline;">
END
} else {
print<<END;
<form action="$script" method="POST" style="display:inline;">
END
}
print<<END;
- ãLéñï“èW -
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="no" value="$Fm{'no'}">
<input type="hidden" name="rno" value="$lrno">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
<table summary="ï\\" border="0" cellspacing="0" cellpadding="0">
<tr><th align="left"><small>Ç®Ç»Ç‹Ç¶</small></th><td><input type="text" size="20" name="name" value="$lname"></td>
<tr><th align="left"><small>ÇdÉÅÅ[Éã</small></th><td><input type="text" size="20" name="mail" value="$lmail"></td>
<tr><th align="left"><small>É^ÉCÉgÉã</small></th><td><input type="text" size="30" name="title" value="$ltitle"> <input type="submit" value="ëóêMÇ∑ÇÈ"><input type="reset" value="ÉäÉZÉbÉg" onClick="if(!confirm('ñ{ìñÇ…ÉäÉZÉbÉgÇµÇ‹Ç∑ÅB\\nì‡óeÇ™ëSÇƒè¡Ç¶Ç‹Ç∑ÅB\\nÅEÅEÅEÇªÇÍÇ≈Ç‡ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;" onKeyPress=""></td>
<tr><th colspan="2" align="left"><small>ÉÅÉbÉZÅ[ÉW</small></th>
<tr><td colspan="2"><textarea cols="70" rows="7" name="comment" wrap="off">$ecomment</textarea></td>
<tr><th align="left"><small>ÇtÇqÇk</small></th><td><input type="text" size="40" name="hp" value="$lhp"></td>
END
if($iconon == 1) {
print<<END;
<tr><th align="left"><small>ÉCÉÅÅ[ÉW</small></th><td><select name="icon">
END
$iconcount = 0;
foreach $tmpicon (@icon) {
($tmpiconaddr,$tmpiconname) = split(/\,/,$tmpicon);
if($tmpiconaddr eq 'special') {
$spwflag = 0;
foreach $spicon (@spicon) {
($spwpass,$spwicon) = split(/\,/,$spicon);
if($licon eq $spwicon) {
$spwflag = 1;
last;
}
}
$selected = ($spwflag == 1) ? ' selected' : '';
} else {
if($licon ne '') { $selected = ($licon eq $tmpiconaddr) ? ' selected' : ''; } else { $selected = ($iconcount == 0) ? ' selected' : ''; }
}
print"<option value=\"$iconcount\"${selected}>$tmpiconname</option>\n";
$iconcount++;
}
print<<END;
</select></td>
END
}
print<<END;
<tr><th align="left"><small>ÉpÉXÉèÅ[Éh</small></th><td><input type="password" size="10" name="newpass" value="$Fm{'pass'}"><small>(ãLéñÇÃÉÅÉìÉeéûÇ…égópÅBîºäpâpêîéöÇ≈8éöà»ì‡)</small></td>
<tr><th align="left"><small>ï∂éöêF</small></th><td>
END
$colorcount = 0;
foreach $tmpcolor (@color) {
if($lcolor ne '') { $checked = ($lcolor eq $tmpcolor) ? ' checked' : ''; } else { $checked = ($colorcount == 0) ? ' checked' : ''; }
print"<input type=\"radio\" name=\"color\" value=\"$colorcount\"${checked}><font color=\"$tmpcolor\" size=\"-1\">Å°</font>&nbsp;\n";
print"<br>\n" if($colorcount % 7 == 6);
$colorcount++;
}
print<<END;
</td></tr>
END
if($upbbs == 1) {
print<<END;
<tr><th align="left"><small>ìYïtÉtÉ@ÉCÉã</small></th><td><input type="file" size="20" name="file"> <small>(<a style="color:#0000FF;cursor:hand;" onClick="alert('${maxup}BytesÇ‹Ç≈\\n\\nägí£éqÇ™\\n${upexplist}\\nÇÃÉtÉ@ÉCÉã');">ÉAÉbÉvÉçÅ[Éhâ¬î\\ÉtÉ@ÉCÉã</a>)</small></td></tr>
END
if($lfile ne '') {
print<<END;
<tr><th align="left"><small>ÉtÉ@ÉCÉãçÌèú</small></th><td><input type="checkbox" name="filedel" value="filedel"></td></tr>
END
}
}
print<<END;
</table>
</form>
</blockquote>
END
} elsif($Fm{'dmode'} eq 'delete') {
print<<END;
<br><br>
<form action="$script" method="POST" style="display:inline;">
<input type="hidden" name="mode" value="$Fm{'dmode'}">
<input type="hidden" name="no" value="$Fm{'no'}">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
Ç±ÇÃãLéñÇ <input type="submit" value="í èÌçÌèúÇ∑ÇÈ">
</form>
END
}
} elsif($find == 2) {
print<<END;
ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB
END
} else {
print<<END;
äYìñÇÃãLéñÇ™å©Ç¬Ç©ÇËÇ‹ÇπÇÒÇ≈ÇµÇΩÅB<br>
ãLéñî‘çÜÇ™ä‘à·Ç¡ÇƒÇ¢ÇÈâ¬î\\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB
END
}
} elsif($Fm{'dmode'} eq 'move') {
$find = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
$cpass = $lpass if(($adminflag == 1) && ($lno eq $Fm{'no'}));
$plpass = $lpass if($lrno eq '');
&jumper;
if(($lno eq $Fm{'no'}) && ($lpass ne $cpass)) { $find = 2; last; }
elsif((($lno eq $Fm{'no'}) && ($lrno eq '') && ($Fm{'mno'} eq '')) 	||
(($lno eq $Fm{'no'}) && ($lrno eq '') && ($Fm{'no'} eq $Fm{'mno'})))	{ $find = 3; last; }
elsif((($lno eq $Fm{'no'}) && ($plpass eq $cpass))	||
(($lno eq $Fm{'no'}) && ($lpass eq $cpass))		||
(($lrno eq $Fm{'no'}) && ($plpass eq $cpass))		||
(($lno eq $Fm{'no'}) && ($adminflag == 1))		||
(($lrno eq $Fm{'no'}) && ($adminflag == 1)))		{
&quotation;
$print .= <<END;
<hr><b>$ltitle</b> ìäçeé“ÅF<b>$lname</b>Ç≥ÇÒ - <small>$ltime</small> <font color="#888800" size="-1">No.$lno</font>
<blockquote><font color="$lcolor">$lcomment</font></blockquote>
END
$find = 1;
}
}

$mfind = 0;
if($Fm{'mno'} eq '') {
$mfind = 1;
} else {
$mprint = '';
$mfind = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
&jumper;
if(($lno eq $Fm{'mno'}) && ($lrno ne '')) { $mfind = 0; last; }
elsif(($lno eq $Fm{'mno'})		||
($lrno eq $Fm{'mno'}))		{
&quotation;
$mprint .= <<END;
<hr><b>$ltitle</b> ìäçeé“ÅF<b>$lname</b>Ç≥ÇÒ - <small>$ltime</small> <font color="#888800" size="-1">No.$lno</font>
<blockquote><font color="$lcolor">$lcomment</font></blockquote>
END
$mfind = 1;
}
}
}
$Fm{'pass'} = $tmppass if($adminflag == 1);
if($mfind == 0) {
print<<END;
à⁄ìÆêÊÇÃÉXÉåÉbÉhÇ™å©Ç¬Ç©ÇËÇ‹ÇπÇÒÇ≈ÇµÇΩÅB<br>
èÆÅAéqãLéñÇ…ãLéñÇà⁄ìÆÇ∑ÇÈÇ±Ç∆ÇÕïsâ¬î\\Ç≈Ç∑ÅB
END
} elsif($find == 1) {
print<<END;
<small>ãLéñNo.$Fm{'no'} ÇÃà⁄ìÆÉtÉHÅ[ÉÄÇ≈Ç∑ÅB[<a href="$script?id=$Fm{'id'}" onClick="if(!confirm('à⁄ìÆÇé~ÇﬂÇƒñﬂÇËÇ‹Ç∑Ç©ÅH')) return false;" onKeyPress="">ñﬂÇÈ</a>]</small><br><br>
<div align="center">
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
$print
<hr></td></table><br>
END
if($Fm{'mno'} eq '') {
print<<END;
ÇÅAêVÉXÉåÉbÉhÇ…
END
} else {
print<<END;
ÇÅA<br>
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
$mprint
<hr></td></table><br>
Ç…
END
}
print<<END;
<br><br>
<form action="$script" method="POST" style="display:inline;">
<input type="hidden" name="mode" value="$Fm{'dmode'}">
<input type="hidden" name="no" value="$Fm{'no'}">
<input type="hidden" name="mno" value="$Fm{'mno'}">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="submit" value="à⁄ìÆÇ∑ÇÈ">
</form>
END
} elsif($find == 2) {
print<<END;
ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB
END
} elsif($find == 3) {
print<<END;
ÉXÉåÉbÉhÇÅAêVÉXÉåÉbÉhÇ…Ç∑ÇÈÇ±Ç∆ÇÕÇ≈Ç´Ç‹ÇπÇÒÅB<br>
Ç‹ÇΩÅAÉXÉåÉbÉhNo.Ç∆à⁄ìÆêÊNo.ÇìØÇ∂Ç…Ç∑ÇÈÇ±Ç∆Ç‡Ç≈Ç´Ç‹ÇπÇÒÅB
END
} else {
print<<END;
äYìñÇÃãLéñÇ™å©Ç¬Ç©ÇËÇ‹ÇπÇÒÇ≈ÇµÇΩÅB<br>
ãLéñî‘çÜÇ™ä‘à·Ç¡ÇƒÇ¢ÇÈâ¬î\\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB
END
}
} elsif($Fm{'dmode'} eq 'pdelete') {
print<<END;
<small>ãLéñNo.$Fm{'no'} ÇÃçÌèúÉtÉHÅ[ÉÄÇ≈Ç∑ÅB[<a href="$script?id=$Fm{'id'}" onClick="if(!confirm('ï“èWÅEçÌèúÇé~ÇﬂÇƒñﬂÇËÇ‹Ç∑Ç©ÅH')) return false;" onKeyPress="">ñﬂÇÈ</a>]</small><br><br>
<div align="center">
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
END
$find = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
$ecomment = $lcomment;
$plpass = $lpass if($lrno eq '');
&jumper;
if(($lno eq $Fm{'no'}) && ($lpass ne $cpass)) { $find = 2; last; }
elsif((($lno eq $Fm{'no'}) && ($plpass eq $cpass))	||
(($lno eq $Fm{'no'}) && ($lpass eq $cpass))		||
(($lrno eq $Fm{'no'}) && ($plpass eq $cpass))		||
(($lno eq $Fm{'no'}) && ($adminflag == 1))		||
(($lrno eq $Fm{'no'}) && ($adminflag == 1)))		{
&quotation;
print<<END;
<hr><b>$ltitle</b> ìäçeé“ÅF<b>$lname</b>Ç≥ÇÒ - <small>$ltime</small> <font color="#888800" size="-1">No.$lno</font>
<blockquote><font color="$lcolor">$lcomment</font></blockquote>
END
$find = 1;
}
}
print<<END;
<hr></td></table><br>
END
$Fm{'pass'} = $tmppass if($adminflag == 1);
if($find == 1) {
print<<END;
<br><br>
<form action="$script" method="POST" style="display:inline;">
<input type="hidden" name="mode" value="$Fm{'dmode'}">
<input type="hidden" name="no" value="$Fm{'no'}">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
Ç±ÇÃãLéñÇ <input type="submit" value="äÆëSçÌèúÇ∑ÇÈ">
</form>
END
} elsif($find == 2) {
print<<END;
ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB
END
} else {
print<<END;
äYìñÇÃãLéñÇ™å©Ç¬Ç©ÇËÇ‹ÇπÇÒÇ≈ÇµÇΩÅB<br>
ãLéñî‘çÜÇ™ä‘à·Ç¡ÇƒÇ¢ÇÈâ¬î\\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB
END
}

}
print<<END;
</div>
END
&footer;
print<<END;
</body>
</html>
END
} else {
&error('ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB');
}
}



sub edit {
&proxy if($proxyok == 1);
if($Fm{'pass'} ne '') {
&error('ïsê≥Ç»ìäçeÇ≈Ç∑ÅB') if(($ENV{'HTTP_REFERER'} !~ /^$reff/) && ($ENV{'HTTP_REFERER'} ne ''));
$Fm{'name'} = 'ñºñ≥Çµ' if($Fm{'name'} eq '');
$Fm{'hp'} = '' if($Fm{'hp'} eq 'http://');
@returncount = split(/<br>/,$Fm{'comment'});
$fileexp = $1 if(($Fm{'file'} =~ /.*\.(.*)/) && ($upbbs == 1));
if($Fm{'title'} eq '') {
&error('É^ÉCÉgÉãÇ™Ç†ÇËÇ‹ÇπÇÒÅB');
} elsif($Fm{'comment'} eq '') {
&error('ÉÅÉbÉZÅ[ÉWÇ™Ç†ÇËÇ‹ÇπÇÒÅB');
} elsif(length($Fm{'name'}) > $maxnam) {
$tmplength = length($Fm{'name'});
&error("Ç®Ç»Ç‹Ç¶Ç™í∑Ç∑Ç¨Ç‹Ç∑ÅB<br>${maxnam}Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif(length($Fm{'mail'}) > $maxmai) {
$tmplength = length($Fm{'mail'});
&error("ÇdÉÅÅ[ÉãÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB<br>${maxmai}Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif(length($Fm{'hp'}) > $maxhpa) {
$tmplength = length($Fm{'hp'});
&error("ÉzÅ[ÉÄÉyÅ[ÉWÉAÉhÉåÉXÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB<br>${maxhpa}Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif(length($Fm{'title'}) > $maxtit) {
$tmplength = length($Fm{'title'});
&error("É^ÉCÉgÉãÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB<br>${maxtit}Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif(length($Fm{'newpass'}) > 8) {
$tmplength = length($Fm{'newpass'});
&error("ÉpÉXÉèÅ[ÉhÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB<br>8Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif((length($Fm{'comment'}) < $minmsg) && ($Fm{'rno'} eq '')) {
$tmplength = length($Fm{'comment'});
&error("ÉÅÉbÉZÅ[ÉWÇ™è≠Ç»Ç∑Ç¨Ç‹Ç∑ÅB<br>ÉXÉåÉbÉhÇÃêeãLéñÇï“èWÇ∑ÇÈèÍçáÇÕÅA${minmsg}Bytesà»è„Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif(length($Fm{'comment'}) > $maxmsg) {
$tmplength = length($Fm{'comment'});
&error("ÉÅÉbÉZÅ[ÉWÇ™ëΩÇ∑Ç¨Ç‹Ç∑ÅB<br>${maxmsg}Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif(@returncount < $minret) {
$tmplength = @returncount;
&error("â¸çsÇ™è≠Ç»Ç∑Ç¨Ç‹Ç∑ÅB<br>${minret}âÒà»è„Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>âÒ)");
} elsif(@returncount > $maxret) {
$tmplength = @returncount;
&error("â¸çsÇ™ëΩÇ∑Ç¨Ç‹Ç∑ÅB<br>${maxret}âÒà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>âÒ)");
} elsif((expcheck($fileexp) == 0) && ($upbbs == 1) && ($Fm{'file'} ne '')) {
&error("ÉAÉbÉvÉçÅ[ÉhÇ≈Ç´Ç»Ç¢É^ÉCÉvÇÃÉtÉ@ÉCÉãÇ≈Ç∑ÅB");
} elsif((length($Cn{'file'}) > $maxup) && ($upbbs == 1)) {
&error("ÉAÉbÉvÉçÅ[ÉhÇ∑ÇÈÉtÉ@ÉCÉãÇ™ëÂÇ´Ç∑Ç¨Ç‹Ç∑ÅB<br>${maxup}Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>".length($Cn{'file'})."</b>Bytes)");
}

$adminflag = 0;
foreach $adpass (@adpass) {
if($Fm{'pass'} eq $adpass) {
$adminflag = 1;
last;
}

}

$wicon = $icon[$Fm{'icon'}];
($wiconaddr,$wiconname) = split(/\,/,$wicon);
&spicon;

$wcolor = $color[$Fm{'color'}];

$cpass = crypt($Fm{'pass'},$crp);
$ncpass = crypt($Fm{'newpass'},$crp);
&gettime;

&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);

foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
$cpass = $lpass if($adminflag == 1);
if(($lno eq $Fm{'no'}) && ($lpass eq $cpass)) {
if($Fm{'file'} eq '') {
if($Fm{'filedel'} eq 'filedel') {
$rfile = '';
} else {
$rfile = $lfile;
}
} else {
$rfile = "$lno\.$fileexp";
}
$tmplog = "$lno<>$lrno<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>$Fm{'name'}<>$Fm{'mail'}<>$Fm{'title'}<>$Fm{'comment'}<>$Fm{'hp'}<>$ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},$lcount,$rfile<>$ncpass<>$wcolor<>$wiconaddr<>\n";
unlink("$uploaddir/$uploadid$lfile") if(($upbbs == 1) && ((($lfile ne '') && ($Fm{'filedel'} eq 'filedel')) || ($Fm{'file'} ne '')));
last;
}
}
open(LOG,"> $multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print LOG @log;
close(LOG);
if(($upbbs == 1) && ($Fm{'file'} ne '')) {
open(ULF,"> $uploaddir/$uploadid$lno\.$fileexp") or &error("ìYïtÉtÉ@ÉCÉãÅF${uploaddir}/$uploadid$lno\.$fileexp Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
binmode(ULF);
print ULF $Cn{'file'};
close(ULF);
chmod("$uploaddir/$uploadid$lno\.$fileexp", 0666);
}
&unlock;
&pagemove("$script?id=$Fm{'id'}");
} else {
&error('ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB');
}
}

sub move {
&proxy if($proxyok == 1);
if($Fm{'pass'} ne '') {
&error('ïsê≥Ç»ìäçeÇ≈Ç∑ÅB') if(($ENV{'HTTP_REFERER'} !~ /^$reff/) && ($ENV{'HTTP_REFERER'} ne ''));
$adminflag = 0;
foreach $adpass (@adpass) {
if($Fm{'pass'} eq $adpass) {
$adminflag = 1;
last;
}

}
&gettime;
&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);

$tlog = '';
$cpass = crypt($Fm{'pass'},$crp);
$find = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
$cpass = $lpass if($adminflag == 1);
$plpass = $lpass if($lrno eq '');
if(($lno eq $Fm{'no'}) && ($lpass ne $cpass)) { last; }
elsif((($lno eq $Fm{'no'}) && ($plpass eq $cpass))	||
(($lno eq $Fm{'no'}) && ($lpass eq $cpass))		||
(($lrno eq $Fm{'no'}) && ($plpass eq $cpass))		||
(($lno eq $Fm{'no'}) && ($adminflag == 1))		||
(($lrno eq $Fm{'no'}) && ($adminflag == 1)))		{
$tlrno = ($Fm{'mno'} eq '') ? '' : $Fm{'mno'};
$tlog .= "$lno<>$tlrno<>$ltime<>$lname<>$lmail<>$ltitle<>$lcomment<>$lhp<>$lhost<>$lpass<>$lcolor<>$licon<>\n";
$tmplog = '';
$find = 1;
}
}

if($find == 1) {
$okflag = 0;
$findflag = 0;
if($Fm{'mno'} eq '') {
$tempcount = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
$tempcount++ if($lrno eq '');
if($tempcount >= $maxthr) {
$tmplog = '';
}
}
unshift(@log,$tlog);
$okflag = 1;
} else {
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
if(($Fm{'mno'} eq $lno) && ($lrno ne '')) { last; }
if(($lrno eq '') && ($findflag == 1)) {
$tmplog = $tlog . $tmplog;
$okflag = 1;
$findflag = 0;
last;
}
if(($lno eq $Fm{'mno'}) || ($lrno eq $Fm{'mno'})) {
$findflag = 1;
} else {
$findflag = 0;
}

}
if($findflag == 1) {
push(@log,$tlog);
$okflag = 1;
}
}
if($okflag == 1) {
open(LOG,"> $multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print LOG @log;
close(LOG);
}
}
&unlock;
&pagemove("$script?id=$Fm{'id'}");
} else {
&error('ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB');
}
}

sub delete {
&proxy if($proxyok == 1);
if($Fm{'pass'} ne '') {
&error('ïsê≥Ç»ìäçeÇ≈Ç∑ÅB') if(($ENV{'HTTP_REFERER'} !~ /^$reff/) && ($ENV{'HTTP_REFERER'} ne ''));
$adminflag = 0;
foreach $adpass (@adpass) {
if($Fm{'pass'} eq $adpass) {
$adminflag = 1;
last;
}

}
&gettime;
&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
$cpass = crypt($Fm{'pass'},$crp);
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
if((($lno eq $Fm{'no'}) && ($lpass eq $cpass)) || (($lno eq $Fm{'no'}) && ($adminflag == 1))) {
$tmplog = "$lno<>$lrno<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>Deleted<><>çÌèúÇ≥ÇÍÇ‹ÇµÇΩÅB<>Ç±ÇÃãLéñÇÕçÌèúÇ≥ÇÍÇ‹ÇµÇΩÅB<><>$ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},0,<>$lpass<>#000000<><>\n";
unlink("$uploaddir/$uploadid$lfile") if(($upbbs == 1) && ($lfile ne ''));
last;
}
}
open(LOG,"> $multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print LOG @log;
close(LOG);
&unlock;
&pagemove("$script?id=$Fm{'id'}");
} else {
&error('ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB');
}
}

sub pdelete {
&proxy if($proxyok == 1);
if($Fm{'pass'} ne '') {
&error('ïsê≥Ç»ìäçeÇ≈Ç∑ÅB') if(($ENV{'HTTP_REFERER'} !~ /^$reff/) && ($ENV{'HTTP_REFERER'} ne ''));
$adminflag = 0;
foreach $adpass (@adpass) {
if($Fm{'pass'} eq $adpass) {
$adminflag = 1;
last;
}

}
&gettime;
&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
$dflag = 0;
$cpass = crypt($Fm{'pass'},$crp);
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
$plpass = $lpass if($lrno eq '');
if((($lno eq $Fm{'no'}) && ($lpass eq $cpass))	||
(($lrno eq $Fm{'no'}) && ($plpass eq $cpass))	||
(($lno eq $Fm{'no'}) && ($adminflag == 1))	||
(($lrno eq $Fm{'no'}) && ($adminflag == 1)))	{
$tmplog = '';
unlink("$uploaddir/$uploadid$lfile") if(($upbbs == 1) && ($lfile ne ''));
}
}
open(LOG,"> $multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print LOG @log;
close(LOG);
&unlock;
&pagemove("$script?id=$Fm{'id'}");
} else {
&error('ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB');
}
}

1;
