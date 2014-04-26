#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� DAY COUNTER-EX : check.cgi - 2011/10/07
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[���錾
use strict;
use CGI::Carp qw(fatalsToBrowser);

require "./init.cgi";
my %cf = &init;

print <<EOM;
Content-type: text/html

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
EOM

# ���O�t�@�C���m�F
my %log = (
	logfile => '�݌v',
	todfile => '�{��',
	yesfile => '���',
	dayfile => '����',
	monfile => '����',
	);
foreach ( keys(%log) ) {
	if (-f $cf{$_}) {
		print "<li>$log{$_}�t�@�C���p�X : OK\n";

		# ���O�t�@�C���̃p�[�~�b�V����
		if (-r $cf{$_} && -w $cf{$_}) {
			print "<li>$log{$_}�t�@�C���p�[�~�b�V���� : OK\n";
		} else {
			print "<li>$log{$_}�t�@�C���p�[�~�b�V���� : NG\n";
		}
	} else {
		print "<li>$log{$_}�t�@�C���p�X : NG\n";
	}
}

# �e���v���[�g
if (-f "$cf{tmpldir}/list.html") {
	print "<li>�e���v���[�g : OK\n";
} else {
	print "<li>�e���v���[�g : NG\n";
}

# �摜�`�F�b�N
foreach ( $cf{gifdir1}, $cf{gifdir2} ) {
	foreach my $i (0 .. 9) {
		if (-e "$_/$i.gif") {
			print "<li>�摜 : $_/$i.gif �� OK\n";
		} else {
			print "<li>�摜 : $_/$i.gif �� NG\n";
		}
	}
}

eval { require $cf{gifcat_pl}; };
if ($@) {
	print "<li>gifcat.pl�e�X�g : NG\n";
} else {
	print "<li>gifcat.pl�e�X�g : OK\n";
}

eval { require Image::Magick; };
if ($@) {
	print "<li>Image::Magick�e�X�g : NG\n";
} else {
	print "<li>Image::Magick�e�X�g : OK\n";
}

# ���쌠�\���F�폜���ϋ֎~
print <<EOM;
</ul>
<p style="font-size:10px;font-family:Verdana,Helvetica,Arial;margin-top:5em;text-align:center;">
- <a href="http://www.kent-web.com/">DayCounter-EX</a> -
</p>
</body>
</html>
EOM
exit;

