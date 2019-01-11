$roomst			= "duelist";						# 対戦用データファイルの名前
$help			= "./etc/help.html";					# help.htmlのパス（絶対パスでも相対パスでも可）
$keyword		= "./etc/keyword.html";					# keyword.htmlのパス（絶対パスでも相対パスでも可）
$css			= "./css";						# duel.cssのパス（絶対パスでも相対パスでも可）
$js			= "./js";							# jsディレクトリへのパス（絶対パスでも相対パスでも可。最後に『/』はつけない）
$lockfile 		= "duel.lock";						# ロックファイル名（変更不要）

$player_dir		=  "./playerdata";   #"http://mesis.twimpt.com/dmx/tmp/playerdata"; 
$room_dir		= "./room";  #"http://mesis.twimpt.com/dm/room"; "./room";
$symbol_dir		= "./symbols";

$title			= "デュエル・マスターズ対戦CGI ex";	# タイトル
$heyakazu		= 30;								# 対戦部屋の数

$mente			= 0;					# メンテナンス中？(YES=1 NO=0)

$image			= "./images";						# 観戦中画像のパス（絶対パスでも相対パスでも可）
@kansen			= ("kansen_1.png","kansen_rupia.png","kansen_baromu.png","kansen_minibaromu.png","kansen_doremi.png", "kansen_haduki.png", "kansen_onpu.png", "kansen_momoko.png", "kansen_hana.png");

$natime			= 5;								# アクセスなしで負けになる時間（分）

@deny_id		= ("OBA35431","ID");						# 対戦へのアクセスを拒否するユーザーID
$deny_proxy		= 0;								# プロクシ経由で来る訪問者を排除する？(YES=1 NO=0)

$max_file		= "";								# 保存するプレイヤーファイルの最大数
													# ※プレイヤーファイル自動削除機能を使用しない場合は#max_file = "";としてください。
$del_day		= 90;								# 最大数を超えた場合に削除されるファイルの、更新されなかった日数

$maxdeck		= 20;
$maxgroup		= 5;								# セーブできるデッキの数
$copy			= 1;								# デッキコピー機能を使う？(YES=1 NO=0)

$bbs			= 1;								# 伝言板機能を使う？(YES=1 NO=0)
$admin			= "mikann";							# 管理パスワード(半角英数8文字以内。必ず変更してください)
$view			= 20;								# 表示記事数(あまり大きくするとテーブルが縦に長くなるので注意)
$maxview		= 300;								# 保有記事数
$leng			= 600;								# 記事の最大文字数（半角）
$ptime			= 10;								# 連続書き込み禁止時間（秒）
$lockfile2 		= "word.lock";						# 伝言板機能用ロックファイル名（変更不要）

$dendoufile     = "./data/dendou.txt";              # 殿堂入りカードのデータファイル
$premiumfile    = "./data/premium.txt";             # P殿堂入りカードのデータファイル

$hostName       = "https://manadream.net";          # ホスト名（node.jsなどで使>
用）
$nodePort       = "3002";                           # node.jsのポート番号

$chatNodePort   = "1337";                           # chatのnode.jsポート番号

$chatNodeHost   = $hostName . ':' . $chatNodePort;  # chatのホスト

# P殿堂入りカード読み込み
open($fh, "<",$premiumfile);
while(my $line = readline $fh){
	push(@premium,$line);
}
close($fh);

# 殿堂入りカード読み込み
open($fh, "<",$dendoufile);
while(my $line = readline $fh){
	push(@dendou,$line);
}
close($fh);

@combi			= ();

@zerodeck		= ([104,104,104,104,1042,1042,1042,1042,427,427,427,427,574,574,922,922,922,922,1666,1666,1666,1666,734,734,1598,1598,608,608,608,608,1090,1090,1090,1090,1601,1601,304,304,304,441],
			   [913,1824,1824,1824,1824,1222,1222,1222,1222,99,99,99,251,251,313,313,313,314,314,314,314,315,315,315,315,191,468,468,468,468,118,260,1082,1082,320,320,754,754,754,754],
			   [468,468,118,260,320,320,320,320,1521,103,103,103,103,1036,1036,1036,1036,333,333,333,104,104,104,104,670,670,1886,1886,1886,1886,1137,1137,1532,275,1040,1887,1887,1887,1887,841],
			   [583,583,1090,1090,1090,1090,1304,1059,1213,586,586,586,586,785,785,785,785,79,79,79,79,645,645,645,167,167,170,170,767,767,767,767,769,769,769,977,1888,1171,1171,1171]);

