#��������������������������������������������������������������������
#�� DreamCounter : magick.pl - 2011/06/09
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
# [ Image::Magick�ɂ��摜�A�����W���[�� ]

#-----------------------------------------------------------
#  Image-Magick�o��
#-----------------------------------------------------------
sub magick {
	my ($count,$dir) = @_;

	# Magick���W���[��
	use Image::Magick;

	# Magick�N��
	my $img = Image::Magick->new;

	# �摜�Ǎ�
	foreach ( split(//, $count) ) {
		$img->Read("$dir/$_.gif");
	}

	# �摜�A��
	$img = $img->Append(stack => 'false');

	# �摜�\��
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	$img->Write('gif:-');
	exit;
}


1;

