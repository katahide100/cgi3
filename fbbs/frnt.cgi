sub rentedit {
&error("åfé¶î¬ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');

if(($Fm{'subm'} eq 'regist') || ($Fm{'subm'} eq 'edit')) {
if($Fm{'subm'} eq 'regist') {
$edit = 0;
} else {
$edit = 1;
}
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error("åfé¶î¬ÇhÇcÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB") if(length($Fm{'id'}) > 8);
&error("ÉpÉXÉèÅ[ÉhÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB") if(length($Fm{'pass'}) > 8);
&error('Ç∑Ç≈Ç…ÇªÇÃåfé¶î¬Ç™ë∂ç›ÇµÇƒÇ¢Ç‹Ç∑ÅB<br>ï ÇÃÇhÇcÇ≈ìoò^ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB') if((-e "${setupdir}/$Fm{'id'}") && ($edit == 0));
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if((!-e "${setupdir}/$Fm{'id'}") && ($edit == 1));

if($edit == 1) {
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbstopcom");
@etopcom = <FILE>;
close(FILE);
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbsstyle");
@estyle = <FILE>;
close(FILE);
open(FILE,"< ${setupdir}/$Fm{'id'}/$usea");
@eagr = <FILE>;
close(FILE);

$espicon =~ s/\:/\n/g;
$eicon =~ s/\:/\n/g;
$ecolor =~ s/\:/\n/g;
$eadpass =~ s/\:/\n/g;

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

foreach $tmpagr (@eagr) {
$tmpestyle =~ s/\&/\&amp\;/g;
$tmpestyle =~ s/</\&lt\;/g;
$tmpestyle =~ s/>/\&gt\;/g;
$tmpestyle =~ s/\"/\&quot\;/g;
$eusea .= $tmpagr;
}

} else {
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');

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
$eusea = $agmcom;
$espicon = '';
$eicon = join("\n",@icon);
$ecolor = join("\n",@color);
$eadpass = $Fm{'pass'};

$etopcom = $topcom;
$estyle = $style;

$eeditpass = $Fm{'pass'};
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
if($edit == 1) {
print"åfé¶î¬ÇhÇcÅF<a href=\"$script?id=$Fm{'id'}\" target=\"_blank\">$Fm{'id'}</a>Å@ÇÃï“èW<br>\n";
} else {
print"åfé¶î¬ÇhÇcÅF<a href=\"$script?id=$Fm{'id'}\" target=\"_blank\">$Fm{'id'}</a>Å@ÇÃêVãKçÏê¨<br>\n";
}
print<<END;
<p>
	<b>ëSçÄñ⁄ÅAîºäpÉJÉ^ÉJÉiÇÕã÷é~ÅI</b><br>
	ï∂éöâªÇØñhé~ÇÃÇΩÇﬂéÁÇ¡ÇƒÇ≠ÇæÇ≥Ç¢ÅB
</p>
<form action="$script" method="POST" onSubmit="if(!confirm('ñ{ìñÇ…ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;">
<input type="hidden" name="mode" value="rentedit">
<input type="hidden" name="subm" value="$Fm{'subm'}p">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="pass" value="$Fm{'pass'}">
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
<tr><td><a href="#" onClick="alert('ÉAÉCÉRÉìÇÃÉAÉhÉåÉX,ÉAÉCÉRÉìñº\\nÉAÉCÉRÉìÇÃÉAÉhÉåÉX,ÉAÉCÉRÉìñº\\nÉAÉCÉRÉìÇÃÉAÉhÉåÉX,ÉAÉCÉRÉìñº\\nÅEÅEÅE\\n\\nÇ∆â]Ç¡ÇΩä¥Ç∂Ç≈ê›íËÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB\\n\\nÇ»Ç®ÅAëSÇƒÅuâÊëúÉtÉ@ÉCÉãÇÃÇ†ÇÈÉAÉhÉåÉXÅvÇ…ì¸Ç¡ÇƒÇ¢ÇÈÇ±Ç∆Ç™èåèÅB');return false;">ÉAÉCÉRÉì</a></td><td><textarea cols="80" rows="4" name="icon">
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
$estyle</textarea><br>
Å¶padding-left... ÇÕè¡ÇµÇƒÇ©Ç‹Ç¢Ç‹ÇπÇÒÅB</td></tr>
<tr><td>óòópãKñÒ</td><td><textarea name="agr" cols="80" rows="5" wrap="off">
$eusea</textarea></td></tr>
<tr><td>åfé¶î¬ê›íËÉpÉX</td><td><input type="password" size="20" name="editpass" value="$eeditpass"></td></tr>
<tr><td>è„ãLÉpÉXÇÃämîF</td><td><input type="password" size="20" name="checkpass" value="$eeditpass"></td></tr>
<tr><td colspan="2"><input type="button" value="ÉLÉÉÉìÉZÉã" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script';" onKeyPress=""> <input type="submit" value="éüÇ÷ &gt;&gt;"></td></tr>
</table>
END
&footer;
print<<END;
</body>
</html>
END
} elsif(($Fm{'subm'} eq 'editp') || ($Fm{'subm'} eq 'registp')) {
if($Fm{'subm'} eq 'registp') {
$edit = 0;
} else {
$edit = 1;
}
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ∆ÅAÇªÇÃämîFópÇÃÉpÉXÇ™àŸÇ»Ç¡ÇƒÇ¢Ç‹Ç∑ÅB") if($Fm{'editpass'} ne $Fm{'checkpass'});
&error("ÉpÉXÉèÅ[ÉhÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB") if(length($Fm{'editpass'}) > 8);
&error('Ç∑Ç≈Ç…ÇªÇÃåfé¶î¬Ç™ë∂ç›ÇµÇƒÇ¢Ç‹Ç∑ÅB<br>ï ÇÃÇhÇcÇ≈ìoò^ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB') if((-e "${setupdir}/$Fm{'id'}") && ($edit == 0));
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if((!-e "${setupdir}/$Fm{'id'}") && ($edit == 1));
if($edit == 1) {
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);
}
$Fm{'topcom'} =~ s/\&amp\;/\&/g;
$Fm{'topcom'} =~ s/\&lt\;/</g;
$Fm{'topcom'} =~ s/\&gt\;/>/g;
$Fm{'topcom'} =~ s/\&quot\;/\"/g;
$Fm{'topcom'} =~ s/\r\n/\n/g;
$Fm{'topcom'} =~ s/\r/\n/g;
$Fm{'agr'} =~ s/\&amp\;/\&/g;
$Fm{'agr'} =~ s/\&lt\;/</g;
$Fm{'agr'} =~ s/\&gt\;/>/g;
$Fm{'agr'} =~ s/\&quot\;/\"/g;
$Fm{'agr'} =~ s/\r\n/\n/g;
$Fm{'agr'} =~ s/\r/\n/g;
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
mkdir("${setupdir}/$Fm{'id'}",0777) or &error("åfé¶î¬ê›íËÉfÉBÉåÉNÉgÉäÅF${setupdir}/$Fm{'id'} ÇÃçÏê¨Ç…é∏îsÇµÇ‹ÇµÇΩÅB") if($edit == 0);
chmod("${setupdir}/$Fm{'id'}",0777);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbssetup") or &error("åfé¶î¬ê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbssetup ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE "$Fm{'title'}<>$Fm{'topon'}<>$Fm{'tcolor'}<>$Fm{'titlei'}<>$Fm{'adname'}<>$Fm{'admail'}<>$Fm{'imgdir'}<>$Fm{'backpa'}<>$Fm{'backpn'}<>$Fm{'upbbs'}<>$Fm{'spicon'}<>$Fm{'icon'}<>$Fm{'color'}<>$Fm{'adpass'}<>$Fm{'editpass'}<>";
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbssetup",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbstopcom") or &error("åfé¶î¬ÉgÉbÉvÉRÉÅÉìÉgÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbstopcom ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE $Fm{'topcom'};
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbstopcom",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$usea") or &error("åfé¶î¬óòópãKíËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$usea ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE $Fm{'agr'};
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$usea",0666);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbsstyle") or &error("åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[Égê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbsstyle ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE $Fm{'style'};
close(FILE);
chmod("${setupdir}/$Fm{'id'}/$bbsstyle",0666);
if($edit == 0) {
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
	print"Content-Type:text/html\n\n";
	print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>${title}</title>
</head>
<body>
<div align="center">
END
if($edit == 1) {
print<<END;
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@Çï“èWÇµÇ‹ÇµÇΩÅB<br><br>
END
} else {
print<<END;
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇçÏê¨ÇµÇ‹ÇµÇΩÅB<br><br>
END
}
print <<END;
<form>
<input type="button" value="äÆóπ" onclick="location.href='$script';">
</form>
</div>
END
	&footer;
	print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'delete') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>åfé¶î¬çÌèú - ${title}</title>
<style type="text/css">
<!--
.confirm {
	font-weight:bolder;
	color:blue;
}
-->
</style>
</head>
<body>
<font size="$tsize" color="$tcolor">åfé¶î¬çÌèú</font><br><br>
<p>åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇÃçÌèú</p>
<p class="confirm">
Ç±ÇÃåfé¶î¬ÇçÌèúÇµÇΩèÍçáÅAåfé¶î¬ÇÃê›íËèÓïÒÅAÉçÉOÅAÇªÇÍÇÁëSÇƒÇ™ñïè¡Ç≥ÇÍÇ‹Ç∑ÅB<br>
è¡Ç¶ÇƒÇµÇ‹Ç¡ÇΩÉfÅ[É^ÇÕå≥Ç…ÇÕñﬂÇËÇ‹ÇπÇÒÅI
</p>
<form action="$script" method="POST" style="display:inline;" name="remove" onSubmit="">
<input type="hidden" name="mode" value="rentedit">
<input type="hidden" name="subm" value="deletep">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="submit" value="åfé¶î¬ÇçÌèúÇ∑ÇÈ"><input type="button" value="Ç‚Ç¡Çœé~ÇﬂÇÈ" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script';" onKeyPress="">
</form>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'deletep') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

unlink("${setupdir}/$Fm{'id'}/$bbssetup");
unlink("${setupdir}/$Fm{'id'}/$bbstopcom");
unlink("${setupdir}/$Fm{'id'}/$bbsstyle");
unlink("${setupdir}/$Fm{'id'}/$log");
unlink("${setupdir}/$Fm{'id'}/$count");
unlink("${setupdir}/$Fm{'id'}/$userc");
unlink("${setupdir}/$Fm{'id'}/$usea");
unlink("${setupdir}/$Fm{'id'}/fbbs.dat");
rmdir("${setupdir}/$Fm{'id'}");
	print"Content-Type:text/html\n\n";
	print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>${title}</title>
</head>
<body>
<div align="center">
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇçÌèúÇµÇ‹ÇµÇΩÅB<br><br>
<a href="$script">ñﬂÇÈ</a>
</div>
END
	&footer;
	print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'change') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

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
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇÃIDïœçX<br>
<form action="$script" method="POST" style="display:inline;">
<input type="hidden" name="mode" value="rentedit">
<input type="hidden" name="subm" value="changep">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
ïœçXå„ÇÃÇhÇcÅF<input type="text" name="newid" value="$Fm{'id'}">
<input type="submit" value="ïœçXÇ∑ÇÈ"><input type="button" value="Ç‚Ç¡Çœé~ÇﬂÇÈ" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script';" onKeyPress="">
</form>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'changep') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

rename("${setupdir}/$Fm{'id'}","${setupdir}/$Fm{'newid'}");
	print"Content-Type:text/html\n\n";
	print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>${title}</title>
</head>
<body>
<div align="center">
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇÅ@<a href="$script?id=$Fm{'newid'}" target="_blank">$Fm{'newid'}</a>Å@Ç…ïœçXÇµÇ‹ÇµÇΩÅB<br><br>
<a href="$script">ñﬂÇÈ</a>
</div>
END
	&footer;
	print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'resetcust') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>åfé¶î¬ê›íËèâä˙âª - ${title}</title>