#@d_boru			= (770,1171,785,986,1237);
#@d_speed		= (57,767,1045,424,160,476,236,515);
#@d_shield		= (1126,838);
#@d_lib			= (661,474,910);
#@d_hand			= (102,602,909,176,506,864,141,1198,1236,1297);
#@d_land			= (638,158,584,1171,479,179,844);
#@d_ws			= (787,789,793,856,796,798,803,806,808,810,868,936,814,816,820,877,823,824,826,879,831);
@minus10		= (770,1237,1601);
@minus5			= (232,661,474,584,612,602,986,57,1046,1068,548,1171,841,1026,2044,1827,170,1909,2206,2069,1576,1895);
@minus3			= (442,924,168,931,160,910,982,670,139,785,977,816,810,856,638,531,1076,844,176,838,778,1420,1339,884,1350,721,909,441,1563,1407,247,1402,1592,1521,1593,427,1327,1830,1474,1239,1962,1964,1952,2049,2062,1975,1738,1198,1126,2153,1954,1297,2120);
@minus1			= (124,759,767,773,542,430,340,270,249,610,787,789,793,796,798,936,806,808,814,877,820,879,823,824,826,1091,1354,1411,1414,1419,1347,918,25,1530,1531,132,1461,1229,1579,822,1470,1543,76,1062,161,674,898,1320,2028,1988,1980,2055,2134,2117,2047,1598,1899,1894,1936,2128);
@plus1			= (44,48,51,362,46,712,1018,1272,131,411,234,803,831,1315,202,1355);

@beginner		= (16,17,18,19,20,21,22,23,24,25,26,27,28,29,30);						# 初心者用対戦ルーム

%order_symbol		= ();
%order_color		= ();
%order_text		= ();

@order_per		= ('tf', 'ts', 'tt', 'dm', 'sp', 'ex', 'light', 'highlight', 'water', 'highwater', 'dark', 'highdark', 'fire', 'highfire', 'nature', 'highnature',
			   'lw', 'highlw', 'wd', 'highwd', 'df', 'highdf', 'fn', 'highfn', 'nl', 'highnl',
			   'ld', 'highld', 'wf', 'highwf', 'dn', 'highdn', 'fl', 'highfl', 'nw', 'highnw', 
			   'lwd', 'highlwd', 'wfl', 'highwfl', 'nlw', 'highnlw', 'fld', 'highfld',
			   'ldn', 'highldn', 'fnl', 'highfnl', 'wdf', 'highwdf', 'wdn', 'highwdn', 'nwf', 'highnwf', 'dfn', 'highdfn',
			   'nolight', 'highnolight', 'nowater', 'highnowater', 'nodark', 'highnodark', 'nofire', 'highnofire', 'nonature', 'highnonature',
			   'full', 'highfull', 'rainbow', 'weak', 'hirand',  'long', 'christmas', 'valentine', 'aprilfool', 'enquete', 'kyoryoku', 'bag', 'admin', 'subadmin', 'kaicho', 'huku','kaiin2',
			   'kun', 'spfull', 'allzero', 'handess', 'nz', 'randess');
$order_symbol{'tf'}		= '★';
$order_color{'tf'}		= '#888800';
$order_text{'tf'}		= '対戦CGI ex 公式戦で、優勝を収めた事のある証';
$order_symbol{'ts'}		= '★';
$order_color{'ts'}		= '#888888';
$order_text{'ts'}		= '対戦CGI ex 公式戦で、準優勝を収めた事のある証';
$order_symbol{'tt'}		= '★';
$order_color{'tt'}		= '#008800';
$order_text{'tt'}		= '対戦CGI ex 公式戦で、３位を収めた事のある証';

