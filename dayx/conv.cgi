#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� DAY COUNTER-EX : conv.cgi - 2011/10/07
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
# [ Ver.3 ���� Ver.4 �փ��O��ϊ����邽�߂̃v���O�����ł� ]
# [ ���O�ϊ���́A�K���폜���Ă��������B                  ]
#
# [ �g���� ]
#  1. �udata�f�B���N�g���v�̒��Ɂudayx.dat�v�utoday.dat�v�uyes.dat�v��u���A
#      �S�ăp�[�~�b�V������666�ɂ���B
#  2. �uconv.cgi�v���udayx�f�B���N�g���v�ɒu���A�p�[�~�b�V������755�ɂ���B
#  3. �uconv.cgi�v�ɃA�N�Z�X���A�u�ϊ�����!�v�̕����񂪕\�����ꂽ�琬���B
#  4. �uconv.cgi�v���폜����B

# ���W���[���錾
use strict;
use CGI::Carp qw(fatalsToBrowser);

require "./init.cgi";
my %cf = &init;

# ���f�[�^
open(IN,"$cf{logfile}") || die;
my $data = <IN>;
close(IN);

my ($key, $yes, $today, $count, $youbi, $ip) = split(/<>/, $data);

open(DAT,"+> $cf{logfile}") || die;
print DAT "$key<>$count<>$youbi<>$ip";
close(DAT);

open(DAT,"+> $cf{todfile}") || die;
print DAT $today;
close(DAT);

open(DAT,"+> $cf{yesfile}") || die;
print DAT $yes;
close(DAT);

chmod( 0666, $cf{logfile}, $cf{todfile}, $cf{yesfile} );

print <<EOM;
Content-type: text/html

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>�ϊ��v���O����</title>
</head>
<body>
�ϊ�����!
</body>
</html>
EOM
exit;

