sub admin {
if($Fm{'pass'} eq '') {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ä«óùÉÇÅ[Éh Å| ${title}</title>
</head>
<body>
<div align="center">
<font size="6" color="#0000ff">ä«óùÉÇÅ[Éh</font><br><br>
<form action="$action" method="POST" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="admin">
<input type="password" size="20" name="pass" value=""><input type="submit" value="îFèÿ">
</form>
<br><br>
<a href="$script?id=$Fm{'id'}">ñﬂÇÈ</a>
</div>
END
&footer;
print<<END;
</body>
</html>
END
} else {
$adminflag = 0;
foreach $adpass (@adpass) {
if($Fm{'pass'} eq $adpass) {
$adminflag = 1;
last;
}

}

if($adminflag == 1) {
if($Fm{'subm'} eq 'delete') {
$Fm{'page'} -= 1 if($Fm{'page'} > 0);
open(LOG,"${multif}${log}") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ãLéñä«óù Å| ${title}</title>
</head>
<body>
<a href="$script?id=$Fm{'id'}&amp;mode=admin&amp;pass=$Fm{'pass'}">ñﬂÇÈ</a>
<form action="$action" method="GET" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="subm" value="deletep">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<div align="center">
<font size="6" color="#0000ff">ãLéñä«óù</font><br><br>
<select name="dmode"><option value="n" selected>í èÌ</option><option value="p">äÆëS</option></select>ÉÇÅ[ÉhÇ≈ÅA<input type="submit" value="çÌèúÇ∑ÇÈ">
<br><br>
<table summary="ï\\" border="0" width="90%" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>çÌèú</td><td>ëËñº</td><td>ìäçeé“</td><td>ì‡óe</td><td>HP</td><td>ìäçeì˙</td><td>IPÅEHOST</td><tr>
END
$threadcount = -1;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
$threadcount++ if($lrno eq '');
if(($Fm{'page'} * $onep <= $threadcount) && ($Fm{'page'} * $onep + $onep > $threadcount)) {
if($lcomment =~ /^.*?<br>.*?<br>.*?<br>.*/) {
$lcomment =~ s/(.*?<br>.*?<br>.*?)<br>.*/\1\.\.\./;
}
$lcomment =~ s/((?:http|https|ftp|news)\:\/\/[\w\/\.\~\-\_\?\&\+\=\#\@\:\;]+)/<a href="$script?mode=check&amp;uri=\1" target="_blank">\1<\/a>/g;
$lname = ($lmail ne '') ? "<a href=\"mailto:$lmail\">$lname</a>" : $lname;
$tmphp = ($lhp ne '') ? "[<a href=\"$lhp\" target=\"_blank\">Home</a>]" : "-";
($raddr,$rhost,$lcount) = split(/\,/,$lhost);
if($lrno eq '') { print"<tr><td colspan=\"7\"><hr></td></tr>\n"; }
print<<END;
<tr align="left" valign="top"><td><input type="checkbox" name="r${lno}" value="${lno}"></td><td><small>No.$lno <b>$ltitle</b></small></td><td><small><b>$lname</b>Ç≥ÇÒ</small></td><td><small>$lcomment</small></td><td><small>$tmphp</small></td><td><small>$ltime</small></td><td><small>IP:$raddr HOST:$rhost</small></td></tr>
END
}

}
print<<END;
<tr><td colspan="7"><hr><div align="center">
END
$logcount = int(($threadcount - 1) / $onep) + 1;
$Fm{'page'}++;
$tmpp = $Fm{'page'} - 1;
if($Fm{'page'} > 1) { print"<a href=\"$script?id=$Fm{'id'}&amp;mode=admin&amp;pass=$Fm{'pass'}&amp;subm=delete&amp;page=$tmpp\">Å©ëOÇÃÉyÅ[ÉW</a> "; } else { print"Å©ëOÇÃÉyÅ[ÉW "; }
for($i=1;$i<=$logcount;$i++) {
if($i eq $Fm{'page'}) {
print"[<b>$i</b>] ";
} else {
print"[<a href=\"$script?id=$Fm{'id'}&amp;mode=admin&amp;pass=$Fm{'pass'}&amp;subm=delete&amp;page=${i}\">${i}</a>] ";
}
}
$tmpp = $Fm{'page'} + 1;
if(($Fm{'page'} * $onep) < $threadcount) { print"<a href=\"$script?id=$Fm{'id'}&amp;mode=admin&amp;pass=$Fm{'pass'}&amp;subm=delete&amp;page=$tmpp\">éüÇÃÉyÅ[ÉWÅ®</a>"; } else { print"éüÇÃÉyÅ[ÉWÅ®"; }
print<<END;
</div></td></tr>
</table>
</td>
</table>
</div>
</form>
<br><br>
<a href="$script?id=$Fm{'id'}&amp;mode=admin&amp;pass=$Fm{'pass'}">ñﬂÇÈ</a>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'deletep') {
&error('ïsê≥Ç»ìäçeÇ≈Ç∑ÅB') if(($ENV{'HTTP_REFERER'} !~ /^$reff/) && ($ENV{'HTTP_REFERER'} ne ''));
$cpass = crypt($Fm{'pass'},$crp);
&gettime;
&lock;
open(LOG,"${multif}${log}") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
if($Fm{'dmode'} eq 'n') {
if($lno eq $Fm{"r${lno}"}) {
$tmplog = "$lno<>$lrno<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>Deleted<><>çÌèúÇ≥ÇÍÇ‹ÇµÇΩÅB<>Ç±ÇÃãLéñÇÕçÌèúÇ≥ÇÍÇ‹ÇµÇΩÅB<><>$ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'}<><>#000000<><>\n";
unlink("$uploaddir/$uploadid$lfile") if(($upbbs == 1) && ($lfile ne ''));
}
} else {
if(($lno eq $Fm{"r${lno}"}) || (($lrno eq $Fm{"r${lrno}"}) && ($Fm{"r${lrno}"} ne ''))) {
$tmplog = '';
unlink("$uploaddir/$uploadid$lfile") if(($upbbs == 1) && ($lfile ne ''));
}
}
}
open(LOG,"> ${multif}${log}") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print LOG @log;
close(LOG);
&unlock;
&pagemove("$script?id=$Fm{'id'}&mode=admin&subm=delete&pass=$Fm{'pass'}");
} elsif($Fm{'subm'} eq 'ipban') {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ÉAÉNÉZÉXãKêß Å| ${title}</title>
</head>
<body>
<div align="center">
<font size="6" color="#0000ff">ÉAÉNÉZÉXãKêß</font><br><br>
<form action="$action" method="POST" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="subm" value="ipbanp">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<textarea name="ipb" cols="80" rows="10" wrap="off">
END
foreach $tipb (@ipb) {
print"${tipb}\n";
}
print<<END;
</textarea><br>
<input type="submit" value="ïœçXÇ∑ÇÈ">
</form>
<br><br>
<a href="$script?id=$Fm{'id'}&amp;mode=admin&amp;pass=$Fm{'pass'}">ñﬂÇÈ</a>
</div>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'ipbanp') {
&lock;
open(IPB,"> ${multif}$ipban") or &error("ÉAÉNÉZÉXãKêßÉfÅ[É^ÅF${multif}${ipban} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print IPB $Fm{'ipb'};
close(IPB);
&unlock;
&pagemove("$script?id=$Fm{'id'}&mode=admin&subm=ipban&pass=$Fm{'pass'}");
} else {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ä«óùÉÅÉjÉÖÅ[ Å| ${title}</title>
</head>
<body>
<div align="center">
<font size="6" color="#0000ff">ä«óùÉÅÉjÉÖÅ[</font><br><br>
<form action="$action" method="GET" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<select name="subm">
<option value="delete" selected>ãLéñä«óùçÌèú</option>
<option value="ipban">ÉAÉNÉZÉXãKêß</option>
</select><input type="submit" value="é¿çs">
</form>
<br><br>
<a href="$script?id=$Fm{'id'}">ñﬂÇÈ</a>
</div>
END
&footer;
print<<END;
</body>
</html>
END
}
} else {
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB');
}

}
}

1;