$order_symbol{'fire'}		= '■';
$order_color{'fire'}		= '#ff0000';
$order_text{'fire'}		= '火単色デッキで幾度も勝利を収めた証';
$order_symbol{'highfire'}	= '□';
$order_color{'highfire'}	= '#ff0000';
$order_text{'highfire'}		= '火単色デッキで数多くの勝利を収めた火を極めし者の証';
$order_symbol{'nature'}		= '■';
$order_color{'nature'}		= '#00ff00';
$order_text{'nature'}		= '自然単色デッキで幾度も勝利を収めた証';
$order_symbol{'highnature'}	= '□';
$order_color{'highnature'}	= '#00ff00';
$order_text{'highnature'}	= '自然単色デッキで数多くの勝利を収めた自然を極めし者の証';
$order_symbol{'light'}		= '■';
$order_color{'light'}		= '#ffff00';
$order_text{'light'}		= '光単色デッキで幾度も勝利を収めた証';
$order_symbol{'highlight'}	= '□';
$order_color{'highlight'}	= '#ffff00';
$order_text{'highlight'}	= '光単色デッキで数多くの勝利を収めた光を極めし者の証';
$order_symbol{'water'}		= '■';
$order_color{'water'}		= '#0000ff';
$order_text{'water'}		= '水単色デッキで幾度も勝利を収めた証';
$order_symbol{'highwater'}	= '□';
$order_color{'highwater'}	= '#0000ff';
$order_text{'highwater'}	= '水単色デッキで数多くの勝利を収めた水を極めし者の証';
$order_symbol{'dark'}		= '■';
$order_color{'dark'}		= '#888888';
$order_text{'dark'}		= '闇単色デッキで幾度も勝利を収めた証';
$order_symbol{'highdark'}	= '□';
$order_color{'highdark'}	= '#888888';
$order_text{'highdark'}		= '闇単色デッキで数多くの勝利を収めた闇を極めし者の証';

$order_symbol{'lw'}		= '■';
$order_color{'lw'}		= '#8888ff';
$order_text{'lw'}		= '光/水デッキで幾度も勝利を収めた証';
$order_symbol{'highlw'}		= '□';
$order_color{'highlw'}		= '#8888ff';
$order_text{'highlw'}		= '光/水デッキで数多くの勝利を収めたアゾリウスカラーを極めし者の証';
$order_symbol{'wd'}		= '■';
$order_color{'wd'}		= '#000088';
$order_text{'wd'}		= '水/闇デッキで幾度も勝利を収めた証';
$order_symbol{'highwd'}		= '□';
$order_color{'highwd'}		= '#000088';
$order_text{'highwd'}		= '水/闇デッキで数多くの勝利を収めたディミーアカラーを極めし者の証';
$order_symbol{'df'}		= '■';
$order_color{'df'}		= '#880000';
$order_text{'df'}		= '闇/火デッキで幾度も勝利を収めた証';
$order_symbol{'highdf'}		= '□';
$order_color{'highdf'}		= '#880000';
$order_text{'highdf'}		= '闇/火デッキで数多くの勝利を収めたラクドスカラーを極めし者の証';
$order_symbol{'fn'}		= '■';
$order_color{'fn'}		= '#888800';
$order_text{'fn'}		= '火/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highfn'}		= '□';
$order_color{'highfn'}		= '#888800';
$order_text{'highfn'}		= '火/自然デッキで数多くの勝利を収めたグルールカラーを極めし者の証';
$order_symbol{'nl'}		= '■';
$order_color{'nl'}		= '#88ff88';
$order_text{'nl'}		= '自然/光デッキで幾度も勝利を収めた証';
$order_symbol{'highnl'}		= '□';
$order_color{'highnl'}		= '#88ff88';
$order_text{'highnl'}		= '自然/光デッキで数多くの勝利を収めたセレズニアカラーを極めし者の証';
$order_symbol{'ld'}		= '■';
$order_color{'ld'}		= '#bbbbbb';
$order_text{'ld'}		= '光/闇デッキで幾度も勝利を収めた証';
$order_symbol{'highld'}		= '□';
$order_color{'highld'}		= '#bbbbbb';
$order_text{'highld'}		= '光/闇デッキで数多くの勝利を収めたオルゾフカラーを極めし者の証';
$order_symbol{'wf'}		= '■';
$order_color{'wf'}		= '#880088';
$order_text{'wf'}		= '水/火デッキで幾度も勝利を収めた証';
$order_symbol{'highwf'}		= '□';
$order_color{'highwf'}		= '#880088';
$order_text{'highwf'}		= '水/火デッキで数多くの勝利を収めたイゼットカラーを極めし者の証';
$order_symbol{'dn'}		= '■';
$order_color{'dn'}		= '#008800';
$order_text{'dn'}		= '闇/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highdn'}		= '□';
$order_color{'highdn'}		= '#008800';
$order_text{'highdn'}		= '闇/自然デッキで数多くの勝利を収めたゴルガリカラーを極めし者の証';
$order_symbol{'fl'}		= '■';
$order_color{'fl'}		= '#ff8888';
$order_text{'fl'}		= '火/光デッキで幾度も勝利を収めた証';
$order_symbol{'highfl'}		= '□';
$order_color{'highfl'}		= '#ff8888';
$order_text{'highfl'}		= '火/光デッキで数多くの勝利を収めたボロスカラーを極めし者の証';
$order_symbol{'nw'}		= '■';
$order_color{'nw'}		= '#008888';
$order_text{'nw'}		= '自然/水デッキで幾度も勝利を収めた証';
$order_symbol{'highnw'}		= '□';
$order_color{'highnw'}		= '#008888';
$order_text{'highnw'}		= '自然/水デッキで数多くの勝利を収めたシミックカラーを極めし者の証';

