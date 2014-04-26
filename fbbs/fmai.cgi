sub main {
	open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
	@log = <LOG>;
	close(LOG);
	$viewcommentcount = 0;
	@threadvalue = ();
	@threadlist = ();
	$threadcount = 0;
	$rescount = 0;
	$Fm{'page'}-- if($Fm{'page'} > 0);
	foreach $tmplog (@log) {
		#ãLéñNo.<>êeãLéñNo.<>éûä‘<>ñºëO<>ÉÅÅ[Éã<>ëËñº<>ÉRÉÅÉìÉg<>ÉEÉFÉuÉTÉCÉg<>ÉzÉXÉg<>ÉpÉXÉèÅ[Éh<>êF<>ÉAÉCÉRÉì<>
		($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
		$tmprescount = $rescount;
		if($lrno eq '') {
			$threadlist[$threadcount] .= "$rescount<>" if($threadcount > 0);
			$rescount = 0;
			$threadlist[$threadcount+1] = "$lno<>$ltitle<>";
		} else {
			$rescount++;
		}
		$vrc = $rescount + 1;
		$threadcount++ if($lrno eq '');

		if((($Fm{'page'} * $onep) < $threadcount) && ((($Fm{'page'} * $onep) + $onep) >= $threadcount)) {
			$oldrescount = $tmprescount;
			&jumper;
			$tmplog = "$lno<>$lrno<>$ltime<>$lname<>$lmail<>${vrc}. $ltitle<>$lcomment<>$lhp<>$lhost<>$lpass<>$lcolor<>$licon<>\n";

			if(($lcomment =~ /^((?:.*?<br>){$redis})/) && ($redis > 0)) {
				$lcomment = $1;
				$tmpnum = ($lrno eq '') ? $lno : $lrno;
				$lcomment .= "<br>\n<br>\n<i style=\"color:#000000;\">Ç±ÇÃãLéñÇÕè»ó™Ç≥ÇÍÇ‹ÇµÇΩÅB<br>ëSÇƒì«ÇﬁÇ…ÇÕ[<a href=\"$script?id=$Fm{'id'}&amp;mode=res&amp;rno=$tmpnum#no$lno\">ï‘êM</a>]ÇÉNÉäÉbÉNÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB</i>\n";
				$tmplog = "$lno<>$lrno<>$ltime<>$lname<>$lmail<>${vrc}. $ltitle<>$lcomment<>$lhp<>$lhost<>$lpass<>$lcolor<>$licon<>\n";
			}

			if($viewcommentcount > 0) {
				if(($lrno eq '') && ($thdis > 0) && ($abbcount > 0)) {
					($tlno,$tlrno,$tltime,$tlname,$tlmail,$tltitle,$tlcomment,$tlhp,$tlhost,$tlpass,$tlcolor,$tlicon) = split(/<>/,$threadvalue[$viewcommentcount-$thdis-1]);
					$threadvalue[$viewcommentcount-$thdis-1] = "$tlno<>$tlrno<>$tltime<>$tlname<>$tlmail<>$tltitle<>$tlcomment<br><br><i style=\"color:#000000;\"><b>$abbcount</b>åèÇ™è»ó™Ç≥ÇÍÇ‹ÇµÇΩÅB<br>ëSïîì«ÇﬁÇ…ÇÕÅA[<a href=\"$script?id=$Fm{'id'}&amp;mode=res&amp;rno=$tlno\">ï‘êM</a>]ÇÉNÉäÉbÉNÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB</i><>$tlhp<>$tlhost<>$tlpass<>$tlcolor<>$tlicon<>\n";
				}
				if(($lrno eq '') && ($oldrescount >= $maxres) && ($maxres > 0)) {
					($tlno,$tlrno,$tltime,$tlname,$tlmail,$tltitle,$tlcomment,$tlhp,$tlhost,$tlpass,$tlcolor,$tlicon) = split(/<>/,$threadvalue[$viewcommentcount-$thdis-1]);
					$threadvalue[$viewcommentcount-$oldrescount+$abbcount-1] = "$tlno<>$tlrno<>$tltime<>$tlname<>$tlmail<>$tltitle<>$tlcomment<br><br><i style=\"color:#000000;\">Ç±ÇÃãLéñÇÕÅAÉåÉXêîÇ™<b>$maxres</b>åèÇ…íBÇµÇΩÇÃÇ≈ÅAÇ±ÇÍà»è„èëÇ´çûÇﬁÇ±Ç∆ÇÕÇ≈Ç´Ç‹ÇπÇÒÅB<br>êVÇµÇ¢ÉXÉåÉbÉhÇåöÇƒÇƒÇ≠ÇæÇ≥Ç¢ÅB</i><>$tlhp<>$tlhost<>$tlpass<>$tlcolor<>$tlicon<>\n";
				}
			}
			$abbcount = 0 if(($lrno eq '') && ($thdis > 0));

			$threadvalue[$viewcommentcount] = $tmplog;
			if(($rescount > $thdis) && ($viewcommentcount > 0) && ($thdis > 0)) {
				for($i=$thdis;$i>0;$i--) {
					$threadvalue[$viewcommentcount-$i] = $threadvalue[$viewcommentcount-$i+1];
				}

				$threadvalue[$viewcommentcount] = '';
				$abbcount++;
			} else {
				$viewcommentcount++;
			}
		}

	}
	if($viewcommentcount > 0) {
		if(($abbcount > 0) && ($thdis > 0)) {
			($tlno,$tlrno,$tltime,$tlname,$tlmail,$tltitle,$tlcomment,$tlhp,$tlhost,$tlpass,$tlcolor,$tlicon) = split(/<>/,$threadvalue[$viewcommentcount-$thdis-1]);
			$threadvalue[$viewcommentcount-$thdis-1] = "$tlno<>$tlrno<>$tltime<>$tlname<>$tlmail<>$tltitle<>$tlcomment<br><br><i style=\"color:#000000;\"><b>$abbcount</b>åèÇ™è»ó™Ç≥ÇÍÇ‹ÇµÇΩÅB<br>ëSïîì«ÇﬁÇ…ÇÕÅA[<a href=\"$script?id=$Fm{'id'}&amp;mode=res&amp;rno=$tlno\">ï‘êM</a>]ÇÉNÉäÉbÉNÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB</i><>$tlhp<>$tlhost<>$tlpass<>$tlcolor<>$tlicon<>\n";
		}
		if(($oldrescount > $maxres) && ($maxres > 0)) {
			($tlno,$tlrno,$tltime,$tlname,$tlmail,$tltitle,$tlcomment,$tlhp,$tlhost,$tlpass,$tlcolor,$tlicon) = split(/<>/,$threadvalue[$viewcommentcount-$oldrescount+$abbcount-1]);
			$threadvalue[$viewcommentcount-$tmprescount+$abbcount-1] = "$tlno<>$tlrno<>$tltime<>$tlname<>$tlmail<>$tltitle<>$tlcomment<br><br><i style=\"color:#000000;\">Ç±ÇÃãLéñÇÕÅAÉåÉXêîÇ™<b>$maxres</b>åèÇ…íBÇµÇΩÇÃÇ≈ÅAÇ±ÇÍà»è„èëÇ´çûÇﬁÇ±Ç∆ÇÕÇ≈Ç´Ç‹ÇπÇÒÅB<br>êVÇµÇ¢ÉXÉåÉbÉhÇåöÇƒÇƒÇ≠ÇæÇ≥Ç¢ÅB</i><>$tlhp<>$tlhost<>$tlpass<>$tlcolor<>$tlicon<>\n";
		}
	}
	$threadlist[$threadcount] .= "$rescount<>" if($threadcount > 0);
	shift(@threadlist);
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
	if($titlei eq '') {
		print"<font size=\"$tsize\" color=\"$tcolor\">${title}</font>\n";
	} else {
		print"<img src=\"${imgdir}${titlei}\" alt=\"$title\">\n";
	}
	if($topon == 1) {
		print<<END;
<br>
<table summary="ï\\" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
${topcom}
</td></tr>
</table>
END
	}
	print<<END;
<hr width="90%">
END
	print"[<a href=\"$backpa\">${backpn}Ç÷ñﬂÇÈ</a>]&nbsp;";
	print"[<a href=\"${script}\">ÉCÉìÉfÉbÉNÉXÇ÷ñﬂÇÈ</a>]&nbsp;" if($bbstype == 1);
	print"[<a href=\"${script}?id=$Fm{'id'}&amp;mode=agreement\">óòópãKñÒ</a>]&nbsp;";
	print"[<a href=\"${script}?id=$Fm{'id'}&amp;mode=iconlist\">ÉAÉCÉRÉìàÍóó</a>]&nbsp;" if($iconon == 1);
	print"[<a href=\"${script}?id=$Fm{'id'}&amp;mode=alluc\">èëÇ´çûÇ›âÒêî</a>]&nbsp;" if($ucon == 1);
	print"[<a href=\"${script}?id=$Fm{'id'}&amp;mode=search\">ãLéñåüçı</a>]&nbsp;";
	print"[<a href=\"${script}?id=$Fm{'id'}&amp;mode=admin\">ä«óùÉÇÅ[Éh</a>]&nbsp;";
	print<<END;
<hr width="90%">
<table summary="ï\\" border="0" cellspacing="0" cellpadding="0" width="90%">
<tr><td align="left">
<table summary="ï\\" border="0" cellspacing="16" cellpadding="0">
<tr><td>
END
	&msgform;
	print<<END;
</td><td>
<form action="$script" method="GET" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="res">
<select size="15" name="rno">
<option value="0" selected>ëSÇƒÇÃÉXÉåÉbÉh</option>
END
	foreach $threadlist (@threadlist) {
		next if($threadlist eq '');
		($thnumber,$thname,$thres) = split(/<>/,$threadlist);
		if($thname =~ /...................../) {
			$thname =~ s/(....................).*/$1\.\.\./;
		}
		print"<option value=\"$thnumber\">No.${thnumber} $thname ($thres)</option>\n";
	}
	print<<END;
</select><br>
<input type="submit" value="Ç±ÇÃãLéñÇå©ÇÈ">
</form>
</td></tr>
</table><hr><br>
END
	$viewcommentcount = 0;
	foreach $threadvalue (@threadvalue) {
		next if($threadvalue eq '');
		($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$threadvalue);
		($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
		if($lrno eq '') {
			print<<END;
<table summary="ï\\" border="1" cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff">
<tr><td>
<table summary="ï\\" border="0" cellspacing="4" cellpadding="0" width="100%">
<tr><td colspan="2">
END
		} else {
			print<<END;
</td></tr>
<tr><td width="64">&nbsp;</td>
<td>
<hr>
END
		}
		$lid = substr($lpass, -10, 10);
		$lname = ($lmail ne '') ? "<a href=\"mailto:$lmail\">$lname</a>" : $lname;
		$lhp = (($lhp ne '') && ($lhp ne 'http://')) ? " [<a href=\"$lhp\" target=\"_blank\">HP</a>]" : '';
		$printicon = ($licon ne '') ? "<img src=\"${imgdir}$licon\" alt=\"$licon\">" : '';
		if(($upbbs == 1) && ($lfile ne '')) {
			$printicon .= '<br>' if($printicon ne '');
			$printicon .= "[<a href=\"$uploadhttp/$uploadid$lfile\" target=\"_blank\">$lfile</a>]";
		}
		if($ucon == 1) {
			$ucview = ($lcount ne '') ? " (èëÇ´çûÇ› <b>${lcount}</b>âÒ)" : '';
		} else {
			$ucview = '';
		}
		print"<b>$ltitle</b> ìäçeé“ÅF<b>$lname</b>Ç≥ÇÒ${ucview} - <small>$ltime</small> <a href=\"#dform\" onClick=\"document.delform.no.value = '$lno';\" onKeyPress=\"\"><font color=\"#888800\" size=\"-1\">No.$lno</font></a>${lhp}";
		if($lrno eq '') {
			print" [<a href=\"${script}?id=$Fm{'id'}&amp;mode=res&amp;rno=${lno}\">ï‘êM</a>]";
		}
		print" <small>ID: ${lid}</small>" if($lpass ne '');
		&quotation;
		print<<END;
<table summary="ï\\" border="0" cellspacing="16" cellpadding="0">
<tr><td>$printicon</td><td><font color="$lcolor">
$lcomment
<!-- IP:${raddr} HOST:${rhost} -->
</font></td></tr>
</table>
END

		($nlno,$nlrno,$nltime,$nlname,$nlmail,$nltitle,$nlcomment,$nlhp,$nlhost,$nlpass,$nlcolor,$nlicon) = split(/<>/,$threadvalue[$viewcommentcount+1]);
		if($nlrno eq '') {
			print"<td width=\"64\">&nbsp;</td></tr></table>\n";
			print"</td></tr>\n</table>\n<br><br>\n";
		}
		$viewcommentcount++;
	}
	print<<END;
<hr><div align="center">
<small>
END
	$logcount = int(($threadcount - 1) / $onep) + 1;
	$Fm{'page'}++;
	$tmpp = $Fm{'page'} - 1;
	if($Fm{'page'} > 1) { print"<a href=\"$script?id=$Fm{'id'}&amp;page=$tmpp\">Å©ëOÇÃÉyÅ[ÉW</a> "; } else { print"Å©ëOÇÃÉyÅ[ÉW "; }
	for($i=1;$i<=$logcount;$i++) {
		if($i eq $Fm{'page'}) {
			print"[<b>$i</b>] ";
		} else {
			print"[<a href=\"$script?id=$Fm{'id'}&amp;page=${i}\">${i}</a>] ";
		}
	}
	$tmpp = $Fm{'page'} + 1;
	if(($Fm{'page'} * $onep) < $threadcount) { print"<a href=\"$script?id=$Fm{'id'}&amp;page=$tmpp\">éüÇÃÉyÅ[ÉWÅ®</a>"; } else { print"éüÇÃÉyÅ[ÉWÅ®"; }
	print<<END;
</small>
<hr>
<form action="$script" name="delform" method="POST" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<small>
<a name="dform"></a>
- ãLéñÇÃï“èWÅEçÌèú -<br>
<input type="hidden" name="mode" value="custom">
ãLéñNo.<input type="text" name="no" size="8"> ÉpÉXÉèÅ[Éh<input type="password" size="8" name="pass"> <select name="dmode">
<option value="edit" selected>ãLéñï“èW</option>
<option value="move">ãLéñà⁄ìÆ</option>
<option value="delete">í èÌçÌèú</option>
<option value="pdelete">äÆëSçÌèú</option>
</select> 
<input type="submit" value="é¿çs"><br>
ãLéñÇÃà⁄ìÆêÊNo.(ãLéñà⁄ìÆÇëIÇÒÇæèÍçá)<input type="text" name="mno" size="8">
</small>
</form>
</div>
</td></tr></table>
</div>
END
	&footer;
	print<<END;
</body>
</html>
END
}

sub msgform {
	$sage = ($Fm{'mode'} eq 'res') ? '<tr><th colspan="2"><small>ÉåÉXéûÇ…ÅAÉXÉåÉbÉhÇè„Ç∞Ç»Ç¢</small> <input type="checkbox" name="sage" value="sage"> | ÉåÉXå„ÅAÇ±ÇÃãLéñÇÃï‘êMâÊñ Ç…ñﬂÇÈ <input type="checkbox" name="resback" value="resback"></th>' : '';
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
<input type="hidden" name="id" value="$Fm{'id'}">
<input type="hidden" name="mode" value="comwrite">
<input type="hidden" name="rno" value="$Fm{'rno'}">
<table summary="ï\\" border="0" cellspacing="0" cellpadding="0">
<tr><th align="left"><small>Ç®Ç»Ç‹Ç¶</small></th><td><input type="text" size="20" name="name" value="$name"></td></tr>
<tr><th align="left"><small>ÇdÉÅÅ[Éã</small></th><td><input type="text" size="20" name="mail" value="$mail"></td></tr>
<tr><th align="left"><small>É^ÉCÉgÉã</small></th><td><input type="text" size="30" name="title" value="$rtitle"> <input type="submit" value="ëóêMÇ∑ÇÈ" onClick="if(!confirm('èëÇ´çûÇ›Ç‹Ç∑Ç©ÅH')) return false;" onKeyPress=""><input type="reset" value="ÉäÉZÉbÉg" onClick="if(!confirm('ñ{ìñÇ…ÉäÉZÉbÉgÇµÇ‹Ç∑ÅB\\nì‡óeÇ™ëSÇƒè¡Ç¶Ç‹Ç∑ÅB\\nÅEÅEÅEÇªÇÍÇ≈Ç‡ÇÊÇÎÇµÇ¢Ç≈Ç∑Ç©ÅH')) return false;" onKeyPress=""></td></tr>
<tr><th colspan="2" align="left"><small>ÉÅÉbÉZÅ[ÉW</small></th></tr>
<tr><td colspan="2"><textarea cols="70" rows="7" name="comment" wrap="off">$Fm{'comment'}</textarea></td></tr>
<tr><th align="left"><small>ÇtÇqÇk</small></th><td><input type="text" size="40" name="hp" value="$hp"></td></tr>
END
	if($iconon == 1) {
		print<<END;
<tr><th align="left"><small>ÉCÉÅÅ[ÉW</small></th><td><select name="icon">
END
		$iconcount = 0;
		foreach $tmpicon (@icon) {
			($tmpiconaddr,$tmpiconname) = split(/\,/,$tmpicon);
			if($icon ne '') { $selected = ($icon eq $iconcount) ? ' selected' : ''; } else { $selected = ($iconcount == 0) ? ' selected' : ''; }
			print"<option value=\"$iconcount\"${selected}>$tmpiconname</option>\n";
			$iconcount++;
		}
		print<<END;
</select></td></tr>
END
	}
	print<<END;
<tr><th align="left"><small>ÉpÉXÉèÅ[Éh</small></th><td><input type="password" size="10" name="pass" value="$pass"> <small>(ãLéñÇÃÉÅÉìÉeéûÇ…égópÅBîºäpâpêîéöÇ≈8éöà»ì‡)</small></td></tr>
<tr><th align="left"><small>ï∂éöêF</small></th><td>
<table summary="ï\\" border="0" cellspacing="0" cellpadding="0" style="background-color:#ffffff;">
<tr><td nowrap>
END
	$colorcount = 0;
	foreach $tmpcolor (@color) {
		if($color ne '') { $checked = ($color eq $colorcount) ? ' checked' : ''; } else { $checked = ($colorcount == 0) ? ' checked' : ''; }
		print"<input type=\"radio\" name=\"color\" value=\"$colorcount\"${checked}><font color=\"$tmpcolor\" size=\"-1\">Å°</font>&nbsp;\n";
		print"<br>\n" if($colorcount % 7 == 6);
		$colorcount++;
	}
	print<<END;
</td></tr>
</table>
</td></tr>
END
	if($upbbs == 1) {
		print<<END;
<tr><th align="left"><small>ìYïtÉtÉ@ÉCÉã</small></th><td><input type="file" size="20" name="file"> <small>(<a style="color:#0000FF;cursor:hand;" onClick="alert('${maxup}BytesÇ‹Ç≈\\n\\nägí£éqÇ™\\n${upexplist}\\nÇÃÉtÉ@ÉCÉã');">ÉAÉbÉvÉçÅ[Éhâ¬î\\ÉtÉ@ÉCÉã</a>)</small></td></tr>
END
	}
	print<<END;
$sage
</table>
</form>
END
}

sub res {
	open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
	@log = <LOG>;
	close(LOG);
	$print = '';
	$vrc = 0;
	foreach $tmplog (@log) {
		($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
		($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
		if(($lno eq $Fm{'rno'}) || ($lrno eq $Fm{'rno'}) || (($lrno eq '') && ($Fm{'rno'} eq '0'))) {
			$vrc++;
			$rtitle = "Re: $ltitle" if($lrno eq '');
			if($lrno ne '') {
				$ltitle = 'Å@Å@' . "${vrc}. " . $ltitle;
			} else {
				$ltitle = "${vrc}. " . $ltitle;
			}
			$lid = substr($lpass, -10, 10);
			&jumper;

			$lname = ($lmail ne '') ? "<a href=\"mailto:$lmail\">$lname</a>" : $lname;
			$lhp = (($lhp ne '') && ($lhp ne 'http://')) ? " [<a href=\"$lhp\" target=\"_blank\">HP</a>]" : '';


			&quotation;
			$printicon = ($licon ne '') ? "<img src=\"${imgdir}$licon\" alt=\"$licon\">" : '';
			if(($upbbs == 1) && ($lfile ne '')) {
				$printicon .= '<br>' if($printicon ne '');
				$printicon .= "[<a href=\"$uploadhttp/$uploadid$lfile\" target=\"_blank\">$lfile</a>]";
			}
			if($ucon == 1) {
				$ucview = ($lcount ne '') ? " (èëÇ´çûÇ› <b>${lcount}</b>âÒ)" : '';
			} else {
				$ucview = '';
			}
			$print .= <<END;
<hr><a name="no$lno"></a><b>$ltitle</b> ìäçeé“ÅF<b>${lname}</b>Ç≥ÇÒ${ucview} - <small>$ltime</small> <a href="#dform" onClick="document.delform.no.value = '$lno';" onKeyPress=""><font color="#888800" size="-1">No.$lno</font></a> ${lhp}
END
			$print .= " [<a href=\"${script}?id=$Fm{'id'}&amp;mode=res&amp;rno=${lno}\">ï‘êM</a>]" if($Fm{'rno'} eq '0');
			$print .= " <small>ID: ${lid}</small>" if($lpass ne '');
			$print .= <<END;
<table summary="ï\\" border="0" cellspacing="16" cellpadding="0">
<tr><td>$printicon</td><td><font color="$lcolor">
$lcomment
<!-- IP:${raddr} HOST:${rhost} -->
</font></td></tr>
</table>
END
		}
	}

	print"Content-Type:text/html\n\n";
	print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
	&header;
if($Fm{'rno'} eq '0') {
print<<END;
<title>êeãLéñÉäÉXÉg Å| ${title}</title>
END
} else {
print<<END;
<title>ï‘êMÉtÉHÅ[ÉÄ Å| ${title}</title>
END
}
	print<<END;
</head>
<body>
END
if($Fm{'rno'} eq '0') {
print<<END;
<small>åfé¶î¬ÇÃÅAêeãLéñÉäÉXÉgÇ≈Ç∑ÅB
[<a href="$script?id=$Fm{'id'}" onClick="if(!confirm('åfé¶î¬ÇÃÉgÉbÉvÇ÷ñﬂÇËÇ‹Ç∑Ç©ÅH')) return false;" onKeyPress="">ñﬂÇÈ</a>]</small><br><br>
END
} else {
print<<END;
<small>ãLéñNo.$Fm{'rno'} Ç÷ÇÃï‘êMÉtÉHÅ[ÉÄÇ≈Ç∑ÅB
[<a href="$script?id=$Fm{'id'}" onClick="if(!confirm('ï‘êMÇé~ÇﬂÇƒñﬂÇËÇ‹Ç∑Ç©ÅH')) return false;" onKeyPress="">ñﬂÇÈ</a>]</small><br><br>
END
}

	if(($vrc > $maxres) && ($maxres > 0) && ($Fm{'rno'} ne '0')) {
		print<<END;
<i style="color:#000000;">Ç±ÇÃãLéñÇÕÅAÉåÉXêîÇ™<b>$maxres</b>åèÇ…íBÇµÇΩÇÃÇ≈ÅAÇ±ÇÍà»è„èëÇ´çûÇﬁÇ±Ç∆ÇÕÇ≈Ç´Ç‹ÇπÇÒÅB<br>êVÇµÇ¢ÉXÉåÉbÉhÇåöÇƒÇƒÇ≠ÇæÇ≥Ç¢ÅB</i><br><br>
END
}
	print<<END;
<div align="center">
<table summary="ï\\" width="90%" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
$print
END
	if(($vrc <= $maxres) || ($maxres == 0)) {
		print<<END;
<hr>
END
		&msgform if($Fm{'rno'} ne '0');
	}
	print<<END;
</td></table>
<hr>
<form action="$script" name="delform" method="POST" style="display:inline;">
<input type="hidden" name="id" value="$Fm{'id'}">
<a name="dform"></a>
- ãLéñÇÃï“èWÅEçÌèú -<br>
<input type="hidden" name="mode" value="custom">
ãLéñNo.<input type="text" name="no" size="8"> ÉpÉXÉèÅ[Éh<input type="password" size="8" name="pass"> <select name="dmode">
<option value="edit" selected>ãLéñï“èW</option>
<option value="delete">í èÌçÌèú</option>
<option value="pdelete">äÆëSçÌèú</option>
</select> 
<input type="submit" value="é¿çs">
</small>
</form>
END
	&footer;
	print<<END;
</body>
</html>
END
}

1;
