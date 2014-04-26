#!/usr/local/bin/perl

$arrange_name = "Error_Check EX v1.2"; ## (2001/07/07)

##オリジナル著作
$script_name = "Error_Check Version 1.1";   #(99/12/05)
# Programmed by Jynichi Sakai(あっぽー)
# E-Mail   : caa95880@pop06.odn.ne.jp
# Homepage : お蕎麦屋あっぽー庵ＷＷＷ（http://appoh.execweb.cx/）
#
#  1.このスクリプトは自分で使うために作者に承諾なしに自由に改造することが
#    できます。ただし、この著作権表示は消さないで下さい。
#  2.また、このスクリプトの使用に際して生じた いかなる損害に対しても、
#    作者は責任を負いません。 再配布に関しては、一言、ご連絡ください。
# --------------------------------------------------------------------

#★#アレンジ著作
#$arrange_name = "Error_Check EX v1.2"; ## (2001/07/07)
## Edited by かっちん
## E-Mail: zap14631@nifty.com
## http://www.infosakyu.ne.jp/~kattin/

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者(かっちん）は一切の責任を負いません。
# 2. その他は上記オリジナルスクリプトの使用条件に準じます。
# 3. このスクリプトは、オリジナル著作者あっぽーさんの許可を得て再配布されています。
#---------------------------------------------------------------#

##このファイルの名前指定します。
###変更した場合は、ファイル名をきちんと変えること

$thisfile = "check_ex.cgi";

##デフォルト検索ファイル名
##（テキストボックスを空白でチェッカー起動した場合の検索ファイル）
##必ず変更設定してください。

$cgi = "index.cgi";

##テキストボックス入力時の拡張子入力を必要とするかどうか(デフォルトは必要なし）
$kakutyousi = 1; ### 行頭のコメントアウトをはずすと、拡張子入力必要。

#--------------------------------------☆ 初期設定はここまで
$F{'mode'} = "surrender";
$F{'id'} = "BBB00000";
$F{'pass'} = "mesisp";
$F{'room'} = "t2";
&header;

# フォームに指定したファイル名を、検索ファイル名変数に代入します。
if ($ENV{'REQUEST_METHOD'} eq "POST") {
&cgiinput;
&error_check;
}
&html_footer;
exit;

#--------------------------------------☆ ＨＴＭＬのヘッダー
sub header{

if($kakutyousi == 1){
$select = ".cgi";
}else{
$comment = "※** 拡張子(.cgi)は、自動的に付加されますので入力不要。";
}
    print <<"_HEADER_";
Content-type: text/html

<HTML><HEAD>
<!--<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=euc-jp">-->
<TITLE>Perlチェッカー</TITLE>
</HEAD>
<BODY BGCOLOR="#ccccff" TEXT="#000000" LINK="#0000FF" ALINK="#008000">
<BASEFONT SIZE=3 FACE="ＭＳ ゴシック">
ファイル名空白時の検索ファイル名: [<b> $cgi </b>]  
<form method="post" action="$thisfile">
ファイル名:<input type="text" name="checking" value="">
<input type="submit"" value="チェッカ－起動"> ★同一フォルダ内のファイルしかエラーチェック不可です。
</form>
入力例 : <b><font color="#3333cc">appoh${select}</font></b> と入力すると、<b><font color="#cc0000">./</font><font color="#3333cc">appoh.cgi</font></b> を検索。<br>
$comment
<hr>
_HEADER_
}


#--------------------------------------☆ ＨＴＭＬのフッター
sub html_footer{
    print<<"_FOOTER_";
<DIV ALIGN="right">
<TT>$script_name<BR>
 [
<!-- 下の著作権表\示は書き換え禁止です -->
 著作：<A HREF="http://appoh.execweb.cx/" TARGET="_blank">あっぽー</A>
  ］</TT><br>
<TT>$arrange_name
 [
<!-- 下の著作権表\示は書き換え禁止です -->
Edited by <A HREF="http://www.infosakyu.ne.jp/~kattin/" TARGET="_blank">かっちん</A>
  ］</TT>
</DIV></BASEFONT>
</BODY></HTML>
_FOOTER_
}

#--------------------------------------☆ エラーチェック
sub error_check{
    if (!eval { require "$cgi"; } ) {
    $@ =~ s/</&lt;/g;
    $@ =~ s/>/&gt;/g;
    $@ =~ s/\r\n/<BR>/g;
    $@ =~ s/\r|\n/<BR>/g;
    $@ =~ s/line/<FONT color=red><B>行番号<\/B><\/FONT>/g;
    print<<"_EOF_";
<CENTER><font size=6><b>$cgiのPerlチェック結果</b></FONT></CENTER>
<BLOCKQUOTE><b>
下の一覧で「行番号」とあるのはサーバーエラーの原因と<BR>なっているＣＧＩファイルの行番号です。<BR>
$cgiをエディタで開いて、その行をご確認下さい。</b><BR><BR>
<HR>●$cgiのエラー内容と行番号●<BR>
$@
<BR><BR><BR><BR>
<HR>
●
500 Internal Server Error の主な原因●<BR>

<B>１．FTPでの転送モードに誤りがある（バイナリーモードで転送している）</B><BR>
<BR>
ＣＧＩスクリプトや、ログファイル、jcode.pl を「バイナリーモード」で<BR>
転送するとエラーになります。「テキスト（アスキー）モード」で転送して下さい。<BR>
画像などは「バイナリーモード」で転送します。<BR>
<BR>
<B>２．プログラム先頭行のPerlのパス(#!/usr/bin/perlなど)の記述が正しくない。</B><BR>
<BR>
これはプロバイダによって記述が異なります。<BR>
プロバイダのホームページに書かれているホームページに書かれているはずですので確認してみてください。<BR>
判らなければプロバイダへメールして問い合わせてみて下さい。<BR>
<BR>
Perlのパスは必ず先頭行になければなりません。
その行の前に「改行」や「スペース」行があるとエラーになります。 <BR>
また、下のように先頭の「#」や「!」は取らないで下さい。<BR>
<BR>
/usr/bin/perl<BR>
<BR>
<B>３．スクリプトの修正時に誤って文法違反を起こしてしまっている。</B><BR>
<BR>
スクリプトを修正した際に、誤って文法違反を起こしているとエラーになります。<BR>
例えば、「"」「'」などや行の最後の「;」を気付かずに削除してしまったり、タイトル部の記述などで、
ダブルクオーテーションマーク「"」の前にエスケープ記号「\\」を付け忘れていたり
などです。<BR>
<BR>
悪い例×：<BR>
print "&lt;font size="4" color="red"&gt;あっぽーＢＢＳ&lt;/font&gt;\\n";<BR>
<BR>
良い例○：<BR>
print "&lt;font size=\\"4\\" color\\"red\\"&gt;あっぽーＢＢＳ&lt;/font&gt;\\n"; <BR>
<BR>
このように「"」で囲んだ内容を読み込むので、その中に「"」を入れる場合は、
「"」の前に「\\」を入れます。<BR>
<BR>
</BLOCKQUOTE>
<BR><HR>
_EOF_
	}else{
print "エラーチェックには引っかかりませんでした。";
}
}
sub cgiinput {
	# POSTを標準入力から読込み
	read(STDIN, $pairs, $ENV{'CONTENT_LENGTH'});

	($form) = $pairs;

#「変数名=値」をイコール( = )で分解。
	($name,$value) = split(/=/, $form);

	if($value ne ''){
		# + や %8A などをデコードします
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		# 調べたファイル名を書き出し表示します
		$cgi = "./${value}.cgi";
		if($kakutyousi == 1){
		$cgi = "./${value}";
		}
	}
	print "<b>$cgi</b>を調べました。\n";
	print "<hr>\n";
}
