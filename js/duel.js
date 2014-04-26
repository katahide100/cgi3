var Timer = 30 * 1000;

$(function(){ Reload(); })

function Reload() {
	Field();
	var mySEL = document.duel.load.selectedIndex;
	var loadTime = read_only ? 30 : document.duel.load[mySEL].value;
	clearTimeout(Timer);
	Timer = setTimeout('Reload()', loadTime * 1000);
}

function sendData(smode, obj) {
	var E = document.createElement('input');
	$("#mode").val(smode);
	E.name = (obj) ? obj.id : smode;
	E.value = smode != 'block_flg' || obj.checked ? 'on' : '';
	$("#duel").append(E).ajaxSubmit().find('input:last').remove();
	if (smode == "drop") {
		alert('ご利用ありがとうございました。');
		document.duel.action = "taisen.cgi";
		document.duel.mode.value = "";
		document.duel.submit();
	} else {
		if (smode == "regist") $("#mess").val("").focus();
		$("#console :checkbox").attr('checked', false);
		if (smode != "cardlist") {
//			$("select[name=vside]").val(u_side);
			$("select[name=varea]").val(0);
		}
		setTimeout('Field();', 500);
		var mySEL = document.duel.load.selectedIndex;
		var loadTime = read_only ? 30 : document.duel.load[mySEL].value;
		clearTimeout(Timer);
		Timer = setTimeout('Reload()', loadTime * 1000);
	}
}

function Field() {
	$("#field").load(
		"duel.cgi",
		{ mode:"field", room:$('#room').val(), id:$('#id').val(), pass:$('#pass').val() },
		showStatus()
	);
	if (read_only) {
		if (admin == "1") {
			$("#console, #surrender, #roommsg, #dropadmit").hide(); $("#kansen, #messagefield").show();
		} else {
			$("#console, #surrender, #roommsg, #dropadmit, #messagefield").hide(); $("#kansen").show();
		}
	} else {
		if (end_flg == "1") {
			$("#console, #surrender, #dropadmit, #roommsg").hide(); $("#kansen, #messagefield").show();
		} else if (!side1 || !side2) {
			$("#console, #surrender, #dropadmit").hide(); $("#kansen, #roommsg, #messagefield").show();
		} else {
			$("#console, #surrender, #dropadmit, #messagefield").show(); $("#kansen, #roommsg").hide();
		}
	}
}

function showStatus() {
	$("#status").load(
		"duel.cgi",
		{ mode:"status", room:$('#room').val(), id:$('#id').val(), pass:$('#pass').val() },
		showCardlist()
	);
}

function showCardlist() {
	$("#cardList").load(
		"duel.cgi",
		{ mode:"cardlist", room:$('#room').val(), id:$('#id').val(), pass:$('#pass').val(), vside:document.duel.vside.value, varea:document.duel.varea.value },
		showMessage()
	);
}

function showMessage() {
	$("#messageLog").load(
		"duel.cgi",
		{ mode:"mess", room:$('#room').val(), id:$('#id').val(), pass:$('#pass').val() }
	);
}

function stopBubble(e) {
	if (e.target) {
		e.stopPropagation();
	} else if (window.event.srcElement) {
		window.event.cancelBubble = true;
	}
}

function showAlert() {
	var Side = document.duel.vside.value,
	    Area = document.duel.varea.value;
	if (Area == 2 || (Area == 0 && Side == u_side2)) {
		var txt = pn + 'は';
		txt += Side == u_side2 ? '相手の' : '自分の';
		txt += Area == 2 ? '山札' : '手札'
		txt += 'を見た！'
		$.post("duel.cgi", { mode:"regist2", room:$('#room').val(), id:$('#id').val(), pass:$('#pass').val(), mess:txt });
		showMessage();
	}
}