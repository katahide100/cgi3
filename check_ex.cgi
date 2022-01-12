#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

$arrange_name = "Error_Check EX v1.2"; ## (2001/07/07)

##�I���W�i������
$script_name = "Error_Check Version 1.1";   #(99/12/05)
# Programmed by Jynichi Sakai(�����ہ[)
# E-Mail   : caa95880@pop06.odn.ne.jp
# Homepage : �������������ہ[���v�v�v�ihttp://appoh.execweb.cx/�j
#
#  1.���̃X�N���v�g�͎����Ŏg�����߂ɍ�҂ɏ����Ȃ��Ɏ��R�ɉ������邱�Ƃ�
#    �ł��܂��B�������A���̒��쌠�\���͏����Ȃ��ŉ������B
#  2.�܂��A���̃X�N���v�g�̎g�p�ɍۂ��Đ����� �����Ȃ鑹�Q�ɑ΂��Ă��A
#    ��҂͐ӔC�𕉂��܂���B �Ĕz�z�Ɋւ��ẮA�ꌾ�A���A�����������B
# --------------------------------------------------------------------

#��#�A�����W����
#$arrange_name = "Error_Check EX v1.2"; ## (2001/07/07)
## Edited by ��������
## E-Mail: zap14631@nifty.com
## http://www.infosakyu.ne.jp/~kattin/

#--- [���ӎ���] ------------------------------------------------#
# 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����	#
#    �����Ȃ鑹�Q�ɑ΂��č��(��������j�͈�؂̐ӔC�𕉂��܂���B
# 2. ���̑��͏�L�I���W�i���X�N���v�g�̎g�p�����ɏ����܂��B
# 3. ���̃X�N���v�g�́A�I���W�i������҂����ہ[����̋��𓾂čĔz�z����Ă��܂��B
#---------------------------------------------------------------#

##���̃t�@�C���̖��O�w�肵�܂��B
###�ύX�����ꍇ�́A�t�@�C������������ƕς��邱��

$thisfile = "check_ex.cgi";

##�f�t�H���g�����t�@�C����
##�i�e�L�X�g�{�b�N�X���󔒂Ń`�F�b�J�[�N�������ꍇ�̌����t�@�C���j
##�K���ύX�ݒ肵�Ă��������B

$cgi = "index.cgi";

##�e�L�X�g�{�b�N�X���͎��̊g���q���͂�K�v�Ƃ��邩�ǂ���(�f�t�H���g�͕K�v�Ȃ��j
$kakutyousi = 1; ### �s���̃R�����g�A�E�g���͂����ƁA�g���q���͕K�v�B

#--------------------------------------�� �����ݒ�͂����܂�
$F{'mode'} = "surrender";
$F{'id'} = "BBB00000";
$F{'pass'} = "mesisp";
$F{'room'} = "t2";
&header;

# �t�H�[���Ɏw�肵���t�@�C�������A�����t�@�C�����ϐ��ɑ�����܂��B
if ($ENV{'REQUEST_METHOD'} eq "POST") {
&cgiinput;
&error_check;
}
&html_footer;
exit;

#--------------------------------------�� �g�s�l�k�̃w�b�_�[
sub header{

if($kakutyousi == 1){
$select = ".cgi";
}else{
$comment = "��** �g���q(.cgi)�́A�����I�ɕt������܂��̂œ��͕s�v�B";
}
    print <<"_HEADER_";
Content-type: text/html

<HTML><HEAD>
<!--<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=euc-jp">-->
<TITLE>Perl�`�F�b�J�[</TITLE>
</HEAD>
<BODY BGCOLOR="#ccccff" TEXT="#000000" LINK="#0000FF" ALINK="#008000">
<BASEFONT SIZE=3 FACE="�l�r �S�V�b�N">
�t�@�C�����󔒎��̌����t�@�C����: [<b> $cgi </b>]  
<form method="post" action="$thisfile">
�t�@�C����:<input type="text" name="checking" value="">
<input type="submit"" value="�`�F�b�J�|�N��"> ������t�H���_���̃t�@�C�������G���[�`�F�b�N�s�ł��B
</form>
���͗� : <b><font color="#3333cc">appoh${select}</font></b> �Ɠ��͂���ƁA<b><font color="#cc0000">./</font><font color="#3333cc">appoh.cgi</font></b> �������B<br>
$comment
<hr>
_HEADER_
}