$order_symbol{'lwd'}		= '■';
$order_color{'lwd'}		= '#4444bb';
$order_text{'lwd'}		= '光/水/闇デッキで幾度も勝利を収めた証';
$order_symbol{'highlwd'}	= '□';
$order_color{'highlwd'}		= '#4444bb';
$order_text{'highlwd'}		= '光/水/闇デッキで数多くの勝利を収めたドロマーカラーを極めし者の証';
$order_symbol{'wfl'}		= '■';
$order_color{'wfl'}		= '#884488';
$order_text{'wfl'}		= '水/火/光デッキで幾度も勝利を収めた証';
$order_symbol{'highwfl'}	= '□';
$order_color{'highwfl'}		= '#884488';
$order_text{'highwfl'}		= '水/火/光デッキで数多くの勝利を収めたトリコロールカラーを極めし者の証';
$order_symbol{'nlw'}		= '■';
$order_color{'nlw'}		= '#448888';
$order_text{'nlw'}		= '自然/光/水デッキで幾度も勝利を収めた証';
$order_symbol{'highnlw'}	= '□';
$order_color{'highnlw'}		= '#448888';
$order_text{'highnlw'}		= '自然/光/水デッキで数多くの勝利を収めたトリーヴァカラーを極めし者の証';
$order_symbol{'fld'}		= '■';
$order_color{'fld'}		= '#bb4444';
$order_text{'fld'}		= '火/光/闇デッキで幾度も勝利を収めた証';
$order_symbol{'highfld'}	= '□';
$order_color{'highfld'}		= '#bb4444';
$order_text{'highfld'}		= '火/光/闇デッキで数多くの勝利を収めたデイガカラーを極めし者の証';
$order_symbol{'ldn'}		= '■';
$order_color{'ldn'}		= '#44bb44';
$order_text{'ldn'}		= '光/闇/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highldn'}	= '□';
$order_color{'highldn'}		= '#44bb44';
$order_text{'highldn'}		= '光/闇/自然デッキで数多くの勝利を収めたネクラカラーを極めし者の証';
$order_symbol{'fnl'}		= '■';
$order_color{'fnl'}		= '#888844';
$order_text{'fnl'}		= '火/自然/光デッキで幾度も勝利を収めた証';
$order_symbol{'highfnl'}	= '□';
$order_color{'highfnl'}		= '#888844';
$order_text{'highfnl'}		= '火/自然/光デッキで数多くの勝利を収めたリースカラーを極めし者の証';
$order_symbol{'wdf'}		= '■';
$order_color{'wdf'}		= '#440044';
$order_text{'wdf'}		= '水/闇/火デッキで幾度も勝利を収めた証';
$order_symbol{'highwdf'}	= '□';
$order_color{'highwdf'}		= '#440044';
$order_text{'highwdf'}		= '水/闇/火デッキで数多くの勝利を収めたクローシスカラーを極めし者の証';
$order_symbol{'wdn'}		= '■';
$order_color{'wdn'}		= '#004444';
$order_text{'wdn'}		= '水/闇/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highwdn'}	= '□';
$order_color{'highwdn'}		= '#004444';
$order_text{'highwdn'}		= '水/闇/自然デッキで数多くの勝利を収めたアナカラーを極めし者の証';
$order_symbol{'nwf'}		= '■';
$order_color{'nwf'}		= '#888888';
$order_text{'nwf'}		= '自然/水/火デッキで幾度も勝利を収めた証';
$order_symbol{'highnwf'}	= '□';
$order_color{'highnwf'}		= '#444444';
$order_text{'highnwf'}		= '自然/水/火デッキで数多くの勝利を収めたシータカラーを極めし者の証';
$order_symbol{'dfn'}		= '■';
$order_color{'dfn'}		= '#444400';
$order_text{'dfn'}		= '闇/火/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highdfn'}	= '□';
$order_color{'highdfn'}		= '#444400';
$order_text{'highdfn'}		= '闇/火/自然デッキで数多くの勝利を収めたデアリガズカラーを極めし者の証';

