#!/usr/local/bin/perl

#Ñ°ÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑü
#Ñ† DAY COUNTER-EX : dayx.cgi - 2011/07/24
#Ñ† Copyright (c) KentWeb
#Ñ† http://www.kent-web.com/
#Ñ§ÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑü

# ÉÇÉWÉÖÅ[ÉãêÈåæ
use strict;

# ê›íËÉtÉ@ÉCÉãéÊçû
require './init.cgi';
my %cf = &init;

# à¯êîÇâéﬂ
my $q = $ENV{QUERY_STRING};
$q =~ s/\W//g;

# îÒçXêVån
if ($q eq "yes" || ($cf{type} == 1 && $q eq "today")) {

	# ÉfÅ[É^ì«Ç›çûÇ›
	my $count = &read_data;

	# âÊëúï\é¶
	&load_image($count);

# çXêVån
} else {

	# ÉfÅ[É^çXêV
	my $count = &renew_data;

	# âÊëúï\é¶
	&load_image($count);
}

#-----------------------------------------------------------
#  ÉfÅ[É^ì«Ç›çûÇ›ÅiîÒçXêVÅj
#-----------------------------------------------------------
sub read_data {
	# è≠Çµë“Ç¬ÅiçXêVånÇ∆ÇÃè’ìÀâÒîÅj
	select(undef, undef, undef, 0.5);

	# ãLò^ÉtÉ@ÉCÉãì«Ç›çûÇ›
	my %data = (today => $cf{todfile}, yes => $cf{yesfile});
	open(DAT,"$data{$q}") or &error;
	my $data = <DAT>;
	close(DAT);

	return $data;
}

#-----------------------------------------------------------
#  ÉfÅ[É^çXêV
#-----------------------------------------------------------
sub renew_data {
	# ãLò^ÉtÉ@ÉCÉãì«Ç›çûÇ›
	open(DAT,"+< $cf{logfile}") or &error;
	eval "flock(DAT, 2);";
	my $data = <DAT>;

	# ãLò^ÉtÉ@ÉCÉãï™â [ ì˙, ó›åv, ójì˙, IP ]
	my ($key, $count, $youbi, $ip) = split(/<>/, $data);

	# ì˙éûéÊìæ
	$ENV{TZ} = "JST-9";
	my ($mday,$mon,$year,$wday) = (localtime(time))[3..6];
	$year += 1900;
	$mon = sprintf("%02d", $mon+1);
	my @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	my $thisday = $week[$wday];
	my $date = "$year/$mon";

	# IPÉ`ÉFÉbÉN
	my ($flg,$addr);
	if ($cf{ip_check}) {
		$addr = $ENV{REMOTE_ADDR};
		if ($addr eq $ip) { $flg = 1; }
	}

	# ÉJÉEÉìÉgÉAÉbÉv
	if (!$flg) {
		$count++;

		# --- ìñì˙èàóù
		if ($key eq $mday) {

			# ñ{ì˙ÉJÉEÉìÉgÉAÉbÉv
			open(TOD,"+< $cf{todfile}") or &error;
			eval "flock(TOD, 2);";
			my $today = <TOD> + 1;
			seek(TOD, 0, 0);
			print TOD $today;
			truncate(TOD, tell(TOD));
			close(TOD);

			# ó›åvÉçÉOÉtÉHÅ[É}ÉbÉg
			$data = "$key<>$count<>$thisday<>$addr";

		# --- óÇì˙èàóù
		} else {

			# ñ{ì˙ÉNÉäÉA
			open(TOD,"+< $cf{todfile}") or &error;
			eval "flock(TOD, 2);";
			my $today = <TOD>;
			seek(TOD, 0, 0);
			print TOD "1";
			truncate(TOD, tell(TOD));
			close(TOD);

			# çì˙çXêV
			open(YES,"+> $cf{yesfile}") or &error;
			eval "flock(YES, 2);";
			print YES $today;
			close(YES);

			# ÉçÉOÉtÉHÅ[É}ÉbÉg
			$data = "$mday<>$count<>$thisday<>$addr";

			&day_count($mday, $key, $mon, $youbi, $today);
			&mon_count($date, $today);
		}

		# ÉçÉOçXêV
		seek(DAT, 0, 0);
		print DAT $data;
		truncate(DAT, tell(DAT));
	}
	close(DAT);

	return $count;
}

