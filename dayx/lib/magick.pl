#┌─────────────────────────────────
#│ DreamCounter : magick.pl - 2011/06/09
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────
# [ Image::Magickによる画像連結モジュール ]

#-----------------------------------------------------------
#  Image-Magick出力
#-----------------------------------------------------------
sub magick {
	my ($count,$dir) = @_;

	# Magickモジュール
	use Image::Magick;

	# Magick起動
	my $img = Image::Magick->new;

	# 画像読込
	foreach ( split(//, $count) ) {
		$img->Read("$dir/$_.gif");
	}

	# 画像連結
	$img = $img->Append(stack => 'false');

	# 画像表示
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	$img->Write('gif:-');
	exit;
}


1;

