sub comwrite {
if($proxyban == 1) {
($kushi,$addr) = &cproxy;
&error('ÉvÉçÉLÉVÇégÇ¡ÇƒÇ¢ÇÈâ¬î\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB<br>ÉZÉLÉÖÉäÉeÉBè„ÅAÉvÉçÉLÉVÇégópÇµÇƒÇÃèëÇ´çûÇ›ÇÕÇ≤âìó∂Ç¢ÇΩÇæÇ¢ÇƒÇ®ÇËÇ‹Ç∑ÇÃÇ≈ÅA<br>ÉvÉçÉLÉVÇäOÇµÇƒÇ©ÇÁÅAçƒìxèëÇ´çûÇ›ÇäËÇ¢Ç‹Ç∑ÅB') if($kushi);
}
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
} elsif(length($Fm{'pass'}) > 8) {
$tmplength = length($Fm{'pass'});
&error("ÉpÉXÉèÅ[ÉhÇ™í∑Ç∑Ç¨Ç‹Ç∑ÅB<br>8Bytesà»ì‡Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
} elsif((length($Fm{'comment'}) < $minmsg) && ($Fm{'rno'} eq '')) {
$tmplength = length($Fm{'comment'});
&error("ÉÅÉbÉZÅ[ÉWÇ™è≠Ç»Ç∑Ç¨Ç‹Ç∑ÅB<br>ÉXÉåÉbÉhÇåöÇƒÇÈèÍçáÇÕÅA${minmsg}Bytesà»è„Ç…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(åªç›ÅF<b>${tmplength}</b>Bytes)");
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
} elsif($lasttime > time - $rewrite) {
$remainder =  $lasttime - time + $rewrite;
&error("òAë±èëÇ´çûÇ›ÇÕÅAÇ‡Ç§ébÇ≠ë“Ç¡ÇƒÇ©ÇÁÇ…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(å„<b>${remainder}</b>ïbå„Ç…ÅAèëÇ´çûÇ›â¬î\\)");
} elsif(($lastthr > time - $rethread) && ($Fm{'rno'} eq '')) {
$remainder =  $lastthr - time + $rethread;
&error("òAë±ÉXÉååöÇƒÇÕÅAÇ‡Ç§ébÇ≠ë“Ç¡ÇƒÇ©ÇÁÇ…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>(å„<b>${remainder}</b>ïbå„Ç…ÅAèëÇ´çûÇ›â¬î\\)");
}

&sendcookie;

$wicon = $icon[$Fm{'icon'}];
($wiconaddr,$wiconname) = split(/\,/,$wicon);
&spicon;

$wcolor = $color[$Fm{'color'}];

$cpass = crypt($Fm{'pass'},$crp) if($Fm{'pass'} ne '');
&gettime;
&lock;
open(LOG,"$multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@log = <LOG>;
close(LOG);
open(CNT,"$multif$count") or &error("èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉãÅF${multif}${count} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
$no = <CNT>;
close(CNT);
$no++;
$writefile = "$no\.$fileexp" if($Fm{'file'} ne '');
if($ucon == 1) {
open(UCN,"$multif$userc") or &error("óòópé“èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉãÅF${multif}${userc} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@uc = <UCN>;
close(UCN);
$ucf = 0;
foreach $tmpuc (@uc) {
($ucid,$ucname,$uccount,$uctimev,$uctimes) = split(/<>/,$tmpuc);
if($ucid eq $cpass) {
$uccount++;
$uctimes = time;
$tmpuc = "$cpass<>$Fm{'name'}<>$uccount<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>$uctimes<>\n";
$registusercount = $uccount;
$ucf = 1;
} else {
$tmpuc = '' if($uctimes < time - 60*60*24*$ucdel);
}
}
if($ucf == 0) {
if($Fm{'pass'} ne '') {
$uctimes = time;
push(@uc,"$cpass<>$Fm{'name'}<>1<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>$uctimes<>\n");
$registusercount = 1;
} else {
$registusercount = '';
}
}
@uc = reverse sort { (split(/<>/,$a))[2] <=> (split(/<>/,$b))[2] } @uc;

}

if($Fm{'rno'} eq '') {
#ãLéñNo.<>êeãLéñNo.<>éûä‘<>ñºëO<>ÉÅÅ[Éã<>ëËñº<>ÉRÉÅÉìÉg<>ÉEÉFÉuÉTÉCÉg<>ÉzÉXÉg<>ÉpÉXÉèÅ[Éh<>êF<>ÉAÉCÉRÉì<>
$tempcount = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
($raddr,$rhost,$lcount,$lfile) = split(/\,/,$lhost);
$tempcount++ if($lrno eq '');
if($tempcount >= $maxthr) {
$tmplog = '';
unlink("$uploaddir/$uploadid$lfile") if(($upbbs == 1) && ($lfile ne ''));
}
}
unshift(@log,"$no<>$Fm{'rno'}<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>$Fm{'name'}<>$Fm{'mail'}<>$Fm{'title'}<>$Fm{'comment'}<>$Fm{'hp'}<>$ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},$registusercount,$writefile<>$cpass<>$wcolor<>$wiconaddr<>\n");
} elsif($Fm{'sage'} eq 'sage') {
$findflag = 0;
$rescount = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
if(($lrno eq '') && ($findflag == 1)) {
$tmplog = "$no<>$Fm{'rno'}<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>$Fm{'name'}<>$Fm{'mail'}<>$Fm{'title'}<>$Fm{'comment'}<>$Fm{'hp'}<>$ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},$registusercount,$writefile<>$cpass<>$wcolor<>$wiconaddr<>\n$tmplog" if($rescount <= $maxres);
$findflag = 0;
last;
}
if(($lno eq $Fm{'rno'}) || ($lrno eq $Fm{'rno'})) {
$findflag = 1;
} else {
$findflag = 0;
}
if($lrno eq '') {
$rescount = 0;
} else {
$rescount++;
}

}
push(@log,"$no<>$Fm{'rno'}<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>$Fm{'name'}<>$Fm{'mail'}<>$Fm{'title'}<>$Fm{'comment'}<>$Fm{'hp'}<>$ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},$registusercount,$writefile<>$cpass<>$wcolor<>$wiconaddr<>\n") if($findflag == 1);

} else {
@templog = ();
$logcount = 0;
foreach $tmplog (@log) {
($lno,$lrno,$ltime,$lname,$lmail,$ltitle,$lcomment,$lhp,$lhost,$lpass,$lcolor,$licon) = split(/<>/,$tmplog);
if(($lno eq $Fm{'rno'}) || ($lrno eq $Fm{'rno'})) {
$templog[$logcount] = $tmplog;
$tmplog = '';
$logcount++;
}
}
push(@templog,"$no<>$Fm{'rno'}<>${year}/${mon}/${mday}(${weekday}) ${hour}:${min}:${sec}<>$Fm{'name'}<>$Fm{'mail'}<>$Fm{'title'}<>$Fm{'comment'}<>$Fm{'hp'}<>$ENV{'REMOTE_ADDR'},$ENV{'REMOTE_HOST'},$registusercount,$writefile<>$cpass<>$wcolor<>$wiconaddr<>\n");
@log = (@templog,@log);
}

open(LOG,"> $multif$log") or &error("ÉçÉOÉtÉ@ÉCÉãÅF${multif}${log} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print LOG @log;
close(LOG);
open(CNT,"> $multif$count") or &error("èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉãÅF${multif}${count} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print CNT $no;
close(CNT);
if($ucon == 1) {
open(UCN,"> $multif$userc") or &error("óòópé“èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉãÅF${multif}${userc} Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
print UCN @uc;
close(UCN);
}
if(($upbbs == 1) && ($Fm{'file'} ne '')) {
open(ULF,"> $uploaddir/$uploadid$no\.$fileexp") or &error("ìYïtÉtÉ@ÉCÉãÅF${uploaddir}/$uploadid$no\.$fileexp Ç÷ÇÃèëÇ´çûÇ›Ç…é∏îsÇµÇ‹ÇµÇΩÅB");
binmode(ULF);
print ULF $Cn{'file'};
close(ULF);
chmod("$uploaddir/$uploadid$no\.$fileexp", 0666);
}
&unlock;

if($Fm{'resback'} eq 'resback') {
&pagemove("$script?id=$Fm{'id'}&mode=res&rno=$Fm{'rno'}&#no$no");
} else {
&pagemove("$script?id=$Fm{'id'}");
}
}

1;
