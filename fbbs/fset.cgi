sub setup {
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
<font size="6" color="#0000ff">åfé¶î¬ê›íËÉÇÅ[Éh</font><br><br>
<form action="$action" method="POST" style="display:inline;">
<input type="hidden" name="mode" value="setup">
<input type="password" size="20" name="pass" value=""><input type="submit" value="îFèÿ">
</form>
</div>
END
&footer;
print<<END;
</body>
</html>
END
} else {

if($Fm{'pass'} eq $setpass) {


if($Fm{'subm'} eq 'edit') {
if(((-e "${setupdir}/$Fm{'id'}") && ($Fm{'id'} ne '') && ($Fm{'edit'} eq 'edit')) || ((!-e "${setupdir}/$Fm{'id'}") && ($Fm{'edit'} ne 'edit'))) {
if($Fm{'edit'} eq 'edit') {
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbstopcom");
@etopcom = <FILE>;
close(FILE);
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbsstyle");
@estyle = <FILE>;
close(FILE);
$etopcom = '';
foreach $tmpetopcom (@etopcom) {
$tmpetopcom =~ s/\&/\&amp\;/g;
$tmpetopcom =~ s/</\&lt\;/g;
$tmpetopcom =~ s/>/\&gt\;/g;
$tmpetopcom =~ s/\"/\&quot\;/g;
$etopcom .= $tmpetopcom;
}
$estyle = '';
foreach $tmpestyle (@estyle) {
$tmpestyle =~ s/\&/\&amp\;/g;
$tmpestyle =~ s/</\&lt\;/g;
$tmpestyle =~ s/>/\&gt\;/g;
$tmpestyle =~ s/\"/\&quot\;/g;
$estyle .= $tmpestyle;
}
} else {
$etitle = $title;
$etopon = $topon;

$etcolor = $tcolor;
$etitlei = $titlei;
$eadname = $adname;
$eadmail = $admail;
$eimgdir = $imgdir;
$ebackpa = $backpa;
$ebackpn = $backpn;
$eupbbs = $upbbs;
$espicon = join(':',@spicon);
$eicon = join(':',@icon);
$ecolor = join(':',@color);
$eadpass = join(':',@adpass);

$etopcom = $topcom;
$estyle = $style;

$eeditpass = $setpass;
}
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>åfé¶î¬ê›íË - ${title}</title>
</head>
<body>
<font size="$tsize" color="$tcolor">åfé¶î¬ê›íË</font><br><br>
END
if($Fm{'edit'} eq 'edit') {
print"åfé¶î¬ID.$Fm{'id'} ÇÃï“èW<br>\n";
} else {
print"åfé¶î¬ID.$Fm{'id'} ÇÃêVãKçÏê¨<br>\n";
}
print<<END;
<form action="$script" method="POST" onSubmit="if(!confirm('ñ{ìñÇ…ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;">
<input type="hidden" name="mode" value="setup">
<input type="hidden" name="subm" value="editp">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="edit" value="$Fm{'edit'}">
<input type="hidden" name="id" value="$Fm{'id'}">
<table summary="ï\\" border="1" cellspacing="0" cellpadding="0">
<tr><td>É^ÉCÉgÉã</td><td><input type="text" size="32" name="title" value="$etitle"></td></tr>
<tr><td>É^ÉCÉgÉãÇÃêF</td><td><input type="text" size="32" name="tcolor" value="$etcolor"></td></tr>
<tr><td>É^ÉCÉgÉãâÊëú</td><td><input type="text" size="32" name="titlei" value="$etitlei"></td></tr>
<tr><td>ä«óùé“ñº</td><td><input type="text" size="32" name="adname" value="$eadname"></td></tr>
<tr><td>ä«óùé“ÉÅÅ[ÉãÉAÉhÉåÉX</td><td><input type="text" size="32" name="admail" value="$eadmail"></td></tr>
<tr><td>âÊëúÇÃÇ†ÇÈÉAÉhÉåÉX</td><td><input type="text" size="64" name="imgdir" value="$eimgdir"></td></tr>
<tr><td>ñﬂÇËêÊÇÃÉyÅ[ÉW</td><td><input type="text" size="64" name="backpa" value="$ebackpa"></td></tr>
<tr><td>ñﬂÇËêÊÇÃÉyÅ[ÉWñº</td><td><input type="text" size="64" name="backpn" value="$ebackpn"></td></tr>
<tr><td>ÉAÉbÉvÉçÅ[Éhã@î\\</td><td>
END
print"égÇÌÇ»Ç¢ <input type=\"radio\" name=\"upbbs\" value=\"0\"";
if($eupbbs == 0) { print" checked"; }
print"><br>\n";
print"égÇ§ <input type=\"radio\" name=\"upbbs\" value=\"1\"";
if($eupbbs == 1) { print" checked"; }
print">\n";
print<<END;
</td></tr>
<tr><td><a href="#" onClick="alert('ÉpÉXÉèÅ[Éh,ÉAÉCÉRÉìÇÃÉAÉhÉåÉX\\nÉpÉXÉèÅ[Éh,ÉAÉCÉRÉìÇÃÉAÉhÉåÉX\\nÉpÉXÉèÅ[Éh,ÉAÉCÉRÉìÇÃÉAÉhÉåÉX\\nÅEÅEÅE\\n\\nÇ∆â]Ç¡ÇΩä¥Ç∂Ç≈ê›íËÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB');return false;">êÍópÉAÉCÉRÉì</a></td><td><textarea cols="80" rows="4" name="spicon">
$espicon</textarea></td></tr>
<tr><td><a href="#" onClick="alert('ÉAÉCÉRÉìÇÃÉAÉhÉåÉX,ÉAÉCÉRÉìñº\\nÉAÉCÉRÉìÇÃÉAÉhÉåÉX,ÉAÉCÉRÉìñº\\nÉAÉCÉRÉìÇÃÉAÉhÉåÉX,ÉAÉCÉRÉìñº\\nÅEÅEÅE\\n\\nÇ∆â]Ç¡ÇΩä¥Ç∂Ç≈ê›íËÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB');return false;">ÉAÉCÉRÉì</a></td><td><textarea cols="80" rows="4" name="icon">
$eicon</textarea></td></tr>
<tr><td><a href="#" onClick="alert('ï∂éöêF\\nï∂éöêF\\nï∂éöêF\\nÅEÅEÅE\\n\\nÇ∆â]Ç¡ÇΩä¥Ç∂Ç≈ê›íËÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB');return false;">ï∂éöêF</a></td><td><textarea name="color" cols="80" rows="5" wrap="off">
$ecolor</textarea>
<tr><td><a href="#" onClick="alert('ä«óùópÉpÉXÉèÅ[Éh\\nä«óùópÉpÉXÉèÅ[Éh\\nä«óùópÉpÉXÉèÅ[Éh\\nÅEÅEÅE\\n\\nÇ∆â]Ç¡ÇΩä¥Ç∂Ç≈ê›íËÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB');return false;">ä«óùópÉpÉXÉèÅ[Éh</a></td><td><textarea name="adpass" cols="80" rows="5" wrap="off">
$eadpass</textarea>
<tr><td>ÉgÉbÉvÇ…ÉRÉÅÉìÉgÇç⁄ÇπÇÈÇ©</td><td>
END
print"ç⁄ÇπÇ»Ç¢ <input type=\"radio\" name=\"topon\" value=\"0\"";
if($etopon == 0) { print" checked"; }
print"><br>\n";
print"ç⁄ÇπÇÈ <input type=\"radio\" name=\"topon\" value=\"1\"";
if($etopon == 1) { print" checked"; }
print">\n";
print<<END;
</td></tr>
<tr><td>ÉgÉbÉvÇÃÉRÉÅÉìÉg</td><td><textarea name="topcom" cols="80" rows="5" wrap="off">
$etopcom</textarea>
</td></tr>
<tr><td>ÉXÉ^ÉCÉãÉVÅ[Ég</td><td><textarea name="style" cols="80" rows="5" wrap="off">
$estyle</textarea></td></tr>
<tr><td>åfé¶î¬ê›íËÉpÉX</td><td><input type="password" size="20" name="editpass" value="$eeditpass"></td></tr>
<tr><td>è„ãLÉpÉXÇÃämîF</td><td><input type="password" size="20" name="checkpass" value="$eeditpass"></td></tr>
<tr><td colspan="2"><input type="submit" value="ï“èWäÆóπ"> <input type="button" value="Ç‚Ç¡Çœé~ÇﬂÇÈ" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script?mode=setup&amp;pass=$Fm{'pass'}';" onKeyPress=""></td></tr>
</table>
END
&footer;
print<<END;
</body>
</html>
END
} else {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ÉGÉâÅ[ - ${title}</title>
</head>
<body>
åfé¶î¬ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç»Ç¢ÅA<br>
ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>
Ç‹ÇΩÅAêVãKçÏê¨Ç≈ÅAÇ∑Ç≈Ç…ÇªÇÃåfé¶î¬Ç™ë∂ç›ÇµÇƒÇ¢Ç‹Ç∑ÅB<br><br>
<a href="$script?mode=setup&amp;pass=$Fm{'pass'}">ñﬂÇÈ</a>
END
&footer;
print<<END;
</body>
</html>
END
}
} elsif($Fm{'subm'} eq 'editp') {
&error("åfé¶î¬ê›íËópÉpÉXÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'editpass'} eq '');
&error("åfé¶î¬ê›íËópÉpÉXÇ∆ÅAÇªÇÃämîFópÇÃÉpÉXÇ™àŸÇ»Ç¡ÇƒÇ¢Ç‹Ç∑ÅB") if($Fm{'editpass'} ne $Fm{'checkpass'});
&error("åfé¶î¬ê›íËópÉpÉXÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB") if(length($Fm{'editpass'}) > 8);
$Fm{'topcom'} =~ s/\&amp\;/\&/g;
$Fm{'topcom'} =~ s/\&lt\;/</g;
$Fm{'topcom'} =~ s/\&gt\;/>/g;
$Fm{'topcom'} =~ s/\&quot\;/\"/g;
$Fm{'topcom'} =~ s/\r\n/\n/g;
$Fm{'topcom'} =~ s/\r/\n/g;
$Fm{'style'} =~ s/\&amp\;/\&/g;
$Fm{'style'} =~ s/\&lt\;/</g;
$Fm{'style'} =~ s/\&gt\;/>/g;
$Fm{'style'} =~ s/\&quot\;/\"/g;
$Fm{'style'} =~ s/\r\n/\n/g;
$Fm{'style'} =~ s/\r/\n/g;
$Fm{'icon'} =~ s/\r\n/\:/g;
$Fm{'icon'} =~ s/\r/\:/g;
$Fm{'icon'} =~ s/\n/\:/g;
$Fm{'color'} =~ s/\r\n/\:/g;
$Fm{'color'} =~ s/\r/\:/g;
$Fm{'color'} =~ s/\n/\:/g;
$Fm{'spicon'} =~ s/\r\n/\:/g;
$Fm{'spicon'} =~ s/\r/\:/g;
$Fm{'spicon'} =~ s/\n/\:/g;
$Fm{'adpass'} =~ s/\r\n/\:/g;
$Fm{'adpass'} =~ s/\r/\:/g;
$Fm{'adpass'} =~ s/\n/\:/g;
&error("åfé¶î¬ÉgÉbÉvÉRÉÅÉìÉgÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB") if(length($Fm{'topcom'}) > $topcommax);
&error("åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[ÉgÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB") if(length($Fm{'style'}) > $stylemax);
mkdir("${setupdir}/$Fm{'id'}",0777) or &error("åfé¶î¬ê›íËÉfÉBÉåÉNÉgÉäÅF${setupdir}/$Fm{'id'} ÇÃçÏê¨Ç…é∏îsÇµÇ‹ÇµÇΩÅB") if($Fm{'edit'} ne 'edit');
chmod("${setupdir}/$Fm{'id'}",0777);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbssetup") or &error("åfé¶î¬ê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbssetup ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE "$Fm{'title'}<>$Fm{'topon'}<>$Fm{'tcolor'}<>$Fm{'titlei'}<>$Fm{'adname'}<>$Fm{'admail'}<>$Fm{'imgdir'}<>$Fm{'backpa'}<>$Fm{'backpn'}<>$Fm{'upbbs'}<>$Fm{'spicon'}<>$Fm{'icon'}<>$Fm{'color'}<>$Fm{'adpass'}<>$Fm{'editpass'}<>";
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbssetup",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbstopcom") or &error("åfé¶î¬ÉgÉbÉvÉRÉÅÉìÉgÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbstopcom ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE $Fm{'topcom'};
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbstopcom",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbsstyle") or &error("åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[Égê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbsstyle ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE $Fm{'style'};
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbsstyle",0666);
if($Fm{'edit'} ne 'edit') {
open(FILE,"> ${setupdir}/$Fm{'id'}/$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$log ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE '';
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$log",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$count") or &error("ÉJÉEÉìÉgâÒêîãLò^ÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$count ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE 0;
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$count",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$userc") or &error("ÉÜÅ[ÉUÅ[èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$count ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE 0;
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$userc",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$ipban") or &error("ÉAÉNÉZÉXãKêßê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$ipban ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE "";
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$ipban",0666);
}
&pagemove("$script?mode=setup&pass=$Fm{'pass'}");
} elsif($Fm{'subm'} eq 'delete') {
unlink("${setupdir}/$Fm{'id'}/$bbssetup");
unlink("${setupdir}/$Fm{'id'}/$bbstopcom");
unlink("${setupdir}/$Fm{'id'}/$bbsstyle");
unlink("${setupdir}/$Fm{'id'}/$log");
unlink("${setupdir}/$Fm{'id'}/$count");
unlink("${setupdir}/$Fm{'id'}/$userc");
rmdir("${setupdir}/$Fm{'id'}");
&pagemove("$script?mode=setup&pass=$Fm{'pass'}");
} elsif($Fm{'subm'} eq 'change') {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>åfé¶î¬IDïœçX - ${title}</title>
</head>
<body>
<font size="$tsize" color="$tcolor">åfé¶î¬IDïœçX</font><br><br>
åfé¶î¬ID.$Fm{'id'} ÇÃIDïœçX<br>
<form action="$script" method="POST" style="display:inline;">
<input type="hidden" name="mode" value="setup">
<input type="hidden" name="subm" value="changep">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
ïœçXå„ÇÃID.<input type="text" name="newid" value="$Fm{'id'}">
<input type="submit" value="ïœçXÇ∑ÇÈ"><input type="button" value="Ç‚Ç¡Çœé~ÇﬂÇÈ" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script?mode=setup&amp;pass=$Fm{'pass'}';" onKeyPress="">
</form>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'changep') {
rename("${setupdir}/$Fm{'id'}","${setupdir}/$Fm{'newid'}");
&pagemove("$script?mode=setup&pass=$Fm{'pass'}");
} elsif($Fm{'subm'} eq 'resetcust') {
$icon = join(':', @icon);
$color = join(':', @color);
$spicon = join(':', @spicon);
$adpass = join(':', @adpass);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbssetup") or &error("åfé¶î¬ê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbssetup ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE "$title<>$topon<>$tcolor<>$titlei<>$adname<>$admail<>$imgdir<>$backpa<>$backpn<>$upbbs<>$spicon<>$icon<>$color<>$adpass<>";
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbssetup",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbstopcom") or &error("åfé¶î¬ÉgÉbÉvÉRÉÅÉìÉgÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbstopcom ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE $topcom;
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbstopcom",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbsstyle") or &error("åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[Égê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbsstyle ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE $style;
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbsstyle",0666);
&pagemove("$script?mode=setup&pass=$Fm{'pass'}");
} elsif($Fm{'subm'} eq 'resetlog') {
open(FILE,"> ${setupdir}/$Fm{'id'}/$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$log ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE '';
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$log",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$count") or &error("ÉJÉEÉìÉgâÒêîãLò^ÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$count ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE 0;
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$count",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$userc") or &error("ÉÜÅ[ÉUÅ[èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$userc ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE 0;
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$userc",0666);
&pagemove("$script?mode=setup&pass=$Fm{'pass'}");
} elsif($Fm{'subm'} eq 'icom') {
open(FILE,"< $indexcom");
@indexcom = <FILE>;
close(FILE);

print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ÉCÉìÉfÉbÉNÉXê›íË - ${title}</title>
</head>
<body>
<font size="$tsize" color="$tcolor">ÉCÉìÉfÉbÉNÉXê›íË</font><br><br>
<form action="$script" method="POST" onSubmit="if(!confirm('ñ{ìñÇ…ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;">
<input type="hidden" name="mode" value="setup">
<input type="hidden" name="subm" value="icomp">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
<table summary="ï\\" border="1" cellspacing="0" cellpadding="0">
<tr><td>ÉCÉìÉfÉbÉNÉXÇÃÉRÉÅÉìÉg</td><td><textarea name="indexcom" cols="80" rows="10" wrap="off" style="font-family:FixedSys;">
END
foreach $tmpindexcom (@indexcom) {
$tmpindexcom =~ s/\&/\&amp\;/g;
$tmpindexcom =~ s/</\&lt\;/g;
$tmpindexcom =~ s/>/\&gt\;/g;
$tmpindexcom =~ s/\"/\&quot\;/g;
print $tmpindexcom;
}
print<<END;
</textarea>
</td></tr>
<tr><td colspan="2"><input type="submit" value="ï“èWäÆóπ"> <input type="button" value="Ç‚Ç¡Çœé~ÇﬂÇÈ" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script?mode=setup&amp;pass=$Fm{'pass'}';" onKeyPress=""></td></tr>
</table>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'icomp') {
$Fm{'indexcom'} =~ s/\&amp\;/\&/g;
$Fm{'indexcom'} =~ s/\&lt\;/</g;
$Fm{'indexcom'} =~ s/\&gt\;/>/g;
$Fm{'indexcom'} =~ s/\&quot\;/\"/g;
$Fm{'indexcom'} =~ s/\r\n/\n/g;
$Fm{'indexcom'} =~ s/\r/\n/g;
open(FILE,"> $indexcom");
print FILE $Fm{'indexcom'};
close(FILE);
chmod($indexcom,0666);
&pagemove("$script?mode=setup&pass=$Fm{'pass'}");
} else {
opendir(DIR, $setupdir);
@bbslist = sort readdir(DIR);
closedir(DIR);
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>åfé¶î¬ï“èW - ${title}</title>
</head>
<body>
<font size="$tsize" color="$tcolor">åfé¶î¬ï“èW</font><br><br>
<table summary="ï\\" border="1" cellspacing="0" cellpadding="0">
<tr><td>åfé¶î¬ID</td><td>ólÅXÇ»ëÄçÏ</td></tr>
END
foreach $bbsid (@bbslist) {
print"<tr><td><a href=\"$script?id=$bbsid\" target=\"_blank\">${bbsid}</a></td><td>[<a href=\"$script?mode=setup&amp;subm=edit&amp;edit=edit&amp;id=$bbsid&amp;pass=$Fm{'pass'}\">ê›íËïœçX</a>] [<a href=\"$script?mode=setup&amp;subm=change&amp;id=$bbsid&amp;pass=$Fm{'pass'}\">IDïœçX</a>] [<a href=\"$script?mode=setup&amp;subm=resetcust&amp;id=$bbsid&amp;pass=$Fm{'pass'}\" onClick=\"if(!confirm('åfé¶î¬ÇÃê›íËÇÅAèâä˙èÛë‘Ç…Ç‡Ç«ÇµÇ‹Ç∑Ç©ÅH\\nÉçÉOÇÕè¡Ç¶Ç‹ÇπÇÒÇ™ÅAëSÇƒÇÃê›íËÇ™èâä˙èÛë‘Ç…ñﬂÇËÇ‹Ç∑ÅB\\nèâä˙âªÇµÇΩèÍçáÅAé©ìÆÇ≈å≥Ç…ñﬂÇ∑Ç±Ç∆ÇÕÇ≈Ç´Ç‹ÇπÇÒÅB\\n\\nÅEÅEÅEÇªÇÍÇ≈Ç‡ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;\" onKeyPress=\"\">ê›íËèâä˙âª</a>] [<a href=\"$script?mode=setup&amp;subm=resetlog&amp;id=$bbsid&amp;pass=$Fm{'pass'}\" onClick=\"if(!confirm('åfé¶î¬ÇÃÉçÉOÇÅAëSÇƒè¡ãéÇµÇƒèâä˙èÛë‘Ç…Ç‡Ç«ÇµÇ‹Ç∑Ç©ÅH\\nê›íËÇÕÇªÇÃÇ‹Ç‹écÇËÇ‹Ç∑Ç™ÅAëSÇƒÇÃÉçÉOÇÕè¡Ç¶Ç‹Ç∑ÅB\\nÉçÉOÇè¡ãéÇµÇΩèÍçáÅAé©ìÆÇ≈å≥Ç…ñﬂÇ∑Ç±Ç∆ÇÕÇ≈Ç´Ç‹ÇπÇÒÅB\\n\\nÅEÅEÅEÇªÇÍÇ≈Ç‡ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;\" onKeyPress=\"\">ÉçÉOèâä˙âª</a>] [<a href=\"$script?mode=setup&amp;subm=delete&amp;id=$bbsid&amp;pass=$Fm{'pass'}\" onClick=\"if(!confirm('ñ{ìñÇ…çÌèúÇµÇ‹Ç∑Ç©ÅH\\nçÌèúÇµÇΩåfé¶î¬ÇÕÅAå≥Ç…ÇÕñﬂÇπÇ‹ÇπÇÒÅB\\nÅEÅEÅEÇªÇÍÇ≈Ç‡ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;\" onKeyPress=\"\">çÌèú</a>]</td></tr>\n" if(($bbsid ne '.') && ($bbsid ne '..'));
}
print<<END;
</table>
<hr>
<form action="$script" method="POST" style="display:inline;">
<input type="hidden" name="mode" value="setup">
<input type="hidden" name="subm" value="edit">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="edit" value="">
åfé¶î¬êVãKçÏê¨<br>
åfé¶î¬ID.<input type="text" name="id" size="32"><input type="submit" value="çÏê¨Ç∑ÇÈ">
</form>
<hr>
<a href="$script?mode=setup&amp;subm=icom&amp;id=$bbsid&amp;pass=$Fm{'pass'}">ÉCÉìÉfÉbÉNÉXÉRÉÅÉìÉgÇÃê›íË</a>
<hr>
<a href="$script">ñﬂÇÈ</a>
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