#-----------------------------------------------------------
#  ì˙éüÉJÉEÉìÉg
#-----------------------------------------------------------
sub day_count {
	my ($mday, $key, $mon, $youbi, $today) = @_;

	# ÉçÉOÇÃì˙éüÉLÅ[ÇÊÇËñ{ì˙ÇÃì˙Ç™è¨Ç≥ÇØÇÍÇŒåéÇ™ïœÇÌÇ¡ÇΩÇ∆îªífÇ∑ÇÈ
	if ($mday < $key) {
		open(DB,"+> $cf{dayfile}") or &error;
		close(DB);

	# åéì‡Ç≈ÇÃèàóù
	} else {
		if ($key < 10) { $key = "0$key"; }

		open(DB,">> $cf{dayfile}") or &error;
		eval "flock(DB, 2);";
		print DB "$mon/$key ($youbi)<>$today<>\n";
		close(DB);
	}
}

#-----------------------------------------------------------
#  åééüÉJÉEÉìÉg
#-----------------------------------------------------------
sub mon_count {
	my ($date, $today) = @_;
	my @mons;

	open(MON,"+< $cf{monfile}") or &error;
	eval "flock(MON, 2);";

	# èâÇﬂÇƒÇÃÉAÉNÉZÉXÇÃèÍçá
	if (-z $cf{monfile}) {
		$mons[0] = "$date<>$today<>\n";

	# ÇQâÒñ⁄à»ç~
	} else {
		@mons = <MON>;

		# ÉçÉOîzóÒÇÃç≈èIçsÇï™â
		$mons[$#mons] =~ s/\n//;
		my ($y_m, $cnt) = split(/<>/, $mons[$#mons]);

		# ìñåéèàóù
		if ($y_m eq $date) {
			$cnt += $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";

		# óÇåéèàóù
		#ÅiÉçÉOîzóÒÇÃç≈èIçsÇ™ $dateÇ∆àŸÇ»ÇÍÇŒÅAåéÇ™ïœÇ¡ÇΩÇ∆îªífÇ∑ÇÈÅj
		} else {
			$cnt += $today;
			$mons[$#mons] = "$y_m<>$cnt<>\n";
			push(@mons,"$date<>0<>\n");
		}
	}

	# ÉçÉOÉtÉ@ÉCÉãçXêV
	seek(MON, 0, 0);
	print MON @mons;
	truncate(MON, tell(MON));
	close(MON);
}

#-----------------------------------------------------------
#  ÉJÉEÉìÉ^âÊëúï\é¶
#-----------------------------------------------------------
sub load_image {
	my ($data) = @_;

	my ($digit,$dir);
	if ($q eq 'gif') {
		$digit = $cf{digit1};
		$dir = $cf{gifdir1};
	} else {
		$digit = $cf{digit2};
		$dir = $cf{gifdir2};
	}

	# åÖêîí≤êÆ
	while (length($data) < $digit) {
		$data = '0' . $data;
	}

	# Image::MagickÇÃÇ∆Ç´
	if ($cf{image_pm} == 1) {
		require $cf{magick_pl};
		&magick($data, $dir);
	}

	# âÊëúì«Ç›çûÇ›
	my @img;
	foreach ( split(//, $data) ) {
		push(@img,"$dir/$_.gif");
	}

	# âÊëúòAåã
	require $cf{gifcat_pl};
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat::gifcat(@img);
}

#-----------------------------------------------------------
#  ÉGÉâÅ[èàóù
#-----------------------------------------------------------
sub error {
	# ÉGÉâÅ[âÊëú
	my @err = qw{
		47 49 46 38 39 61 2d 00 0f 00 80 00 00 00 00 00 ff ff ff 2c
		00 00 00 00 2d 00 0f 00 00 02 49 8c 8f a9 cb ed 0f a3 9c 34
		81 7b 03 ce 7a 23 7c 6c 00 c4 19 5c 76 8e dd ca 96 8c 9b b6
		63 89 aa ee 22 ca 3a 3d db 6a 03 f3 74 40 ac 55 ee 11 dc f9
		42 bd 22 f0 a7 34 2d 63 4e 9c 87 c7 93 fe b2 95 ae f7 0b 0e
		8b c7 de 02	00 3b
	};

	print "Content-type: image/gif\n\n";
	foreach (@err) {
		print pack('C*', hex($_));
	}
	exit;
}

