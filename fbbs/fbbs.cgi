#!/usr/local/bin/perl

#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/#
#_/                                                              _/#
$ver =  "FortressBBS Ver4.07";#                                  _/#
#_/        çÏé“ÅF   ÉÅÉVÉX                                       _/#
#_/        ÉÅÅ[ÉãÅF mewsyoui@hotmail.com                         _/#
#_/        äJî≠å≥ÅF http://mesis.s41.xrea.com/                   _/#
#_/                                                              _/#
#_/        ã≠å≈ÇΩÇÈÉZÉLÉÖÉäÉeÉBÇå÷ÇÈåfé¶î¬ÅBÅEÅEÅEÇæÇ∆évÇ§      _/#
#_/        égÇ¢êSínÇÅAÇ»ÇÈÇ◊Ç≠YY-BoardÇ…éóÇπÇƒÇ†ÇÈÇ‡ÇÃÇÃÅA      _/#
#_/        Ç‚ÇÕÇËÇ‹Ç¡ÇΩÇ≠ÇÃï ï®Ç»ÇÃÇ≈ÅAÇøÇ∆égÇ¢Ç…Ç≠Ç¢Ç©Ç‡ÅB      _/#
#_/                                                              _/#
#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/#

# åfé¶î¬ÇÃéÌóﬁÅB
# 0Ç»ÇÁÅANormalå^ÅB
# 1Ç»ÇÁÅAMultiå^
$bbstype = 0;

# ëççáìIÇ»É^ÉCÉgÉãÇ≈Ç∑ÅB
# IDñ≥ãLì¸éûÇ…ÇÕÅAÇ±ÇÃÉ^ÉCÉgÉãÇ™égópÇ≥ÇÍÇ‹Ç∑ÅB
$title	= 'F-BBS';

# åfé¶î¬ÇÃàÍî‘è„Ç…ÅAÉRÉÅÉìÉgÇç⁄ÇπÇÈÇ©
# 0 Ç»ÇÁç⁄ÇπÇ»Ç¢
# 1 Ç»ÇÁç⁄ÇπÇÈ
$topon	= 0;

# åfé¶î¬ÇÃàÍî‘è„Ç…ç⁄ÇπÇÈÉRÉÅÉìÉg
$topcom = <<END;
åfé¶î¬Ç≈Ç∑ÅB
END

# åfé¶î¬ÇÃÉåÉìÉ^ÉãÇÇ∑ÇÈÇ©
# 0 ÇµÇ»Ç¢
# 1 Ç∑ÇÈ
$bbsrental = 0;

# åfé¶î¬ÉgÉbÉvÉRÉÅÉìÉgÇÃè„å¿ÉTÉCÉY
$topcommax = 2048;

# åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[ÉgÇÃè„å¿ÉTÉCÉY
$stylemax = 2048;

#-- à»â∫ÇÕÅAåfé¶î¬ÇÃéÌóﬁÇ≈1ÇëIÇÒÇæèÍçáÇÃê›íËÇ≈Ç∑ --#

# åfé¶î¬äÓñ{ê›íËÉtÉ@ÉCÉãñº
$bbssetup = 'bbsdata.cgi';

# åfé¶î¬ÇÃè„ïîÉRÉÅÉìÉg
$bbstopcom = 'bbscomment.cgi';

# åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[Égê›íËÉtÉ@ÉCÉã
$bbsstyle = 'bbsstyle.cgi';

# åfé¶î¬ê›íËópÉpÉXÉèÅ[Éh
$setpass = 'pass';

# åfé¶î¬ê›íËÉtÉ@ÉCÉãäiî[ÉtÉHÉãÉ_
$setupdir = 'setup';

# åfé¶î¬IDÇ™ñ¢ì¸óÕÇÃéûÇÃÅAÉ^ÉCÉgÉã
$noidtitle = 'ÉCÉìÉfÉbÉNÉX';

# åfé¶î¬IDÇ™ñ¢ì¸óÕÇÃèÍçáÇ…ï\é¶Ç≥ÇÍÇÈÉÅÉbÉZÅ[ÉWäiî[ÉtÉ@ÉCÉãñº
# èâä˙èÛë‘Ç»ÇÁÇŒÅAí èÌÇÕ indexcom.cgiÅAÉåÉìÉ^ÉãÉÇÅ[ÉhÇ»ÇÁ indexcomrental.cgi
$indexcom = 'indexcom.cgi';

#-- 1ÇëIÇÒÇæèÍçáÇÃëIëà»è„ --#

# É^ÉCÉgÉãÇÃëÂÇ´Ç≥ÅB1Å`7ÅBÉ^ÉCÉgÉãâÊëúÇégÇÌÇ»Ç¢èÍçáÇÕÅAê›íËïsóvÅB
$tsize	= 6;

# É^ÉCÉgÉãÇÃêFÅBÉ^ÉCÉgÉãâÊëúÇégÇÌÇ»Ç¢èÍçáÇÕÅAê›íËïsóvÅB
$tcolor	= '#888888';

# É^ÉCÉgÉãâÊëúÅBégÇÌÇ»Ç¢èÍçáÇÕÅAãÛóìÇ…ÇµÇƒÇ®Ç¢ÇƒÇ≠ÇæÇ≥Ç¢ÅB
$titlei = '';

# ä«óùêlñº
$adname	= 'ä«óùêl';

# ä«óùé“ÉÅÅ[ÉãÉAÉhÉåÉX
$admail	= 'Ç«Ç±Ç©@Ç«Ç¡Ç©.Ç«Ç¡Ç©';