$order_symbol{'nofire'}		= '■';
$order_color{'nofire'}		= '#00bbbb';
$order_text{'nofire'}		= '光/水/闇/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highnofire'}	= '□';
$order_color{'highnofire'}	= '#00bbbb';
$order_text{'highnofire'}	= '光/水/闇/自然デッキで数多くの勝利を収めた火を嫌いし者の証';
$order_symbol{'nonature'}	= '■';
$order_color{'nonature'}	= '#bb00bb';
$order_text{'nonature'}		= '光/水/闇/火デッキで幾度も勝利を収めた証';
$order_symbol{'highnonature'}	= '□';
$order_color{'highnonature'}	= '#bb00bb';
$order_text{'highnonature'}	= '光/水/闇/火デッキで数多くの勝利を収めた自然を嫌いし者の証';
$order_symbol{'nolight'}	= '■';
$order_color{'nolight'}		= '#0000bb';
$order_text{'nolight'}		= '水/闇/火/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highnolight'}	= '□';
$order_color{'highnolight'}	= '#0000bb';
$order_text{'highnolight'}	= '水/闇/火/自然デッキで数多くの勝利を収めた光を嫌いし者の証';
$order_symbol{'nowater'}	= '■';
$order_color{'nowater'}		= '#bbbb00';
$order_text{'nowater'}		= '光/闇/火/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highnowater'}	= '□';
$order_color{'highnowater'}	= '#bbbb00';
$order_text{'highnowater'}	= '光/闇/火/自然デッキで数多くの勝利を収めた水を嫌いし者の証';
$order_symbol{'nodark'}		= '■';
$order_color{'nodark'}		= '#bbbbbb';
$order_text{'nodark'}		= '光/水/火/自然デッキで幾度も勝利を収めた証';
$order_symbol{'highnodark'}	= '□';
$order_color{'highnodark'}	= '#bbbbbb';
$order_text{'highnodark'}	= '光/水/火/自然デッキで数多くの勝利を収めた闇を嫌いし者の証';


$order_symbol{'full'}		= '■';
$order_color{'full'}		= '#88ffff';
$order_text{'full'}		= '５色デッキで幾度も勝利を収めた証';
$order_symbol{'highfull'}	= '□';
$order_color{'highfull'}	= '#88ffff';
$order_text{'highfull'}		= '５色デッキで数多くの勝利を収めた虹を極めし者の証';


