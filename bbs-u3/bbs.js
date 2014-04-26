var BbsPathArray=[];
BbsSet();
BbsGet(0);

function BbsReadCookie(bid){
	if(document.cookie=="") return;
	if(!bid) bid="";
	var cookie=document.cookie.split(/[ ;]/);
	for(i in cookie){
		var line=cookie[i].split(/=/,2);
		if(line[0]=="BbsName") document.getElementById('BbsName'+bid).value=unescape(line[1]);
	}
}
function BbsRecordCookie(bid){
	if(!bid) bid="";
	if(document.getElementById('BbsSubmit'+bid).value=="送信中") return(false);
	document.getElementById('BbsSubmit'+bid).value="送信中";
	var str=document.getElementById('BbsName'+bid).value;
	var expires=new Date();
	expires.setYear(expires.getFullYear()+1);
	document.cookie="BbsName="+escape(str)+";path=/;expires="+expires.toGMTString()+";";
	return(true);
}

function BbsShowForm(bid){
	if(!bid) bid="";
	var form=document.getElementById('BbsForm'+bid);
	if(form.style.display=='block'){
		form.style.display="none";
		return;
	}
	BbsReadCookie(bid);
	if(document.getElementById('BbsName'+bid).value=="" && typeof BbsNoname!="undefined"){
		document.getElementById('BbsName'+bid).value=BbsNoname;
	}
	form.style.display="block";
}

function BbsGet(n,bid){
	var obj=document.createElement('script');
	var d=new Date();
	if(!bid){
		bid="";
		obj.src=BbsPath+'page/'+n+'.dat?'+d.getTime();
	}else{
		obj.src=BbsPathArray[bid]+'page/'+n+'.dat?'+d.getTime();
	}
	obj.charset='utf-8';
	var block=document.getElementById('BbsBlock'+bid);
	block.appendChild(obj);
	obj=document.getElementById('BbsNumber');
	obj.innerHTML='&nbsp;'+n+'&nbsp;';
	obj=document.getElementById('BbsLeft'+bid);
	if(n>0){
		if(!bid){
			obj.href='javascript:BbsGet('+(n-1)+',0)';
		}else{
			obj.href='javascript:BbsGet('+(n-1)+','+bid+')';
		}
	}
	obj=document.getElementById('BbsRight'+bid);
	if(!bid){
		obj.href='javascript:BbsGet('+(n+1)+',0)';
	}else{
		obj.href='javascript:BbsGet('+(n+1)+','+bid+')';
	}
}

function BbsPage(page,bid){
	if(!bid) bid="";
	var block,line,obj,d,span;
	var date=new Array();
	block=document.getElementById('BbsContent'+bid);
	while(block.firstChild){
		block.removeChild(block.firstChild);
	}
	for(i in page){
		line=document.createElement('div');
		line.style.borderBottom='1px dashed';
		line.style.margin='5px 0px';
		line.className='BbsContentBlock';
		obj=document.createElement('div');
		obj.innerHTML=page[i].comment;
		obj.className='BbsContentComment';
		line.appendChild(obj);
		obj=document.createElement('div');
		obj.className='BbsContentFooter';
		d=new Date(page[i].time);
		d.setTime(page[i].time*1000);
		date[0]=d.getFullYear();
		date[1]=d.getMonth()+1;
		date[2]=d.getDate();
		date[3]=d.getHours();
		date[4]=d.getMinutes();
		for(j=1;j<5;j++){
			if((""+date[j]).length==1) date[j]='0'+date[j];
		}
		span=document.createElement('span');
		span.className='BbsContentName';
		span.innerHTML=page[i].name;
		if(page[i].id){
			span.title="ID:"+page[i].id;
		}
		obj.appendChild(span);
		if(page[i].trip){
			span=document.createElement('span');
			span.className='BbsContentTrip';
			span.appendChild(document.createTextNode(" #"+page[i].trip));
			obj.appendChild(span);
		}
		span=document.createElement('span');
		span.className='BbsContentTime';
		span.appendChild(document.createTextNode(' [ '+date[0]+'-'+date[1]+'-'+date[2]+' '+date[3]+':'+date[4]+' ]'));
		obj.appendChild(span);
		
		obj.style.textAlign='right';
		line.appendChild(obj);
		block.appendChild(line);
	}
}

function BbsSet(bid){
	if(!bid) bid="";
	var script,block,form,obj;
	script=document.getElementById('BbsScript'+bid);
	while(script.firstChild){
		script.removeChild(script.firstChild);
	}
	block=document.createElement('div');
	block.id='BbsBlock'+bid;
	script.appendChild(block);
	
	obj=document.createElement('a');
	
	obj.appendChild(document.createTextNode("[共有掲示板入力フォーム表示(クリック)]"));
	
	//obj.appendChild(obj=document.createElement('input');obj.type='submit');
	if(!bid){
		obj.href='javascript:BbsShowForm()';
	}else{
		obj.href='javascript:BbsShowForm('+bid+')';
	}
	block.appendChild(obj);
	
	form=document.createElement('form');
	form.id='BbsForm'+bid;
	form.style.margin='0px';
	if(!bid){
		form.action=BbsPath+'write.cgi';
	}else{
		form.action=BbsPathArray[bid]+'write.cgi';
	}
	form.method='post';
	if(form.addEventListener){
		form.addEventListener('submit',function(){BbsRecordCookie(bid)},false);
	}else{
		form.attachEvent('onsubmit',function(){BbsRecordCookie(bid)});
	}
	form.style.display='none';
	
	obj=document.createElement('div');
	obj.appendChild(document.createTextNode('名前'));
	form.appendChild(obj);
	obj=document.createElement('input');
	obj.name='BbsName';
	obj.id='BbsName'+bid;
	obj.style.width='95%';
	obj.style.maxWidth='320px';
	form.appendChild(obj);
	
	obj=document.createElement('div');
	obj.appendChild(document.createTextNode('コメント'));
	form.appendChild(obj);
	obj=document.createElement('textarea');
	obj.name='BbsComment';
	obj.style.width='95%';
	obj.style.maxWidth='320px';
	//obj.style.maxWidth='640px';
	//obj.style.height='10px';
	//obj.style.display='block';
	form.appendChild(obj);
	
	obj=document.createElement('input');
	obj.id="BbsSubmit"+bid;
	obj.type='submit';
	obj.value='書き込む';
	form.appendChild(obj);
	
	block.appendChild(form);
	
	obj=document.createElement('div');
	obj.style.borderTop='1px dashed';
	obj.style.margin='5px 0px';
	obj.id='BbsContent'+bid;
	block.appendChild(obj);
	
	obj=document.createElement('a');
	obj.id='BbsLeft'+bid;
	obj.innerHTML='&nbsp;&lt;&lt;&nbsp;';
	block.appendChild(obj);
	
	obj=document.createElement('span');
	obj.id='BbsNumber';
	obj.innerHTML='&nbsp;0&nbsp;';
	block.appendChild(obj);
	
	obj=document.createElement('a');
	obj.id='BbsRight'+bid;
	obj.innerHTML='&nbsp;&gt;&gt;&nbsp;';
	block.appendChild(obj);
}