# 1ÉyÅ[ÉWÇ…âΩåèï\é¶Ç∑ÇÈÇ©
$onep	= 5;

# 1Ç¬ÇÃÉXÉåÉbÉhÇ…ÅAÇ¢Ç≠Ç¬ÇÃÉåÉXÇï\é¶Ç∑ÇÈÇ©
# 0Ç»ÇÁñ≥êßå¿
$thdis	= 5;

# ãLéñÇÕÅAâΩçsí¥Ç¶ÇÈÇ∆è»ó™Ç≥ÇÍÇÈÇ©ÅB
# 0Ç»ÇÁè»ó™ÇµÇ»Ç¢
$redis	= 10;

# ç≈ëÂÉXÉåÉbÉhêîÅB
$maxthr	= 30;

# ÇPÇ¬ÇÃÉXÉåÉbÉhÇ…ëŒÇ∑ÇÈç≈ëÂÉåÉXêîÅB
# 0Ç»ÇÁñ≥êßå¿
$maxres = 100;

# åüçıÇ≈ÅAÇPÉyÅ[ÉWÇ…âΩåèï\é¶Ç∑ÇÈÇ©
$sonep	= 10;

# èëÇ´çûÇ›å„ÅAÇ«ÇÍÇ≈ÉyÅ[ÉWÇêÿÇËë÷Ç¶ÇÈÇ©
# 0 LocationÇ≈êÿÇËë÷Ç¶(êÑèß)
# 1 METAÇ≈êÿÇËë÷Ç¶
$afterw	= 0;

# ÉçÉbÉNÉfÉBÉåÉNÉgÉäÅB
$lockd	= 'lock';

# ÉçÉbÉNééçsâÒêî
$try	= 5;

# òAë±èëÇ´çûÇ›ä‘äuÅBïbêîÇ≈éwíËÅB
# 0Ç»ÇÁêßå¿ÇµÇ»Ç¢ÅB
$rewrite = 120;

# êVÇµÇ¢ÉXÉåÉbÉhÇåöÇƒÇÁÇÍÇÈä‘äuÅBïbêîÇ≈éwíËÅB
# 0Ç»ÇÁêßå¿ÇµÇ»Ç¢ÅB
#	    ïb ï™ éû ì˙
$rethread = 60*60*24*1;

# énÇﬂÇ…óòópãKñÒÇ…ä÷Ç∑ÇÈéøñ‚ÇçsÇ§Ç©ÅB
# 0 Ç»ÇÁçsÇÌÇ»Ç¢
# 1 Ç»ÇÁçsÇ§
$queson	= 0;

# >>(Number) Ç≈ï\é¶Ç≥ÇÍÇÈÉäÉìÉNÇ≈à⁄ìÆÇ∑ÇÈÉEÉCÉìÉhÉE
# 0 åªç›ÇÃÉEÉCÉìÉhÉEÇ≈à⁄ìÆ
# 1 êVÇµÇ¢ÉEÉCÉìÉhÉEÇ≈äJÇ≠
$targetlink = 0;

# ä«óùópÉpÉXÉèÅ[ÉhÇ≈Ç∑ÅB'pass'Çí«â¡ÇµÇƒÇ¢ÇØÇŒÅAï°êîçÏÇÍÇ‹Ç∑ÅB
# àÍî‘ç≈å„à»äOÇÕÅAå„ÇÎÇ… , ÇïtÇØÇƒÇ≠ÇæÇ≥Ç¢ÅB
@adpass	= (
'pass1',
'pass2' # ç≈å„ÇÕ , ÇÇ¬ÇØÇ»Ç¢
);

# ÉåÉtÉFÉâÅ[êßå¿ópÅB
# Ç±ÇÍÇ≈énÇ‹ÇÈÉAÉhÉåÉXÇ©ÇÁÇÃìäçeÅA
# Ç‹ÇΩÇÕÉåÉtÉFÉâÅ[Ç™ñ≥Ç¢èÍçá(ÉmÅ[ÉgÉìÉCÉìÉ^Å[ÉlÉbÉgÉZÉLÉÖÉäÉeÉBÅ[Ç»Ç«Ç≈)ÇµÇ©éÛÇØïtÇØÇ»Ç¢ÅB
# égópÇµÇ»Ç¢èÍçáÇÕÅAãÛóìÇ…ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB
$reff = '';

# âÊëúÇ™íuÇ¢ÇƒÇ†ÇÈÉfÉBÉåÉNÉgÉäÇéwíË
$imgdir	= 'http://Ç«Ç¡Ç©.Ç«Ç¡Ç©/';

# ñﬂÇËêÊÇÃÉyÅ[ÉWÇéwíË
$backpa	= 'http://Ç«Ç¡Ç©.Ç«Ç¡Ç©/';

# ñﬂÇËêÊÇÃÉyÅ[ÉWñºÇéwíË
$backpn = 'ÉzÅ[ÉÄÉyÅ[ÉW';

# ÉXÉ^ÉCÉãÉVÅ[ÉgÇÃê›íËÅB
$style = <<END;
body {
color:#000000; /* äÓñ{ìIÇ»ï∂éöêF */
font-size:10pt; /* äÓñ{ìIÇ»ï∂éöÇÃëÂÇ´Ç≥ */
background-color:#e0e0e0; /* îwåiêF */
}
td,th {
color:#000000; /* äÓñ{ìIÇ»ï∂éöêF */
font-size:10pt; /* äÓñ{ìIÇ»ï∂éöÇÃëÂÇ´Ç≥ */
}
small {
font-size:9pt; /* smallÉ^ÉOÇÃÅAëÂÇ´Ç≥ */
}
input,textarea {
font-family:'ÇlÇr ÇoÉSÉVÉbÉN'; /* ì¸óÕóìÇÃÉtÉHÉìÉg */
}
a:link {
color:#0000ff;
}
a:vlink {
color:#800080;
}
a:alink {
color:#ff0000;
}
END

