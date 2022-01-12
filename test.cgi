#!/usr/local/bin/perl
use FindBin;
use lib $FindBin::Bin;

&bosyuu_gazo();

sub bosyuu_gazo{

	open (IN,"setting.txt");

	@aaa = <IN>;

	close (IN);
	
	foreach $bbb (@aaa) {

		my @ccc = split(/@@/,$bbb);

		if(($ccc[0] == "bosyuu") && ($ccc[1] == '1')){
print <<"HTML";

<script language="JavaScript">
<!--
vType   = ["visible","hidden"];
flag    = 0;		//�@�_�Ńt���O
imgName = "myIMG";	//�@�_�ł�����摜��
function iFlash()
{
	document.images[imgName].style.visibility = vType[flag ^= 1];
	setTimeout('iFlash()',800);
}
// --></script>

<div onLoad="setTimeout('iFlash()',1000)">
<img src="./tnm.png" width="80" height="20" name="myIMG"><br>
</div>

HTML
		}
	}
	exit;
}