#!/usr/bin/perl
$Charset='';
$PageLength=20;
$MaxLine=200;
$MaxComment=3000;
$MaxName=50;
$BbsId=0;

$UseTrip=1;
$UseId=1;
###
use Encode;
use Encode::Guess qw/euc-jp shiftjis/;
use Digest::SHA;
###
read(STDIN,$FormData,$ENV{'CONTENT_LENGTH'});
&WriteData;
&PrintLocation($ENV{HTTP_REFERER});
###
sub WriteData{
	my($comment,$name,$code,@bbs,$i,$j,@page,@line,$id,$trip,$tkey);
	$comment=&GetValue($FormData,"BbsComment");
	$comment=&UrlUnescape($comment);
	$name=&GetValue($FormData,"BbsName");
	$name=&UrlUnescape($name);
	&CheckCharset($comment.$name);
	$comment=&CommentEncode($comment);
	if($UseTrip && $name=~/#./){
		($name,$tkey)=split(/#/,$name,2);
		Encode::from_to($tkey,$Charset,'utf8') if($Charset && $Charset ne 'utf8');
		$trip=Digest::SHA::hmac_sha256_base64($tkey,$UseTrip);
		$trip=substr($trip,-8);
	}
	if($UseId){
		$id=Digest::SHA::hmac_sha256_base64($ENV{REMOTE_ADDR},$UseId);
		$id=substr($id,-8);
	}
	$name=&NameEncode($name);
	&PrintLocation('error/101.html') if(length($name)>$MaxName);
	&PrintLocation('error/102.html') if(!$name);
	&PrintLocation('error/103.html') if(!$comment);
	&PrintLocation('error/104.html') if(length($comment)>$MaxComment);
	&CheckConfig($name,$comment,$tkey);
	open(FILE,"bbs.dat");
	flock(FILE,1);
	@bbs=<FILE>;
	close(FILE);
	unshift(@bbs,"$comment<>$name<>".time."<>$id<>$trip<>$tkey<>$ENV{REMOTE_ADDR}<>\n");
	while($#bbs>=$MaxLine){
		pop(@bbs);
	}
	open(FILE,"+<bbs.dat");
	flock(FILE,2);
	seek(FILE,0,0);
	print FILE @bbs;
	truncate(FILE,tell(FILE));
	close(FILE);
	for($i=0;-e("page/$i.dat");$i++){
		undef(@page);
		for($j=$i*$PageLength;$j<($i+1)*$PageLength&&$bbs[$j];$j++){
			$bbs[$j]=~s/[\r\n]//g;
			@line=split(/<>/,$bbs[$j]);
			push(@page,'{"comment":"'.$line[0].'","name":"'.$line[1].'","time":"'.$line[2].'","id":"'.$line[3].'","trip":"'.$line[4].'"}');
		}
		if(@page){
			$content="BbsPage([".join(',',@page)."],$BbsId);";
			open(FILE,"+>page/$i.dat");
			print FILE $content;
			close(FILE);
		}
	}
}
###
sub CheckConfig{
	my(@file,$left,$right,$name,$comment,$tkey,$allow);
	($name,$comment,$tkey)=@_;
	open(FILE,"bbs.conf");
	@file=<FILE>;
	close(FILE);
	foreach(@file){
		s/[\r\n]//g;
		($left,$right)=split(/:/,$_,2);
		if($left eq 'block'){
			($left,$right)=split(/:/,$right,2);
			if($left eq 'word'){
				&PrintLocation('error/201.html') if($comment=~/$right/);
			}elsif($left eq 'ip'){
				&PrintLocation('error/202.html') if($ENV{REMOTE_ADDR} eq $right || $ENV{REMOTE_ADDR}=~/^$right\./);
			}
		}elsif($left eq 'allow'){
			$allow=1 if(!$allow);
			($left,$right)=split(/:/,$right,2);
			if($left eq 'trip'){
				$allow=2 if($tkey eq $right);
			}
		}
	}
	&PrintLocation('error/301.html') if($allow==1);
}
###
sub CheckCharset{
	return if($Charset);
	my($str,$code);
	$str=shift;
	$code=guess_encoding($str);
	$Charset=$code->name if(ref($code));
}
###
sub NameEncode{
	my($str,$code);
	$str=shift;
	Encode::from_to($str,$Charset,'utf8') if($Charset && $Charset ne 'utf8');
	$str=&MetaEscape($str);
	$str=~s/\r//g;
	$str=~s/\n//g;
	$str="No name" if(!$str);
	return($str);
}
###
sub CommentEncode{
	my($str);
	$str=shift;
	Encode::from_to($str,$Charset,'utf8') if($Charset && $Charset ne 'utf8');
	$str=&MetaEscape($str);
	$str=~s/\r//g;
	$str=~s/\n/<br \/>/g;
	$str=~s/(http:\/\/[\w\!\#\$\%\&\=\-\~\+\:,\.\/\?]+)/&AutoLink($1)/eg;
	return($str);
}
###
sub AutoLink{
	my($href,$text);
	$href=shift;
	$text=$href;
	$href=~s/&amp;/&/g;
	return("<a href='$href' target='_blank'>$text<\/a>");
}
###
sub MetaEscape{
	my($str);
	$str=shift;
	$str=~s/&/&amp;/g;
	$str=~s/</&lt;/g;
	$str=~s/>/&gt;/g;
	$str=~s/ /&nbsp;/g;
	$str=~s/"/&quot;/g;
	$str=~s/\\/\\\\/g;
	return($str);
}
###
sub UrlUnescape{
	my($str);
	$str=$_[0];
	$str=~tr/+/ /;
	$str=~s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2",$1)/eg;
	return($str);
}
###
sub GetValue{
	my(@objects);
	@objects=split(/[&]/,$_[0]);
	foreach(@objects){
		return($1) if(/^$_[1]=(.+)$/);
	}
	return;
}
###
sub PrintLocation{
	print "Location:$_[0]\n\n";
	exit;
}
###