# à√çÜâªÇ…ópÇ¢ÇÈï∂éöóÒÅBîºäpâpêîéöÇ≈2BytesÅAìKìñÇ…ì¸óÕÇµÇƒíuÇ¢ÇƒÇ≠ÇæÇ≥Ç¢ÅB
$crp	= 'fb';

# èëÇ´çûÇ›éûÇ…ÅAÉvÉçÉLÉVÇÁÇµÇ´Ç‡ÇÃÇÕíeÇ≠Ç©ÅB
# 0 íeÇ©Ç»Ç¢
# 1 íeÇ≠
$proxyban = 0;

# Ç®Ç»Ç‹Ç¶ÇÃç≈ëÂï∂éöêîÅBByteíPà 
$maxnam = 32;

# ÉÅÅ[ÉãÉAÉhÉåÉXÇÃç≈ëÂï∂éöêîÅBByteíPà 
$maxmai = 64;

# ÉzÅ[ÉÄÉyÅ[ÉWÉAÉhÉåÉXÇÃç≈ëÂï∂éöêîÅBByteíPà 
$maxhpa = 128;

# É^ÉCÉgÉãÇÃç≈ëÂï∂éöêîÅBByteíPà 
$maxtit = 64;

# ÉXÉååöÇƒÇÃç€ÇÃÅAÉÅÉbÉZÅ[ÉWÇÃç≈í·ï∂éöêîÅBByteíPà 
$minmsg = 128;

# ÉÅÉbÉZÅ[ÉWÇÃç≈ëÂï∂éöêîÅBByteíPà 
$maxmsg = 5120;

# ÉÅÉbÉZÅ[ÉWÇÃç≈í·â¸çsêîÅB
# 0Ç»ÇÁàÍçsÉXÉåÅEÉåÉXâ¬
$minret = 0;

# ÉÅÉbÉZÅ[ÉWÇÃç≈ëÂâ¸çsêîÅB
$maxret = 50;

# óòópé“èëÇ´çûÇ›âÒêîÇï\é¶Ç∑ÇÈÇ©ÅB
$ucon	= 1;

# óòópé“èëÇ´çûÇ›âÒêîÇ≈ÅAâΩì˙ä‘èëÇ´çûÇÒÇ≈Ç¢Ç»Ç¢êlÇÃÉfÅ[É^ÇçÌèúÇ∑ÇÈÇ©ÅB
$ucdel	= 30;

# ÉAÉbÉvÉçÅ[Éhã@î\ÇégÇ§Ç©
# 0 Ç»ÇÁégÇÌÇ»Ç¢
# 1 Ç»ÇÁégÇ§
$upbbs = 1;

# ÉAÉbÉvâ¬î\ç≈ëÂÉtÉ@ÉCÉãÉTÉCÉY(Bytes)
$maxup = 4096;

# ÉAÉbÉvâ¬î\ÉtÉ@ÉCÉãägí£éq
@upexp = ('txt','gif','jpg','jpeg','png');

# ÉAÉbÉvÉçÅ[ÉhÉtÉ@ÉCÉãäiî[ÉtÉHÉãÉ_(ëäëŒÉpÉX(./Å`ÅA../Å`))
$uploaddir = './upload';

# ÉAÉbÉvÉçÅ[ÉhÉtÉ@ÉCÉãäiî[ÉtÉHÉãÉ_(ê‚ëŒÉpÉX(http://Å`)ÅAÇ‹ÇΩÇÕëäëŒÉpÉX(./Å`ÅA../Å`))
$uploadhttp = './upload';

# ÉAÉCÉRÉìÇégópÇ∑ÇÈÇ©ÅB
$iconon	= 1;

# êÍópÉAÉCÉRÉìÇ≈Ç∑ÅB'pass,icon'Çí«â¡ÇµÇƒÇ¢ÇØÇŒÅAï°êîçÏÇÍÇ‹Ç∑ÅB
@spicon = (
'pass1,admin.gif',
'pass2,subadmin.gif' # ç≈å„ÇÕ , ÇÇ¬ÇØÇ»Ç¢
);

# ÉAÉCÉRÉìÇ≈Ç∑ÅB
@icon	= (
',ÉAÉCÉRÉìÇ»Çµ',
'icon1.gif,ÉAÉCÉRÉìÇP',
'icon2.gif,ÉAÉCÉRÉìÇQ',
'icon3.gif,ÉAÉCÉRÉìÇR',

'special,êÍópÉAÉCÉRÉì'
);

# ï∂éöêFÅB
@color	= (
'#bbbbbb','#ff8888','#ffff88','#88ff88','#88ffff','#8888ff','#ff88ff',
'#888888','#ff0000','#ffff00','#00ff00','#00ffff','#0000ff','#ff00ff',
'#000000','#880000','#888800','#008800','#008888','#000088','#880088'
);

# égópãñâ¬Ç∑ÇÈÉ^ÉO
@oktag = (
'b','i','u','s'
);

# ñ{ëÃÇÃñºëO
$script	= 'fbbs.cgi';