</head>
<body>
<font size="$tsize" color="$tcolor">åfé¶î¬ê›íËèâä˙âª</font><br><br>
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇÃê›íËèâä˙âª<br>
<form action="$script" method="POST" style="display:inline;" onSubmit="if(!confirm('ñ{ìñÇ…ÅAåfé¶î¬ÇÃê›íËÇèâä˙âªÇµÇ‹Ç∑Ç©ÅH\nç°Ç‹Ç≈Ç…ïœçXÇµÇΩì‡óeÇÕÅAëSÇƒå≥Ç…ñﬂÇËÇ‹Ç∑ÅB\nÇªÇÍÇ≈Ç‡ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;">
<input type="hidden" name="mode" value="rentedit">
<input type="hidden" name="subm" value="resetcustp">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="submit" value="ê›íËÇèâä˙âªÇ∑ÇÈ"><input type="button" value="Ç‚Ç¡Çœé~ÇﬂÇÈ" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script';" onKeyPress="">
</form>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'resetcustp') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

$icon = join(':', @icon);
$color = join(':', @color);
$spicon = join(':', @spicon);
$adpass = join(':', @adpass);
open(FILE,"> ${setupdir}/$Fm{'id'}/$bbssetup") or &error("åfé¶î¬ê›íËÉtÉ@ÉCÉãÅF${setupdir}/$Fm{'id'}/$bbssetup ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
print FILE "$title<>$topon<>$tcolor<>$titlei<>$adname<>$admail<>$imgdir<>$backpa<>$backpn<>$upbbs<>$spicon<>$icon<>$color<>$adpass<>$eeditpass<>";
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
	print"Content-Type:text/html\n\n";
	print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>${title}</title>
</head>
<body>
<div align="center">
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇÃê›íËÇèâä˙âªÇµÇ‹ÇµÇΩÅB<br><br>
<a href="$script">ñﬂÇÈ</a>
</div>
END
	&footer;
	print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'resetlog') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>åfé¶î¬ÉçÉOèâä˙âª - ${title}</title>