#--------------------------------------�� �g�s�l�k�̃t�b�^�[
sub html_footer{
    print<<"_FOOTER_";
<DIV ALIGN="right">
<TT>$script_name<BR>
 [
<!-- ���̒��쌠�\\���͏��������֎~�ł� -->
 ����F<A HREF="http://appoh.execweb.cx/" TARGET="_blank">�����ہ[</A>
  �n</TT><br>
<TT>$arrange_name
 [
<!-- ���̒��쌠�\\���͏��������֎~�ł� -->
Edited by <A HREF="http://www.infosakyu.ne.jp/~kattin/" TARGET="_blank">��������</A>
  �n</TT>
</DIV></BASEFONT>
</BODY></HTML>
_FOOTER_
}

#--------------------------------------�� �G���[�`�F�b�N
sub error_check{
    if (!eval { require "$cgi"; } ) {
    $@ =~ s/</&lt;/g;
    $@ =~ s/>/&gt;/g;
    $@ =~ s/\r\n/<BR>/g;
    $@ =~ s/\r|\n/<BR>/g;
    $@ =~ s/line/<FONT color=red><B>�s�ԍ�<\/B><\/FONT>/g;
    print<<"_EOF_";
<CENTER><font size=6><b>$cgi��Perl�`�F�b�N����</b></FONT></CENTER>
<BLOCKQUOTE><b>
���̈ꗗ�Łu�s�ԍ��v�Ƃ���̂̓T�[�o�[�G���[�̌�����<BR>�Ȃ��Ă���b�f�h�t�@�C���̍s�ԍ��ł��B<BR>
$cgi���G�f�B�^�ŊJ���āA���̍s�����m�F�������B</b><BR><BR>
<HR>��$cgi�̃G���[���e�ƍs�ԍ���<BR>
$@
<BR><BR><BR><BR>
<HR>
��
500 Internal Server Error �̎�Ȍ�����<BR>

<B>�P�DFTP�ł̓]�����[�h�Ɍ�肪����i�o�C�i���[���[�h�œ]�����Ă���j</B><BR>
<BR>
�b�f�h�X�N���v�g��A���O�t�@�C���Ajcode.pl ���u�o�C�i���[���[�h�v��<BR>
�]������ƃG���[�ɂȂ�܂��B�u�e�L�X�g�i�A�X�L�[�j���[�h�v�œ]�����ĉ������B<BR>
�摜�Ȃǂ́u�o�C�i���[���[�h�v�œ]�����܂��B<BR>
<BR>
<B>�Q�D�v���O�����擪�s��Perl�̃p�X(#!/usr/bin/perl�Ȃ�)�̋L�q���������Ȃ��B</B><BR>
<BR>
����̓v���o�C�_�ɂ���ċL�q���قȂ�܂��B<BR>
�v���o�C�_�̃z�[���y�[�W�ɏ�����Ă���z�[���y�[�W�ɏ�����Ă���͂��ł��̂Ŋm�F���Ă݂Ă��������B<BR>
����Ȃ���΃v���o�C�_�փ��[�����Ė₢���킹�Ă݂ĉ������B<BR>
<BR>
Perl�̃p�X�͕K���擪�s�ɂȂ���΂Ȃ�܂���B
���̍s�̑O�Ɂu���s�v��u�X�y�[�X�v�s������ƃG���[�ɂȂ�܂��B <BR>
�܂��A���̂悤�ɐ擪�́u#�v��u!�v�͎��Ȃ��ŉ������B<BR>
<BR>
/usr/bin/perl<BR>
<BR>
<B>�R�D�X�N���v�g�̏C�����Ɍ���ĕ��@�ᔽ���N�����Ă��܂��Ă���B</B><BR>
<BR>
�X�N���v�g���C�������ۂɁA����ĕ��@�ᔽ���N�����Ă���ƃG���[�ɂȂ�܂��B<BR>
�Ⴆ�΁A�u"�v�u'�v�Ȃǂ�s�̍Ō�́u;�v���C�t�����ɍ폜���Ă��܂�����A�^�C�g�����̋L�q�ȂǂŁA
�_�u���N�I�[�e�[�V�����}�[�N�u"�v�̑O�ɃG�X�P�[�v�L���u\\�v��t���Y��Ă�����
�Ȃǂł��B<BR>
<BR>
������~�F<BR>
print "&lt;font size="4" color="red"&gt;�����ہ[�a�a�r&lt;/font&gt;\\n";<BR>
<BR>
�ǂ��ၛ�F<BR>
print "&lt;font size=\\"4\\" color\\"red\\"&gt;�����ہ[�a�a�r&lt;/font&gt;\\n"; <BR>
<BR>
���̂悤�Ɂu"�v�ň͂񂾓��e��ǂݍ��ނ̂ŁA���̒��Ɂu"�v������ꍇ�́A
�u"�v�̑O�Ɂu\\�v�����܂��B<BR>
<BR>
</BLOCKQUOTE>
<BR><HR>
_EOF_
	}else{
print "�G���[�`�F�b�N�ɂ͈���������܂���ł����B";
}
}
sub cgiinput {
	# POST��W�����͂���Ǎ���
	read(STDIN, $pairs, $ENV{'CONTENT_LENGTH'});

	($form) = $pairs;

#�u�ϐ���=�l�v���C�R�[��( = )�ŕ����B
	($name,$value) = split(/=/, $form);

	if($value ne ''){
		# + �� %8A �Ȃǂ��f�R�[�h���܂�
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		# ���ׂ��t�@�C�����������o���\�����܂�
		$cgi = "./${value}.cgi";
		if($kakutyousi == 1){
		$cgi = "./${value}";
		}
	}
	print "<b>$cgi</b>�𒲂ׂ܂����B\n";
	print "<hr>\n";
}