# ÉÅÉCÉìÉâÉCÉuÉâÉäÇÃñºëO
$mailib	= 'fmai.cgi';

# èëÇ´çûÇ›ópÉâÉCÉuÉâÉäÇÃñºëO
$reglib	= 'freg.cgi';

# ãLéñï“èWÅEçÌèúópÉâÉCÉuÉâÉäÇÃñºëO
$cuslib	= 'fcus.cgi';

# ä«óùópÉâÉCÉuÉâÉäÇÃñºëO
$admlib	= 'fadm.cgi';

# ÉIÉvÉVÉáÉìópÉâÉCÉuÉâÉäÇÃñºëO
$etclib	= 'fetc.cgi';

# Multiåfé¶î¬ê›íËÉâÉCÉuÉâÉäÇÃñºëO
$setlib	= 'fset.cgi';

# åfé¶î¬ÉåÉìÉ^ÉãÉtÉHÅ[ÉÄópÉâÉCÉuÉâÉäÇÃñºëO
$rntlib	= 'frnt.cgi';

# ÉçÉOÉtÉ@ÉCÉãñº
$log	= 'fbbs.log';

# ÉJÉEÉìÉgâÒêîãLò^ÉtÉ@ÉCÉãñº
$count	= 'fbbs.cnt';

# ÉAÉNÉZÉXãKêßÉfÅ[É^
$ipban	= 'fbbs.dat';

# èëÇ´çûÇ›âÒêîãLò^ÉtÉ@ÉCÉã
$userc	= 'fbbs.ucn';

# åfé¶î¬ÉgÉbÉvÉRÉÅÉìÉgê›íËÉtÉ@ÉCÉã
$bbstopcom = 'bbstopcom.cgi';

# åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[Égê›íËÉtÉ@ÉCÉã
$bbsstyle = 'bbsstyle.cgi';

# ï∂éöÉRÅ[Éh
$wcode	= 'Shift_Jis';