</head>
<body>
<font size="$tsize" color="$tcolor">åfé¶î¬ÉçÉOèâä˙âª</font><br><br>
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇÃÉçÉOèâä˙âª<br>
<form action="$script" method="POST" style="display:inline;" onSubmit="if(!confirm('ñ{ìñÇ…ÅAÉçÉOÇèâä˙âªÇµÇ‹Ç∑Ç©ÅH\nç°Ç‹Ç≈Ç…èëÇ´çûÇ‹ÇÍÇΩãLéñÇÕÅAëSÇƒçÌèúÇ≥ÇÍÇ‹Ç∑ÅB\nÇªÇÍÇ≈Ç‡ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;">
<input type="hidden" name="mode" value="rentedit">
<input type="hidden" name="subm" value="resetlogp">
<input type="hidden" name="pass" value="$Fm{'pass'}">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="submit" value="ÉçÉOÇèâä˙âªÇ∑ÇÈ"><input type="button" value="Ç‚Ç¡Çœé~ÇﬂÇÈ" onClick="if(confirm('ñ{ìñÇ…é~ÇﬂÇ‹Ç∑Ç©ÅH')) location.href = '$script';" onKeyPress="">
</form>
END
&footer;
print<<END;
</body>
</html>
END
} elsif($Fm{'subm'} eq 'resetlogp') {
&error("ÇhÇcÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'id'} eq '');
&error("ÉpÉXÉèÅ[ÉhÇ™ì¸óÕÇ≥ÇÍÇƒÇ¢Ç‹ÇπÇÒÅB") if($Fm{'pass'} eq '');
&error('ÇªÇÃÇhÇcÇÃåfé¶î¬Ç™ë∂ç›ÇµÇ‹ÇπÇÒÅB<br>ÇhÇcÇÃì¸óÕÇä‘à·Ç¶ÇΩÇ©ÅAÇ‡ÇµÇ≠ÇÕçÌèúÇ≥ÇÍÇΩâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB') if(!-e "${setupdir}/$Fm{'id'}");
open(FILE,"< ${setupdir}/$Fm{'id'}/$bbssetup");
($etitle,$etopon,$etcolor,$etitlei,$eadname,$eadmail,$eimgdir,$ebackpa,$ebackpn,$eupbbs,$espicon,$eicon,$ecolor,$eadpass,$eeditpass) = split(/<>/,<FILE>);
close(FILE);
&error('ÉpÉXÉèÅ[ÉhÇ™ä‘à·Ç¡ÇƒÇ¢Ç‹Ç∑ÅB') if($Fm{'pass'} ne $eeditpass);

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
	print"Content-Type:text/html\n\n";
	print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>${title}</title>
</head>
<body>
<div align="center">
åfé¶î¬ÇhÇcÅF<a href="$script?id=$Fm{'id'}" target="_blank">$Fm{'id'}</a>Å@ÇÃÉçÉOÇèâä˙âªÇµÇ‹ÇµÇΩÅB<br><br>
<a href="$script">ñﬂÇÈ</a>
</div>
END
	&footer;
	print<<END;
</body>
</html>
END
} else {
&pagemove("$script");
}

}

1;
