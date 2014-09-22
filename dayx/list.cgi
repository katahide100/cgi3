#!/usr/local/bin/perl

#Ñ°ÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑü
#Ñ† DAY COUNTER-EX : list.cgi - 2011/08/08
#Ñ† Copyright (c) KentWeb
#Ñ† http://www.kent-web.com/
#Ñ§ÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑüÑü

# ÉÇÉWÉÖÅ[ÉãêÈåæ
use strict;
use CGI::Carp qw(fatalsToBrowser);

# ê›íËÉtÉ@ÉCÉãéÊçû
require './init.cgi';
my %cf = &init;

# ÉäÉXÉgàÍóó
&list_data;

#-----------------------------------------------------------
#  ÉäÉXÉgàÍóó
#-----------------------------------------------------------
sub list_data {
	# ó›åvÉtÉ@ÉCÉãì«Ç›çûÇ›
	open(IN,"$cf{logfile}") or die "open err: $!";
	my $data = <IN>;
	close(IN);
	my ($day) = (split(/<>/, $data))[0];

	# ñ{ì˙ÉtÉ@ÉCÉãì«Ç›çûÇ›
	open(IN,"$cf{todfile}") or die "open err: $!";
	my $tod = <IN>;
	close(IN);

	# éûä‘éÊìæ
	$ENV{TZ} = "JST-9";
	my ($mday,$mon,$year,$wday) = (localtime(time))[3..6];
	my @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	my $date = sprintf("%02d/%02d (%s) ", $mon+1,$mday,$week[$wday]);
	my $D_Y  = sprintf("%04d/%02d", $year+1900,$mon+1);

	# ì˙éüÉtÉ@ÉCÉãì«Ç›çûÇ›
	open(IN,"$cf{dayfile}") or die "open err: $!";
	my @dayfile = <IN>;
	close(IN);
	push(@dayfile,"$date<>$tod<>\n");

	# åééüÉtÉ@ÉCÉãÇì«Ç›çûÇ›
	open(IN,"$cf{monfile}") or die "open err: $!";
	my @monfile = <IN>;
	close(IN);

	my $under = pop(@monfile);
	my ($Y,$C,$C2);
	if ($under =~ /^(\d+)\/(\d+)<>(\d+)/) {
		$Y = "$1/$2";
		$C = $3;
	}
	if ($Y eq $D_Y) {
		$C2 = $C + $tod;
		push(@monfile,"$Y<>$C2<>\n");
	} else {
		push(@monfile,"$D_Y<>$tod<>\n");
	}

	# ÉeÉìÉvÉåÅ[Égì«Ç›çûÇ›
	open(IN,"$cf{tmpldir}/list.html") or die "open err: $!";
	my $tmpl = join('', <IN>);
	close(IN);

	# ÉeÉìÉvÉåÅ[Égï™äÑ
	my ($head,$dcel,$mid,$mcel,$foot);
	if ($tmpl =~ /(.+)<!-- dayloop_begin -->(.+)<!-- dayloop_end -->(.+)<!-- monloop_begin -->(.+)<!-- monloop_end -->(.+)/s) {
		($head,$dcel,$mid,$mcel,$foot) = ($1,$2,$3,$4,$5);
	} else {
		die "template is no good";
	}

	# ï∂éöíuÇ´ä∑Ç¶
	foreach ($head,,$mid,,$foot) {
		s/!home!/$cf{home}/g;
	}

	# ï\é¶äJén
	print "Content-type: text/html\n\n";
	print $head;

	# ì˙éü
	my $tochu = 0;
	my $i = 0;
	foreach (@dayfile) {
		$i++;
		chomp;
		my ($m_d, $dcnt) = split(/<>/);
		if ($i == 1 && $m_d =~ /^(\d+)\/(\d+)/) {
			if ($2 != 1) { $tochu = 1; }
		}

		# ÉOÉâÉtïùÇéwíË
		my $width;
		if ($dcnt > 0) {
			$width = int($dcnt / $cf{dKEY});
		} else {
			$width = 1;
		}
		if ($width < 1) { $width = 1; }

		# åÖèàóù
		$dcnt = &comma($dcnt);

		# êFïœçX
		$m_d =~ s/Sat/<span style="colo:blue">Sat<\/span>/;
		$m_d =~ s/Sun/<span style="color:red">Sun<\/span>/;

		# ÉãÅ[Év
		my $tmp = $dcel;
		$tmp =~ s/!date!/$m_d/g;
		$tmp =~ s/!count!/$dcnt/g;
		$tmp =~ s/!graph!/<img src="$cf{graph1}" width="$width" height="5">/g;
		print $tmp;
	}

	# íÜåpÇ¨
	print $mid;

	# åééü
	foreach (@monfile) {
		my ($y_m,$mcnt) = split(/<>/);
		my ($year,$mon) = split(/\//, $y_m);

		my ($avr,$waru);
		if ($_ eq $monfile[$#monfile]) {
			if ($day == 1) { $avr = ' - '; }
			else {
				if ($tochu) {
					$waru = @dayfile - 1;
				} else {
					$waru = $day - 1;
				}
				if ($C > 0) {
					$avr = int (($C / $waru) + 0.5);
					$avr = &comma($avr);
				} else {
					$avr = ' - ';
				}
			}
		} else {
			my $last = &lastday($year, $mon);
			$avr = int (($mcnt / $last) + 0.5);
			$avr = &comma($avr);
		}

		# ÉOÉâÉtïùÇéwíË
		my $width;
		if ($mcnt > 0) {
			$width = int($mcnt / $cf{mKEY});
		} else {
			$width = 1;
		}
		if ($width < 1) { $width = 1; }

		# åÖèàóù
		$mcnt = &comma($mcnt);

		# ÉãÅ[Év
		my $tmp = $mcel;
		$tmp =~ s/!date!/$y_m/g;
		$tmp =~ s/!month!/$mcnt/g;
		$tmp =~ s/!average!/$avr/g;
		$tmp =~ s/!graph!/<img src="$cf{graph2}" width="$width" height="10">/g;
		print $tmp;
	}

	# ÉtÉbÉ^
	&footer($foot);
}

#-----------------------------------------------------------
#  åéÇÃññì˙
#-----------------------------------------------------------
sub lastday {
	my ($year, $mon) = @_;

	my $last = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31) [$mon - 1]
	+ ($mon == 2 && (($year % 4 == 0 && $year % 100 != 0) || $year % 400 == 0));

	return $last;
}

#-----------------------------------------------------------
#  åÖãÊÇ´ÇË
#-----------------------------------------------------------
sub comma {
	local($_) = @_;

	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	$_;
}

#-----------------------------------------------------------
#  ÉtÉbÉ^Å[
#-----------------------------------------------------------
sub footer {
	my $foot = shift;

	# íòçÏå†ï\ãLÅiçÌèúã÷é~Åj
	my $copy = <<EOM;
<p style="margin-top:2em;text-align:center;font-family:Verdana,Helvetica,Arial;font-size:10px;">
- <a href="http://www.kent-web.com/" target="_top">DayCounterEX</a> -
</p>
EOM

	if ($foot =~ /(.+)(<\/body[^>]*>.*)/si) {
		print "$1$copy$2\n";
	} else {
		print "$foot$copy\n";
		print "<body></html>\n";
	}
	exit;
}