# óòópãKñÒÇÃï∂ÅB
$agmcom	= <<END;
<table summary="ï\\" border="0" cellspacing="16" cellpadding="0" style="background-color:#ffffff;">
<tr><td>
ñ{åfé¶î¬ÇóòópÇ∑ÇÈÇ…ìñÇΩÇËÅAéüÇÃÇ±Ç∆Ç…íçà”ÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br><br>
ÅEäÓñ{ìIÇ…ÅAëºêlÇÃñ¿òfÇ…Ç»ÇÈÇ±Ç∆ÇÇµÇ»Ç¢ÅB<br>
ÅEÇ±ÇÃåfé¶î¬Ç≈ÇÕÅA<b>b , i , s , u</b> à»äOÉ^ÉOÇÕÅAégópÇ≈Ç´Ç‹ÇπÇÒÅBÇ≤óπè≥Ç≠ÇæÇ≥Ç¢ÅB<br><br>

ÅEï∂ÇÅA<b>&lt;&gt;Å`&lt;/&gt;</b>Ç≈àÕÇ¶ÇŒÅAçïÇ≠ìhÇËÇ¬Ç‘Ç≥ÇÍÇ‹Ç∑ÅBÉlÉ^ÇŒÇÍèÓïÒÇç⁄ÇπÇÈéûÇ»Ç«Ç…ÅAÇ≤égópÇ≠ÇæÇ≥Ç¢ÅB<br><br>
</td>
</table>
END

# ÉAÉNÉZÉXãKêßÇ…Ç©Ç©Ç¡ÇΩêlÇ™ï\é¶Ç≥ÇÍÇÈÉÅÉbÉZÅ[ÉW
$ipbm	= <<END;
<div align="center">
<font size="6" color="red">
ÉGÉâÅ[
</font>
<br><br>
ÉAÉNÉZÉXãëî€Ç≥ÇÍÇ‹ÇµÇΩÅB<br>
óòópãKñÒÇ…à·îΩÇµÇΩâ¬î\\ê´Ç™Ç†ÇËÇ‹Ç∑ÅB<br>
óòópãKñÒÇ…à·îΩÇµÇΩäoÇ¶Ç™Ç»Ç¢ÇÃÇ…ÅAÇ±ÇÃÉÅÉbÉZÅ[ÉWÇ™ï\\é¶Ç≥ÇÍÇΩÇ»ÇÁÅA<br>
Ç®ñºëO(HN)ìôÇìYÇ¶ÇƒÅA<a href="mailto:$admail">$adname</a>Ç…òAóçÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB<br>
Ç±ÇøÇÁÇ≈í≤Ç◊ÇΩè„Ç≈ÅAâèúÇåüì¢ÇµÇ‹Ç∑ÅB
<hr>
- óòópãKñÒëSï∂ -<br><br>
$agmcom
<hr>
<a href="$backpa">$backpn</a>Ç÷ñﬂÇÈ
</div>
END


@ques	= (); @cand	= (); @answ	= ();
$ques[0] = 'çrÇÁÇµÇ™èoÇΩÇÁÅAÇ«Ç§ëŒèàÇ∑ÇÍÇŒÇÊÇ¢ÇÃÇ©ÅH'; # ñ‚ëËï∂
$cand[0] = 'çrÇÁÇµÇÃçsà◊ÇÕñ≥éãÇµÅA<br>çÌèúêlÇ…òAóçÇ∑ÇÈÅB<>çrÇÁÇµÇ…ï∂ãÂÇåæÇ¡ÇƒÅA<br>çrÇÁÇµÇåÇëﬁÇ∑ÇÈÅB<>Ç¢Ç¡ÇµÇÂÇ…çrÇÁÇ∑ÅB'; # âÒìöåÛï‚
$answ[0] = 1; # ê≥âÇÃî‘çÜÅB

$ques[1] = 'ÅuÇÕÇ∂ÇﬂÇ‹ÇµÇƒÅvÇÃÇ†Ç¢Ç≥Ç¬ÇÕÅAÇ«ÇÍÇ≈Ç∑ÇÈÇÃÇ™çDÇ‹ÇµÇ¢ÅH';
$cand[1] = 'êVãKÉXÉåÉbÉhÇ≈ÅA<br>Ç†Ç¢Ç≥Ç¬ÇÇ∑ÇÈÅB<>Ç†Ç¢Ç≥Ç¬ÇæÇØÇÃì‡óeÇ…ÇπÇ∏ÅA<br>ï ÇÃì‡óeÇ‡ä‹ÇﬂÇƒÇ†Ç¢Ç≥Ç¬Ç∑ÇÈÅB<>Ç†Ç¢Ç≥Ç¬ópÇÃÉXÉåÉbÉhÇíTÇµÇƒÅA<br>ÇªÇ±Ç≈Ç†Ç¢Ç≥Ç¬ÇÇ∑ÇÈÅB';
$answ[1] = 3;

$ques[2] = 'éøñ‚ÇÇ∑ÇÈèÍçáÅAÇªÇÃéËèáÇÕÅH';
$cand[2] = 'Ç∑ÇÆÇ…éøñ‚Ç∑ÇÈÅB<>åªçsÉçÉOÅEâﬂãéÉçÉOÇíTÇ∑ìôÅA<br>Ç≈Ç´ÇÈÇ±Ç∆ÇÇµÇΩè„Ç≈ÅA<br>å©Ç¬Ç©ÇÁÇ»ÇØÇÍÇŒÅA<br>éøñ‚Ç∑ÇÈÅB<>éøñ‚ÇÇµÇƒÅA<br>âÒìöÇ™ï‘Ç¡ÇƒÇ±Ç»Ç¢Ç»ÇÁÅA<br>é©ï™Ç≈í≤Ç◊ÇÈÅB';
$answ[2] = 2;

#$ques[] = ''; # ñ‚ëËÅB
#$cand[] = '<><>'; # <>Ç≈ãÊêÿÇËÅAÇRÇ¬ÅAâÒìöåÛï‚ÇçÏÇÈÅB
#$answ[] = ; # ê≥âÇÃî‘çÜ

#-- à»â∫ÇÕÉvÉçÉOÉâÉÄñ{ëÃÇ≈Ç∑ÅBñ≥à≈Ç…Ç¢Ç∂ÇÈÇ∆ÅAÉGÉâÅ[Ç…Ç»ÇÈÇ©Ç‡ÇµÇÍÇ‹ÇπÇÒÅB --#

$multif = '';

$upexplist = join(', ', @upexp);

&decode; # ÉfÉRÅ[ÉhåƒèoÅB$Fm{'ñºëO'}Ç…ÅAÉfÅ[É^Çì¸ÇÍÇ‹Ç∑ÅB
&decodecookie; # ÉNÉbÉLÅ[ì«Ç›çûÇ›ÅB

$uploadid = '';
if(($Fm{'mode'} eq 'setup') && ($bbstype == 1)) {
require $setlib; &setup;
} elsif(($Fm{'mode'} eq 'rentedit') && ($bbstype == 1) && ($bbsrental == 1)) {
require $rntlib; &rentedit;
} elsif($Fm{'mode'} eq 'admin') {
&multiload if($bbstype == 1);
require $admlib; &admin;
} elsif($Fm{'mode'} eq 'check') {
require $etclib; &check;
} elsif(($Fm{'id'} eq '') && ($bbstype == 1) && (($cflag eq 'ok') || ($queson == 0))) {
open(INC,$indexcom) or &error("ÉCÉìÉfÉbÉNÉXÉRÉÅÉìÉgÉfÅ[É^ÅF${indexcom} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@indexcom = <INC>;
close(INC);
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>$noidtitle - ${title}</title>
</head>
<body>
END
foreach $tmpindexcom (@indexcom) {
print $tmpindexcom;
}
&footer;
print<<END;
</body>
</html>
END
exit;
} elsif((!-e "${setupdir}/$Fm{'id'}/${bbssetup}") && ($bbstype == 1) && (($cflag eq 'ok') || ($queson == 0))) {
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
ÇªÇÃIDÇÃåfé¶î¬Ç™å©Ç¬Ç©ÇËÇ‹ÇπÇÒÇ≈ÇµÇΩÅB(ID:$Fm{'id'})<br><br>
<a href="$script">ñﬂÇÈ</a>
END
&footer;
print<<END;
</body>
</html>
END
exit;
} elsif(($cflag eq 'ok') || ($queson == 0)) {
&multiload if($bbstype == 1);
open(IPB,"$multif$ipban") or &error("ÉAÉNÉZÉXãKêßÉfÅ[É^ÅF$multif${ipban} ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@ipb = <IPB>;
close(IPB);

foreach $ipbdata (@ipb) {
$ipbdata =~ s/\ //g; $ipbdata =~ s/\r//g; $ipbdata =~ s/\n//g;
($ipb,$ipcom) = split(/\#/,$ipbdata);
if(($ENV{'REMOTE_ADDR'} =~ /^${ipb}/) || ($ENV{'REMOTE_HOST'} =~ /^${ipb}/)) {
&ipban;
}
}

if($Fm{'mode'} eq 'comwrite')				{ require $reglib; &comwrite;	}
elsif($Fm{'mode'} eq 'res')				{ require $mailib; &res;	}
elsif($Fm{'mode'} eq 'custom')				{ require $cuslib; &custom;	}
elsif($Fm{'mode'} eq 'edit')				{ require $cuslib; &edit;	}
elsif($Fm{'mode'} eq 'move')				{ require $cuslib; &move;	}
elsif($Fm{'mode'} eq 'delete')				{ require $cuslib; &delete;	}
elsif($Fm{'mode'} eq 'pdelete')				{ require $cuslib; &pdelete;	}
elsif($Fm{'mode'} eq 'search')				{ require $etclib; &search;	}
elsif($Fm{'mode'} eq 'numbers')				{ require $etclib; &numbers;	}
elsif(($Fm{'mode'} eq 'iconlist') && ($iconon == 1))	{ require $etclib; &iconlist;	}
elsif(($Fm{'mode'} eq 'alluc') && ($ucon == 1))		{ require $etclib; &alluc;	}
elsif($Fm{'mode'} eq 'agreement')			{ require $etclib; &agreement;	}
elsif($Fm{'mode'} eq 'cookiedel')			{
print "Set-Cookie: FortressBBS=$cookie; expires=, Thu, 01-Jan-1970 00:00:00 GMT;\n";
&pagemove("$script");
}
else							{ require $mailib; &main;	}
} else {
if($Fm{'mode'} eq 'cookie')				{ require $etclib; &setcookie;	}
elsif($Fm{'mode'} eq 'question')			{ require $etclib; &question;	}
else							{ require $etclib; &agreement;	}
}

sub multiload {
$multif = "${setupdir}/$Fm{'id'}/";
open(BSU,"${multif}$bbssetup") or &error("åfé¶î¬ê›íËÉtÉ@ÉCÉãÅF${multif}$bbssetup ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
my($icon,$color,$spicon,$adpass);
($title,$topon,$tcolor,$titlei,$adname,$admail,$imgdir,$backpa,$backpn,$upbbs,$spicon,$icon,$color,$adpass,$editpass) = split(/<>/,<BSU>);
close(BSU);
@icon = split(/\:/,$icon);
@color = split(/\:/,$color);
@spicon = split(/\:/,$spicon);
@adpass = split(/\:/,$adpass);
open(TCM,"${multif}$bbsstyle") or &error("åfé¶î¬ÉXÉ^ÉCÉãÉVÅ[Égê›íËÉtÉ@ÉCÉãÅF${multif}$bbsstyle ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@style = <TCM>;
close(TCM);
$style = '';
foreach $tmpstyle (@style) { $style .= $tmpstyle; }
open(TCM,"${multif}$bbstopcom") or &error("åfé¶î¬ÉRÉÅÉìÉgÉtÉ@ÉCÉãÅF${multif}$bbstopcom ÇÃÉIÅ[ÉvÉìÇ…é∏îsÇµÇ‹ÇµÇΩÅB");
@topcom = <TCM>;
close(TCM);
$topcom = '';
foreach $tmptopcom (@topcom) { $topcom .= $tmptopcom; }
}

sub ipban {
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
${ipbm}
END
&footer;
print<<END;
</body>
</html>
END
exit;
}

sub error {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
END
&header;
print<<END;
<title>ÉGÉâÅ[ Å| ${title}</title>
</head>
<body>
$_[0]
<br><br>
<a href="$script?id=$Fm{'id'}">ñﬂÇÈ</a>
END
&footer;
print<<END;
</body>
</html>
END
exit;
}

sub lock {
$endcount = 0;
until(mkdir("$multif$lockd",0777)) {
if($try > $endcount) {
$endcount++;
sleep 1;
if (-e "$multif$lockd") {
$locktime = (stat "$multif$lockd")[9];
	&unlock if($locktime < time - 30);
}
} else {
&error('ÉçÉbÉNíÜÇ≈Ç∑ÅB<br>Ç‡Ç§ÇµÇŒÇÁÇ≠ë“Ç¡ÇƒÇ©ÇÁÅAçƒééçsÇµÇƒÇ≠ÇæÇ≥Ç¢ÅB');
}
}
}

sub unlock {
rmdir("$multif$lockd");
}

sub spicon {
$spflag = 0;
if($wiconaddr eq 'special') {
foreach $spdata (@spicon) {
($tmpsppass,$tmpspicon) = split(/\,/,$spdata);
if($Fm{'pass'} eq $tmpsppass) {
$spflag = 1;
last;
}
}
if($spflag == 1) {
$wiconaddr = $tmpspicon;
} else {
$wiconaddr = '';
}
}
}

sub quotation {
@lcomment = split(/<br>/,$lcomment);
$lcomment = '';
foreach $tcomment (@lcomment) {
$tmpctop = substr($tcomment, 0, 1);
$tmpctoptwo = substr($tcomment, 0, 2);
$tmpctopfour = substr($tcomment, 0, 4);
if(($tmpctopfour eq '&gt;') || ($tmpctop eq '>') || ($tmpctoptwo eq 'ÅÑ')) {
$tcomment = "<font style=\"color:#888800;background-color:ffffff;\">$tcomment</font><br>\n";
} else {
$tcomment .= "<br>\n";
}
$lcomment .= $tcomment;
}
return;
}

sub jumper {
my($jno) = ($lrno eq '') ? $lno : $lrno;
my($tl) = ($targetlink == 1) ? ' target="_blank"' : '';
$lcomment =~ s/&gt;&gt;([0-9\-]+)/<a href="$script?id=$Fm{'id'}&amp;mode=numbers&amp;n=\1&amp;t=$jno&amp;page=0"${tl}>&gt;&gt;\1<\/a>/g;
$lcomment =~ s/\*&gt;([0-9\-]+)/<a href="$script?id=$Fm{'id'}&amp;mode=numbers&amp;n=\1&amp;page=0"${tl}>\*&gt;\1<\/a>/g;
$lcomment =~ s/((?:http|https|ftp|news)\:\/\/[\w\/\.\~\-\_\?\&\+\=\#\@\%\*\:\;]+)/<a href="$script?id=$Fm{'id'}&mode=check&amp;uri=\1" target="_blank">\1<\/a>/g;
}

sub header {
print<<END;
<LINK REV="MADE" HREF="mailto:$admail"> 
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=$wcode">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<STYLE TYPE="text/css">
<!--
$style
-->
</STYLE>
END
}

sub footer {
print"<p align=\"right\" style=\"font-size:12px;\">ä«óùé“ÅF<a href=\"mailto:$admail\">$adname</a> <a href=\"http://mesis.s41.xrea.com/\" target=\"_blank\">${ver}</a></p>\n";
}

sub sendcookie {

    local ($sec,$min,$hour,$mday,$mon,$year,$wday) = gmtime(time + 3*30*24*60*60); # ÇRÉñåé
    $wday = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday];
    $mon = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mon];
    local $expiredate = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",$wday,$mday,$mon,$year+1900,$hour,$min,$sec);

    $lasttime = ($Fm{'mode'} eq 'setcookie') ? 0 : time;
    $lastthr = ($Fm{'mode'} eq 'setcookie') ? 0 : time if($Fm{'rno'} eq '');
    local $cookie = join("<>",'ok',$Fm{'name'},$Fm{'mail'},$Fm{'hp'},$Fm{'pass'},$Fm{'color'},$Fm{'icon'},$lasttime,$lastthr);

    $cookie =~ tr/\x0A\x0D//;
    $cookie =~ s/(\W)/'%' . unpack('H2',$1)/eg;
    $cookie =~ tr/ /+/;
    
    print "Set-Cookie: FortressBBS=$cookie; expires=$expiredate\n";
}

sub decodecookie {
    local $cname,$cvaule;
    for (split(/; */,$ENV{'HTTP_COOKIE'})) {
        ($cname,$cvalue) = split(/=/,$_);
	if ($cname eq 'FortressBBS') {
        last;
	} else {
	$cname = ''; $cvalue = '';
	}
    }
    $cvalue =~ tr/+/ /;
    $cvalue =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

    ($cflag,$name,$mail,$hp,$pass,$color,$icon,$lasttime,$lastthr) = split(/<>/,$cvalue);

    for ($cflag,$name,$mail,$hp,$pass,$color,$icon,$lasttime,$lastthr) {
        local $tmp = $_;
        $_ = $tmp;
        $_ =~ s/&/&amp;/g;
        $_ =~ s/>/&gt;/g;
        $_ =~ s/</&lt;/g;
        $_ =~ s/\"/&quot;/g;
    }
}

sub gettime {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time);
$mon++;
$year += 1900;
$min=sprintf("%.2d",$min);
$sec=sprintf("%.2d",$sec);
$hour=sprintf("%.2d",$hour);
if($wday == 0) {
$weekday = 'ì˙';
} elsif($wday == 1) {
$weekday = 'åé';
} elsif($wday == 2) {
$weekday = 'âŒ';
} elsif($wday == 3) {
$weekday = 'êÖ';
} elsif($wday == 4) {
$weekday = 'ñÿ';
} elsif($wday == 5) {
$weekday = 'ã‡';
} elsif($wday == 6) {
$weekday = 'ìy';
} else {
$weekday = '[ïsñæ]';
}
}

sub pagemove {
if($afterw == 1) {
print"Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="refresh" CONTENT="1; URL=$_[0]">
END
&header;
print<<END;
<title>êÿÇËë÷Ç¶íÜ - ${title}</title>
</head>
<body>
<div align="center">
ÉyÅ[ÉWêÿÇËë÷Ç¶íÜÇ≈Ç∑ÅB<br>
ÇµÇŒÇÁÇ≠Ç®ë“ÇøÇ≠ÇæÇ≥Ç¢...<br><br>
<a href="$_[0]">ã≠êßêÿÇËë÷Ç¶</a>
END
&footer;
print<<END;
</div>
</body>
</html>
END
} else {
print"Location: $_[0]\n\n";
}
}

sub expcheck {
my($exp) = $_[0];
my($upexp);
foreach $upexp (@upexp) {
return 1 if($exp eq $upexp);
}
return 0;
}

sub cproxy {
my($proxy) = 0;
my($rtn, $strH);

if($ENV{'HTTP_USER_AGENT'} =~ /via|squid|delegate|httpd|proxy|cache|gateway|www|ANONYM|keeper/i){
$rtn = 1;
} elsif($ENV{'REMOTE_HOST'} =~ /^dns|^gw|^fw|^ns|^news|^web|^secure|cgi|ftp|pop|cache|dummy|firewall|gate|www|keep|mail|proxy|prox|smtp|squid|w3/i){
$rtn=1;
} elsif($ENV{'HTTP_FORWARDED'}) {
$rtn=1;
} elsif($ENV{'HTTP_VIA'}) {
$rtn=1;
} elsif($ENV{'HTTP_X_FORWARDED_FOR'}) {
$rtn=1;
} elsif($ENV{'HTTP_MAX_FORWARDS'}) {
$rtn=1;
} elsif($ENV{'HTTP_SP_HOST'}) {
$rtn=1;
} elsif($ENV{'HTTP_CLIENT_IP'}) {
$rtn=1;
} elsif($ENV{'HTTP_CACHE_INFO'}) {
$rtn=1;
} elsif($ENV{'HTTP_PROXY_CONNECTION'}) {
$rtn=1;
} elsif($ENV{'HTTP_XROXY_CONNECTION'}) {
$rtn=1;
} elsif($ENV{'HTTP_TE'}) {
$rtn=1;
} elsif($ENV{'HTTP_PROXY_AUTHORIZATION'}) {
$rtn=1;
} elsif($ENV{'HTTP_X_CISCO_BBSM_CLIENTIP'}) {
$rtn=1;
} elsif($ENV{'HTTP_X_HTX_AGENT'}) {
$rtn=1;
} elsif($ENV{'HTTP_EXTENSION'}) {
$rtn=1;
} elsif($ENV{'HTTP_XONNECTION'}) {
$rtn=1;
} elsif($ENV{'HTTP_X_LOCKING'}) {
$rtn=1;
}

if($ENV{'HTTP_WEFERER'}) {
$rtn+=2;
} elsif($ENV{'HTTP_WSER_AGENT'}) {
$rtn+=2;
}

$strH = $ENV{'HTTP_SP_HOST'} if($ENV{'HTTP_SP_HOST'} ne '');
$strH = $ENV{'HTTP_VIA'} if($ENV{'HTTP_VIA'} =~ s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/);
$strH = $ENV{'HTTP_CLIENT_IP'} if($ENV{'HTTP_CLIENT_IP'} =~ s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/);
$strH = $ENV{'HTTP_X_FORWARDED_FOR'} if($ENV{'HTTP_X_FORWARDED_FOR'} =~ s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/);
$strH = $ENV{'HTTP_FORWARDED'} if($ENV{'HTTP_FORWARDED'} =~ s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/);
$strH = $ENV{'HTTP_FROM'} if($ENV{'HTTP_FROM'} ne '');
if($rtn == 0) {
$strH = $ENV{'REMOTE_ADDR'};
}

return ($rtn, $strH);
}

sub decode {
	# ÉfÉRÅ[Éh
	if($ENV{'CONTENT_TYPE'} =~ /multipart\/form\-data\; boundary\=(.*)/) {
		my(@decode) = <STDIN>;
		my($bound) = "\-\-$1";
		my($count) = 0;
		my($decode,$name,$file,$type);
		foreach $decode (@decode) {
			if($decode =~ /^$bound/) {
				if($count == 0) {
					next;
				} else {
					if($type eq 'file') {
						$Cn{$name} =~ s/\r\n$/\n/;
						$Cn{$name} =~ s/\r$/\n/;
						$Cn{$name} =~ s/\n$//;
					} elsif($type eq 'text') {
						$Fm{$name} =~ s/\r\n$/\n/;
						$Fm{$name} =~ s/\r$/\n/;
						$Fm{$name} =~ s/\n$//;
					}
				next;
				}
			}
			if($decode =~ /Content\-Disposition\: form\-data\; name\=\"(.*?)\"\; filename\=\"(.*?)\"/) {
				$name = $1;
				$file = $2;
				$type = 'file';
				$Fm{$name} = $file;
				$Cn{$name} = '';
				$count = 0;
				next;
			} elsif($decode =~ /Content\-Disposition\: form\-data\; name\=\"(.*?)\"/) {
				$name = $1;
				$file = '';
				$type = 'text';
				$Fm{$name} = '';
				$count = 1;
				next;
			}
			$count++;
			next if($count < 3);
			if($type eq 'file') {
				$Cn{$name} .= $decode;
				next;
			} elsif($type eq 'text') {
				$decode     =~ s/\&/\&amp\;/g;
				$decode     =~ s/</\&lt\;/g;
				$decode     =~ s/>/\&gt\;/g;
				$decode     =~ s/\"/\&quot\;/g;
				$Fm{$name} .= $decode;
				next;
			}
		}
	} elsif ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $buffer);
	} else { @pairs = split(/&/, $ENV{'QUERY_STRING'}); }

	foreach $pair (@pairs) {
		my($name, $value) = split(/=/, $pair);
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		$value     =~ s/\&/\&amp\;/g;
		$value     =~ s/</\&lt\;/g;
		$value     =~ s/>/\&gt\;/g;
		$value     =~ s/\"/\&quot\;/g;
		$Fm{$name} = $value if($Fm{$name} eq '');
	}
	$Fm{'comment'} =~ s/\r\n/<br>/g;
	$Fm{'comment'} =~ s/\r/<br>/g;
	$Fm{'comment'} =~ s/\n/<br>/g;

	$Fm{'comment'} =~ s/\&lt\;\&gt\;(.*?)\&lt\;\/\&gt\;/<font style=\"color:#000000;background-color:#000000;\">\1<\/font>/g;

	foreach $oktag (@oktag) {
		$Fm{'comment'} =~ s/\&lt\;${oktag}\&gt\;(.*?)\&lt\;\/${oktag}\&gt\;/<${oktag}>\1<\/${oktag}>/g;
	}

	return;
}