$order_symbol{'weak'}		= '◆';
$order_color{'weak'}		= '#008800';
$order_text{'weak'}		= 'カードパワーの低い物を多く使用したデッキで、勝利を収めた事のある証';
$order_symbol{'hirand'}		= '◆';
$order_color{'hirand'}		= '#888888';
$order_text{'hirand'}		= 'ハイランダーデッキで勝利を収めた事のある証';
$order_symbol{'rainbow'}	= '◆';
$order_color{'rainbow'}		= '#88ffff';
$order_text{'rainbow'}		= 'レインボーカードのみで構成されたデッキで勝利を収めた事のある証';
$order_symbol{'long'}		= '●';
$order_color{'long'}		= '#008888';
$order_text{'long'}		= '長期戦の末に勝利を収めた事のある証';

$order_symbol{'ex'}		= '▲';
$order_color{'ex'}		= '#008800';
$order_text{'ex'}		= 'かなり多くのポイントを獲得した、デュエルエキスパートの証';
$order_symbol{'sp'}		= '▲';
$order_color{'sp'}		= '#888888';
$order_text{'sp'}		= 'とてつもなく多くのポイントを獲得した、デュエルスペシャリストの証';
$order_symbol{'dm'}		= '▲';
$order_color{'dm'}		= '#888800';
$order_text{'dm'}		= '想像を絶するほどのポイントを獲得した、デュエルを極めし者・デュエルマスターの証';

$order_symbol{'christmas'}	= '★';
$order_color{'christmas'}	= '#8888ff';
$order_text{'christmas'}	= 'クリスマスにも関わらず、対戦CGIへ現れた孤高のデュエリストである証';

$order_symbol{'valentine'}	= '★';
$order_color{'valentine'}	= '#880000';
$order_text{'valentine'}	= 'バレンタインに恨みと憎しみを募らせ、怒りに燃えるデュエリストである証';

$order_symbol{'aprilfool'}	= '★';
$order_color{'aprilfool'}	= '#880088';
$order_text{'aprilfool'}	= 'エイプリルフールに釣られたか、もしくは勲章コレクターのデュエリストである証';

$order_symbol{'enquete'}	= '★';
$order_color{'enquete'}		= '#FF0000';
$order_text{'enquete'}		= '対戦CGI ex 公式アンケートに回答したことがあるデュエリストである証';
$order_symbol{'kyoryoku'}	= '★';
$order_color{'kyoryoku'}	= '#880088';
$order_text{'kyoryoku'}	= 'カードで遊ぶだけでは飽き足らずサイト構築にまで手を出した開発チームの一員である証';
$order_symbol{'bag'}		= '★';
$order_color{'bag'}		= '#880088';
$order_text{'bag'}		= '重大なバグに遭遇してしまった不幸なデュエリストである証';

$order_symbol{'admin'}		= '☆';
$order_color{'admin'}		= '#8888ff';
$order_text{'admin'}		= '対戦CGI ex を管理する権限を持つ者である証';
$order_symbol{'subadmin'}	= '☆';
$order_color{'subadmin'}	= '#0000ff';
$order_text{'subadmin'}		= '対戦CGI ex を監視する権限を持つ者である証';

$order_symbol{'kaicho'}	= '☆';
$order_color{'kaicho'}	= '#0000ff';
$order_text{'kaicho'}		= 'デュエル・マスターズ推進の会の会長である証';

$order_symbol{'huku'}	= '☆';
$order_color{'huku'}	= '#0000ff';
$order_text{'huku'}		= 'デュエル・マスターズ推進の会の副会長である証';

$order_symbol{'kaiin2'}	= '☆';
$order_color{'kaiin2'}	= '#0000ff';
$order_text{'kaiin2'}		= 'デュエル・マスターズ推進の会会員で、ある程度の位置を持つ者である証';

$order_symbol{'kun'}	= '☆';
$order_color{'kun'}	= '#0000ff';
$order_text{'kun'}		= '対戦cgiの勲章をデザインした勲章クリエイターである証';

$order_symbol{'spfull'}	= '■
';
$order_color{'spfull'}	= '#0000ff';
$order_text{'spfull'}	= '５色デッキで想像を絶するほどの勝利を収めた虹神の証';

$order_symbol{'allzero'}	= '◆
';
$order_color{'allzero'}	= '#0000ff';
$order_text{'allzero'}	= '無色カードのみで構成されたデッキで勝利を収めた事のある証';

$order_symbol{'handess'}	= '◆
';
$order_color{'handess'}	= '#0000ff';
$order_text{'handess'}	= '対戦中に相手の手札を山札の半分以上の枚数捨てた嫌がらせマスターの証';

$order_symbol{'nz'}	= '□
';
$order_color{'nz'}	= '#0000ff';
$order_text{'nz'}	= '自然/無デッキで幾度も勝利を収めた証';

$order_symbol{'randess'}	= '□
';
$order_color{'randess'}	= '#0000ff';
$order_text{'randess'}	= '対戦中に相手のマナを20枚以上墓地へ送った友達イレイサーの勲章';


@uppoint = (50, 150, 300, 500, 750, 1050, 1400, 1800, 2250, 2750, 3300, 3900, 4550, 5250, 6000, 6800, 7650, 8550, 9500, 10500, 11550, 12650, 13800, 15000, 16250);
@rankmark = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z');

$ver			= '5.12b ex';							# デュエルCGIバージョンNo.（変更不要）

open(DNY, "./denyip.dat");
@denyip = <DNY>;
close(DNY);

foreach $denyip (@denyip) {
chomp($denyip);
if(($ENV{'REMOTE_ADDR'} =~ /^$denyip/) && ($ENV{'REMOTE_ADDR'} ne '')) {
print "Content-Type:text/html\n\n";
print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
	"http://www.w3.org/TR/REC-html40/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<meta http-equiv="Pragma" content="no-cache">
	<link rel="stylesheet" href="$css" type="text/css">
	<title>エラー！</title>
</head>
<body>
あなたのホストは、現在アクセス規制をかけられています。<BR>
悪いことをした覚えが無いのにこの画面が出た場合、掲示板などで管理者までご連絡ください。<BR>
<BR>
尚、一般的に荒らし行為は威力業務妨害という犯罪行為の一種です。<BR>
場合によっては、五年以下の懲役又は百万円以下の罰金に処せられます。<BR>
<BR>
<BR>
<A href="http://stardust.sytes.net/~mesis/dm/bbs/fbbs.cgi?id=duel">デュエルマスターズ対戦CGIの掲示板</a><BR>
</body>
</html>
END
exit;
}
}

@denyadd = ();
$ref = lc $ENV{'HTTP_REFERER'};
$ref =~ s/[\:\/\?\=\.]//g;
foreach $denyadd (@denyadd) {
	$ban = lc $denyadd;
	$ban =~ s/[\:\/\?\=\.]//g;
	if($ref =~ /^$ban/) {
		print "Content-Type:text/html\n\n";
		print<<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
	"http://www.w3.org/TR/REC-html40/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
	<meta http-equiv="Content-Style-Type" content="text/css">
	<meta http-equiv="Content-Script-Type" content="text/javascript">
	<meta http-equiv="Pragma" content="no-cache">
	<link rel="stylesheet" href="$css" type="text/css">
	<title>エラー！</title>
</head>
<body>
不正なウェブサイトからのアクセスです。<BR>
規約に違反したページからのリンクは弾かせていただいています。<BR>
<BR>
▼ リンク規約<BR>
　デュエルマスターズ対戦ＣＧＩへのリンクは、基本的に自由です。<BR>
　どのような形でリンクを行って頂いても構いませんが、その際には管理人がメシスであることを明記してください。<BR>
　あたかもメシス以外が管理者であるウェブサイトの一コンテンツであるように扱う事は禁止させていただいております。<BR>
<BR>
▼ 規約違反ウェブサイト一覧<BR>
END
		foreach $denyadd2 (@denyadd) {
			print "　$denyadd2<BR>\n";
		}
		print <<END;
<BR>
<A href="http://www.bmybox.com/~hhhtto/dm/bbs/fbbs.cgi?id=duel">デュエルマスターズ対戦CGIの掲示板</a>
</body>
</html>
END
exit;
	}

}

1;
