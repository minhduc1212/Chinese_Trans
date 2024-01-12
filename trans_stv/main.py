//qtOnline.js v3.4//created by Sir
//the ngex corp
//this file have copyright, every commercial copy of this file is prohibited.
var contentcontainer = "maincontent";
var abookchapter,abookhost,abookid;
function printStackTrace() {
	try{
		var e = new Error('dummy');
		var stack = e.stack.replace(/^[^\(]+?[\n$]/gm, '')
		.replace(/^\s+at\s+/gm, '')
		.replace(/^Object.<anonymous>\s*\(/gm, '{anonymous}()@')
		.split('\n');
		console.log(stack);
	}
	catch(except){
		console.log(except);
	}
}
var tse={
	ws:{},
	connected:false,
	startconnect:false,
	autoexcute:false,
	connecting:false,
	connect:function(){
		//this.ws.readyState=2;
		//this.ws.connected=true;
		//return;
		if(this.startconnect)return;
		//this.connected=true;
		//return;
		this.startconnect=true;
		if(window.endpoint){
			try{
				if(location.protocol !== "https:"){
					this.ws=new WebSocket("ws://sangtacviet.com"+window.endpoint);
					this.connecting=true;
				}
				else{
					this.ws=new WebSocket("wss://sangtacviet.com"+window.endpoint);
					this.connecting=true;
				}
			}catch(errr){
				try {
					this.ws=new WebSocket("wss://sangtacviet.com"+window.endpoint);
					this.connecting=true;
				} catch(e) {
					this.ws={
						send:function(){void(0);}
					}
				}
			}
		}else{
			this.ws.readyState=2;
			this.connected=true;
		}
		this.ws.onopen=function(){
			tse.lastpacket = new Date().getTime();
			//tse.waiting=[];
			tse.connected=true;
			tse.connecting=false;
			if(tse.autoexcute){
				excute(true);
				tse.autoexcute=false;
			}
			while (tse.waiting.length > 0) {
				var ppacket = tse.waiting.pop();
				this.send(ppacket);
			}
			//clearInterval(tse.monitor);
			//tse.monitor=setInterval(function(){
			//	if(new Date().getTime() - tse.lastpacket > 3500){
			//		tse.ws.close();
			//		clearInterval(tse.monitor);
			//	}
			//}, 500);
		}
		this.ws.onmessage=function(mes){
			var id = parseInt(mes.data.substring(0, 8));
			tse.capture[id].down=mes.data.substring(8);
			try{
				tse.capture[id].callback(tse.capture[id].down);
			}
			catch(except){
				if(true||window.debug){
					console.log(except);
					console.log(tse.capture[id].callback.toString());
					console.log(tse.capture[id].up);	
				}
			}
			tse.pending=tse.pending-1;
			if(tse.pending==0){
				tse.onall();
			}
		}
		this.ws.onerror=function(event){
		    tse.connecting=false;
		}
	},
	lastpacket:0,
	monitor:false,
	reconnect:function(){
		if(this.ws.readyState==3){
			this.connected=false;
			this.startconnect=false;
			this.connect();
		}
	},
	pad:function(n, width, z) {
	    z = z || '0';
	    n = n + '';
	    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
	},
	messageid:1,
	pending:0,
	waiting:[],
	send:function(type,data,callback){
		if(this.ws.readyState==3){
			this.reconnect();
		}
		if(type=="001"){
			if(data=="|"||data=="")return;
			var mea=phrasetree.getmean(data).split("=");
			if(mea.length>1){
				var pk={};
				pk.down=mea[1];
				pk.callback=callback;
				pk.callback(mea[1]);
				return;
			}else if(!window.endpoint){
				this.formXhr(data,function(d){
					var pk={};
					pk.down=d;
					pk.callback=callback;
					pk.callback(d);
				});
				return;
			}
		}
		if(type=="008"){
			if(data=="|"||data=="")return;
			var mea=phrasetree.getmean(data).split("=");
			if(mea.length>1){
				var pk={};
				pk.down=mea[1];
				pk.callback=callback;
				pk.callback(mea[1]);
				return;
			}else if(!window.endpoint){
				this.formXhrMM(data,function(d){
					var pk={};
					pk.down=d;
					pk.callback=callback;
					pk.callback(d);
				});
				return;
			}
		}
		if(type=="007"){
			if(data=="|"||data=="")return;
			var mea=phrasetree.getmean(data);
			if(mea!=""){
				var pk={};
				pk.down=mea;
				pk.callback=callback;
				try{
					pk.callback(mea);
				}catch(xx){}
				return;
			}
			else if(window.endpoint){
				type="004";
			}else{
				this.formXhr(data,function(d){
					var cmb1 = data.split("|");
					var cmb2 = d.split("|");
					var cmbl = [];
					for(var k=0;k<cmb1.length;k++){
						cmbl.push(convertohanviets(cmb1[k]) + "=" + cmb2[k]);
					}
					var pk={};
					pk.down=cmbl.join("|");
					pk.callback=callback;
					try{
						pk.callback(pk.down);
					}catch(xx){}
				});
				return;
			}
		}
		if(type=="005"){
			if(data=="")return;
			else if(!window.endpoint){
				this.formXhr3(data,function(d){
					if(d.contain("|")){
						d="false";
					}
					var pk={};
					pk.down=d;
					pk.callback=callback;
					try{
						pk.callback(pk.down);
					}catch(xx){}
				});
				return;
			}
		}
		if(type=="002"&&(data=="|"||data=="")){
			var pk={};
			pk.down="=";
			pk.callback=callback;
			pk.callback("=");
			return;
		}
		if(type=="004"){
			var mn=phrasetree.getmean(data);
			if(mn){
				var pk={};
				if(mn[0]=="=")
					pk.down=convertohanviets(data)+mn;
				else{
					pk.down=mn;
				}
				pk.callback=callback;
				try{
					pk.callback(pk.down);
				}catch(xx){}
				return;
			}else if(!window.endpoint){
				this.formXhr3(data,function(d){
					var cmb1 = data.split("-");
					var cmb2 = d.split("|");
					var cmbl = [];
					for(var k=0;k<cmb1.length;k++){
						cmbl.push(convertohanviets(cmb1[k]) + "=" + cmb2[k]);
					}
					var pk={};
					pk.down=cmbl.join("|");
					pk.callback=callback;
					try{
						pk.callback(pk.down);
					}catch(xx){}
					//var pk={};
					//pk.down=convertohanviets(data) + "=" + d;
					//pk.callback=callback;
					//try{
					//	pk.callback(pk.down);
					//}catch(xx){}
				});
				return;
			}
		}
		var pk = {};
		pk.id=this.messageid;
		var pa=this.pad(pk.id,8);
		pk.type=type;
		pk.up=data;
		pk.callback=callback||pk.callback;
		this.capture[pk.id]=pk;
		try {
			if(!this.ws.readyState==WebSocket.OPEN && window.endpoint){
				this.waiting.push(pa+pk.type+data);
			}
			else if(window.endpoint){
				this.ws.send(pa+pk.type+data);
				this.lastpacket = new Date().getTime();
			}else{
			}
		} catch(e) {
			console.log(e);
		}
		this.messageid++;
		this.pending++;
	},
	onall:function(){
	},
	capture:{},
	xhrPending:false,
	xhrPending2:false,
	xhrPending3:false,
	formXhr:function(msg,calb){
		if(this.xhrPending==false){
			var pendingMsg = {};
			pendingMsg.msg = [];
			pendingMsg.pending = [];
			pendingMsg.timer = setTimeout(function(){
				pendingMsg.send();
			}, 1000);
			pendingMsg.send = function(){
				window.tse.xhrPending=false;
				var reference = this;
				ajaxUrl(getDomain("https://comic.sangtacvietcdn.xyz/tsm.php"),"sajax=trans&content="+encodeURIComponent(this.msg.join("<split>")),function(down){
					var rspList=down.toLowerCase().split("<split>");
					for(var i=0;i<rspList.length;i++){
						var packet = {
							down: rspList[i].trim(),
							callback : reference.pending[i]
						}
						packet.callback(packet.down);
					}
					//replaceName();
					//meanSelector();
				},"/index.php");
			}
			pendingMsg.add = function(msg,calb){
				this.pending.push(calb);
				this.msg.push(msg);
			}
			this.xhrPending = pendingMsg;
		}
		this.xhrPending.add(msg,calb);
	},
	formXhr2:function(msg,calb){
		if(this.xhrPending2==false){
			var pendingMsg = {};
			pendingMsg.msg = [];
			pendingMsg.pending = [];
			pendingMsg.timer = setTimeout(function(){
				pendingMsg.send();
			}, 1000);
			pendingMsg.send = function(){
				window.tse.xhrPending2=false;
				var reference = this;
				ajax("sajax=worddict&content="+encodeURIComponent(this.msg.join("<split>")),function(down){
					var rspList=down.substring(1).toLowerCase().split("<split>");
					for(var i=0;i<rspList.length;i++){
						var packet = {
							down: rspList[i].trim(),
							callback : reference.pending[i]
						}
						packet.callback(packet.down);
					}
				});
			}
			pendingMsg.add = function(msg,calb){
				this.pending.push(calb);
				this.msg.push(msg);
			}
			this.xhrPending2 = pendingMsg;
		}
		this.xhrPending2.add(msg,calb);
	},
	formXhr3:function(msg,calb){
		if(this.xhrPending3==false){
			var pendingMsg = {};
			pendingMsg.msg = [];
			pendingMsg.pending = [];
			pendingMsg.timer = setTimeout(function(){
				pendingMsg.send();
			}, 350);
			pendingMsg.send = function(){
				window.tse.xhrPending3=false;
				var reference = this;
				ajaxUrl(getDomain("https://comic.sangtacvietcdn.xyz/tmm.php"),"sajax=transmulmean&wp=1&content="+encodeURIComponent(this.msg.join("<split>")),function(down){

					var rspList=down.toLowerCase().split("<split>");
					for(var i=0;i<rspList.length;i++){
						var packet = {
							down: rspList[i].trim(),
							callback : reference.pending[i]
						}
						packet.callback(packet.down);
					}
				},"/index.php");
			}
			pendingMsg.add = function(msg,calb){
				this.pending.push(calb);
				this.msg.push(msg);
			}
			this.xhrPending3 = pendingMsg;
		}
		this.xhrPending3.add(msg,calb);
	}
};

var callb=[];
var store = localStorage;
var calfunc={
	func:function(e){},
	excute:function(e){func(e);isrunned=true;},
	isrunned:false
}
if (window.NodeList && !NodeList.prototype.forEach) {
    NodeList.prototype.forEach = function (callback, thisArg) {
        thisArg = thisArg || window;
        for (var i = 0; i < this.length; i++) {
            callback.call(thisArg, this[i], i, this);
        }
    };
}
function findsel(){
	if(window.isMobile){
		return;
	}
	var sel = getSelectionText();
	if(sel!=""){
		g("fastseltext").value=sel;
		g("fastgentext").value=titleCase(sel);
	}
}
function bigsel(){
	
}
function arrtoobj(arr){
	var obj={};
	for(var i=0;i<arr.length;i++){
		obj[arr[i]]=true;
	}
	obj.indexOf = function(find){
		if(find in this)return 1;
		return -1;
	}
	obj.have=function(find) {
		return find in this;
	}
	return obj;
}
function arrstoobj(arrs){
	var obj={};
	var l;
	for(var c=0;c<arrs.length;c++){
		l=arrs[c].length;
		for(var i=0;i<l;i++){
			obj[arrs[c][i]]=true;
		}
	}
	obj.indexOf = function(find){
		if(find in this)return 1;
		return -1;
	}
	obj.have=function(find) {
		return find in this;
	}
	return obj;
}
function fastAddNS(){
	var left = g("fastseltext");
	var right = g("fastgentext");
	if(left!=""){
		namew.value += "\n"+left.value+"="+right.value;
	}
	saveNS();
}
var runned=false;
function joinfromto(arr,st,en){
	var str="";
	for(var i=st;i<=en;i++){
		str+=arr[i];
	}
	return str;
}
Array.prototype.joinlast = function(last){
	for(var i=0;i<last;i++)this.shift();
	return this.join("=");
};
function flushToView() {
	var tmpct = g(contentcontainer);
	g("tmpcontentview").innerHTML=tmpct.innerHTML//.replace(/<\/?p>/g,"<br>")
		.replace(/ ,/g,",").replace(/<br>/g,"<p>").replace(/<br \/>/g,"</p>")
		.replace(/ \./g,".");//.replace(/ (<i.*?><\/i>),/g,"$1,");
	g("tmpcontentview").id=contentcontainer;
	tmpct.id="tmpcontentdiv";
}
function pushFromView(){
	var tmpct = g("tmpcontentdiv");
	tmpct.innerHTML=g(contentcontainer).innerHTML.replace(/<p>/g,"<br>").replace(/<\/p>/g,"<br />");//.replace(/<br>/g)
	g(contentcontainer).id="tmpcontentview";
	tmpct.id=contentcontainer;
}
function excute(invokeMeanSelector){
	if(g(contentcontainer)==null)return;
	if(typeof(thispage)=="undefined")return;
	if(!defined)return;
	if(getCookie("foreignlang") && getCookie("foreignlang") != "vi"){
		return;
	}
	if(getCookie("transmode") == "chinese"){
		return;
	}
	if(dictionary && dictionary.finished==false){
		dictionary.readTextFile("//sangtacviet.com/wordNoChi.htm?update=1");
		phrasetree.load();
		tse.connect();
		return;
	}
	if(tse.ws.readyState!=1){
		tse.autoexcute=true;
		tse.connect();
	}
	var curl = document.getElementById("hiddenid").innerHTML.split(";");
	var book=curl[0];
	var chapter = curl[1];
	var host = curl[2];
	if(host=="sangtac")return;
	hideNb();
	//if(g("tmpcontentdiv")){
	//	pushFromView();
	//}
	
	if(host!="dich")
	fastNaming();
	prediction.enable=true;
	if(window.endpoint){
		
	}
	var reg;
	if(window.setting!=null&&window.setting.onlyonename){
		reg= store.getItem("qtOnline0");
	}else
	reg = store.getItem(host+book);
	if(reg==null){
		reg = store.getItem(book);
		if(reg!=null){
			store.setItem(host+book,reg);
		}
	}
	if(reg!=null || window.bookHaveDefaultName){
		if(!reg){
			reg = "";
		}
		var rowlist = reg.split("~//~");
		if(window.namew==null){
			window.namew=g("namewd");
		}
		if(namew==null){
			setTimeout(function(){
				excute();
			}, 500);
			return;
		}
		namew.value=rowlist.join("\n");
		// if(!window.setting && window.bookHaveDefaultName){
		// 	setTimeout(function(){
		// 		excute();
		// 	}, 500);
		// 	return;
		// }
		if(window.bookHaveDefaultName && window.setting && !window.setting.disabledefaultname){
			var dfname = window.bookDefaultName.split("\n");
			dfname.forEach(function(e){
				if(e!=""){
					var row = e.split("=");
					if(row.length<2){}
					else{
						if(row[0]!=""){
							if(row[0].charAt(0)=="@"){
								row[0]=row[0].substring(1).split("|");
								if(row[1]!=null)
									row[1]=row[1].split("|");
								replaceByNode(row[0],row[1]);
							}else 
							if(row[0].charAt(0)=="#"){
								dictionary.set(row[0].substring(1),row[1]);
							}else 
							if(row[0].charAt(0)=="$"){

								var sear=row[0].substring(1);
								var rep=row.joinlast(1);
								if(sear.length==1){
									if(convertohanviets(sear)==rep.toLowerCase()){
										return;
									}
								}
								if(true){

									dictionary.set(sear,rep);
									nametree.setmean(sear,"="+rep);
								}else
								replaceOnline(sear,rep);
							}else 
							if(row[0].charAt(0)=="~"){
								meanengine(e.substr(1));
							}
							else{
								toeval2+="replaceByRegex(\""+eE(row[0])+"\",\""+eE(row[1])+"\");";
							}
						}
						
					}

				}
			});
		}
		rowlist.forEach(function(e){
			if(e!=""){
				var row = e.split("=");
				if(row.length<2){
					
				}
				else{
					if(row[0]!=""){
						if(row[0].charAt(0)=="@"){
							row[0]=row[0].substring(1).split("|");
							if(row[1]!=null)
								row[1]=row[1].split("|");
							replaceByNode(row[0],row[1]);
						}else 
						if(row[0].charAt(0)=="#"){
							dictionary.set(row[0].substring(1),row[1]);
						}else 
						if(row[0].charAt(0)=="$"){
							var sear=row[0].substring(1);
							var rep=row.joinlast(1);
							if(sear.length==1){
								if(convertohanviets(sear)==rep.toLowerCase()){
								//	return;
								}
							}
							if(window.setting&&window.setting.allownamev3){
								dictionary.set(sear,rep);
								nametree.setmean(sear,"="+rep);
							}else
							replaceOnline(sear,rep);
						}else 
						if(row[0].charAt(0)=="~"){
							meanengine(e.substr(1));
						}
						else{
							toeval2+="replaceByRegex(\""+eE(row[0])+"\",\""+eE(row[1])+"\");";
						}
					}
					
				}

			}
		});

	}
	replaceVietphrase();
	if(window.setting&& window.setting.allownamev3){
		replaceName();
	}
	needbreak=false;
	//meanstrategy.invoker= !meanstrategy.invoker ? setTimeout(function(){
	//		
	//}, 10) : 0;
	meanengine.usedefault();
	if(!tse.connecting){
		if(invokeMeanSelector==null || invokeMeanSelector!==false){
			window.meanSelectorCheckpoint = 0;
			if(window.lazyProcessor){
				window.lazyProcessor.clear();
			}
			meanSelector();
			setTimeout(function(){
				//replaceName();
			}, 1200);
		}
	}
	
	setTimeout(doeval,100);
	runned=true;
}
function talkDetection(){
	if(q("#"+contentcontainer + " i.talk").length>0){
		return;
	}
	console.time("talkDetection");
	var nodes = q('[id^="exran"]');
	var fullNodes = flatNodes();
	for(var i=0;i<nodes.length;i++){
		var node = nodes[i];
		if(node.textContent.contain("â€œ")){
			(function(nodes,start){
				var end = start;
				var count = 0;
				var max = 30;
				var n = nodes[start+1];
				while(n!=null && count<max){
					if(n.textContent.contain("â€")){
						end = start+count+1;
						break;
					}
					count++;
					n = nodes[start+count+1];
				}
				if(end>start){
					for(var i=start;i<=end;i++){
						if(nodes[i].tagName == "I"){
							nodes[i].classList.add("talk");
						}
					}
				}
			})(fullNodes, fullNodes.indexOf(node));
		}
	}
	console.timeEnd("talkDetection");
}
function excuteApp(invokeMeanSelector){
	if(g(contentcontainer)==null)return;
	if(typeof(thispage)=="undefined")return;
	if(!defined)return;
	if(getCookie("foreignlang") && getCookie("foreignlang") != "vi"){
		return;
	}
	if(getCookie("transmode") == "chinese"){
		return;
	}
	if(dictionary.finished==false){
		dictionary.readTextFile("//sangtacviet.com/wordNoChi.htm?update=1");
		phrasetree.load();
		tse.connect();
		return;
	}
	var curl = document.getElementById("hiddenid").innerHTML.split(";");
	var book=curl[0];
	var chapter = curl[1];
	var host = curl[2];
	if(host=="sangtac")return;
	
	if(host!="dich")
	fastNamingApp();
	talkDetection();
	prediction.enable=true;
	var rowlist = namew.value.split("\n").concat(namew.valueglobal.split("\n"));
	
	if(window.bookHaveDefaultName && window.setting && !window.setting.disabledefaultname){
		var dfname = window.bookDefaultName.split("\n");
		dfname.forEach(function(e){
			if(e!=""){
				var row = e.split("=");
				if(row.length<2){}
				else{
					if(row[0]!=""){
						if(row[0].charAt(0)=="@"){
							row[0]=row[0].substring(1).split("|");
							if(row[1]!=null)
								row[1]=row[1].split("|");
							replaceByNode(row[0],row[1]);
						}else 
						if(row[0].charAt(0)=="#"){
							dictionary.set(row[0].substring(1),row[1]);
						}else 
						if(row[0].charAt(0)=="$"){

							var sear=row[0].substring(1);
							var rep=row.joinlast(1);
							if(sear.length==1){
								if(convertohanviets(sear)==rep.toLowerCase()){
									return;
								}
							}
							if(true){

								dictionary.set(sear,rep);
								nametree.setmean(sear,"="+rep);
							}else
							replaceOnline(sear,rep);
						}else 
						if(row[0].charAt(0)=="~"){
							meanengine(e.substr(1));
						}
						else{
							toeval2+="replaceByRegex(\""+eE(row[0])+"\",\""+eE(row[1])+"\");";
						}
					}
					
				}

			}
		});
	}
	rowlist.forEach(function(e){
		if(e!=""){
			var row = e.split("=");
			if(row.length<2){
				
			}
			else{
				if(row[0]!=""){
					if(row[0].charAt(0)=="@"){
						row[0]=row[0].substring(1).split("|");
						if(row[1]!=null)
							row[1]=row[1].split("|");
						replaceByNode(row[0],row[1]);
					}else 
					if(row[0].charAt(0)=="#"){
						dictionary.set(row[0].substring(1),row[1]);
					}else 
					if(row[0].charAt(0)=="$"){
						var sear=row[0].substring(1);
						var rep=row.joinlast(1);
						if(sear.length==1){
							if(convertohanviets(sear)==rep.toLowerCase()){
							//	return;
							}
						}
						if(window.setting&&window.setting.allownamev3){
							dictionary.set(sear,rep);
							nametree.setmean(sear,"="+rep);
						}else
						replaceOnline(sear,rep);
					}else 
					if(row[0].charAt(0)=="~"){
						meanengine(e.substr(1));
					}
					else{
						toeval2+="replaceByRegex(\""+eE(row[0])+"\",\""+eE(row[1])+"\");";
					}
				}
				
			}

		}
	});
	replaceVietphrase();
	if(window.setting&& window.setting.allownamev3){
		replaceName();
	}
	needbreak=false;
	meanengine.usedefault();
	if(!tse.connecting){
		if(invokeMeanSelector==null || invokeMeanSelector!==false){
			window.meanSelectorCheckpoint = 0;
			if(window.lazyProcessor){
				window.lazyProcessor.clear();
			}
			meanSelector();
			setTimeout(function(){
				//replaceName();
			}, 1200);
		}
	}
	
	setTimeout(doeval,100);
	runned=true;
}
function autocheck(){
	if(!runned)excute();
}
function sortname(){
	var nameTextArea = null;
	if(!window.namew){
		window.namew = document.getElementById("namewd");
		if(!window.namew){
			return;
		}
	}
	nameTextArea = window.namew;
	var str=nameTextArea.value.split("\n").sort();
	for(var i=9999;i<str.length;i++){
		if(str[i].charAt(0)=="$"){
			if(str[i+1]!=null&&(str[i+1].substring(0,str[i].split("=")[0].length)==str[i].split("=")[0])){
				if(str[i+1].length=str[i].length+1){
					if(str[i+1].lastChar()!="çš„"){
						str[i]="";
					}
				}
			}
		}
	}
	for(var i=0;i<str.length;i++){
		if(str[i+1]===str[i]){
			str[i+1]="";
		}
	}
	str=str.sort(function(a,b){if(a.charAt(0)=="#")return -1; else return a.split("=")[0].length - b.split("=")[0].length;});
	var lastans="";
	for(var i=0;i<str.length;i++){
		if(str[i]!=""){
			lastans+=str[i]+"\n";
		}
	}
	nameTextArea.value=lastans;
	saveNS();
}
function ensure(node,id){
	var nodelist=g(contentcontainer).childNodes;
	var exranid=0;
	nodelist.forEach(function(e){
		if(e.nodeType==3){
			if(e.textContent.match(/[^ \.,â€œ\:\?â€\!\"\*\)\(\$\^\+\@\%\|\/\=\ã€‘ã€ã€Œã€Œã€â€¦ã€Šã€‹â€˜â€™\r\n]/)){
				converttonode(e,id+"r"+exranid);
				exranid++;
			}
		}
		if(e.tagName=="p"){
			ensure(e,id+"r"+id);
		}
	});
}
function flatNodes(){
	if(q("#" + contentcontainer + " p").length>0){
		var result = [];
		var nodelist=g(contentcontainer).childNodes;
		nodelist.forEach(function(e){
			if(e.tagName=="P"){
				var nodelist2=e.childNodes;
				result = result.concat(Array.from(nodelist2));
			}else{
				result.push(e);
			}
		});
		return result;
	}
	var nodelist=g(contentcontainer).childNodes;
	return nodelist;
}
function fastNaming(){
	if(g(contentcontainer)==null)return;
	if(getCookie("transmode") == "tfms"||getCookie("transmode") == "bing"){
		return;
	}
	var nodelist= flatNodes();//g(contentcontainer).childNodes;
	var exranid=0;
	nodelist.forEach(function(e){
		if(e.nodeType==3){
			if(e.textContent===" "){
				e.isspacehidden=true;
				return;
			}
			if(e.textContent.match(/[^ \.,â€œ\:\?â€\!\"\*\)\(\$\^\+\@\%\|\/\=\ã€‘ã€ã€Œã€Œã€â€¦ã€Šã€‹â€˜â€™\r\n\u200B]/)){
				converttonode(e,"exran"+exranid);
				exranid++;
			}
			e.isexran=true;
		}
		if(e.tagName=="p"){
			ensure(e,exranid);
		}
		if(e.nodeType==8){
			e.remove();
		}
	});
	//var str = document.getElementById(contentcontainer).innerHTML;
	var keyword1 = ["ã€Š","ã€Œ","ã€Ž","ã€ˆ","ã€","ï¼»","â€˜","â€œ"];
	keyword1.forEach(function(e){
	//	var regx = new RegExp("("+e+")","ig");
	//	str = str.replace(regx,"<span class='fastname' style='text-transform:capitalize'>$1");
	});
	var keyword2 = ["ã€‘","ï¼½","ã€","ã€","ã€‹","ã€‰","â€™","â€"];
	keyword2.forEach(function(e){
	//	var regx = new RegExp("("+e+")","ig");
	//	str = str.replace(regx,"</span>$1");
		
	}); 
	
	//g(contentcontainer).innerHTML = str;
	q(".fastname").forEach(function(e){
		if(e.innerText.length>60)e.style.textTransform = "";
	});
}
function fastNamingApp(){
	if(g(contentcontainer)==null)return;
	if(getCookie("transmode") == "tfms"||getCookie("transmode") == "bing"){
		return;
	}
	var nodelist= flatNodes();
	var exranid=0;
	nodelist.forEach(function(e){
		if(e.nodeType==3){
			if(e.textContent===" "){
				e.isspacehidden=true;
				return;
			}
			if(e.textContent.match(/[^ \.,\:\?\!\"\*\)\(\$\^\+\@\%\|\/\=\ã€‘ã€ã€Œã€Œã€â€¦ã€Šã€‹â€˜â€™\r\n\u200B]/)){
				converttonode(e,"exran"+exranid);
				exranid++;
			}
			e.isexran=true;
		}
		if(e.tagName=="p"){
			ensure(e,exranid);
		}
		if(e.nodeType==8){
			e.remove();
		}
	});
}
function instring(str1,str2){
	for(var i=0;i<str2.length;i++){
		if(str1.indexOf(str2.charAt(i))>=0)return true;
	}
	return false;
}
Element.prototype.containName = function(){
	//return this.textContent.toLowerCase()!=this.textContent;
	return this.isname()||((titleCase(this.textContent)==this.textContent)&&this.textContent.indexOf(" ")>0);
};
Element.prototype.containHan = function(callback,none,nofast){
	var t=this.gT();
	if(instring(t,meanstrategy.ignore)){
		if(this.pE())
		if(!instring(t,meanstrategy.ignore2)||meanstrategy.testcommon([this.pE(),this])<2){
			return;
		}
	}
	if(this.isname())return;
	if(!nofast&&(this.textContent==this.gH()||this.containName())){
		callback();
		return;
	}
	if(t in meanstrategy.database){
		if(meanstrategy.database[t].toLowerCase().indexOf(this.gH())>=0){
			callback(meanstrategy.database[t]);
		}
		return;
	}
	var _self=this;
	var mean=phrasetree.getmean(t);
	if(mean!=""){
		mean=mean.split("=")[1];
		if(mean!=null){
			if(mean.toLowerCase().indexOf(this.gH())>=0){
				callback(mean);
			}else if (none!=null) {
				none();
			}
		}
		
	}else if(this.mean()){
		if(this.mean().toLowerCase().indexOf(this.gH())>=0){
			callback(this.mean());
		}else if (none!=null) {
			none();
		}
	}
	else
	tse.send("001",t,function(){
		meanstrategy.database[this.up]=this.down;
		if(_self.isname())return;
		if(this.down.toLowerCase().indexOf(_self.gH())>=0){ 
			callback(this.down);
		}else if (none!=null) {
			none();
		}
	});
};
Element.prototype.containHan2 = function(nofast){
	var t=this.gT();
	if(instring(t,meanstrategy.ignore)){
		if(this.pE())
		if(!instring(t,meanstrategy.ignore2)||meanstrategy.testcommon([this.pE(),this])<2){
			return false;
		}
	}
	if(this.isname())return false;
	if(!nofast&&(this.textContent==this.gH()||this.containName())){
		return this.textContent;
	}
	var _self=this;
	var mean=phrasetree.getmean(t).trim();
	if(mean!=""){
		mean=mean.split("=")[1];
		if(mean!=null){
			if(mean.toLowerCase().indexOf(this.gH())>=0){
				return mean;
			}
		}
		
	}else if(this.mean()){
		var m = this.mean().trim();
		if(m.length >= 1 && m.toLowerCase().indexOf(this.gH())>=0){
			return this.mean();
		}
	}
	return false;
};
Element.prototype.mean =function(){
	return this.getAttribute("v");
}
Element.prototype.near=function(end){
	if(end){
		var walked=0;
		var nod=this;
		for(var i=0;i<3;i++){
			if(nod.nextSibling!=null){
				walked+=nod.gT().length;
				if(walked>7)return false;
				if(/[\.,]/.test(nod.nextSibling.textContent)){
					return true;
				}
				nod=nod.nextElementSibling;
				if(!nod){
					return true;
				}
				if(nod.tagName=="BR")return true;
			}else return true;
		}
		return false;
	}else {
		var walked=0;
		var nod=this;
		for(var i=0;i<3;i++){
			if(nod.previousSibling!=null){
				walked+=nod.gT().length;
				if(walked>7)return false;
				if(/[\.,]/.test(nod.previousSibling.textContent)){
					return true;
				}
				nod=nod.previousElementSibling;
				if(!nod)return true;
				if(nod.tagName=="BR")return true;
			}else return true;
		}
		return false;
	}
}
Element.prototype.pE = function(){
	return this.previousElementSibling;
};
Element.prototype.nE = function(){
	return this.nextElementSibling;
};
Element.prototype.gT = function(){
	return this.cn||this.getAttribute("t")||"";
};
Element.prototype.gP = function(){
	return this.getAttribute("p")||"";
};
Element.prototype.gH = function(){
	return this.getAttribute("h")||"";
};
Element.prototype.isname = function(){
	return this.getAttribute("isname")==="true";
};
Element.prototype.tomean = function(mean) {
	if(mean==""){
		this.textContent="";
		return;
	}
	//if(this.pE() && this.pE().tagName!="BR"){
	if(!isUppercase(this)){
		//if(this.previousSibling.textContent.indexOf(".")>-1){
		//	this.textContent=mean[0].toUpperCase() + mean.substring(1);
		//}else
		this.textContent=mean;
	}else{
		this.textContent=mean[0].toUpperCase() + mean.substring(1);
	}
};
Element.prototype.getmean = function(callb){
	if(this.gT() in meanstrategy.database){
		callb(meanstrategy.database[this.gT()]);
	}else {
		tse.send("001",this.gT(),function(){
			meanstrategy.database[this.up]=this.down.trim();
			callb(this.down.trim());
		});
	}
};
Element.prototype.isspace = function(right){
///	if(right)return this.nextSibling!=null&&this.nextSibling.textContent===" ";
//	else {
//		return this.previousSibling!=null&&this.previousSibling.textContent===" ";
//	}
	if(right)return this.nextSibling!=null&&(this.nextSibling.textContent===" "||this.nextSibling.isspacehidden);
	else {
		return this.previousSibling!=null&&(this.previousSibling.textContent===" "||this.previousSibling.isspacehidden);
	}
};
String.prototype.splitn=function(n){
	var arr=[];
	var str="";
	var chars=0;
	for(var i=0;i<this.length;i++){
		str+=this.charAt(i);
		chars++;
		if(n==chars){
			arr.push(str);
			str="";
			chars=0;
		}
	}
	if(str!="")arr.push(str);
	return arr;
}
var looper={
	search:function(node,right,max,find,senonly){
		if(right){
			for(var i=0;i<max;i++){
				node=node.nE();
				if(node==null)return false;
				if(senonly&&!node.isspace(false))return false;
				if(node.gT()[0]==find){
					return node;
				}
			}
		}else{
			for(var i=0;i<max;i++){
				node=node.pE();
				if(node==null)return false;
				if(senonly&&!node.isspace(true))return false;
				if(node.gT().lastChar()==find){
					return node;
				}
			}
		}
		return false;
	},
	searchphrase:function(node,right,max,find,senonly){
		if(right){
			for(var i=0;i<max;i++){
				node=node.nE();
				if(node==null)return false;
				if(senonly&&!node.isspace(false))return false;
				if(node.gT().indexOf(find)==0){
					return node;
				}
			}
		}else{
			for(var i=0;i<max;i++){
				node=node.pE();
				if(node==null)return false;
				if(senonly&&!node.isspace(true))return false;
				if(node.gT().endwith(find)){
					return node;
				}
			}
		}
		return false;
	},
	searchphraseex:function(node,right,max,find,senonly){
		if(right){
			for(var i=0;i<max;i++){
				node=node.nE();
				if(node==null)return false;
				if(senonly&&!node.isspace(false))return false;
				for(var j=0;j<find.length;j++)
				if(node.gT().indexOf(find[j])==0){
					return node;
				}
			}
		}else{
			for(var i=0;i<max;i++){
				node=node.pE();
				if(node==null)return false;
				if(senonly&&!node.isspace(true))return false;
				for(var j=0;j<find.length;j++)
				if(node.gT().endwith(find[j])){
					return node;
				}
			}
		}
		return false;
	},
	searchex:function(node,right,max,find,senonly){
		if(right){
			for(var i=0;i<max;i++){
				node=node.nE();
				if(node==null)return false;
				if(senonly&&!node.isspace(false))return false;
				if(find.indexOf(node.gT()[0])>-1){
					return node;
				}
			}
		}else{
			for(var i=0;i<max;i++){
				node=node.pE();
				if(node==null)return false;
				if(senonly&&!node.isspace(true))return false;
				if(find.indexOf(node.gT().lastChar())>-1){
					return node;
				}
			}
		}
		return false;
	}
}
function pIsNewLine(node){
	if(node.pE()){
		return node.pE().tagName=="BR";
	}else return true;
}
function isUppercase(node){
	if(node.push){
		node = node[0];
	}
	if(node.pE()){
		if(node.pE().tagName=="BR"){
			return true;
		}else return /[ã€Š:\.â€œ]/.test(node.previousSibling.textContent);
	}else return true;
}
function ucFirst(t){
	if(t.length > 0)
		return t[0].toUpperCase() + t.substring(1);
	return "";
}
function getDefaultMean(node){
	if(!node.getAttribute){
		return node.textContent;
	}
	var m =  node.getAttribute("v");
	if(typeof m !="undefined" && m!=null){
		return m.split("/")[0] || "";
	}else if(m==null){
		console.log(node);
	}
	return node.gH();
}
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

var meanstrategy={
	"collected":"",
	"nodelist":{},
	"highlight":function(node,type){
		try{
		if(setting.highlight===true){
			switch (type) {
				case "f":
					node.style.backgroundColor = '#78aafa';
					break;
				case "m":
					node.style.backgroundColor = '#eeeeee';
					break;
				case "o":
					node.style.backgroundColor = '#38ff38';
					break;
				case "s":
					node.style.backgroundColor = '#8fceab';
					break;
				case "e":
					node.style.backgroundColor = '#d866ff';
					break;
				case "i":
					node.style.backgroundColor = '#80fafd';
					break;
				case "ln":
					node.style.backgroundColor = '#bae7b4';
				default:break;
			}
		}
		}catch(xxx){}
	},
	"countname":function(right,start,max){
		if(!right){
			var pnum = 0;
			var count = 0;
			var curnod = start;
			while (pnum < max && curnod.previousElementSibling != null) {
				pnum++;
				curnod = curnod.previousElementSibling;
				if(curnod.containName()){
					count++;
				}
			}
			return count;
		}else {
			var pnum = 0;
			var count = 0;
			var curnod = start;
			while (pnum < max && curnod.nextElementSibling != null) {
				pnum++;
				curnod = curnod.nextElementSibling;
				if(curnod.containName()){
					count++;
				}
			}
			return count;
		}
	},
	scope:function(node,type){
		if(!setting.scopefilter){
			return;
		}
		var curnod=node.nextSibling;
		var nodlist=[];
		var walked=0;
		var flag=false;
		var tester=this.database.scope.close.charAt(this.database.scope.open.indexOf(type));
		var breaker=/[.;:,?!]/;
		var looped=0;
		while (curnod!=null) {
			looped++;
			if(looped>10)return;
			if(curnod.nodeType==Element.TEXT_NODE){
				continue;
			}
			var cn = curnod.gT ? curnod.gT() : "";
			walked+=cn.length;
			if(walked>6)return;
			nodlist.push(curnod);
			if(curnod.nextSibling!=null){
				if(curnod.nextSibling.textContent.indexOf(tester)>-1){
					flag=1;
					break;
				}
				if(breaker.test(curnod.nextSibling.textContent)){
					return;
				}
			}
			if(!curnod.nE){
				return;
			}
			curnod=curnod.nE();
			if(curnod==null||curnod.tagName=="BR"){
				return;
			}
		}
		if(flag){
			nodlist.forEach( function(e) {
				e.containHan(function(){
					e.textContent=meanstrategy.testsuffix(e.gT(),titleCase(e.gH()));
				});
			});
			if(walked<6){
				if(type!="â€˜")
				analyzer.update(nodlist.sumChinese(),3);
			}
		}
	},
	worddelay:function(node){
		if(node.previousSibling
			&&node.previousSibling.tagName=='I'
			&&node.previousSibling.gT().length==1
		){
			if(node.nextSibling
				&&node.nextSibling.tagName=='I'
				&&node.nextSibling.gT().charAt(0)==node.previousSibling.gT()
				&&!this.database.pronoun.contain(node.previousSibling.gT())
			){
				var neww=node.nextSibling.innerHTML.split(" ")[0]; //titleCase(node.previousSibling.gH());
				if(node.previousSibling.gT() in this.database.preposition){
					neww=titleCase(this.database.preposition[node.previousSibling.gT()]);
				}
				node.previousSibling.textContent=neww;
				if(node.nextSibling.gT().length==1){
					//node.nextSibling.innerHTML=neww;
				}
				this.highlight(node,"m");
			}
		}
	},
	meancomparer:function(arr1,arr2,allowback){
		for(var i=0;i<arr1.length;i++){
			var tx=arr1[i].split(" ");
			var lastword=tx.pop();
			for (var j = 0; j < arr2.length; j++) {
				if(lastword==arr2[j].split(" ")[0]){
					tx=tx.join(" ").trim() +" "+ arr2[j].trim();
					if(allowback){
						tx=tx.replace("giÃ¡","cÃ¡i nÃ y")
						.replace("nÄƒng","cÃ³ thá»ƒ");
					}
					return {
						code:true,
						new:tx
					};
				}
			}
		}
		return {code:false};
	},
	wordconnector:function(node){
		if(this.connectignore.indexOf(node.gT())>-1)return;
		if(node.isspace(false)){
			try{
				if(node.pE()!=null){
					if(node.pE().isname())return;
					if(node.pE().gT().length>3||node.pE().gT()<2)return;
					node.pE().getmean(function(mean1){
						if(!node.pE()){
							return;
						}
						var phrase=[node.pE(),node].sumChinese("");
						var chi2=phrase.substring(node.pE().gT().length-1);
						meanstrategy.database.getmean(chi2,function(mean2){
							if(mean2=="false")return;
							mean1=mean1.split("/");
							mean2=mean2.split("/");
							var ret={code:false};
							if (/[è¿™èƒ½]/.test(node.pE().gT())) {
								ret=meanstrategy.meancomparer([node.pE().gH()],mean2,true);
								if(ret.code){
									node.pE().innerHTML=ret.new;
									node.pE().setAttribute("t", phrase);
									node.pE().cn=phrase;
									node.pE().setAttribute("h", node.pE().gH()+" "+node.gH());
									meanstrategy.highlight(node.pE(),"m");
									node.innerHTML="";
									node.setAttribute("h","");
									node.setAttribute("t","");
									node.cn="";
									node.remove();
								}
							}
							if(!ret.code){
								ret=meanstrategy.meancomparer(mean1,mean2);
								if(ret.code){
									node.pE().innerHTML=ret.new;
									node.pE().setAttribute("t", phrase);
									node.pE().cn=phrase;
									node.pE().setAttribute("h", node.pE().gH()+" "+node.gH());
									meanstrategy.highlight(node.pE(),"m");
									node.innerHTML="";
									node.setAttribute("h","");
									node.setAttribute("t","");
									node.cn="";
									node.remove();
								}
							}
						});
					});
				}
			}catch(e){}
		}
	},
	//inode: @locate
	loctransform:function(node,mean1,mean2){
		return;
		if(node.innerHTML!=""&&!node.innerHTML.contain(mean2))return;
		var nd=looper.searchex(node,false,3,'åœ¨ä»ŽäºŽ',true);
		if(nd){
			var nmean = "";
			var mean3 = mean2;
			if(nd.nE().gT()=="è¿™"){
				nmean="nÃ y";
				nd.nE().innerHTML="";
			}
			if(nd.nE().gT()=="è¿™ä¸ª"){
				nmean="nÃ y";
				nd.nE().innerHTML="";
				mean2+=" cÃ¡i";
			}
			if(node.gT().length==1){
				nd.innerHTML+=" "+mean2;
				if(nmean != ""){
					//node.innerHTML=node.innerHTML.replace(mean1,"").replace(mean3,"").replace("nÃ y","") + "nÃ y";
					node.innerHTML=nmean;
				}else
				node.innerHTML=node.innerHTML.replace(mean1,"").replace(mean2,"");
			}
			else{
				var m=getDefaultMean(nd)+" "+getDefaultMean(node);
				if(pIsNewLine(nd)){
					m = capitalizeFirstLetter(m);
				}
				nd.innerHTML=m;
				this.highlight(nd,"m");
				node.innerHTML=nmean;
			}
			return true;
		}
		return false;
	},
	"ä¸€ä¸€":function(node){
		if(!node.nE() || (node.nE().tagName=="BR") || !node.isspace(true)){
			node.innerHTML="ä¸€ä¸€";
		}
	},
	"_L":function(node){
		if(node.pE()){
			if(/^má»™t/i.test(node.pE().textContent)){
				var r = /^(trong |ngoÃ i |trÃªn |dÆ°á»›i )/i;
				if(r.test(node.textContent)){
					var m = r.exec(node.textContent);
					node.pE().textContent = m[1] + node.pE().textContent.toLowerCase();
					if(isUppercase(node.pE())){
						node.pE().textContent = ucFirst(node.pE().textContent);
					}
					node.textContent = node.textContent.replace(r, "");
					this.highlight(node,"m");
				}
			}
		}
	},
	tokensregex:function(node,least,alter,end){
		if(!setting.tokensregex)return;
		least=least || 2;
		end=end||"çš„";
		var cnl = node.cn.length;
		var nl = [node];

		for(var i=0;i<5;i++){
			node=node.nE();
			if(!node || !node.isspace(false) || node.cn.contain("çš„")){
				break;
			}
			nl.push(node);
			cnl+=node.cn.length;
		}
		for(;nl.length>0;){
			if(this.testcommon(nl) >= least){
				if(alter){
					alter(nl);
				}else{
					for(var i=0;i<nl.length;i++){
						nl[i].textContent=titleCase(nl[i].textContent);
					}
					this.addname(3,nl.sumChinese(""),nl.sumHan(),"titleCase");
				}
				return;
			}
			nl.pop();
		}
	},
	"åä¸º":function(node){
		if(node.nE() && node.nE().textContent.length > 0)
		if(node.nE().textContent[0].toLowerCase() == node.nE().textContent[0]){
			//this.tokensregex(node.nE(),1,function(nl){
				//console.log(nl.sumHan());
			//});
			this.tokensregex(node.nE(),1);
		}
	},
	"ä¸€ä¸ªå«":function(node){
		if(node.nE() && node.nE().textContent[0])
		if(node.nE().textContent[0].toLowerCase() == node.nE().textContent[0]){
			//this.tokensregex(node.nE(),1,function(nl){
				//console.log(nl.sumHan());
			//});
			this.tokensregex(node.nE(),1);
		}
	},
	"çš„è¯":function(node) {
		if(node.isspace(true)){
			node.tomean("lá»i nÃ³i");
		}else if(node.nextSibling && !(node.nextSibling.textContent.contain(","))){
			node.tomean("lá»i nÃ³i");
		}
	},
	"è¯":function (node) {
		if(node.pE() && node.pE().gT().lastChar()=="çš„"){
			if(node.nextSibling && node.nextSibling.textContent.contain(",")){
				node.tomean("mÃ  nÃ³i");
			}
		}else if(looper.searchphrase(node,false,10,"å¦‚æžœ")){
			node.tomean("mÃ  nÃ³i");
		}
	},
	"äºº":function (node) {
		if(node.pE()){
			if(node.pE().gT().lastChar() =="çš„"){
				if(node.pE().pE() && node.pE().pE().isname()){
					swapnode(node,node.pE().pE());
					//node.pE().pE().tomean("ngÆ°á»i cá»§a");
				}
			}
		}
	},
	"è¿˜ç»™æˆ‘":function(node) {
		if(!node.isspace(true)){
			node.tomean("tráº£ cho ta");		
		}else
		prediction.parse(node,function(n,p,l,i){
			var confident = 0;
			for(i=i+1;i<l.length;i++){
				if(l[i].tag=="uj"||l[i].tag=="n"){
					confident++;
				}
			}
			if(confident == 0){
				n.tomean("cÃ²n cho ta");
			}

		},"è¿˜ç»™");
	},
	"ä¸‹è½":function(node) {
		if(node.pE() && node.pE().gT().lastChar() == "çš„"){
			node.tomean("tung tÃ­ch");
		}
	},
	"ç„¶":function(node){
		if( !node.isspace(false) ){
			node.tomean("nhÆ°ng");
		}
	},
	"è‹¥":function(node){
		if( !node.isspace(false) ){
			node.tomean("náº¿u");
		}
	},
	"å¥ˆä½•":function(node){
		if(!node.isspace(false)){
			node.tomean("lÃ m gÃ¬");
		}
	},
	"å¾—":function(node){
		prediction.parse(node,function(n,p,d,i){
			if(p=="ud" && !d[i+1] =="v"){
				n.tomean("Ä‘Æ°á»£c");
			}
			//if(d.length > i+1 && d[i+1].indexOf("v") >= 0){
			//	n.tomean("pháº£i");
			//}
		});
	},
	"ä¸Š":function(node){
		//return;
		this.loctransform(node,"bÃªn trÃªn","trÃªn");
		return;
		if(!node.innerHTML.contain("trÃªn"))return;
		var nd=looper.searchex(node,false,4,'åœ¨ä»ŽäºŽ',true);
		if(nd){
			if(node.gT().length==1){
				nd.innerHTML+=" trÃªn";
				node.innerHTML=node.innerHTML.replace("bÃªn trÃªn","").replace("trÃªn","");
			}
			else{
				nd.innerHTML+=" "+node.innerHTML;
				node.innerHTML="";
			}
		}
	},
	"é‡Œé¢":function(node){
		this.loctransform(node,"bÃªn trong","trong");
	},
	"åœ°æ­¥":function(node){
		if(!node.isspace(true)){
			var nd=looper.search(node,false,10,'åˆ°',false);
			if(nd){
				nd.tomean(getDefaultMean(nd) +" tÃ¬nh cáº£nh");
				node.innerHTML="";
			}
		}
	},
	"å…‰":function(node){
		if(!node.isspace(false) && looper.searchex(node,true,7,'æ¥è¿‡å°±',false)){
			node.tomean("chá»‰");
		}
	},
	"-ä¸‹":function(node){
		this.loctransform(node,"phÃ­a dÆ°á»›i","dÆ°á»›i");
		return;
		if(!node.innerHTML.contain("dÆ°á»›i"))return;
		var nd=looper.searchex(node,false,4,'åœ¨ä»ŽäºŽ',true);
		if(nd){
			if(node.gT().length==1){
				nd.innerHTML+=" dÆ°á»›i";
				node.innerHTML=node.innerHTML.replace("phÃ­a dÆ°á»›i","").replace("dÆ°á»›i","");
			}
			else{
				nd.innerHTML+=" "+node.innerHTML;
				node.innerHTML="";
			}
		}
	},
	"ä½·":function(node){
		if(!node.isspace(true) && node.pE() && node.pE().gT().lastChar()=="çš„"){
			node.tomean("vÃ´ cÃ¹ng");
		}
	},
	"å¾ˆ":function(node){
		if(!node.isspace(true) && node.pE() && node.pE().gT().lastChar()=="çš„"){
			node.tomean("vÃ´ cÃ¹ng");
		}
	},
	"çš„ä½·":function(node){
		if(!node.isspace(true)){
			node.tomean("vÃ´ cÃ¹ng");
		}
	},
	"å´æ˜¯":function(node){
		if(node.isspace(false)){
			node.tomean("láº¡i lÃ ");
		}
	},
	"æ‰€è°“":function(node){
		if(!node.isspace(true)){
			node.tomean("váº¥n Ä‘á» gÃ¬");
		}
	},
	"æƒ…":function(node){
		if(node.pE() && node.isspace(false) && node.pE().gT().lastChar() == "äº‹"){
			node.tomean("");
		}
	},
	"ä¸æˆ":function(node){
		if(node.nextSibling && node.nextSibling.textContent.contain("?")){
			node.tomean("hay sao");
		}
	},
	"é‡Œè¾¹":function(node){
		this.loctransform(node,"bÃªn trong","trong");
		return;
		if(!node.innerHTML.contain("trong"))return;
		var nd=looper.searchex(node,false,4,'åœ¨ä»ŽäºŽ',true);
		if(nd){
			if(node.gT().length==1){
				nd.innerHTML+=" trong";
				node.innerHTML=node.innerHTML.replace("bÃªn trong","").replace("trong","");
			}
			else{
				nd.innerHTML+=" "+node.innerHTML;
				node.innerHTML="";
			}
		}
	},
	"è¶Š":function(node){
		if(node.nE()&&this.containnumber(node.nE())){
			node.tomean("vÆ°á»£t");
		}
	},
	"åº”ç€":function(node){
		if(!node.isspace(true)){
			node.innerHTML="Ä‘Ã¡p lá»i";
		}
	},
	"å·¦å³":function(node){
		if(node.pE()&&this.containnumber(node.pE())){
			if(node.pE() && node.pE().pE() && (node.pE().pE().isspace(true) || node.pE().innerHTML[0] ==" ")){
				node.pE().pE().tomean( getDefaultMean(node.pE().pE()) + " trÃªn dÆ°á»›i");
				node.innerHTML="";
			}else{
				if(node.pE().isspace(false)){
					node.pE().tomean("trÃªn dÆ°á»›i "+getDefaultMean(node.pE()));
					node.innerHTML="";
				}else if(node.pE().innerHTML[0]==" "){
					node.pE().tomean(" trÃªn dÆ°á»›i"+getDefaultMean(node.pE()));
					node.innerHTML="";
				}else{
					node.pE().tomean(" trÃªn dÆ°á»›i "+getDefaultMean(node.pE()));
					node.innerHTML="";
				}
			}
		}
	},
	"å·¦å³çš„":function(node){
		this["å·¦å³"](node);
	},
	"ä»¤":function(node){
		if(!node.isspace(true)){
			node.tomean("lá»‡nh");
			meanstrategy.highlight(node,"m");
		}
		if(node.pE()&&node.pE().tagName=="I"){
			if(node.pE().innerHTML.toLowerCase()==node.pE().gH()){
				node.tomean("lá»‡nh");
				meanstrategy.highlight(node,"m");
			}
		};
	},
	"ä»¤ä¸º":function(node){
		if(node.pE()&&node.pE().tagName=="I"){
			if(node.pE().innerHTML.toLowerCase()==node.pE().gH()){
				node.tomean("lá»‡nh lÃ m");
				meanstrategy.highlight(node,"m");
			}
		};
	},
	"-è®©":function(node){
		if(!node.isspace(false)||(node.nE() && node.nE().gT().length>1)){
			node.tomean("Ä‘á»ƒ cho");
		}
	},
	"åŽŸæ¥":function(node){
		if(!node.isspace(false)){
			node.tomean("thÃ¬ ra");
			if(node.pE()&&node.pE().tagName=="BR"){
				node.tomean("ThÃ¬ ra");
			}
			meanstrategy.highlight(node,"m");
		}
	},
	"èƒ½ä¸º":function(node){
		if(!node.isspace(true)){
			node.tomean("nÄƒng lá»±c");
		}
	},
	"ç­‰":function(node){
		var thi=looper.search(node,true,7,"æ—¶",true);
		if(thi!=null){
		//	node.innerHTML="chá» Ä‘áº¿n lÃºc";
		//	thi.innerHTML="";
		//	return;
		}
		if(node.pE()!=null){
			if(/exran/.test(node.pE().id)){
				if(instring(node.pE().innerHTML,this.database.level)){
					node.tomean("Ä‘áº³ng");
					return;
				}
			}else if (this.database.level.contain(node.pE().gT().lastChar())) {
				node.tomean("Ä‘áº³ng");
				return;
			}
		}
		var balance = this.countname(false,node,4) - this.countname(true,node,4);
		if(balance>0){
			node.tomean("máº¥y ngÆ°á»i");
		}else if (balance<0 || !node.near(true) || node.near(false)) {
			node.tomean("chá»");
			if(node.near(true)&&!node.near(false)){
				node.tomean("cÃ¡c loáº¡i");
			}
		}else{
			node.textContent="cÃ¡c loáº¡i";
		}
		meanstrategy.highlight(node,"m");
	},	
	"ç­‰ç­‰":function(node){
		if(!node.isspace(false)&&!node.isspace(true)){
			if(node.previousSibling && node.previousSibling.textContent.contain("...")){
				node.tomean("vÃ¢n vÃ¢n");
			}else
			node.tomean("Chá» Ä‘Ã£");
			meanstrategy.highlight(node,"m");
		}
	},
	"å½“":function(node){
		var thi=looper.search(node,true,3,"æ˜¯",true);
		if(thi && node.isspace(false)){
			node.textContent="coi";
		}
		if(!node.isspace(false) && node.isspace(true)){
			node.tomean("khi");
		//	thi=looper.search(node,true,10,"æ—¶",true);
		//	if(thi && !thi.isspace(true)){
		//		node.textContent="LÃºc";
		//		thi.textContent=thi.innerHTML.replace("lÃºc", "");
		//	}
		}
	},
	"ä¹Ÿæ˜¯":function(node){
		if(!node.isspace(false)&&!node.isspace(true)){
			node.tomean("CÅ©ng Ä‘Ãºng");
			meanstrategy.highlight(node,"m");
		}
	},
	"ä¹‹åŽ":function(node){
		var nd=looper.search(node,false,5,'å½“');
		if(nd){
			nd.tomean("sau khi");
			node.textContent="";
		}
	},
	"-æ‰‹ä¸­":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().textContent="Trong tay";
				return true;
			}
		}
	},
	"å¿ƒä¸­":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			node.pE().tomean("trong lÃ²ng");
		}
	},
	"èº«åŽ":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().textContent="Sau lÆ°ng";
			}
		}
	},
	"èº«è¾¹":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().textContent="BÃªn cáº¡nh";
			}
		}
	},
	"çš„èº«è¾¹":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().textContent="BÃªn cáº¡nh";
			}
		}
	},
	"-çœ¼ä¸­":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().innerHTML="Trong máº¯t";
			}
		}
	},
	"èº«ä¸Š":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().innerHTML="TrÃªn thÃ¢n";
			}
		}
	},
	"çš„èº«ä¸Š":function(node){
		if(node.pE()&&node.pE().isname()&&node.isspace(false)){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().innerHTML="TrÃªn thÃ¢n";
			}
		}
	},
	"ä¸‹æ–¹":function(node){
		if(node.pE()&&node.pE().isname()){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().innerHTML="PhÃ­a dÆ°á»›i";
			}
		}
	},
	"çš„æ‰‹æ®µ":function(node){
		return;
		if(node.pE()&&node.pE().isname()){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().innerHTML="Thá»§ Ä‘oáº¡n cá»§a";
			}else{
				node.pE().innerHTML="thá»§ Ä‘oáº¡n cá»§a";
			}
		}
	},
	"çš„æ ·å­":function(node){
		var nd=looper.search(node,false,2,'å‰¯',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.innerHTML="";
		}
	},
	"å€Ÿå£":function(node){
		var nd=looper.search(node,false,5,'ç€',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.innerHTML="";
		}
	},
	"æƒ¯äº†":function(node){
		var nd=looper.search(node,false,3,'æ˜¯',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.innerHTML="";
		}
	},
	"æ ·å­":function(node){
		var nd=looper.search(node,false,5,'å‰¯',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.innerHTML="";
		}
	},
	"å¯¹":function(node){
		if(node.nextSibling!=null){
			if(new RegExp(this.database.brk).test(node.nextSibling.textContent)){
				node.tomean("Ä‘Ãºng");
				meanstrategy.highlight(node,"m");
			}
		}
	},
	"è¿˜":function(node){
		if(!node.isspace(true)){
			node.innerHTML="hoÃ n";
		}
	},
	"è°ˆä½•":function(node){
		if(!node.isspace(true)){
			node.tomean("nÃ³i chi lÃ ");
			meanstrategy.highlight(node,"m");
		}
	},
	"é¢å‰":function(node){
		var nd=looper.searchex(node,false,3,'åœ¨',true);
		if(nd && !nd.innerHTML.contain("trÆ°á»›c máº·t")){
			nd.innerHTML+=" trÆ°á»›c máº·t";
			node.innerHTML="";
		}
	},
	"æ–¹é¢":function(node){
		var nd=looper.search(node,false,3,'åœ¨',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.innerHTML="";
		}
	},
	"å˜´é‡Œ":function(node){
		var nd=looper.search(node,false,6,'è‡ª',true)
			||looper.search(node,false,6,'ä»Ž',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.innerHTML="";
		}else
		if(node.pE()&&node.pE().isname()){
			swapnode(node,node.pE());
			if(pIsNewLine(node.pE())){
				node.pE().innerHTML="Trong miá»‡ng";
			}
		}
	},
	"æ€»æ˜¯":function(node){
		if(pIsNewLine(node)){
			node.innerHTML="NÃ³i chung";
		}
	},
	"é€”ä¸­":function(node){
		var nd=looper.search(node,false,6,'åœ¨',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.innerHTML="";
		}
	},
	"é¢":function(node){
		if(!node.innerHTML.contain("máº·t"))return;
		var nd=looper.search(node,false,3,'ç€')||looper.search(node,false,3,'å‰');
		if(nd){
			if(node.gT().length==1){
				nd.innerHTML+=" máº·t";
				nd.innerHTML=nd.innerHTML.replace("máº·t máº·t","máº·t");
				node.innerHTML=node.innerHTML.replace("máº·t","");
			}
			else{
				nd.innerHTML+=" "+node.innerHTML;
				node.innerHTML="";
			}
		}
	},
	"-èµ„æ ¼":function(node){
		var nd=looper.search(node,false,5,'è¿ž',true);
		if(nd){
			nd.innerHTML+=" "+node.innerHTML;
			node.tomean("");
		}
	},
	"éƒ½å¯¹":function(node){
		if(node.nextSibling!=null){
			if(!(new RegExp(this.database.brk).test(node.nextSibling.textContent))){
				node.tomean("Ä‘á»u Ä‘á»‘i");
				meanstrategy.highlight(node,"m");
			}
		}
	},
	"æ‰æ˜¯å¯¹":function(node){
		if(node.nextSibling!=null){
			if(new RegExp(this.database.brk).test(node.nextSibling.textContent)){
				node.textContent="má»›i lÃ  Ä‘á»‘i";
				meanstrategy.highlight(node,"m");
			}
		}
	},
	"ä¹Ÿå¯¹":function(node){
		if(node.nextSibling!=null){
			if(new RegExp(this.database.brk).test(node.nextSibling.textContent)){
				node.tomean("cÅ©ng Ä‘Ãºng");
				meanstrategy.highlight(node,"m");
			}
		}
	},
	"å¼€å§‹":function(node){
		while(node.nE() && node.isspace(true)){
			node = node.nE();
			if(node.textContent.contain("báº¯t Ä‘áº§u")){
				node.textContent = node.textContent.replace("báº¯t Ä‘áº§u","");
			}
		}
	},
	"èµ·æ¥":function(node){
		if(node.pE() && node.pE().gT() && node.pE().gT().lastChar()=="äº†"){
			node.textContent="";
		}else
		if(node.pE() && node.pE().innerHTML=="báº¯t Ä‘áº§u"){
			node.textContent="";
		}else
		if(node.pE() && node.pE().pE() && node.pE().pE().innerHTML=="báº¯t Ä‘áº§u"){
			node.textContent="";
		}else
		if(node.pE() && node.pE().pE() && node.pE().pE().pE() && node.pE().pE().pE().innerHTML=="báº¯t Ä‘áº§u"){
			node.textContent="";
		}else
		if(looper.searchphrase(node,false,6,"å˜å¾—",true)){
			node.textContent="";
		}
	},
	"ç»™æˆ‘":function(node){
		var nd=looper.search(node,false,4,'å€Ÿ',true)||looper.searchphrase(node,false,4,'å€Ÿç‚¹',true);
		if(nd){
			if(true){
				nd.textContent=node.innerHTML+" "+nd.innerHTML;
				node.tomean("");
				meanstrategy.highlight(nd,"m");
			}
		}
	},
	"å¯èƒ½":function(node){
		if(!node.isspace(true)){
			node.textContent="kháº£ nÄƒng";
		}
		if(false && node.pE()&&node.pE().pE()){
			if(node.pE().pE().gT().contain("æœ‰") && !node.pE().pE().innerHTML.contain("kháº£ nÄƒng")){

				node.pE().pE().innerHTML+=" kháº£ nÄƒng";
				node.tomean("");
			}else if (node.pE().pE().pE()&&node.pE().pE().pE().gT().contain("æœ‰")
				 && !node.pE().pE().pE().innerHTML.contain("kháº£ nÄƒng")) {
				node.pE().pE().pE().innerHTML+=" kháº£ nÄƒng";
				node.tomean("");
			}
		}
	},
	"å’Œ":function(node){
		if(node.pE()&&node.isspace(false)&&node.pE().gT().contain("çš„")&&node.pE().gT().length==4){
			var pch=node.pE().gT();
			if(pch.contain("å¥¹")
				||pch.contain("å…¶")
				||pch.contain("ä»–")
				||pch.contain("å®ƒ")
				||pch.contain("è‡ªå·±")
				||pch.contain("ä½ ")
				||pch.contain("æˆ‘"))
			{
				var m=/^(.*? .*?) cá»§a (.*?)$/i.exec(node.pE().innerHTML);
				if(m!=null&&node.nE()&&node.nE().gT().length==2){
					node.innerHTML=node.nE().innerHTML+" cÃ¹ng "+node.pE().innerHTML;
					node.nE().tomean("");
					node.pE().tomean("");
					meanstrategy.highlight(node,"m");
				}
			}
		}
	},
	"ä¸":function(node){
		if(node.pE()&&node.nE()&&node.isspace(true)&&node.isspace(false)){
			if(node.pE().gT()==node.nE().gT()){
				node.textContent="hay khÃ´ng";
			}
		}

	},
	"å˜å¾—":function(node){
		if(node.nE() && node.nE().textContent.contain("trá»Ÿ nÃªn")){
			node.tomean("");
		}
	},

	"å¼€":function(node){

		if(node.nE() && node.nE().gT()=="ç€" &&node.nE().nE()){
			var c=node.nE().nE();
			if(c.gT() in this.database.carbrand){
				node.tomean("lÃ¡i");
				node.nE().tomean("");
				c.tomean(this.database.carbrand[c.gT()]);
				meanstrategy.highlight(node,"m");
			}else{
				var node2=node;
				for(var i=0;i<3;i++){
					node2=node2.nE();
					if(node2==null)return;
					if(!node.isspace(false))return;
					if(instring(node2.gT(),"è½¦æœº")){
						node.tomean("lÃ¡i");
						node.nE().tomean("");
						meanstrategy.highlight(node,"m");
						return;
					}
				}
			}
		}else if(node.nE()){
			var c=node.nE();
			if(c.gT() in this.database.carbrand){
				node.tomean("lÃ¡i");
				c.tomean(this.database.carbrand[c.gT()]);
				meanstrategy.highlight(node,"m");
			}else{
				var node2=node;
				for(var i=0;i<3;i++){
					node2=node2.nE();
					if(node2==null)return;
					if(!node.isspace(false))return;
					if(instring(node2.gT(),"è½¦æœº")){
						node.tomean("lÃ¡i");
						meanstrategy.highlight(node,"m");
						return;
					}
				}
			}
		}
		//å¼€ç€
	},
	"è¿˜ç»™":function(node){
		if(node.pE()&&node.pE().containName()){
			node.tomean("tráº£ cho");
		}
	},
	"æˆ‘å°±æ˜¯":function(node){
		if(!node.isspace(true)){
			node.tomean("chÃ­nh lÃ  ta");
		}
	},
	"è¯´ç€":function(node){
		if(!node.isspace(false)){
			node.tomean("nÃ³i xong");
		}
	},
	"å¯¹ä¸èµ·":function(node){
		if(node.nextSibling!=null){
			if(new RegExp(this.database.brk).test(node.nextSibling.textContent)){
				node.tomean("tháº­t xin lá»—i");
				meanstrategy.highlight(node,"m");
			}
		}
	},
	"numberpow":function(node){
		if(node.gT().length==1){
			node.tomean("láº§n");
		}else {
			var bt=node.gT().substring(1);
			if(node.nE()){
				bt+=node.nE().gT();
				node.nE().tomean("");
			}
			tse.send("002",bt,function(){
				node.tomean("láº§n "+this.down.split("=")[1]);
			});
		}
	},
	"faction":function(node,find,replace){
		if(!setting.factionfilter)return;
		if(node.pE() && node.pE().containName()){
			return;
		}
		if(this.countname(false,node,1)){
			if(find!=""){
				node.textContent=node.innerHTML.replace(find,replace);
			}else{
				node.textContent=replace;
			}
			this.highlight(node,"f");
			meanstrategy.recognized[node.id]={
				type:"faction",
				range:[node.pE(),node]
			}
		}else if(node.pE()!=null){
			if(!node.isspace(false))return;
			if(node.pE().gT().length==1){
				node.pE().containHan(function(){
					if(find!=""){
						node.textContent=node.innerHTML.replace(find,replace);
					}else{
						node.textContent=replace;
					}
					node.pE().textContent=titleCase(node.pE().gH());

					meanstrategy.recognized[node.id]={
						type:"faction",
						range:[node.pE(),node]
					}

					if(node.pE().pE()!=null&&node.pE().pE().gT().length==1&&node.pE().isspace(false)){
						node.pE().pE().containHan(function(){
							node.pE().pE().textContent=titleCase(node.pE().pE().gH());
							meanstrategy.collected+=titleCase(node.pE().pE().gH()+" "+node.pE().gH())+" "+node.gH()+"\n";

							meanstrategy.recognized[node.id].range.unshift(node.pE().pE());

						},function(){
							meanstrategy.collected+=titleCase(node.pE().gH())+" "+node.gH()+"\n";
						});
					}else {
						meanstrategy.collected+=titleCase(node.pE().gH())+" "+node.gH()+"\n";
					}
					meanstrategy.highlight(node,"f");
				});
			}else if(node.isspace(false))
			node.pE().containHan(function(){
				if(find!=""){
					node.textContent=node.innerHTML.replace(find,replace);
				}else{
					node.textContent=replace;
				}
				node.pE().textContent=titleCase(node.pE().gH());
				meanstrategy.collected+=titleCase(node.pE().gH())+" "+node.gH()+"\n";

				meanstrategy.recognized[node.id]={
					type:"faction",
					range:[node.pE(),node]
				}

				meanstrategy.highlight(node,"f");
			});
		}
	},
	recognized:{},
	factions:"é—¨æ´¾å®—åŸŽå›½å±±å®«æ•™æ¥¼åºœé•‡é˜å¢ƒå¸‚æ‘å¯ºçœè°·å³°å´–æ®¿".split("")
		.concat(["å¤§é™†","è”ç›Ÿ","å‰‘æ´¾","å‰‘å®—"
		,"å­¦é™¢","å•†ä¼š","å¤§å­¦","å­¦å®«","åœ£åœ°","å±±åº„","æ£®æž—"
		,"ä¸€æ—","å±±è„‰","ç§˜å¢ƒ","ä¸–å®¶","å†›å›¢","å…¬ä¼š","ä¹‹åœ°","æ´žå¤©"
		,"ç¥žå®—","åœ£å®—","ä»™å®—","å¤©å®—","é­”å®—"
		,"ç¥žé—¨","åœ£é—¨","ä»™é—¨","å¤©é—¨","é­”é—¨","é›†å›¢","é¢†åŸŸ","ä¸€æ—","ä¹‹ç¥ž","é˜µè¥"
		,"å¤§å­¦","å±±è„ˆ","å±±è„‰","æ˜Ÿç³»","ä¹‹ä½“","çŽ‹å›½","å¸å›½","ç¥žå›½","ä¸»ç¥ž","ç¥žçŽ‹","çµä½“","ç•ŒåŸŸ"
		,"å³¡è°·","ä¹‹æ£®","ä¸»åŸŽ"
		]),
	people:function(node,leng){
		if(!setting.peoplefilter)return;
		if(node.pE()!=null){
			if(node.pE().getAttribute("aname")=="2"){
				this.testcommon([node.pE(),node]);
				return;
			}
			if(node.pE().gT().length==1&&this.surns.indexOf(node.pE().gT())>-1)return;
		}
		if(node.isname())return;
		if(this.testignore(node))return;
		if(node.gT()[0] == "ä¸‡" || node.gT()[0]=="æžš"){
			if(node.pE() && this.containnumber(node.pE())){
				return;
			}
		}
		var maxleng=(leng==1)?3:4;
		if(node.gT().length>leng){
			if(node.gT().length>leng+2)return;
			else {
				if(node.nE()!=null&&node.nE().gT().length==1){
					if(node.nextSibling.textContent!=" ")return;
					if(node.nE().gT().length+node.gT().length<=maxleng)
					node.nE().containHan(
						function(down){
							if(!meanstrategy.iscommsurn(node.gT().charAt(0))&&meanstrategy.testcommon([node,node.nE()])<3){

							}else if(meanstrategy.testcommon([node,node.nE()])>1&&(meanstrategy.testcommon([node,node.nE()])>=meanstrategy.testcommon([node]))
								||meanstrategy.testcommon([node,node.nE()])>3){
								node.textContent=titleCase(node.gH());
								node.nE().textContent=titleCase(node.nE().gH());
								meanstrategy.highlight(node,"o");
								node.setAttribute("aname","2");

								analyzer.update([node,node.nE()].sumChinese(),1);

							}else if(meanstrategy.iscommsurn(node.gT().charAt(0))){
								if(node.gH()==node.innerHTML.toLowerCase()){
									if(node.nE().gH()==node.nE().innerHTML.toLowerCase()){
										node.textContent=titleCase(node.gH());
										node.nE().textContent=meanstrategy.testsuffix(node.nE().gT(),titleCase(node.nE().gH()));
										meanstrategy.highlight(node,"o");
										node.setAttribute("aname","2");

										analyzer.update([node,node.nE()].sumChinese(),1);
									}
								}
							}
						}
					);
				}
				if(node.gT().length<=maxleng){
					if(this.testcommon([node])>3&&this.iscommsurn(node.gT().charAt(0))){
						node.containHan(function(down){
							if(down.split("/").length<3){
								node.textContent=meanstrategy.testsuffix(node.gT(),titleCase(node.gH()));
								meanstrategy.highlight(node,"o");

								analyzer.update(node.gT(),1);
							}
						},null,true);
					}
				}
			}
		}else 
		if(node.nE()!=null&&node.nE().gT().length==1){
			if(node.nextSibling.textContent!=" ")return;
			if(node.nE().gT().length+node.gT().length<=maxleng)
			node.nE().containHan(
				function(){
					if(!meanstrategy.iscommsurn(node.gT())&&meanstrategy.testcommon([node,node.nE()])<2){

					}else {

						var na=node.gT()+node.nE().gT();
						if(!(na in meanstrategy.addedname)){
							meanstrategy.addedname[na]=true;
							meanstrategy.addname(na,[node,node.nE()]);
						}

						node.textContent=titleCase(node.gH());
						node.nE().textContent=meanstrategy.testsuffix(node.nE().gT(),titleCase(node.nE().gH()));
						meanstrategy.highlight(node,"o");
						node.setAttribute("aname","2");

						analyzer.update([node,node.nE()].sumChinese(),1);

					}
				},
				function(){
					if(!(node.gT()+node.nE().gT() in meanstrategy.addedname)&&meanstrategy.testcommon([node,node.nE()])>3){
						var na=node.gT()+node.nE().gT();
						meanstrategy.highlight(node,"o");
						meanstrategy.addedname[na]=true;
						needbreak=true;
						namew.value="$"+na+"="+titleCase(node.gH()+" "+node.nE().gH())+"\n"+namew.value;
						saveNS();
						excute();
					}
				}
			);
			if(node.nE().nE()!=null&&node.nE().nE().gT().length==1){
				if(node.nE().nextSibling.textContent!=" ")return;
				if(this.testcommon([node,node.nE(),node.nE().nE()])>2||(this.testcommon([node,node.nE()])<=this.testcommon([node,node.nE(),node.nE().nE()])))
				if(node.nE().nE().gT().length+node.nE().gT().length+node.gT().length<=maxleng)
				node.nE().nE().containHan(
					function(){

						var na=node.gT()+node.nE().gT()+node.nE().nE().gT();
						if(!(na in meanstrategy.addedname)){
							meanstrategy.addedname[na]=true;
							meanstrategy.addname(na,[node,node.nE(),node.nE().nE()]);
						}
						node.nE().setAttribute("aname","2");
						node.nE().nE().textContent=meanstrategy.testsuffix(node.nE().nE().gT(),titleCase(node.nE().nE().gH()));

						analyzer.update([node,node.nE(),node.nE().nE()].sumChinese(),1);
					}
				);
			}
		}else if(node.nE()!=null&&node.nE().gT().length==2){
			if(node.nextSibling.textContent!=" ")return;
			if(node.nE().gT().length+node.gT().length>maxleng)return;
			node.nE().containHan(
				function(){
					if(!meanstrategy.iscommsurn(node.gT())&&meanstrategy.testcommon([node,node.nE()])<2){

					}else {
						var na=node.gT()+node.nE().gT();
						if(!(na in meanstrategy.addedname)){
							meanstrategy.addedname[na]=true;
							meanstrategy.addname(na,[node,node.nE()]);
						}
						node.textContent=titleCase(node.gH());
						node.nE().textContent=meanstrategy.testsuffix(node.nE().gT(),titleCase(node.nE().gH()));
						meanstrategy.highlight(node,"o");
						node.setAttribute("aname","2");

						analyzer.update([node,node.nE()].sumChinese(),1);
					}
				},
				function(){
					if(!(node.gT()+node.nE().gT() in meanstrategy.addedname)&&meanstrategy.testcommon([node,node.nE()])>3){
						meanstrategy.highlight(node,"o");
						var na=node.gT()+node.nE().gT();
						meanstrategy.addedname[na]=true;
						needbreak=true;
						namew.value="$"+na+"="+titleCase(node.gH()+" "+node.nE().gH())+"\n"+namew.value;
						saveNS();
						excute();
					}
				}
			);
		}
	},
	people2:function(node,leng){
	    if(!setting.peoplefilter)return;
	    var extensible= /[çš„]/;
	    var n2 = node.nE();
	    var t = node.gT();
	    if(n2){
			if(n2.isname())return;
	        var t2 = n2.gT();
	        if(t2.length == 1 && t2.match(extensible)){
	        	n2=null;
	        }else{
	        	var n3 = node.nE().nE();
		        if(n3){
		        	var t3 = n3.gT();
		        	if(t3.length == 1 && t3.match(extensible)){
		        		n3=null;
		        	}
		        }
	        }
	        
	    }
	    var n_1 = node.pE();
	    if(n_1){
	        if(n_1.getAttribute("aname")=="2"){
	            meanstrategy.testcommon([n_1,node]);
	            return;
	        }
	        //if(n_1.gT().length==1&&meanstrategy.surns.indexOf(n_1.gT())>-1)return;
	    }
	    if(node.isname())return;
	    if(meanstrategy.testignore(node))return;
	    if(t[0] == "ä¸‡" || t[0]=="æžš"){
	        if(n_1 && meanstrategy.containnumber(n_1)){
	            return;
	        }
	    }
	    var iscomm = meanstrategy.iscommsurn(t.substring(0,leng));
	    var surncomm = meanstrategy.testcommon([node]);
	    var n1han = node.containHan2(false);
	    if(n2){
	        var n2han = n2.containHan2(false);
	        var n1n2comm = meanstrategy.testcommon([node,n2]);
	    }
	    var maxleng=(leng==1)?3:4;
	    var havedchar = false;
	    if(n2 && t2.length>0 && false){
	    	
	    	if(t2.length + t.length - 1 <= maxleng){
	    		if(n3 && t3.length > 0 && t2.length + t3.length + t.length - 1 <= maxleng){
		    		if(t3.lastChar().match(extensible)||t2.lastChar().match(extensible)){
		    			maxleng++;
		    			havedchar = true;
		    		}
		    	}else{
					if(t2.lastChar().match(extensible)){
		    			maxleng++;
		    			havedchar = true;
		    		}
		    	}
	    	}
	    }
	    var result = [];
	    var setResult = function(arr){
	        if(arr.length > result.length){
	            result = arr;
	        }
	    }
	    if(t.length>leng){
	    	
	        if(t.length>leng+2){
	            if(havedchar){
	                if(t.length>leng+3){
	                    return;
	                }
	            }else return;
	        }
	        else {

	            if(n2 && n2han && t2.length + t.length<=maxleng && node.isspace(true)){
	                if(iscomm || n1n2comm > 2){
	                	if(leng==2){
	                		setResult([node,n2]);
	                	}else
	                    if(convertohanviets(t) == node.textContent.toLowerCase() &&convertohanviets(t2) == n2.textContent.toLowerCase()){
	                        setResult([node,n2]);
	                    }else{
		                    if((n1n2comm>1 && n1n2comm >= surncomm )|| n1n2comm >= 3){
		                        setResult([node,n2]);
		                    }
		                }
	                }else{
	                    if((n1n2comm>1 && n1n2comm >= surncomm )|| n1n2comm >= 3){
	                        setResult([node,n2]);
	                    }
	                }
	            }
	            if(t.length <= maxleng && surncomm > 3 && iscomm && n1han && n1han.split("/").length<3 && !node.gP().contain("v")){
	            	if(!node.gP().match(/.?v.?|ns/))
	                setResult([node]);
	            }
	        }
	    }else if(n2&&t2.length==1 && node.isspace(true) && t2.length+t.length<=maxleng){
	        if(n2han){
	        	if(!iscomm &&  n1n2comm < 2){}else setResult([node,n2]);
	        }else if(n1n2comm > 3){
	            setResult([node,n2]);
	        }
	        if(n2han && n3 && n2.isspace(true) && t3.length + t.length + t2.length <= maxleng){
	            if((this.testcommon2([node,n2,n3])>=surncomm || this.testcommon([node,n2,n3]) >= 3) && n3.containHan2(false)){
	                setResult([node,n2,n3]);
	            }
	        }
	    }else if(n2 && node.isspace(true) && t2.length + t.length<=maxleng){
	        if(n2han){
	            if(iscomm){
	                setResult([node,n2]);
	            }else if(n1n2comm>=2){
	                setResult([node,n2]);
	            }
	        }else if(n1n2comm > 3){
	            setResult([node,n2]);
	        }
	    }
	    if(result.length > 0){
	    	var ignorep = /.?v.?|.?m.?|.?t.?|.?j.?|.?p.?/
	    	if(result[result.length-1].gP().match(ignorep)){
	    		if(result[0].gP().match(ignorep) && this.testcommon2(result) < 4){
	    			return;
	    		}else if(result[result.length-1].textContent!=result[result.length-1].gH()){
	    			return;
	    		}else if(this.testcommon2(result) < 3){
    				return;
    			}
	    	}
	    	var chi = result.sumChinese("");
			console.log(chi);
	        var name = this.testsuffix(chi,titleCase(convertohanviets(chi)).replace(/^Ti /,"TÆ° ").replace("ChÆ° CÃ¡t","Gia CÃ¡t"));
	        result[0].textContent = name;
	        analyzer.update(result.sumChinese(),1);
	        var combinedcomm = this.testcommon2(result);

	        if(combinedcomm > this.testcommon(result)){
	            if(result.length==2){
	                var needbreak = this.maincontent.qq('[t="'+result[0].cn+'"]+[t^="'+result[1].cn+'"]');
	            }
	            if(result.length==3){
	                var needbreak = this.maincontent.qq('[t="'+result[0].cn+'"]+[t="'+result[1].cn+'"]+[t^="'+result[2].cn+'"]');
	            }
	            for(var i=0;i<needbreak.length;i++){
	                var nodes = [needbreak[i]];
	                while(nodes.length < result.length){
	                    nodes.unshift(nodes[0].pE());
	                }
	                var r = nodes.sumChinese("").substring(chi.length);
	                mergeWord(nodes);
	                if(r.length>0){
	                	(function(){
		                	var ndw = insertWordWaitAsync(nodes[0],r);
		                	tse.send("007",r,function(){
								var meancomb=this.down.split("|")[0].split("=");
								var m1 = getMeanFrom(meancomb);
								console.log(m1);
								ndw.textContent=m1;
								ndw.setAttribute("v")=m1;
							});	
		                })();
	                }
	                
	                nodes[0].textContent = name;
	                nodes[0].cn=chi;
	                nodes[0].setAttribute("t",chi);
	                nodes[0].setAttribute("v",name+"/"+nodes[0].gH());
	                console.log(name);
	                this.highlight(nodes[0],"o");
	            }
	        }else{
	            mergeWord(result);
	            result[0].setAttribute("v",name+"/"+result[0].gH());
	            this.highlight(result[0],"o");
	        }
	        //console.log(result);
	    }
	},
	commsurn:155,
	iscommsurn:function(chi){
		return this.surns.indexOf(chi)<=this.commsurn;
	},
	surns:"è¡€çŽ‹æŽå¼µå¼ åŠ‰åˆ˜é™³é™ˆæ¥Šæ¨é»ƒé»„è¶™èµµå³å´å‘¨å¾å­«å­™é¦¬é©¬æœ±èƒ¡éƒ­ä½•æž—ç¾…ç½—é„­éƒ‘æ¢è¬è°¢å®‹å”è¨±è®¸éŸ“éŸ©é¦®å†¯é„§é‚“æ›¹å½­è•­è§ç”°è‘£è¢æ½˜è”£è’‹è”¡æ¥šä½™æœè‘‰å¶ç¨‹è˜‡è‹é­å‘‚å•ä¸ä»»æ²ˆå§šç›§å¢å§œå´”é¾é’Ÿè­šè°­é™¸é™†æ±ªèŒƒçŸ³å»–è³ˆè´¾å¤éŸ‹éŸ¦å‚…æ–¹é„’é‚¹å­Ÿç†Šç§¦é‚±æ±Ÿå°¹è–›é–»é˜Žæ®µé›·ä¾¯é¾é¾™å²é™¶é»Žè³€è´ºé¡§é¡¾æ¯›éƒé¾”é¾šé‚µè¬éŒ¢åš´ä¸¥è¦ƒæ­¦æˆ´èŽ«å­”æ¹¯æ±¤åº·æ˜“å–¬ä¹”è³´èµ–æ–‡é£Žæ–½æ´ªè¾›æŸ¯èŽŠåº„äº‘å‡Œå¤å¤œå®ç‘œé­‚å¢¨é±¼æ¸©"
		+"ç„±å¯’ä¸ä¸‡ä¸˜ä¸›ä¸œä¸¥ä¸°ä¸´ä¸¹ä¹‰ä¹Œä¹ä¹”ä¹™ä¹œä¹ äºŽäº‘äº“äº•äº¢äº¦äº¬ä»‡ä»‰ä»‹ä»˜çµä»ä»£ä»ªä»°ä»²ä»»ä¼Šä¼ä¼ä¼¯ä½•ä½˜ä½™ä½Ÿä½´ä¾ä¾¯ä¿ä¿žä¿±å€ªå‚…å‚¨å„€å„²å…ƒå……å…†å…šå…¬å…°å…³å…´å†€å†‰å†’å†œå† å†¬å†¯å†µå†·å‡Œå‡¤å‡¯å‡°å‡±åˆåˆ‘åˆ—åˆ˜åˆ¥åˆ©åˆ«å‰›åŠ‰åŠ³å‹žå‹Ÿå‹¾åŒ…åŒ¡åŒºå€åƒåŽå“å•åœåžå å¢å«å°å±å¿åŽ†åŽ‰åŽåŽšåŽŸåŽ²åŒå¢å¤å¬å°å²å¶å¸å‰å‘å•å¯å³å´å¾å‘‚å‘˜å‘¼å’¸å“å“ˆå“¡å”å•†å•“å–„å–¬å–®å–»å˜‰åš´å›ºå›½åœ†åœ‹åœ“åšåž£å …å ¯å µå¡—å¢žå¢¨å£«å£¶å£ºå£½å¤å¤”å¤§å¤ªå¥‡å¥‰å¥Žå¥•å¥šå§šå§œå§¬å¨„å¨‡å©å¬Œå¬´å­å­”å­™å­Ÿå­£å­«å®å®‡å®‰å®‹å®Œå®å®“å®—å®˜å®šå®›å®œå®£å®¦å®«å®®å®°å®¹å®¾å®¿å¯†å¯‡å¯Œå¯§å¯»å¯¿å°å°‰å°‹å°šå°¤å°§å°¹å±…å±ˆå±•å± å±±å²å²‘å²šå²©å²³å´‡å´”åµ‡å¶½å·¢å·¦å·©å·«å·´å¸ƒå¸…å¸ˆå¸¥å¸«å¸­å¸¸å¹²å¹³å¹´å¹¸å¹¹å¹½å¹¿åº„åº†åºåº”åºžåº·åº¾å»‰å»–å»£å»¬å»¶å¼“å¼˜å¼ å¼µå¼·å¼ºå½ªå½­å½°å¾Œå¾å¾žå¾·å¿—å¿µå¿»æ€€æ€æ’æ©æ‚…æ‚¦æƒ æ„›æ„¼æ…ˆæ…•æ…§æ…¶æ‡‰æ‡·æˆˆæˆŽæˆæˆ˜æˆšæˆ°æˆ´æˆ¶æˆ·æˆ¿æ‰€æ‰ˆæ‰¬æ‰¶æ‰¿æŠ˜æ‹“æšæ“æ”¯æ”¹æ”¿æ•–æ–‡æ–¯æ–°æ–¹æ–¼æ–½æ—­æ—·æ˜Œæ˜Žæ˜“æ˜™æ˜æ˜Ÿæ™æ™‰æ™‹æ™æ™¯æ™ºæ›æ›†æ› æ›²æ›¹æ›¾æœ±æƒæŽæœæŸæ¨æ­æ±æ¾æž—æžšæŸæŸ”æŸ¥æŸ¯æŸ³æŸ´æ ¾æ¡‚æ¡‘æ¡“æ¢æ¢…æ¥Šæ¥šæ¥¼æ¦†æ¦®æ¨‚æ¨Šæ¨“æª€æ¬Šæ¬’æ¬§æ¬½æ­æ­¥æ­¦æ®³æ®´æ®µæ®·æ¯†æ¯‹æ¯•æ¯›æ°´æ±æ±Ÿæ± æ±¤æ±ªæ±²æ²ƒæ²ˆæ²‰æ²æ²™æ²§æ³æ³•æ³°æ´›æ´ªå€šæµ™æµ¦æ¶‚æ¶¢æ·©æ·µæ¸Šæ¸¸æ¹›æ¹¯æºæº«æ»„æ»‘æ»•æ»¿æ¼†æ½˜æ½¼æ¾¹æ¿®çƒç„¦ç†Šç‡•çˆ±ç‰›ç‰Ÿç‰§ç‹„ç‹ç’çŽ‰çŽ‹ç­çªç³ç´ç’©ç”„ç”˜ç”¯ç”°ç”±ç”³ç•™ç•¢ç™½ç™¾çš‡ç›Šç›–ç››ç›§ç›¸ç£çž¿çŸ³ç¥ç¥ˆç¥–ç¥ç¥¥ç¥¿ç¦„ç¦ç¦šç¦¹ç¦»ç§‹ç§ç§¦ç¨‹ç¨®ç¨½ç©†ç©Œç©ºçª¦ç«‡ç« ç«¥ç«¯ç«¹ç«ºç¬¦ç¬ªç­‘ç­±ç®€ç®¡ç®«ç¯€ç¯„ç¯‰ç°¡ç±ç²˜ç²Ÿç²¤ç²µç³œç´€ç´…ç´¢ç´«çµ‚ç¶“ç·±ç¹†çº¢çºªç»ˆç»ç¼ªç½—ç¾…ç¾Šç¾Œç¾©ç¾¿ç¿ç¿’ç¿Ÿç¿°è€¿è‚èžè¶è‚–èƒ¡èƒ¥è…¾è‡§è‡¨èˆˆèˆ’è‰¾èŠ‚èŠ¦èŠ®èŠ±èŠ³è‹è‹è‹‘è‹—è‹»èŒƒèŒ…èŒ¹è€è†èŠè£èŽŠèŽ˜èŽ«è¯è§è¨è¬è‘‰è‘›è‘£è’‹è’™è’¯è’²è’¼è“‹è“è“Ÿè“¬è””è”šè”¡è”£è”ºè•­è•²è–„è–Šè–©è—‰è—è—¤è—ºè—¿è˜†è˜‡è˜­è™žèžè¡›è¡¡è¡£è¢è£˜è£´è¤šè¥„è¦ƒè§€è§‚è§£è¨€è¨ˆè¨±è¨¾è©¹è«‡è«¸è¬è­šè®¡è®¸è¯¸è°ˆè°¢è°­è°¯è°·è±è²è²¢è²«è²´è²»è³€è³è³ˆè³“è³žè³´è´è´¡è´¯è´²è´µè´¹è´ºè´¾èµèµ–èµ«èµµè¶Šè¶™è·¯è»Šè»’è½¦è½©è¾›è¾œè¾²è¾¹è¿œè¿žé€„é€é€šé€£é€¯éŠé”é é‚Šé‚“é‚›é‚¢é‚¬é‚¯é‚°é‚±é‚´é‚µé‚¸é‚¹éƒéƒŽéƒéƒ‘éƒ—éƒœéƒéƒžéƒ¤éƒ¦éƒ¨éƒ­é„‚é„’é„”é„¢é„§é„­é…†é…ˆé‡‘éˆ„éˆŽéˆ•éŠ€éŒ¢éŒ«é¾é˜éµé’Ÿé’¦é’©é’®é’±é“é“¶é”¡é”ºé–†é–”é–»é—•é—œé—«é—µé—»é˜Žé˜™é˜šé˜®é˜³é˜´é™ˆé™°é™³é™¶é™¸é™½éš†éš‹éš—é›†é›é›™é›¢é›ªé›²é›¶é›·éœé’é–é™éœé³éžéž éŸ‹éŸ“éŸ¦éŸ©éŸ¶é …é ˆé¡é¡”é¡§é¡¹é¡»é¡¾é¢œé¢¨é£Žé¤Šé¥’é¦¬é¦®é§±é¨°é©¬éª†é«˜é¬±é­é­šé­¯é®‘é±¼é²é²é³³é´»é¸¿é¹¹é¹¿éº’éº¥éº¦éº´éº»é»ƒé»„é»Žé»‘é»˜é»¨é½Šé½é¾é¾é¾”é¾™é¾šæµ·æµå›å¡”æ—¬å‰‘éª…éœèŠ’é­”å—çŽ„å†°æœ¨æ°´ç«åœŸæž­",
	surns2:"ç™¾é‡Œæ·³äºŽç¬¬äº”æ±æ–¹ä¸œæ–¹æ±é–£ä¸œé˜æ±éƒ­ä¸œéƒ­æ±é–€ä¸œé—¨ç«¯æœ¨ç¨å­¤ç‹¬å­¤çˆ¾æœ±å°”æœ±"+
		"å…¬å­«å…¬å­™å…¬ç¾Šå…¬å†¶å­£å†¶å…¬è¥¿æ¯Œä¸˜ç©€æ¢è°·æ¢è³€è˜­è´ºå…°èµ«é€£èµ«è¿žè³€è‹¥è´ºè‹¥çš‡ç”«"+
		"é»„æ–¯å‘¼å»¶å…°å‘ä»¤ç‹é™†è²»é™†è´¹ç”ªé‡Œé–­ä¸˜é—¾ä¸˜ä¸‡ä¿Ÿæ…•å®¹ç´è˜­çº³å…°å—å®®å—å®«æ­é™½"+
		"æ¬§é˜³æ²™å’ä¸Šå®˜ç”³å± å¸é¦¬å¸é©¬å¸å¾’å¸ç©ºå¸å¯‡å¤ªå²æ¾¹è‡ºæ¾¹å°æ‹“è·‹å®Œé¡å®Œé¢œèžäºº"+
		"é—»äººå·«é¦¬å·«é©¬å¤ä¾¯é®®äºŽé²œäºŽè¥¿é–€è¥¿é—¨è»’è½…è½©è¾•æ¥Šå­æ¨å­è€¶å¾‹æ¨‚æ­£ä¹æ­£å°‰é²"+
		"å°‰è¿Ÿå®‡æ–‡é•·å­«é•¿å­™é¾é›¢é’Ÿç¦»è«¸è‘›è¯¸è‘›ç¥èžå­è»Šå­è½¦å·¦äºº",
	skill:function(node,lastchar){
		if(!setting.skillfilter)return;
		if(this.skillignore.indexOf(node.gT())>-1)return;
		var maxleng=5;
		if(node.cn && node.cn.lastChar()=="çš„"){
			maxleng++;
		}
		var cumulated=node.gT().length;
		var acceptrange=2;
		if(node.gT().length<2){
			acceptrange=3;
		}
		node.containHan(function(down0){
			if(node.pE()!=null){//layer 1
				if(!node.isspace(false))return;
				if(cumulated+node.pE().gT().length <= maxleng){
					node.pE().containHan(function(down1){
						//if(meanstrategy.testcommon([node.pE(),node])<3)return;
						if(down1.split("/").length>acceptrange
							&&down1.indexOf(node.pE().gH())!=0
							&&down1.split(node.pE().gH()).length<3)return;
						cumulated+=node.pE().gT().length;
						node.pE().textContent=meanstrategy.skillcasing(node.pE().gH());
						node.textContent=meanstrategy.skillcasing(node.gH());
						meanstrategy.highlight(node,"s");
						if(node.pE().pE()!=null
						 &&node.pE().isspace(false)
						 &&cumulated+node.pE().pE().gT().length <= maxleng)
						 {//layer 2
							node.pE().pE().containHan(function(down2){
								//if(meanstrategy.testcommon([node.pE(),node.pE(),node])<3)return;
								if(down2.split("/").length>acceptrange
									&&down2.indexOf(node.pE().pE().gH())!=0
									&&down2.split(node.pE().pE().gH()).length<3)return;
								cumulated+=node.pE().pE().gT().length;
								node.pE().pE().textContent=meanstrategy.skillcasing(node.pE().pE().gH());
								if(node.pE().pE().pE()!=null){//layer 3
									if(!node.pE().pE().isspace(false))return;
									if(cumulated+node.pE().pE().pE().gT().length <= maxleng){
										//if(meanstrategy.testcommon([node.pE().pE().pE(),node.pE().pE(),node.pE(),node])<3)return;
										node.pE().pE().pE().containHan(function(down3){
											if(down3.split("/").length>acceptrange
												&&down3.indexOf(node.pE().pE().pE().gH())!=0
												&&down3.split(node.pE().pE().pE().gH()).length<3)return;
											node.pE().pE().pE().textContent=meanstrategy.skillcasing(node.pE().pE().pE().gH());
										},null,true);
									}
								}
							},function(){
								if(node.gT().length+node.pE().gT().length<3){
									node.textContent=node.gH();
									node.pE().textContent=node.pE().gH();
								}
							},true);
						}else {
							if(node.gT().length+node.pE().gT().length<3){
								node.textContent=node.gH();
								node.pE().textContent=node.pE().gH();
							}
						}
					},null,true);
				}
			}
		},null,false);
	},
	skill2:function(node,lastchar){
		if(!setting.skillfilter)return;
		if(this.skillignore.indexOf(node.gT())>-1)return;
		var maxleng=5;
		if(node.cn.lastChar()=="çš„"){
			maxleng++;
		}
		var cumulated=node.gT().length;
		var acceptrange=2;
		if(node.gT().length<2){
			acceptrange=3;
		}
		var ishan = node.containHan2(false);
		if(ishan){
			var p1 = node.pE();
			if(p1 && node.isspace(false) && cumulated+p1.gT().length <= maxleng){
				var down1 = p1.containHan2(true);
				if(down1){
					if(down1.split("/").length>acceptrange && down1.indexOf(p1.gH()) != 0 &&down1.split(p1.gH()).length < 3)return;
					cumulated+=p1.gT().length;
					p1.textContent=meanstrategy.skillcasing(p1.gH());
					node.textContent=meanstrategy.skillcasing(node.gH());
					meanstrategy.highlight(node,"s");
					var p2 = p1.pE();
					if(p1.isspace(false) && p2 && cumulated+p2.gT().length <= maxleng){
						var down2 = p2.containHan2(true);
						if(down2 && down2.split("/").length <= acceptrange && down2.indexOf(p2.gH())==0&&down2.split(p2.gH()).length>=3){
							cumulated+=p2.gT().length;
							p2.textContent=meanstrategy.skillcasing(p2.gH());
							var p3 = p2.pE();
							if(p2.isspace(false) && p3 && cumulated+p2.gT().length <= maxleng){
								var down3 = p3.containHan2(true);
								if(down3 && down3.split("/").length<=acceptrange&&down3.indexOf(p3.gH())==0&&down3.split(p3.gH()).length>=3){
									p3.textContent=meanstrategy.skillcasing(p3.gH());
								}
							}
						}else{
							if(node.gT().length+p1.gT().length<3){
								node.textContent=node.gH();
								p1.textContent=p1.gH();
							}
						}
					}else{
						if(node.gT().length+p1.gT().length<3){
							node.textContent=node.gH();
							p1.textContent=p1.gH();
						}
					}
				}
			}
		}
	},
	skills:"è¡«ç½©åŠŸç»è¯€å…¸æ³•å‰‘æ‹³æŽŒåˆ€è¸¢è„šæŒ‡æ­¥æ–©å†³å°å¼ä¸¹é˜µ".split("").concat("é­”åŠŸé“ç»é‡‘èº«ç¥žåŠŸç»çš„".splitn(2)),
	skillignore:"åŠŸæ³•èº«æ³•æ— æ³•æ–¹å¼æ¬¾å¼".splitn(2),
	skillcasing:function(translated){
		if(!!setting.skilluppercase){
			return titleCase(translated);
		}else return translated;
	},
	isitem:function(lc){
		if(this.items_a.indexOf(lc)<0
			&&this.items_s.indexOf(lc)<0
			&&this.items_sp.indexOf(lc)<0
			&&this.items_t.indexOf(lc)<0
			&&this.items_p.indexOf(lc)<0){
			return true;
		}
		return false;
	},
	item:function(node,lastchar){
	    if(!setting.enablesuffix)return;
	    if(this.itemignore.indexOf(node.gT())>-1)return;
	    if(!node.containHan2())return;
	    var nodes=[node];
	    var t=node.gT();
	    var pignore = /m|j|v|s|f|^n?t/;
	    if(node.gP().match(pignore)){
	        return;
	    }
	    if(this.isitem(lastchar) && node.textContent.toLowerCase()!=node.gH()){
	    	return;
	    }
	    while(t.length < 5) {
	        if(node.isspace(false) && nodes[0].pE() && nodes[0].pE().tagName=="I"){
	            var tmpt = nodes[0].pE().gT();
	            for(var wt in meanengine.db.tokenfind){
	                if(meanengine.db.tokenfind[wt].indexOf(tmpt)>-1){
	                    break;
	                }
	            }
	            if(t.length+tmpt.length > 5 || pignore.exec(nodes[0].pE().gP())){
	            	break;
	            }
	            nodes.unshift(nodes[0].pE());
	            t=tmpt + t;
	        }else{
	            break;
	        }
	    }
	    if(t.length < 3){
	        return;
	    }
	    var acceptrange=2;
	    if(node.gT().length<2){
	        acceptrange=3;
	    }
	    function testMean(n){
	        var m = n.mean();
	        if(!m)return false;
	        var f = m.split("/").length > acceptrange && m.split(n.gH()).length < 3;
	        if(f && !ichar3.allIsPopular(n.cn.split(""))){
	            return false;
	        }
	        if(f && meanstrategy.testcommon(nodes) < 3 && m.indexOf(node.gH())!=0){
	            return false;
	        }
	        return true;
	    }
	    for(var i=nodes.length-2;i>=0;i--){
	        var ishan = nodes[i].containHan2();
	        if(!ishan || !testMean(nodes[i])){
	            for(var j=0;j<=i;j++){
	                nodes.shift();
	            }
	            t = nodes.sumChinese("");
	            if(t.length < 3){
	                return;
	            }
	        }
	    }
	    if(nodes.length == 1){
	    	return;
	    }
	    mergeWord(nodes);
	    var name = convertohanviets(t);
	    if(this.isitem(lastchar)){

	    }else
	    if(tokenizeName(t).push){
    		if(this.items_p.indexOf(lastchar)>=0){
    			name = lowerNLastWord(titleCase(name),1);
	    	}else if(this.items_t.indexOf(lastchar)>=0){
	    		name = titleCase(name);
	    	}else if(this.items_a.indexOf(lastchar)>=0){
	    		name = titleCase(name);
	    	}else if(this.items_s.indexOf(lastchar)>=0){
	    		name = this.skillcasing(name);
	    	}else if(this.surns.indexOf(t[0])>=0){
	    		name = titleCase(name);
	    	}else{
	    		name = titleCase(name);
	    	}
    	}
    	nodes[0].textContent = name;
    	meanstrategy.highlight(nodes[0],"i");
	    if(isUppercase(nodes[0])){
	    	nodes[0].textContent = ucFirst(nodes[0].textContent);
	    }
	    nodes[0].setAttribute("v",nodes[0].textContent);
	},
	items:"è¡«ç½©åŠŸç»è¯€å…¸æ³•å‰‘æ‹³æŽŒåˆ€è¸¢è„šæŒ‡æ­¥æ–©å†³å°å¼ä¸¹é˜µè›Šå±±é´é¾™é­”é©¬é¬¼è™Žè›‡ç‹¼å…½é¹°ç‰›ç†Šç‹®é¹¤é±¼å‡°è›Ÿé¹è±¡é¹¿èŸ’èŽç¾ŠéºŸçŒ¿è¶é¾Ÿè™«é²¨é¸Ÿè››å¤­çŒªçŒ´ç‹—é¸¡èœ‚é¼ é²¸é²²ç¦½èš•é¾é¹žé³„æž—å¤©æ˜Ÿæµ·å‡Œæ±Ÿå®«é—¨å®—é•‡å²³æ²³è°·åº„åŸŽæ¸Šæœç•Œé”‹æ³‰æ± é™µç‹±åŸŸåº­æ¥¼ä¸˜é¢†æ¶¯ç å±…å°è‘¬æºªå¸®å¸å·žåŒºé˜å´–éƒ¡å²­å²›å‰‘çŽ‰é‡‘å¶æ–‡æ°´è¡€ç«èŠ±å†°å¿ƒé“çŸ³æœ¨åŽä¸¹åˆ€èŽ²é’Ÿç‚Žæ¯’æ²™ä¹¦è¯çƒŸç«¹å›¾ç¬¦ä»¤é›¾ç”²è§’å²©æ™®ç´é˜µæ ‘æ•£è‰è¡£æžªè—¤ä½©é…’å°é†‰é¡»æ ¹æžœçš®åˆƒé«“ç®€é•œæ±‚èœœç›¾å·æ˜†æ³¥é“ƒé¡¶èŒ¶è‚‰å£åŠªç®­å°ºæ±¤å‰‘æ³•åˆ€æ³¢éœ‡èˆžæ­¥ç»åŠŸæŽŒæžªæ‰‹é—ªå°çˆªæµªæˆˆåˆƒåˆºåŠ²æŒ‡ç›¾æ˜†æ¢å å˜ç®­å°ºé£Žäº‘é›·æ°´ç«é­‚ä¸–å«åŠ«é­„çŽ‹ä»™åœ£å¸ä½›ä¾¯ç¥–ä¸»".split(""),
	itemignore:"",
	items_p:"æž—å¤©æ˜Ÿæµ·å‡Œæ±Ÿå®«é—¨å®—é•‡å²³æ²³è°·åº„åŸŽæ¸Šæœç•Œé”‹æ³‰æ± é™µç‹±åŸŸåº­æ¥¼ä¸˜é¢†æ¶¯ç å±…å°è‘¬æºªå¸®å¸å·žå±±",
	items_s:"å‰‘æ³•åˆ€æ³¢éœ‡èˆžæ­¥ç»åŠŸæŽŒæžªæ‰‹é—ªå°çˆªæµªæˆˆåˆƒåˆºåŠ²æŒ‡ç›¾æ˜†æ¢å å˜ç®­å°ºè¡«ç½©åŠŸç»è¯€å…¸æ³•å‰‘æ‹³æŽŒåˆ€è¸¢è„šæŒ‡æ­¥æ–©å†³å°å¼ä¸¹é˜µ",
	items_t:"çŽ‹ä»™åœ£å¸ä½›ä¾¯ç¥–ä¸»",
	items_sp:"é£Žäº‘é›·æ°´ç«é­‚ä¸–å«åŠ«é­„",
	items_a:"è›Šé¾™é­”é©¬é¬¼è™Žè›‡ç‹¼å…½é¹°ç‰›ç†Šç‹®é¹¤é±¼å‡°è›Ÿé¹è±¡é¹¿èŸ’èŽç¾ŠéºŸçŒ¿è¶é¾Ÿè™«é²¨é¸Ÿè››å¤­çŒªçŒ´ç‹—é¸¡èœ‚é¼ é²¸é²²ç¦½èš•é¾é¹žé³„",
	entity:function(node,lastchar){
		if(!setting.entityfilter)return;
		if(this.entityignore.indexOf(node.gT())>-1)return;
		var maxleng=5;
		var cumulated=node.gT().length;
		var acceptrange=2;
		if(node.gT().length<2){
			acceptrange=3;
		}
		node.containHan(function(down0){
			if(node.pE()!=null){//layer 1
				if(!node.isspace(false))return;
				if(cumulated+node.pE().gT().length <= maxleng){
					node.pE().containHan(function(down1){
						//if(meanstrategy.testcommon([node.pE(),node])<3)return;
						if(down1.split("/").length>acceptrange
							&&down1.indexOf(node.pE().gH())!=0
							&&down1.split(node.pE().gH()).length<3)return;
						cumulated+=node.pE().gT().length;
						node.pE().textContent=meanstrategy.skillcasing(node.pE().gH());
						node.textContent=meanstrategy.skillcasing(node.gH());
						meanstrategy.highlight(node,"s");
						if(node.pE().pE()!=null
						 &&node.pE().isspace(false)
						 &&cumulated+node.pE().pE().gT().length <= maxleng)
						 {//layer 2
							node.pE().pE().containHan(function(down2){
								//if(meanstrategy.testcommon([node.pE(),node.pE(),node])<3)return;
								if(down2.split("/").length>acceptrange
									&&down2.indexOf(node.pE().pE().gH())!=0
									&&down2.split(node.pE().pE().gH()).length<3)return;
								cumulated+=node.pE().pE().gT().length;
								node.pE().pE().textContent=meanstrategy.skillcasing(node.pE().pE().gH());
								if(node.pE().pE().pE()!=null){//layer 3
									if(!node.pE().pE().isspace(false))return;
									if(cumulated+node.pE().pE().pE().gT().length <= maxleng){
										//if(meanstrategy.testcommon([node.pE().pE().pE(),node.pE().pE(),node.pE(),node])<3)return;
										node.pE().pE().pE().containHan(function(down3){
											if(down3.split("/").length>acceptrange
												&&down3.indexOf(node.pE().pE().pE().gH())!=0
												&&down3.split(node.pE().pE().pE().gH()).length<3)return;
											node.pE().pE().pE().textContent=meanstrategy.skillcasing(node.pE().pE().pE().gH());
										},null,true);
									}
								}
							},function(){
								if(node.gT().length+node.pE().gT().length<3){
									node.textContent=node.gH();
									node.pE().textContent=node.pE().gH();
								}
							},true);
						}else {
							if(node.gT().length+node.pE().gT().length<3){
								node.textContent=node.gH();
								node.pE().textContent=node.pE().gH();
							}
						}
					},null,true);
				}
			}
		},null,false);
	},
	entities:"",
	entityignore:"",
	ignore:"å¸éƒ½äºŽä¸ŽåŠ¡ä½åº§æˆ‘é—¨æ´¾ä¹ƒä»–å¥¹å®ƒå„ç”¨æ‰¾è¿™æ˜¯ä¸ªå§çš„æŽ¥å¼ƒåå…¥ç£‹å˜›å¹´è¿›é‚£å‡ å™¨å•Šè¿™åå’Œè‡ªè´§å°±çº§ç»™å›žé˜µé‡Œåˆ°å—Žå—å‡ºåŽè¢«åˆå„¿å¯ä»¥å§ç­‰å‘¢ä»Žå¼Ÿå‘å’ŒåŠ ä½“ç¦»åœ¨å°†æ‰€æœ‰é¢ç«ŸæŒºå¯¹é€‰ä¸­æ‚¨è¿žä»æŠ€æ€§æ—ä¹Ÿä»¬ä¸ºæ–½å†…æˆäº›é‡Žä¸ºç‚¼éƒŠè¦ç„¶é”™å½“",
	connectignore:"å’Œå°†åˆšéƒ½ç„¶",
	ignore2:"äºŽåŠ ä½“ç¦»åœ¨å¹´å°†é€‰è®ºç„¶é‡Žç‚¼éƒŠç„¶å‡ çš„",
	havemean:"ä¿®ç‚¼".splitn(2),
	testignore:function(node){
		if(instring(node.gT(),meanstrategy.ignore)){
			if(!instring(node.gT(),meanstrategy.ignore2)||(node.pE()&&meanstrategy.testcommon([node.pE(),node])<2)){
				return true;
			}
		}
		return false;
	},
	testignorechi:function(chi){
		if(instring(chi,meanstrategy.ignore)){
			return true;
		}
		return false;
	},
	//addname:function(chi,tra){
		//namew.value="$"+chi+"="+this.testsuffix(tra.sumChinese(""),titleCase(tra.sumHan()))+"\n"+namew.value;
		//this.collected+="\n"+this.testsuffix(tra.sumChinese(""),titleCase(tra.sumHan()));
	//},
	suffix:"é“å®¶æ¦œæŸè€å“¥å…„å€™ä¼¯çˆ¶æ¯å”æ°æ€»è‘£å¯¼å±€é˜Ÿå°‘".split("").concat("å››çˆ·å®¶ä¸»å¤§å¸ˆé“å‹å‰è¾ˆå¸ˆå¦¹ç§˜ä¹¦å¤§å¤«è­¦å®˜å°å­ç¼–å‰§ä¹¦è®°å¤§ç¥žæ ¡èŠ±å¾‹å¸ˆå‘˜å¤–ä¸Šæ ¡çœŸäººæ•™å®˜ä»™å­ä»™å¥³å©†å©†å¤«äººå¸®ä¸»äºŒå¨˜äºŒçˆ·å¤§ä¾ ç›Ÿä¸»ä¾›å¥‰çŸ®å­å¥³å£«é˜¿å§¨æ—…é•¿ç¥žåŒ»å”å”å¸ä»¤ä¸»å¸­ä¼¯ä¼¯åŒå­¦åº„ä¸»å“¥å“¥é•–å¤´å°‘ä¾ å¤§å“¥å¥³ä¾ å¯¼å¸ˆåœ£å¥³è€æ¿è€å¸ˆé•¿è€å§‘å¨˜å°‘çˆ·å°†å†›æŠ¤å«æ•™ä¹ æ•™å¤´å…¬å­é«˜æ‰‹å¤§å¸ˆå¤§äººå®¶äººè€å¤§è€äºŒè€ä¸‰è€å››è€äº”è€å…­è€ä¸ƒè€å…«è€ä¹è€åå…ˆç”ŸæŽŒé—¨æ­¦è€…å®¿ä¸»å•†åŸŽå¸ˆå…„ä¾„å¥³å®—é—¨ç®¡äº‹".splitn(2)),
	testsuffix:function(text,translated){
		for(var i=0;i<text.length;i++){
			if(this.suffix.indexOf(text.substring(i))>-1){
				return lowerNLastWord(translated,text.length-i);
			}
		}
		return translated;
	},
	testcommon:function(nodecomb){
		var len=nodecomb.length;
		var comb=nodecomb.sumChinese();
		nodecomb = nodecomb.map(function(n){
			if(!n.cn){return "";}
			return n.cn.replace(/"/g,"");
		});
		
		if(comb in this.commondata){
			return this.commondata[comb];
		}
		var count = 0;
		if(len==1){
			count = this.maincontent.qq('[t="'+nodecomb[0].cn+'"]').length;
		}
		if(len==2){
			count = this.maincontent.qq('[t="'+nodecomb[0].cn+'"]+[t="'+nodecomb[1].cn+'"]').length;
		}
		if(len==3){
			count = this.maincontent.qq('[t="'+nodecomb[0].cn+'"]+[t="'+nodecomb[1].cn+'"]+[t="'+nodecomb[2].cn+'"]').length;
		}

		this.commondata[comb]=count;
		return count;
	},
	testcommon2:function(nodecomb){
	    var len=nodecomb.length;
	    var count = 0;
	    if(len==2){
	        count = this.maincontent.qq('[t="'+nodecomb[0].cn+'"]+[t^="'+nodecomb[1].cn+'"]').length;
	    }
	    if(len==3){
	        count = this.maincontent.qq('[t="'+nodecomb[0].cn+'"]+[t="'+nodecomb[1].cn+'"]+[t^="'+nodecomb[2].cn+'"]').length;
	    }
	    return count;
	},
	prepositionmover:function(node){
		var cn=node.gT();
		if(node.getAttribute("moved")=="true")return;
		if(this.database.phasemarginr.c(cn.substring(cn.length-2))
			||this.database.phasemarginr.c(cn.substring(cn.length-1))){
			if(instring(cn,meanstrategy.ignore))return;
			if(!node.isspace(false))return;
			var nd=looper.searchex(node,false,3,this.database.phasemarginul,true);
			if(nd){
				nd.innerHTML+=" "+node.innerHTML;
				node.innerHTML="";
				this.highlight(nd,"m");
				node.setAttribute("moved","true");
				return;
			}else if(node.pE()&&node.pE().isname()){
				swapnode(node,node.pE());
				node.setAttribute("moved","true");
				this.highlight(node,"m");
				//casingvp(node.pE(),node.pE().innerHTML);
			}else if(node.pE()&&node.pE().gT().length>1&&
				(node.pE().pE()&&node.pE().pE().tagName=="BR" || !node.pE().pE())){
				swapnode(node,node.pE());
				node.setAttribute("moved","true");
				this.highlight(node,"m");
				//casingvp(node.pE(),node.pE().innerHTML);
			}
		}
	},
	"commondata":{},
	"invoker":false,
	"åˆ€é—¨":function(node){
		this.faction(node,"","Äao mÃ´n");
	},
	"addedname":{},
	"ä¸Šå¤©":function(node){
		node.tomean("thÆ°á»£ng thiÃªn");
	},
	"vpdatabase":{},
	"è§’è‰²":function(node){
		node.tomean("nhÃ¢n váº­t");
	},
	"å¤©å¢ƒ":function(node){
		this.faction(node,"","ThiÃªn cáº£nh");
	},
	"ç¥žå¢ƒ":function(node){
		this.faction(node,"","Tháº§n cáº£nh");
	},
	"åœ£å¢ƒ":function(node){
		this.faction(node,"","ThÃ¡nh cáº£nh");
	},
	"å¤§å¸":function(node){
		this.faction(node,"","Äáº¡i Äáº¿");
	},
	"é“å›":function(node){
		this.faction(node,"","Äáº¡o QuÃ¢n");
	},
	"ä¸»å®°":function(node){
		this.faction(node,"","ChÃºa Tá»ƒ");
	},
	"å¥³å¸":function(node){
		this.faction(node,"","Ná»¯ Äáº¿");
	},
	"çŽ‹æœ":function(node){
		this.faction(node,"","VÆ°Æ¡ng Triá»u");
	},
	"å¸æœ":function(node){
		this.faction(node,"","Äáº¿ Triá»u");
	},
	"ç¥žæœ":function(node){
		this.faction(node,"","Tháº§n Triá»u");
	},
	"å¤©æœ":function(node){
		this.faction(node,"","ThiÃªn Triá»u");
	},
	"çŽ„å¢ƒ":function(node){
		this.faction(node,"","Huyá»n cáº£nh");
	},
	"ç«å®—":function(node){
		this.faction(node,"","Há»a tÃ´ng");
	},
	testenglish:function(node){
		var currentnode=node;
		if(this.surns.indexOf(node.cn[0]) >=0){
			return;
		}
		var walked=0;
		var nodlist=[];
		while (currentnode!=null) {
			walked++;
			if(walked>5)break;
			if(engtse.alliseng(currentnode.gT())){
				nodlist.push(currentnode);
			}else {
				break;
			}
			if(!currentnode.isspace(true))break;
			currentnode=currentnode.nE();
		}
		if(nodlist.length<2)return;
		var chi=nodlist.sumChinese("");
		if(chi.length<3)return;
		if(this.testcommon(nodlist) < 3)return;
		var engname = titleCase(engtse.trans(chi));
		node.textContent=engname;
		node.setAttribute("v", engname);
		for(var i=1;i<nodlist.length;i++){
			node.setAttribute("h",node.gH()+" "+nodlist[i].gH());
			node.setAttribute("t",node.gT()+nodlist[i].gT());
			node.cn=node.gT()+nodlist[i].gT();
			nodlist[i].remove();
		}
		meanstrategy.highlight(node,"e");
	},
	containnumber:function(node){
		if(this.database.numrex.test(node.gT())){
			return true;
		}
		return false;
	},
	containmargin:function(node){

	},
	database:{
		preposition:{
			"è¿™":"nÃ y",
			"ä¸":"khÃ´ng"
		},
		phasemarginul:"è¿™äºŽé‚£åˆ°åœ¨".split(""),
		phasemarginl:"è¿™äºŽä»–å¥¹å®ƒä¹ƒä¸ªæ˜¯é‚£å°±åˆ°å‡ºåœ¨å°†".split(""),
		phasemarginr:"é‡ŒåŽä¸­å†…é—´å‰ä¸Šå·¦å³å¤–è¾¹".split("").concat("é™„è¿‘".splitn(2)),
		getmean:function(chi,calb){
			if(chi in this){
				calb(this[chi]);
			}else {
				tse.send("005",chi,function(d){
					if(this.down!="false"){
						meanstrategy.database[this.up]=this.down.trim();
					}
					calb(this.down.trim());
				});
			}
		},
		brk:"[,\.â€œâ€!\?]",
		scope:{
			open: "[ã€Šã€Œã€Žã€ˆã€ï¼»â€˜:Â·]",
			close:"[ã€‹ã€ã€ã€‰ã€‘ï¼½â€™ã€‘ã€‘]"
		},
		pronoun:"æˆ‘ä½ æ‚¨ä»–å¥¹å®ƒ",
		numbers:"ä¸€äºŒä¸‰å››äº”å…­ä¸ƒå…«ä¹åç™¾",
		numrex:/[0-9\.\-\,ä¸€äºŒä¸‰å››äº”å…­ä¸ƒå…«ä¹åç™¾åƒä¸‡ä¸¤äº¿å‡ ]+/,
		level:"ABCDEFGHIKabcdefghikSs123456789ä¸Š",
		carbrand:(function(){var names = ("è®´æ­Œ=ACURA/é˜¿å°”æ³•ç½—å¯†æ¬§=ALFA ROMEOS/é˜¿æ–¯é¡¿é©¬ä¸=ASTON MARTIN/å¥¥è¿ª=AUDI/å®¾åˆ©=BENTLEY/å®é©¬=BMW/å¸ƒåŠ è¿ª=BUGATTI/åˆ«å…‹=BUICK/æ¯”äºšè¿ª=BYD/å¡è¿ªæ‹‰å…‹=CADILLAC/"+
			"é›ªä½›å…°=CHEVROLET/å…‹èŽ±æ–¯å‹’=CHRYSLER/é›ªé“é¾™=CITROEN/é“å¥‡=DODGE/æ³•æ‹‰åˆ©=FERRARI/è²äºšç‰¹=FIAT/ç¦ç‰¹=FORD/æœ¬ç”°=HONDA/æ‚é©¬=HUMMER/çŽ°ä»£=HYUNDAI/è‹±è²å°¼è¿ª=INFINITI/ä¾ç»´æŸ¯=IVECO/"
			+"æ·è±¹=JAGUAR/å‰æ™®=JEEP/èµ·äºš=KIA/å…°åšåŸºå°¼=LAMBORGHINI/è“æ——äºš=LANCIA/è·¯è™Ž=LAND ROVER/é›·å…‹è¨æ–¯=LEXUS/æž—è‚¯=LINCOLN/åŠ³ä¼¦æ–¯=LORINSER/èŽ²èŠ±=LOTUS/çŽ›èŽŽæ‹‰è’‚=MASERATI/"+
			"è¿ˆå·´èµ«=MAYBACH/é©¬è‡ªè¾¾=MAZDA/å¥”é©°=MERCEDES-BENZ/æ°´æ˜Ÿ=MERCURY/åçˆµ=MORRISGARAGES/ä¸‰è±=MITSUBISHI/æ—¥äº§=NISSAN/æ¬§å®=OPEL/å¸•åŠ å°¼=PAGANI/æ ‡è‡´=PEUGEOT/æ™®åˆ©èŒ…æ–¯=PLYMOUTH/"+
			"åºžè’‚äºšå…‹=PONTIAC/ä¿æ—¶æ·=PORSCHE/é›·è¯º=RENAULT/åŠ³æ–¯èŽ±æ–¯=ROLLS ROYCE/ç½—å­š=ROVER/è¨åš=SAAB/ä¸–çˆµ=SPYKER/åŒé¾™=SSANGYONG/æ–¯å·´é²=SUBARU/é“ƒæœ¨=SUZUKI/ä¸°ç”°=TOYOTA/ç‰¹æ–¯æ‹‰=TESLA/"+
			"æ²ƒå…‹æ–¯è±ªå°”=VAUXHALL/æ–‡å›¾ç‘ž=VENTURI/å¤§ä¼—=VOLKSWAGEN/æ²ƒå°”æ²ƒ=VOLVO/ç”µé©´=xe Ä‘áº¡p Ä‘iá»‡n/æ¯’è¯=Veneno").split("/");
				var obj={};
				for(var i=0;i<names.length;i++){
					var name=names[i].split("=");
					obj[name[0]]=name[1];
				}
				obj["names"]=("è®´æ­Œ/é˜¿å°”æ³•ç½—å¯†æ¬§/é˜¿æ–¯é¡¿é©¬ä¸/å¥¥è¿ª/å®¾åˆ©/å®é©¬/å¸ƒåŠ è¿ª/åˆ«å…‹/æ¯”äºšè¿ª/å¡è¿ªæ‹‰å…‹/é›ªä½›å…°/å…‹èŽ±æ–¯å‹’/é›ªé“é¾™/é“å¥‡/æ³•æ‹‰åˆ©/è²äºšç‰¹/ç¦ç‰¹/æœ¬ç”°/"+
					"æ‚é©¬/çŽ°ä»£/è‹±è²å°¼è¿ª/ä¾ç»´æŸ¯/æ·è±¹/å‰æ™®/èµ·äºš/å…°åšåŸºå°¼/è“æ——äºš/è·¯è™Ž/é›·å…‹è¨æ–¯/æž—è‚¯/åŠ³ä¼¦æ–¯/èŽ²èŠ±/çŽ›èŽŽæ‹‰è’‚/è¿ˆå·´èµ«/é©¬è‡ªè¾¾/å¥”é©°/æ°´æ˜Ÿ/åçˆµ/ä¸‰è±/æ—¥äº§/"+
					"æ¬§å®/å¸•åŠ å°¼/æ ‡è‡´/æ™®åˆ©èŒ…æ–¯/åºžè’‚äºšå…‹/ä¿æ—¶æ·/é›·è¯º/åŠ³æ–¯èŽ±æ–¯/ç½—å­š/è¨åš/ä¸–çˆµ/åŒé¾™/æ–¯å·´é²/é“ƒæœ¨/ä¸°ç”°/ç‰¹æ–¯æ‹‰/æ²ƒå…‹æ–¯è±ªå°”/æ–‡å›¾ç‘ž/å¤§ä¼—/æ²ƒå°”æ²ƒ/ç”µé©´/æ¯’è¯").split('/');
				return obj;
			})(),
		english:"ä¸ä¸‡ä¸˜ä¸œä¸°ä¸¹ä¹…ä¹Œä¹”äº‘äºšäº¨äº¬ä»€ä»“ä»£ä»»ä¼Šä¼ä¼‘ä¼¦ä¼¯ä½ä½©ä¿å…‰å…‹å…°å…³å…´å…¹å†…å†ˆå†œå‡†å‡¡å‡¯åˆ‡åˆ©åŠ åŠªåŠ³å‹’åŒ¡åŽå—åšå¡å¢åŽ„å¤å‰å“ˆå“²å”å› å›¾åœ­åŽå¦åŸƒåŸºå¡”å¡žå¤å¤šå¤«å¤¸å¥‡å¥ˆå¥Žå¥¥å§†å¨å«©å­”å­™å®å®‰å®—å®°å®¹å®½å®¾å¯Œå¯Ÿå°Šå°”å°šå°¤å°§å°¼å²‘å·´å¸ƒå¸Œå¸•å¹³åº“åºžåº·å»¶å»·å¼—å½“å½­å½»å¾·æ€€æ©æƒ æˆˆæ‰Žæ‰˜æ‰¬æ‹‰æ‹œæŽªæ•¦æ–‡æ–¯æ–¹æ—¥æ—ºæ˜‚æ˜†æ˜Œæ˜Žæ˜¥æ™®æ›¹æ›¼æ›¾æœ—æœ¬æœ±æœæ­æ°æ¾æž—æžœæŸ¥æŸ³æŸ´æ ¹æ ¼æ¡‘æ¢…æ£®æ¥šæ¬£æ­¦æ¯”æ¯›æ°¸æ±‰æ²ƒæ²™æ³•æ³¢æ³°æ³½æ´›æ´¥æ´ªæ´¾æµ·æ¸©æ»•æ½˜ç¿çƒ­ç„¦ç‰¹çŽ¯ç€ç­ç´ç¼ç‘™ç‘Ÿç“œç“¦ç”˜ç”³ç•™ç™»çš®ç›–çœŸç¥–ç¦ç§‘ç©†ç« ç­–ç±³ç´¢çº¦çº³çº½ç»ç»´ç¼ªç½—ç¿è€ƒè€¶èªè‚–è‚¯èƒ¡èˆèˆ’è‰¾èŠ’èŠ¬è‹è‹¥è‹±èŒ¨èŒ¹èŽ«èŽ±è²è¨è’‚è’™è“¬è”¡è—è—»è¥¿è©¹è®©è¯ºè°¢è±ªè´è´¡è´¹è´¾èµ–èµ›èµžèµ«è¾›è¾¾è¿ˆè¿ªé€šé“é‚¦é‡Œé‡‘é’¦é’±é—¨é˜”é˜¿é™¶éš†é›„é›·éœé’éŸ¦é¡ºé©¬é«˜é²é²é»„é»˜é½é¾™"
	},
	addname:function(level,base,name,script){
		if(script=="titleCase"){
			name=titleCase(name);
		}
		if(script=="firstWord"){
			name=name[0].toUpperCase() + name.substring(1);
		}
		if(script=="firstTwoWord"){
			var c2 = name.indexOf(" ")+1;
			name=name[0].toUpperCase() + name.substr(1,c2-1)+name[c2].toUpperCase()+name.substring(c2+1);
		}
		if(script=="lowerAll"){
			name=name.toLowerCase();
		}
		if(level==0){
			namew.value+="\n"+base+"="+name;
		}
		if(level==1){
			namew.value+="\n@"+base+"="+name;
		}
		if(level==2||level==3){
			namew.value+="\n$"+base+"="+name;
		}
		saveNS();
	}
};

function meanengine(ln,sub){
	if(meanengine.checkparse(ln)){
		return;
	}
	var baseln = ln;
	if(/>?.*?\+.*?=.*/.test(ln)){
		ln=meanengine.shorthand(ln);
	}
	if(/.*?\{0\}.*?=.*/.test(ln)){
		ln=meanengine.shorthand2(ln);
	}
	var delim = "->";
	ln = ln.split(delim);
	if(ln.length<2 || ln[0].contain("=")){
		delim="=";
		ln=baseln.split("=");
		if(ln.length<2){
			console.log(ln + " khÃ´ng Ä‘áº§y Ä‘á»§, bá» qua.");
			return;
		}
		if(!ln[0].contain("{")){
			return meanenginelight(baseln,sub);
		}
	}
	var lefts = ln[0].replace(" ","");
	var stack = [];
	var mstack = [];
	
	var asigner = /@(.+?):(\d+)/.exec(lefts);
	if(asigner){
		lefts = lefts.substr(asigner[0].length);
	}

	var regex ={
		base:/{.*?}(\[.+?\])?/g,
		extend:/{(\d+)(?:\.\.|\~)(\d+)}/,
		exactwidth:/{(\d+)}/,
		havechar:/{\*(.+?)}/,
		haveword:/{\~(.+?)}/,
		lastword:/^{:(.+?)}$/,
		firstword:/^{(.+?):}$/,
		firstandlastword:/^{(.+?):(.+?)}$/,
		mtransform:/{(\d+)->(.*?)}/,
		mremove:/{(\d+_?)X}/,
		mshort:/{(\d+)->@}/,
		mappend:/{(\d+)\+(.+?)}/,
		mreplace:/{(\d+)\-(.+?)}/,
		mrepapp:/{(\d+)\-(.+?)\+(.+?)}/,
		mprepend:/{(.+?)\+(\d+)}/,
		mreppre:/{(.+?)\+(\d+)\-(.+?)}/,
		mrepins:/{(.+?)\+(\d+)\-(.+?)\+(.+?)}/,
		minside:/{(.+?)\+(\d+)\+(.+?)}/,
		mdefault:/{(\d+):}/,
		mfunction:/f\((.*?)\)/,
	};
	var typing={
		"{N}": "name",
		"{PN}": "proname",
		"{P}": "pronoun",
		"{S}": "number",
		"{D}" : "deter",
		"{SD}":"numdeter",
		"{D-}":"deter-",
		"{L}":"locat",
		"{*L}":"lastlocat",
		"{L1}":"locat1",
		"{L2}":"locat2",
		"{T}":"subw",
		"{R}":"relv",
		"{R1}":"relv1",
		"{R2}":"relv2",
		"{R3}":"relv3",
		"{*}":"unlim",
		"{~}":"unlim",
		"{SW}":"stw",
		"{t:F}":"faction",
		"{t:I}":"item",
		"{t:S}":"skill",
		"{VI}":"tviet",
		"{[}":"lbound",
		"{]}":"rbound"
	}
	var m;
	var m2;
	var isEnableAnl = false;
	var bound = {};
	var tkindex = 0;
	do{
		m=regex.base.exec(lefts);
		if(m){
			var mdf = false;
			var token = m[0];
			if(m[1]){
				token= token.substr(0,token.length - m[1].length);
				if(m[1][1] == ':'){
					var m3 = m[1].substr(2,m[1].length-3).toLowerCase();
					mdf = { type: "pos", postype: m3};
				}else{
					var m3 = /^\[(\d+)?(,)?(\d+)?\]$/.exec(m[1]);
					if(m3 == null)m3=[];
					if(m3[1] && m3[2] && m3[3]){
						mdf = { type: "length", min: parseInt(m3[1]), max: parseInt(m3[3])};
					}else if( m3[2] && m3[3]){
						mdf = { type: "length", min: 0, max: parseInt(m3[3])};
					}else if(m3[1] && m3[2]){
						mdf = { type: "length", min: parseInt(m3[1]), max: 99};
					}else if(m3[1]){
						mdf = { type: "length", min: parseInt(m3[1]), max: parseInt(m3[1])};
					}else{
						mdf = { type: "have", text: m[1].substr(1,m[1].length-2)};
					}					
				}
			}
			if(token=="{[}"){
				bound.l = tkindex - 1;
				continue;
			}
			if(token=="{]}"){
				bound.r = tkindex;
				continue;
			}
			tkindex++;
			if(token in typing){
				stack.push({type: typing[token], modifier: mdf});
				continue;
			}
			m2 = regex.extend.exec(token);
			if(m2){
				stack.push({type: "extend", min:parseInt(m2[1]), max:parseInt(m2[2]), modifier: mdf});
				continue;
			}
			m2 = regex.exactwidth.exec(token);
			if(m2){
				stack.push({type: "extend", min:parseInt(m2[1]), max:parseInt(m2[1]), modifier: mdf});
				continue;
			}
			m2 = regex.havechar.exec(token);
			if(m2){
				stack.push({type: "havechar", char: m2[1], modifier: mdf});
				continue;
			}
			m2 = regex.haveword.exec(token);
			if(m2){
				stack.push({type: "haveword", word: m2[1], modifier: mdf});
				continue;
			}
			m2 = regex.lastword.exec(token);
			if(m2){
				stack.push({type: "lastword", word: m2[1], modifier: mdf});
				continue;
			}
			m2 = regex.firstword.exec(token);
			if(m2){
				stack.push({type: "firstword", word: m2[1], modifier: mdf});
				continue;
			}
			m2 = regex.firstandlastword.exec(token);
			if(m2){
				stack.push({type: "firstlast", word1: m2[1], word2: m2[2], modifier: mdf});
				continue;
			}
			stack.push({type:"exact" , word: token.substr(1,token.length-2)});
		}
	}while (m!=null);
	if(lefts[0]=='>'){
		stack[0].isfirst=true;
	}
	if(lefts[lefts.length-1] == '<'){
		stack[stack.length-1].islast=true;
	}
	ln.shift();
	var rights = ln.join(delim);
	do{
		m=regex.base.exec(rights);
		if(m){
			var token = m[0];
			m2 = regex.mshort.exec(token);
			if(m2){
				mstack.push({nodeid:  parseInt(m2[1]) - 1, type: "short"});
				continue;
			}
			m2 = regex.mtransform.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "transform", word: m2[2]});
				continue;
			}
			m2 = regex.mremove.exec(token);
			if(m2){
				if(m2[1].lastChar() == "_"){
					mstack.push({nodeid: parseInt(m2[1]) - 1, type: "removenode"});
				}else{
					mstack.push({nodeid: parseInt(m2[1]) - 1, type: "remove"});
				}
				continue;
			}
			m2 = regex.mappend.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "append", word: m2[2]});
				continue;
			}
			
			m2 = regex.mrepapp.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "repapp", repword: m2[2], word: m2[3]});
				continue;
			}
			m2 = regex.mrepins.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "repins", repword: m2[3], lword: m2[1], rword: m2[4]});
				continue;
			}
			m2 = regex.mreppre.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "reppre", repword: m2[3], word: m2[1]});
				continue;
			}
			m2 = regex.minside.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "inside", lword: m2[1], rword: m2[3]});
				continue;
			}
			m2 = regex.mprepend.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "prepend", word: m2[1]});
				continue;
			}
			m2 = regex.mreplace.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "replace", repword: m2[2]});
				continue;
			}
			m2 = regex.mdefault.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "default"});
				continue;
			}
			mstack.push({nodeid: parseInt(token.substr(1,token.length-2)) - 1, type:"retain"});
		}else{
			m = regex.mfunction.exec(rights);
			if(m){
				mstack.push({function: m[1].trim()});
				break;
			}else{
				if(rights.trim() == "transform" || rights.trim() == "" || rights.trim() == "auto"){
					mstack.push({function: "TFCoreLn"});
					break;
				}
			}
		}
	}while (m!=null);
	if(mstack.length >0 && !mstack[0]["function"])
	if(mstack.length<stack.length){
		for(var i=0;i<stack.length;i++){
			var fl = false;
			for(var j=0;j<mstack.length;j++){
				if(mstack[j].nodeid == i){
					fl=true;
					break;
				}
			}
			if(!fl){
				mstack.push({nodeid:i, type:"remove"});
			}
		}
	}
	var strat = window.meanstrategy;
	if(sub){
		strat = meanengine.db.subpattern;
	}
	if(asigner){
		if(asigner[1] in strat){
			if(!strat[asigner[1]].stack){
				(function(w,dic){
					dic["_def-"+w]=dic[w];
					dic[w]=function(root,subbound){
						for(var i2=0;i2<dic[w].stack.length;i2++){
							if(dic[w].stack[i2](root,subbound)){
								return true;
							}
						}
					}
					dic[w].stack=[
						function(node){
							dic["_def-"+w](node);
						}
					];
				})(asigner[1],strat);
			}
		}else{
			(function(w,dic){
				dic[w]=function(root,subbound){
					for(var i2=0;i2<dic[w].stack.length;i2++){
						if(dic[w].stack[i2](root,subbound)){
							return true;
						}
					}
				}
				dic[w].stack=[];
			})(asigner[1],strat);
		}
		(function(w,startpoint,stk,transformer,base,anl,bound,dic){
			for(var i=0;i<dic[w].stack.length;i++){
				if(dic[w].stack[i].indentity==base){
					return;
				}
			}
			dic[w].stack.push(function(noderoot,subbound){
				if(window.meanengine.matcher(stk[startpoint],noderoot,{})){
					if(window.meanengine.run(noderoot,stk,transformer,startpoint,anl,bound,subbound||bound)){
						console.log('Match ln: '+base);
						return true;
					}
					return false;
				}
				return false;
			});
			dic[w].stack[dic[w].stack.length-1].indentity=base;
		})(asigner[1],parseInt(asigner[2]),stack,mstack,baseln,isEnableAnl,bound,strat);
	}else
	for(var i=0;i<stack.length;i++){
		if(stack[i].type=="exact"){
			if(stack[i].word in strat){
				if(!strat[stack[i].word].stack){
					(function(w,dic){
						dic["_def-"+w]=dic[w];
						dic[w]=function(root,subbound){
							for(var i2=0;i2<dic[w].stack.length;i2++){
								if(dic[w].stack[i2](root,subbound)){
									return true;
								}
							}
						}
						dic[w].stack=[
							function(node){
								dic["_def-"+w](node);
							}
						];
					})(stack[i].word,strat);
				}
			}else{
				(function(w,dic){
					dic[w]=function(root,subbound){
						for(var i2=0;i2<dic[w].stack.length;i2++){
							if(dic[w].stack[i2](root,subbound)){
								return true;
							}
						}
					}
					dic[w].stack=[];
				})(stack[i].word,strat);
			}
			(function(w,startpoint,stk,transformer,base,anl,bound,dic){
				for(var i=0;i<dic[w].stack.length;i++){
					if(dic[w].stack[i].indentity==base){
						return;
					}
				}
				dic[w].stack.push(function(noderoot,subbound){
					if(window.meanengine.run(noderoot,stk,transformer,startpoint,anl,subbound||bound)){
						console.log('Match ln: '+base);
						return true;
					}
					return false;
				});
				dic[w].stack[dic[w].stack.length-1].indentity=base;
			})(stack[i].word,i,stack,mstack,baseln,isEnableAnl,bound,strat);
		}
	}
}
meanengine.parsed={};
function meanenginelight(ln,sub){
	var baseln = ln;
	var delim = "=";
	ln = ln.split(delim);
	if(ln.length<2){
		console.log(ln + " khÃ´ng Ä‘áº§y Ä‘á»§, bá» qua.");
		return;
	}
	var lefts = ln[0].trim();
	var stack = [];
	var mstack = [];
	var regex ={
		base:/{.*?}/g,
		extend:/^(\d+)(?:\.\.|\~)(\d+)$/,
		exactwidth:/^(\d+)$/,
		havechar:/^\*(.+?)$/,
		haveword:/^\~(.+?)$/,
		lastword:/^:(.+?)$/,
		firstword:/^(.+?):$/,
		mdefault:/{(\d+):}/,
		mtransform:/{(\d+)->(.*?)}/,
		mremove:/{(\d+_?)X}/,
		mshort:/{(\d+)->@}/,
		mappend:/{(\d+)\+(.+?)}/,
		mreplace:/{(\d+)\-(.+?)}/,
		mrepapp:/{(\d+)\-(.+?)\+(.+?)}/,
		mprepend:/{(.+?)\+(\d+)}/,
		mreppre:/{(.+?)\+(\d+)\-(.+?)}/,
		mrepins:/{(.+?)\+(\d+)\-(.+?)\+(.+?)}/,
		minside:/{(.+?)\+(\d+)\+(.+?)}/,
		mfunction:/f\((.*?)\)/,
	};
	var typing={
		"N": "name",
		"PN": "proname",
		"P": "pronoun",
		"S": "number",
		"D" : "deter",
		"D-":"deter-",
		"SD":"numdeter",
		"L":"locat",
		"*L":"lastlocat",
		"L1":"locat1",
		"L2":"locat2",
		"T":"subw",
		"R":"relv",
		"R1":"relv1",
		"R2":"relv2",
		"R3":"relv3",
		"*":"unlim",
		"~":"unlim",
		"SW":"stw",
		"t:F":"faction",
		"t:I":"item",
		"t:S":"skill",
		"VI":"tviet",
		"HV":"hviet",
		"[":"lbound",
		"]":"rbound"
	}
	var m;
	var m2;
	lefts= lefts.split(" ");
	var tkindex = 0;
	var bound = {};
	for(var i=0;i<lefts.length;i++){
		m=lefts[i];
		if(m==""){
			continue;
		}
		if(m){
			var token = m;
			if(token=="["){
				bound.l = tkindex - 1;
				continue;
			}
			if(token=="]"){
				bound.r = tkindex;
				continue;
			}
			tkindex++;
			if(token in typing){
				stack.push({type: typing[token]});
				continue;
			}
			m2 = regex.extend.exec(token);
			if(m2){
				stack.push({type: "extend", min:parseInt(m2[1]), max:parseInt(m2[2])});
				continue;
			}
			m2 = regex.exactwidth.exec(token);
			if(m2){
				stack.push({type: "extend", min:parseInt(m2[1]), max:parseInt(m2[1])});
				continue;
			}
			m2 = regex.havechar.exec(token);
			if(m2){
				stack.push({type: "havechar", char: m2[1]});
				continue;
			}
			m2 = regex.haveword.exec(token);
			if(m2){
				stack.push({type: "haveword", word: m2[1]});
				continue;
			}
			m2 = regex.lastword.exec(token);
			if(m2){
				stack.push({type: "lastword", word: m2[1]});
				continue;
			}
			m2 = regex.firstword.exec(token);
			if(m2){
				stack.push({type: "firstword", word: m2[1]});
				continue;
			}
			if(m!=">" && m!="<")
			stack.push({type:"exact" , word: token});
		}		
	}

	if(lefts[0]=='>'){
		stack[0].isfirst=true;
	}
	if(lefts[lefts.length-1] == '<'){
		stack[stack.length-1].islast=true;
	}
	//console.log(stack);
	ln.shift();
	var rights = ln.join(delim);
	//console.log(rights);
	do{
		m=regex.base.exec(rights);
		if(m){
			var token = m[0];
			m2 = regex.mshort.exec(token);
			if(m2){
				mstack.push({nodeid:  parseInt(m2[1]) - 1, type: "short"});
				continue;
			}
			m2 = regex.mtransform.exec(token);
			//console.log(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "transform", word: m2[2]});
				continue;
			}
			m2 = regex.mremove.exec(token);
			if(m2){
				if(m2[1].lastChar() == "_"){
					mstack.push({nodeid: parseInt(m2[1]) - 1, type: "removenode"});
				}else{
					mstack.push({nodeid: parseInt(m2[1]) - 1, type: "remove"});
				}
				continue;
			}
			m2 = regex.mappend.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "append", word: m2[2]});
				continue;
			}
			
			m2 = regex.mrepapp.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "repapp", repword: m2[2], word: m2[3]});
				continue;
			}
			m2 = regex.mrepins.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "repins", repword: m2[3], lword: m2[1], rword: m2[4]});
				continue;
			}
			m2 = regex.mreppre.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "reppre", repword: m2[3], word: m2[1]});
				continue;
			}
			m2 = regex.minside.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "inside", lword: m2[1], rword: m2[3]});
				continue;
			}
			m2 = regex.mprepend.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[2]) - 1, type: "prepend", word: m2[1]});
				continue;
			}
			m2 = regex.mreplace.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "replace", repword: m2[2]});
				continue;
			}
			m2 = regex.mdefault.exec(token);
			if(m2){
				mstack.push({nodeid: parseInt(m2[1]) - 1, type: "default"});
				continue;
			}
			mstack.push({nodeid: parseInt(token.substr(1,token.length-2)) - 1, type:"retain"});
		}else{
			m = regex.mfunction.exec(rights);
			if(m){
				mstack.push({function: m[1].trim()});
				break;
			}else{
				if(rights.trim() == "transform" || rights.trim() == "" || rights.trim() == "auto"){
					mstack.push({function: "TFCoreLn"});
					break;
				}
			}
		}
	}while (m!=null);
	if(mstack.length >0 && !mstack[0]["function"])
	if(mstack.length<stack.length){
		for(var i=0;i<stack.length;i++){
			var fl = false;
			for(var j=0;j<mstack.length;j++){
				if(mstack[j].nodeid == i){
					fl=true;
					break;
				}
			}
			if(!fl){
				mstack.push({nodeid:i, type:"remove"});
			}
		}
	}
	var strat = window.meanstrategy;
	if(sub){
		strat = meanengine.db.subpattern;
	}
	for(var i=0;i<stack.length;i++){
		if(stack[i].type=="exact" && stack[i].word!="çš„"){
			if(stack[i].word in strat){
				if(!strat[stack[i].word].stack){
					(function(w,dic){
						dic["_def-"+w]=dic[w];
						dic[w]=function(root,subbound){
							for(var i2=0;i2<dic[w].stack.length;i2++){
								if(dic[w].stack[i2](root,subbound)){
									break;
								}
							}
						}
						dic[w].stack=[
							function(node){
								dic["_def-"+w](node);
							}
						];
					})(stack[i].word,strat);
				}
			}else{
				(function(w,dic){
					dic[w]=function(root,subbound){
						for(var i2=0;i2<dic[w].stack.length;i2++){
							if(dic[w].stack[i2](root,subbound)){
								break;
							}
						}
					}
					dic[w].stack=[];
				})(stack[i].word,strat);
			}
			(function(w,startpoint,stk,transformer,base,bound,dic){
				for(var i=0;i<dic[w].stack.length;i++){
					if(dic[w].stack[i].indentity==base){
						return;
					}
				}
				dic[w].stack.push(function(noderoot,subbound){
					return window.meanengine.run(noderoot,stk,transformer,startpoint,false,subbound||bound);
				});
				dic[w].stack[dic[w].stack.length-1].indentity=base;
			})(stack[i].word,i,stack,mstack,baseln,bound,strat);
		}
	}
}
meanengine.shorthand=function(ln){
	return ln.replace(/^(>)?(.*?)\+(.*?)=(.*)/,"$1{$2}{*}{$3}->{1->$4}{2}{3}");
}
meanengine.shorthand2=function(ln){
	return ln.replace(/^\{0\}(.+?)=\{0\}(.+)/,"{1..2}{$1}->{1}{2->$2}").
		   replace(/^(.+?)\{0\}(.+?)=\{0\}(.+)/,"{$1}{1..2}{$2}->{1X}{2}{3->$3}").
		   replace(/^(.+?)\{0\}=\{0\}(.+)/,"{$1}{1..2}->{2}{1->$2}").

		   replace(/^\{0\}(.+?)=(.+?)\{0\}$/,"{1..2}{$1}->{2->$2}{1}").
		   replace(/^(.+?)\{0\}(.+?)=(.+?)\{0\}$/,"{$1}{1..2}{$2}->{1->$3}{2}{3X}").
		   replace(/^(.+?)\{0\}=(.+?)\{0\}$/,"{$1}{1..2}->{1->$2}{2}").

		   replace(/^\{0\}(.+?)=(.+?)\{0\}(.+)/,"{1..2}{$1}->{$2+1}{2->$3}").
		   replace(/^(.+?)\{0\}(.+?)=(.+?)\{0\}(.+)/,"{$1}{1..2}{$2}->{1->$3}{2}{3->$4}").
		   replace(/^(.+?)\{0\}=(.+?)\{0\}(.+)/,"{$1}{1..2}->{1->$2}{2+$3}").
		   replace(" *","");
}
meanengine.lbound = function(node,chk){
	if(!chk){
		return node.isspace(false);
	}else{
		return node.pE().id != chk.l;
	}
}
meanengine.rbound = function(node,chk){
	if(!chk){
		return node.isspace(true);
	}else{
		return node.nE().id != chk.r;
	}
}
meanengine.islbound = function(node,chk){
	if(chk){
		return node.id == chk.l;
	}
}
meanengine.isrbound = function(node,chk){
	if(chk){
		return node.id == chk.r;
	}
}
meanengine.subrun=function(root,bound){
	var node = root;
	var cn,lc;
	var dic = meanengine.db.subpattern;
	while(node.id != bound.r){
		cn=node.gT();
		lc=cn.lastChar();
		if(cn in dic){
			dic[cn](node,bound);
		}
		else if(meanengine.db.tokenfind.locat.indexOf(lc)>=0){
			dic['_L'](node,bound);
		}
		else if(lc=='çš„'){
			dic['_çš„'](node,bound);
		}
		node = node.nE();
	}
}
meanengine.run=function(root,stack,transform,start,anl,bound){
	if(anl){
		prediction.parse(root,function(){
			meanengine.run(root,stack,transform,start);
		});
	}
	var subbound = false;
	if(!bound.r){
		bound = false;
	}else{
		if(!isNaN(bound.r)){
			subbound = {
				l:bound.l,
				r:bound.r
			};
			bound = false;
		}
	}
	var flag=false;
	var cr = start;
	var nodepointer=root;
	var nodel = [root];

	if(stack[cr].isfirst){
		if(nodepointer.isspace(false)){
			return false;
		}
	}
	if(stack[cr].islast){
		if(nodepointer.isspace(true)){
			return false;
		}
	}
	if(start>0){
		for(;cr>=0;cr--){
			if(stack[cr].isfirst){
				if(this.lbound(nodepointer,bound)){
				//if(nodepointer.isspace(false)){
					return false;
				}
			}
			if(stack[cr].islast){
				if(this.rbound(nodepointer,bound)){
				//if(nodepointer.isspace(true)){
					return false;
				}
			}
			if(cr>0 && (stack[cr-1].type=="extend"||stack[cr-1].type=="unlim")){
				if(cr-1 > 0){
					var rs = meanengine.finder(stack[cr-2],stack[cr-1],false,nodepointer);
					if(rs==false){
						return false;
					}
					nodel.unshift(rs.ins);
					nodel.unshift(rs.found);
					nodepointer=rs.found;
					cr--;
				}else if(stack[cr-1].isfirst){
					var rs = meanengine.findend(stack[cr-1],false,nodepointer);
					if(rs==false){
						return false;
					}
					nodel.unshift(rs);
					nodepointer=rs[0];
				}else{
					var rs = meanengine.findmax(stack[cr-1],false,nodepointer);
					if(rs==false){
						return false;
					}
					nodel.unshift(rs);
					nodepointer=rs[0];
				}
			}else{
				if(cr>0){
					var passer = {};
					if(nodepointer.pE() && nodepointer.isspace(false) && meanengine.matcher(stack[cr-1],nodepointer.pE(),passer)){
						nodel.unshift(passer.grp || nodepointer.pE());
						nodepointer=nodepointer.pE();
					}else{
						return false;
					}
				}
			}
		}
	}
	cr=start;
	nodepointer=root;
	var stmaxidx = stack.length-1;
	if(start<stack.length-1){
		
		for(;cr<=stmaxidx;cr++){
			if(stack[cr].isfirst){
				if(this.lbound(nodepointer,bound)){
				//if(nodepointer.isspace(false)){
					return false;
				}
			}
			if(stack[cr].islast){
				if(this.rbound(nodepointer,bound)){
				//if(nodepointer.isspace(true)){
					return false;
				}
			}
			if(cr<stmaxidx && (stack[cr+1].type=="extend"||stack[cr+1].type=="unlim")){
				if(stack[cr+1].islast){
					var rs = meanengine.findend(stack[cr+1],true,nodepointer);
					if(rs==false){
						return false;
					}
					nodel.push(rs);
					nodepointer=rs[rs.length-1];
				}else if(cr+1 < stmaxidx){
					var rs = meanengine.finder(stack[cr+2],stack[cr+1],true,nodepointer);
					if(rs==false){
						return false;
					}
					nodel.push(rs.ins);
					nodel.push(rs.found);
					nodepointer=rs.found;
					cr++;
				}else{
					var rs = meanengine.findmax(stack[cr+1],true,nodepointer);
					if(rs==false){
						return false;
					}
					nodel.push(rs);
					nodepointer=rs[rs.length-1];
				}
			}else{
				if(cr<stmaxidx){
					var passer = {};
					if(nodepointer.nE() && nodepointer.isspace(true) && meanengine.matcher(stack[cr+1],nodepointer.nE(),passer)){
						nodel.push(passer.grp || nodepointer.nE());
						nodepointer=nodepointer.nE();
					}else{
						return false;
					}
				}
			}
		}
	}
	var mct = g(contentcontainer);
	for(var i=0;i<nodel.length;i++){
		if(nodel[i].length==1){
			nodel[i]=nodel[i][0];
			meanstrategy.highlight(nodel[i],"ln");
			continue;
		}
		if(nodel[i].length===0){
			nodel[i] = document.createElement("i");
			//mct.insertBefore(nodel[i], nodel[i+1]);
			nodel[i].id="emp"+i;
		}
		if(nodel[i].push){
			for(var j=0;j<nodel[i].length;j++){
				meanstrategy.highlight(nodel[i][j],"ln");
			}
		}else{
			meanstrategy.highlight(nodel[i],"ln");
		}
	}
	//console.log(nodel)
	var performtrans=[];
	
	if(false && subbound){
		var nroot = nodel[subbound.l + 1];
		if(nroot.push){
			nroot = nroot[0];
		}
		var bl = nodel[subbound.l];
		var br = nodel[subbound.r];
		subbound.l = bl.id || bl[bl.length-1].id;
		subbound.r = br.id || br[0].id;
		meanengine.subrun(nroot,subbound);
	}
	if(transform[0] && transform[0]["function"]){
		return window[transform[0]["function"]](nodel);
	}
	meanengine.transform(nodel,transform,performtrans);
	meanengine.swapper2(nodel,performtrans);

	return true;
}
meanengine.transform=function(nodel,transform,performtrans){
	
	var removedword=[];
	for(var i=0;i<transform.length;i++){
		var nodeid = transform[i].nodeid;
		if(!nodel[nodeid]){
			console.log("Unexpected nodeId "+nodeid);
			return;
		}
		if(nodel[nodeid].length>0){
			var b=nodel[nodeid];
			if(transform[i].type=="default"){
				for(var j=0;j<b.length;j++){
					b[j].textContent=getDefaultMean(b[j]);
				}
			}else
			if(transform[i].type=="remove"){
				for(var j=0;j<b.length;j++){
					b[j].textContent="";
				}
			}else
			if(transform[i].type=="transform"){
				if(transform[i].word[0]=="&"){
					b[0].textContent=getDefaultMean(nodel[parseInt(transform[i].word.substring(1)) - 1]);
				}else
				b[0].textContent=transform[i].word;
				for(var j=1;j<b.length;j++){
					b[j].textContent="";
				}
			}else
			if(transform[i].type=="append"){
				b[b.length-1].textContent = getDefaultMean(b[b.length-1]) + " "+transform[i].word;
			}else
			if(transform[i].type=="prepend"){
				b[0].textContent =transform[i].word + " " + getDefaultMean(b[0]);
			}else
			if(transform[i].type=="replace"){
				var rp = transform[i].repword.split("/");
				rp[0] = new RegExp(rp[0], "g");
				for(var j=0;j<b.length;j++){
					if(rp.length>1){
						b[j].textContent=getDefaultMean(b[j]).replace(rp[0],rp[1]);
					}else{
						b[j].textContent=getDefaultMean(b[j]).replace(rp[0],"");
					}
				}
			}
		}else{
			if(transform[i].type=="removenode"){
				nodel[nodeid].textContent="";
				nodel[nodeid].cn="";
				nodel[nodeid].setAttribute("t", "");
			}else
			if(transform[i].type=="default"){
				if(i==0 && isUppercase(nodel[0])){
					nodel[nodeid].textContent=ucFirst(getDefaultMean(nodel[nodeid]));
				}else
				nodel[nodeid].textContent=getDefaultMean(nodel[nodeid]);
			}else
			if(transform[i].type=="retain"){
				if(i==0 && isUppercase(nodel[0])){
					nodel[nodeid].textContent=ucFirst(nodel[nodeid].textContent);
				}
				//nodel[nodeid].textContent=getDefaultMean(nodel[nodeid]);
			}else
			if(transform[i].type=="remove"){
				nodel[nodeid].textContent="";
				//nodel[nodeid].cn = "";
				//nodel[nodeid].setAttribute("t", "");
			}else
			if(transform[i].type=="transform"){
				if(transform[i].word[0]=="&"){
					transform[i].word=getDefaultMean(nodel[parseInt(transform[i].word.substring(1)) - 1]);
				}else
				if(i==0 && isUppercase(nodel[0])){
					//nodel[nodeid].textContent=ucFirst(getDefaultMean(nodel[nodeid]));
					nodel[nodeid].textContent=ucFirst(transform[i].word);
				}else
				nodel[nodeid].textContent=transform[i].word;
			}else
			if(transform[i].type=="short"){
				nodel[nodeid].textContent=meanengine.getshortform(nodel[nodeid].gT());
			}else
			if(transform[i].type=="append"){
				transform[i].word = transform[i].word.replace(/\&(\d)/g, function(a,b){return removedword[parseInt(b)-1]});
				if(i==0 && isUppercase(nodel[0])){
					nodel[nodeid].textContent=ucFirst(getDefaultMean(nodel[nodeid]) + " "+transform[i].word);
				}else
				nodel[nodeid].textContent = getDefaultMean(nodel[nodeid]) + " "+transform[i].word;
			}else
			if(transform[i].type=="prepend"){
				if(i==0 && isUppercase(nodel[0])){
					nodel[nodeid].textContent=ucFirst(transform[i].word + " " + getDefaultMean(nodel[nodeid]));
				}else
				nodel[nodeid].textContent =transform[i].word + " " + getDefaultMean(nodel[nodeid]);
			}else
			if(transform[i].type=="replace"){
				var rp = transform[i].repword.split("/");
				rp[0] = new RegExp(rp[0], "g");
				var oldtext = getDefaultMean(nodel[nodeid]);
				if(rp.length>1){
					nodel[nodeid].textContent=oldtext.replace(rp[0],rp[1]);
					//removedword.push(oldtext.replace(nodel[nodeid].textContent,""));
				}else{
					nodel[nodeid].textContent=oldtext.replace(rp[0],"");
					removedword.push(oldtext.replace(nodel[nodeid].textContent,""));
				}
			}else
			if(transform[i].type=="reppre"){
				var rp = transform[i].repword.split("/");
				rp[0] = new RegExp(rp[0], "g");
				var lw=getDefaultMean(nodel[nodeid]);
				if(rp.length>1){
					lw=transform[i].word+" "+lw.replace(rp[0],rp[1]);
				}else{
					lw=transform[i].word+" "+lw.replace(rp[0],"");
				}
				nodel[nodeid].textContent =lw;
			}else
			if(transform[i].type=="repapp"){
				var rp = transform[i].repword.split("/");
				rp[0] = new RegExp(rp[0], "g");
				var lw=getDefaultMean(nodel[nodeid]);
				if(rp.length>1){
					lw=lw.replace(rp[0],rp[1])+" "+transform[i].word;
				}else{
					lw=lw.replace(rp[0],"")+" "+transform[i].word;
				}
				nodel[nodeid].textContent =lw;
			}else
			if(transform[i].type=="repins"){
				var rp = transform[i].repword.split("/");
				rp[0] = new RegExp(rp[0], "g");
				var lw=getDefaultMean(nodel[nodeid]);
				if(rp.length>1){
					lw=transform[i].lword+" "+lw.replace(rp[0],rp[1])+" "+transform[i].rword;
				}else{
					lw=transform[i].lword+" "+lw.replace(rp[0],"")+" "+transform[i].rword;
				}
				nodel[nodeid].textContent =lw;
			}else
			if(transform[i].type=="inside"){
				var lw=getDefaultMean(nodel[nodeid]);
					lw=transform[i].lword+" "+lw+" "+transform[i].rword;
				nodel[nodeid].textContent =lw;
			}
		}
		
		performtrans.push(nodel[transform[i].nodeid]);
	}
}
meanengine.checkparse=function(source){
	if(source in this.parsed){
		return true;
	}else{
		this.parsed[source]=true;
		return false;
	}
}
meanengine.db={};
meanengine.db.subpattern={
	"_L":function(node){},
	"_çš„":function(node){}
};
meanengine.db.default=[
	"ä¸ºä½• PN={1->vÃ¬ sao}{2}",
	//"> ä¹‹å‰={1->trÆ°á»›c Ä‘Ã³}",
	"> {å¯}{SW}={1->nhÆ°ng}{2}",
	"> {å¯}{1}[:v]={1->cÃ³ thá»ƒ}{2}",
	"> å¯ <={1->cÃ³ thá»ƒ}",
	"> å¯={1->nhÆ°ng}",
	"{è¿ž} {1}[:v] {S}={1->liÃªn tá»¥c}{2}{3}",
	"{è¢«} {PN} {ç»™} {1}[:v]={1}{2}{3->}{4}",
	"{è¿ž} {1}[:n]={1->ngay cáº£}{2}",
	"æ€Žä¹ˆ ä¸ª 1~4 æ³• <={3}{4->nhÆ° tháº¿ nÃ o}",
	"å¸¦ç€ * ç›®çš„ æ¥={1}{3}{2}{4->mÃ  tá»›i}",
	"å¸¦ç€ * ç›®çš„={1}{3}{2}",
	"å›ž 1~5 *ä¿¡={1->tráº£ lá»i tin cá»§a}{2}",
	//"*åœ¨ * æ—¶={1-táº¡i/trong lÃºc}{2}",
	"å— 1~10 å½±å“={1+áº£nh hÆ°á»Ÿng cá»§a}{2}",
	"*åƒ * ä¸€æ · ç®€å•={1-giá»‘ng/Ä‘Æ¡n giáº£n giá»‘ng}{2}",
	"*åƒ * ä¸€æ ·={1}{2}",
	"*å¾… * æ€åº¦={thÃ¡i Ä‘á»™+1}{2}",
	"*æŒ * çƒ­æƒ…={1}{3}{2}",
	"åˆ·æ–° * è®°å½•={1->phÃ¡ ká»· lá»¥c}{2}",
	"é™¤äº† * *å¤– <={1}{2}{3-ngoÃ i|bÃªn ngoÃ i|á»Ÿ ngoÃ i}",
	"å¦‚ * èˆ¬={1->giá»‘ng nhÆ°}{2}",
	":åƒæ˜¯ 1~10 ä¸€èˆ¬={1}{2}",
	":åƒ 1~10 ä¸€èˆ¬={1}{2}",
	"å¦‚ 1~10 ä¸€èˆ¬={1->giá»‘ng nhÆ°}{2}",
	"è·Ÿ 1~10 ä¸€æ ·={1->giá»‘ng nhÆ°}{2}",
	"å›žå¤ 1~6 æ¶ˆæ¯={1->tráº£ lá»i tin cá»§a}{2}",

	"æ²¡æœ‰å›žå¤ 1~6 æ¶ˆæ¯={1->khÃ´ng cÃ³ tráº£ lá»i tin cá»§a}{2}",
	//"åœ¨ <={1->á»Ÿ Ä‘Ã¢y}",
	"*è®© 1~2 ç»™ 1 <={1-Ä‘á»ƒ cho|nhÆ°á»ng|nhÆ°á»£ng|Ä‘á»ƒ|lÃ m cho/bá»‹}{2}{4}",
	"ç»ƒä¹  1~6 è¿‡ç¨‹ä¸­={trong quÃ¡ trÃ¬nh+1}{2}",
	//"é€šè¿‡ 1~5 çš„ 1 *æ¥={1}{4}{3}{2}{5->Ä‘á»ƒ}",
	"å¯è¡Œ <={1->cÃ³ thá»ƒ thá»±c hiá»‡n}",
	"> è¿‡åŽ={1->sau Ä‘Ã³}",
	"> å†å– <={1->oh}",
	"@_L:1{SD}[1,1]{*L}[^trong]={trong+1}{2-trong}",
	"@_L:1{SD}[1,1]{*L}[^bÃªn trong]={trong+1}{2-bÃªn trong}",
	"@_L:1{SD}[1,1]{*L}[^trÃªn]={trÃªn+1}{2-trÃªn}",
	"@_L:1{SD}[1,1]{*L}[^bÃªn trÃªn]={trÃªn+1}{2-bÃªn trÃªn}",
	"æ˜¯ä»¥ 1~3 æ‰“é€ çš„={1->lÃ  dÃ¹ng}{2}{3->mÃ  cháº¿ táº¡o ra}",
	"å‡ºè‡ª 1~10 *å£={1+miá»‡ng cá»§a}{2}",
	"ä¸ä¼šæ˜¯ N çš„ å¯¹æ‰‹={1+Ä‘á»‘i thá»§ cá»§a}{2}",
	"æ˜¯ N çš„ å¯¹æ‰‹={1->lÃ  Ä‘á»‘i thá»§ cá»§a}{2}",
	"æ­£åœ¨ 0~2 *ç€={1->Ä‘ang}{2}{3}",
	"æ­£åœ¨ 1~20 ä¸­ <={1->Ä‘ang}{2}",
	"> åœ¨ t:F æ—¶ <={1->lÃºc á»Ÿ}{2}",
	"> åœ¨ 1~20 æ—¶ <={1->lÃºc}{2}",
	"> åœ¨ 1~20 æ—¶å€™ <={1->lÃºc}{2}",
	"> ç­‰ 1~20 æ—¶å€™ <={1->chá» Ä‘áº¿n lÃºc}{2}",
	"> ç­‰ 1~20 æ—¶ <={1->chá» Ä‘áº¿n lÃºc}{2}",
	"> åœ¨ 1~20 ä¹‹åŽ <={1->sau khi}{2}",
	"> å´åœ¨ 1~20 æ—¶ <={1->nhÆ°ng khi}{2}",
	"> å´åœ¨ 1~20 æ—¶å€™ <={1->nhÆ°ng khi}{2}",
	"> çœ‹å‘ 1~20 æ—¶ <={1->khi nhÃ¬n vá»}{2}",
	"> åœ¨æ²¡æœ‰ 1~20 ä¹‹å‰ <={1->khi chÆ°a cÃ³}{2}",
	"> æ¯æ¬¡ 1~20 çš„æ—¶å€™ <={1->má»—i khi}{2}",
	"{åœ¨} {1}[:v] {1~20} {çš„æ—¶å€™}<={1->khi}{2}{3}",
	"{åœ¨} {1}[:v] {1~20} {:çš„} {æ—¶å€™}<={1->khi}{2}{3}{4}",
	"*å½“ 1~20 æ—¶å€™ <={1}{2}",
	"*å½“ 1~20 çš„æ—¶å€™ <={1}{2}",
	":æ˜¯ ~ åŽ ~ :çš„ 1 <={1}{6}{5}{4}{3}{2}",
	"å°±è¿ž ~ *ä¹Ÿ={1->ngay cáº£}{2}{3}",
	"é‚£äº› 0~2 :ä»¬={1->nhá»¯ng}{2}{3-cÃ¡c|nhÃ³m+kia}",
	"åœ° <={1->Ä‘á»‹a}",
	"ä¸å¯¹ä»˜ <={1->khÃ´ng há»£p nhau}",
	"ç½® 1~5 äºŽ ä¸é¡¾ <={1->khÃ´ng Ä‘áº·t}{2}{3->trong lÃ²ng}",
	"S ä»¥ä¸‹={1}{2->trá»Ÿ xuá»‘ng}",
	"S ä»¥ä¸Š={1}{2->trá»Ÿ lÃªn}",
	"ä»¥ä¸Š S={1->dÃ¹ng hÆ¡n}{2}",
	"> ä»¥ä¸Š={1->phÃ­a trÃªn}",
	"è®© PN <={1->nhÆ°á»ng}{2}",
	"è®© 1={1->Ä‘á»ƒ cho}{2}",
	"ä¸€ä¸ª èƒ½ 1~10 *çš„ 1 <={1}{5}{2}{3:}{4}",
	"å”¯ä¸€ä¸€ä¸ª èƒ½ 1~10 *çš„ 1 <={má»™t cÃ¡i+5+duy nháº¥t}{cÃ³ thá»ƒ+3}",
	"ä¸€ä¸ª èƒ½å¤Ÿ 1~10 *çš„ 1 <={má»™t cÃ¡i+5}{cÃ³ thá»ƒ+3}",
	"å”¯ä¸€ä¸€ä¸ª èƒ½å¤Ÿ 1~10 *çš„ 1 <={má»™t cÃ¡i+5+duy nháº¥t}{cÃ³ thá»ƒ+3}",
	"ä»Ž 1~2 æ·±å¤„={1->tá»« sÃ¢u trong}{2}",
	"å‘ 1~2 æ·±å¤„={1->hÆ°á»›ng sÃ¢u trong}{2}",
	"*ä»¥ 1~3 ä¹‹åŠ¿={1->láº¥y tháº¿}{2}",
	"é—®é“ <={1->há»i}",
	"å¦‚åŒ 1~5 ä¸€èˆ¬={1}{2}",
	"ä¼¼ä¹Ž ~ ä¸€èˆ¬={1}{2}",
	"æœ‰ç§ 1~6 *çš„ æ„Ÿè§‰={1->cÃ³ loáº¡i cáº£m giÃ¡c}{2}{3}",
	"N è‡ªå·±çš„é€‰æ‹©={1}{2->tá»± lá»±a chá»n}",
	"æœ‰ 1~3 ~å®žåŠ›={1+thá»±c lá»±c}{2}{3-thá»±c lá»±c|cá»§a}",
	"> ä¸€èˆ¬={1->bÃ¬nh thÆ°á»ng}",
	"> è¿™ ä¸ <={1->khÃ´ng}{2->pháº£i sao}",
	"è·Ÿ 1~3 ä¼¼çš„ <={1->nhÆ°}{2}",
	"*æ˜¯ 0~3 æ²¡ è·‘äº† <={1}{2}{4->khÃ´ng sai Ä‘Æ°á»£c}",
	"åˆ° 1~3 æ¥è¿‡={1->tá»«ng Ä‘áº¿n}{2}",
	//"æ˜¯ä¸æ˜¯ 1~9 ä¸€ä¼š å°±:={1->cÃ³ pháº£i}{2+hay khÃ´ng}{3}{4}",
	//"æ˜¯ä¸æ˜¯ 1~9 å°±:={1->cÃ³ pháº£i}{2+hay khÃ´ng}{3}",
	":æœ‰ 1~10 å¯èƒ½={1+kháº£ nÄƒng}{2}",
	//"æ˜¯ä¸æ˜¯ 1~9 <={1->cÃ³ pháº£i}{2+hay khÃ´ng}",
	//"ä¸€ä¸ª ~ *ä¸­={1->trong má»™t cÃ¡i}{2}{3-bÃªn trong|á»Ÿ trong|trong}",
	"ä¾¿é—» åˆ° *ä¸€ 1~99 çš„ å‘³é“={1-nghe/ngá»­i}{2}{3+mÃ¹i vá»‹}{4}",
	"ä¾¿é—» *ä¸€ 1~99 çš„ å‘³é“={1-nghe/ngá»­i}{2+mÃ¹i vá»‹}{3}",
	":åˆ° 1~3 çš„ é¢å‰={1+trÆ°á»›c máº·t}{2}",
	":åœ¨ 1~3 çš„ å¤´é¡¶={1->á»Ÿ trÃªn Ä‘á»‰nh Ä‘áº§u}{2}",
	":åœ¨ 1~3 çš„ å¤´ä¸Š={1->á»Ÿ trÃªn Ä‘áº§u}{2}",
	"> æ€» ~ *æ•°={1->tá»•ng}{2}{3}",
	"> æ€» ~ S={1->tá»•ng}{2}{3}",
	"> æ€» ~ *äº†={1->cuá»‘i cÃ¹ng}{2}{3}",
	"> æ€» ~ PN={1->luÃ´n}{2}{3}",
	//"è¢« 1~6 çš„ 1 <={4}{1}{2}{3X}",
	"t:F å››å¤§ ~ä¹‹ä¸€={2->má»™t trong tá»© Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",
	"t:F ä¸‰å¤§ ~ä¹‹ä¸€={2->má»™t trong tam Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",
	"t:F äº”å¤§ ~ä¹‹ä¸€={2->má»™t trong ngÅ© Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",
	"t:F å…­å¤§ ~ä¹‹ä¸€={2->má»™t trong lá»¥c Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",
	"t:F ä¸ƒå¤§ ~ä¹‹ä¸€={2->má»™t trong tháº¥t Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",
	"t:F å…«å¤§ ~ä¹‹ä¸€={2->má»™t trong bÃ¡t Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",
	"t:F ä¹å¤§ ~ä¹‹ä¸€={2->má»™t trong cá»­u Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",
	"t:F åå¤§ ~ä¹‹ä¸€={2->má»™t trong tháº­p Ä‘áº¡i}{3-má»™t trong}{á»Ÿ+1}",

	"t:F å››å¤§ 1~5 ä¹‹ä¸€={2->má»™t trong tá»© Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",
	"t:F ä¸‰å¤§ 1~5 ä¹‹ä¸€={2->má»™t trong tam Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",
	"t:F äº”å¤§ 1~5 ä¹‹ä¸€={2->má»™t trong ngÅ© Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",
	"t:F å…­å¤§ 1~5 ä¹‹ä¸€={2->má»™t trong lá»¥c Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",
	"t:F ä¸ƒå¤§ 1~5 ä¹‹ä¸€={2->má»™t trong tháº¥t Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",
	"t:F å…«å¤§ 1~5 ä¹‹ä¸€={2->má»™t trong bÃ¡t Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",
	"t:F ä¹å¤§ 1~5 ä¹‹ä¸€={2->má»™t trong cá»­u Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",
	"t:F åå¤§ 1~5 ä¹‹ä¸€={2->má»™t trong tháº­p Ä‘áº¡i}{3-má»™t trong}{4-má»™t trong}{á»Ÿ+1}",

	"å››å¤§ ~ ~ä¹‹ä¸€={1->má»™t trong tá»© Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	"ä¸‰å¤§ ~ ~ä¹‹ä¸€={1->má»™t trong tam Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	"äº”å¤§ ~ ~ä¹‹ä¸€={1->má»™t trong ngÅ© Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	"å…­å¤§ ~ ~ä¹‹ä¸€={1->má»™t trong lá»¥c Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	"ä¸ƒå¤§ ~ ~ä¹‹ä¸€={1->má»™t trong tháº¥t Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	"å…«å¤§ ~ ~ä¹‹ä¸€={1->má»™t trong bÃ¡t Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	"ä¹å¤§ ~ ~ä¹‹ä¸€={1->má»™t trong cá»­u Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	"åå¤§ ~ ~ä¹‹ä¸€={1->má»™t trong tháº­p Ä‘áº¡i}{2-má»™t trong}{3-má»™t trong}",
	
	"ä¸€æ¬¡ ~ *çš„ æœºä¼š={1->má»™t cÆ¡ há»™i}{2}{3}",
	"äºŒæ¬¡ ~ *çš„ æœºä¼š={1->hai cÆ¡ há»™i}{2}{3}",
	"ä¸‰æ¬¡ ~ *çš„ æœºä¼š={1->ba cÆ¡ há»™i}{2}{3}",
	"å››æ¬¡ ~ *çš„ æœºä¼š={1->bá»‘n cÆ¡ há»™i}{2}{3}",
	"äº”æ¬¡ ~ *çš„ æœºä¼š={1->nÄƒm cÆ¡ há»™i}{2}{3}",
	"å…­æ¬¡ ~ *çš„ æœºä¼š={1->sÃ¡u cÆ¡ há»™i}{2}{3}",
	"ä¸ƒæ¬¡ ~ *çš„ æœºä¼š={1->báº£y cÆ¡ há»™i}{2}{3}",
	"å…«æ¬¡ ~ *çš„ æœºä¼š={1->tÃ¡m cÆ¡ há»™i}{2}{3}",
	"ä¹æ¬¡ ~ *çš„ æœºä¼š={1->chÃ­n cÆ¡ há»™i}{2}{3}",
	"åæ¬¡ ~ *çš„ æœºä¼š={1->mÆ°á»i cÆ¡ há»™i}{2}{3}",
	"å¾€ 1~3 æ¥={1->tá»›i}{2}",
	"å¾€ 1~3 æ¥äº†={1->tá»›i}{2}",
	"å¾€ 1~3 *æ¥={1->hÆ°á»›ng tá»›i}{2}{3-tá»›i}",
	"ä¸€ 1 å°±={1->vá»«a}{2}{3}",
	"åœ¨è¿›å…¥ 1~3 ä¹‹å‰={trÆ°á»›c+1}{2}",
	":åœ¨ [ :è¿™ 1~8 ] ä¸Š={1+trÃªn}{3+nÃ y}",
	":åœ¨ [ 1~5 ] ä¸Š={1+trÃªn}{2}",
	":åœ¨ [ :è¿™ 1~8 ] ä¸­={1+trong}{3+nÃ y}",
	":åœ¨ 1~5 ä¸­çš„ 1~5 ä¸­={1+trong}{4}{5}{3}{2}",
	":åœ¨ [ 1~5 ] ä¸­={1+trong}{2}{3X}",
	"SD [ 1~2 ] ä¸­={trong+1}{2}",

	":åœ¨ [ 1~5 ] ä¹‹ä¸­={1+trong}{2}{3->}",
	":ä»Ž [ :è¿™ 1~8 ] ä¸­={1+trong}{3+nÃ y}",

	":ä»Ž [ 1~5 ] ä¸­={1+trong}{2}",
	":è¿› [ 1~5 ] ä¸­={1+trong}{2}",
	":åˆ° [ 1~5 ] ä¸­={1+trong}{2}",
	":åˆ°äº† [ 1~5 ] ä¸­={1+trong}{2}",
	":å…¥ [ 1~5 ] ä¸­={1+trong}{2}",
	":å…¥äº† [ 1~5 ] ä¸­={1+trong}{2}",
	":å…¥ [ 1~5 ] ä¹‹ä¸­={1+trong}{2}",

	":åˆ° [ 1~5 ] ä¸Š={1+trÃªn}{2}",
	":åˆ°äº† [ 1~5 ] ä¸Š={1+trÃªn}{2}",

	":æ˜¯ [ 1~5 ] é‡Œ={1+trong}{2}",
	":åœ¨ [ 1~5 ] é‡Œ={1+trong}{2}",
	//	"N ä¸Š={2->trÃªn}{1}",
	"t:F ä¸Š={2->trÃªn}{1}",
	"t:F ä¸­={2->trong}{1}",
	"t:F å†…={2->trong}{1}",
	"t:F é‡Œ={2->trong}{1}",
	"t:F ä¹‹ä¸­={2->bÃªn trong}{1}",
	"t:F ä¹‹ä¸Š={2->phÃ­a trÃªn}{1}",
	"PN åœ¨ t:F çš„ åœ°ä½={Ä‘á»‹a vá»‹ cá»§a+1}{2}{3}",
	"PN åœ¨ N çš„ åœ°ä½={Ä‘á»‹a vá»‹ cá»§a+1}{2}{3}",
	"è¿™ 1~3 ] ä¸Š={1->trÃªn}{2}{3->nÃ y}",
	//"è¿™ 0~3 ä¸Š={trÃªn+1-nÃ y}{2-nÃ y}{3->nÃ y}",
	"è¿™ 1~3 ] ä¸­={trong+1}{2}{3->nÃ y}",
	//"è¿™ 0~3 ä¸­={trong+1-nÃ y}{2-nÃ y}{3->nÃ y}",
	"åœ¨ 1~3 çœ¼ä¸­={1->á»Ÿ trong máº¯t}{2}",
	"PN çœ¼ä¸­={2}{1}",
	"åœ¨ æˆä¸º 1~8 ä¹‹å‰={1->trÆ°á»›c khi}{2}{3}",
	"> å†… ä¸ª <={1->cÃ¡i}{2->kia}",
	"è¶³è¶³ 1~3 å¤š={1+hÆ¡n}{2}",
	"ä»¿ä½›åœ¨ 1~3 ä¸€èˆ¬={1->giá»‘ng nhÆ° Ä‘ang}{2}",
	"åœ¨ 1~5 å¸¦é¢†ä¸‹={1->dÆ°á»›i sá»± dáº«n Ä‘áº§u cá»§a}{2}",
	"ä¸ªå¤´ ~ *ä½Žé«˜è…°è‚©={1->chiá»u cao}{2}{3}",
	"æŒ¡ 1~3 *çš„ è·¯={1->cáº£n Ä‘Æ°á»ng}{2}{3}",
	"ä¹Ÿ <={1->a}",
	"> ä¸­ S={1->trÃºng}{2}",
	"è¿™èŠ± S={1->láº§n nÃ y tá»‘n}{2}",
	"ä¸æ­¢ <={1->khÃ´ng ngá»«ng}",
	"è¿™ä¹ˆ 1 <={1X}{2+nhÆ° váº­y}",
	"é‚£ä¹ˆé«˜ çš„ 1 <={1-> }{2-> }{3+cao nhÆ° váº­y}",
	"é‚£æ · çš„ 1 <={1X}{2X}{3+nhÆ° tháº¿}",
	"è¿™æ · çš„ 1 <={1X}{2X}{3+nhÆ° váº­y}",
	"å¦‚æ­¤ 1 <={1X}{2+nhÆ° tháº¿}",
	"è¿™èˆ¬ 1 <={1X}{2+nhÆ° váº­y}",

	//"è¿™ä¹ˆ 1 <={1+nhÆ° váº­y}",
	//	"å°† é‚£:={1->Ä‘em}{2}",
	//	"å°† è¿™:={1->Ä‘em}{2}",
	///	"å°† æ­¤:={1->Ä‘em}{2}",
	//	"å°† ä¸‹ <{1->sáº½}{2->xuá»‘ng}",
	//	"å°† 1 <={1->sáº½}{2}",
	"æœ‰ç€ 1 ä¸€èˆ¬ *çš„ 1 <={1->cÃ³}{5+giá»‘ng nhÆ°}{2}",
	"æœ‰ç€ 1 ä¸€èˆ¬ *çš„={1->cÃ³ giá»‘ng nhÆ°}{2}{3X}{4}",
	"è¿›å…¥ 1~3 å‰={1->trÆ°á»›c khi vÃ o}{2}",
	"å¾—å¾ˆ <={1->vÃ´ cÃ¹ng}",
	"ä¸­äº† ~ *çš„ ç®—è®¡={1->Ä‘Ã£ trÃºng káº¿ cá»§a}{2}{3}",
	"è·ç¦» S={1->cÃ¡ch}{2}",
	"è·ç¦» t:F={1->cÃ¡ch}{2}",
	"å—åˆ° ~ ~å°Šæ•¬={1->Ä‘Æ°á»£c}{2}{3}",
	"S å‡ºå¤´={2->hÆ¡n}{1:}",
	"S åˆšå‡ºå¤´={2->vá»«a má»›i hÆ¡n}{1:}",
	"æ•¢æ€ ~ çš„ äºº={ngÆ°á»i+1}{2}",
	"è¢« [ 1~5 ] æ‰€={1}{2}",
	"PN æ‰€={1}",
	"S ä¸ªäºº={1}{2->ngÆ°á»i}",
	"*å¬ ~ çš„è¯ <={1}{2}{3->lá»i nÃ³i}",
	"æ¥ä¹Ÿ <={1->tá»›i Ä‘Ã¢y}",
	"ç„¶ä¹Ÿ <={1->Ä‘Ãºng váº­y}",
	"èµ°ä¸‹åŽ» <={1->tiáº¿p tá»¥c Ä‘i}",
	"æŠ±ç€ å°†ä»– 1 ç›®çš„={1->mang theo má»¥c Ä‘Ã­ch}{3}{2->háº¯n}",
	"æŠ±ç€ 1~8 ç›®çš„={1->mang theo má»¥c Ä‘Ã­ch lÃ }{2}",
	"æ¯” 1~2 è¦ 1~2 å¤š:={1X}{3X}{4+hÆ¡n}{2}{5->nhiá»u}",
	//"ä¸€è¾¹ 1 ç€={1->vá»«a Ä‘ang}{2}",
	"*æ¯ ~ éƒ½å°†={1}{2}{3->Ä‘á»u sáº½}",
	"S è¦ 1~5 äº† <={1}{2->lÃ  sáº½}{3}{4->rá»“i}",
	//"è¦ 1~5 äº† <={1->sáº¯p}{2}{3->rá»“i}",
	//"S è¦ :äº† <={1}{2->lÃ  sáº½}{3+rá»“i}",
	//"è¦ :äº† <={1->sáº¯p}{2-rá»“i+rá»“i}",
	//"> 1 äº† <={1-rá»“i}{2->rá»“i}",
	//"> PN 1 äº† <={1}{2-rá»“i}{3->rá»“i}",
	"> PN é“ <={1}{2->nÃ³i}",
	"PN :å’Œ 1~3 åˆ†æ‰‹åŽ={2->sau khi}{1+chia tay}{3}",
	":å’Œ 1~3 åˆ†æ‰‹åŽ={1->sau khi chia tay}{2}",
	":åœ¨ 1~4 æ‰‹ä¸­={1+trong tay}{2}",
	"PN æ‰‹ä¸­={2}{1}",
	"è¿›å…¥: 1~5 çŠ¶æ€={1+tráº¡ng thÃ¡i}{2}",
	//"> 1 çš„ äºº={ngÆ°á»i+1}{2X}{3X}",
	"æŠŠ 1~3 å˜æˆäº†={1->Ä‘Ã£ biáº¿n}{2}{3->thÃ nh}",
	"è¶³æœ‰ S ä¹‹å¤š={1->cÃ³ hÆ¡n}{2}",
	"è¶³æœ‰ S S ä¹‹å¤š={1->cÃ³ hÆ¡n}{2}{3}",
	"PN åœ¨ 1~8 åš çš„ äº‹:={6->chuyá»‡n}{1}{4}{2->á»Ÿ}{3}{5X}",
	"{S}[nÄƒm]{é‡Œ}={trong+1}{2->}",
	"S ä¸¤={1}{2->láº¡ng}",
	"> è¿™æ · PN={1->nhÆ° váº­y}{2}",
	":ä¸­ åˆ†åˆ« æœ‰={1}{2->cÃ³ chia}{3->thÃ nh}",
	"ä»¿ä½› 1~5 ä¸€èˆ¬={1->giá»‘ng nhÆ° lÃ }{2}{3->}",
	//"å†æ¥ S={1->láº¡i thÃªm}{2}",,,
	//MG
	"è¿™äº› 1~2 L={3+nhá»¯ng}{2}{1->nÃ y}",
	"è¿™ä¸ª t:F L={3}{2}{1->nÃ y}",
	"è¿™ t:F L={3}{2}{1->nÃ y}",
	"é‚£äº› 1~2 å®ž:={1->nhá»¯ng}{2+kia}{3}",
	"è¿™ä¸ª 1~2 æ˜¯:={1->cÃ¡i}{2+nÃ y}{3}",
	"PN çš„ è¿™ä¸ª 1~2 çš„ 1 <={6+cá»§a}{4}{3->nÃ y cá»§a}{1:}",
	//ST
	"åœ¨æ²¡æœ‰ å…¶ä»– ~ æƒ…å†µ ä¸‹={1->trong tÃ¬nh huá»‘ng khÃ´ng cÃ³}{3+khÃ¡c}",
	"åœ¨æ²¡æœ‰ ~ æƒ…å†µ ä¸‹={1->trong tÃ¬nh huá»‘ng khÃ´ng cÃ³}{2}",
	"åœ¨ ~ æƒ…å†µ ä¸‹={1->dÆ°á»›i tÃ¬nh huá»‘ng}{2}",
	"çœ‹äº† PN ä¸€çœ¼={1->liáº¿c}{2}{3->má»™t cÃ¡i}",
	"> å°±åœ¨ 1~10 ä¹‹é—´ <={1->ngay lÃºc}{2}",
	//SS
	"å’Œ 1~3 ä¸ä¸€æ ·={1->khÃ´ng giá»‘ng vá»›i}{2}",
	//LR
	"åœ¨ æˆ‘ è¿™={3->á»Ÿ ta cÃ¡i nÃ y}",
	"åœ¨ é‚£={1->á»Ÿ}{2->Ä‘Ã³}",
	"é‚£ å„¿={1->chá»—}{2->Ä‘Ã³}",
	"è¿™ å„¿={1->chá»—}{2->nÃ y}",

	"{PN}[2,] {ä½“å†…}={trong cÆ¡ thá»ƒ cá»§a+1}{2X}",
	"{PN}[2,] {R1} {ä½“å†…}={trong cÆ¡ thá»ƒ cá»§a+1}{2X}{3X}",
	"{PN}[2,] {èº«ä½“}={cÆ¡ thá»ƒ cá»§a+1}{2X}",
	"{PN}[2,] {R1} {èº«ä½“}={cÆ¡ thá»ƒ cá»§a+1}{2X}{3X}",
	"{PN}[2,] {æ³¨æ„åŠ›}={sá»± chÃº Ã½ cá»§a+1}{2X}",
	"{PN}[2,] {R1} {æ³¨æ„åŠ›}={sá»± chÃº Ã½ cá»§a+1}{2X}",
	"{è¢«} {1}[:v,vn] {0~3} {:çš„} {PN}={4}{1}{2}{3}",
	":æ˜¯ ä¹‹å‰={1}{2->lÃºc trÆ°á»›c}",
	//"{:ç€}[2,] {ä¸€ä¸ª} {1}[:n]<={cÃ³+2}{3}{Ä‘ang+1}",
	//"{:ç€}[2,] {ä¸€ä¸ª} {~} {:çš„} {1}<={cÃ³+2}{5}{3}{4}{Ä‘ang+1}",
	//"@_çš„:3{:ç€}[2,] {SD} {~} {:çš„} {1}<={cÃ³+2}{5}{3}{4}{Ä‘ang+1}",
	//"@_çš„:3{:ç€}[2,] {SD} {~} {:çš„} {1}[:a,n] {1}[:n]={cÃ³+2}{6}{5}{3}{4}{Ä‘ang+1}",
	//":ç€ ä¸€ä¸ª={cÃ³ Ä‘ang+1}{2}",
	"è¦å›žæ¥ <={1->sáº½ trá»Ÿ vá»}",
	"{å¥½} {1}[:v]={1->dá»…}{2}",
	"{å¥½} {1}[:i,a]={1->tháº­t}{2}",
	"{PN} {å¥½}<={1}{2->tá»‘t}",
	"{1}[:uj,v,i,a] {å¾—}={1}{2->Ä‘áº¿n}",
	"{è¿™ä¹ˆå¤š} {1}[:n]={1->nhiá»u}{2+nhÆ° váº­y}",
	"{è¿™ä¹ˆå¤š} {R1} {1}[:n]={1->nhiá»u}{2}{3+nhÆ° váº­y}",
	"P å¦‚æ­¤ 1 çš„ 1 <={5}{3}{nhÆ°+1}",
	"P å¦‚æ­¤ :çš„ 1 <={4}{3}{nhÆ°+1}",
	"> ä¸Š <={1->lÃªn}",
	"è¿˜ç»™ 1 <={1->tráº£ cho}{2}",
	"è¿˜ç»™ 1 R<={1->tráº£ cho}{2}",
	"è¿˜ç»™æˆ‘ <={1->tráº£ cho ta}",
	"è¿˜ç»™æˆ‘ R <={1->tráº£ cho ta}",
	"{1}[:v,vg,a]{ä¸‹åŽ»}={1}{2->tiáº¿p}",
	"{1}[^Ä‘ang]{ç€}={1}",
	"{1}[2,]{å„¿}={1}",
	"{1}[:v]{ä½}={1}{2->ná»•i}",
	//"@_çš„:0>{:çš„}{N}={2}{1:}",
	//">{1}[:3,]{çš„}{N}={3}{1:}{2}",
	//"@_çš„:2>{1}[:v]{1~2}{:çš„}{N}={4}{1:}{2}{3}",
	//">{1}[:v]{1~2}{çš„}{N}<={4}{1}{2}{3}",
	//">{1}[:n,s]{1}[:v,r]{0~2}{çš„}{N}={5}{1}{2}{3}{4}",
	"å† 1 ç‚¹={1}{2}{3->thÃªm chÃºt}",
	"æœ <={1->triá»u}",
	"å†² <={1->xÃ´ng}",
	"{è¿™} {1}[^trong|bÃªn trong|trÃªn]={1->}{2+nÃ y}",
	"{PN} {0~2} {ç»™} {PN} {1}[:v]={1}{2}{5}{3}{4}",
	"{:æ˜¯} {PN} {1}[:v,vp] {PN} {çš„} {1}[:n,np,v,vp]<={1}{6+Ä‘á»ƒ}{2}{3}{5}{4}",
	
	//
	"{1}[:v,vp] {èµ·æ¥}={1}",
	"{:åˆ°} {PN} {1}[:s]=>{1}{3}{2}",
	//"{PN} {å¿ƒ} {ä¸­}={2->trong lÃ²ng}{1}",
	//"@_çš„:1>{PN} {*L} {1}[:n,np]<={3}{2}{1}",
	//
	//"@_çš„:1>{PN} {1} {*L} {1}[:n,np]<={3}{2}{1}",
	//"@_çš„:1>{1}[n,np] {*L} {1}[:n,np]<={3}{2}{1}",
	"{PN} {æ‰€åœ¨} {çš„} {1~2}[:n,np,ns]<={4+nÆ¡i}{1}{2->Ä‘ang á»Ÿ}",
	"{PN} {æ‰€åœ¨} {çš„} {1~2}[:n,np,ns] {*L}={5}{4+nÆ¡i}{1}{2->Ä‘ang á»Ÿ}",
	"S å¤©åŽ={1}{2}",
	"å¤©åŽ={1->ThiÃªn háº­u}",
	//"@_L:2{:åœ¨}{PN}{*L}[:n,np]={1}{3-nÃ y+cá»§a}{2}",
	//"@_L:3{:åœ¨}{PN}{çš„}{*L}[:n,np]={1}{4-nÃ y+cá»§a}{2}{3}",
	//"@_L:2{:åœ¨}{PN}{*L}={1}{3-nÃ y}{2}",
	//"@_L:3{:åœ¨}{PN}{çš„}{*L}={1}{4-nÃ y}{2}{3}",
	"{å½“:}[khi] {*} {æ—¶}={1}{2}",
	//"@_çš„:1{PN}{1}[:a]{1}[:n,np,ns,m]<={3}{2+cá»§a}{1}",
	"{è¿™ç§} {*L}[trong]={1->trong loáº¡i}{2+nÃ y}",
	"{è¿™ç§} {*L}[trÃªn]={1->trÃªn loáº¡i}{2+nÃ y}",
	"{è¿™ç§} {*L}[dÆ°á»›i]={1->dÆ°á»›i loáº¡i}{2+nÃ y}",
	"{è¿™ç§} {*L}[giá»¯a]={1->giá»¯a loáº¡i}{2+nÃ y}",
	"{é‚£ç§} {*L}[trong]={1->trong loáº¡i}{2+kia}",
	"{é‚£ç§} {*L}[trÃªn]={1->trÃªn loáº¡i}{2+kia}",
	"{é‚£ç§} {*L}[dÆ°á»›i]={1->dÆ°á»›i loáº¡i}{2+kia}",
	"{é‚£ç§} {*L}[giá»¯a]={1->giá»¯a loáº¡i}{2+kia}",
	"{æœç€} {1~2} {é—®é“}={1}{2}{3->há»i}",
	"åœ¨ ~ è¿‡ç¨‹ä¸­ <={1->trong quÃ¡ trÃ¬nh}{2}",
	"@_çš„:0{å¦‚:} {1}[:n]={2}{1}",
	"@_çš„:2{SW} {è¿™:} {*L} {1}[:n]<={1}{4}{3}{2}",
	"@_çš„:2{PN} {è¿™:} {*L} {1}[:n]<={1}{4}{3}{2}",
	"@_çš„:1>{è¿™:} {*L} {1}[:n]<={1}{4}{3}{2}",
	//"{å’Œ} {PN} {:çš„} {æ—¶å€™}={4}{1}{2}{3}",
	//"{SW} {PN} {SW} {PN} {1}[:v] {çš„} {1}[:n]<={1}{7}{2}{3}{4}{5}",
	//"{è¢«} {1}[:n,np] {1}[:v,vp] {:çš„} {1}<={5}{1}{2}{3}{4}",
	//"~{è¢«} {1}[:n,np] {:çš„}[:v,vp] {1}<={4}{1}{2}{3}",
	//"@_L:2{SW} {PN} {*L}={1}{3}{2}",
	"*L é¢={1}",
	//":åˆ° 1~2 çš„æ—¶å€™={1}{3}{2}",
	//":åˆ° 1~2 æ—¶å€™={1}{3}{2}",
	"æ­£å‡†å¤‡ ~ æ—¶å€™={3->khi}{1}{2}",
	//"@_L:1{SD}[má»™t]{*L}[^trong|trÃªn|dÆ°á»›i|ngoÃ i|gáº§n|xa]={1+&2}"
];
meanengine.db.defaultwoln=[
	"{PN} {1}[:v,vp] {PN} {çš„} {1}[:n,np,v,vp]<={1}{2}{5}{4}{3}",
];
meanengine.db.defaultwln=[
	"@_çš„:1>{PN} {:çš„} {1~3}<=f(TFCoreLn)",
	"@_çš„:2>{PN} {1~5} {:çš„} {1~3}<=f(TFCoreLn)",
	"@_çš„:1>{PN} {*L} {1}[:n,np]<=f(TFCoreLn)",
	"æœ‰ ~ :çš„ ~ åœ¨=f(TFCoreLn)",
];
meanengine.db.sdefault=[
	"åˆšåˆš ~ :çš„ 1={4}{1:}{2}{3}",
	"> PN 1 2~10 L æ—¶={5}{1:}{2}{4}{3}",
	"> PN 3~10 æ—¶={3}{1:}{2}",
	"{å°†} {1} {1}[:v]={1X}{3-(Ä‘áº¿n|vÃ o|tá»›i|qua|lÃªn|xuá»‘ng|vá»).*}{2+&1}",
	"{æŠŠ}[tá»›i] {1} {1}<={1X}{3-tá»›i}{2+tá»›i}",
	"{æŠŠ}[Ä‘áº¿n] {1} {1}<={1X}{3-Ä‘áº¿n}{2+Ä‘áº¿n}",
	"{æŠŠ}[lÃªn] {1} {1}<={1X}{3-lÃªn}{2+lÃªn}",
	"{æŠŠ}[xuá»‘ng] {1} {1}<={1X}{3-xuá»‘ng}{2+xuá»‘ng}",
	"{æŠŠ}[qua] {1} {1}<={1X}{3-qua}{2+qua}",
	"æœç€ 1 1 <={3-tá»›i|hÆ°á»›ng|vá»+vá»}{1X}{2}",
	"æœ 1 1 <={3-tá»›i|hÆ°á»›ng|vá»+vá»}{1X}{2}",
	"ä»€ä¹ˆ 1 <={1X}{2+gÃ¬}",
	"{ä»€ä¹ˆ} {1}[:n] {1}[:n]={1X}{2}{3+gÃ¬}",
	"{å¯¹} {PN} {çš„} {1}[:n,d]={4}{3}{1}{2}",
	"{å¯¹} {PN} {1}[:v] {çš„} {1}[:n,d]={5}{4}{3}{1}{2}",
	"{1}[:a]{çš„}{1}[:n,a]<={2:}{3}{1:}",
	"{1}[:a]{çš„}{1}[:n,a] {1}[:d,v,ad,p,u]={2:}{3}{1:}",
	//">{1}{PN}{çš„}{1}{SW}={1}{4+cá»§a}{2:}{5}{3_X}",
	">{PN}{çš„}{1}<={3+cá»§a}{1:}{2_X}",
	">{1}[:c,a]{PN}{çš„}{1}<={1}{4+cá»§a}{2:}{3_X}",
	">{PN}{çš„}{1}[:n]{1}[:v,d,ad,p,u]={3+cá»§a}{1:}{4}",
	">{PN}{çš„}{1}{è¢«:}={3+cá»§a}{1}{4:}{2_X}",
	"{PN}{çš„}{1}{*å’Œ}{PN}{çš„}{1}={3+cá»§a}{1}{4->vÃ }{7+cá»§a}{5}",
	"{æˆä¸º} {PN} {çš„} {1} <={1}{4}{2}{3}",
	"{æˆä¸º} {1} {çš„} {1} <={4}{1}{2}{3}",
	"{:æ˜¯} {PN} {çš„} {1} <={1}{4+cá»§a}{2}{3_X}",
	"{æ˜¯} {PN} {:çš„}[1,3] {1} <={1}{4+cá»§a}{2}{3}",
	"{æ˜¯} {PN} {:çš„}[4,] {1} <={1}{4}{2}{3}",
	"{æ˜¯} {:çš„} {1} <={1}{3}{2}",
	"{:æ˜¯} {PN} {PN} {çš„} {1} <={1}{5+cá»§a}{4_X}{3}{2}",
	"{PN} {1}{çš„} {1}[:v]={1}{2}{3->mÃ }{4}",
	"{PN} {1}[:v]{çš„} {1}[:n] {1}[:n]<={5}{4}{1}{2}",
	
	"{PN} {1}[:v]{çš„} {1}[:n]<={4}{1}{2}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n] {1}[:n]<={5}{4}{2}{1}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n]<={4}{2}{1}",
	"{PN} {1}[:v]{çš„} {1}[:n] {1}[:n] {SW}={5}{4}{1}{2}{6}",
	"{PN} {1}[:v]{çš„} {1}[:n] {SW}={4}{1}{2}{5}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n] {1}[:n] {SW}={5}{4}{2}{1}{6}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n] {SW}={4}{2}{1}{5}",
	"{PN} {çš„} {1}[^trong|ngoÃ i|trÃªn|dÆ°á»›i]={3+cá»§a}{1}",
	"{PN} {çš„} {1} {1}[^trong|ngoÃ i|trÃªn|dÆ°á»›i]={4}{3+cá»§a}{1}",
	//">{PN} {1}{çš„} {1}<={4}{2+cá»§a}{1}",
	//">{PN} {1}[:v]{çš„} {1} {SW}={4}{1}{2}{5}",
	//">{PN} {1}{çš„} {1} {SW}={4}{2+cá»§a}{1}{5}",

	"@_çš„:1>{PN} {:çš„}[:v] {1}[nÃ y]<={3-nÃ y}{1}{2+nÃ y}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[:v]<={1}{2}{3}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[:n]<={3}{1}{2}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:c]<={1}{2}{3}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:v]<={1}{3}{2}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}<={3}{2+cá»§a}{1}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[nÃ y] {SW}={3-nÃ y}{1}{2+nÃ y}{4}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[:n] {SW}={3}{1}{2}{4}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:n] {SW}={3}{2+cá»§a}{1}{4}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:n]<={3}{2+cá»§a}{1}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:n] {SW}={3}{2+cá»§a}{1}{4}",


	//"{:æ˜¯} {1} {PN} {PN} {çš„} {1} <={1}{2}{6+cá»§a}{5_X}{3}{4}",

	//"{:æ˜¯} {1} {PN} {çš„} {1} <={1}{2}{5+cá»§a}{4_X}{3}",
	//"{:æ˜¯} {1} {t:F} {çš„} {1} <={1}{2}{5+cá»§a}{4_X}{3}",
	//"{PN} {åœ¨} {~} {1}[:v] {~}<={1}{4}{5}{2}{3}",
	///"{PN} {åœ¨} {t:F} {~}<={1}{4}{2}{3}",

		"{:è¿™} {PN} {çš„} {1} <={4}{2}{3_X}{1->nÃ y}",
	"{è¿™} {PN} {:çš„} {1} <={4}{2}{3_X}{1->nÃ y}",
	"{è¿™} {:çš„} {1} <={3}{2}{1->nÃ y}",
	"{:è¿™} {PN} {PN} {çš„} {1} <={5}{4_X}{3}{2}{1->nÃ y}",
	//"{:è¿™} {1} {PN} {PN} {çš„} {1} <={2}{6}{5_X}{3}{4}{1->nÃ y}",

	"{:è¿™} {1} {PN} {çš„} {1} <={1}{2}{5}{4_X}{3}",
	"{:è¿™} {1} {t:F} {çš„} {1} <={1}{2}{5}{4_X}{3}",



	"{è¢«:åœ¨} {0~1} {L} {çš„} {1} <={5}{1}{2}{3}{4_X}",
	"{è¢«:} {~} {:åœ¨} {~} {L} {çš„} {1} <={7}{1}{2}{3}{4}{5}{6}",


		//"{è¿™}{SD}{1~2}[:n]{çš„}{1}[:n]={2}{5}{3}{1->nÃ y}{4}",
		//"{è¿™}{SD}{1~2}[:a]{çš„}{1}[:n]={2}{5}{3}{1->nÃ y}{4}",
		//"{è¿™}{SD}{1~2}{çš„}{VI}={2}{5}{3}{1->nÃ y}{4}",
	//"{è¿™}{SD}{1~2}{çš„}{1}<={2}{5}{3}{1->nÃ y}{4}",
	//"{è¿™}{SD}{:çš„}{VI}={2}{4}{3}{1->nÃ y}",
	//"{è¿™}{SD}{:çš„}{1}<={2}{4}{3}{1->nÃ y}",

		"{è¿™}{SD}{1~2}{çš„}{VI}={5}{2}{3}{1->nÃ y}{4}",
	"{è¿™}{SD}{1~2}{çš„}{1}<={5}{2}{3}{1->nÃ y}{4}",
	"{è¿™}{SD}{:çš„}{VI}={4}{2}{3}{1->nÃ y}",
	"{è¿™}{SD}{:çš„}{1}<={4}{2}{3}{1->nÃ y}",

		"{é‚£}{SD}{1~2}{çš„}{VI}={2}{5}{3}{1->kia}{4}",
	"{é‚£}{SD}{1~2}{çš„}{1}<={2}{5}{3}{1->kia}{4}",
	"{é‚£}{SD}{:çš„}{VI}={2}{4}{3}{1->kia}",
	"{é‚£}{SD}{:çš„}{1}<={2}{4}{3}{1->kia}",

	"{SD}{1~2}{çš„}{VI}={1}{4}{2}{3}",
	"{SD}{1~2}{çš„}{1}<={1}{4}{2}{3}",
	"{SD}{:çš„}{VI}={1}{3}{2}",
	"{SD}{:çš„}{1}<={1}{3}{2}",

	//	"@_çš„:2{SD}{1~2}{:çš„}{VI}={1}{4}{2}{3}",
	//	"@_çš„:2{SD}{1~2}{:çš„}{1}<={1}{4}{2}{3}",
	//	"@_çš„:1{SD}{:çš„}{VI}={1}{3}{2}",
	//	"@_çš„:1{SD}{:çš„}{1}<={1}{3}{2}",

		"{è¿™}{D}{1~2}{çš„}{VI}={2}{5}{3}{1->nÃ y}{4}",
	"{è¿™}{D}{1~2}{çš„}{1}<={2}{5}{3}{1->nÃ y}{4}",
	"{è¿™}{D}{:çš„}{VI}={2}{4}{3}{1->nÃ y}",
	"{è¿™}{D}{:çš„}{1}<={2}{4}{3}{1->nÃ y}",

		"{é‚£}{D}{1~2}{çš„}{VI}={2}{5}{3}{1->kia}{4}",
	"{é‚£}{D}{1~2}{çš„}{1}<={2}{5}{3}{1->kia}{4}",
	"{é‚£}{D}{:çš„}{VI}={2}{4}{3}{1->kia}",
	"{é‚£}{D}{:çš„}{1}<={2}{4}{3}{1->kia}",

		"{D-}[1]{1~2}{çš„}{VI}={4}{2}{3}{1-cÃ¡i}",
	"{D-}[1]{1~2}{çš„}{1}<={4}{2}{3}{1-cÃ¡i}",
	"{D-}[1]{:çš„}{VI}={3}{2}{1-cÃ¡i}",
	"{D-}[1]{:çš„}{1}<={3}{2}{1-cÃ¡i}",

		"{D}{1~2}{çš„}{VI}={1}{4}{2}{3}",
	"{D}{1~2}{çš„}{1}<={1}{4}{2}{3}",
	"{D}{:çš„}{VI}={1}{3}{2}",
	"{D}{:çš„}{1}<={1}{3}{2}",


	//		"{è¿™}{S}{D}{1~2}{çš„}{VI}={2}{3}{6}{4}{1->nÃ y}{5}",
	//	"{è¿™}{S}{D}{1~2}{çš„}{1}<={2}{3}{6}{4}{1->nÃ y}{5}",
	//	"{è¿™}{S}{D}{:çš„}{VI}={2}{3}{5}{4}{1->nÃ y}",
	//	"{è¿™}{S}{D}{:çš„}{1}<={2}{3}{5}{4}{1->nÃ y}",

			"{è¿™}{S}{D}{1~2}{çš„}{VI}={6}{2}{3}{4}{1->nÃ y}{5}",
	"{è¿™}{S}{D}{1~2}{çš„}{1}<={6}{2}{3}{4}{1->nÃ y}{5}",
	"{è¿™}{S}{D}{:çš„}{VI}={5}{2}{3}{4}{1->nÃ y}",
	"{è¿™}{S}{D}{:çš„}{1}<={5}{2}{3}{4}{1->nÃ y}",

		"{é‚£}{S}{D}{1~2}{çš„}{VI}={2}{3}{6}{4}{1->kia}{5}",
	"{é‚£}{S}{D}{1~2}{çš„}{1}<={2}{3}{6}{4}{1->kia}{5}",
	"{é‚£}{S}{D}{:çš„}{VI}={2}{3}{5}{4}{1->kia}",
	"{é‚£}{S}{D}{:çš„}{1}<={2}{3}{5}{4}{1->kia}",

		"{S}{D}{1~2}{çš„}{VI}={1}{2}{5}{3}{4}",
	"{S}{D}{1~2}{çš„}{1}<={1}{2}{5}{3}{4}",
	"{S}{D}{:çš„}{VI}={1}{2}{4}{3}",
	"{S}{D}{:çš„}{1}<={1}{2}{4}{3}",

			"{PN}{è¿™}{1~2}{çš„}{VI}={5}{3}{2->nÃ y cá»§a}{1:}{4}",
	"{PN}{è¿™}{1~2}{çš„}{1}<={5}{3}{2->nÃ y cá»§a}{1:}",
	"{PN}{è¿™}{:çš„}{VI}={4}{3}{2->nÃ y cá»§a}{1:}",
	"{PN}{è¿™}{:çš„}{1}<={4}{3}{2->nÃ y cá»§a}{1:}",

	"{è¿™}{1~2}{çš„}{VI}={4}{2}{1->nÃ y}{3}",
	"{è¿™}{1~2}{çš„}{1}<={4}{2}{1->nÃ y}{3}",
	"{è¿™}{:çš„}{VI}={3}{2}{1->nÃ y}",
	"{è¿™}{:çš„}{1}<={3}{2}{1->nÃ y}",


			"{PN}{é‚£}{1~2}{çš„}{VI}={5}{3}{2->kia cá»§a}{1:}{4}",
	"{PN}{é‚£}{1~2}{çš„}{1}<={5}{3}{2->kia cá»§a}{1:}",
	"{PN}{é‚£}{:çš„}{VI}={4}{3}{2->kia cá»§a}{1:}",
	"{PN}{é‚£}{:çš„}{1}<={4}{3}{2->kia cá»§a}{1:}",

		"{é‚£}{1~2}{çš„}{VI}={4}{2}{1->kia}{3}",
	"{é‚£}{1~2}{çš„}{1}<={4}{2}{1->kia}{3}",
	"{é‚£}{:çš„}{VI}={3}{2}{1->kia}",
	"{é‚£}{:çš„}{1}<={3}{2}{1->kia}",



	"åœ¨ 1~3 L1={1}{3-phÃ­a|bÃªn}{2}",

	"{è¿™}{SD}{VI}={2}{3}{1->nÃ y}",
	"{è¿™}{SD}{1}<={2}{3}{1->nÃ y}",
	"{é‚£}{SD}{VI}={2}{3}{1->kia}",
	"{é‚£}{SD}{1}<={2}{3}{1->kia}",

	"{è¿™}{S}{D}{VI}={2}{3}{4}{1->nÃ y}",
	"{è¿™}{S}{D}{1}<={2}{3}{4}{1->nÃ y}",
	"{é‚£}{S}{D}{VI}={2}{3}{4}{1->kia}",
	"{é‚£}{S}{D}{1}<={2}{3}{4}{1->kia}",

	"{è¿™}{D}{VI}={2}{3}{1->nÃ y}",
	"{è¿™}{D}{1}<={2}{3}{1->nÃ y}",
	"{é‚£}{D}{VI}={2}{3}{1->kia}",
	"{é‚£}{D}{1}<={2}{3}{1->kia}",

	"æœ‰ D ~ :çš„ 1 <={1}{2}{5}{3}{4}",
	"æœ‰ SD ~ :çš„ 1 <={1}{2}{5}{3}{4}",
	"æœ‰ ~ :çš„ 1 <={1}{4}{2}{3}",
	"æœ‰ ~ :çš„ 1 SW={1}{4}{2}{3}{5}",
	"ä¸ºä»€ä¹ˆ ~ :çš„ 1 SW={1->táº¡i sao}{4}{2:}{3:}{5:}",
	"ä»€ä¹ˆ ~ :çš„ 1 SW={1X}{4}{2}{3+gÃ¬}{5}",
	">{1}[trong|trÆ°á»›c|ngoÃ i|trÃªn|dÆ°á»›i|cáº¡nh]{çš„}{1}{SW}={3}{1}{4}",
	"{*L}[3,]{çš„}{1}{SW}={3}{1}{4}",
	"{SW}{1~3}{L}{çš„}{1~2}{SW}={1}{5}{3}{2}{6}",
	//SS
	"æ¯” 1~2 å¥½çš„={1->tá»‘t hÆ¡n}{2}",
	"æ¯” 1~2 å¥½çš„ 1 å¯ä»¥={4}{1->tá»‘t hÆ¡n}{2}{3X}{5}",
	"æ¯” 1~2 å¥½çš„ 1 <={4}{1->tá»‘t hÆ¡n}{2}",
	"æ¯” 1~2 è¿˜å¥½ 1 <={1->cÃ²n dá»…}{4+hÆ¡n}{2}",
	"æ¯” è¿™: è¿˜ 1={1->cÃ²n}{4+hÆ¡n}{2}",
	"æ¯” è¿™ 1 è¿˜ 1={1->cÃ²n}{5+hÆ¡n}{3}{2->nÃ y}",
	"æ¯” 1~2 :äº† ä¸å°‘={1X}{3+hÆ¡n}{2}{4->khÃ´ng Ã­t}",
	"æ¯” {PN} 1 äº†={3+hÆ¡n}{2}",
	"SD 1~5 ä¸€èˆ¬çš„ 1={1}{4}{2}",
	"D 1~5 ä¸€èˆ¬çš„ 1={1}{4}{2}",
	//FV

	"@_çš„:0{è¿™:çš„}[4,10]{*L}[trong|trÆ°á»›c|ngoÃ i|trÃªn|dÆ°á»›i|cáº¡nh]{1}={2:}{1:}",
	"@_çš„:0{é‚£:çš„}[kia|Ä‘Ã³]{1}<={2+cá»§a}{1}",
	"@_çš„:0>{:çš„}[trong|trÆ°á»›c|ngoÃ i|trÃªn|dÆ°á»›i|cáº¡nh]{1}{SW}={2}{1}{3}",
	//"@_çš„:0{å†:çš„}[4,5]{1}<={2:}{1:}",
	//"@_çš„:0{å†:çš„}[4,5]{1}{VI}={2:}{1:}{3}",
	//MV
	"å°† PN 1 <={3}{2}{1_X}",
	"{è¿™}{PN}{L}={3}{2}{1->nÃ y}",
	"{é‚£}{PN}{L}={3}{2}{1->kia}",
	"{è¿™}{PN}={2}{1->nÃ y}",
	"{é‚£}{PN}={2}{1->kia}",
	"é‚£ 1~3 L={3}{2}{1->kia}",
	//"é‚£ 1~3 SW={2}{1->kia}{3}",
	"è¿™ 1~3 L={3}{2}{1->nÃ y}",
	"{è¿™} {1}[:n] {SW}={2}{1->nÃ y}{3}",
	"{è¿™} {1}[:n] {1}[:n] {SW}={2}{1->nÃ y}{3}",
	"{è¿™} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {1}[:n]={3}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:n] {SW}={2}{1->nÃ y}{3}",
		"{è¿™ä¸ª} {1}[:n] {1}[:n] {SW}={2}{1->nÃ y}{3}",
		"{è¿™ä¸ª} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {1}[:n]={3}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->nÃ y}",
		"{è¿™} {1}[:n] {SW}={2}{1->nÃ y}{3}",
	"{é‚£} {1}[:n] {1}[:n] {SW}={2}{1->kia}{3}",
	"{é‚£} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {1}[:n]={3}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:n] {SW}={2}{1->kia}{3}",
		"{é‚£ä¸ª} {1}[:n] {1}[:n] {SW}={2}{1->kia}{3}",
		"{é‚£ä¸ª} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {1}[:n]={3}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->kia}"
];
meanengine.db.cdefault=[
	"> {1} {~} {:çš„} {1}[:n,np,vp,v,m,ns]<={4}{1}{2}{3}",
	"@_çš„:0{è¿™:çš„}[4,10]{*L}[trong|trÆ°á»›c|ngoÃ i|trÃªn|dÆ°á»›i|cáº¡nh]{1}={2:}{1:}",
	"@_çš„:0{é‚£:çš„}[kia|Ä‘Ã³]{1}<={2+cá»§a}{1}",
	"@_çš„:0>{:çš„}[trong|trÆ°á»›c|ngoÃ i|trÃªn|dÆ°á»›i|cáº¡nh]{1}{SW}={2}{1}{3}",
	//"@_çš„:0{å†:çš„}[4,5]{1}<={2:}{1:}",
	//"@_çš„:0{å†:çš„}[4,5]{1}{VI}={2:}{1:}{3}",
	//MV
	"å°† PN 1 <={3}{2}{1_X}",
	"{è¿™}{PN}{L}={3}{2}{1->nÃ y}",
	"{é‚£}{PN}{L}={3}{2}{1->kia}",
	"{è¿™}{PN}={2}{1->nÃ y}",
	"{é‚£}{PN}={2}{1->kia}",
	"é‚£ 1~3 L={3}{2}{1->kia}",
	//"é‚£ 1~3 SW={2}{1->kia}{3}",
	"è¿™ 1~3 L={3}{2}{1->nÃ y}",
	"{è¿™} {1}[:n] {SW}={2}{1->nÃ y}{3}",
	"{è¿™} {1}[:n] {1}[:n] {SW}={2}{1->nÃ y}{3}",
	"{è¿™} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {1}[:n]={3}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
	"{è¿™} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:n] {SW}={2}{1->nÃ y}{3}",
		"{è¿™ä¸ª} {1}[:n] {1}[:n] {SW}={2}{1->nÃ y}{3}",
		"{è¿™ä¸ª} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {1}[:n]={3}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->nÃ y}",
		"{è¿™ä¸ª} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->nÃ y}",
		"{è¿™} {1}[:n] {SW}={2}{1->nÃ y}{3}",
	"{é‚£} {1}[:n] {1}[:n] {SW}={2}{1->kia}{3}",
	"{é‚£} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {1}[:n]={3}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->kia}",
	"{é‚£} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:n] {SW}={2}{1->kia}{3}",
		"{é‚£ä¸ª} {1}[:n] {1}[:n] {SW}={2}{1->kia}{3}",
		"{é‚£ä¸ª} {1}[:i,a] {VI}[:n] {1}[:n]={4}{3}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {1}[:n] {VI}[:n]={4}{3}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {1}[:n] {1}[:n]={3}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {1}[:n]={3}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {VI}[:n] {1}[:n]={5}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {1}[:n] {VI}[:n]={5}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {1}[:n] {1}[:n]={5}{4}{2}{1->kia}",
		"{é‚£ä¸ª} {1}[:i,a] {çš„} {1}[:n]={4}{2}{1->kia}",
		"{PN} {1}{çš„} {1}[:v]={1}{2}{3->mÃ }{4}",
	"{PN} {1}[:v]{çš„} {1}[:n] {1}[:n]<={5}{4}{1}{2}",
	"{PN} {1}[:v]{çš„} {1}[:n]<={4}{1}{2}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n] {1}[:n]<={5}{4}{2}{1}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n]<={4}{2}{1}",
	"{PN} {1}[:v]{çš„} {1}[:n] {1}[:n] {SW}={5}{4}{1}{2}{6}",
	"{PN} {1}[:v]{çš„} {1}[:n] {SW}={4}{1}{2}{5}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n] {1}[:n] {SW}={5}{4}{2}{1}{6}",
	"{PN} {1}[:n,a,i,m]{çš„} {1}[:n] {SW}={4}{2}{1}{5}",
	"{PN} {çš„} {1}[^trong|ngoÃ i|trÃªn|dÆ°á»›i]={3+cá»§a}{1}",
	"{PN} {çš„} {1} {1}[^trong|ngoÃ i|trÃªn|dÆ°á»›i]={4}{3+cá»§a}{1}",
	//">{PN} {1}{çš„} {1}<={4}{2+cá»§a}{1}",
	//">{PN} {1}[:v]{çš„} {1} {SW}={4}{1}{2}{5}",
	//">{PN} {1}{çš„} {1} {SW}={4}{2+cá»§a}{1}{5}",

	"@_çš„:1>{PN} {:çš„}[:v] {1}[nÃ y]<={3-nÃ y}{1}{2+nÃ y}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[:v]<={1}{2}{3}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[:n]<={3}{1}{2}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:c]<={1}{2}{3}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:v]<={1}{3}{2}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}<={3}{2+cá»§a}{1}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[nÃ y] {SW}={3-nÃ y}{1}{2+nÃ y}{4}",
	"@_çš„:1>{PN} {:çš„}[:v] {1}[:n] {SW}={3}{1}{2}{4}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:n] {SW}={3}{2+cá»§a}{1}{4}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:n]<={3}{2+cá»§a}{1}",
	"@_çš„:1>{PN} {:çš„}[3,] {1}[:n] {SW}={3}{2+cá»§a}{1}{4}",


	//"{:æ˜¯} {1} {PN} {PN} {çš„} {1} <={1}{2}{6+cá»§a}{5_X}{3}{4}",

	//"{:æ˜¯} {1} {PN} {çš„} {1} <={1}{2}{5+cá»§a}{4_X}{3}",
	//"{:æ˜¯} {1} {t:F} {çš„} {1} <={1}{2}{5+cá»§a}{4_X}{3}",
	//"{PN} {åœ¨} {~} {1}[:v] {~}<={1}{4}{5}{2}{3}",
	///"{PN} {åœ¨} {t:F} {~}<={1}{4}{2}{3}",

		"{:è¿™} {PN} {çš„} {1} <={4}{2}{3_X}{1->nÃ y}",
	"{è¿™} {PN} {:çš„} {1} <={4}{2}{3_X}{1->nÃ y}",
	"{è¿™} {:çš„} {1} <={3}{2}{1->nÃ y}",
	"{:è¿™} {PN} {PN} {çš„} {1} <={5}{4_X}{3}{2}{1->nÃ y}",
	//"{:è¿™} {1} {PN} {PN} {çš„} {1} <={2}{6}{5_X}{3}{4}{1->nÃ y}",

	"{:è¿™} {1} {PN} {çš„} {1} <={1}{2}{5}{4_X}{3}",
	"{:è¿™} {1} {t:F} {çš„} {1} <={1}{2}{5}{4_X}{3}",



	"{è¢«:åœ¨} {0~1} {L} {çš„} {1} <={5}{1}{2}{3}{4_X}",
	"{è¢«:} {~} {:åœ¨} {~} {L} {çš„} {1} <={7}{1}{2}{3}{4}{5}{6}",


		//"{è¿™}{SD}{1~2}[:n]{çš„}{1}[:n]={2}{5}{3}{1->nÃ y}{4}",
		//"{è¿™}{SD}{1~2}[:a]{çš„}{1}[:n]={2}{5}{3}{1->nÃ y}{4}",
		//"{è¿™}{SD}{1~2}{çš„}{VI}={2}{5}{3}{1->nÃ y}{4}",
	//"{è¿™}{SD}{1~2}{çš„}{1}<={2}{5}{3}{1->nÃ y}{4}",
	//"{è¿™}{SD}{:çš„}{VI}={2}{4}{3}{1->nÃ y}",
	//"{è¿™}{SD}{:çš„}{1}<={2}{4}{3}{1->nÃ y}",

		"{è¿™}{SD}{1~2}{çš„}{VI}={5}{2}{3}{1->nÃ y}{4}",
	"{è¿™}{SD}{1~2}{çš„}{1}<={5}{2}{3}{1->nÃ y}{4}",
	"{è¿™}{SD}{:çš„}{VI}={4}{2}{3}{1->nÃ y}",
	"{è¿™}{SD}{:çš„}{1}<={4}{2}{3}{1->nÃ y}",

		"{é‚£}{SD}{1~2}{çš„}{VI}={2}{5}{3}{1->kia}{4}",
	"{é‚£}{SD}{1~2}{çš„}{1}<={2}{5}{3}{1->kia}{4}",
	"{é‚£}{SD}{:çš„}{VI}={2}{4}{3}{1->kia}",
	"{é‚£}{SD}{:çš„}{1}<={2}{4}{3}{1->kia}",

	"{SD}{1~2}{çš„}{VI}={1}{4}{2}{3}",
	"{SD}{1~2}{çš„}{1}<={1}{4}{2}{3}",
	"{SD}{:çš„}{VI}={1}{3}{2}",
	"{SD}{:çš„}{1}<={1}{3}{2}",

	//	"@_çš„:2{SD}{1~2}{:çš„}{VI}={1}{4}{2}{3}",
	//	"@_çš„:2{SD}{1~2}{:çš„}{1}<={1}{4}{2}{3}",
	//	"@_çš„:1{SD}{:çš„}{VI}={1}{3}{2}",
	//	"@_çš„:1{SD}{:çš„}{1}<={1}{3}{2}",

		"{è¿™}{D}{1~2}{çš„}{VI}={2}{5}{3}{1->nÃ y}{4}",
	"{è¿™}{D}{1~2}{çš„}{1}<={2}{5}{3}{1->nÃ y}{4}",
	"{è¿™}{D}{:çš„}{VI}={2}{4}{3}{1->nÃ y}",
	"{è¿™}{D}{:çš„}{1}<={2}{4}{3}{1->nÃ y}",

		"{é‚£}{D}{1~2}{çš„}{VI}={2}{5}{3}{1->kia}{4}",
	"{é‚£}{D}{1~2}{çš„}{1}<={2}{5}{3}{1->kia}{4}",
	"{é‚£}{D}{:çš„}{VI}={2}{4}{3}{1->kia}",
	"{é‚£}{D}{:çš„}{1}<={2}{4}{3}{1->kia}",

		"{D-}[1]{1~2}{çš„}{VI}={4}{2}{3}{1-cÃ¡i}",
	"{D-}[1]{1~2}{çš„}{1}<={4}{2}{3}{1-cÃ¡i}",
	"{D-}[1]{:çš„}{VI}={3}{2}{1-cÃ¡i}",
	"{D-}[1]{:çš„}{1}<={3}{2}{1-cÃ¡i}",

		"{D}{1~2}{çš„}{VI}={1}{4}{2}{3}",
	"{D}{1~2}{çš„}{1}<={1}{4}{2}{3}",
	"{D}{:çš„}{VI}={1}{3}{2}",
	"{D}{:çš„}{1}<={1}{3}{2}",


	//		"{è¿™}{S}{D}{1~2}{çš„}{VI}={2}{3}{6}{4}{1->nÃ y}{5}",
	//	"{è¿™}{S}{D}{1~2}{çš„}{1}<={2}{3}{6}{4}{1->nÃ y}{5}",
	//	"{è¿™}{S}{D}{:çš„}{VI}={2}{3}{5}{4}{1->nÃ y}",
	//	"{è¿™}{S}{D}{:çš„}{1}<={2}{3}{5}{4}{1->nÃ y}",

			"{è¿™}{S}{D}{1~2}{çš„}{VI}={6}{2}{3}{4}{1->nÃ y}{5}",
	"{è¿™}{S}{D}{1~2}{çš„}{1}<={6}{2}{3}{4}{1->nÃ y}{5}",
	"{è¿™}{S}{D}{:çš„}{VI}={5}{2}{3}{4}{1->nÃ y}",
	"{è¿™}{S}{D}{:çš„}{1}<={5}{2}{3}{4}{1->nÃ y}",

		"{é‚£}{S}{D}{1~2}{çš„}{VI}={2}{3}{6}{4}{1->kia}{5}",
	"{é‚£}{S}{D}{1~2}{çš„}{1}<={2}{3}{6}{4}{1->kia}{5}",
	"{é‚£}{S}{D}{:çš„}{VI}={2}{3}{5}{4}{1->kia}",
	"{é‚£}{S}{D}{:çš„}{1}<={2}{3}{5}{4}{1->kia}",

		"{S}{D}{1~2}{çš„}{VI}={1}{2}{5}{3}{4}",
	"{S}{D}{1~2}{çš„}{1}<={1}{2}{5}{3}{4}",
	"{S}{D}{:çš„}{VI}={1}{2}{4}{3}",
	"{S}{D}{:çš„}{1}<={1}{2}{4}{3}",

			"{PN}{è¿™}{1~2}{çš„}{VI}={5}{3}{2->nÃ y cá»§a}{1:}{4}",
	"{PN}{è¿™}{1~2}{çš„}{1}<={5}{3}{2->nÃ y cá»§a}{1:}",
	"{PN}{è¿™}{:çš„}{VI}={4}{3}{2->nÃ y cá»§a}{1:}",
	"{PN}{è¿™}{:çš„}{1}<={4}{3}{2->nÃ y cá»§a}{1:}",

	"{è¿™}{1~2}{çš„}{VI}={4}{2}{1->nÃ y}{3}",
	"{è¿™}{1~2}{çš„}{1}<={4}{2}{1->nÃ y}{3}",
	"{è¿™}{:çš„}{VI}={3}{2}{1->nÃ y}",
	"{è¿™}{:çš„}{1}<={3}{2}{1->nÃ y}",


			"{PN}{é‚£}{1~2}{çš„}{VI}={5}{3}{2->kia cá»§a}{1:}{4}",
	"{PN}{é‚£}{1~2}{çš„}{1}<={5}{3}{2->kia cá»§a}{1:}",
	"{PN}{é‚£}{:çš„}{VI}={4}{3}{2->kia cá»§a}{1:}",
	"{PN}{é‚£}{:çš„}{1}<={4}{3}{2->kia cá»§a}{1:}",

		"{é‚£}{1~2}{çš„}{VI}={4}{2}{1->kia}{3}",
	"{é‚£}{1~2}{çš„}{1}<={4}{2}{1->kia}{3}",
	"{é‚£}{:çš„}{VI}={3}{2}{1->kia}",
	"{é‚£}{:çš„}{1}<={3}{2}{1->kia}",
	">{PN}{çš„}{1}<={3+cá»§a}{1:}{2_X}",
	">{1}[:c,a]{PN}{çš„}{1}<={1}{4+cá»§a}{2:}{3_X}",
	">{PN}{çš„}{1}[:n]{1}[:v,d,ad,p,u]={3+cá»§a}{1:}{4}",
	">{PN}{çš„}{1}{è¢«:}={3+cá»§a}{1}{4:}{2_X}",
	"{PN}{çš„}{1}{*å’Œ}{PN}{çš„}{1}={3+cá»§a}{1}{4->vÃ }{7+cá»§a}{5}",
];
meanengine.db.tokenfind={
	"deter":arrtoobj(["è¿™","è¿™ä¸ª","é‚£","é‚£ä¸ª","æŠŠ","èˆ¬","ç­","ç“£","ç£…","å¸®","åŒ…","è¾ˆ","æ¯","æœ¬","ç¬”","æŸ„","æ­¤","è¿™äº›","é‚£äº›","äº›"
		,"æ‹¨","éƒ¨","é¤","å†Œ","å±‚","åœº","åœº","æˆ","å°º","é‡","å‡º","å¤„","ä¸²","å¹¢","ç°‡","æ’®","æ‰“"
		,"è¢‹","ä»£","æ‹…","æ¡£","é“","æ»´","ç‚¹","é¡¶","æ ‹","å µ","åº¦","ç«¯","æ®µ","å¯¹","å †","é˜Ÿ","é¡¿"
		,"å¨","æœµ","å‘","ç•ª","æ–¹","åˆ†","ä»½","å°","å³°","ä»˜","å¹…","å‰¯","æœ","æ†","ä¸ª","æ ¹","å…¬"
		,"å°º","å…¬","åˆ†","å…¬","æ–¤","å…¬","é‡Œ","å…¬","é¡·","å…¬","å‡","è‚¡","æŒ‚","ç®¡","è¡Œ","ç›’","æˆ·"
		,"å£¶","ä¼™","è®°","çº§","å‰‚","æž¶","å®¶","åŠ ","ä»‘","ä»¶","é—´","ç»ž","è§’","å±Š","æˆª","èŠ‚","æ–¤"
		,"èŒŽ","å±€","å…·","å¥","å±…","å·","åœˆ","å¡","å®¢","æ£µ","é¢—","å…‹","å­”","å£","å—","æ†","ç±»"
		,"é‡Œ","ç²’","è¾†","ä¸¤","åˆ—","ç«‹","æ–¹","è‹±","å°º","ç«‹","æ–¹","ç±³","é¢†","ç¼•","è½®","æ‘ž","æ¯›"
		,"æžš","é—¨","ç±³","é¢","ç§’","å","äº©","å¹•","æŽ’","æ´¾","ç›˜","æ³¡","å–·","ç›†","åŒ¹","æ‰¹","ç‰‡"
		,"ç¯‡","æ’‡","ç“¶","å¹³","æ–¹","å…¬","é‡Œ","æœŸ","èµ·","çˆ¿","åƒ","å…‹","ç“¦","é¡·","æ›²","åœˆ"
		,"ç¾¤","å·¥","æ‰‡","å‹º","èº«","å‡","æ‰‹","é¦–","æŸ","åŒ","ä¸","è‰˜","æ‰€","å°","æ‘Š","æ»©"
		,"è¶Ÿ","å ‚","å¥—","å¤©","æ¡","æŒ‘","è´´","æŒº","ç­’","æ¡¶","é€š","å¤´","å›¢","å¨","ä¸¸","ç¢—","ä½"
		,"å°¾","å‘³","çª","å¸­","çº¿","ç®±","é¡¹","äº›","ç‰™","çœ¼","æ ·","é¡µ","è‹±","äº©","å‘˜","å…ƒ","åˆ™"
		,"ç›","ä¸ˆ","ç« ","å¼ ","é˜µ","æ”¯","æž","åª","ç§","è½´","æ ª","å¹¢","æ¡©","æ¡Œ","å®—","ç»„","å°Š","åº§","å£°"]),
	"deter-":["è¿™","è¿™ä¸ª","é‚£","é‚£ä¸ª","æ­¤","è¿™äº›","é‚£äº›"],
	"locat":["é‡Œ","åŽ","ä¸­","å†…","é—´","å‰","ä¸Š","ä¸‹","å·¦","å³","å¤–","è¾¹"
			,"ä¹‹ä¸­","ä¹‹å†…","ä¹‹é—´","ä¹‹å‰","ä¹‹ä¸Š","ä¹‹ä¸‹","ä¹‹å¤–"
			,"é‡Œé¢","å†…é¢","ä¸Šé¢","ä¸‹é¢"],
	"locat1":["ä¸Š","ä¸‹","ä¹‹ä¸Š","ä¹‹ä¸‹"],
	"locat2":["é‡Œ","ä¸­","å†…","é—´","å¤–","ä¹‹ä¸­","ä¹‹å†…","ä¹‹é—´","ä¹‹å¤–"],
	"subw":["åˆ°","åœ¨","ä»Ž","è‡ª","ç”±","äºŽ"],
	"relv":["çš„","å¾—","äº†"],
	"relv1":["çš„"],
	"relv2":["å¾—"],
	"relv3":["äº†"],
	"cc":["è€Œåˆ","ä¸Ž","è·Ÿ","å’Œ"],
	"stwd":arrtoobj([
		"åº”","è¿˜","æ‰","åœ¨","å¯","ä¸º","å°±","å·²","è¦","æ˜¯","ä¹Ÿ","åˆ°","å±…","è¢«","åˆ°","ä»Ž"
		]),
	"pronoun":arrtoobj(["äºº","ä»–è‡ªå·±","æˆ‘","ä½ ","æ‚¨","ä»–","å¥¹","å®ƒ","å¤§å®¶","å¤§äºº","å®ƒä»¬","å¥¹ä»¬","ä»–ä»¬","ä½ ä»¬","æˆ‘ä»¬","ä¸ˆå¤«","äº²å®¶å…¬","äº²å®¶æ¯","ä¼¯ä¼¯"
		,"ä¼¯æ¯","ä¼¯çˆ¶","ä¾„å¥³","ä¾„å­","å„¿å­","å…„å¼Ÿ","å…¬å…¬","å”å”","è¡¨å¦¹","è¡¨å§","è¡¨å¼Ÿ","é˜¿å§¨"
		,"å”çˆ¶","åŽå¦ˆ","å“¥å“¥","å ‚å…„","å ‚å“¥","å ‚å¦¹","å ‚å§","å ‚å¼Ÿ","å¤–å…¬","å¤–å©†","å¤–å­™","å¤–å­™å¥³","å¤–ç”¥"
		,"å¤–ç”¥å¥³","å¤ªå¤ª","å¤ªå§¥å§¥","å¤ªå§¥çˆ·","å¤ªçˆ·","å¥³å„¿","å¥³å©¿","å¥¶å¥¶","å¦ˆå¦ˆ","å¦¹","å¦¹å¤«","å¦¹å¦¹","å¦»å­"
		,"å§","å§å¤«","å§å¦¹","å§å§","å§‘å¤«","å§‘å¦ˆ","å§‘å§‘","å§‘çˆ¶","å§¨ä¾„","å§¨ä¾„å¥³","å§¨å¤«","å§¨å¦ˆ","å§¨çˆ¶","å§ªå¥³"
		,"å§ªå­","å©†å©†","å©¶å©¶","åª³å¦‡","å«‚å«‚","å­™å¥³","å­™å­","å²³æ¯","å²³çˆ¶","å¼Ÿ","å¼Ÿåª³","å¼Ÿå¼Ÿ","æ¯äº²","çˆ¶äº²"
		,"çˆ·çˆ·","çˆ¸çˆ¸","ç‹¬ç”Ÿå¥³","ç‹¬ç”Ÿå­","ç»§æ¯","ç»§çˆ¶","è€å…¬","è€å©†","èˆ…ä¾„","èˆ…ä¾„å¥³","èˆ…å¦ˆ","èˆ…èˆ…","è¡¨å“¥"
		,"ä¸‡å²","ä¸‡å²çˆ·","ä¸‹å®˜","ä¸ä½ž","ä¸æ‰","ä¸è‚–","ä¸è°·","ä¸»æ•™","äºˆä¸€äºº","äººå®¶","ä»å…„","ä»å…¬"
		,"ä»™å§‘","ä»¤å…„","ä»¤åƒé‡‘","ä»¤å ‚","ä»¤å°Š","ä»¤çˆ±","ä»¤éƒŽ","ä»¤é˜ƒ","ä¿®å£«","å„¿è‡£","å…ˆå¸","å…ˆç”Ÿ","å…ˆè´¤","å…¬å­"
		,"å†°ç¿","å‰è¾ˆ","åŒ»ç”Ÿ","åƒå²","å‘ä¸‹","å‘èŒ","åšå£«","å¿","å°ç«¯","åŒå¿—","å“€å®¶","åœ£ä¸Š","åœ£é©¾","åœ¨ä¸‹","å¤§äºº"
		,"å¤§å¤«","å¤©å­","å¤ªåŽ","å¤«äºº","å¤«å›","å¥³å£«","å¥´å©¢","å¥´å®¶","å¥´æ‰","å¦¾","å¦¾èº«","å§‘å¨˜","å¨˜å¨˜","å©¢","å©¢å¥³"
		,"å­¤","å­¤çŽ‹","å­ºäºº","å®˜äºº","å¯’èˆ","å¯¡","å¯¡äºº","å°Šä¸Š","å°Šäº²","å°Šå…¬","å°Šå ‚","å°Šå¤«äºº","å°Šé©¾"
		,"å°äºº","å°å„¿","å°å","å°å¥³","å°å¥³å­","å°å§","å°ç”Ÿ","å±…å£«","å±žä¸‹","å¸ˆå‚…","å¸ˆçˆ¶","åºœä¸Š","æ„š","æ‰§å£«"
		,"æ‹™å¤«","æ‹™è†","æ•™å®—","æ•äºº","æ˜¾å¦£","æ˜¾è€ƒ","æ™šå­¦","æ™šç”Ÿ","æ™šè¾ˆ","æœ•","æœ«å®˜","æœ«å°†","æœ¬äºº","æœ¬å®˜","æœ¬å®«"
		,"æœ¬å°†å†›","æœ¬å¸…","æœ¬åºœ","æœ¬çŽ‹","æ®¿ä¸‹","æ¯åŽ","æ°‘å¥³","æ³•å¸ˆ","çˆµå£«","çˆ¶å›","çˆ¶å¸","çˆ¶çŽ‹","çˆ¶çš‡","ç‰§å¸ˆ"
		,"çŠ¬å­","çš‡å¸","ç›¸å…¬","ç¥–å¦£","ç¥–è€ƒ","ç¥žçˆ¶","çªƒ","ç»ç†","è€å¤«","è€å¸ˆ","è€æ‹™","è€æœ½","è€æ±‰","è€ç²—","è€è¡²"
		,"è€èº«","è‡£","è‡£å¦¾","èŠ‚ä¸‹","è‰æ°‘","è´¤ä¹”æ¢“","è´¤ä¼‰ä¿ª","è´¤ä¾„","è´¤å¦»","è´¤å®¶","è´¤å¼Ÿ","è´¤æ˜†ä»²","è´¤æ˜†çŽ‰","è´¤éƒŽ"
		,"è´«åƒ§","è´«å°¼","è´«é“","è´±å†…","è´±å¦¾","è´±æ¯","è´µä¸ˆå¤«","è´µå…¬å¸","è´µå›½","è´µå¤«äºº","è´µå§“","è´µå­å¥³","è´µå­å¼Ÿ"
		,"è´µå®å·","è´µå®¶é•¿","è´µåºš","è´µåºœ","é“é•¿","éƒŽå›","é„™äºº","é˜ä¸‹","é™›ä¸‹","é«˜å ‚","éº¾ä¸‹"])
}
meanengine.matcher=function(find,node,passed){
	if(find.modifier){
		if(!meanengine.modifier(node,find.modifier)){
			return false;
		}
	}
	if(find.type=="extend"){
		if(find.isfirst){
			return !node.isspace(false);
		}
		if(find.islast){
			return !node.isspace(true);
		}
		return true;
	}
	if(find.type=="exact"){
		return node.gT()==find.word;
	}
	if(find.type in meanengine.db.tokenfind){
		return meanengine.db.tokenfind[find.type].indexOf(node.gT()) >= 0;
	}
	if(find.type=="lastlocat"){
		var t = node.gT();
		if(t.lastChar()=="çš„" && t.length > 1){
			return meanengine.db.tokenfind.locat.indexOf(t[t.length-2]) >= 0;
		}else
		return meanengine.db.tokenfind.locat.indexOf(t.lastChar()) >= 0;
	}
	if(find.type=="name"){
		return node.containName();
	}
	if(find.type=="proname"){
		if(node.containName() || meanengine.db.tokenfind.pronoun.indexOf(node.gT()) >= 0){
			return true;
		}
		return false;
	}
	if(find.type=="number"){
		return meanstrategy.containnumber(node);
	}
	if(find.type=="faction"){
		return meanengine.wordIsFaction(node,passed);
	}
	if(find.type=="havechar"){
		var a=node.gT();
		for(var i=0;i<a.length;i++){
			if(find.char.indexOf(a[i])>=0){
				return true;
			}
		}
		return false;
	}
	if(find.type=="haveword"){
		return node.gT().indexOf(find.word)>=0;
	}
	if(find.type=="lastword"){
		return node.gT().indexOf(find.word, node.gT().length - find.word.length) !== -1;
	}
	if(find.type=="stw"){
		//if(!node.isspace(true)){
		//	return true;
		//}
		var a=node.gT();
		for(var i=0;i<a.length;i++){
			if(meanengine.db.tokenfind.stwd.indexOf(a[i]) >= 0){
				return true;
			}
		}
		return false;
	}
	if(find.type=="firstlast"){
		return (node.gT().indexOf(find.word1) === 0) 
			&& (node.gT().indexOf(find.word2, node.gT().length - find.word2.length) !== -1);
	}
	if(find.type=="firstword"){
		return node.gT().indexOf(find.word) === 0;
	}
	if(find.type=="numdeter"){
		return meanstrategy.containnumber(node) && meanengine.db.tokenfind["deter"].indexOf(node.gT().lastChar()) >= 0;
	}
	if(find.type=="tviet"){
		var m=node.getAttribute("v");
		if(m){
			m=m.toLowerCase().split("/");
			var h = node.gH();
			if(h==""){
				return false;
			}
			var hc = 0;
			for(var c=0;c<m.length;c++){
				if(h == m[c]){
					hc++;
				}
			}
			return hc/m.length < 0.4;
		}
	}
	return false;
}
meanengine.modifier=function(node,mod){
	if(mod.type == "have"){
		//if(node.textContent.contain(mod.text)){
		//	return true;
		//}else {
		//	return false;
		//}
		return new RegExp(mod.text).test(node.textContent);
	}
	if(mod.type=="length"){
		var l = node.gT().length;
		if(l> mod.max || l<mod.min){
			return false;
		}
		return true;
	}
	if(mod.type=="pos"){
		var pl = mod.postype.split(",");
		var np = node.getAttribute("p");
		for(var i=0;i<pl.length;i++){
			if(pl[i] == np){
				return true;
			}
		}
		return false;
	}
}
meanengine.finder = function(tofind,step,dir,node,b){
	var ndin=[];
	if(step.type=="unlim"){
		step.max=999;
		step.min=0;
	}
	var grp = {};
	if(dir){
		for(var i=0;i<=step.max;i++){
			node=node.nE();
			if(node==null || !node.isspace(false) || this.isrbound(node,b))return false;
			if(i<step.min){
				if(step.modifier){
					if(!this.modifier(node,step.modifier)){
						return false;
					}
				}
				ndin.push(node);
				continue;
			}
			if(meanengine.matcher(tofind,node,grp)){
				return {
					ins: ndin,
					found: grp.grp||node
				};
			}
			ndin.push(node);
		}
	}else{
		for(var i=0;i<=step.max;i++){
			node=node.pE();
			if(node==null || !node.isspace(true) || this.islbound(node,b))return false;
			if(i<step.min){
				if(step.modifier){
					if(!this.modifier(node,step.modifier)){
						return false;
					}
				}
				ndin.unshift(node);
				continue;
			}
			if(meanengine.matcher(tofind,node,grp)){
				return {
					ins: ndin,
					found: grp.grp||node
				};
			}
			ndin.unshift(node);
		}
	}
	return false;
}
meanengine.findend = function(step,dir,node,bound){
	var ndin=[];
	if(step.type=="unlim"){
		step.max=999;
		step.min=0;
	}
	if(dir){
		for(var i=0;i<=step.max;i++){
			node=node.nE();
			if(node==null||!node.isspace(false))return i>=step.min ? ndin : false;
			if(step.modifier){
				if(!this.modifier(node,step.modifier)){
					return i>=step.min ? ndin : false;
				}
			}
			ndin.push(node);
			continue;
		}
	}else{
		for(var i=0;i<=step.max;i++){
			node=node.pE();
			if(node==null||!node.isspace(true))return i>=step.min ? ndin : false;
			if(step.modifier){
				if(!this.modifier(node,step.modifier)){
					return i>=step.min ? ndin : false;
				}
			}
			ndin.unshift(node);
		}
	}
	return false;
}
meanengine.findmax = function(step,dir,node){
	var ndin=[];
	if(step.type=="unlim"){
		step.max=999;
		step.min=0;
	}
	if(dir){
		for(var i=0;i<=step.max;i++){
			node=node.nE();
			if(node==null||!node.isspace(false)||i==step.min)return i>=step.min ? ndin : false;
			if(step.modifier){
				if(!this.modifier(node,step.modifier)){
					return i>=step.min ? ndin : false;
				}
			}
			ndin.push(node);
		}
	}else{
		for(var i=0;i<=step.max;i++){
			node=node.pE();
			if(node==null||!node.isspace(true)||i==step.min)return i>=step.min ? ndin : false;
			if(step.modifier){
				if(!this.modifier(node,step.modifier)){
					return i>=step.min ? ndin : false;
				}
			}
			ndin.unshift(node);
		}
	}
	return false;
}
meanengine.swapper = function(froms,tos){
	var ctn =froms[0].parentElement || froms[0][0].parentElement;
	var ida,idb;
	//for(var lo = 0;lo<froms.length;lo++)
	for(var i=0;i<froms.length;i++){
		idb=tos[i].id||tos[i][0].id;
		ida=froms[i].id||froms[i][0].id;
		if(ida != idb){
			//console.log("transform: "+ida + " - "+idb)
			if(froms[i].push){
				if(tos[i].push){
					for(var j=0;j<tos[i].length;j++){
						ctn.insertBefore(document.createTextNode(" "), froms[i][0]);
						ctn.insertBefore(tos[i][j], froms[i][0]);
						//meanengine.swapgt(tos[i][j], froms[i][0]);
						//meanengine.swapm(tos[i][j], froms[i][0]);
					}
				}else{
					ctn.insertBefore(document.createTextNode(" "), froms[i][0]);
					ctn.insertBefore(tos[i], froms[i][0]);
					//meanengine.swapgt(tos[i], froms[i][0]);
					//meanengine.swapm(tos[i], froms[i][0]);
				}
			}else{
				if(tos[i].push){
					for(var j=0;j<tos[i].length;j++){
						ctn.insertBefore(document.createTextNode(" "), froms[i]);
						ctn.insertBefore(tos[i][j], froms[i]);
						//meanengine.swapgt(tos[i][j], froms[i]);
						//meanengine.swapm(tos[i][j], froms[i]);
					}
				}else{
					ctn.insertBefore(document.createTextNode(" "), froms[i]);
					ctn.insertBefore(tos[i], froms[i]);
					//meanengine.swapgt(tos[i], froms[i]);
					//meanengine.swapm(tos[i], froms[i]);
				}
			}
			//meanengine.swapnode(froms[i],tos[i]);
			if(i<froms.length-1){
				var tmp=froms[i];
					froms[i]=froms[i+1];
					froms[i+1]=tmp;
					if(froms[i+1].push){
						if(froms[i+1][0].previousSibling&&froms[i+1][0].previousSibling.nodeType!=3){
							ctn.insertBefore(document.createTextNode(" "), froms[i+1][0]);
						}
					}else
					if(froms[i+1].previousSibling&&froms[i+1].previousSibling.nodeType!=3){
						ctn.insertBefore(document.createTextNode(" "), froms[i+1]);
					}
			}
		}
	}
	if(tos[0].push){
		tos[0][0].tomean(tos[0][0].textContent);
	}else
	tos[0].tomean(tos[0].innerHTML);
}
meanengine.swapper2 = function(froms,tos){
	var flag = false;
	for(var i=0;i<froms.length;i++){
		if(tos[i] != froms[i]){
			flag = true;
			break;
		}
	}
	if(!flag){
		return;
	}
	var ctn =froms[0].parentElement || froms[0][0].parentElement;
	if(!ctn)return;
	var lastn = froms[froms.length - 1].nextSibling;
	for(var i=0;i<froms.length;i++){
		if(froms[i].push){
			for(var j=0;j<froms[i].length;j++){
				if(froms[i][j].isspace(false)){
					froms[i][j].previousSibling.remove();
				}
				froms[i][j].remove();
			}
		}else{
			if(froms[i].isspace(false)){
				froms[i].previousSibling.remove();
			}
			froms[i].remove();
		}
	}
	try{
		var tn;
		for(var i=tos.length - 1;i >= 0;i--){
			if(tos[i].push){
				for(var j=tos[i].length - 1;j >= 0; j--){
					tn = document.createTextNode(" ");
					ctn.insertBefore(tos[i][j], lastn);
					ctn.insertBefore(tn, tos[i][j]);
					lastn = tn;
				}
			}else{
				tn = document.createTextNode(" ");
				ctn.insertBefore(tos[i], lastn);
				ctn.insertBefore(tn, tos[i]);
				lastn = tn;
			}
		}
	}catch(er){
		return;
	}
	if(tos[0].push){
		tos[0][0].tomean(tos[0][0].textContent);
	}else
	tos[0].tomean(tos[0].textContent);
}
meanengine.swapgt=function(node1,node2){
	var tmp=node1.gT();
	var tmp2=node1.getAttribute("v");
	node1.setAttribute("t", node2.gT());
	node1.cn=node2.gT();
	node1.setAttribute("v", node2.getAttribute("v"));
	node2.setAttribute("t", tmp);
	node2.cn=tmp;
	node2.setAttribute("v", tmp2);
}
meanengine.swapm=function(node1,node2){
	var tmp=node1.innerHTML;
	node1.setmean(node2.textContent);
	node2.setmean(tmp);
}
meanengine.cleantext=function(){
	var str=g(contentcontainer).innerHTML;
	str=str.replace(/Ä‘áº¡o ?<\/i>:/g,"nÃ³i</i>:");
	str=str.replace(/&nbsp;&nbsp;&nbsp;&nbsp;/g,"<br>");
	str=str.replace(/ â€/g,"â€");
	str=str.replace(/ ([,\.!\?â€]+)/g,"$1").replace(/ +<\/i>([ ,\.â€\?\!])/g,"</i>$1");
	g(contentcontainer).textContent=str;
}
meanengine.usedefault=function() {
	if(window.defaultmeanenginerun){
		return;
	}
	window.defaultmeanenginerun=true;
	for(var i=0;i<this.db.default.length;i++){
		meanengine(this.db.default[i]);
	}
	for(var i=0;i<this.db.cdefault.length;i++){
	//	meanengine(this.db.cdefault[i],true);
	}
	if(window.setting.enabletestln){
		for(var i=0;i<this.db.sdefault.length;i++){
			meanengine(this.db.sdefault[i]);
		}
	}
	if(window.setting.enabletransformcore){
		for(var i=0;i<this.db.defaultwln.length;i++){
			meanengine(this.db.defaultwln[i]);
		}
	}else{
		for(var i=0;i<this.db.defaultwoln.length;i++){
			meanengine(this.db.defaultwoln[i]);
		}
	}
}
meanengine.wordIsFaction=function(node,passed){
	if(meanstrategy.recognized[node.id] && meanstrategy.recognized[node.id].type=="faction"){
		var rgobj = meanstrategy.recognized[node.id];
		passed.grp = rgobj.range;
		return true;
	}else if(node.textContent.toLowerCase() != node.textContent && node.textContent.split(" ").length>1){
		return meanstrategy.factions.indexOf(node.gT().lastChar())>=0;
	}
}
var analyzer={
	add:function(chi,num){
		this.data[chi]=num;
	},
	load:function(){
		var s=store.getItem("a"+abookhost+abookid);
		if(s==null){
			return;
		}
		s=s.split("&");
		this.readed=s[0].split(";");
		dat=s[1].split(";");
		dat.forEach(function(it){
			if(it!=""){
				var a=it.split("=");
				analyzer.data[a[0]]=parseInt(a[1]);
			}
		});
	},
	g:function(chi){
		return this.data[chi];
	},
	update:function(chi,num){
		if(this.readed.indexOf(abookchapter)<0){
			if(chi in this.data){
				this.data[chi]+=num;
			}else{
				this.data[chi]=num;
			}
		}else if (!(chi in this.data)) {
			this.data[chi]=num;
		}
	},
	readthis:function(){
		if(this.readed.indexOf(abookchapter)<0){
			this.readed.push(abookchapter);
		}
	},
	readed:[],
	data:{},
	addedname:{},
	collected:{},
	tocollect:[],
	collectphrase:function(node) {
		try{
			var chitext = node.gT();
			var vitext = node.textContent;
			var hvtext = node.gH();
			var multext = node.getAttribute("v");
			var nd = node;
			while(nd.isspace(true)){
				nd=nd.nE();
				chitext += nd.gT();
				vitext +=" "+nd.textContent;
				hvtext +=" "+nd.gH();
				multext +=" "+nd.getAttribute("v");
			}
			nd = node;
			while(nd.isspace(false)){
				nd=nd.pE();
				chitext = nd.gT() + chitext;
				vitext =nd.textContent+" "+vitext;
				hvtext =nd.gH()+" "+hvtext;
				multext =nd.getAttribute("v")+" "+multext;
			}
			if(chitext in this.collected){
				return;
			}else{
				this.collected[chitext] = true;
			}
			ajax("sajax=collectphrase&chi="+encodeURIComponent(chitext)
				+"&vi="+encodeURIComponent(vitext)
				+"&hv="+encodeURIComponent(hvtext)
				+"&mul="+encodeURIComponent(multext),function(){
					console.log("Collected "+chitext);
				});
		}catch(x){}
	},
	lookforcollect:function(){
		if(this.tocollect.length>0){
			this.allowcollect = true;
			for(var i=0;i<this.tocollect.length;i++){
				if(this.tocollect[i] in meanstrategy){
					var keyname="_old-"+this.tocollect[i];
					meanstrategy[keyname] = meanstrategy[this.tocollect[i]];
					meanstrategy[this.tocollect[i]] = function(node){
						analyzer.collectphrase(node);
						meanstrategy[keyname](node);
					}
				}else{
					meanstrategy[this.tocollect[i]] = function(node){
						analyzer.collectphrase(node);
					}
				}
			}
		}
	},
	tryupdatename:function(){
		if(setting.allowanalyzerupdate===true){
			for(var k in this.data){
				if(k.length<2)continue;
				if(k.indexOf("....")>=0)continue;
				var phrase=k.split("-").join("");
				if(meanstrategy.testignorechi(phrase))continue;
				if(dictionary.get(phrase)!=phrase)continue;
				if(phrase in this.addedname)continue;
				if(meanstrategy.surns2.indexOf(phrase.substring(0,2))>-1){
					if(this.data[k]>=4){
						this.addname(k,phrase);
						//tse.send("003",phrase,function(){
						//	analyzer.addname("$"+this.up+"="+meanstrategy.testsuffix(this.up,titleCase(this.down)));
						//});
						this.addedname[phrase]=true;
					}
				}else if (meanstrategy.iscommsurn(phrase.charAt(0))) {
					if(this.data[k]>=4){
						this.addname(k,phrase);
						///tse.send("003",phrase,function(){
						//	analyzer.addname("$"+this.up+"="+meanstrategy.testsuffix(this.up,titleCase(this.down)));
						//});
						this.addedname[phrase]=true;
					}
				}else if (meanstrategy.surns.indexOf(phrase.charAt(0))>-1) {
					if(this.data[k]>=8){
						this.addname(k,phrase);
						//tse.send("003",phrase,function(){
						//	analyzer.addname("$"+this.up+"="+meanstrategy.testsuffix(this.up,titleCase(this.down)));
						//});
						this.addedname[phrase]=true;
					}
				}
			}
			setTimeout(function(){
				sortname();
				saveNS();
			}, 2000);
		}
	},
	addname:function(phraseori,phrase){
		//ajax("sajax=transmulmean&wp=1&content="+encodeURIComponent("çœ è¶³å¤Ÿ"),function(down){
		//	console.log(down)
		//});
		
		tse.send("004",phraseori,function(){
			var dat=this.down.split("|");
			console.log(dat);
			var han="";
			var isfail=false;
			dat.forEach(function(str){
				//han=vp|han=vp
				var s=str.split("=");
				if(s[1].toLowerCase().indexOf(s[0])<0){
					console.log(s);
					isfail=true;
				}else{
					han+=s[0]+" ";
				}
			});
			if(!isfail){
				namew.value="$"+phrase+"="+meanstrategy.testsuffix(phrase,titleCase(han.trim()))+"\n"+namew.value;
			}
		});
		
	},
	save:function(){
		var dat="";
		for(var item in this.data){
			dat+=item+"="+this.data[item]+";";
		}
		this.tryupdatename();
		try{
			store.setItem("a"+abookhost+abookid,this.readed.join(";")+"&"+dat);
		}catch(exce){

		}
	},
	reset:function(){
		this.data={};
		readed=[];
		this.save();
	}
}
function setArrayContain(arrar){
	arrar.c=function(se){
		return this.indexOf(se)>=0;
	}
}
setArrayContain(meanstrategy.database.phasemarginr);
Array.prototype.sumChinese=function(delimiter){
	if(this[0]==null)return "";
	if(delimiter==""){}else
	delimiter=delimiter||"-";
	var str=this[0].gT();
	for(var i=1;i<this.length;i++){
		str+=delimiter+this[i].gT();
	}
	return str;
}
function sumChinese(array,delimiter){
	if(array[0]==null)return "";
	if(delimiter==""){}else
	delimiter=delimiter||"-";
	var str=array[0].gT();
	for(var i=1;i<array.length;i++){
		str+=delimiter+array[i].gT();
	}
	return str;
}
Array.prototype.sumHan=function(){
	var str=this[0].gH();
	for(var i=1;i<this.length;i++){
		str+=" "+this[i].gH();
	}
	return str;
}
function rdmzr(a){
	var rate=0.5;
	var dc=a.split("\n");
	for(var i=0;i<dc.length;i++){
		var f=Math.random()>rate||(function(g,v){v.splice(g,10000/1e4)=="success"})(i,dc)
	}
	return dc.join("\n").replace(/\n+/g,"\n");
}
function lowerNLastWord(str,n){
	var lowered=0;
	for(var i=str.length-1;i>-1;i--){
		if(str.charAt(i)==" "){
			if(i+1==str.length)return str;
			str = str.substring(0, i+1)+str.charAt(i+1).toLowerCase()+str.substring(i+2);
			lowered++;
			if(lowered==n)return str;
		}
	}
	return str.toLowerCase();
}

var needbreak=false;
var analyzerloaded=false;
var prediction={
	sentences:[],
	anl:{},
	enable:false,
	getAllSen:function(){
		var startnd=g(contentcontainer).childNodes[0];
		var allsens=[];
		var sen=[];
		var minsen=[];
		var stack="";
		while(startnd!=null){
			if(startnd.tagName=="BR"){
				if(sen.length>0){
					allsens.push(sen);
					sen=[];
				}
			}else
			if(startnd.tagName=="I"){
				sen.push(startnd);
			}else 
			if(startnd.nodeType==document.TEXT_NODE){
				if(startnd.textContent.contain("â€œ")){
					if(sen.length>0){
						allsens.push(sen);
						sen=[];
					}
					sen.push(startnd);
				}else if(startnd.textContent.contain("â€")){
					sen.push(startnd);
					allsens.push(sen);
					sen=[];
				}else if(startnd.textContent.contain(",")){
					sen.push(startnd);
					allsens.push(sen);
					sen=[];
				}else if(startnd.textContent.contain(".")){
					sen.push(startnd);
					allsens.push(sen);
					sen=[];
				}else{
					sen.push(startnd);
				}
			}
			startnd=startnd.nextSibling;
		}
		if(sen.length>0){
			allsens.push(sen);
		}
		this.sentences=allsens;
	},
	predicted:[],
	tokenize:function(sen){
		var stack=[];
		var chi;
		for(var i=0;i<sen.length;i++){
			if(sen[i].tagName=="I"){
				chi=sen[i].gT();
				for(var x=0;x<chi.length;x++){}
			}
		}
	},
	sentotext:function(sen){
		var tx="";
		for(var i=0;i<sen.length;i++){
			tx+=sen[i].textContent;
		}
		return tx;
	},
	predict:function(sen,cal){
		if(!this.enable){
			return;
		}
		var x = new XMLHttpRequest();
		x.open("POST","//anl.sangtacvietcdn.xyz",true);
		x.onreadystatechange=function() {
			if(this.readyState==4 && this.status==200){
				var arr = JSON.parse(this.responseText);
				cal(arr);
				console.log(arr);
			}
		}
		x.send(sen);
	},
	predictgender:function(name){
		ajax("ajax=genderpredict&name="+encodeURIComponent(name),function(down){
			if(down=="male"){
				console.log("nam");
			}else{
				console.log("ná»¯");
			}
		});
	},
	predictdefault:function(n,cb){
		var v = n.gT();
		v = v.replace(/(.)[ç€äº†]/, "$1");
		this.predict(v,function(d){
			var p = d[0].tag;
			n.setAttribute("p", p);
			if(cb)cb(p);
		});
	},
	parse:function(node,cal,part){
		if(node.getAttribute("p")){
			if(this.cache[node.id]){
				if(cal){
					cal(node,node.getAttribute("p"),this.cache[node.id].taglist,this.cache[node.id].pos);
				}
				return;
			}
		}
		var sentext = node.gT();
		var nd = node;
		var basetext = part||sentext;
		var sen = [nd];
		while(nd.isspace(true)){
			nd=nd.nE();
			if(!nd){
				break;
			}
			sen.push(nd);
			sentext += nd.gT();
		}
		nd = node;
		while(nd.isspace(false)){
			nd=nd.pE();
			if(!nd){
				break;
			}
			sen.unshift(nd);
			sentext = nd.gT() + sentext;
		}
		this.predict(sentext,function(predicted){
			for(var i=0;i<predicted.length;i++){
				if(predicted[i].word == basetext){
					node.setAttribute("p", predicted[i].tag);
					prediction.cache[node.id]={
						taglist: predicted,
						pos: i
					};
					if(cal){
						cal(node,predicted[i].tag,predicted,i);
					}
				}else{
					for(var j=0;j<sen.length;j++){
						if(sen[j].gT() == predicted[i].word){
							sen[j].setAttribute("p", predicted[i].tag);
						}
					}
				}
			}
		});
	},
	cache:{},
	connect:function() {
		if(this.anl.readyState!==1){
			this.anl = new WebSocket("wss://anl.sangtacvietcdn.xyz");
			this.anl.onmessage=function(m) {

				console.log(JSON.parse(m.data));
			}
		}
	},
	data:{
		margin:"",
		count:""
	}
}
function lazyProcessing(){
	if(window.lazyProcessor){
		return;
	}
	window.lazyProcessor = {
		scrollDelay : 300,
		invokable : true,
		currentOffset : 0,
		windowHeight : document.body.scrollHeight || window.innerHeight || document.documentElement.clientHeight|| document.body.clientHeight,
		funList : []
	}
	var getOffset = function(){
		if(excute == excuteApp){
			return window.scrollY;
		}
		return document.body.scrollTop;
	}
	window.addEventListener("scroll", function(){
		if(window.lazyProcessor.invokable){
			window.lazyProcessor.invokable = false;
			setTimeout(function(){
				window.lazyProcessor.invokable = true;
			}, window.lazyProcessor.scrollDelay);
			window.lazyProcessor.currentOffset = getOffset();
			var funList = window.lazyProcessor.funList;
			for(var i=0;i<funList.length;i++){
				if(funList[i].type == 1 && window.lazyProcessor.currentOffset >= funList[i].checkpoint){
					funList[i].fun(funList[i].data);
					funList[i].type = 0;
				}
				if(funList[i].type == 2 
					&& window.lazyProcessor.currentOffset >= funList[i].checkpoint * window.lazyProcessor.windowHeight){
					funList[i].fun(funList[i].data);
					funList[i].type = 0;
				}
			}
		}
	});
	window.lazyProcessor.addCheckPoint = function(type,checkpoint,fun,data){
		this.funList.push({checkpoint:checkpoint,fun:fun,type:type,data:data});
	};
	window.lazyProcessor.clear = function(){
		this.funList=[];
	}
}
window.meanSelectorCheckpoint = 0;
function meanSelector(){
	if(window.setting && window.setting.disablemeanstrategy){
		return;
	}
	if(g(contentcontainer)==null||needbreak)return;
	console.time("mean selector");
	if(!analyzerloaded){
		analyzerloaded=true;
		var str=g("hiddenid").innerHTML.split(";");
		abookchapter=str[1];
		abookhost=str[2];
		abookid=str[0];
		analyzer.load();
	}
	meanstrategy.nodelist=q("#"+contentcontainer+" i");
	meanstrategy.maincontent=g(contentcontainer);
	var surns = arrtoobj(meanstrategy.surns.split(""));
	var surns2 = arrtoobj(meanstrategy.surns2.splitn(2));
	var fts = arrtoobj(meanstrategy.factions);
	var sks = arrtoobj(meanstrategy.skills);
	var ite = arrtoobj(meanstrategy.items);
	var ndlen = meanstrategy.nodelist.length;
	var e;
	var cn;
	var lc;
	var islongchapter = ndlen > 1800;
	var longchapsplit = 200;
	q('[v="hvd"]').forEach(function(e){
		e.innerHTML="";
		e.setAttribute("s", titleCase(convertohanviets(e.gT())));
	});
	if(islongchapter){
		lazyProcessing();
	}
	var brk = false;
	for(var i=window.meanSelectorCheckpoint;i<meanstrategy.nodelist.length;i++) {
		e=meanstrategy.nodelist[i];
		cn=e.gT();
		lc=cn.lastChar();
		//brk = false;
		if(e.id=="ran134"){
				console.log(e);
			}
		if(needbreak)break;
		if(islongchapter){
			if(i > window.meanSelectorCheckpoint + 300){
				needbreak = true;
				window.meanSelectorCheckpoint += 300;
				//console.log("add func");
				window.lazyProcessor.addCheckPoint(2, (i - 300) / ndlen, function(){
					needbreak = false;
				//	console.log('Invoke meanSelector at '+(window.meanSelectorCheckpoint));
					meanSelector();
					
				},{});
				setTimeout(function(){
					analyzer.readthis();
				},1200);
				analyzer.save();
				clearWhiteSpace();
				console.timeEnd("mean selector");
				return;
			}
		}
		if(cn in meanstrategy){
			meanstrategy[cn](e);
		}
		else if(meanengine.db.tokenfind.locat.indexOf(lc)>=0){
			meanstrategy['_L'](e);
		}
		else if(lc=='çš„'){
			
			meanstrategy['_çš„'](e);
		}else if(cn in fts){
			if(cn=="")continue;
			meanstrategy.faction(e,"",e.getAttribute("h"));
			if(lc in ite){
				meanstrategy.item(e,lc);
			}
		}else if (cn.length<4){
			if(cn.length>=2&&surns2.have(cn.substring(0,2))){
				meanstrategy.people2(e,2);
			}else if (cn[0] in surns) {
				meanstrategy.people2(e,1);
			//}else if (meanstrategy.surns.indexOf(cn[0])>=0){
			//	meanstrategy.people(e,1);
			}else if(e.containName()&&!e.isname()){
				if(meanstrategy.surns.indexOf(cn[0])>=0){
					meanstrategy.people2(e,1);
				}
			}
			if(lc in sks||cn in sks){
				meanstrategy.skill(e,"");
			}

			if(lc in ite){
				meanstrategy.item(e,lc);
			}
			if(cn.length==1){
				if(window.setting.allowwordconnector){
					meanstrategy.wordconnector(e);
				}
			}
			if(window.setting.englishfilter){
				//if(meanstrategy.database.english.contain(e.gT().charAt(0))){
				if(cn[0] in engtse.data){
					meanstrategy.testenglish(e);
				}
			}
			if(window.setting.allowphraseshiftor){
				meanstrategy.prepositionmover(e);
			}
		}
	}
	var opentester=new RegExp("("+meanstrategy.database.scope.open+")");
	var numbertester=new RegExp("[0-9]");
	var childlist = g(contentcontainer).childNodes;
	for(var i=0;i<childlist.length;i++){
		if(childlist[i].isexran){
			var m;
			if((m=opentester.exec(childlist[i].textContent))!==null){
				meanstrategy.scope(childlist[i],m[1]);
			}else if (childlist[i].textContent=="...... ") {
				meanstrategy.worddelay(childlist[i]);
			}else if (childlist[i+1]!=null
				&&childlist[i+1].tagName=="I"
				&&childlist[i+1].gT()[0]=='å€'
				&&numbertester.test(childlist[i].textContent)) {
					meanstrategy.numberpow(childlist[i+1]);
			}
		}
	}

	if(window.setting.hideblanknode){
		var ndlist = q("#"+contentcontainer+" i");
		for(var i=0;i<ndlist.length;i++){
			if(ndlist[i].innerHTML!=""){
				if(ndlist[i].gT() && ndlist[i].hasAttribute("hd")) ndlist[i].removeAttribute("hd");
			}
			else{
				ndlist[i].setAttribute("hd", "");
			}
		}
	}

	if(window.setting.pronouninsert||true){
		q("[isname=\"true\"]+[t^=\"è‡ªå·±çš„\"]").forEach(function(e){
			if(getDefaultMean(e).contain("cá»§a")){
				e.pE().tomean(getDefaultMean(e).replace(/chÃ­nh mÃ¬nh|mÃ¬nh/, e.pE().textContent));
				e.textContent="";
			}
		});
		/*
		var pnmatcher = {type:"proname"};
		q("[t*=\"çš„\"]").forEach(function(e){
			if(e.pE())
			if(e.textContent.contain("cá»§a") && meanengine.matcher(pnmatcher,e.pE())){
				//e.textContent += e.pE().textContent;
				e.pE().tomean(e.textContent +" "+ getDefaultMean(e.pE()));
				e.textContent = "";
			}
		});*/
		q("[t*=\"çš„\"]").forEach(function(e){
			if(e.textContent.match(/cá»§a ./) && e.nE() && e.isspace(true)){
				if(e.hasAttribute("asynctask")){
					return;
				}
				var ofw = e.gT().split("çš„")[1];
				var nn = e.nE();
				var tw = ofw + nn.gT();
				var wlv = tw.length;
				if(wlv > 4 || (ofw.length < 2 && !e.cn.contain("æ˜¯")) || tw.match(/[ä¸€äº†å‘¢å’Œå—å•Šè¿‡]/)) return;
				for(var i=0;i<tw.length;i++){
					if(meanengine.db.tokenfind.stwd.indexOf(tw[i]) >= 0){
						return;
					}
				}
				e.setAttribute("asynctask", "true");
				meanstrategy.database.getmean(tw,function(m){
					e.removeAttribute("asynctask");
					if(m=="false" || m=="")return;
					var dm=m.split("/")[0].trim();
					var mlv=dm.split(" ").length;
					if(mlv != wlv){
						return;
					}
					if(e.cn.contain("æ˜¯")){
						var fw = e.textContent.split("cá»§a");
						e.tomean(fw[0] + dm + " cá»§a" + fw[1]);
					}else{
						var cfw = e.textContent.split("cá»§a")[1];
						e.tomean(dm + " cá»§a" + cfw);
					}
					e.cn += nn.gT();
					e.setAttribute("t", e.cn);
					e.setAttribute("v", e.textContent);
					nn.remove();
					if(nn){
						nn.setAttribute("t", "");
						nn.textContent="";
					}
					e.nextSibling.remove();
					ajax("sajax=ofwcwfchk&ofw="+encodeURIComponent(e.cn+"="+e.textContent.trim()),function(){});
				});
			}
		});
		if(false)
		q("[isname=\"true\"]+[t^=\"çš„\"]").forEach(function(e){
			
			var sizemax = 5;
			var size=e.cn.length;
			var ndlist=[e];
			var namenode = e.pE();
			if(namenode.isspace(false))return;
			if(size<sizemax){
				if(e.nE() && e.isspace(true))
				if(e.nE().gT().length + size <= sizemax){
					ndlist.push(e.nE());
					size+=e.nE().gT().length;
					if(size<sizemax){
						if(e.nE().nE() && e.nE().isspace(true))
						if(e.nE().nE().gT().length + size <= sizemax){
							ndlist.push(e.nE().nE());
							size+=e.nE().nE().gT().length;
						}
					}
				}
			}
			if (size >= 3) {
				var phrase=ndlist.sumChinese("");
				size = phrase.length;
				meanstrategy.database.getmean("æˆ‘"+phrase,function(mean1){
					if(mean1=="false"){
						ndlist.pop();
						phrase=ndlist.sumChinese("");
						size = phrase.length;
						if(size>2)
						meanstrategy.database.getmean("æˆ‘"+phrase,function(mean1){
							if(mean1=="false"){
								ndlist.pop();
							}else{
								mean1=mean1.split("/");
								namenode.tomean(mean1[0].replace("ta", namenode.textContent));
								for(var i=0;i<ndlist.length;i++){
									ndlist[i].textContent="";
									ndlist[i].previousSibling.remove();
								}
							}
						});
					}else{
						mean1=mean1.split("/");
						namenode.tomean(mean1[0].replace("ta", namenode.textContent));
						for(var i=0;i<ndlist.length;i++){
							ndlist[i].textContent="";
							ndlist[i].previousSibling.remove();
						}
					}
				});
			}
			
		});
	}

	setTimeout(function(){
		analyzer.readthis();
	},1200);
	analyzer.save();
	meanstrategy.invoker=false;
	//clearDiLastSen();
	clearWhiteSpace();
	console.timeEnd("mean selector");
}
function moveitoupper2(){
	var wd=g(contentcontainer);
	var newstring="";
	var total=0;
	wd.querySelectorAll("p").forEach( function(el) {
		total++;
		newstring+=el.innerHTML+"<br><br>";
		el.remove();
	});
	if(total>17)
		wd.innerHTML=newstring;
	else {
		wd.innerHTML+=newstring;
	}
}
function moveitoupper(text){
	g(contentcontainer).innerHTML=text.replace(/<p[^>]*?>([\s\S]*?)<\/p>/gi,"$1<br><br>");
	//q("br+br+br+br").forEach( function(e) {
	//	if(e.previousElementSibling.previousSibling.textContent.length < 1){
	//		e.previousElementSibling.remove();
	//		e.remove();
	//	}
	//});
}
function converttonode(textnode,givenid){
	if(!window.dictionary){return;};
	var replacementNode = document.createElement('i');
	replacementNode.textContent = textnode.textContent.replace(/([^ \.,â€œ\:\?\â€\!\"\*\)\(\$\^\-\+\@\%\|\/\=\~ã€‘ã€Œã€â€¦ã€Šâ€”ã€‹â€˜â€™\r\n\d]+)/g , function(match,p1)
	    {
		   return dictionary.get(p1);
	    }
	);
	replacementNode.id=givenid;
	replacementNode.setAttribute("h",textnode.textContent);
	replacementNode.setAttribute("t",textnode.textContent);
	replacementNode.cn=textnode.textContent;
	replacementNode.setAttribute("onclick","pr(this);");
	textnode.parentNode.insertBefore(replacementNode, textnode);
	textnode.parentNode.removeChild(textnode);
}

function saveNS(){
	if(typeof(thispage)=="undefined")return;
	var str = namew.value.split("\n");
	var curl = document.getElementById("hiddenid").innerHTML.split(";");
	var book=curl[0];
	var chapter = curl[1];
	var host = curl[2];
	var last = str.join("~//~");
	if(window.setting!=null&&window.setting.onlyonename){
		store.setItem("qtOnline0",last);
	}else{
		try{
			store.setItem(host+book,last);
		}catch(err){
			if(err.message.contain("exceeded")){
				ui.notif("Dung lÆ°á»£ng lÆ°u trá»¯ cá»§a stv trÃªn trÃ¬nh duyá»‡t Ä‘Ã£ Ä‘áº§y, sáº½ khÃ´ng thá»ƒ lÆ°u.")
			}
		}
	}
	
}
function clearNS(){
	if(!confirm("Báº¡n xÃ¡c nháº­n muá»‘n xÃ³a?!!!!"))return;
	namew.value="";
	saveNS();
}
function hideNS(){
	document.getElementById("namewdf").style.visibility="hidden";
}
function showNS(){
	document.getElementById("namewdf").style.visibility="visible";
}
function getNSOnline(){
	g("toolbar").style.display="none";
	g("toolbar2").style.display="block";
	g("dlnametb").style.zIndex="99";
	if(typeof(thispage)=="undefined")return;
	var curl = document.getElementById("hiddenid").innerHTML.split(";");
	var book=curl[0];
	var chapter = curl[1];
	var host = curl[2];
	var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        g("dlnametbcontent").innerHTML = '<tr><th>NgÆ°á»i Ä‘Äƒng</th><th style="max-width:50%">Preview</th><th>Äá»™ dÃ i</th><th>NgÃ y</th><th></th></tr>';
                        g("dlnametbcontent").innerHTML += this.responseText;
                    }
                };
                xhttp.open("GET", "/namesys.php?host="+host+"&book="+book, true);
                xhttp.send();
}
function uploadNS(){
	g("upnamewd").style.zIndex="55";
}
function dlName(e){
	namew.value += e.parentElement.parentElement.children[1].children[0].innerHTML;
}
function sendNS(){
	if(typeof(thispage)=="undefined"){
		g("sendnsbt").disabled=false;
		return;}
	var curl = document.getElementById("hiddenid").innerHTML.split(";");
	var book=curl[0];
	var chapter = curl[1];
	var host = curl[2];
	var xhttp = new XMLHttpRequest();
	var data = "data="+encodeURI(namew.value)+"&username="+encodeURI(g("uploaduser").value)+"&bookid="+book+"&host="+host;
	xhttp.open("POST", "/index.php?upload=true", true);
	xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	 xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
		    if(this.responseText.indexOf("success")>0){
			    alert("ÄÄƒng thÃ nh cÃ´ng.");
			    g("sendnsbt").disabled=false;
			    g("upnamewd").style.zIndex="-1";
		    }
		    else{
			    alert("ÄÄƒng khÃ´ng thÃ nh cÃ´ng: KÃ­ch thÆ°á»›c name tá»‘i thiá»ƒu 200 kÃ­ tá»±.");
			    g("sendnsbt").disabled=false;
			    g("upnamewd").style.zIndex="-1";
		    }
		}
	 };
	 
	 xhttp.send(data);
}
function isVietWord(a){
	if(typeof(a)=="undefined")return false;
	if(a.match(/[a-z]/))return true;
	else return false;
}
function LW(a){
	if(typeof(a)=="undefined")return a;
	return a.replace(/[\:â€œ!\?\.â€,"]+/,"");
}
function isex(left,center,right){
	left=LW(left);
	center = LW(center);
	right=LW(right);
	if(exclude.indexOf(left+" "+center)>-1){
		return false;
	}
	else if(exclude.indexOf(center+" "+right)>-1){
		return false;
	}
	else if(exclude.indexOf(center)>-1){
		return false;
	}
	return true;
}
var nb;
var nbfather;
var i1,is1,is2,is3,is4;
var i2;
var i3;
var i4;
var i5;
var windowWidth = 0; 
(function(){
	try{
		var w = window.innerWidth || document.body.clientWidth || document.documentElement.clientWidth;
		window.windowWidth = w;
	}catch(e){
		window.windowWidth = screen.width;
	}
})(window);

var selNode=[];
var basestr="";
var leftflag=false;
var rightflag=false;
var toeval="";
var toeval2="";
var defined=false;
function defineSys(){
	if(typeof(thispage)=="undefined")return;
	nb = document.getElementById("nsbox");
	nbfather = document.getElementById("boxfather");
	i1=g("vuc");
	i2=g("hv");
	i3=g("huc");
	i4=g("op");
	i5=g("zw");
}
function compareM(left,right){
	var last="";
	left=left.toLowerCase();
	right=right.toLowerCase();
	var end=false;
	var leftidx=0;
	var rightidx=0;
	var pleft=left.split(" ");
	var pright=right.split(" ");
	var curphrase ="";
	while(leftidx<pleft.length){
			if(typeof(pleft[leftidx])=="undefined"){
				break;
			}
			if(!isVietWord(pleft[leftidx])){
				last+=pleft[leftidx]+" ";
				leftidx++;
				rightidx++;
				continue;
			}
			if(pleft[leftidx]==pright[rightidx]){//náº¿u giá»‘ng
	//			console.log(pleft[leftidx]);
				if(pleft[leftidx+1]==pright[rightidx+1] && isVietWord(pright[rightidx+1])&&isex(pleft[leftidx-1],pleft[leftidx],pleft[leftidx+1])&&isex(pleft[leftidx],pleft[leftidx+1],pleft[leftidx+2])){//náº¿u tá»« káº¿ giá»‘ng
					last+=cap(pleft[leftidx])+" ";curphrase+=cap(pleft[leftidx])+" ";
					leftidx++;
					rightidx++;
				}
				else if(leftidx>0){//náº¿u tá»« káº¿ khÃ´ng giá»‘ng vÃ  vá»‹ trÃ­ dÆ°Æ¡ng
					if(pleft[leftidx-1]==pright[rightidx-1]&&isVietWord(pleft[leftidx-1])&&isex(pleft[leftidx-1],pleft[leftidx],pleft[leftidx+1])&&curphrase!=""){//náº¿u tá»« trÆ°á»›c giá»‘ng
						last+=cap(pleft[leftidx])+" ";
						g("t3").value+=curphrase+cap(pleft[leftidx])+"\n";
						curphrase="";
						leftidx++;
						rightidx++;
					}else{//náº¿u tá»« trÆ°á»›c khÃ´ng giá»‘ng
						last+=pleft[leftidx]+" ";
						leftidx++;
						rightidx++;
					}
				}else{//náº¿u tá»« giá»‘ng Ä‘á»©ng má»™t mÃ¬nh	8\
					last+=pleft[leftidx]+" ";
					leftidx++;
					rightidx++;
				}
			}
			else {
				
				if(pleft[leftidx+1]==pright[rightidx]){
					last+=pleft[leftidx]+" ";
					leftidx++;
				}else if(pleft[leftidx]==pright[rightidx+1]){
					rightidx++;
				}else{
					last+=pleft[leftidx]+" ";
					leftidx++;
					rightidx++;
				}
					
			}
			
	}
	return last;
}
function excuteX(){
	var last ="";
	var str1 = g("t1").value;
	var str2=g("t2").value;
	str1 = str1.split("\n");
	str2=str2.split("\n");
	for(var i=0;i<str1.length;i++){
		if(str1[i].length==0){
			last+="\n";
			continue;}
		var a=str1[i].split(",");
		var b=str2[i].split(",");
		for(var x=0;x<a.length;x++){
			last+=compareM(a[x],b[x]);
			if(x!=a.length-1)last+=",";
		}
			
		last+="\n";
	}
	g("t1").value=last.replace(/ ,/g,",")
	.replace(/([\n].)/g,function(v){return v.charAt(0)+v.charAt(1).toUpperCase();})
	.replace(/,([\:â€œ!\?\.â€,"]+)/g,"$1")
	.replace(/\. ./g,function(v){return ". "+v.charAt(2).toUpperCase();})
	.replace(/â€œ./g,function(v){return v.charAt(0)+v.charAt(1).toUpperCase();});
}
function applyNodeList(){
	var ranid =0;
	var ndlist = q("#"+contentcontainer+" i");
	//g(contentcontainer).addEventListener("click", function() {
	//	if(event.target.tagName=="I"){
	//		pr(event.target);
	//	}
	//});
	for(var i=0;i<ndlist.length;i++){
		ndlist[i].id="ran"+i;
		ndlist[i].addEventListener("click", pr);
		ndlist[i].cn = ndlist[i].gT();
		ielement(ndlist[i]);
	}
	//q("#"+contentcontainer+" i").forEach(function(e){e.setAttribute("onclick","pr(this);");e.id="ran"+ranid;ranid++;});
	q("#"+contentcontainer+" br").forEach( function(e) {
		if(e.nextSibling && e.nextSibling.textContent===" "){
			e.nextSibling.remove();
		}
	});
	defined=true;
	//excute();
}
function directeditout(e){
	e.removeAttribute("onfocusout");
	e.contentEditable=false;
	e.removeAttribute("contenteditable");
	e.removeAttribute("onkeydown");
	e.isediting=false;
	if(stilledit==false)
	hideNb();
}
var stilledit=false;
function directeditkeydown(e,key){
	var textlen=e.childNodes[0].textContent.length;
	//key = document.all ? window.event.keyCode : 0;
	var curs=getCaretCharacterOffsetWithin(e);
	if(key==37||key==8){
		if(curs==0){
			stilledit=true;
			var le=e.pE();
			if(!(selNode.indexOf(le)>=0)){
				expandLeft();
			}
			le.isediting=true;
			le.contentEditable=true;
			le.setAttribute("onfocusout","directeditout(this);");
			le.setAttribute("onkeydown","directeditkeydown(this,event.keyCode);");
			le.focus();
			stilledit=false;
			if(key==8){
				le.innerHTML=le.innerHTML.substring(0, le.innerHTML.length-1);
			}
			setEndOfContenteditable(le);
		}
	}
	if(key==39){
		if(curs==textlen){
			stilledit=true;
			var le=e.nE();
			if(!(selNode.indexOf(le)>=0)){
				expandRight();
			}
			le.contentEditable=true;
			le.isediting=true;
			le.setAttribute("onfocusout","directeditout(this);");
			le.setAttribute("onkeydown","directeditkeydown(this,event.keyCode);");
			le.focus();
			stilledit=false;
		}
	}
}

function getCaretCharacterOffsetWithin(element) {
    var caretOffset = 0;
    var doc = element.ownerDocument || element.document;
    var win = doc.defaultView || doc.parentWindow;
    var sel;
    if (typeof win.getSelection != "undefined") {
        sel = win.getSelection();
        if (sel.rangeCount > 0) {
            var range = win.getSelection().getRangeAt(0);
            var preCaretRange = range.cloneRange();
            preCaretRange.selectNodeContents(element);
            preCaretRange.setEnd(range.endContainer, range.endOffset);
            caretOffset = preCaretRange.toString().length;
        }
    } else if ( (sel = doc.selection) && sel.type != "Control") {
        var textRange = sel.createRange();
        var preCaretTextRange = doc.body.createTextRange();
        preCaretTextRange.moveToElementText(element);
        preCaretTextRange.setEndPoint("EndToEnd", textRange);
        caretOffset = preCaretTextRange.text.length;
    }
    return caretOffset;
}
function setEndOfContenteditable(contentEditableElement)
{
    var range,selection;
    if(document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
    {
        range = document.createRange();//Create a range (a range is a like the selection but invisible)
        range.selectNodeContents(contentEditableElement);//Select the entire contents of the element with the range
        range.setEnd(contentEditableElement.childNodes[0],contentEditableElement.childNodes[0].textContent.length);
        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
        selection = window.getSelection();//get the selection object (allows you to change selection)
        selection.removeAllRanges();//remove any selections already made
        selection.addRange(range);//make the range you have just created the visible selection
    }
    else if(document.selection)//IE 8 and lower
    { 
        range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
        range.moveToElementText(contentEditableElement);//Select the entire contents of the element with the range
        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
        range.select();//Select the range (make it the visible selection
    }
}
var instrans;
function pr(e){
	if(e.currentTarget){
		e=e.currentTarget;
	}
	if(typeof setting !="undefined"){
		if(setting.allowtaptoedit!=null&&!setting.allowtaptoedit){
			return;
		}
	}
	if(nb==null){
		nb=g("nsbox");
	}
	if(nb.parentNode==e){
		if(window.setting.directedit){
			if(e.isediting==true)return;
			e.contentEditable=true;
			e.isediting=true;
			e.setAttribute("onfocusout","directeditout(this);");
			e.setAttribute("onkeydown","directeditkeydown(this,event.keyCode);");
			clearSelection();
			e.focus();
			return;
		}
		else{
			return;
		}
	}

	unlock();
	selNode=[];
	e.style.color="red";
	if(i1==null){
		defineSys();
	}
	i1.value=titleCase(e.innerHTML);
	//i2.value=e.getAttribute("h").toLowerCase();
	//i3.value=titleCase(e.getAttribute("h"));
	i2.value=convertohanviets(e.gT()).toLowerCase();
	i3.value=titleCase(convertohanviets(e.gT()));
	i4.value="";
	i5.value=e.gT();
	if(phrasetree.getmean(i5.value)!=""){
		g("instrans").value=phrasetree.getmean(i5.value).split("=")[1];
	}
	else{
		try{
			if(!instrans){
				instrans = g("instrans");
			}
			if(e.mean()){
				g("instrans").value=e.mean();
			}else
			tse.send("001",i5.value,function(){
				g("instrans").value=this.down;
			});
		}catch(xxx){
			tse.send("001",i5.value,function(){
				g("instrans").value=this.down;
			});
		}
		
		
	}
	
	basestr=e.innerHTML;
	is1=i1.value;
	is2=i2.value;
	is3=i3.value;
	is4=i4.value;

	//nb.style.left="0";
	//e.appendChild(nb);
	if(true){
		var offset = getPos(e);
		if(offset.x+257>windowWidth){
			nb.style.left=(windowWidth-256)+"px";
		}else{
			nb.style.left=offset.x+"px";
		}
		nb.style.top=(e.offsetTop + offset.h) +"px";
	}
	showNb();
	//var x=getPos(nb).x;
	//if(x+257>windowWidth){
	//	nb.style.left=(windowWidth-256-x)+"px";
	//}

	selNode.push(e);
}
function expandRight(e){
	var nextNode = nextNSibling(e);
	if(!nextNode){
		return;
	}
	var t1,t2,t3,t4;
	if(nextNode.nodeType==3){
		if(nextNode.textContent.length>1){
			t1=titleCase(nextNode.textContent);
			t2=nextNode.textContent.toLowerCase();
			t3=titleCase(nextNode.textContent);
			t4=nextNode.textContent;
			i1.value+=t1;
			i2.value+=t2;
			i3.value+=t3;
			//i4.value+=t4;
			is1+=t1;
			is2+=t2;
			is3+=t3;
			//is4+=t4;
			//basestr+=t4;
		}
		expandRight(nextNode);
		return;
	}
	t1=titleCase(nextNode.innerHTML)
	//t2=nextNode.getAttribute("h").toLowerCase();
	//t3=titleCase(nextNode.getAttribute("h"));
	t2=convertohanviets(nextNode.gT()).toLowerCase();
	t3=titleCase(convertohanviets(nextNode.gT()));
	t4=nextNode.innerHTML;
	t5=nextNode.gT();
	i1.value+=" "+t1;
	i2.value+=" "+t2;
	i3.value+=" "+t3;
	i5.value+=t5;
	if(nextNode.mean()){
		g("instrans").value+=" "+nextNode.mean();
	}else
	tse.send("001",i5.value,function(){
		g("instrans").value=this.down;
	});
	is1+="|"+t1;
	is2+="|"+t2;
	is3+="|"+t3;
	is4+="|"+t4;
	basestr+="|"+nextNode.innerHTML;
}
function nextNSibling(e){
	var nod =selNode[selNode.length-1].nextSibling;
	if(!nod){
		return null;
	}
	if(nod.nodeType!=3)
	nod.style.color="red";
	selNode.push(nod);
	return selNode[selNode.length-1];
}
function expandLeft(e){
	var nextNode = previousNSibling(e);var t1,t2,t3,t4;
	if(nextNode.nodeType==3){
		if(nextNode.textContent.length>0){
			t1=titleCase(nextNode.textContent);
			t2=nextNode.textContent.toLowerCase();
			t3=titleCase(nextNode.textContent);
			t4=nextNode.textContent;
			i1.value=t1+i1.value;
			i2.value=t2+i2.value;
			i3.value=t3+i3.value;
			//i4.value=t4+i4.value;
			is1=t1+is1;is2=t2+is2;is3=t3+is3;//is4=t4+is4;
			//basestr+=t4;
		}
		leftflag=true;
		expandLeft(nextNode);
		return;
	}
	t1=titleCase(nextNode.innerHTML);
	//t2=nextNode.getAttribute("h").toLowerCase();
	//t3=titleCase(nextNode.getAttribute("h"));
	t2=convertohanviets(nextNode.gT()).toLowerCase();
	t3=titleCase(convertohanviets(nextNode.gT()));
	t4=nextNode.innerHTML;
	t5=nextNode.gT();
	i1.value=t1+i1.value;
	i2.value=t2+i2.value;
	i3.value=t3+i3.value;
	i5.value=t5+i5.value;
	if(nextNode.mean()){
		g("instrans").value=nextNode.mean()+" "+g("instrans").value;
	}else
	tse.send("001",i5.value,function(){
		g("instrans").value=this.down;
	});
	is1=t1+"|"+is1;is2=t2+"|"+is2;is3=t3+"|"+is3;is4=t4+"|"+is4;
	basestr=t4+"|"+basestr;
}
function previousNSibling(e){
	var nod =selNode[0].previousSibling;
	if(nod.nodeType!=3)nod.style.color="red";
	selNode.unshift(nod);
	return selNode[0];
}
function rpqt(a){
	var i = 1;
	var index=a.indexOf("[");
	while(index>=0){
		a=a.replace("[","$"+i);
		i+=2;
		index=a.indexOf("[",i);
	}
	i=2;
	index=a.indexOf("]");
	while(index>=0){
		a=a.replace("]","$"+i);
		i+=2;
		index=a.indexOf("]",i);
	}
	return a;
}
function getPos(el) {
	if(el.getBoundingClientRect){
		var bd = el.getBoundingClientRect();
		return {x: bd.x,y: bd.y,h: bd.height};
	}
    for (var lx=0, ly=0;
	    el != null;
	    lx += el.offsetLeft, ly += el.offsetTop, el = el.offsetParent);
    return {x: lx,y: ly};
}
if(!Element.prototype.remove)
Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}
function applyNs(t){
	if(!selNode[0]){
		return;
	}
	selNode[0].innerHTML=g(t).value;
	unlock();
	for(var i = 1;i<selNode.length;i++){
		selNode[i].remove();
	}
	selNode=[];
}
function applyAndSaveNs(t){
	var right;
	switch(t){
		case "vuc":right=is1;break;
		case "hv":right=is2;break;
		case "huc":right=is3;break;
		case "op":right=i4.value;break
	}
	if(basestr!=""){
		namew.value += "\n@"+basestr+"="+right;
	}
	basestr="";
	unlock();
	selNode=[];
	saveNS();
	excute();
}
function hideNb(){
	if(nb==null
		//||nb.parentElement==nbfather
	)return;
	nb.style.display="none";
	unlock();
	
	
	//nbfather.appendChild(nb);
}
function showNb(){
	nb.style.display="block";
}
function replaceByNode(search,replace){
	var nodelist = q("#"+contentcontainer+" i");
	var len = nodelist.length;
	for(var i=0;i<len;i++){
		if(mc(nodelist[i].innerText,search[0])){
			var flag = true;
			for(var x=1;x<search.length;x++){
				if(x+i>=len)return;
				if(!mc(search[x],nodelist[i+x].innerText)){
					flag=false;
					break;
				}
			}
			if(flag){
				if(search.length==replace.length)
				for(var x=0;x<search.length;x++){
					toeval+="g('"+nodelist[x+i].id+"').innerHTML=\""+eE(replace[x])+"\";";
				}
				else{
					toeval+="g('"+nodelist[i].id+"').innerHTML=\""+eE(replace.join(" "))+"\";";
					var sumhv =nodelist[i].getAttribute("h");
					
					
					for(var x=1;x<search.length;x++){
						if(nodelist[i+x].previousSibling.textContent==' ')
						nodelist[i+x].previousSibling.remove();
						sumhv+=" "+nodelist[i+x].getAttribute("h");
						toeval2+="g('"+nodelist[i+x].id+"').innerHTML='';";
					}
					toeval+="g('"+nodelist[i].id+"').setAttribute(\"h\",\""+eE(sumhv)+"\");";
					
				}
			}
		}
	}
}
function replaceByRegex(search,replace){
	search=search.split(" ");
	var tofind=search[0].toUpperCase();
	var nodelist = g(contentcontainer).childNodes;
	if(nodelist.length<10){
		if(nodelist.length==0)return;
		nodelist=nodelist[1].childNodes;
		if(nodelist.length<10){
			nodelist=g(contentcontainer).childNodes[4].childNodes;
		}
	}
	var len = nodelist.length;
	console.log(len);
	var idot;
	for(var i=0;i<len;i++){
		idot= toU(nodelist[i].textContent).split(" ").indexOf(tofind);
		if(idot>=0){
			var flag = true;
			var arr = nodelist[i].textContent.split(" ");
			var nindex = 2;
			for(var x=1;x<search.length;x++){
				if(x+idot>=arr.length){
					if(i+nindex==nodelist.length){
						return;
					}
					arr = arr.concat(nodelist[i+nindex].textContent.split(" "));
					nindex+=2;
				}
				if(toU(arr[x+idot])!=toU(search[x])){
					flag=false;
					break;
				}
			}
			if(flag){
				var regx = new RegExp(search.join(" "),"i");
				nodelist[i].parentNode.childNodes[i].textContent=arr.join(" ").replace(regx,replace);
				for(var x=1;x<nindex-1;x++){
					nodelist[i+x].parentNode.childNodes[i+x].textContent="";
				}
			}
		}
	}
}
function replaceOnline(search,replace){
	dictionary.set(search,replace);
	var nodelist = q("#"+contentcontainer+" i");
	var len = nodelist.length;
	var firstchar=search.substring(0, 1);
	if(nodelist.length<10){
		if(nodelist.length==0)return;
		if(!nodelist[1]){
			return;
		}
		nodelist=nodelist[1].childNodes;
		if(nodelist.length<10){
			nodelist=g(contentcontainer).childNodes[4].childNodes;
		}
	}
	var len = nodelist.length;
	console.log(len);
	for(var i=0;i<len;i++){
		idot = contain(nodelist[i].gT(),firstchar);
		if(idot>=0){
			var flag=true;
			var x=1;
			var strg=nodelist[i].gT();
			while(strg.length<search.length+idot){
				if(nodelist[i+x]){
					strg+=nodelist[i+x].gT();
					x++;
				}
				else {
					flag=false;
					break;
				}
			}
			if(!flag)continue;;
			if(contain(strg,search)<0){
				continue;;
			}
			try{
				dictionary.editcounter++;
				dictionary.edit(nodelist[i],x,strg,search);
			}catch(exc){

			}
		}
	}
}
function insertAfter(node,newnode){
	node.parentElement.insertBefore(newnode, node.nextSibling);
}
function insertBefore(node,newnode){
	node.parentElement.insertBefore(newnode, node);
}
function shiftnode(node1,node2){
	var nd3=node2.nE();
	g(contentcontainer).insertBefore(node2, node1);
	g(contentcontainer).insertBefore(node1, nd3);
}
function swapnode(node1,node2){
	var node3t=node2.innerHTML;
	var node3c=node2.gT();
	node2.textContent=node1.innerHTML;
	node2.setAttribute("t", node1.gT());
	node2.cn=node1.cn;
	node1.textContent=node3t;
	node1.setAttribute("t", node3c);
	node1.cn=node3c;
}
function insertWordAfter(node,chi,han,viet){
	var newnode=document.createElement("i");
	newnode.innerHTML=viet;
	newnode.setAttribute("t", chi);
	newnode.cn=chi;
	newnode.setAttribute("h", han);
	newnode.setAttribute("onclick", "pr(this);");
	newnode.setAttribute("id", node.id+"-2");
	insertAfter(node,newnode);
	var space=document.createTextNode(" ");
	insertAfter(node,space);
}
function insertWordWaitAsync(node,chi){
	var newnode=document.createElement("i");
	var han = convertohanviets(chi);
	newnode.textContent=han;
	newnode.setAttribute("t", chi);
	newnode.cn=chi;
	newnode.setAttribute("h", han);
	newnode.setAttribute("onclick", "pr(this);");
	newnode.setAttribute("id", node.id+"-2");
	insertAfter(node,newnode);
	var space=document.createTextNode(" ");
	insertAfter(node,space);
	return newnode;
}
function insertWordBefore(node,chi,han,viet){
	var newnode=document.createElement("i");
	newnode.innerHTML=viet;
	newnode.setAttribute("t", chi);
	newnode.cn=chi;
	newnode.setAttribute("h", han);
	newnode.setAttribute("onclick", "pr(this);");
	newnode.setAttribute("id", node.id+"-1");
	insertBefore(node,newnode);
	var space=document.createTextNode(" ");
	insertBefore(node,space);
}
function insertWordBeforeWaitAsync(node,chi){
	var newnode=document.createElement("i");
	var han = convertohanviets(chi)
	newnode.textContent= han;
	newnode.setAttribute("t", chi);
	newnode.cn=chi;
	newnode.setAttribute("h", han);
	newnode.setAttribute("onclick", "pr(this);");
	newnode.setAttribute("id", node.id+"-1");
	insertBefore(node,newnode);
	var space=document.createTextNode(" ");
	insertBefore(node,space);
	return newnode;
}
function mergeWord(nodelist){
	var wordf=nodelist[0];
	//console.log(nodelist);
	for(var i=1;i<nodelist.length;i++){
		//wordf.innerHTML += " " + nodelist[i].innerHTML;
		wordf.setAttribute("t", wordf.gT()+nodelist[i].gT());
		wordf.cn=wordf.cn+nodelist[i].cn;
		wordf.setAttribute("h", wordf.gH()+" "+nodelist[i].gH());
		if(nodelist[i].isspace(false) && nodelist[i-1].isspace(true)){
			nodelist[i].previousSibling.remove();
		}
		nodelist[i].remove();
	}
}
function casingvp(node,mean){
	if(mean == "undefined")return;
	if(node.pE()&&node.pE().tagName=="BR"){
		return mean[0].toUpperCase() + mean.substring(1);
	}else {
		return mean;
	}
}

function replaceVietphrase(){
	var curword=q("#"+contentcontainer+" i")[0];
	var touchnext=false;
	var isHaveP = q("#"+contentcontainer+" p").length > 0;
	var pList = [];
	var pIndex = 0;
	if(isHaveP){
		pList = q("#"+contentcontainer+" p");
		var f = findNextI(pList, 0);
		if(f){
			curword = f.i;
			pIndex = f.idx;
		}
	}
	while(curword!=null){
		if(!(curword.getAttribute("isname")))
		if(curword.gT()[0] in phrasetree.data){
			var ndlen=curword.gT().length-1;
			var minleng=(window.priorvp)?0:ndlen;
			var chi=curword.gT();
			var tree=phrasetree.data[chi[0]];
			var maxleng=tree.maxleng;
			var nodelist=[curword];
			var nd;
			while (chi.length<maxleng) {
				nd=nodelist[nodelist.length-1].nE();
				if(nd==null)break;
				nodelist.push(nd);
				chi+=nd.gT();
			}
			for(var i = maxleng;i>minleng;i--){
				if(chi.substr(0, i) in tree){
					var left=chi.substr(0, i);
					try{
					if(left.length < curword.gT().length){
						//second case
						(function(){
							var l=left;
							var r=curword.gT().substr(l.length);
							var n=curword;
							var t=tree;
							tse.send("004",r,function(){
								var meancomb=this.down.split("|")[0].split("=");
								var mean=t[l].split("=");
								n.setAttribute("t", l);
								n.cn=l;
								var meanlist=mean[1].split("/");
								n.setAttribute("h", mean[0]);
								n.textContent=casingvp(n,meanlist[0]);
								insertWordAfter(n,r,meancomb[0],meancomb[1].split("/")[0].trim());
							});
						})();
					}
					else if (left==curword.gT()) {
						//first case
						//
						var mean=tree[left].split("=");
						if(mean.length < 2){
							continue;
						}
						var meanlist=mean[1].split("/");
						//curword.setAttribute("h", mean[0]);
						curword.textContent=casingvp(curword,meanlist[0]);
					}else{
						//third case
						maxleng=left.length;
						nodelist=[curword];
						var countedlen=curword.gT().length;
						var chi2=curword.gT();
						while (countedlen<maxleng) {
							nd=nodelist[nodelist.length-1].nE();
							if(nd==null)break;
							nodelist.push(nd);
							countedlen+=nd.gT().length;
							chi2+=nd.gT();
						}
						if(countedlen>maxleng){
							(function(){
								var l=left;
								var r=chi2.substr(maxleng);
								var n=nodelist;
								var t=tree;
								tse.send("004",r,function(){
									mergeWord(n);
									var meancomb=this.down.split("|")[0].split("=");
									var mean=t[l].split("=");
									n[0].setAttribute("t", l);
									n[0].cn=l;
									var meanlist=mean[1].split("/");
									n[0].setAttribute("h", mean[0]);
									n[0].textContent=casingvp(n[0],meanlist[0]);
									insertWordAfter(n[0],r,meancomb[0],meancomb[1].split("/")[0].trim());
								});
							})();
						}
						else {
							mergeWord(nodelist);
							var mean=tree[left].split("=");
							var meanlist=mean[1].split("/");
							curword.textContent=casingvp(curword,meanlist[0]);
						}
					}
					}catch(xx){}
					break;
				}
			}
		}
		curword=curword.nE();
		if(isHaveP){
			if(curword == null){
				pIndex++;
				if(pIndex>=pList.length)break;
				var f = findNextI(pList, pIndex);
				if(f){
					curword = f.i;
					pIndex = f.idx;
				}
			}
		}
	}
}
function getMeanFrom(meanpair){
	if(meanpair.length==1)return "";
	if(meanpair[1].indexOf("   ")>0){
		var mword = meanpair[1].split("   ");
		return (mword[0].split("/")[0]+" "+mword[1].split("/")[0]).trim();
	}else{
		return meanpair[1].split("/")[0].trim();
	}
}
function findNextI(pList, start){
	while(start < pList.length){
		var i = pList[start].querySelector("i");
		if(i != null){
			return {i: i, idx: start};
		}
		start++;
	}
	return null;
}
function replaceName(){
	console.time("rpname");
	var curword=q("#"+contentcontainer+" i")[0];
	var touchnext=false;
	var fnodel = 0;
	var isHaveP = q("#"+contentcontainer+" p").length > 0;
	var pList = [];
	var pIndex = 0;
	if(isHaveP){
		pList = q("#"+contentcontainer+" p");
		//curword = pList[0].querySelector("i");
		var f = findNextI(pList, 0);
		if(f){
			curword = f.i;
			pIndex = f.idx;
		}
	}
	while(curword!=null){
		if(true){
			var chi=curword.gT();
			var c2 = chi;
			var breakout=false;
			for(var indexer=0;indexer<c2.length&&indexer<12;indexer++){
				if(breakout)break;

				if(chi[indexer] in nametree.data){
					var tree=nametree.data[chi[indexer]];
					var maxleng=tree.maxleng;
					var nodelist=[curword];
					var nd;
					while (chi.length-indexer<maxleng) {
						nd=nodelist[nodelist.length-1].nE();
						if(nd==null||nd.tagName=="BR")break;
						if(!nd.isspace(false)&&nd.id.substr(0, 5)!="exran"
							&&nodelist[nodelist.length-1].id.substr(0, 5)!="exran"){
							break;
						}
						nodelist.push(nd);
						chi+=nd.gT();
					}
					var i= maxleng; //name = abc phr = ab cd maxleng = 3 cl = 4
					if(i+indexer > chi.length){
						i=chi.length - indexer;
					}
					for(;i>0;i--){
						if(indexer==0){
							if(chi.substr(0, i) in tree){
								var left=chi.substr(0, i);
								if(left.length < curword.gT().length){
									//second case
									indexer += i;
									(function(){
										var l=left;
										var r=curword.gT().substr(l.length);
										var n=curword;
										var t=tree;
										var ndw = insertWordWaitAsync(n,r);
										var mean=t[l].split("=");
										n.setAttribute("t", l);
										n.cn=l;
										n.setAttribute("h", mean[0]);
										n.textContent=mean.joinlast(1).trim();
										n.setAttribute("isname","true");
										n.setAttribute("v",mean[0]);
										window.endpoint2 = window.endpoint;
											window.endpoint = false;
										tse.send("007",r,function(){
											var meancomb=this.down.split("|")[0].split("=");
											var m1 = getMeanFrom(meancomb);
											//phrasetree.setmean(r,this.down.split("|")[0]);
											console.log(meancomb);
											//insertWordAfter(n,r,meancomb[0],meancomb[1].split("/")[0].trim());
											ndw.textContent=m1;//meancomb[1].split("/")[0].trim();
										});
										window.endpoint = window.endpoint2;
									})();
								}
								else if (left==curword.gT()) {
									//first case
									//
									var mean=tree[left].split("=");
									//curword.setAttribute("h", mean[0]);
									curword.textContent=mean.joinlast(1).trim();
									curword.setAttribute("isname","true");
									curword.setAttribute("v",mean[0]);
								}else{
									//third case
									maxleng=left.length;
									nodelist=[curword];
									var countedlen=curword.gT().length;
									var chi2=curword.gT();
									while (countedlen<maxleng) {
										nd=nodelist[nodelist.length-1].nE();
										if(nd==null||nd=="BR")break;
										nodelist.push(nd);
										countedlen+=nd.gT().length;
										chi2+=nd.gT();
									}
									if(countedlen>maxleng){
										indexer += i;
										(function(){
											var l=left;
											var r=chi2.substr(maxleng);
											var n=nodelist;
											var t=tree;
											mergeWord(n);
											var mean=t[l].split("=");
											n[0].setAttribute("t", l);
											n[0].cn=l;
											n[0].setAttribute("h", mean[0]);
											n[0].textContent=mean.joinlast(1).trim();
											n[0].setAttribute("isname","true");
											n[0].setAttribute("v",mean[0]);
											var ndw = insertWordWaitAsync(n[0],r);
											window.endpoint2 = window.endpoint;
											window.endpoint = false;
											tse.send("007",r,function(){
												var meancomb=this.down.split("|")[0].split("=");
												//phrasetree.setmean(r,this.down.split("|")[0]);
												var m1 = getMeanFrom(meancomb);
												//console.log(n[0]);
												//insertWordAfter(n,r,meancomb[0],meancomb[1].split("/")[0].trim());
												ndw.textContent =m1;// meancomb[1].split("/")[0].trim();
											});
											window.endpoint = window.endpoint2;
										})();
									}
									else {
										mergeWord(nodelist);
										var mean=tree[left].split("=");
										curword.textContent=mean.joinlast(1).trim();
										curword.setAttribute("isname","true");
										curword.setAttribute("v",mean[0]);
									}
								}
								breakout=true;
								break;
							}
						}
						else{//012345678 name=345 pos=3 sub0-3=012
							if(chi.substr(indexer, i) in tree){
								console.log("found ", chi, indexer, i, curword.gT());
								var center=chi.substr(indexer, i);
								if(i+indexer<= curword.gT().length){
									
									//left + center = chi
									if(i+indexer==curword.gT().length)
									(function(){
										var l=chi.substr(0, indexer);
										var c=center;
										var n=curword;
										var t=tree;
										var mean=t[c].split("=");
										n.setAttribute("t", c);
										n.cn=c;
										n.setAttribute("h", convertohanviets(c));
										n.textContent=mean.joinlast(1).trim();
										n.setAttribute("isname","true");
										n.setAttribute("v",mean[0]);
										//n.__defineSetter__("textContent", function(v){
										//	console.log("set text content",v);
										//	console.log(printStackTrace());
										//});
										var ndwl = insertWordBeforeWaitAsync(n,l);
										window.endpoint2 = window.endpoint;
											window.endpoint = false;
										tse.send("007",l,function(){
											var meancomb=this.down.split("|")[0].split("=");
											//phrasetree.setmean(l,this.down.split("|")[0]);//cache
											var m1 = getMeanFrom(meancomb);
											//insertWordBefore(n,l,meancomb[0],meancomb[1].split("/")[0].trim());
											ndwl.textContent =m1;// meancomb[1].split("/")[0].trim();
										});
										window.endpoint = window.endpoint2;
									})();
									//left + center + right = chi
									else {
										(function(){
											var l=chi.substr(0, indexer);
											var c=center;
											var r=curword.gT().substr(i+indexer);
											var n=curword;
											var t=tree;
											var mean=t[c].split("=");
											n.setAttribute("t", c);
											n.cn=c;
											n.setAttribute("h", convertohanviets(c));
											n.textContent=mean.joinlast(1).trim();
											n.setAttribute("isname","true");
											n.setAttribute("v",mean[0]);
											var ndwl = insertWordBeforeWaitAsync(n,l);
											var ndwr = insertWordWaitAsync(n,r);
											window.endpoint2 = window.endpoint;
											window.endpoint = false;
											tse.send("007",l+"|"+r,function(){
												var wordcomb=this.down.split("|");
												var leftmean=wordcomb[0].split("=");
												//phrasetree.setmean(l,wordcomb[0]);//cache
												var rightmean=wordcomb[1].split("=");
												//phrasetree.setmean(r,wordcomb[1]);//cache
												//insert name
												var m1 = getMeanFrom(leftmean);
												var m2 = getMeanFrom(rightmean);
												//insert word
												//console.log(n);
												//insertWordBefore(n,l,leftmean[0],leftmean[1].split("/")[0].trim());
												//insertWordAfter(n,r,rightmean[0],rightmean[1].split("/")[0].trim());
												ndwl.textContent = m1;//leftmean[1].split("/")[0].trim();
												ndwr.textContent = m2;//rightmean[1].split("/")[0].trim();
											});
											window.endpoint = window.endpoint2;
										})();
									}
								}
								else{
									
									//third case
									//
									maxleng=i+indexer;
									nodelist=[curword];
									var countedlen=curword.gT().length;
									var chi2=curword.gT();
									while (countedlen<maxleng) {
										nd=nodelist[nodelist.length-1].nE();
										if(nd==null||nd.tagName=="BR")break;
										nodelist.push(nd);
										countedlen+=nd.gT().length;
										chi2+=nd.gT();
									}
									console.log("getting full word ",chi2, maxleng, countedlen);
									if(countedlen>maxleng){
										//left + center + right = n chi
										(function(){
											var l=chi2.substr(0, indexer);
											var c=center;
											var r=chi2.substr(i+indexer);
											var n=nodelist;
											var t=tree;
											mergeWord(n);
											var mean=t[c].split("=");
											n[0].setAttribute("t", c);
											n[0].cn=c;
											n[0].setAttribute("h", convertohanviets(c));
											n[0].textContent=mean.joinlast(1).trim();
											n[0].setAttribute("isname","true");
											n[0].setAttribute("v",mean[0]);
											var ndwl = insertWordBeforeWaitAsync(n[0],l);
											var ndwr = insertWordWaitAsync(n[0],r);
											window.endpoint2 = window.endpoint;
											window.endpoint = false;
											tse.send("007",l+"|"+r,function(){
												var wordcomb=this.down.split("|");
												var leftmean=wordcomb[0].split("=");
												//phrasetree.setmean(l,wordcomb[0]);//cache
												var rightmean=wordcomb[1].split("=");
												//phrasetree.setmean(r,wordcomb[1]);//cache
												//insert name
												var m1 = getMeanFrom(leftmean);
												var m2 = getMeanFrom(rightmean);
												//insert word
												//insertWordBefore(n[0],l,leftmean[0],leftmean[1].split("/")[0].trim());
												//insertWordAfter(n[0],r,rightmean[0],rightmean[1].split("/")[0].trim());
												ndwl.textContent =m1;// leftmean[1].split("/")[0].trim();
												ndwr.textContent =m2; //rightmean[1].split("/")[0].trim();
											});
											window.endpoint = window.endpoint2;
										})();
									}
									else {
										(function(){
											var l=chi2.substr(0, indexer);
											var c=center;
											var n=nodelist;
											var t=tree;
											mergeWord(n);
											var mean=t[c].split("=");
											n[0].setAttribute("t", c);
											n[0].cn=c;
											n[0].setAttribute("h", mean[0]);
											n[0].textContent=mean.joinlast(1).trim();
											n[0].setAttribute("isname","true");
											n[0].setAttribute("v",mean[0]);
											var ndw = insertWordBeforeWaitAsync(n[0],l);
											window.endpoint2 = window.endpoint;
											window.endpoint = false;
											tse.send("007",l,function(){
												
												var meancomb=this.down.split("|")[0].split("=");
												//phrasetree.setmean(l,this.down.split("|")[0]);//cache
												var m1 = getMeanFrom(meancomb);
												//insertWordBefore(n[0],l,meancomb[0],meancomb[1].split("/")[0].trim());
												ndw.textContent = m1;//meancomb[1].split("/")[0].trim();

											});
											window.endpoint = window.endpoint2;
										})();
									}
								}
								breakout=true;
								break;
							}

						}
					}
				}
			}
		}
		curword=curword.nE();
		if(isHaveP){
			if(curword == null){
				pIndex++;
				if(pIndex>=pList.length)break;
				var f = findNextI(pList, pIndex);
				if(f){
					curword = f.i;
					pIndex = f.idx;
				}
			}
		}
	}
	console.timeEnd("rpname");
}
function contain(a,b){
	if(a){
		return a.indexOf(b);
	}
}
function doeval(){
	try{
		eval(toeval);
		eval(toeval2);
	}catch(e){
		console.log(e);
	}
	toeval="";
	toeval2="";
}
function unlock(){
	if(selNode)
	selNode.forEach(function(e){try{e.style.color="inherit";}catch(e){}});
	selNode = [];
}
function toU(a){
	if(a==null)return a;
	else return a.toUpperCase();
}
function doRp(n,t){
	n.textContent=t;
}
function eE(a){
	if(typeof(a)=="undefined")return "";
	else if(a==null)return "";
	else	return a.replace(/\"/g,"\\\"");
}
function mc(a,b){
	if(a!=null){
		if(b!=null){
			return a.toUpperCase()==b.toUpperCase();
		}
		return false;
	}
	return false;
}
var dictionary={
	editcounter:0,
	get:function(key){
		if(key.toUpperCase() in this.data)return this.data[key.toUpperCase()];
		else if(key.replace(" ","").toUpperCase() in this.data)return this.data[key.replace(" ","").toUpperCase()];
		else return key;
	},
	updateonline:function(words,node,numnode,found,search,bases){
		tse.send("002",words,function(){
			var resp = this.down.split("|");
			resp.forEach(function(e){
				dictionary.add(e);
			});
			saveNS();
			if(node.getAttribute("isname")=="true"){
				if(search.length < parseInt(node.getAttribute("namelen")))
					return;
			}
			for(var i=0;i<found.length;i++){
				found[i]=dictionary.get(found[i])||"";
			}
			node.innerHTML=found.join(" "+dictionary.get(search)+" ").trim();
			node.setAttribute("isname","true");
			node.setAttribute("namelen",search.length);
			node.setAttribute("t", bases);
			node.cn=bases;
			var lens=bases.length;
			for(var i=1;i<numnode;i++){
				if(bases.indexOf(node.nE().gT())<0)break;
				node.nextSibling.remove();
				node.setAttribute("h", node.getAttribute("h")+" "+node.nextSibling.getAttribute("h"));
				node.nextSibling.remove();
			}
			dictionary.editcounter--;
		});
	},
	add:function(phrase){
		if(phrase=="="||phrase=="")return;
		var bb=phrase.split("=");
		if(this.get(bb[0])==bb[1])return;
		namew.value="#"+phrase+"\n"+namew.value;
		this.set(bb[0],bb[1]);
	},
	edit:function(node,numnode,found,search){
		var bases=found;
		found=found.split(search);
		var find;
		var needupdate=[];
		if(node.getAttribute("isname")=="true"){
			if(search.length < parseInt(node.getAttribute("namelen")))
				return;
		}
		for(var i=0;i<found.length;i++){
			find=this.get(found[i])||"";
			if(find==found[i]){
				needupdate.push(find);
			}else{
				found[i]=find+" ";
			}
		}
		if(needupdate.length==0){
			node.innerHTML=found.join(" "+this.get(search)+" ").trim();
			node.setAttribute("isname","true");
			node.setAttribute("namelen",search.length);
			node.setAttribute("t",bases);
			node.cn=bases;
			var lens=bases.length;
			for(var i=1;i<numnode;i++){
				if(bases.indexOf(node.nE().gT())<0)break;
				node.nextSibling.remove()
				node.setAttribute("h", node.getAttribute("h")+" "+node.nextSibling.getAttribute("h"));
				node.nextSibling.remove();
			}
			dictionary.editcounter--;
		}else{
			this.updateonline(needupdate.join("|"),node,numnode,found,search,bases);
		}
	},
	set:function(key,value){
		this.data[key]=value;
	},
	load:function(file){
		return;
		//file=file.replace(/[\s\S]*?body>(.*?)<\/body[\s\S]*?/,"$1");
		file=file.split("-//-");
		var a;
		this.count=0;
		var refer=this;
		file.forEach(function(e){
			refer.count++;
			a=e.split("=");
			refer.set(a[0].replace(" ","").toUpperCase(),a[1]);
		});
		console.log("Loaded dictionary");
		this.finished=true;
		excute();
	},
	count:0,
	readTextFile:function(file){
		this.finished=true;
		excute();
		return;
	},
	data:{"ZUIBA":"miá»‡ng","YUANZIDAN":"bom nguyÃªn tá»­","FENGCHEN":"phong tráº§n","QU":"quáº§n",
		"SHUXIONG":"buá»™c ngá»±c","CHÃ‰NGJIÄ€O":"thÃ nh giao","CHÃ‰NGJÄªNG":"thÃ nh dáº¥u áº¥n tinh tháº§n",
		"CHÃ‰NGXÃŒNG":"thÃ nh tÃ­nh","LUÃ€NCHÃ‰NG":"loáº¡n thÃ nh","NÃ’NGCHÃ‰NG":"biáº¿n thÃ nh",
		"SHUANGFENG":"song phong","XIÇOCHÃ‰NG":"tiá»ƒu thÃ nh","CHILUO":"xÃ­ch lÃµa",
		"GAOCHAO":"cao trÃ o","QINGREN":"tÃ¬nh nhÃ¢n","JIAOCHUAN":"giao hoan",
		"LUÃ€NXÃŒNG":"máº¥t lÃ½ trÃ­","MÃ‰NGMÃ‰NG":"má» má»‹t","XIÇODÃ’NG":"lá»— nhá»",
		"XIÇOXIÇO":"nho nhá»","XÃŒNGJIÄ€O":"tÃ­nh giao","XIÅŒNGMÃO":"lÃ´ng ngá»±c",
		"ZHONGYÄ€NG":"trung Æ°Æ¡ng","ZHÅŒNGYÄ€NG":"trung Æ°Æ¡ng","YINGUN":"dÃ¢m cÃ´n",
		"BÄ€NGCÃ€O":"bá»•ng thao","CÃ€ONÃ’NG":"Ä‘iá»u khiá»ƒn","CHÃ‰NGSÃˆ":"pháº©m cháº¥t",
		"CHÃ‰NGRÃ‰N":"thanh niÃªn","DÃ’NGMÃ‰N":"cá»­a Ä‘á»™ng","DÃ’NGXÃ™E":"hang Ä‘á»™ng",
		"DONGQUÃ‚N":"dong quÃ¢n","HUÄ€JÄªNG":"hoa tinh","HÃšNJIÄ€O":"há»—n giao",
		"HÃšNLUÃ€N":"há»—n loáº¡n","HÃšNMÃ‰NG":"lá»«a gáº¡t","HUÃ’LUÃ€N":"mÃª hoáº·c",
		"JIÄ€OHÃšN":"pha láº«n","LUÃ€NSHÃˆ":"loáº¡n xáº¡","MÃ‰NGHÃšN":"lá»«a dá»‘i",
		"MÃ‰NGYÃ€O":"thuá»‘c mÃª","RÃ’UBÄ€NG":"cÃ´n thá»‹t","XIÇOHUÄ€":"hoa nhá»",
		"XIÇOMÃO":"Tiá»ƒu Mao","XIÇOMÃ‰N":"cá»­a nhá»","XIÇOTUÇ":"chÃ¢n nhá»",
		"YÃ€OXÃŒNG":"dÆ°á»£c tÃ­nh","BÄªJIÄ€N":"cÆ°á»¡ng gian","FÃ‰IRÃ’U":"thá»‹t má»¡",
		"HUÄ€FÃ‰I":"bÃ³n thÃºc","HUÄ€HUÄ€":"Hoa Hoa","HUÄ€YÃ€O":"bao pháº¥n",
		"HÃšNHÃšN":"lÆ°u manh","JIANYIN":"gian dÃ¢m","JINGSHÃ‰N":"tinh tháº§n",
		"LUÃ€NMÅŒ":"sá» loáº¡n","MÃOMÃO":"chÃ­p bÃ´ng","MÃ‰NXÃ™E":"ká»³ mÃ´n","MÃLUÃ€N":"mÃª loáº¡n"
		,"MÃMÃ‰NG":"mÃ´ng lung","NÇIMÃO":"tÃ³c mÃ¡u","NÇINÇI":"nÃ£i nÃ£i","NVXÃŒNG":"ná»¯ tÃ­nh"
		,"RÃŒJIÄ€N":"Nháº­t gian","SHÃˆMÃ‰N":"sÃºt gÃ´n","TUÇRÃ’U":"thá»‹t Ä‘Ã¹i","BEIJING":"Báº¯c Kinh"
		,"DONGXUE":"huyá»‡t Ä‘á»™ng","HOUFANG":"houfang","HUÄ€SÃˆ":"sáº¯c hoa","JIAOYIN":"rÃªn rá»‰"
		,"KUAIGAN":"khoÃ¡i cáº£m","MÃOSÃˆ":"mÃ u lÃ´ng","MÃHUÃ’":"mÃª hoáº·c","MÃYÃ€O":"mÃª dÆ°á»£c"
		,"NÇODÃ€I":"nÃ£o to","QINGCHU":"quan sÃ¡t","RÃ’USÃˆ":"mÃ u da","SHÃˆRÃŒ":"xáº¡ nháº­t"
		,"SHENYIN":"rÃªn rá»‰","YÃ€OKÃ™":"kho thuá»‘c","YÃ€ONV":"DÆ°á»£c Ná»¯","YINCHAO":"Ã¢m tráº§m"
		,"YUNIRYU":"yuniryu","ZHENGFU":"chÃ­nh phá»§","CHÃ‰NG":"thÃ nh","XIÅŒNG":"ngá»±c"
		,"BÅŒSÃˆ":"mÃ u nÆ°á»›c","CHUANG":"giÆ°á»ng","CHUÃNG":"giÆ°á»ng","FÇNGFO":"pháº£ng pháº¥t"
		,"HÃ’UHÃ’U":"tháº­t dÃ y","JIA-GE":"giÃ¡ cáº£","JÄªDÃ€NG":"kÃ­ch Ä‘á»™ng","KENENG":"kháº£ nÄƒng"
		,"KÄšNÃ‰NG":"kháº£ nÄƒng","LUONV":"lÃµa ná»¯","MÃ‰IYÇ‘U":"khÃ´ng cÃ³","MÅŒMÅŒ":"sá» sá»"
		,"NAINAI":"nÃ£i nÃ£i","NVSÃˆ":"ná»¯ sáº¯c","QIGUÃ€I":"kÃ¬ quÃ¡i","SÃˆMÃ":"hÃ¡o sáº¯c"
		,"TI-NEI":"thÃ¢n thá»ƒ","YOUHUO":"dá»¥ hoáº·c","ZHÃˆGÃˆ":"cÃ¡i nÃ y","ZHENYA":"tráº¥n Ã¡p"
		,"ZHIDAO":"biáº¿t","ZHIDÃ€O":"biáº¿t","JIÄ€N":"gian","JIÄ€O":"giao","LUÃ€N":"loáº¡n"
		,"MÃ‰NG":"mÃ´ng","NÃ’NG":"lá»™ng","TIÇN":"liáº¿m","XIÇO":"tiá»ƒu","XÃŒNG":"tiÌnh"
		,"LUO":"lÃµa","LUÇ‘":"lÃµa","BÃ™CUÃ’":"khÃ´ng tá»‡","DULI":"Ä‘á»™c láº­p","DUANG":"Ä‘oÃ ng"
		,"GUANG":"quang","JIANG":"giÆ°Æ¡ng","JÄªDÃ€N":"báº¯n","JÄªSHÃˆ":"báº¯n nhanh","LUOLI":"loli"
		,"MÇNYÃŒ":"vá»«a Ã½","NIANG":"nÆ°Æ¡ng","NVXIN":"ná»¯ nhÃ¢n","PAUSE":"pause","QIANG":"thÆ°Æ¡ng"
		,"QIÄ€NG":"thÆ°Æ¡ng","SHÄ€SÇ":"giáº¿t cháº¿t","SHÃME":"cÃ¡i gÃ¬","XIONG":"ngá»±c"
		,"YUAN-":"nguyÃªn","ZHENG":"chÃ­nh","ZHONG":"chuÃ´ng","ZIYOU":"tá»± do",
		"ZÃŒYÃ“U":"tá»± do","ZUILU":"ZUILU","CÃ€O":"thÃ¡o","FÃ‰I":"phÃ¬","HUÄ€":"hoa"
		,"HÃšN":"há»—n","HUÃ’":"hoáº·c","MÃO":"mao","MÃ‰N":"mÃ´n","NÇI":"sá»¯a","RÃ’U":"nhá»¥c"
		,"SHÃˆ":"sáº¯c","TUÇ":"chÃ¢n","XÃ™E":"huyá»‡t","YÃ€N":"thÃ¡n","YÃ€O":"dÆ°á»£c","YÃ’U":"dá»¥"
		,"1ANG":"sÃ³ng","1UAN":"loáº¡n","BÄ€NG":"bá»•ng","BÄªNG":"binh","CHÅŒU":"trá»«u "
		,"CHÃšN":"chá»“n","CHÅªN":"xuÃ¢n","DANG":"Ä‘Ã£ng","DIAO":"Ä‘iáº¿u","DONG":"Ä‘á»™ng"
		,"FENG":"phong","GÄšGÃ‰":"ca ca","GIVE":"give","GUÄ€N":"quan","JIAN":"gian"
		,"JIAO":"giao","JING":"tinh","JÇNG":"cáº£nh","LUAN":"loáº¡n","NIAO":"niá»‡u"
		,"NONG":"lá»™ng","QING":"tÃ¬nh","SHEN":"thÃ¢n","SHÄ’N":"kiá»u ngÃ¢m","SHÇ‘U":"thá»§"
		,"SHÇ“N":"háº¥p ","SUDU":"tá»‘c Ä‘á»™","TÇNG":"tháº­t","XDJM":"anh chá»‹ em","XIAO":"tiá»ƒu"
		,"XING":"tÃ­nh","YÃ‰YÃ‰":"gia gia","YUAN":"nguyÃªn","YUÇN":"viá»…n","ZANG":"tÃ ng"
		,"ZHAN":"gian","ZHE-":"mang","ZHEN":"tráº¥n","BÄª":"bá»©c","BÅŒ":"ba","KÃ™":"khá»‘"
		,"MÃ":"mÃª","MÅŒ":"mÃ²","NV":"ná»¯","RÃŒ":"nháº­t","1OU":"lá»™","1UN":"loáº¡n","CÄ€O":"thao"
		,"CHÄ€":"xuáº¥t","DÄ€I":"hÃ£i ","DÄ€O":"Ä‘ao","DOU":"Ä‘áº¥u","GOU":"chÃ³","GÇ‘U":"cáº©u","HEI":"Ä‘en"
		,"HOU":"háº­u","HUN":"há»“n","HUO":"hoáº·c","ÃŒNG":"linh","ÄªNG":"tinh","JÄ€O":"giao","JIÄ€":"ra "
		,"JUN":"quÃ¢n","LIÃš":"lÆ°u","MÇI":"mua","MEI":"má»¹","MEN":"mÃ´n","MIÃˆ":"diá»‡t","NBA":"NBA"
		,"NIÄ’":"niáº¿t","QIÃš":"cáº§u","RMB":"nhÃ¢n dÃ¢n tá»‡","ROU":"nhá»¥c","SÄ€O":"nÃ¡o","SHÄ€":"giáº¿t",
		"SHE":"báº¯n","SHÃŒ":"thá»‹","TOU":"Ä‘áº§u","TUO":"thoÃ¡t","UÃ€N":"loáº¡n","XÇO":"tiá»ƒu","XÃŒN":"tÃ­nh",
		"XUÃ‰":"huyá»‡t","XUÃˆ":"huyáº¿t","XÃšE":"huyáº¿t","YAO":"dÆ°á»£c","YIN":"Ã¢m","YÃN":"Ã¢m","ZHA":"táº¡c",
		"ZHÃ€":"táº¡c","3Q":"thanks you","BH":"bÆ°u hÃ£n","BL":"BL","BZ":"mod","CJ":"trong tráº¯ng",
		"DD":"Ä‘á»‡ Ä‘á»‡","DÃš":"Ä‘á»™c","Ä’N":"uyá»ƒn ","FÇ":"phÃ¡p","FU":"phá»¥","FÃ™":"phá»¥","FÇ“":"phá»§",
		"JL":"máº·t khÃ¡c","JQ":"gian tÃ¬nh","JS":"gian thÆ°Æ¡ng","JY":"tinh dá»‹ch","LÃŒ":"lá»µ","LJ":"LJ",
		"QÃŒ":"khÃ­","RÇ“":"sá»¯a","SE":"sáº¯c","SÇ":"cháº¿t","SÄª":"tÆ°","SM":"SM","SS":"SS","TJ":"TJ",
		"TM":"TM","TV":"TV","VS":"vs","WX":"bá»‰ á»•i","XB":"tiá»ƒu báº¡ch","XÄª":"xa","YA":"Ã¡p","YÃ€":"dÆ°á»£c"
		,"YD":"Ã¢m Ä‘áº¡o","YÃ‰":"gia","YU":"dá»¥c","YÃ™":"muá»‘n","YY":"tá»± sÆ°á»›ng","ZÃ":"phÃ¡","ZF":"chÃ­nh phá»§"
		,"ZG":"Trung Quá»‘c","GAO":"hiá»ƒu","GUAN":"quan","ZUI":"miá»‡ng","QUN":"quáº§n","JINGYAN":"rung Ä‘á»™ng"
		,"FALUN":"luÃ¢n","YE":"thá»±c","MEISHAONV":"má»¹ thiáº¿u ná»¯","YINYU":"dÃ¢m dá»¥c","HUÃ“DÃ’NG":"hoáº¡t Ä‘á»™ng"
		,"ROUBANG":"cÃ´n thá»‹t","TIANSHANGRENJIAN":"thiÃªn thÆ°á»£ng nhÃ¢n gian","SHANGCHUANG":"lÃªn giÆ°á»ng"
		,"NOZUONODIE":"KhÃ´ng tÃ¬m Ä‘Æ°á»ng cháº¿t sáº½ khÃ´ng pháº£i cháº¿t","XIONGQIANG":"lá»“ng ngá»±c",
		"TINGXIONG":"Æ°á»¡n ngá»±c","XIONGQIAN":"trÆ°á»›c ngá»±c","ZHANCHANG":"chiáº¿n trÆ°á»ng",
		"CHUSHENG":"sÃºc sinh","JIANTING":"nghe lÃ©n","JIANYING":"cáº¯t áº£nh","JIAOXIAO":"nhá» nháº¯n"
		,"MEIXIONG":"bá»™ ngá»±c","TUDGUANG":"má»Ÿ rá»™ng","TUOGUANG":"cá»Ÿi sáº¡ch","XIONGKOU":"ngá»±c"
		,"ZHAOHONG":"há»“ng hÃ o","CHANDOU":"run ráº©y","CHANRAO":"quáº¥n quanh","DIANFEN":"tinh bá»™t"
		,"FEIHONG":"á»­ng Ä‘á»","FENGLIU":"phong lÆ°u","FENGMAN":"Ä‘áº§y Ä‘áº·n","FENGSAO":"láº³ng lÆ¡"
		,"GAOTING":"Ãªm tai","HUANGSE":"mÃ u vÃ ng","JIAORUO":"máº£nh mai","JIAOXIU":"tháº¹n thÃ¹ng",
		"KUANGYE":"hÃ³a thÃº","MEIMIAO":"má»¹ diá»‡u","ROURUAN":"má»m máº¡i","SHENCHU":"vÆ°Æ¡n ra",
		"SUXIONG":"hai vÃº","XIAMIAN":"phÃ­a dÆ°á»›i","XIAOZUI":"miá»‡ng nhá»","XINGGAN":"gá»£i cáº£m"
		,"XIONGBU":"bá»™ ngá»±c","XIONGPU":"bá»™ ngá»±c","YINDANG":"dÃ¢m Ä‘Ã£ng","GUOGUO":"xÃ­ch lÃµa"
		,"HENYIN":"thanh ngÃ¢m","JIAOQU":"thÃ¢n thá»ƒ má»m máº¡i","JINBAO":"kÃ¬nh báº¡o","JIQING":"kÃ­ch tÃ¬nh"
		,"POSHEN":"phÃ¡ thÃ¢n","ROSHAN":"Roshan","SAOHUO":"láº³ng lÆ¡","SELANG":"sáº¯c lang"
		,"SHUANG":"sáº£ng khoÃ¡i","TUOGUI":"chá»‡ch Ä‘Æ°á»ng ray","XIUKUI":"xáº¥u há»•","YUFENG":"nÃºi Ä‘Ã´i"
		,"YUWANG":"hormone","ZHUANG":"trang","ZONGYI":"cuá»“ng ngáº¡o","CHUAN":"thá»Ÿ",
		"HUANG":"vÃ ng","JINJI":"cáº¥m ká»µ","JUHUA":"hoa cÃºc","LUOLU":"cá»Ÿi tráº§n","LUOTI":"lá»a thá»ƒ"
		,"MEISE":"má»‹ sáº¯c ","MIREN":"má»‹ lá»±c","NEIKU":"quáº§n lÃ³t","PINRU":"báº§n nhÅ©",
		"REHUO":"dá»¥ ngÆ°á»i","ROUTI":"thá»ƒ xÃ¡c","RUYAO":"nhu yáº¿u","SHALU":"giáº¿t chÃ³c",
		"SHANG":"lÃªn","TUIQU":"thá»‘i lui","WUHUI":"Ã´ uáº¿","XIANG":"hÆ°á»›ng","YEWAI":"dÃ£ ngoáº¡i",
		"YOHUO":"dá»¥ hoáº·c","ZUOSI":"tÃ¬m Ä‘Æ°á»ng cháº¿t","AIFU":"vuá»‘t ve","BIAN":"Ä‘áº§u",
		"CHAO":"trÃ o","CHOU":"rung","CHUN":"mÃ´i","COMI":"comi","FANG":"nghá»‡",
		"HOLD":"khá»‘ng cháº¿","JIMO":"tá»‹ch má»‹ch","KUSO":"kuso","LIÃ€N":"luyá»‡n",
		"PIAO":"phiÃªu","RUAN":"má»m","SEMI":"dÃ¢m Ä‘Ã£ng","SETU":"sáº¯c cáº§u","SHÃ’U":"phÃºc",
		"TAMA":"con máº¹ nÃ³","TIAO":"tÃ¹y tiá»‡n","TING":"Ä‘á»‰nh","VISA":"visa","UU":"UUKANSHU"
		,"WANG":"vá»ng","WUYE":"váº­t nghiá»‡p","XIAN":"váº¡ch","XIÃ€N":"hiá»‡n","YANG":"dÃ­nh"
		,"YING":"tiá»ƒu","BAO":"táº¡o","CAO":"nhá»•","CHA":"cáº¯m","CHU":"ra","DAO":"Ä‘Æ°á»ng",
		"DAY":"day","FAN":"pháº¡m","FEI":"phi","GAN":"cáº£m","IUO":"lá»a","JIN":"cáº¥m",
		"JÄªN":"cáº¥m","KAN":"nhanh","LOU":"lá»™","NAI":"sá»¯a","NIE":"bÃ³p","PAO":"phÃ¡o",
		"RAO":"quáº¥n","REN":"nÃ³ng","SHA":"báº¯n","SHI":"Æ°á»›t","SIM":"sim","SUO":"rÅ©",
		"TUN":"mÃ´ng","WAN":"muá»™n","WEN":"hÃºt","XIÃ€":"phÃºc","XIE":"tÃ ","XUN":"huáº¥n",
		"YAN":"nghiÃªn","YOU":"dá»¥","YUN":"thai","ZHI":"chi","ZHU":"trá»¥","ZUO":"lÃ m",
		"AO":"ngáº¡o","CA":"sÃ¡t","DA":"Ä‘áº¡i","DU":"Ä‘á»™c","LI":"lá»£i","PA":"phÃ¡o","PO":"phÃ¡",
		"RU":"nhÅ©","SI":"nghÄ©","YÃŒ":"Ã½","ZÃ‰":"chá»n","ZI":"tá»­","BIAO":"biá»ƒu"},
	finished:false
}
function loadCustomName(pack){
	var rawFile = new XMLHttpRequest();
    rawFile.open("GET", "/customname/"+pack+".txt", true);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
				namew.value=this.responseText+"\n"+namew.value;
				$('customnamebox').modal('hide');
				saveNS();
				excute();
            }
        }
    }
	rawFile.send(null);
}

function synctusach(){
	//return;
	if(!setting.autosync)return;
	if(store.getItem("lastsync")){
		if(parseInt(store.getItem("lastsync")) + 300000  >  new Date().getTime()){
			return;
		}
	}
	store.setItem("lastsync", new Date().getTime());
	syncdo("sync");
}

function syncvp(){
	//return;
	if(store.getItem("lastsyncvp")){
		if(parseInt(store.getItem("lastsyncvp")) + 300000  >  new Date().getTime()){
			return;
		}
	}
	store.setItem("lastsyncvp", new Date().getTime());
	syncvpfile("sync");
}
function syncvpfile(type){
	//return;
	if(type=="sync"){
		var xhttp = new XMLHttpRequest();
		var params="ajax=syncvp&step=1&edittime="+store.getItem("lastedittime");
		xhttp.open("POST","/index.php",true);
		xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xhttp.onreadystatechange = function () {
			if (this.readyState == 4 && this.status == 200) {
				if(this.responseText.substring(0, 8)=="needsync"){
					var srtime=this.responseText.split("-")[1];
					store.setItem("lastedittime", srtime);
					var xhttp = new XMLHttpRequest();
					var params="ajax=syncvp&step=2";
					xhttp.open("POST","/index.php",true);
					xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
					xhttp.onreadystatechange = function () {
						if (this.readyState == 4 && this.status == 200) {
							store.setItem("vietphrase", this.responseText);
							phrasetree.load();
							replaceVietphrase();
						}
					};
				    xhttp.send(params);
				}else{
					if(this.responseText.substring(0, 6)=="needup"){
						syncvpfile("update");
					}
				}
			}
		};
	    xhttp.send(params);
	}else if (type=="update") {
		var xhttp = new XMLHttpRequest();
		var params="ajax=syncvp&step=3&data="+encodeURIComponent(store.getItem("vietphrase"));
		xhttp.open("POST","/index.php",true);
		xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xhttp.onreadystatechange = function () {
			if (this.readyState == 4 && this.status == 200) {
				if(this.responseText!=""){
					store.setItem("lastedittime", this.responseText);
				}else{

				}
			}
		};
	    xhttp.send(params);
	}
}
function exportName(){
	var md=createModal("Xuáº¥t dá»¯ liá»‡u name");
	var dat="";
	var str=namew.value.split("\n");
	for(var i=0;i<str.length;i++){
		if(str[i].charAt(0)=="$"){
			dat+=str[i].substring(1)+"\n";
		}
	}
	md.body().innerHTML="<textarea style='width:100%;min-height:360px;'>"+dat+"</textarea>";
	md.show();
}
function importName(){
	var md=createModal("Nháº­p dá»¯ liá»‡u name");
	md.body().innerHTML="<textarea id='ipnametarea' style='width:100%;min-height:360px;'></textarea>";
	md.button("Nháº­p dá»¯ liá»‡u","doreadnamefile()","primary");
	md.show();
}
function doreadnamefile(){
	var tx=g("ipnametarea").value.split("\r\n");
	if(tx.length==1)tx=tx[0].split("\n");
	tx.forEach(function(e){
		namew.value+="\n$"+e;
	});
	saveNS();
	ui.alert("ÄÃ£ import thÃ nh cÃ´ng. Náº¿u muá»‘n lÆ°u dc cho nhiá»u truyá»‡n, vui lÃ²ng báº­t chá»‰ sá»­ dá»¥ng 1 bá»™ name trong cÃ i Ä‘áº·t.");
}
ggtse={}
function googletranslate(chi,callb){
	if(dictionary.get('e'+chi)!=='e'+chi){
		if(callb!=null)
		callb(dictionary.get('e'+chi));
		else g("instrans").value=dictionary.get('e'+chi);
		return;
	}
	if(callb!=null){
		if(chi in ggtse){
			return;
		}
		else {
			ggtse[chi]=true;
		}
	}
	var http = new XMLHttpRequest();
	var url = "https://translate.googleapis.com/translate_a/single?client=gtx&text=&sl=zh-CN&tl=en&dt=t&q=" + encodeURI(chi);
	http.open('GET', url, true);
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	http.onreadystatechange = function() {
		if(http.readyState == 4 && http.status == 200) {
			var result=JSON.parse(this.responseText)[0][0][0];
			dictionary.set("e"+chi,result);
			if(callb!=null){
				callb(result);
			}else
			g("instrans").value=result;
		}
	}
	http.send();
}
function googletranslateNocache(chi,callb){
	var http = new XMLHttpRequest();
	var url = "https://translate.googleapis.com/translate_a/single?client=gtx&text=&sl=zh-CN&tl=en&dt=t&q=" + encodeURI(chi);
	http.open('GET', url, true);
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	http.onreadystatechange = function() {
		if(http.readyState == 4 && http.status == 200) {
			var result=JSON.parse(this.responseText)[0][0][0];
			if(callb!=null){
				callb(result);
			}
		}
	}
	http.send();
}
engtse={
	data:(function(){
		var obj={};
		["äºša","å…¶","å¸ƒb","æ™®p","å¾·d","ç‰¹t","æ ¼g","å…‹k","å¤«v","å¼—v","å¤«w","å¼—w","å¤«f","å¼—f","å…¹z","èŒ¨ts","æ–¯s","ä¸s","ä»€sh","å¥‡dz","å¥‡st","èµ«h","å§†m","æ©n","å°”r","å°”l","ä¼Šj","å¤q","åº“c","èƒ¡wh","é˜¿a","å·´ba","å¸•pa","è¾¾da","å¡”ta","åŠ ga","å¡ka","ç“¦va","å¨ƒva","ç“¦wa","å¨ƒwa","æ³•fa","å¨ƒfa","æ‰Žza","å¯Ÿtsa","è¨sa","èŽŽsa","æ²™sha","èŽŽsha","è´¾dza","æŸ¥sta","å“ˆha","é©¬ma","çŽ›ma","å¨œna","çº³na","æ‹‰la","æ‹‰ra","ç“œqa","å¤¸ca","åŽwha","åŸƒei","è´be","ä½©pei","å¾·dei","ç‰¹tei","æ³°tei","ç›–gei","å‡¯kei","éŸ¦vei","éŸ¦wei","è´¹fei","æ³½zei","ç­–tsei","å¡žsei","è°¢shei","æ°dzei","åˆ‡stei","èµ«hei","é»‘hei","æ¢…mei","å†…nei","èŽ±lei","é›·rei","è•¾rei","è€¶jei","åœ­qei","å¥Žcei","æƒ whei","åŽ„e","ä¼¯be","ç€pe","å¾·de","ç‰¹te","æ ¼ge","å…‹ke","å¼—ve","æ²ƒwe","å¼—fe","æ³½ze","ç­–tse","ç‘Ÿse","èˆshe","å“²dze","å½»ste","èµ«he","é»˜me","çº³ne","å¨œne","å‹’le","å‹’re","è€¶je","æžœqe","é˜”ce","éœwhe","ä¼Ši","æ¯”bi","çš®pi","è¿ªdi","è’‚ti","å‰gi","åŸºki","ç»´vi","å¨wi","è²fi","é½zi","é½tsi","è¥¿si","å¸Œshi","å‰dzi","å¥‡sti","å¸Œhi","ç±³mi","å°¼ni","å¦®ni","åˆ©li","èŽ‰li","é‡Œri","ä¸½ri","ä¼Šji","åœ­qi","å¥Žci","æƒ whi","å¥¥o","åšbo","æ³¢po","å¤šdo","æ‰˜to","æˆˆgo","ç§‘ko","æ²ƒvo","æ²ƒwo","ç¦fo","ä½zo","æŽªtso","ç´¢so","è‚–sho","ä¹”dzo","ä¹”sto","éœho","èŽ«mo","è¯ºno","æ´›lo","ç½—ro","èro","çº¦jo","æžœqo","é˜”co","éœwho","ä¹Œu","å¸ƒbu","æ™®pu","æœdu","å›¾tu","å¤gu","åº“ku","æ­¦vu","ä¼wu","å¯Œfu","ç¥–zu","æ¥štsu","è‹su","èˆ’shu","æœ±dzu","æ¥šstu","èƒ¡hu","ç©†mu","åŠªnu","å¢lu","é²ru","å°¤ju","åº“cu","ä¹…gju","ä¸˜kju","ä¹…zju","ä¸˜tsju","ä¼‘sju","ä¼‘shju","ä¹…dzju","ä¸˜stju","ä¼‘hju","ç¼ªmju","çº½nju","æŸ³lju","ç•™rju","è‰¾ai","æ‹œbai","æ´¾pai","ä»£dai","æ³°tai","ç›–gai","å‡¯kai","éŸ¦vai","æ€€wai","æ³•fai","å®°zai","è”¡tsai","èµ›sai","å¤shai","è´¾dzai","æŸ´stai","æµ·hai","è¿ˆmai","å¥ˆnai","èŽ±lai","èµ–rai","è€¶jai","å¤¸cai","æ€€whai","å¥¥au","é²bau","ä¿pau","é“dau","é™¶tau","é«˜gau","è€ƒkau","æ²ƒvau","æ²ƒwau","ç¦fau","è—»zau","æ›¹tsau","ç»sau","ç»shau","ç„¦dzau","ä¹”stau","è±ªhau","æ¯›mau","ç‘™nau","åŠ³lau","åŠ³rau","å°§jau","é˜”cau","å®‰an","ç­ban","æ½˜pan","ä¸¹dan","å¦tan","ç”˜gan","åŽkan","ä¸‡van","ä¸‡wan","å‡¡fan","èµžzan","ç¿tsan","æ¡‘san","å°šshan","è©¹dzan","é’±stan","æ±‰han","æ›¼man","å—nan","å…°ran","å…°lan","æ‰¬jan","å…³qan","å®½can","çŽ¯whan","æ˜‚ang","é‚¦bang","åºžpang","å½“dang","å”tang","å†ˆgang","åº·kang","æ—ºvang","æ—ºwang","æ–¹fang","è—zang","ä»“tsang","æ¡‘sang","å°šshang","ç« dzang","æ˜Œstang","æ­hang","èŠ’mang","å—nang","æœ—lang","æœ—rang","æ‰¬jang","å…‰qang","åŒ¡cang","é»„whang","æ©en","æœ¬ben","å½­pen","ç™»den","æ»•ten","æ ¹gen","è‚¯ken","æ–‡ven","æ–‡wen","èŠ¬fen","æ›¾zen","å²‘tsen","æ£®sen","ç”³shen","çœŸdzen","ç´sten","äº¨hen","é—¨men","å«©nen","ä¼¦len","ä¼¦ren","å»¶jen","æ˜†cen","å› in","å®¾bin","å¹³pin","ä¸din","å»·tin","é‡‘gin","é‡‘kin","æ¸©vin","æ¸©win","èŠ¬fin","æ´¥zin","æ¬£tsin","è¾›sin","æ¬£shin","é‡‘dzin","é’¦stin","æ¬£hin","æ˜Žmin","å®nin","æž—lin","æž—rin","å› jin","æ˜†cin","è‹±ing","å®¾bing","å¹³ping","ä¸ding","å»·ting","äº¬ging","é‡‘king","æ¸©ving","æ¸©wing","èŠ¬fing","äº¬zing","é’tsing","è¾›sing","å…´shing","äº¬dzing","é’sting","å…´hing","æ˜Žming","å®ning","æž—ling","æž—ring","è‹±jing","æ¸©un","æœ¬bun","è“¬pun","æ•¦dun","é€štun","è´¡gun","æ˜†kun","æ–‡vun","æ–‡wun","ä¸°fun","å°Šzun","èªtsun","å­™sun","é¡ºshun","å‡†dzun","æ˜¥stun","æ´ªhun","è’™mun","å†œnun","ä¼¦lun","ä¼¦run","äº‘jun","ç¿ung","é‚¦bung","è“¬pung","ä¸œdung","é€štung","è´¡gung","å­”kung","ç¿vung","ç¿wung","ä¸°fung","å®—zung","èªtsung","æ¾sung","é›„shung","ç¼dzung","ç¼stung","æ´ªhung","è’™mung","å†œnung","éš†lung","é¾™rung","æ°¸jung","æ´ªwhung","äºšya","ä¸€y","ä¸tin","ä¸‡van","ä¸œto","ä¸ce","ä¸¹de","ä¸½lea","ä¹Œoo","ä¹le","ä¹”jo","ä¹¦sh","äº¨hen","äº²kean","ä»€sh","ä»‘leon","ä»¥e","ä¼Ši","ä¼‘hu","ä¼¦ren","ä¼¯b","ä½zo","ä½›f","ä½©pe","ä¾ƒkan","ä¾y","ä¾¬non","ä¿pa","ä¿®thew","å„¿le","å…‹c","å…°ran","å…¹ze","å†…na","å‡¡fan","å‡¯chae","åˆ‡che","åˆ—le","åˆ©ri","åŠ›lli","åŠ ga","åŠªnu","åŠ³lo","å‹’le","åŽwar","å—nan","åšbo","åœb","å¡ca","å¢lu","å«vy","åŽ„ha","åŽ†le","å£ko","å¤gus","å¯xi","å²S","å„co","å‰ji","å“ˆhu","å”do","å˜‰ga","å›¾to","åœ°de","åŽcan","å¦than","åžƒla","åŸƒe","åŸºch","å¡”ta","å¡žse","å£«ce","å¤tia","å¤šdo","å¤«ve","å¥‡chi","å¥ˆnet","å¥Žckly","å¥¥o","å¦®ny","å§†m","å§¬kie","å¨wi","å¨ƒva","å¨…ya","å¨œna","å©·ne","å®nin","å®‰an","å®‹son","å®pau","å®¾byn","å¯†mi","å¯‡co","å¯Œf","å°”l","å°¤yo","å°¹e","å°¼ni","å±±xan","å´”tri","å·´ba","å¸ƒb","å¸Œsi","å¸•pa","å¸–ther","åº“ku","åº•tes","åº·con","å»‰liam","å¼—f","å¼¥mi","å¼ºjoh","å½“dam","å½¼pe","å¾—ter","å¾·d","æ€th","æ©an","æ‚‰si","æ„£lon","æˆˆgo","æˆ´da","æ‰Žza","æ‰˜to","æ‹‰ra","æ‹œby","æ‹¿na","æti","æ‘©mo","æ•ne","æ–‡vin","æ–fae","æ–‘bam","æ–¯s","æ–¹fon","æ—¥ge","æ—ºwan","æ˜‚an","æ˜†quen","æ˜Žmin","æ˜“i","æ™’shei","æ™®p","æ›¼man","æœ—ran","æœ¬ben","æœ±ju","æ¥ri","æ°ja","æž—line","æžœgo","æŸbe","æŸ¥cha","æŸ¯co","æ ¹gan","æ ¼g","æ¡‘san","æ¢…me","æ¢¨ri","æ£®than","æ¬£ne","æ¬§o","æ­‡sha","æ­¥b","æ¯”bi","æ±€tine","æ±‰ha","æ±¤to","æ²ƒwa","æ²™shu","æ²»rge","æ²½g","æ³•fa","æ³¢po","æ³°tay","æ³½sa","æ´›lo","æ´¾pa","æµ¦pe","æµ·he","æ¶…nie","æ¸©wen","çƒˆre","çˆ±e","ç‰¹t","çŽ›ma","ç€per","çŠzanna","çje","ç rl","ç†ri","ç¦ki","çªki","ç³ri","ç‘žre","ç‘Ÿe","ç’lu","ç“¦va","ç”˜gan","ç”°ten","ç”±yu","ç”¸den","ç•¥li","ç™»den","ç™½beth","çš®pie","ç›–ga","ç£rist","ç ´po","ç¢§bi","ç¦fo","ç§‘co","ç¨£sus","ç©†mu","ç¬†ba","ç­”da","ç­˜co","ç±³my","ç´¢so","çº¦jo","çº³na","ç»´ve","ç»¿lot","ç¼‡ty","ç½•ham","ç½—ro","ç¾Žme","ç¿um","ç¿ tri","ç¿°han","è€ƒco","è€Œle","è€nai","è€¶je","è‚–sha","è‚¯ken","èˆ’shu","è‰¯lian","è‰¾e","èŠ˜pea","èŠ™ve","èŠ¬phine","èŠ­ba","è‹so","è‹±in","èŒƒfan","èŒ…mo","èŒ‰mo","èŒœsi","è·ho","èŽ‰ri","èŽŽsha","èŽ«mo","èŽ±ri","èŽ²le","è²phi","èro","è¨sa","è’‚ti","è’™mon","è“len","è”—ge","è”¡cha","è•¾re","è–‡wi","è¥¿ce","è¦ƒtan","è©¹ja","è¯ºno","è°¢che","è°¬mu","è±ªrol","è´be","è´¹fe","è´¾ja","èµ›se","èµ«her","è·¯lu","è¾›cin","è¾¾da","è¿ªdi","é€Šson","é“dou","é‚“dun","é‚¦ban","é‚±chior","é‚µshau","éƒ½do","é‡Œri","é‡‘kim","é—¨men","é˜‘ran","é˜¿a","éš†ron","é›…a","é›¨hu","é›ªsha","é›¯wen","é›·ly","éœho","éœžsia","éœ²ru","éŸ¦we","é¡¿ton","é£žphy","é©¬ma","é²ru","é²bo","éº¦ma","é»˜me","é»›d","å’”car","æ’’tha"].forEach(function(e){
				var k=e.charAt(0);
				var cont=e.substring(1);
				if(k in obj){
					obj[k]+="/"+cont;
				}else{
					obj[k]=cont;
				}
			});
		return obj;
	})(),
	selectlonger:function(eng){
		var ret="";
		var ls=eng.split("/");
		ls.forEach( function(e) {
			if(e.length>1){ret=e;return;}
		});
		return ret||ls[0];
	},
	trans:function(chi){
		var news="";
		var tmp;
		for(var i=0;i<chi.length;i++){
			if(i==chi.length-1&&chi[i]=="äºš"){
				tmp="a";
			}
			else tmp=(this.data[chi[i]]||chi[i]).split("/")[0];
			if(i==0){
				if(tmp.length==1){
					tmp=this.selectlonger(this.data[chi[i]]);
				}
			}
			news+=tmp;
		}
		return news;
	},
	alliseng:function(chi){
		for(var i=0;i<chi.length;i++){
			if(!(chi[i] in this.data)){
				return false;
			}
		}
		return true;
	}
}
phrasetree={
	data:{
	},
	getmean:function(word){
		var firstchar=this.data[word.charAt(0)];
		if(firstchar==null)return "";
		if(word in firstchar)
			return firstchar[word];
		else {
			return "";
		}
	},
	setmean:function(word,mean){
		if(mean.indexOf("=")<0)return;
		this.data[word[0]]=this.data[word[0]]||{maxleng:0};
		this.data[word[0]][word]=mean;
		if(this.data[word[0]].maxleng < word.length){
			this.data[word[0]].maxleng = word.length;
		}
	},
	save:function(){
		if(store.getItem("useofflinevietphrase")=="true"){
			if(!window.indexedDB){
				return alert("TrÃ¬nh duyá»‡t cá»§a báº¡n khÃ´ng há»— trá»£ file vietphrase riÃªng.");
			}
			if(ngdb==null){
				ngdb=new IdbKvStore('vietphrase');
				//ngdb.set("vietphrasedata",phrasetree.data);
			}
			ngdb.set("vietphrasedata",phrasetree.data); 
		}else
		store.setItem("vietphrase", JSON.stringify(this.data));
	},
	load:function(){
		console.time("loadvp");
		if(true||store.getItem("isloadsingword")=="true"){
			if(store.getItem("useofflinevietphrase")=="true"){
				window.priorvp=true;
				window.attachedvp=false;
				if(store.getItem("trans-win")=="true"){}else{
					window.open("http://sangtacviet.com/transwin.htm");
				}
				setTimeout(function(){
					if(window.attachedvp==false){
						store.setItem("trans-win", "false");
					}
				},30000);
				//loadVietphraseOffline();
			}else{
				try{
					this.data=JSON.parse(store.getItem("vietphrase"))||{};
				}catch(ed){

				}
			}
			
		}else
		this.loadsingword();
		console.timeEnd("loadvp");
		phrasetree.setmean("çœŸ Â· ","chÃ¢n Â· =ChÃ¢n Â· ");
		phrasetree.setmean("å“†å•¦ A æ¢¦","Doraemon=Doraemon");
		phrasetree.setmean(" T æ¤"," T Shirt= T Shirt");
		phrasetree.setmean(" U ç›˜"," USB= USB");
		phrasetree.setmean(" B ç«™"," Bilibili= Bilibili");
		phrasetree.setmean("çš„","=");
	},
	loadsingword:function(){
		return;
		var http = new XMLHttpRequest();
		var url = "/singword.txt";
		http.open('GET', url, true);
		http.overrideMimeType('text/plain; charset=utf-8');
		http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		http.onreadystatechange = function() {
			if(http.readyState == 4 && http.status == 200) {
				this.responseText.split("\n").forEach( function(e) {
					phrasetree.setmean(e[0], e.substring(1));
				});
				phrasetree.save();
				phrasetree.data=JSON.parse(store.getItem("vietphrase"))||{};
				store.setItem("isloadsingword","true");
			}
		}
		http.send();
	}
}
function ielement(e){(function(w,e){if(e.hasAttribute('hd')){if(!w.m){w.m=st.create();w.m.use();};w.m.set("#"+e.id,"color:transparent;font-size:1px;white-space:nowrap;display:inline-block;width:1px;overflow:hidden;");e.removeAttribute('hd');}})(window,e)};
nametree={
	data:{
	},
	getmean:function(word){
		var firstchar=this.data[word.charAt(0)];
		if(firstchar==null)return "";
		if(word in firstchar)
			return firstchar[word];
		else {
			return "";
		}
	},
	setmean:function(word,mean){
		this.data[word[0]]=this.data[word[0]]||{maxleng:0};
		this.data[word[0]][word]=mean;
		if(this.data[word[0]].maxleng < word.length){
			this.data[word[0]].maxleng = word.length;
		}
	},
	save:function(){
		var curl = document.getElementById("hiddenid").innerHTML.split(";");
		var book=curl[0];
		var chapter = curl[1];
		var host = curl[2];
		store.setItem(host+book+"v3", JSON.stringify(this.data));
	},
	load:function(){
		
		var curl = document.getElementById("hiddenid").innerHTML.split(";");
		var book=curl[0];
		var chapter = curl[1];
		var host = curl[2];
		this.data=JSON.parse(store.getItem(host+book+"v3"))||{};
		
	}
}
function loadnodedata(txt){
	var node=q("#"+contentcontainer+" i")[0];
	while(node!=null){
		node.setAttribute("v",node.innerHTML);
		node.innerHTML=node.innerHTML.split("/")[0];
		node=node.nE();
	}
}
window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.msIDBTransaction || {READ_WRITE: "readwrite"}; 
window.IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange || window.msIDBKeyRange;
(function(e) {
    if (typeof exports === "object" && typeof module !== "undefined") { module.exports = e() } else if (typeof define === "function" && define.amd) { define([], e) } else { var t; if (typeof window !== "undefined") { t = window } else if (typeof global !== "undefined") { t = global } else if (typeof self !== "undefined") { t = self } else { t = this } t.IdbKvStore = e() }
})(function() { var e, t, r; return function() {
        function l(o, s, u) {
            function a(r, e) { if (!s[r]) { if (!o[r]) { var t = "function" == typeof require && require; if (!e && t) return t(r, !0); if (f) return f(r, !0); var n = new Error("Cannot find module '" + r + "'"); throw n.code = "MODULE_NOT_FOUND", n } var i = s[r] = { exports: {} };
                    o[r][0].call(i.exports, function(e) { var t = o[r][1][e]; return a(t || e) }, i, i.exports, l, o, s, u) } return s[r].exports } for (var f = "function" == typeof require && require, e = 0; e < u.length; e++) a(u[e]); return a } return l }()({ 1: [function(e, t, r) { var a = Object.create || E; var u = Object.keys || j; var o = Function.prototype.bind || k;

            function n() { if (!this._events || !Object.prototype.hasOwnProperty.call(this, "_events")) { this._events = a(null);
                    this._eventsCount = 0 } this._maxListeners = this._maxListeners || undefined } t.exports = n;
            n.EventEmitter = n;
            n.prototype._events = undefined;
            n.prototype._maxListeners = undefined; var i = 10; var s; try { var f = {}; if (Object.defineProperty) Object.defineProperty(f, "x", { value: 0 });
                s = f.x === 0 } catch (e) { s = false } if (s) { Object.defineProperty(n, "defaultMaxListeners", { enumerable: true, get: function() { return i }, set: function(e) { if (typeof e !== "number" || e < 0 || e !== e) throw new TypeError('"defaultMaxListeners" must be a positive number');
                        i = e } }) } else { n.defaultMaxListeners = i } n.prototype.setMaxListeners = function e(t) { if (typeof t !== "number" || t < 0 || isNaN(t)) throw new TypeError('"n" argument must be a positive number');
                this._maxListeners = t; return this };

            function l(e) { if (e._maxListeners === undefined) return n.defaultMaxListeners; return e._maxListeners } n.prototype.getMaxListeners = function e() { return l(this) };

            function c(e, t, r) { if (t) e.call(r);
                else { var n = e.length; var i = b(e, n); for (var o = 0; o < n; ++o) i[o].call(r) } }

            function h(e, t, r, n) { if (t) e.call(r, n);
                else { var i = e.length; var o = b(e, i); for (var s = 0; s < i; ++s) o[s].call(r, n) } }

            function p(e, t, r, n, i) { if (t) e.call(r, n, i);
                else { var o = e.length; var s = b(e, o); for (var u = 0; u < o; ++u) s[u].call(r, n, i) } }

            function v(e, t, r, n, i, o) { if (t) e.call(r, n, i, o);
                else { var s = e.length; var u = b(e, s); for (var a = 0; a < s; ++a) u[a].call(r, n, i, o) } }

            function d(e, t, r, n) { if (t) e.apply(r, n);
                else { var i = e.length; var o = b(e, i); for (var s = 0; s < i; ++s) o[s].apply(r, n) } } n.prototype.emit = function e(t) { var r, n, i, o, s, u; var a = t === "error";
                u = this._events; if (u) a = a && u.error == null;
                else if (!a) return false; if (a) { if (arguments.length > 1) r = arguments[1]; if (r instanceof Error) { throw r } else { var f = new Error('Unhandled "error" event. (' + r + ")");
                        f.context = r; throw f } return false } n = u[t]; if (!n) return false; var l = typeof n === "function";
                i = arguments.length; switch (i) {
                    case 1:
                        c(n, l, this); break;
                    case 2:
                        h(n, l, this, arguments[1]); break;
                    case 3:
                        p(n, l, this, arguments[1], arguments[2]); break;
                    case 4:
                        v(n, l, this, arguments[1], arguments[2], arguments[3]); break;
                    default:
                        o = new Array(i - 1); for (s = 1; s < i; s++) o[s - 1] = arguments[s];
                        d(n, l, this, o) } return true };

            function y(e, t, r, n) { var i; var o; var s; if (typeof r !== "function") throw new TypeError('"listener" argument must be a function');
                o = e._events; if (!o) { o = e._events = a(null);
                    e._eventsCount = 0 } else { if (o.newListener) { e.emit("newListener", t, r.listener ? r.listener : r);
                        o = e._events } s = o[t] } if (!s) { s = o[t] = r;++e._eventsCount } else { if (typeof s === "function") { s = o[t] = n ? [r, s] : [s, r] } else { if (n) { s.unshift(r) } else { s.push(r) } } if (!s.warned) { i = l(e); if (i && i > 0 && s.length > i) { s.warned = true; var u = new Error("Possible EventEmitter memory leak detected. " + s.length + ' "' + String(t) + '" listeners ' + "added. Use emitter.setMaxListeners() to " + "increase limit.");
                            u.name = "MaxListenersExceededWarning";
                            u.emitter = e;
                            u.type = t;
                            u.count = s.length; if (typeof console === "object" && console.warn) { console.warn("%s: %s", u.name, u.message) } } } } return e } n.prototype.addListener = function e(t, r) { return y(this, t, r, false) };
            n.prototype.on = n.prototype.addListener;
            n.prototype.prependListener = function e(t, r) { return y(this, t, r, true) };

            function _() { if (!this.fired) { this.target.removeListener(this.type, this.wrapFn);
                    this.fired = true; switch (arguments.length) {
                        case 0:
                            return this.listener.call(this.target);
                        case 1:
                            return this.listener.call(this.target, arguments[0]);
                        case 2:
                            return this.listener.call(this.target, arguments[0], arguments[1]);
                        case 3:
                            return this.listener.call(this.target, arguments[0], arguments[1], arguments[2]);
                        default:
                            var e = new Array(arguments.length); for (var t = 0; t < e.length; ++t) e[t] = arguments[t];
                            this.listener.apply(this.target, e) } } }

            function m(e, t, r) { var n = { fired: false, wrapFn: undefined, target: e, type: t, listener: r }; var i = o.call(_, n);
                i.listener = r;
                n.wrapFn = i; return i } n.prototype.once = function e(t, r) { if (typeof r !== "function") throw new TypeError('"listener" argument must be a function');
                this.on(t, m(this, t, r)); return this };
            n.prototype.prependOnceListener = function e(t, r) { if (typeof r !== "function") throw new TypeError('"listener" argument must be a function');
                this.prependListener(t, m(this, t, r)); return this };
            n.prototype.removeListener = function e(t, r) { var n, i, o, s, u; if (typeof r !== "function") throw new TypeError('"listener" argument must be a function');
                i = this._events; if (!i) return this;
                n = i[t]; if (!n) return this; if (n === r || n.listener === r) { if (--this._eventsCount === 0) this._events = a(null);
                    else { delete i[t]; if (i.removeListener) this.emit("removeListener", t, n.listener || r) } } else if (typeof n !== "function") { o = -1; for (s = n.length - 1; s >= 0; s--) { if (n[s] === r || n[s].listener === r) { u = n[s].listener;
                            o = s; break } } if (o < 0) return this; if (o === 0) n.shift();
                    else g(n, o); if (n.length === 1) i[t] = n[0]; if (i.removeListener) this.emit("removeListener", t, u || r) } return this };
            n.prototype.removeAllListeners = function e(t) { var r, n, i;
                n = this._events; if (!n) return this; if (!n.removeListener) { if (arguments.length === 0) { this._events = a(null);
                        this._eventsCount = 0 } else if (n[t]) { if (--this._eventsCount === 0) this._events = a(null);
                        else delete n[t] } return this } if (arguments.length === 0) { var o = u(n); var s; for (i = 0; i < o.length; ++i) { s = o[i]; if (s === "removeListener") continue;
                        this.removeAllListeners(s) } this.removeAllListeners("removeListener");
                    this._events = a(null);
                    this._eventsCount = 0; return this } r = n[t]; if (typeof r === "function") { this.removeListener(t, r) } else if (r) { for (i = r.length - 1; i >= 0; i--) { this.removeListener(t, r[i]) } } return this };
            n.prototype.listeners = function e(t) { var r; var n; var i = this._events; if (!i) n = [];
                else { r = i[t]; if (!r) n = [];
                    else if (typeof r === "function") n = [r.listener || r];
                    else n = L(r) } return n };
            n.listenerCount = function(e, t) { if (typeof e.listenerCount === "function") { return e.listenerCount(t) } else { return w.call(e, t) } };
            n.prototype.listenerCount = w;

            function w(e) { var t = this._events; if (t) { var r = t[e]; if (typeof r === "function") { return 1 } else if (r) { return r.length } } return 0 } n.prototype.eventNames = function e() { return this._eventsCount > 0 ? Reflect.ownKeys(this._events) : [] };

            function g(e, t) { for (var r = t, n = r + 1, i = e.length; n < i; r += 1, n += 1) e[r] = e[n];
                e.pop() }

            function b(e, t) { var r = new Array(t); for (var n = 0; n < t; ++n) r[n] = e[n]; return r }

            function L(e) { var t = new Array(e.length); for (var r = 0; r < t.length; ++r) { t[r] = e[r].listener || e[r] } return t }

            function E(e) { var t = function() {};
                t.prototype = e; return new t }

            function j(e) { var t = []; for (var r in e)
                    if (Object.prototype.hasOwnProperty.call(e, r)) { t.push(r) } return r }

            function k(e) { var t = this; return function() { return t.apply(e, arguments) } } }, {}], 2: [function(e, t, r) { if (typeof Object.create === "function") { t.exports = function e(t, r) { t.super_ = r;
                    t.prototype = Object.create(r.prototype, { constructor: { value: t, enumerable: false, writable: true, configurable: true } }) } } else { t.exports = function e(t, r) { t.super_ = r; var n = function() {};
                    n.prototype = r.prototype;
                    t.prototype = new n;
                    t.prototype.constructor = t } } }, {}], 3: [function(e, t, r) { t.exports = n;

            function n(r) { var n; var i; var o; if (r != null && typeof r !== "function") throw new Error("cb must be a function"); if (r == null && typeof Promise !== "undefined") { n = new Promise(function(e, t) { i = e;
                        o = t }) }

                function e(e, t) { if (n) { if (e) o(e);
                        else i(t) } else { if (r) r(e, t);
                        else if (e) throw e } } e.promise = n; return e } }, {}], "/": [function(e, t, r) { t.exports = y; var p = e("events").EventEmitter; var n = e("inherits"); var f = e("promisize"); var v = typeof window === "undefined" ? self : window; var d = v.indexedDB || v.mozIndexedDB || v.webkitIndexedDB || v.msIndexedDB;
            y.INDEXEDDB_SUPPORT = d != null;
            y.BROADCAST_SUPPORT = v.BroadcastChannel != null;
            n(y, p);

            function y(e, t, r) { var n = this; if (typeof e !== "string") throw new Error("A name must be supplied of type string"); if (!d) throw new Error("IndexedDB not supported"); if (typeof t === "function") return new y(e, null, t); if (!(n instanceof y)) return new y(e, t, r); if (!t) t = {};
                p.call(n);
                n._db = null;
                n._closed = false;
                n._channel = null;
                n._waiters = []; var i = t.channel || v.BroadcastChannel; if (i) { n._channel = new i(e);
                    n._channel.onmessage = h } var o = d.open(e);
                o.onerror = s;
                o.onsuccess = a;
                o.onupgradeneeded = f;
                n.on("newListener", c);

                function s(e) { _(e);
                    n._close(e.target.error); if (r) r(e.target.error) }

                function u(e) { _(e);
                    n._close(e.target.error) }

                function a(e) { if (n._closed) { e.target.result.close() } else { n._db = e.target.result;
                        n._db.onclose = l;
                        n._db.onerror = u; for (var t in n._waiters) try{n._waiters[t]._init(null);}catch(uxi){}
                        n._waiters = null; if (r) r(null);
                        n.emit("open") } }

                function f(e) { var t = e.target.result;
                    t.createObjectStore("kv", { autoIncrement: true }) }

                function l() { n._close() }

                function c(e) { if (e !== "add" && e !== "set" && e !== "remove") return; if (!n._channel) return n.emit("error", new Error("No BroadcastChannel support")) }

                function h(e) { if (e.data.method === "add") n.emit("add", e.data);
                    else if (e.data.method === "set") n.emit("set", e.data);
                    else if (e.data.method === "remove") n.emit("remove", e.data) } } y.prototype.get = function(e, t) { return this.transaction("readonly").get(e, t) };
            y.prototype.getMultiple = function(e, t) { return this.transaction("readonly").getMultiple(e, t) };
            y.prototype.set = function(e, t, r) { r = f(r); var n = null; var i = this.transaction("readwrite", function(e) { n = n || e;
                    r(n) });
                i.set(e, t, function(e) { n = e }); return r.promise };
            y.prototype.json = function(e, t) { return this.transaction("readonly").json(e, t) };
            y.prototype.keys = function(e, t) { return this.transaction("readonly").keys(e, t) };
            y.prototype.values = function(e, t) { return this.transaction("readonly").values(e, t) };
            y.prototype.remove = function(e, t) { t = f(t); var r = null; var n = this.transaction("readwrite", function(e) { r = r || e;
                    t(r) });
                n.remove(e, function(e) { r = e }); return t.promise };
            y.prototype.clear = function(t) { t = f(t); var r = null; var e = this.transaction("readwrite", function(e) { r = r || e;
                    t(r) });
                e.clear(function(e) { r = e }); return t.promise };
            y.prototype.count = function(e, t) { return this.transaction("readonly").count(e, t) };
            y.prototype.add = function(e, t, r) { r = f(r); var n = null; var i = this.transaction("readwrite", function(e) { n = n || e;
                    r(n) });
                i.add(e, t, function(e) { n = e }); return r.promise };
            y.prototype.iterator = function(e, t) { return this.transaction("readonly").iterator(e, t) };
            y.prototype.transaction = function(e, t) { if (this._closed) throw new Error("Database is closed"); var r = new i(this, e, t); if (this._db) r._init(null);
                else this._waiters.push(r); return r };
            y.prototype.close = function() { this._close() };
            y.prototype._close = function(e) { if (this._closed) return;
                this._closed = true; if (this._db) this._db.close(); if (this._channel) this._channel.close();
                this._db = null;
                this._channel = null; if (e) this.emit("error", e);
                this.emit("close"); for (var t in this._waiters) this._waiters[t]._init(e || new Error("Database is closed"));
                this._waiters = null;
                this.removeAllListeners() };

            function i(e, t, r) { if (typeof t === "function") return new i(e, null, t);
                this._kvStore = e;
                this._mode = t || "readwrite";
                this._objectStore = null;
                this._waiters = null;
                this.finished = false;
                this.onfinish = f(r);
                this.done = this.onfinish.promise; if (this._mode !== "readonly" && this._mode !== "readwrite") { throw new Error('mode must be either "readonly" or "readwrite"') } } i.prototype._init = function(e) { var t = this; if (t.finished) return; if (e) return t._close(e); var r = t._kvStore._db.transaction("kv", t._mode);
                r.oncomplete = i;
                r.onerror = o;
                r.onabort = o;
                t._objectStore = r.objectStore("kv"); for (var n in t._waiters) t._waiters[n](null, t._objectStore);
                t._waiters = null;

                function i() { t._close(null) }

                function o(e) { _(e);
                    t._close(e.target.error) } };
            i.prototype._getObjectStore = function(e) { if (this.finished) throw new Error("Transaction is finished"); if (this._objectStore) return e(null, this._objectStore);
                this._waiters = this._waiters || [];
                this._waiters.push(e) };
            i.prototype.set = function(n, i, o) { var s = this; if (n == null || i == null) throw new Error("A key and value must be given");
                o = f(o);
                s._getObjectStore(function(e, t) { if (e) return o(e); try { var r = t.put(i, n) } catch (e) { return o(e) } r.onerror = _.bind(this, o);
                    r.onsuccess = function() { if (s._kvStore._channel) { s._kvStore._channel.postMessage({ method: "set", key: n, value: i }) } o(null) } }); return o.promise };
            i.prototype.add = function(n, i, o) { var s = this; if (i == null && n != null) return s.add(undefined, n, o); if (typeof i === "function" || i == null && o == null) return s.add(undefined, n, i); if (i == null) throw new Error("A value must be provided as an argument");
                o = f(o);
                s._getObjectStore(function(e, t) { if (e) return o(e); try { var r = n == null ? t.add(i) : t.add(i, n) } catch (e) { return o(e) } r.onerror = _.bind(this, o);
                    r.onsuccess = function() { if (s._kvStore._channel) { s._kvStore._channel.postMessage({ method: "add", key: n, value: i }) } o(null) } }); return o.promise };
            i.prototype.get = function(n, i) { var e = this; if (n == null) throw new Error("A key must be given as an argument");
                i = f(i);
                e._getObjectStore(function(e, t) { if (e) return i(e); try { var r = t.get(n) } catch (e) { return i(e) } r.onerror = _.bind(this, i);
                    r.onsuccess = function(e) { i(null, e.target.result) } }); return i.promise };
            i.prototype.getMultiple = function(u, a) { var e = this; if (u == null) throw new Error("An array of keys must be given as an argument");
                a = f(a); if (u.length === 0) { a(null, []); return a.promise } e._getObjectStore(function(e, t) { if (e) return a(e); var n = u.slice().sort(); var i = 0; var o = {}; var s = function() { return u.map(function(e) { return o[e] }) }; var r = t.openCursor();
                    r.onerror = _.bind(this, a);
                    r.onsuccess = function(e) { var t = e.target.result; if (!t) { a(null, s()); return } var r = t.key; while (r > n[i]) {++i; if (i === n.length) { a(null, s()); return } } if (r === n[i]) { o[r] = t.value;
                            t.continue() } else { t.continue(n[i]) } } }); return a.promise };
            i.prototype.json = function(e, r) { var t = this; if (typeof e === "function") return t.json(null, e);
                r = f(r); var n = {};
                t.iterator(e, function(e, t) { if (e) return r(e); if (t) { n[t.key] = t.value;
                        t.continue() } else { r(null, n) } }); return r.promise };
            i.prototype.keys = function(e, r) { var t = this; if (typeof e === "function") return t.keys(null, e);
                r = f(r); var n = [];
                t.iterator(e, function(e, t) { if (e) return r(e); if (t) { n.push(t.key);
                        t.continue() } else { r(null, n) } }); return r.promise };
            i.prototype.values = function(e, r) { var t = this; if (typeof e === "function") return t.values(null, e);
                r = f(r); var n = [];
                t.iterator(e, function(e, t) { if (e) return r(e); if (t) { n.push(t.value);
                        t.continue() } else { r(null, n) } }); return r.promise };
            i.prototype.remove = function(n, i) { var o = this; if (n == null) throw new Error("A key must be given as an argument");
                i = f(i);
                o._getObjectStore(function(e, t) { if (e) return i(e); try { var r = t.delete(n) } catch (e) { return i(e) } r.onerror = _.bind(this, i);
                    r.onsuccess = function() { if (o._kvStore._channel) { o._kvStore._channel.postMessage({ method: "remove", key: n }) } i(null) } }); return i.promise };
            i.prototype.clear = function(n) { var e = this;
                n = f(n);
                e._getObjectStore(function(e, t) { if (e) return n(e); try { var r = t.clear() } catch (e) { return n(e) } r.onerror = _.bind(this, n);
                    r.onsuccess = function() { n(null) } }); return n.promise };
            i.prototype.count = function(n, i) { var e = this; if (typeof n === "function") return e.count(null, n);
                i = f(i);
                e._getObjectStore(function(e, t) { if (e) return i(e); try { var r = n == null ? t.count() : t.count(n) } catch (e) { return i(e) } r.onerror = _.bind(this, i);
                    r.onsuccess = function(e) { i(null, e.target.result) } }); return i.promise };
            i.prototype.iterator = function(n, i) { var e = this; if (typeof n === "function") return e.iterator(null, n); if (typeof i !== "function") throw new Error("A function must be given");
                e._getObjectStore(function(e, t) { if (e) return i(e); try { var r = n == null ? t.openCursor() : t.openCursor(n) } catch (e) { return i(e) } r.onerror = _.bind(this, i);
                    r.onsuccess = function(e) { var t = e.target.result;
                        i(null, t) } }) };
            i.prototype.abort = function() { if (this.finished) throw new Error("Transaction is finished"); if (this._objectStore) this._objectStore.transaction.abort();
                this._close(new Error("Transaction aborted")) };
            i.prototype._close = function(e) { if (this.finished) return;
                this.finished = true;
                this._kvStore = null;
                this._objectStore = null; for (var t in this._waiters) this._waiters[t](e || new Error("Transaction is finished"));
                this._waiters = null; if (this.onfinish) this.onfinish(e);
                this.onfinish = null };

            function _(e, t) { if (t == null) return _(null, e);
                t.preventDefault();
                t.stopPropagation(); if (e) e(t.target.error) } }, { events: 1, inherits: 2, promisize: 3 }] }, {}, [])("/") });
var ngdb;
function loadVietphraseOffline(cb) {
	if(!window.indexedDB){
		return alert("TrÃ¬nh duyá»‡t cá»§a báº¡n khÃ´ng há»— trá»£ file vietphrase riÃªng.");
	}
	if(ngdb==null){
		ngdb=new IdbKvStore('vietphrase',{},loadVietphraseOffline);
		//ngdb.set("vietphrasedata",phrasetree.data);
	}else{
		ngdb.get("vietphrasedata",function(err,val){
			if(err)throw err;
			phrasetree.data=val;
			if(window.loadvp===false){
				window.loadvp=true;
			}
			//replaceVietphrase();
		});
	}
}
function insertVietphraseOffline(file){
	if(!window.indexedDB){
		return alert("TrÃ¬nh duyá»‡t cá»§a báº¡n khÃ´ng há»— trá»£ file vietphrase riÃªng.");
	}
	if(ngdb==null){
		ngdb=new IdbKvStore('vietphrase');
		//ngdb.set("vietphrasedata",phrasetree.data);
	}
	var fr = new FileReader();
    fr.onload = function(e)
        {
        	//alert(fr.result.length);
        	var lines=fr.result.split(/\r?\n/);
        	//return console.log(lines.length);
        	var count=0;
        	for(var i=0;i<lines.length;i++){
        		var phr=lines[i].split("=");
        		if(phr.length>1){
        			phrasetree.setmean(phr[0],"="+phr[1]);
        			count++;
        		}
        	}
            ngdb.set("vietphrasedata",phrasetree.data); 
            store.setItem("useofflinevietphrase","true");
            window.priorvp=true;
            alert("Nháº­p thÃ nh cÃ´ng "+count+" dÃ²ng.");
        };
    fr.readAsText(file);
}
function openinsertvpmodal() {
	var md=createModal("Nháº­p vietphrase cÃ¡ nhÃ¢n");
	md.body().innerHTML='<br><input type="file" id="vpfile" onch="insertVietphraseOffline(this.files[0])"><br><center><button class="btn" onclick="insertVietphraseOffline(g(\'vpfile\').files[0])">Nháº­p</button></center><br><div id="insertvpstatus"></div>';
	md.show();
}
function toonemeaning(mulmean) {
	return mulmean.split(/[\/\|]/)[0];	
}
function convertchitovi(chinese) {
	chinese=standardizeinput(chinese);
	var stringBuilder = [];
    var num = chinese.length - 1;
    var lastword={data:""};
    var i = 0;
    while (i <= num)
    {
        var flag = false;
        for (var j = 12; j > 0; j--)
        {
            if (chinese.length >= i + j)
            {
                var cn=chinese.substr(i, j);
                var text=phrasetree.getmean(cn);
                if (text!=""&&text.length>0)
                {
                	text=text.substring(1);
                    lastlen = j;
                    appendTranslatedWord(stringBuilder, "<i h=''t='"+cn+"'v='"+text+"'>" + toonemeaning(text) + "</i>", lastword);
                    flag = true;
                    i += j;
                    break;
                }
            }
        }
        if (!flag)
        {
            var han = convertohanviet(chinese[i]);
            appendTranslatedWord(stringBuilder, "<i h='"+han+"'t='"+chinese[i]+"'>"+han+"</i>",lastword);
            i++;
        }
    }
    return stringBuilder.join("");
}
function convertohanviet(chi){
	return hanvietdic[chi]||"";
}
function convertohanviets(str){
	var result=[];
	for(var i=0;i<str.length;i++){
		result.push(convertohanviet(str[i]));
	}
	return result.join(" ");
}
function appendTranslatedWord(result,translatedText,lastTranslatedWord)
{
    if (/(\. |\â€œ|\'|\? |\! |\.\â€ |\?\â€ |\!\â€ |\: )$/.test(lastTranslatedWord.data))
    {
        lastTranslatedWord.data = appendUcFirst(translatedText);
    }
    else if (/[ \(]$/.test(lastTranslatedWord.data))
    {
        lastTranslatedWord.data = translatedText;
    }
    else
    {
        lastTranslatedWord.data = " " + translatedText;
    }
    result.push(lastTranslatedWord.data);
}
function appendUcFirst(text)
{
	var result;
	if (!text)
	{
		result = text;
	}
	else if (text[0]=="[" && 2 <= text.length)
	{
		result = "[" + text[1].toUpperCase() + ((text.length <= 2) ? "" : text.substring(2));
	}
	else
	{
		result = text[0].toUpperCase() + ((text.length <= 1) ? "" : text.substring(1));
	}
	return result;
}
function standardizeinput(original)
{
	var result;
	if (!original)
	{
		result = "";
	}
	else
	{
		var text = original;
		var array=["â€œ", "ï¼Œ", "ã€‚", "ï¼š", "â€", "ï¼Ÿ", "ï¼", "ï¼Ž", "ã€", "â€¦"]; 
		var array2=[" â€œ", ", ", ".", ": ", "â€ ", "?", "!", ".", ", ", "..."];
		for (var i = 0; i < array.length; i++)
		{
			text = text.replace(new RegExp(array[i],"g"), array2[i]);
		}
		text = text.replace(/  /g, " ").replace(/ \r\n/g, "\n").replace(/ \n/g, "\n");
		return text;
	}
	return result;
}
function override(funcName,newFunc){
	if(!window.overrideglobal)window.overrideglobal={};
	if(window[funcName]){
		window.overrideglobal[funcName]=window[funcName];
		window[funcName]=function(){
			var _super=window.overrideglobal[funcName];
			newFunc(argument);
		}
	}
}

var speaker={
	utter:false,
	parsed:false,
	senid:-1,
	sentences:[],
	senmap:[],
	hnrgx:/[!â€œâ€]/,
	loadedconfig:false,
	speaking:false,
	autocontinue:(function(l){var v = l && l.hash == "#autocontinue"; return v;})(window.location),
	parseSen:function () {
		var startnd=g(contentcontainer).childNodes[0];
		var allsens=[];
		var sen=[];
		var minsen=[];
		var stack="";
		var pList = q("#" + contentcontainer + " p");
		var pIndex = 0;
		if(startnd.tagName=="P" && pList.length > 0){
			var f = findNextI(pList, 0);
			if(f){
				startnd = f.i;
				pIndex = f.idx;
			}
		}
		while(startnd!=null){
			if(startnd.tagName=="BR"){
				if(sen.length>0){
					allsens.push(sen);
					sen=[];
				}
			}else
			if(startnd.tagName=="I" 
				&& startnd.id[0] != "e" 
				&& !startnd.classList.contains("talk")){
				sen.push(startnd);
			}else 
			if(startnd.nodeType==document.TEXT_NODE || startnd.tagName=="I"){
				if(startnd.textContent.contain("â€œ")){
					if(sen.length>0){
						allsens.push(sen);
						sen=[];
					}
					sen.push(startnd);
				}else if(startnd.textContent.contain("â€")){
					sen.push(startnd);
					allsens.push(sen);
					sen=[];
				}
				else if(startnd.textContent.contain(",")){
				 	sen.push(startnd);
				}
				else if(startnd.textContent.contain(".")){
					sen.push(startnd);
					allsens.push(sen);
					sen=[];
				}else{
					sen.push(startnd);
				}
			}
			startnd=startnd.nextSibling;
			if(startnd==null){
				if(pIndex<pList.length){
					pIndex++;
					var f = findNextI(pList, pIndex);
					if(f){
						startnd = f.i;
						pIndex = f.idx;
						allsens.push(sen);
						sen=[];
					}
				}
			}
		}
		if(sen.length>0){
			allsens.push(sen);
		}
		this.sentences=allsens;
		parsed=true;
		this.senmap = [];
		for(var i=0;i<allsens.length;i++){
			var tx=this.senToText(i);
			this.senmap.push({
				text:tx.trim().replace(/[â€œâ€\.]/g,""),
				type:this.getSenType3(tx)
			});
		}
		for(var i=0;i<allsens.length;i++){
			if(this.senmap[i].type=="vo"){
				for(var co=0;co<15;co++){
					if(i+co>=allsens.length){
						break;
					}
					if(this.senmap[i+co].type!="ve"){
						this.senmap[i+co].type="hn";
					}else{
						this.senmap[i+co].type="hn";
						break;
					}
				}
			}
		}
	},
	getSenType3:function(text){
		var text;
		if(text.contain("â€œ")&&text.contain("â€")){
			return "hn";
		}
		if(text.contain("â€œ")){
			return "vo";
		}
		if(text.contain('!')&&text.contain("?")){
			return "hs";
		}
		if(text.contain("â€")){
			return "ve";
		}
		return "nn";
	},
	getSenType2:function(sen){
		var text;
		for(var i=0;i<sen.length;i++){
			text=sen[i].textContent;
			if(text.contain("â€œ")&&text.contain("â€")){
				return "hn";
			}
			if(text.contain("â€œ")){
				return "vo";
			}
			if(text.contain('!')&&text.contain("?")){
				return "hs";
			}
			if(text.contain("â€")){
				return "ve";
			}
		}
		return "nn";
	},
	getSenType:function(text){
		if(text.contain('!')&&text.contain("?")){
			return "hs";
		}
		if(this.hnrgx.test(text)){
			return "hn";
		}
		return "nn";
	},
	senToText:function(senid){
		var text="";
		var sen=this.sentences[senid];
		for(var i=0;i<sen.length;i++){
			if(sen[i].tagName=="I"){
				if(sen[i].gT().length>0)text+=" "+sen[i].textContent;
			}else
			text+=" "+sen[i].textContent;
		}
		return text;
		//return [text.trim().replace(/[â€œ,â€\.]/g,""),this.getSenType(text)];
	},
	trimNaN: function(v){
		v =	Math.round(v * 10) / 10;
		if(isNaN(v)){
			return 1;
		}
		return v;
	},
	engine: {
		promiseValue: function(v){
			return new Promise(function(r){r(v);});
		},
		getUtter: function(){
			if(window.setting && window.setting.ttsengine){
				var e = window.setting.ttsengine;
				switch (e) {
					case "browser":
						return this.browserEngine();
					case "bing":
						return this.wrappedEngine("bing", {voice:"0"});
					case "bing_male":
						return this.wrappedEngine("bing", {voice:"1"});
					case "stv":
					default:
						return this.stvWrappedEngine();
				}
			}
			var e = this.browserEngine();
			if(!e){
				return this.wrappedEngine("bing", {voice:"0"});
			}
			return e;
		},
		setEngine: function(e){
			setting.ttsengine = e;
			store.setItem("setting", JSON.stringify(setting));
		},
		browserEngine: function(){
			if(!window.speechSynthesis){
				return this.promiseValue(null);
			}
			var voices = window.speechSynthesis.getVoices();
			var isVietnamese = false;
			var voice = false;
			for(var i=0;i<voices.length;i++){
				if(voices[i].lang == "vi-VN" || voices[i].lang.contain("vi")){
					isVietnamese = true;
					if(voices[i].localService == false){
						voice = voices[i];
						break;
					}
				}
			}
			if(!isVietnamese){
				if(this.waitForBrowser && voices.length != 0 ){
					return this.promiseValue(null);;
				}else{
					this.waitForBrowser = true;
					return new Promise(function(resolve){
						setTimeout(function(){
							speaker.engine.getUtter().then(resolve);
						}, 2000);
					});
				}
			}
			var utter=new SpeechSynthesisUtterance();
			if(voice){
				utter.voice = voice;
			}
			return this.promiseValue(utter);
		},
		loadTtsScript: function(){
			return new Promise(function(resolve){
				ui.scriptmanager.load("/stv.tts.js", function(){
					resolve();
				});
			});
		},
		wrappedEngine: function(e, o){
			return this.loadTtsScript().then(function(){
				ttsEngine.init(e, o || {});
				window.STV_SERVER = location.origin;
				var utter = {
					speak: function(){
						if(this.preloadedItem){
							ttsEngine.play(this.preloadedItem);
							this.isWaiting = false;
							this.preloadedItem = null;
							this.onstart();
						}else{
							this.isWaiting = true;
						}
						this.preload();
					},
					text: "",
					nextText: false,
					preloadedItem: null,
					rate: 1,
					pitch: 1,
					volume: 1,
					preload: function(){
						if(this.nextText && !this.isLoading){
							var ref = this;
							this.isLoading = true;
							ttsEngine.requestAudioInstant(this.nextText,this).then(function(audioItem){
								ref.preloadedItem = audioItem;
								ref.nextText = "";
								ref.isLoading = false;
								if(ref.isWaiting){
									ref.speak();
								}
							});
						}
					},
					pause: function(){
						ttsEngine.audio.pause();
					},
					resume: function(){
						ttsEngine.audio.play();
					},
					onend: function(){},
					onstart: function(){}
				};
				ttsEngine.onSentenceEnd = function(){
					utter.onend();
				}
				return utter;
			});
		},
		bingEngine: function(){
			return this.wrappedEngine("bing");
		},
		stvWrappedEngine: function(){
			return this.wrappedEngine("stv");
		}
	},
	loadconfig:function (iswaiter) {
		if(abookhost=="faloo"){
			return;
		}
		if(!this.utter){
			if(!window.speechSynthesis){
				return alert("Thiáº¿t bá»‹ cá»§a báº¡n khÃ´ng há»— trá»£ nghe sÃ¡ch.");
			}
			var voices = window.speechSynthesis.getVoices();
			var isVietnamese = false;
			var voice = false;
			console.log(voices);
			for(var i=0;i<voices.length;i++){
				//console.log(voices[i]);
				if(voices[i].lang == "vi-VN" || voices[i].lang.contain("vi")){
					isVietnamese = true;
					//break;

					if(voices[i].localService == false){
						voice = voices[i];

						break;
					}
				}
			}
			if(!isVietnamese){
				if(iswaiter && voices.length != 0 ){
					alert("ChÆ°a cÃ i Ä‘áº·t tiáº¿ng viá»‡t, nghe sÃ¡ch chá»‰ há»• trá»£ thiáº¿t bá»‹ android, hoáº·c trÃ¬nh duyá»‡t edge, truy cáº­p cÃ i Ä‘áº·t giá»ng nÃ³i trÃªn thiáº¿t bá»‹ vÃ  táº£i tiáº¿ng viá»‡t.");
					return;
				}else{
					setTimeout(function(){speaker.loadconfig(true);}, 2000);
					return;
				}
			}
			this.utter=new SpeechSynthesisUtterance();
			this.utter.lang="vi-VN";
			if(voice){
				this.utter.voice = voice;
			}
			this.utter.onend=function(){
				speaker.readnext();
			}
			if(store.getItem("speaker-flex")=="false"){
				this.flexread=false;
			}
			if(store.getItem("speaker-spd")){
				this.utter.rate=0+store.getItem("speaker-spd");
			}
			if(store.getItem("speaker-pit")){
				this.utter.pitch=0+store.getItem("speaker-pit");
			}
			if(store.getItem("speaker-vol")){
				this.utter.volume=0+store.getItem("speaker-vol");
			}
			if(store.getItem("speaker-auto") == "true"){
				this.autocontinue = true;
			}
		}
	},
	loadconfig2:function (iswaiter) {
		if(abookhost=="faloo"){
			return;
		}
		if(!this.utter){
			return this.engine.getUtter().then((function(u){
				this.utter=u;
				this.utter.lang="vi-VN";
				
				this.utter.onend=function(){
					speaker.readnext();
				}
				this.utter.onstart=function(){
					speaker.preloadNextOnline();
				}
				if(store.getItem("speaker-flex")=="false"){
					this.flexread=false;
				}
				if(store.getItem("speaker-spd")){
					this.utter.rate=0+this.trimNaN(store.getItem("speaker-spd"));
				}
				if(store.getItem("speaker-pit")){
					this.utter.pitch=0+this.trimNaN(store.getItem("speaker-pit"));
				}
				if(store.getItem("speaker-vol")){
					this.utter.volume=0+this.trimNaN(store.getItem("speaker-vol"));
				}
				if(store.getItem("speaker-auto") == "true"){
					this.autocontinue = true;
				}
			}).bind(this));
		}else{
			return this.engine.promiseValue(null);
		}
	},
	readBook:function(retry){
		this.showsetting();
		if(this.speaking){
			return;
		}
		return this.readBook2();
		this.loadconfig();
		if(!this.utter){
			if(!retry)
			setTimeout(function(){
				speaker.readBook(true);
			},3000);
			return;
		}
		if(!this.parsed){
			this.parseSen();
		}
		this.senid=-1;
		this.readnext();
		this.speaking=true;
	},
	readBook2: function(){
		if(this.speaking){
			this.showsetting();
			return;
		}
		this.loadconfig2().then((function(){
			if(!this.parsed){
				this.parseSen();
			}
			//this.senid=-1;
			this.readnext();
			this.speaking=true;
		}).bind(this));
	},
	setPitch(type){
		if(this.flexread==false){
			return;
		}
		if(type=="hs"){
			this.utter.pitch=1.2;
			this.utter.rate=0.7;
		}
		if(type=="hn"){
			this.utter.pitch=1.2;
			this.utter.rate=1;
		}
		if(type=="nn"){
			this.utter.pitch=0.8;
			this.utter.rate=1;
		}
		this.onVUpdate();
	},
	readSen:function(senid){
		var s=this.senToText(this.senid);
		if(!this.utter){
			this.loadconfig();
		}
		this.utter.text=s[0];
		this.setPitch(s[1]);
		this.speak();
	},
	highlightOff:function(id){
		if(id<0)return;
		var s=this.sentences[id];
		if(!s)return;
		for(var i=0;i<s.length;i++){
			if(s[i].tagName=="I"){
				s[i].style.color="inherit";
			}
		}
	},
	highlightOn:function(id, cl){
		if(id<0)return;
		var s=this.sentences[id];
		if(s!=null){
			var firstEle = null; 
			for(var i=0;i<s.length;i++){
				if(s[i].tagName=="I"){
					s[i].style.color=cl || "red";
					if(!firstEle){
						firstEle = s[i];
					}
				}
			}
			try{
				if(firstEle){
					ui.scrollto(firstEle.id, -230, document.body);
				}
				
			}catch(e){}
		}
	},
	readnext:function(){
		this.highlightOff(this.senid);
		this.senid++;
		this.highlightOn(this.senid);
		var s=this.senmap[this.senid];

		if(!this.utter){
			this.loadconfig();
		}
		if(!this.utter){
			return;
		}
		//this.utter.text=s.text;
		if(this.senid >= this.senmap.length){
			this.speaking=false;
			this.senid = -1;
			if(this.autocontinue){
				var n = g("navnextbot");
				n.setAttribute("href", n.href + "#autocontinue");
				n.click();
			}
			this.senmap =[];
			this.sentences = [];
			return;
		}
		this.utter.text=this.nextSenText || s.text;
		if(this.utter.text.length == ""){
			return this.readnext();
		}
		this.utter.nextText = this.utter.text;
		if(this.senid < this.sentences.length){
			convertSenWithGG(this.sentences[this.senid]);
		}
		this.setPitch(s.type);
		this.after(0);
	},
	pause: function(){
		this.speaking = false;
		if(this.utter){
			if(this.utter.speak){
				this.utter.pause();
			}else{
				speechSynthesis.pause();
			}
			this.speaking = false;
		}
	},
	resume: function(){
		if(this.utter){
			if(this.utter.speak){
				this.utter.resume();
			}else{
				speechSynthesis.resume();
			}
			this.speaking = true;
		}
	},
	preloadNextOnline: function(){
		var preloadSen = this.senmap[this.senid + 1];
		if(preloadSen && preloadSen.text.length > 0){
			this.utter.nextText = preloadSen.text;
		}
	},
	after:function(time){
		setTimeout(function(){
			speaker.speak();
		}, time);
	},
	speak:function(){
		//speechSynthesis.speak(this.utter);
		if(this.utter.speak){
			this.utter.speak();
		}else{
			speechSynthesis.speak(this.utter);
		}
	},
	showsetting:function () {
		this.loadconfig();
		var wd=ui.win.create("CÃ i Ä‘áº·t nghe sÃ¡ch");
		var rw=wd.body.row();
		rw.addText("Engine TTS:");
		rw.addPadder();
		var enSel = document.createElement("select");
		var list = {
			browser: "TTS cá»§a trÃ¬nh duyá»‡t",
			stv: "Giá»ng nam Sogou",
			bing: "Giá»ng ná»¯ Bing",
			bing_male: "Giá»ng nam Bing",
		}
		for(var name in list){
			var e = document.createElement("option");
			e.textContent = list[name];
			e.value = name;
			enSel.appendChild(e);
		}
		enSel.addEventListener("change", function(){
			speaker.engine.setEngine(this.value);
			speaker.loadconfig2();
		});
		if(window.setting&&window.setting.ttsengine){
			enSel.value = window.setting.ttsengine;
		}
		rw.appendChild(enSel);
		rw=wd.body.row();
		rw.addText("Ã‚m Ä‘iá»‡u nhá»‹p nhÃ ng");
		var tg = rw.addToggle(function() {
			store.setItem("speaker-flex", this.checked.toString());
			speaker.flexread=this.checked;
		});
		tg.checked=true;
		if(store.getItem("speaker-flex")=="false"){
			tg.checked=false;
		}
		rw=wd.body.row();
		rw.addText("Ghi chÃº: báº­t Ã¢m Ä‘iá»‡u nhá»‹p nhÃ ng sáº½ k thá»ƒ Ä‘á»•i tá»‘c Ä‘á»™ Ä‘á»c vÃ  cao giá»ng");
		rw.style.whiteSpace = "normal";
		rw = wd.body.row();
		rw.addText("Tá»‘c Ä‘á»™ Ä‘á»c: &nbsp;&nbsp;");
		rw.addButton("Cháº­m hÆ¡n","speaker.decSpd()","green");
		var ip = rw.addInput("ip-speakerspd","Tá»‘c Ä‘á»™");
		ip.style.height="25px";
		ip.value=this.trimNaN(this.utter.rate);
		rw.addButton("Nhanh hÆ¡n","speaker.incSpd()","green");
		rw = wd.body.row();
		rw.addText("Cao Ä‘á»™ Ä‘á»c: &nbsp;&nbsp;");
		rw.addButton("Tháº¥p hÆ¡n","speaker.decPit()","green");
		var ip = rw.addInput("ip-speakerpit","Cao Ä‘á»™");
		ip.value=this.trimNaN(this.utter.pitch);
		ip.style.height="25px";
		rw.addButton("Cao hÆ¡n","speaker.incPit()","green");
		rw = wd.body.row();
		rw.addText("Ã‚m lÆ°á»£ng: &nbsp;&nbsp;");
		rw.addButton("Tháº¥p hÆ¡n","speaker.decVol()","green");
		var ip = rw.addInput("ip-speakervol","Ã‚m lÆ°á»£ng");
		ip.style.height="25px";
		ip.value=this.utter.volume > 0 ? this.trimNaN(this.utter.volume) : 1;
		rw.addButton("Cao hÆ¡n","speaker.incVol()","green");
		rw = wd.body.row();
		rw.addText("Tá»± Ä‘á»™ng sang chÆ°Æ¡ng: &nbsp;&nbsp;");
		rw.addPadder();
		var tg = rw.addToggle(function(){
			speaker.setAutoContinue(this.checked);
		});
		tg.checked = this.autocontinue;
		rw = wd.body.row();
		rw.addButton("Táº¡m ngÆ°ng","speaker.pause()","blue w-50");
		rw.addButton("Tiáº¿p tá»¥c Ä‘á»c","speaker.resume()","green w-50");
		wd.show();
	},
	decPit:function () {
		this.utter.pitch-=0.1;
		this.utter.pitch = this.trimNaN(this.utter.pitch);
		store.setItem("speaker-pit",this.utter.pitch);
		try{
			g("ip-speakerpit").value=this.trimNaNText(this.utter.pitch);
		}catch(e){};
	},
	incPit:function () {
		this.utter.pitch+=0.1;
		this.utter.pitch = this.trimNaN(this.utter.pitch);
		store.setItem("speaker-pit",this.utter.pitch);
		try{
			g("ip-speakerpit").value=this.trimNaNText(this.utter.pitch);
		}catch(e){};
	},
	decSpd:function () {
		this.utter.rate-=0.1;
		this.utter.rate = this.trimNaN(this.utter.rate);
		store.setItem("speaker-spd",this.utter.rate);
		try{
			g("ip-speakerspd").value=this.trimNaNText(this.utter.rate);
		}catch(e){};
	},
	incSpd:function () {
		this.utter.rate+=0.1;
		this.utter.rate = this.trimNaN(this.utter.rate);
		store.setItem("speaker-spd",this.utter.rate);
		try{
			g("ip-speakerspd").value=this.trimNaNText(this.utter.rate);
		}catch(e){};
	},
	decVol:function () {
		if(this.utter.volume < 0){
			this.utter.volume = 1;
		}
		this.utter.volume-=0.1;
		this.utter.volume = this.trimNaN(this.utter.volume);
		store.setItem("speaker-vol",this.utter.volume);
		try{
			g("ip-speakervol").value=this.trimNaNText(this.utter.volume);
		}catch(e){};
	},
	incVol:function () {
		if(this.utter.volume < 0){
			this.utter.volume = 1;
		}
		this.utter.volume+=0.1;
		this.utter.volume = this.trimNaN(this.utter.volume);
		store.setItem("speaker-vol",this.utter.volume);
		try{
			g("ip-speakervol").value=this.trimNaNText(this.utter.volume);
		}catch(e){};
	},
	trimNaNText: function(v){
		v = this.trimNaN(v);
		var t = v + "";
		t = t.split(".");
		if(t.length == 1){
			return t[0];
		}
		return t[0]+"."+t[1].substring(0, 1);
	},
	setAutoContinue:function (v) {
		this.autocontinue = v;
		store.setItem("speaker-auto",""+v);
	},
	onVUpdate:function(){
		try{
			g("ip-speakervol").value=this.utter.volume;
			g("ip-speakerspd").value=this.utter.rate;
			g("ip-speakerpit").value=this.utter.pitch;
		}catch(e){};
	}
}
var ntsengine={
	tim:0,
	wordConnector:function(node){
		if(node.nE()!=null&&node.isspace(true)){
			var l=[node,node.nE()];
			if(l[1].nE()!=null&&l[1].isspace(true)){
				l.push(l[1].nE());
			}
			if(l.length>2){
				this.containWord(l
					,function(d){
						l[0].style.border="1px solid green";
						l[0].style.borderWidth="1px 0 1px 1px";
						l[2].style.border="1px solid green";
						l[2].style.borderWidth="1px 1px 1px 0px";
						if(l[2].nE()!=null){
							ntsengine.wordConnector(l[2].nE());
						}
					}
					,function(d){
						l.pop();
						ntsengine.containWord(l
							,function(d){
								l[0].style.border="1px solid green";
								l[0].style.borderWidth="1px 0 1px 1px";
								l[1].style.border="1px solid green";
								l[1].style.borderWidth="1px 1px 1px 0px";
								if(l[1].nE().nE()!=null){
									ntsengine.wordConnector(l[1].nE().nE());
								}
							}
							,function(d){
								ntsengine.wordConnector(l[1]);
							}
						);
					}
				);
			}
			else{
				this.containWord(l
					,function(d){
						l[0].style.border="1px solid green";
						l[0].style.borderWidth="1px 0 1px 1px";
						l[1].style.border="1px solid green";
						l[1].style.borderWidth="1px 1px 1px 0px";
						if(l[1].nE()!=null){
							ntsengine.wordConnector(l[1].nE());
						}
					}
					,function(d){
						ntsengine.wordConnector(l[1]);
					}
				);
			}
		}else if(node.nE()){
			this.wordConnector(node.nE());
		}else{
			console.timeEnd("nts");
		}
	},
	containWord:function (wl,t,f){
		tse.send("005",wl.sumChinese(''),function(){
			if(this.down!="false"){
				t(this.down);
			}else{
				f(this.down);
			}
		});
	},
	retrans:function(){
		var nd=q("#"+contentcontainer+" i")[0];
		console.time("nts");
		this.wordConnector(nd);
	}
}
function overread(){

}
function clearWhiteSpace(){
	var empty = q("#"+contentcontainer+" i:empty");
	for(var i=0;i<empty.length;i++){
		if(!empty[i].isspace(true)&&empty[i].isspace(false)){
			empty[i].previousSibling.textContent="";
			empty[i].previousSibling.isspacehidden=true;
			var crn = empty[i];
			while(crn.pE()&&crn.pE().textContent==""&&crn.pE().isspace(false)){
				crn = crn.pE();
				crn.previousSibling.textContent="";
				crn.previousSibling.isspacehidden=true;
				if(crn.previousSibling.previousSibling.nodeType==3){
					crn.previousSibling.previousSibling.textContent="";
					crn.previousSibling.previousSibling.isspacehidden=true;
				}
			}
			//console.log(empty[i]);
			
		}
	}
	clearDiLastSen();
}
function clearDiLastSen(){
	q("#"+contentcontainer+" i[t=\"çš„\"],#"+contentcontainer+" i[t=\"äº†\"]").forEach(function(e){
		if(e.isspace(false) && (!e.isspace(true) || (e.nE() && e.nE().textContent=="") )){
			e.previousSibling.textContent="";
			e.previousSibling.isspacehidden=true;
		}
	});
}
function nodeIsHan(node){
	if(node.textContent=="")return false;
	var m=node.getAttribute("v");
	if(m==null){
		return false;
	}
	m=m.split("/");

	var percent = 0;
	
	var h=node.gH().toLowerCase().split(" ");
	var l=node.textContent.toLowerCase().split(" ");
	if(l.length<2){
		return false;
	}
	for(var j=0;j<m.length;j++){
		l=m[j].toLowerCase().split(" ");
		for(var i=0;i<l.length;i++){
			if(h.indexOf(l[i]) < 0)
			{
				percent++;
				break;
			}
		}
	}
	if(percent > m.length/3){
		return false;
	}
	return true;
}
function toCnWithName(){
	q("#"+contentcontainer+" i").forEach(function(e){
		if(!e.containName() && !nodeIsHan(e)){
			e.textContent=e.cn;
		}else{
			e.textContent =""+e.textContent+"";
		}
	});
	var a=g(contentcontainer);
	ui.copy(a.innerText);
}
function modvp(){
	phrasetree.setmean(g("modifyvpboxip1").value,g("modifyvpboxip2").value+"="+g("modifyvpboxip3").value);
	phrasetree.save();

//	var params = "ajax=logeditvp&value="
//			+encodeURIComponent(g("modifyvpboxip1").value+"="+g("modifyvpboxip3").value)+"&log="+encodeURIComponent(g("modifyvpboxip2").value);
//	ajax(params,function(down){});
	hideNb();
	replaceVietphrase();
	$("#modifyvpbox").hide();
	syncvpfile("update");
}
function movemeaning(){
	var mean=g('modifyvpboxip3').value;
	if(mean.indexOf("/")>=0){
		var idx=mean.indexOf("/");
		mean=mean.substring(idx+1)+"/"+mean.substring(0,idx);
		g('modifyvpboxip3').value=mean;
	}
	
}
function movehantomean(){
	g('modifyvpboxip3').value=g("modifyvpboxip2").value;
}
function delvp(){
	if(window.priorvp){
		var vptodel=g("modifyvpboxip1").value;
		if(phrasetree.data[vptodel[0]][vptodel]){
			delete phrasetree.data[vptodel[0]][vptodel];
			phrasetree.save();
		}
	}else{
		var vptodel=g("modifyvpboxip1").value;
		if(vptodel[0] in phrasetree.data && vptodel in phrasetree.data[vptodel[0]]){
				delete phrasetree.data[vptodel[0]][vptodel];
				phrasetree.save();
				location.reload();
		}else{
			//var params = "ajax=logdelvp&value="
			//+encodeURIComponent(g("modifyvpboxip1").value)+"&log="+encodeURIComponent(g("modifyvpboxip2").value+" => "+g("modifyvpboxip3").value);
			//ajax(params,function(down){});
			//	alert("NghÄ©a nÃ y chá»‰ tá»“n táº¡i trÃªn mÃ¡y chá»§ vÃ  báº¡n khÃ´ng thá»ƒ xÃ³a. ÄÃ£ gá»­i yÃªu cáº§u xÃ³a.");
		}
	}
}
function deleteName(){
	var nametodel=g("addnameboxip1").value;
	namew.value=namew.value.replace(new RegExp("^\\$"+nametodel+"=.*?$", "gm"),"\n");
	saveNS();
}
function copychinese(){
	  var copyText = g("zw");
	  copyText.select();
	  copyText.setSelectionRange(0, 99999);
	  document.execCommand("copy");
}
function googletrans(a){
	 // var win = window.open("https://translate.google.com/?q="+g(a).value+"&view=home&op=translate&sl=zh-CN&tl=en&text=", '_blank');
	//  win.focus();
	googletranslate(g(a).value);
}
function googlesearch(a){
	var win = window.open("https://www.google.com/search?q="+g(a).value, '_blank');
	win && win.focus();
}
function instrans(e){
	if(phrasetree.getmean(e.value)!=""){
		g("instrans").value=phrasetree.getmean(e.value).split("=")[1];
	}
	else
	tse.send("001",e.value,function(){
		g("instrans").value=this.down;
	});
}
function isNameLv2(){
	return (window.setting && (window.setting.allownamev3 || window.setting.allownamev2));
}
function flatArray( array_of_arrays ){ // stack overflow
    if( ! array_of_arrays ){return [];}
    if( ! Array.isArray( array_of_arrays ) ){ return [];}
    if( array_of_arrays.length == 0 ){return [];}
    for( let i = 0 ; i < array_of_arrays.length; i++ ){
        if( ! Array.isArray(array_of_arrays[i]) || array_of_arrays[i].length == 0 ){return [];}
    }
    let outputs = [];
    function permute(arrayOfArrays, whichArray=0, output=""){
        arrayOfArrays[whichArray].forEach((array_element)=>{
            if( whichArray == array_of_arrays.length - 1 ){ 
                outputs.push( output.trim() +" "+ array_element.trim() );
            }
            else{
                permute(arrayOfArrays, whichArray+1, output.trim() +" "+ array_element.trim() );
            }
        });
    }
    permute(array_of_arrays);
    return outputs;
}
function instrans2(e,isfirst){
		
	ajax("sajax=transmulmean&wp=1&content=a"+encodeURIComponent(e.value),function(down){
		var wl = down.split("|");
		var selec=g("addnameboxip2").previousElementSibling;
		selec.innerHTML="";
		var sox;
		for(var i=0;i<wl.length;i++){
			wl[i] = wl[i].split("/");
		}

		var da=flatArray(wl);
		da.forEach(function(e){
			sox=document.createElement("option");
			sox.setAttribute("value",e.trim());
			sox.innerHTML=e.trim();
			selec.appendChild(sox);
		});
		//=document.createElement("option");
		//sox.setAttribute("value",i3.value);
		//sox.innerHTML=i3.value;
		//selec.appendChild(sox);
		
		g("addnameboxip2").value=selec.children[0].value;
		//if(!isfirst)
		//g("addnameboxip2").value=da[0].trim();
	});
	g("addnameboxip3").value=convertohanviets(e.value).replace(/ +/g," ").trim();
	//tse.send("004",e.value,function(){
	//	//g("addnameboxip3").value=this.down.split("=")[0].replace(/ +/g," ").trim();
	//	g("addnameboxip3").value=this.down.split("=")[0].replace(/ +/g," ").trim();
	//	g("addnameboxip3").value=convertohanviets(e.value);
	//});
	googletranslate(e.value,function(d){
		g("addnameboxip4").value=d;
	});
	ajax("sajax=getnamefromdb&name="+encodeURIComponent(e.value.trim()),function(down){
		var da=down.split("/");
		var selec=g("addnameboxip5").previousElementSibling;
		selec.innerHTML="";
		var sox;
		da.forEach(function(e){
			sox=document.createElement("option");
			sox.setAttribute("value",e.trim());
			sox.innerHTML=e.trim();
			selec.appendChild(sox);
		});
		g("addnameboxip5").value=selec.children[0].value;
	});
}
function getTfcoreSuggest(t,f,ft=""){
	if(window.allowtf === false){return;}
	window.allowtf = false;
	var xhttp =  new XMLHttpRequest();
	xhttp.open("POST","https://comic.sangtacvietcdn.xyz/tfcore.php?noucf=true"+ft);
	xhttp.onreadystatechange = function(){
		if(xhttp.readyState==4 && xhttp.status==200){
			f(this.responseText);
			window.allowtf = true;
		}
	}
	xhttp.send(t);
	setTimeout(function(){window.allowtf = true},1000);
}
function getTfcoreNameSuggest(t,f){
	var xhttp =  new XMLHttpRequest();
	xhttp.open("POST","https://comic.sangtacvietcdn.xyz/tfcore.php?isname=true");
	xhttp.onreadystatechange = function(){
		if(xhttp.readyState==4 && xhttp.status==200){
			var s = this.responseText.split(";");
			var o = {};
			s.forEach(function(e){
				var pair = e.split("=");
				o[pair[0]] = pair[1];
			});
			f(o);
		}
	}
	xhttp.send(t);
	setTimeout(function(){window.allowtf = true},1000);
}
function getBingSuggest(t,f,ft=""){
	if(window.allowbg === false){return;}
	window.allowbg = false;
	var xhttp =  new XMLHttpRequest();
	xhttp.open("POST","https://comic.sangtacvietcdn.xyz/tfms.php?noucf=true"+ft);
	xhttp.onreadystatechange = function(){
		if(xhttp.readyState==4 && xhttp.status==200){
			f(this.responseText);
			window.allowbg = true;
		}
	}
	xhttp.send(t);
	setTimeout(function(){window.allowbg = true},1000);
}
function instrans3(e,isfirst){
	ajax("sajax=transmulmean&wp=1&content=a"+encodeURIComponent(e.value),function(down){
		var vptext = [];
		var wl = down.split("|");
		var sox;
		var total = 0;
		for(var i=0;i<wl.length;i++){
			wl[i] = wl[i].split("/");
			total += wl[i].length;
		}
		if(total < 8){
			var da=flatArray(wl);
			da.forEach(function(e){
				vptext.push(e.trim());
			});
		}else{
			wl.forEach(function(e){
				vptext.push(e.join("/"));
			});
		}
		
		g("modifyvpboxip3").value=vptext.join("/");
		g("modifyvpboxip3").setAttribute("rvalue",vptext.join("/"));
		if(wl.length > 1){
			getTfcoreSuggest(e.value,function(sg){
				g("modifyvpboxip3").value=sg.trim()+"/"+ g("modifyvpboxip3").value;
				g("modifyvpboxip3").setAttribute("rvalue",g("modifyvpboxip3").value);
			});
			getBingSuggest(e.value,function(sg){
				g("modifyvpboxip3").value=sg.trim()+"/"+ g("modifyvpboxip3").value;
				g("modifyvpboxip3").setAttribute("rvalue",g("modifyvpboxip3").value);
			});
		}
	});
	//tse.send("004",e.value,function(){
	//	g("modifyvpboxip2").value=this.down.split("=")[0].replace(/ +/g," ").trim();
	//});
	g("modifyvpboxip2").value=convertohanviets(e.value).replace(/ +/g," ").trim();
	//if(phrasetree.getmean(e.value)!=""){
	//	g("modifyvpboxip3").value=phrasetree.getmean(e.value).split("=")[1];
	//}
	//else{
		//if(isfirst){
		//	g("modifyvpboxip3").value=g("instrans").value;
		//}
		//g("addnameboxip3").value=convertohanviets(e.value).replace(/ +/g," ").trim();
		//tse.send("001",e.value,function(){
		//	g("modifyvpboxip3").value=this.down.trim();
		//});
	//}
	
}
function removeoddvp(){
	var vp = g("modifyvpboxip3").value;
	g("modifyvpboxip3").value = vp.split("/")[0];
}
function openselectvp(){
	var sel = ui.select();
	sel.proc = function(val){
		g("modifyvpboxip3").value = val;
	}
	var vps = g("modifyvpboxip3").getAttribute("rvalue").split("/");
	for(var i=0; i<vps.length; i++){
		sel.option(vps[i],vps[i]);
	}
	sel.show();
}
var isfirsttimeopennamebox = true;
var isbookmanager = false;
function showAddName(){
	g("addnameboxip1").value=i5.value;
	g("addnameboxip3").value=i2.value;
	instrans2(g("addnameboxip1"),true);
	$("#addnamebox").show();
	if(isfirsttimeopennamebox){
		isfirsttimeopennamebox = false;
		checkIsManager();
	}
	if(isbookmanager){
		g("booknamemanager").removeAttribute("hidden");
		if(store.getItem("issavetobook") == "true"){
			g("issavetobook").checked = true;
		}
	}
}
function checkIsManager(){
	ajax("ajax=defaultbooknaming&sub=ismanager&host="+bookhost+"&bookid="+bookid,function(d){
		if(d=="true"){
			isbookmanager=true;
			g("booknamemanager").removeAttribute("hidden");
			if(store.getItem("issavetobook") == "true"){
				g("issavetobook").checked = true;
			}
		}
	});
}
function addNameToBook(name){
	if(g("issavetobook").checked){
		ajax("ajax=defaultbooknaming&sub=addname&bookid="+bookid
			+"&host="+bookhost
			+"&name="+encodeURIComponent(name),function(){});
	}
}
function addSuperName(type,flag){
	var phr="";
	var nname = "";
	if(type=="el"){
		nname="$"+g("addnameboxip1").value+"="+g("addnameboxip4").value;

	//	namew.value="$"+g("addnameboxip1").value+"="+g("addnameboxip4").value+"\n"+namew.value;
	}else if(type=="hv"){
		if(flag=="a"){
			nname="$"+g("addnameboxip1").value+"="+titleCase(g("addnameboxip3").value);

	//		namew.value="$"+g("addnameboxip1").value+"="+titleCase(g("addnameboxip3").value)+"\n"+namew.value;
		}else if (flag=="z") {
			nname="$"+g("addnameboxip1").value+"="+g("addnameboxip3").value;


	//		namew.value="$"+g("addnameboxip1").value+"="+g("addnameboxip3").value+"\n"+namew.value;
		}else if (flag=="f") {
			phr=g("addnameboxip3").value;
			phr=phr.replace(phr.charAt(0),titleCase(phr.charAt(0)));
			nname="$"+g("addnameboxip1").value+"="+phr;

	//		namew.value="$"+g("addnameboxip1").value+"="+phr+"\n"+namew.value;
		}else if (flag=="l") {
			nname="$"+g("addnameboxip1").value+"="+lowerNLastWord(titleCase(g("addnameboxip3").value),1);

	//		namew.value="$"+g("addnameboxip1").value+"="+lowerNLastWord(titleCase(g("addnameboxip3").value),1)+"\n"+namew.value;
		}
		else if (flag=="s") {
			nname="$"+g("addnameboxip1").value+"="+lowerNLastWord(titleCase(g("addnameboxip3").value),g("addnameboxip1").value.length-2);

	//		namew.value="$"+g("addnameboxip1").value+"="+lowerNLastWord(titleCase(g("addnameboxip3").value),g("addnameboxip1").value.length-2)+"\n"+namew.value;
		}
	}else if (type=="vp") {
		nname="$"+g("addnameboxip1").value+"="+g("addnameboxip2").value;

	// 	namew.value="$"+g("addnameboxip1").value+"="+g("addnameboxip2").value+"\n"+namew.value;
	}
	else if (type=="kn") {
		nname="$"+g("addnameboxip1").value+"="+g("addnameboxip5").value;

	//	namew.value="$"+g("addnameboxip1").value+"="+g("addnameboxip5").value+"\n"+namew.value;
	}
	namew.value=nname +"\n"+namew.value;
	addNameToBook(nname);
	$("#addnamebox").hide();
	saveNS();
	excute();
}
function openmodvp(){
	instrans3(g("zw"),true);
	g("modifyvpboxip1").value=g("zw").value;
	g("modifyvpboxip2").value=i2.value;
	$("#modifyvpbox").show();
}
function convertSenWithGG(s){
	return false;
}
function convertSenWithGG2(node){
	var namedb = {};
	var genname = function(n){
	    var name = Math.random().toString(36).replace(/[^a-z]+/g,"").substr(0,5);
	    var name = n;
	    if(!(name in namedb)){
	    	namedb[name] = n;
	    	return name;
	    }else{
	    	return genname(n);
	    }
	}
	var nd = node;
	var sen = [nd];
	while(nd.isspace(true)){
		nd=nd.nE();
		sen.push(nd);
	}
	nd = node;
	while(nd.isspace(false)){
		nd=nd.pE();
		sen.unshift(nd);
	}
	var t = "";
	for(var i =0 ;i<sen.length;i++){
		if(sen[i].nodeType == 3){
			t += sen[i].textContent;
		}else
		if(sen[i].containName()){
			t += " "+genname(sen[i].textContent)+" ";
		}else{
			var m=sen[i].getAttribute("v");
			var m2 = false;
			if(m){
				m=m.toLowerCase().split("/");
				var h = sen[i].gH();
				var hc = 0;
				for(var c=0;c<m.length;c++){
					if(h == m[c]){
						hc++;
					}
				}
				m2 = hc/m.length > 0.4;
			}
			if(m2){
				t += " "+genname(sen[i].textContent)+" ";
			}else
			t+=sen[i].gT();
		}
	}
	//t = t.replace(/ /g,"").trim();
	googletranslatevi(t,function(s){
		for(var n in namedb){
			var r = new RegExp(n, "gi");
			s = s.replace(r, namedb[n]);

			//console.log(s);
		//	speaker.nextSenText = s;
		}
		mergeWord(sen);
		sen[0].textContent=s;
	});
	console.log(t);
	return t;
}
function googletranslatevi(chi,callb){
	var http = new XMLHttpRequest();
	var url = "https://translate.googleapis.com/translate_a/single?client=gtx&text=&sl=zh-CN&tl=vi&dt=t&q=" + encodeURI(chi);
	http.open('GET', url, true);
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	http.onreadystatechange = function() {
		if(http.readyState == 4 && http.status == 200) {
			callb(JSON.parse(this.responseText)[0][0][0]);
		}
	}
	http.send();
}
function getNodeIndex(nodeid){
	if(nodeid[0] == "r"){
		return parseInt(nodeid.substring(3));
	}else if(nodeid[0]=="e"){
		return parseInt(nodeid.substring(5));
	}
	return 0;
}
function TFCoreLn(nodes){
	//return;
	var chi="";
	var sortedNodes = [];
	for(var i=0; i<nodes.length; i++){
		if(nodes[i].push){
			var subarr = nodes.splice(i,1)[0];
			for(var j=0; j<subarr.length; j++){
				nodes.splice(i,0,subarr[j]);
			}
		}
		//chi += nodes[i].gT();
		sortedNodes.push({
			key: getNodeIndex(nodes[i].id),
			txt: nodes[i].gT()
		});
	}
	sortedNodes.sort(function(a,b){ return a.key - b.key; });
	for (var i = 0; i<sortedNodes.length;i++){
		chi += sortedNodes[i].txt;
	}
	mergeWord(nodes);
	if(chi.length < 3){
		return;
	}
	var http = new XMLHttpRequest();
	var url = "https://comic.sangtacvietcdn.xyz/tfcore.php?isln=true";
	http.open('POST', url, true);
	http.onreadystatechange = function() {
		if(http.readyState == 4 && http.status == 200) {
			var t = http.responseText;
			
			nodes[0].setAttribute("t",chi);
			nodes[0].setAttribute("vi",t);
			if(isUppercase(nodes)){
				nodes[0].textContent = ucFirst(t.trim());
			}
			else nodes[0].textContent = t.trim();
		}
	}
	http.send(chi);
}
function TFCoreTranslate(node){
	var text ="";
	var c = g(contentcontainer).childNodes;
	var namemap = {};
	function toSlug(str) {
		str = str.toLowerCase();
		str = str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
		str = str.replace(/[Ä‘Ä]/g, 'd');
		str = str.replace(/([^0-9a-z-\s])/g, '');
		str = str.replace(/(\s+)/g, '');
		return str;
	}
	function mapName(name,chi){
		var sname = toSlug(name);
		//if(sname.split(" ").length > 2){
		//	sname = sname.replace(/ +/g, "");
		//}
		sname = titleCase(sname);
		namemap[sname] = chi;
		return sname;
	}
	for(var i=0;i<c.length;i++){
		if(c[i].tagName=="BR"){
			text += "\n";
		}
		if(c[i].nodeType == 3){
			text += c[i].textContent.trim();
		}
		if(c[i].tagName=="I"){
			if(c[i].containName()){
				text += mapName(c[i].textContent,c[i].gT());
			}else
			text += c[i].gT();
		}
	}
	console.log(namemap);
	TFInit.fromString(text,function(e){
		e.transform();
		var tfm = e.getText();
		for(var name in namemap){
			var r = new RegExp(name, "gi");
			tfm = tfm.replace(r, namemap[name]);
		}
		ajax("ajax=trans&content="+encodeURIComponent(tfm),function(e){
			g(contentcontainer).innerHTML =preprocess(e.substring(1));
			applyNodeList();
			excute();
		});
	});
}
function TFCoreTranslatePage(){
	var text ="";
	var c = g(contentcontainer).children;
	var namemap = {};
	function toSlug(str) {
		str = str.toLowerCase();
		str = str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
		str = str.replace(/[Ä‘Ä]/g, 'd');
		str = str.replace(/([^0-9a-z-\s])/g, '');
		str = str.replace(/(\s+)/g, '');
		return str;
	}
	var sens = [];
	function mapName(name,chi){
		var sname = toSlug(name);
		sname = titleCase(sname);
		namemap[sname] = chi+" ";
		return sname+" ";
	}
    function unMapName(chi){
        for(var n in namemap){
            chi =chi.replace(new RegExp(n,"g"),namemap[n]);
        }
        return chi;
    }
	function getSen(node){
		while(node.pE() && node.pE().tagName !="BR"){
            node = node.pE();
        }
        var sen = {
            text: node.cn,
            start: node.id,
            end: null
        };
        while(node.nextElementSibling && node.nextElementSibling.tagName !="BR"){
            node = node.nextSibling;
            if(node.tagName=="I" && node.containName()){
                sen.text += mapName(node.textContent,node.textContent);
            }else if(node.nodeType==3){
                sen.text += node.textContent.trim();
            }else{
                sen.text+=node.cn;
            }
        }
        if(sen.text.length > 3){
            sen.end = node.id;
            return sen;
        }
        return false;
	}
    function setSen(sen){
        var node = g(sen.start);
        var base = node;
        while(node.nextSibling && node.nextSibling.id!= sen.end){
        	if(node.nextSibling.tagName == "I"){
            	base.cn+=node.nextSibling.cn;
            }else{
            	base.cn+=node.nextSibling.textContent;
            }
            node.nextSibling.remove();
        }
        g(sen.end).remove();
        base.textContent = ucFirst(unMapName(sen.trans));
        base.setAttribute("t",base.cn);
    }
    var criteria = /[çš„]/;
	for(var i=0;i<c.length;i++){
		if(c[i].tagName=="I"){
			if(criteria.test(c[i].cn)){
                var sen = getSen(c[i]);
                if(sen){
                    sens.push(sen);
                    text+=sen.text+"\n\n";
                    for(;i<c.length;i++){
                        if(c[i].id == sen.end){
                            i++;
                            break;
                        }
                    }
                }
            }
		}
	}
	console.log(namemap);
	var xhttp =  new XMLHttpRequest();
    xhttp.open("POST","https://comic.sangtacvietcdn.xyz/tfcore.php?tonly=true");
    xhttp.onreadystatechange = function(){
        if(xhttp.readyState==4 && xhttp.status==200){
            var ss = xhttp.responseText.split("\n\n");
            for(var i=0;i<sens.length;i++){
                sens[i].trans = ss[i].trim();
                setSen(sens[i]);
            }
        }
    }
    xhttp.send(text);
}
function _instanceof(left, right) { if (right != null && typeof Symbol !== "undefined" && right[Symbol.hasInstance]) { return !!right[Symbol.hasInstance](left); } else { return left instanceof right; } }
function _classCallCheck(instance, Constructor) { if (!_instanceof(instance, Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }
function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
var Dictionary = function () {function Dictionary(name,w,t) {
    var load = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;
    _classCallCheck(this, Dictionary);
    _defineProperty(this, "name", "");
    this.name = name;
    var ls = t.split(",");
    for (var i=0;i<ls.length;i++) {
    	this[ls[i].substring(0,w)]=parseInt(ls[i].substring(2));
    }
  }
  _createClass(Dictionary, [{
    key: "index",
    value: function index(key) {
      if (this[key]) {
        this[key]++;
      } else {
        this[key] = 1;
      }
    }
  }, {
    key: "toArray",
    value: function toArray() {
      var l = [];
      for (var k in this) {
        if (this[k] > 3) {
          l.push({
            char: k,
            count: this[k]
          });
        }
      }
      return l;
    }
  }, {
    key: "isPopular",
    value: function isPopular(t) {
      var level = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 3;
      return this[t] > level;
    }
  }, {
    key: "allIsPopular",
    value: function allIsPopular(t) {
      var level = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 3;

      for (var i = 0; i < t.length; i++) {
        if (!this.isPopular(t[i], level)) {
          return false;
        }
      }
      return true;
    }
  }]);
  return Dictionary;
}();
var ichar2=new Dictionary("2char",2,"ä¸œæ–¹158,æ¬§é˜³136,å—å®«115,æ…•å®¹101,ä¸Šå®˜85,é˜´é˜³72,è¥¿é—¨67,ç‹¬å­¤65,å…¬å­™62,æ˜Ÿè¾°56,äº”è¡Œ55,å¤©é­”53,é»„é‡‘52,å¤ªé˜³52,ä¹å¤©50,é»‘æš—48,æ··æ²Œ46,çº³å…°46,é‡‘åˆš43,ä¸æ­»43,ç”Ÿæ­»41,å¹½å†¥41,æ­»äº¡41,æ— æž40,å…ˆå¤©39,å¤©åœ°39,çŽ„å¤©38,é€šå¤©38,å®‡æ–‡38,ç«ç„°37,ä¹¾å¤34,å…‰æ˜Ž34,çš‡ç”«34,çŽ„å†°33,è½©è¾•33,ä¹å¹½33,å¯’å†°33,æ— é‡32,ç™¾é‡Œ32,è¯¸è‘›31,è™šç©º30,ç«¯æœ¨30,ç™¾èŠ±29,é£Žé›·28,æŽå¤©27,ä¸ƒæ˜Ÿ26,ä¿®ç½—26,çƒˆé˜³26,é»‘é¾™26,é’äº‘26,åœ°ç‹±25,é£Žäº‘25,å¤ªå¤25,æ€æˆ®25,çŽ„é˜´25,å¤ªé˜´25,æ··å…ƒ24,ç©ºé—´24,ç‰ç’ƒ24,é€ åŒ–24,å‡¤å‡°24,çŽ„æ­¦23,ç™½éª¨23,ä¸Šå¤23,é‡‘å…‰23,å¤ä¾¯23,å¤©é¾™22,ä¹é¾™22,ç«çµ22,å¤§æ—¥22,é’æœ¨22,é»„æ³‰22,åŒ—å†¥22,ä¸‡å¹´21,ç”Ÿå‘½21,å¦‚æ„21,æ—¥æœˆ21,ç«äº‘21,å¤©é›·20,è½®å›ž20,ä¹é˜´20,å¤§ç½—20,å¤©æœº20,å¤ªä¸Š20,çƒˆç«20,å¤©å‰‘20,æ¥šå¤©20,ä¸ç­19,æ°¸æ’19,åäºŒ19,åžå¤©19,å…«å¦19,ç«é¾™19,çƒˆç„°19,åä¸‰19,åœ°å¿ƒ19,å¤§åŠ›19,å¤©äº‘19,å¤ªè™š19,æœ±é›€19,æµäº‘19,ç™½çŽ‰19,é­”é¾™19,éœ¹é›³19,å¤§åœ°19,é•¿ç”Ÿ19,ä¸ƒå½©18,é€†å¤©18,å¤©ç»18,çµé­‚18,ç¢§æ°´18,é’é¾™18,å¼ å¤§18,èŠ±çŽ‰18,çŽ²ç‘17,é˜´é£Ž17,å†°ç«17,å¤©æ˜Ÿ17,å¤©æ²³17,å¤©ç½¡17,å®Œé¢œ17,åžå™¬17,æ— å½±17,é˜¿å°”17,é£žé¾™17,ä»¤ç‹17,åŽå¤©17,å¼ å°17,çŽ‹å¤§17,ç½—å¤©17,çŽ‹å¤©17,è£‚å¤©16,å…ƒæ°”16,ä¸‰çœ¼16,æ˜Žæœˆ16,å¤©å…ƒ16,é£Žä¹‹16,ä¸–ç•Œ16,åå…«16,ç„šå¤©16,æ°´æœˆ16,ç–¾é£Ž16,ç™½è™Ž16,ç¾½åŒ–16,è™šæ— 16,æš—å½±16,æ¸…é£Ž16,å¶å¤©16,ç´«é‡‘15,ä¸‡å‰‘15,ä¹è½¬15,èŽ²èŠ±15,é»‘é­”15,å†°é›ª15,çº¯é˜³15,å¤§è’15,é­”ç¥ž15,æ¯ç­15,çˆ†ç‚Ž15,è½æ—¥15,ä¸‡é­”15,å—å®®15,æ£®ç½—15,å¼ å¤©15,æ‹“è·‹15,æŽå°15,çŽ‹å°15,çœŸé¾™14,çµè›‡14,äº¡çµ14,å¤©çµ14,å…­åˆ14,åŒå¤´14,é£žå¤©14,å¤©é¦™14,æ¶é­”14,é—ªç”µ14,æ½œé¾™14,çŽ‰å¥³14,æ“Žå¤©14,é’èŽ²14,äº‘å¤©14,å¤©è“14,å¤©é£Ž14,æš´é£Ž14,æž—å°14,æ¾¹å°14,é»„å¤©14,å¶å°14,æ…•æ˜Ÿ14,æŽäº‘14,æŽçŽ‰14,ç™½ç´ 14,ç½—æ·‘14,å¤©ç¥ž13,ä¸‡å¤13,ä¸‰åƒ13,éº’éºŸ13,å¤§å¤©13,ä¼é­”13,ç²¾çµ13,åƒå¹´13,å—œè¡€13,ä¹å¤´13,æµæ˜Ÿ13,å¤©ä¹‹13,å¤©çŽ„13,å¤ªæž13,å¤ªçŽ„13,å¤©é“13,æ— é—´13,é­”æ³•13,æ°´æ™¶13,ç¥žä¹‹13,è¡€ç¥ž13,å¤§åœ£13,å‡Œå¤©13,åœ£çµ13,å¤©å¤–13,è¡€ç…ž13,æŽçŽ„13,æŽè‹¥13,æ¨å¤©13,æž—é›¨13,èµµæ— 13,é»‘é£Ž13,æ¡ƒèŠ±12,åŒ–é¾™12,ä¸Šæ¸…12,ä¹æ›²12,å¤§æ‰‹12,ä¹éœ„12,äº”è‰²12,å¤ºå‘½12,å†°é­„12,ç‚¼ç¥ž12,å¤©ç«12,å±±æ²³12,å¹»å½±12,æ—‹é£Ž12,æœˆåŽ12,æ´ªè’12,çœŸçµ12,é€šçµ12,é‡‘æ¯›12,è¿œå¤12,æ¬¢å–œ12,é£Žç«12,é£˜æ¸º12,å¤©ä¸€12,å¤©å¿ƒ12,å¤©æ¶¯12,å¤©ç½—12,æ–¹å¤©12,ç¥žåœ£12,èµ«è¿ž12,åˆ˜å¤§12,å”å¤©12,å¼ æ–‡12,å¼ æ­£12,æŽå¤§12,æ±Ÿä¸12,çŽ‹é’12,é©¬å°12,è¡€é­”11,è‡³å°Š11,å†°éœœ11,é’çµ11,ä¸ƒç»11,ä¸‡è±¡11,ä¸‰æ˜Ÿ11,ä¸åŠ¨11,å¤§ä¸–11,ç¥žé¾™11,é‡‘é¾™11,ä¹é˜³11,äº‘éœ„11,æ˜Šå¤©11,é€é¥11,ç¦»ç«11,æ°´çµ11,ä»™é“11,å…ƒç¥ž11,å…«è’11,ç ´ç­11,å‘¨å¤©11,ç¥žå‰‘11,ç‚¼æ°”11,å¼€å¤©11,å¦‚æ¥11,æ˜Ÿç©º11,çœŸå…ƒ11,ç ´å¤©11,å¤©å¦–11,çƒˆæ—¥11,ç‹¬è§’11,èœ˜è››11,ç¢§è½11,è‹ç©¹11,é¾™è™Ž11,é»„æ²™11,ä¸œçš‡11,å†°å°11,å†°çµ11,åœŸä¹‹11,å¤©çŽ‹11,å¤©é¹°11,æ˜Ÿäº‘11,æµ·çŽ‹11,ç«ä¹‹11,é“¶æœˆ11,é»‘ç…ž11,å‘¨å¤§11,å­™å°11,å¼ å›½11,å¼ å­11,æŽé’11,æž—äº‘11,æž—å­11,çŸ³å¤©11,å¤©æµ·10,éœ‡å¤©10,ä¸‡çµ10,æš—é»‘10,å¤©ä»™10,å™¬é­‚10,ä¹é‡10,å‡Œäº‘10,ç‚¼å™¨10,äº”å½©10,ç ´ç©º10,ç‚¼é­‚10,ä½£å…µ10,æˆ˜ç¥ž10,å™¬çµ10,å¤©äºº10,å¤ªæ¸…10,æ˜Ÿæ²³10,å…¬ç¾Š10,èµ¤ç«10,æ°´ç«10,çŽ„å†¥10,é•‡é­”10,ç´«ç„°10,ç´«ç”µ10,å¼‘ç¥ž10,é®å¤©10,è“å¤©10,é“ç”²10,é’å¤©10,é»‘æ°´10,ä¸‰ç»10,ä¹å°¾10,å…ƒçµ10,åŽå¤©10,å¤©é˜´10,æ— å10,æ¢¦å¹»10,çµå…½10,ç™½äº‘10,ç™½é©¬10,ç™½é¾™10,ç²¾ç¥ž10,è¡€äº‘10,é‡‘ä¹‹10,é•¿å­™10,é™ˆçŽ‰10,é¬¼çŽ‹10,å­™å¤§10,æŽæ˜Ž10,çŽ‹ä¸€10,è‹ç´«10,é™ˆå¤§10,äº”é›·9,ç­é­‚9,ä¸‡å¦–9,ä¸‡é¬¼9,ä¸‰é˜´9,é‡‘èº«9,ä¸­å¤®9,ä¹ä¹9,ä¹å¶9,ä¹å·ž9,äº‘é›¾9,åœ£é¾™9,å®‡å®™9,å¤§å¸9,ç‹‚é£Ž9,ç¬¬ä¸€9,å¤©å±±9,å¤©ç©º9,å¤©é˜¶9,å­æ¯9,é¾™çˆª9,å·¨çµ9,æ— åŒ9,æš—å¤œ9,æž¯æœ¨9,æµ·å¤©9,æ¶…ç›˜9,ç‚¼ç‹±9,ç„šå¿ƒ9,èµ¤è¡€9,åœ°é¾™9,çŽ„é»„9,ç™¾æ¯’9,ç¥žé­”9,é“¸å‰‘9,é¬¼ç¥ž9,é‡‘è‰²9,é¡»å¼¥9,é»‘è‰²9,ä¸‡å®9,äº‘æ¢¦9,å¸è¡€9,å¤©éƒ½9,å¥¥å°”9,å¾¡å…½9,æ‘„é­‚9,æ­»ç¥ž9,ç ´äº‘9,è¡€é­‚9,é‡‘çŽ‰9,é˜¿é‡Œ9,é›ªæœˆ9,é›·äº‘9,é£Žé›ª9,é£žé¹°9,éª·é«…9,é¾™è¡€9,åˆ˜å¤©9,å¼ æ™“9,å¼ çŽ‰9,æŽå…ƒ9,æŽæ–‡9,æŽæ¸…9,æ¨å°9,æž—å¤©9,çŽ‹å¿—9,çŽ‹æ–‡9,è‚é£Ž9,è´ºä¸€9,é™†å°9,é™ˆå›½9,é™ˆå¤©9,é™ˆå®¶9,å¤©ç‹¼8,æœ¨çµ8,å¼ æ— 8,å¼€å±±8,é£žäº‘8,æŸ³å¦‚8,ä¸€æ°”8,ç©¿å¿ƒ8,ä¸‡åŒ–8,ä¸‡ç‰©8,è›®è’8,ä¸‰é˜³8,åœ°çµ8,å°é­”8,å‡Œéœ„8,ä¹æ˜Ÿ8,äº”æ˜Ÿ8,çˆ†è£‚8,åŠŸå¾·8,å…­é“8,å†°æ™¶8,åŒ–è¡€8,åƒé‡Œ8,åŽŸå§‹8,å¤©ä¸‹8,åå­—8,å…½æ­¦8,å…ƒç£8,å¤§æ‚²8,å¤§è¡8,æ˜Ÿæ˜Ÿ8,å¤©å°¸8,åƒå¹»8,æ±Ÿå±±8,æ— ä¸Š8,æ˜¥ç§‹8,æ³¢ç½—8,æ¸…å¿ƒ8,çµå…‰8,ç†”å²©8,çŒ›è™Ž8,ç™½è‰²8,é»„é¾™8,ç™¾å…½8,ç¥žè¡Œ8,æƒŠå¤©8,ç©¿å±±8,ä¸‰èŠ±8,æœˆå…‰8,ç¹æ˜Ÿ8,èµ¤ç‚Ž8,é‡‘è›‡8,é‡‘é“¶8,é˜¿æ‹‰8,ç«ç¥ž8,é¾™è±¡8,ä¸Šå“8,äº‘ä¸­8,å…‰è¾‰8,å†°é­‚8,åŒ–å½¢8,åŒ–ç¥ž8,å—æ–¹8,å¤©å‘½8,å¤©æ€8,å¤ªå¹³8,å¤ªç™½8,å¥”é›·8,å¯‚ç­8,å°‰è¿Ÿ8,å¼—æ‹‰8,å¾¡å‘½8,æƒŠé¾™8,æ‹“æ‹”8,æ–­é­‚8,æœ¨ä¹‹8,æž—ä¸­8,æ··ä¹±8,æ¸…è™š8,çµæ­¦8,çŽ‰æ¸…8,çœŸæ­¦8,ç´«è‰²8,è“è‰²8,è¡€çµ8,è¥¿æ–¹8,é›·éœ†8,é»„å°8,é»‘äº‘8,åˆ˜æ˜Ž8,å­™æ™“8,æŽå­8,æŽé“8,æŽé•¿8,æ¨çŽ‰8,æž—è‹¥8,æž—é›ª8,æŸ³äº‘8,æ¥šäº‘8,ç§¦å¤©8,è§å¤©8,è¢ç¤¼8,èµµå¤§8,é™ˆå°8,é©¬å¤©8,é¾™å¤©8,èµµå¿—7,å¿ƒé­”7,é”€é­‚7,ç­‘åŸº7,ç­ä¸–7,ä¸‡å…½7,ä¸æœ½7,é‡ç”Ÿ7,å¾¡å‰‘7,ä¹™æœ¨7,å‡¤èˆž7,è½¬è½®7,å›žå¤©7,ç‚¼ä¸¹7,ä¸‡é‡Œ7,äº‘æµ·7,äººæ—7,åœ£å…‰7,æ¸¸é¾™7,å…«æ–¹7,åŒç¿¼7,å…­é˜³7,å°ç¥ž7,åˆ†ç¥ž7,é’å†¥7,è¿žçŽ¯7,åæ–¹7,è¿½é­‚7,å¤©æ‰7,é›·ç”µ7,å››è±¡7,åœ£å¤©7,åœ°ç…ž7,ç¬¬äºŒ7,è‡ªç„¶7,å¤©å¸ˆ7,å¤©ç‹7,å¤©è“¬7,å¤ªä¸€7,çº¢èŽ²7,å¤©æœˆ7,é¾™å‡¤7,éœ¸å¤©7,å½’ä¸€7,å¿ƒçµ7,é¾™è›‡7,æ¯’é¾™7,çµçŠ€7,çƒŸé›¨7,ç‰›é­”7,è½å¶7,çŽ„å…ƒ7,é­”ç„°7,ç™½çœ‰7,ç¢§çŽ‰7,ç¢§çœ¼7,è¡€å…‰7,é“æ‹³7,é“è¡€7,æ´žå¤©7,åŒ–é­‚7,é¸¿è’™7,é»‘ç‹±7,é»‘ç¥ž7,é¾™ä¹‹7,ä¸‰è¶³7,ä¸¹æ­¦7,ä¸¹é’7,äº‘ä¹‹7,äº”é¾™7,å…‹æ‹‰7,å†¥çŽ‹7,å‡Œå¤§7,å¡æ‹‰7,å´å¤§7,å¤§å¤7,å¤©æ™¶7,å¤©æ­¦7,å¤©é’7,å±±æµ·7,å¸ƒé›·7,å¹»çµ7,å½’å…ƒ7,å¾å¤§7,æ¨å¤©7,æ‘˜æ˜Ÿ7,æ‘©ç½—7,æ–©é¾™7,æ— ç©º7,æ˜Ÿæœˆ7,æš—æœˆ7,æ±æ–¹7,æž—å¤§7,æ­»çµ7,æ°´ä¹‹7,æ²§æ¾œ7,æµ®äº‘7,çŽ‹è€…7,ç”µä¹‹7,ç™½èŽ²7,ç™¾è‰7,ç¥žé£Ž7,ç´«å…‰7,ç´«ç«¹7,çºªå…ƒ7,ç½—åˆ¹7,èšçµ7,è…¾é¾™7,è¯çŽ‹7,è©æ7,è¡€æ€7,èµ¤ç‚¼7,èµ¤é˜³7,èµ·æº7,é“ä¹‹7,é“èƒŒ7,é•¿ç©º7,é—»äºº7,é™é­”7,é›·ä¹‹7,é£žä»™7,é½å¤©7,åˆ˜çŽ‰7,åŒ—å ‚7,å¶å›7,å‘¨é•¿7,å®‹çŽ‰7,å¼ äº‘7,å¼ å¿—7,å½©è™¹7,æ…•é“7,æ…•é’7,æ–¹å°7,æœ±é«˜7,æ¨å¤§7,æž—ä½³7,æž—å©‰7,æž—çŽ‰7,æž—é›…7,æ±Ÿæ¸…7,æ·³äºŽ7,çŽ‹å­7,çŽ‹å¾·7,ç”°ä¸­7,ç”³å± 7,ç½—å°7,èƒ¡å°7,è‹å¤§7,è‹æ–‡7,è‹æ˜Ž7,é‡‘å‡¤7,é™ˆæ˜Ž7,é›·å¤©7,é£Žæ— 7,é»„å¤§7,é¾™é›ª7,èµµå¤©6,çŽ„é˜³6,è¡€æµ·6,äº˜å¤6,å°å¤©6,å¤§ä»™6,ç»æ€6,ä¸‡ä»™6,ç‚¼ä½“6,ä¸‡æ³•6,ä¸‰å¤´6,ä¸¤ä»ª6,ä¹å®«6,é­”å¥³6,å±±å²³6,ä¹ä»™6,æ˜ŽçŽ‹6,äº”æ¯’6,è¯›é­”6,åœ£äºº6,ä¿®çœŸ6,ç»å¤©6,å± é¾™6,å…‹é‡Œ6,æ¸¸èº«6,ä¸­å¤©6,åˆ†èº«6,å¤§é­”6,å†°æœˆ6,å†°è“6,åŒ—æž6,ä¸‡æ¯’6,é›·ç¥ž6,ç¢Žæ˜Ÿ6,è‹±é›„6,ç¢Žç©º6,ç­é­”6,å¤§é‡‘6,ç¬¬äº”6,ç¬¬å››6,çŒŽé­”6,å¤©è›‡6,å¤©éŸ³6,å¤ªä¹™6,å¤ªçš‡6,å¤ºå¤©6,å­”é›€6,å¯’é“6,å°çµ6,å°åƒ6,ç¿ çŽ‰6,é›ªçŽ‰6,å‡é¾™6,æ…ˆèˆª6,æ’¼å¤©6,æ— æƒ…6,çœŸæ°”6,é›·å…‰6,ç‹®å­6,æ—­æ—¥6,æ˜“å¤©6,æ˜“ç­‹6,æ— ç”Ÿ6,æœ«æ—¥6,é‡‘æœ¨6,æ°´é¾™6,ç¥žé­‚6,æµ·é¾™6,æµ·æ— 6,æ¸¡åŠ«6,å¹½çµ6,ç‹‚ç‹®6,çŽ„å¦™6,çŽ„ç«6,ç™½é‡‘6,çš‡å¤©6,ç›˜å¤6,çœŸç©º6,ç¢§æµ·6,ä¹¾å…ƒ6,ç¥žå¨6,ç´«æž6,ç´«è™š6,çº¢è‰²6,è“é“¶6,è‹å¤©6,è‹é¾™6,è¯å¸ˆ6,è‘µæ°´6,èœ€å±±6,æ‘©è¯ƒ6,è¡€è‰²6,è¡€é¾™6,è¯›ç¥ž6,æµå…‰6,é“çŽ„6,éƒ½å¤©6,é‡‘ç¿…6,é‡‘è§’6,é‡‘é˜³6,é£Žé›¨6,çŽ‹å®¶6,é‡‘ç”²6,é˜³æ˜Ž6,é˜¿æ–¯6,é™é¾™6,é›ªèŠ±6,æ°´äº‘6,ä¸ƒå¤§6,ä¸‡ä½›6,ä¸‡ç¥ž6,ä¸‡èŠ±6,ä¹Œå…°6,äº¡é­‚6,äººé“6,äººé¢6,å‚²å¤©6,å…½äºº6,åˆ€é”‹6,å‰‘é“6,åŒ—å®«6,åƒæ‰‹6,å¡æ–¯6,å›å¤§6,å¤šå®6,å¤©ç½š6,å¤ªç´ 6,å©†ç½—6,å®‰å¾·6,å®šæµ·6,å¸ƒæ‹‰6,å¹½å½±6,å¼ ä¸‰6,å½¼å²¸6,å¾·å°”6,å¿˜å¿§6,æ–‘æ–“6,æ–¯å¦6,æ— ä¸º6,æ— å­—6,æ˜Ÿç½—6,æœˆäº®6,æœ›æœˆ6,æœé˜³6,æŽè€6,æ°´å…ƒ6,æ´›ç¥ž6,ç«ç‚Ž6,ç«è¡Œ6,ç­ç¥ž6,çµå®6,çˆ±ä¸½6,çˆ±å°”6,çŽ„æ°´6,çŽ„é­”6,çŽ‰çš‡6,çŽ‰é¾™6,çŽ‹é“6,ç™½é›ª6,ç™¾çµ6,ç¢§è¡€6,ç¥žæœ¨6,ç´«äº‘6,çº¢äº‘6,ç»æƒ…6,è‡ªç”±6,è£è€€6,è½éœž6,è“¬èŽ±6,èžºæ—‹6,è¡€å‰‘6,è¯›ä»™6,é˜´å½±6,é›·é¸£6,é’åŸŽ6,é’è¡£6,é¬¼å½±6,é­”çµ6,é»‘çŸ³6,é¾™é³ž6,ä½•å¤§6,å‡ŒäºŒ6,åˆ˜æ­£6,åˆ˜æµ·6,å‰‘ç¥ž6,å¤å‰‘6,å‘¨å­6,å‘¨å°6,å”å°6,åœ£çš‡6,å¤œå‰6,å­™çŽ‰6,å°ç™½6,å¼ ä¸½6,å¾å­6,æ…•å¤©6,æ–¹å‰‘6,æœ›å¤©6,æœ¨é’6,æŽå…‰6,æŽå¾·6,æŽå¿—6,æŽæ€6,æŽæ™“6,æŽæ¢¦6,æŽç¾Ž6,æœäº‘6,æž—äºŒ6,æž—æ™“6,æž—æ¸…6,æž—é’6,æ°´æ¼«6,ç‡•æ— 6,ç‰›å¤§6,çŽ‹å›½6,çŽ‹è€6,çŽ‹é•¿6,ç™½å¤©6,ç™½æ— 6,ç™½æ¸…6,ç¢§äº‘6,ç¬¬å…­6,ç½—äº‘6,èƒ¡å¤©6,èŠ±æ— 6,è‹é›ª6,èŽ«å¤©6,è§å¤§6,è¡¥å¤©6,è£‚å±±6,è´¾æ–‡6,èµµå­6,èµµé£ž6,æŸ³é’5,ç£çŸ³5,é¾™é­”5,æ¢§æ¡5,åœ£é­”5,ä¸€å…ƒ5,ä¸€åˆ€5,ä¸ƒå¶5,é¾™æ¸Š5,ä¸ƒé‡5,åŒå¿ƒ5,é”é­‚5,ä¸‰å°¾5,ä¸‰æ‰5,ä¸‰ç¥ž5,å…«å®5,ç¥žçµ5,é£Žç¥ž5,ä¸œè¥¿5,ä¿®ä»™5,å°å¤©5,å¤©è¾°5,ä¹çŽ„5,ä¹é¼Ž5,ç´«é›·5,è¿·å¹»5,ç½—æ±‰5,é›·éŸ³5,ä¼—æ˜Ÿ5,å…ƒå§‹5,æ›¼é™€5,å…«ä»™5,é•‡æµ·5,æˆ®ä»™5,çœŸé­”5,å†¥ç¥ž5,é¾™é¡»5,ç¢§è“5,æ°´é›¾5,å››ç¥ž5,ä¸‰å 5,ç‚Žé¾™5,åœ°é˜¶5,å¤©å·«5,é¾™æˆ˜5,å¤§æ±Ÿ5,å¤§ç­5,å¤§è‡ª5,ä¼—ç”Ÿ5,å‚€å„¡5,å¤©æ¯’5,å¤©æ°´5,ç¦é­”5,å¤©è’5,åŒ–çµ5,é¸³é¸¯5,å¤§æ˜Ž5,å°‘æž—5,å±±åœ°5,å’†å“®5,å´©å±±5,è£‚åœ°5,å¸ƒå…°5,å¸çŽ‹5,å¹»é˜´5,å¹¿å¯’5,å¼¥ç½—5,æ‹ˆèŠ±5,ç ´è™š5,æ–¯å¡”5,æ— ç•5,é›·å¸5,æš´é›¨5,é£“é£Ž5,æ³¢åŠ¨5,æžé˜´5,æ ¼æ‹‰5,æ®‹è¡€5,ä¹æœˆ5,å¹½é­‚5,æ±ŸæŒ¯5,æ´—é«“5,æµ©ç„¶5,æ·±æµ·5,æ¸…æ˜Ž5,ç‡•å­5,ç‰›å¤´5,æŽ§æ°´5,ä¹çµ5,çŽ„æ˜Ž5,çŽ„çµ5,çŽ„éƒ½5,ç™¾åˆ5,çŽ„é“5,çŸ³ä¸­5,é‡‘ç›5,ç¥žéœ„5,ç¥žé­„5,ç´«æ™¶5,ç´«çŽ‰5,ç¥žé›·5,ç­å¤©5,ç½ªæ¶5,é£žå‡5,ç¿»äº‘5,é»‘é‡‘5,è‹èŽ½5,è¡€æ™¶5,èµ¤æ˜Ž5,èµ¤ç„°5,ç´«é˜³5,å¼¥é™€5,æ‹‰æ–¯5,é‡‘ä¸5,é‡‘äº‘5,é‡‘æ²™5,å¤§é¹5,å¹»é­”5,é˜¿å…‹5,é“ç¾½5,éª‘å£«5,é”¦ç»£5,é•¿åºš5,åšå°”5,é™¨æ˜Ÿ5,å†’é™©5,é£Žçµ5,é£Žé¾™5,é£˜äº‘5,é£žæ˜Ÿ5,é»‘ç™½5,é»‘é“5,ç‹¼ç‰™5,é¾™åŸ5,é¾™å½¢5,ä¸ƒçŽ„5,ä¸‡é­‚5,ä¸è€5,ä¸œåŽ5,ä¸œæµ·5,ä¹å½©5,äº‘é¾™5,ä»™äºº5,ä»™çµ5,å…‰ä¹‹5,å…«å¤§5,å…½ç¥ž5,å…½é­‚5,å†°é›·5,å‡è¡€5,å‡ºçª5,åˆ‘å¤©5,åŒ—æ–¹5,å—å¤©5,å¤æœˆ5,å¶å¤§5,å¶å­5,åˆä½“5,å‰ç¥¥5,å›è€5,å”è€5,å™¬è¡€5,åœ£çŽ‹5,åœ°ç«5,åœ°è¡Œ5,å¤§å‘¨5,å¤§æˆ5,å¤§çµ5,å¤§é“5,å¤©å ‚5,å¤©å¯’5,å¤©ç¾½5,å¤ªå²5,å¦–ä¸¹5,å¦–é­”5,å®¡åˆ¤5,å°‘ç‚Ž5,å·¦æ‰‹5,å·¨é¾™5,å¹»ä¹‹5,å¹½æœˆ5,å½±å­5,å¾è€5,å¾¡é£Ž5,å¿ƒå‰‘5,æƒŠäº‘5,æˆ˜å¤©5,æ‰§æ³•5,æ–°æœˆ5,æ–¹æ­£5,æ—¥è€€5,æš´é›·5,æš´é¾™5,æ›¹å¤©5,æœˆå½±5,æœˆç¥ž5,æžé“5,æ ¼æ–—5,æµ·ç¥ž5,æ·±æ¸Š5,æ··å¤©5,æ¸…çµ5,æºå¤©5,æ¿®é˜³5,ç­ç»5,çµçœ¼5,çŽ‰é¢5,çŽ‹å°‘5,ç³ç…5,ç’‡çŽ‘5,ç”µé›·5,ç–¯é­”5,ç™½çµ5,ç™½è¡£5,ç™½é“¶5,ç™½é¹¤5,ç™½é¹­5,ç™½é¹¿5,ç›˜é¾™5,ç¥žæœº5,ç§‘å°”5,ç©ºçµ5,ç²¾å…ƒ5,ç´ å¥³5,ç´«æœˆ5,ç´«ç½—5,ç´«éœž5,çº¢å‘5,çº¢ç²‰5,ç»ƒä½“5,ç¿¡ç¿ 5,è†æ£˜5,èŽ«åˆ©5,èŽ«å°‘5,è¨å°”5,è—å‰‘5,è—æ˜Ÿ5,è™šå¤©5,è´è¶5,èŸ é¾™5,è¡€è¡£5,è´ºå…°5,èµ¤è‰²5,è¶…çº§5,è¿·é›¾5,é“å¾·5,é—å¿˜5,é‡‘å…ƒ5,é‡‘å¤§5,é‡‘çœ¼5,é‡‘çŸ³5,é“æœ¨5,é“¶ç¿¼5,éšé£Ž5,éšé¾™5,é›·å…¬5,é’ä¸˜5,é¢„è¨€5,é£Žæœˆ5,é£Žæµ5,é­”å¤©5,é­”å¹»5,é­”çŽ‹5,é»„äº‘5,é»‘å¤©5,é»‘çƒŸ5,é»‘è™Ž5,é¾™ç¥ž5,äºŽæ–‡5,å†·æ— 5,å‡Œä¸‰5,åˆ˜ä¸€5,åˆ˜å°5,åˆ˜å»º5,åˆ˜å¿—5,åˆ˜æ–‡5,åˆ˜æ™“5,åŽå°5,å«å¤©5,å¤å¤©5,å¶å­¤5,å¶æ— 5,å›èŽ«5,å‘¨æ–‡5,å¤œæ— 5,å¤©è¿5,å¤ªå”5,å¥‰å¤©5,å§¬é•¿5,å®‰å°5,å¼ ä¼¯5,å¼ å¾·5,å¼ æ˜Ž5,å¼ æ˜¥5,å¼ æ³½5,æ–¹æ–‡5,æŽä¿®5,æŽå†°5,æŽå°‘5,æŽæ…•5,æŽæˆ5,æŽé“5,æž—æ–‡5,æž—éœ‡5,æ®·æ— 5,æ°´åƒ5,æ°´æ— 5,æ±Ÿå¤©5,æ±Ÿæµ©5,æ³•æ‹‰5,ç«éºŸ5,ç‚¼å¦–5,ç‡•èµ¤5,çŽ„å…µ5,çŽ‰æ— 5,çŽ‹å…‰5,çŽ‹å®ˆ5,çŽ‹æ˜Ž5,çŽ‹æ™“5,çŽ‹é“5,ç”°ä¸5,ç”°å¤§5,ç™½ä¸–5,ç™½å­5,ç™½ç§€5,ç§¦å°5,ç§¦æ˜Ž5,ç¬¬ä¸ƒ5,ç½—å¤§5,ç½—æµ®5,è‚é’5,èƒ¡ä¸€5,èƒ¡é’5,è‹å°5,è‹é’5,èŽ«å°5,è§çŽ‰5,è°¢å°5,è³ˆçŽ‰5,è´¾çŽ‰5,èµµä¸–5,èµµå…‰5,èµµæ˜Ž5,èµµæ™“5,èµµè‹¥5,èµµé›…5,è¾¾å¥š5,é‰´å®5,é“ä¸­5,é•‡å¦–5,é•‡é­‚5,é™†å¤§5,é™ˆå­5,é™ˆæ€5,é™ˆæ™“5,é›ªèŽ²5,é›·éœ‡5,éŸ©å°5,é©¬å…ƒ5,é½äº‘5,å­åˆ4,é‡‘é’±4,ç§¦é›ª4,å†·å‡4,çŽ‹ä¸½4,é›·ç‹±4,å›å¤©4,ä¸€å‰‘4,ä¹å…ƒ4,ä¸€çº¿4,ä¸ƒè½¬4,è¿·è¸ª4,é¬¼çµ4,ä¸‡æ¶4,å¤ºç¥ž4,èŽ²å¿ƒ4,ä¸‰å¶4,ä¸‰å±±4,æ¯’ç«4,ä¸‰è‰²4,è›®ç‰›4,é”»ä½“4,ä¸Šå¤©4,è‡ªåœ¨4,å—åŒ—4,ä¸¤æž4,ä¹Œäº‘4,ä¹Œé‡‘4,ä¹åŠ«4,é¾™å…ƒ4,çµå‡¤4,ç¤¾ç¨·4,ä¹æ–¹4,è¯•ç‚¼4,å›°é­”4,ä¹è›‡4,å¤©é˜³4,è¿˜é­‚4,è›‡å½¢4,é‡‘èŠ±4,çœŸç«4,äº”è½¬4,ç´«è¡€4,å€šå¤©4,å…ƒç´ 4,å¬å”¤4,ç´«æ°”4,å…‹èŽ±4,é‡‘æ™¶4,ç ´é­”4,å¯’å…‰4,ç¥žè¯4,æ½®æ±4,æ€äºº4,åƒå½±4,åƒé‡‘4,åŽå¤4,æ°´å¦–4,å››ç¿…4,æ— å½¢4,åœ£åŸŸ4,ç”Ÿçµ4,åŸƒå°”4,å¤§å…‰4,é˜´é­”4,å¤§é™†4,å¤§é¾™4,å¤©å—4,æ€ç”Ÿ4,å¤©ç©¹4,å¤©é—¨4,å¤©é­‚4,èžè¡€4,è‡³é˜³4,å¸çš‡4,è’èŠœ4,å¤ªé»„4,å¥¥æ–¯4,ç¥–ç¥ž4,å°å‘¨4,å°é¾™4,å·¨é­”4,é‡‘ä¹Œ4,é£Ÿäºº4,å·«å¦–4,ç¥žå¥³4,è¨å¸ƒ4,é£Žå¤§4,çŽ„å¥³4,å¹»éŸ³4,åƒå˜4,å¼±æ°´4,å¤©é‚ª4,å¤§å®—4,çš‡å¤ª4,æ‹‰å°”4,æ‘©äº‘4,æ–¯ç§‘4,æ— æˆ‘4,æ˜Ÿé¾™4,æ— è‰²4,æ— éª¨4,å±±æ°´4,æ˜Ÿæ–—4,æ˜Ÿè¡4,æ¢¨èŠ±4,é¾™å®«4,æžä¹4,ç‰¹ä¸½4,ç»ä¸–4,å‰‘é­‚4,æ±Ÿå—4,ç ´æµª4,æ²§æµ·4,è¯é“4,ç¢ŽçŽ‰4,å´©å¤©4,ç²¾è‹±4,é¾™çŽ‹4,æ–­è‚ 4,ç‹®çŽ‹4,ç‹©çŒŽ4,ç¥žæ°´4,çŽ„èŠ±4,çŽ‰è™š4,çŽ°åœ¨4,çˆè“4,é¹°çˆª4,ç™¾å¹»4,ç™¾è„‰4,é£˜é¦™4,å…½çŽ‹4,ç¢Žéª¨4,é›·ç«4,çŽ„å‡¤4,å®šæ˜Ÿ4,ç²¾é‡‘4,çœŸé›·4,ç´«å·4,ç´«å¿ƒ4,ç´«çº¹4,çº¯é˜´4,å›žæ—‹4,ç»¿æ°´4,äº”å…‰4,ä¹±èˆž4,å± ä»™4,è‡³é«˜4,å°é‡‘4,è“å±±4,å°å°4,è¡€æœˆ4,èµ¤æ°´4,è„±èƒŽ4,è¾¾æ‹‰4,è¿‡åŽ»4,è¿Žé£Ž4,ç½—ç”Ÿ4,é€é¹¿4,é‡æ°´4,é‡‘å† 4,é‡‘æˆˆ4,é¾™é˜³4,é‡‘é’Ÿ4,é‡‘é£Ž4,ç¥žå¤©4,é•¿æ±Ÿ4,é›¾äº‘4,é˜´é­‚4,é˜¿ç‰¹4,é›·é¾™4,é’ç«¹4,æ¸¸å¤©4,æµç«4,æ“’é¾™4,é£žçµ4,çˆ†ç‚¸4,é«˜çº§4,èšå…ƒ4,åœ£åœŸ4,éº¦å…‹4,é»‘æ›œ4,é»‘ç„°4,çŽ„ç…ž4,é»‘ç”²4,é¾™çº¹4,ä¸ƒå‰‘4,ä¸ƒæ€4,ä¸ƒé¾™4,ä¸‡é¾™4,ä¸‰æ¸…4,ä¸‹å“4,ä¸è´¥4,ä¸œå—4,ä¸¤ç•Œ4,ä¸­å“4,ä¹å¤§4,ä¹å­—4,äº‘å²š4,äº‘èŽ±4,äº‘é›¨4,äº‘éœž4,äººé±¼4,ä»™å¥³4,ä½›é—¨4,å…ƒå©´4,å…‹ç½—4,å†°ä¹‹4,å†°æµ·4,å†°çŽ‰4,å‡Œæ™¨4,å‡Œæ³¢4,å‡å…ƒ4,å‡ç¥ž4,åˆ¹é‚£4,å‹¿é“4,åŒ–è›Ÿ4,åŒ–éª¨4,åŒ—å±±4,åŒ—æµ·4,åŒ—çµ4,åä¹4,åŠç¥ž4,å—è’4,å¡å¸ƒ4,å¡ç‰¹4,å¡ç±³4,å§é¾™4,åˆæ¬¢4,å¬é£Ž4,å´å¤©4,å‘¼å»¶4,å“ˆå°”4,å”å¤§4,å››å¤§4,å››æ–¹4,å››æž4,å››çµ4,åœ†æœˆ4,åœŸè¡Œ4,åœ°çº§4,åŸƒæ–¯4,åŸŸå¤–4,å¤§ä¹˜4,å¤§ä¹¾4,å¤§å®‰4,å¤§æ¢¦4,å¤§æ²³4,å¤§æµ·4,å¤§æ¸…4,å¤§é›·4,å¤©å¨4,å¤©å°˜4,å¤©å¸4,å¤©æ®‹4,å¤©ç…ž4,å¤©è‰4,å¤©è±¡4,å¤©é©¬4,å¤ªå…ƒ4,å¥‡è¿¹4,å¦–å…½4,å¦–çš‡4,å¦–ç²¾4,å§‹ç¥–4,å®‡å¤©4,å¯’éœœ4,å°ä¸‰4,å²©æµ†4,å²©çŸ³4,å·¦ä¸˜4,å·«å¤©4,å¸ƒç½—4,å¸Œå°”4,åºžå¤§4,å¼ è€4,å¼ºå¤§4,å¾€ç”Ÿ4,å¿˜æƒ…4,å¿ ä¹‰4,æ’å®‡4,æ‚¬æµ®4,æƒŠæ¶›4,æƒŠé›·4,æ‰‹ä¸‰4,æŠ±å…ƒ4,æ‹‰å…‹4,æŽ§ç«4,æ–‡å­4,æ–—æˆ˜4,æ–©ç¥ž4,æ–­åˆƒ4,æ–­é¾™4,æ–¯å›¾4,æ–¯ç‰¹4,æ—…è€…4,æ— é™4,æ˜Žå¿ƒ4,æ˜Žæ—¥4,æš—ä¹‹4,æœˆçµ4,æœˆèˆž4,æœ¨ç¥ž4,æœ¬æº4,æœ±å…ƒ4,æžå“4,æž—è€4,æž¯è£4,æŸ³ç”Ÿ4,æ°¸ç”Ÿ4,æ±‰æœˆ4,æ³•ç¥ž4,æ³¢å°”4,æ³£è¡€4,æ´›è€4,æµæ°´4,æµ©æ¸º4,æµ®å± 4,æµ®ç©º4,æµ·ä¹‹4,æµ·å¦–4,æ»´è¡€4,ç«å±±4,çµå…ƒ4,çµåŠ¨4,çµå±±4,çµç•Œ4,çƒ½ç«4,ç‹‚æš´4,çŽ„æœº4,çŽ„é‡4,ç‘¶æ± 4,ç™»å¤©4,ç™½æ°´4,ç™¾å˜4,çœŸç¥ž4,ç ´å†›4,ç¥žæœˆ4,ç¥žæžª4,ç¥žè™š4,ç¥žé“4,ç¥žé¹°4,ç¦»å¤©4,ç¦»æ¨4,ç§˜æ³•4,ç§©åº4,ç±³ç‰¹4,ç´«å®µ4,ç´«åºœ4,ç´«æ¸…4,ç´«ç«4,ç´«èƒŒ4,ç´«èŽ²4,ç´«é¾™4,çº¢å°˜4,ç¼šé¾™4,ç¼©åœ°4,èšæ°”4,è‰å‰ƒ4,èŽ«å°”4,èŽ±èŒµ4,è§ç§‹4,è¨æ‹‰4,è“å…‰4,è“æœˆ4,è“æ¢¦4,è—å¤©4,è™šç¥ž4,è›‡è¡Œ4,è¶èˆž4,è¡€å½±4,è¡€æ²³4,è¡€ç‚Ž4,è¡€çº¹4,è¡€èŽ²4,èµ¤æœˆ4,èµ¤é‡‘4,èµµå°4,è½¬ç”Ÿ4,è¾‰ç…Œ4,è¾Ÿé‚ª4,è¾¾å…‹4,è¿·å¤±4,è¿½é£Ž4,é‚ªçµ4,é‚ªé­”4,éƒ­è€4,é‡‘å¶4,é‡‘èŽ²4,é’Ÿç¦»4,é•¿æ˜¥4,é—®å¤©4,é˜ŽçŽ‹4,é˜Žç½—4,é˜¿å¾·4,é›ªå±±4,é›ªé­”4,é›·çµ4,é›¾æµ·4,é’å…ƒ4,é’å±±4,é’çŸ³4,é£Žæš´4,é­”è¡€4,é­”é¬¼4,é»„åŸ”4,é»„æ˜4,é»„é£Ž4,é»‘è¢4,é»‘é¹ž4,é¾™åŠ›4,é¾™çµ4,é¾Ÿæ¯4,ä¹±é­”4,äº‘è‹¥4,äº‘é’4,äº‘é£Ž4,äººé—´4,ä»»ä¸œ4,ä»»å¤©4,ä»»é’4,ä½•ä¸½4,ä½•å›½4,ä½™å­4,ä¿žå°4,å‚…å›4,å…¬å­4,å…»é­‚4,å†¯å¤§4,å†¯å°4,å†°å¿ƒ4,å‡Œè‹¥4,åˆ€ç–¤4,åˆ˜ä¸–4,åˆ˜ä¼¯4,åˆ˜å…‰4,åˆ˜å®š4,åˆ˜å¾·4,åˆ˜æ¢¦4,åˆ˜æµ©4,åˆ˜é›ª4,åŽäº‘4,å¡è¥¿4,å¤è‹4,å¶å‡Œ4,å¶å‰‘4,å¶å¦‚4,å¶çŽ‰4,å¶è½»4,å¶é•¿4,å‘ä¹‹4,å›å­4,å›æ— 4,å´æ–‡4,å‘¨å‰‘4,å‘¨èŠ·4,å”äº‘4,å”æ–‡4,å¤§åˆ€4,å¤§å‰‘4,å¤ªå’Œ4,å§œå¤©4,å§¬äº‘4,å§¬å¤©4,å­Ÿå£«4,å®‡æ— 4,å®‹å¤©4,å®‹æ–‡4,å¯’æœˆ4,å°çµ4,å°çŸ³4,å°é’4,å²³å­4,å·¦åƒ4,å·´å›¾4,å·´å°”4,å¼ ä¸œ4,å¼ äºŒ4,å¼ ä»²4,å¼ å­¦4,å¼ å®‡4,å¼ å°‘4,å¼ æŒ¯4,å¼ æµ·4,å¼ æ¸…4,å¼ ç™¾4,å¼ ç§€4,å¼ è¿œ4,å¼ é“4,å¾ä¸–4,å¾å…ƒ4,å¾æ–‡4,å¾æ™“4,å¾è‹¥4,å¾é’4,å¾¡çµ4,æ€’è›Ÿ4,æ‚¬ç©º4,æ…•çŽ„4,æ…•é£ž4,æ‰¶æ¡‘4,æ†ä»™4,æ–©å¤©4,æ–¹ä»¤4,æ–¹å¤§4,æ–¹å¦‚4,æ˜“å¤§4,æ˜Ÿç¥ž4,æœˆå¤©4,æœå¤©4,æœ¨å©‰4,æœ±å¤§4,æœ±å­4,æŽä¸€4,æŽä¸‰4,æŽä¸–4,æŽä¸œ4,æŽä¹4,æŽä»²4,æŽå‰‘4,æŽå‘4,æŽå˜‰4,æŽå­˜4,æŽå®—4,æŽå®¶4,æŽå¸ˆ4,æŽå»º4,æŽå¿ 4,æŽæ˜Œ4,æŽæ˜“4,æŽæ­¦4,æŽçˆ±4,æŽç§‹4,æŽçº¢4,æŽé£ž4,æœæ–‡4,æœæœˆ4,æ¨å¦‚4,æ¨å­4,æ¨å´‡4,æ¨æ˜Ž4,æž—ä¸€4,æž—å…ƒ4,æž—å†°4,æž—å›4,æž—å¦‚4,æž—æ˜Ž4,æž—æœˆ4,æž—ç”Ÿ4,æž—ç´ 4,æž—èŠ·4,æž—è¿œ4,æž—é•¿4,æž—é£ž4,æŸ³å«£4,æŸ³å¯’4,æŸ³æ²³4,æŸ³æ¸…4,æŸ³çŽ‰4,æ –å‡¤4,æ®µå°4,æ®·å¤©4,æ°´å¤©4,æ°´æ¢¦4,æ°´è‹¥4,æ±Ÿå°4,æ²‰å¸Œ4,æµ·äº‘4,æµ·è“4,æ»•æ°¸4,çµè¯4,çµé¹«4,çƒˆéš4,ç‰§é‡Ž4,çŽ‰æ–©4,çŽ‹ä¸–4,çŽ‹å»º4,çŽ‹æ³½4,çŽ‹é›ª4,çå®4,ç”˜æ²4,ç”³å»º4,ç™½å›4,ç™½å°4,ç™½æ–‡4,ç™½æ™¯4,çŸ³å¤´4,ç¢§é³ž4,ç§‹æ°´4,ç§¦æ…•4,ç§¦æœˆ4,ç¨‹è‹±4,çº¢æœˆ4,èŠ±ä¸½4,èŠ±å¤§4,èŠ±æœˆ4,èŠ±ç‘·4,è‹è¿œ4,è‹é›¨4,è€å¤©4,è†å°4,è§å­4,è§è¿œ4,è§é£Ž4,è½é­‚4,è’‹äº‘4,è¡€ç‹¼4,è®¸æ˜Ž4,è°¢æ–‡4,è°¢æ™“4,è°¢çµ4,è°¢çŽ‰4,è´ºä¸½4,è´ºå­4,èµµä¸€4,èµµä¸½4,èµµå…¬4,èµµåŒ¡4,èµµåŠ4,èµµå›½4,èµµå¸ˆ4,èµµå¾·4,èµµæˆ4,è¿ªå¡4,éƒ­äº‘4,éƒ­å¤§4,éƒ­å­4,éƒ­å°4,é‡‘å¤ª4,é‡‘æž—4,é’Ÿæ— 4,é“å‰‘4,é“å£4,é—ªé›·4,é˜´å¤©4,é˜´æ— 4,é™†å¤©4,é™†å­4,é™†æ–‡4,é™†è€4,é™ˆå…‰4,é™ˆå‡¤4,é™ˆå‹4,é™ˆæ€¡4,é™ˆæ–‡4,é™ˆæ˜¥4,é™ˆæ­£4,é™ˆæ°¸4,é™ˆæµ·4,é™ˆæ·‘4,é›¨å¸ˆ4,é’å…‰4,é’å²©4,éŸ©çŽ‰4,é¡¹å¤©4,é¡¾å¤§4,é¡¾é•¿4,é£Žå·4,é£Žè¡Œ4,é£˜é›ª4,é©¬æ™“4,é©¬çŽ‰4,é«˜å¤©4,é­æ˜Ž4,é­”æ‹³4,é­”ç¤¼4,é»„å»º4,é»„æ–‡4,é»Žæ˜Ž4,é»‘çš‡4,é¾™æ— 4,é¾™çŽ‰4");
var ichar3=new Dictionary("3char",1,"å¤©1815,å¤§1054,ç¥ž849,ä¹‹811,æŽ750,çŽ‹679,å°652,çµ639,äº‘625,é¾™613,æž—562,å‰‘552,å¼ 548,çŽ‰525,é­”514,é‡‘507,æ— 440,é’427,é£Ž411,ä»™410,ç™½398,ç½—377,é™ˆ371,æ˜Ÿ362,æœˆ338,èµµ338,å¶334,å…ƒ319,é“319,çœŸ314,é›·314,æ–‡311,çŽ„305,æ°´304,è¡€302,æ–¹300,æµ·299,é»„297,é˜³293,åˆ˜289,è€284,åœ£284,å‘¨283,æ˜Ž281,ç«278,å±±276,æ¨270,é›ª265,å­265,ä¸‡257,ä¸€244,æ¸…241,é»‘236,å…¬236,èŠ±233,å†°232,ä¸œ231,æŸ³230,é£ž227,ç´«222,ä¸‰219,å¿ƒ219,ç§¦218,è‹217,è§216,å­™215,ä¹210,å¤209,é©¬203,é•¿197,åƒ196,é“192,çŸ³192,è¥¿192,é­‚189,å‡Œ189,å¸185,å¤ª184,æ±Ÿ182,å”180,å¸ˆ178,æœ¨175,å°”174,ä¸–173,å®173,çº¢172,å…‰172,é›¨166,åŽ166,å¾·166,å—165,æœ±165,æ¥š159,æ–¯157,çš‡156,èŽ«156,æ­¦155,æ…•154,å¯’153,ç™¾152,å…°152,é˜´151,è‹¥149,å‡¤149,å®‰146,ä¸­144,å¦–143,å¾142,ä½•141,æˆ˜141,è“141,åœ°141,æ¢¦140,å…‹140,æ™“140,å¦‚137,ä¸136,é«˜136,æ³•135,å´135,å›133,æ‹‰133,å®‹131,å¤129,è°¢127,äºº126,å°‘125,ä¸½125,å¡124,é™†124,æ²ˆ123,é¬¼123,é˜¿123,ä¸ƒ116,éŸ©116,åŒ–115,å›½114,é‡Œ114,å®¶113,ä¸¹112,é½112,èƒ¡111,ç©º110,æ°”109,ä¸Š107,æœ107,äº”105,å¿—105,æˆ104,æ­£103,æ´›103,åŒ—102,ç¢§102,éƒ­102,è‹100,å…ˆ99,ç”Ÿ99,ç§‹98,éƒ‘97,æ¬§97,ç¨‹97,å…«96,é¦™96,èµ¤95,åˆ€94,ç ´94,æ€94,å››93,è®¸93,ç”°92,é›…91,å­¦91,çƒˆ91,ä¼¯91,å¹½91,é¡¾91,ç‡•91,å¤œ90,ç¾Ž90,ç‰¹90,å®«89,å»º88,é—¨88,å¥³87,æ´ª86,äºŒ86,ç§€86,é“¶85,å·´83,æ¢…83,å®‡83,ä½™83,å¥¥82,èŽ²81,é’Ÿ81,å†·80,æ°¸80,å«80,æ˜¥80,çº³80,å­Ÿ80,è™Ž79,è¿ž78,ç‚Ž78,è›‡77,ç‚¼77,è¡Œ77,æ˜“77,æµ77,å½±77,å¸ƒ77,æµ©76,æ—¥76,è½76,è¾¾76,ç¾½76,é‚ª75,å¤«75,äºŽ75,é­75,å®—74,å·¨74,ç´ 74,å73,æ ¼73,æ¢72,å†¥71,å‡70,æ¯’70,å•70,å§œ70,æ€69,æ²™69,è™š69,ä¹¦69,å‰69,ä¹Œ69,ç²¾69,æž68,å¹³68,é’±67,å…­67,ç±³67,å°Š66,ç»66,è¿œ66,å®¹66,å­¤65,åŒ65,éª¨65,å¹»65,è¢65,ä¿®64,è‹±64,å®64,è²64,ä¸64,ç»´64,å‘64,æ­»63,å¾¡63,é•‡63,å§¬63,è´º61,è´¾60,ç­60,æ™¶60,ä¼Š60,ç‹¼59,æ›¹59,èŽ‰59,å…½59,ç‘ž59,å·¦59,é€š58,è¯58,è¿ª58,ç„°58,çƒŸ57,äºš57,å§‘57,æ³¢57,å²³57,æƒŠ56,åŠ›56,æ²³56,æœ‰55,å°¼55,è–›55,é‡54,ä½›54,å©‰54,ä»»54,è´53,åˆ©52,è£‚52,å¤š52,ç¦52,èŒƒ52,è½»51,é²51,è‘›51,é™51,éœ‡51,ä¸¥51,ç¦»50,æ„50,ç‹‚50,éœ50,ç«¹50,ä¾¯50,çˆ±50,å†¯50,å‚²49,èŽ±49,æ·‘49,ä¹49,å®š48,é¹°48,æ¸©48,å¸Œ48,é€¸47,è¾°47,ç©†47,å­”47,ç‰›47,è”¡47,ç§˜46,æš—46,å•†45,æ–°45,ä½³45,èˆž45,å½©45,ç¿ 45,ç‹¬44,å¢¨44,åš44,å®˜44,è—44,æŒ¯44,å¦™43,å½’43,å“43,æ–—43,å†›43,ç¥–43,è°·43,ç†Š43,æœ›43,å›ž43,å¯42,æ‰¿42,çºª42,æ‘©42,å›¾42,é»Ž42,æ–­42,å°42,å¼€42,å‚…42,åœŸ42,ä¾41,æ…§41,ç‹41,ç¿¼41,æ™¯41,å¡”41,éœ¸40,åº”40,æ£®40,æ–©40,è…¾40,åŠ 40,ä»²40,é¸¿40,å± 39,ç‹®39,å‰39,ä¹¾39,è¯º39,å¥‡39,ä¸39,å¸¸39,åŽ‰39,éƒ½39,å‡¯39,é¸£39,é—®38,ç« 38,è¯—38,å’Œ38,è‡³38,ç¬¦38,è’38,æ¯”38,ç«‹38,æ¬£37,æ··37,ç„š37,ç”µ37,ç§‘37,æ³½37,è€€37,æ±‰37,å…³37,çŸ¥37,åº†37,ä»¤36,æ´ž36,åˆ36,æµ®36,å”36,é¹¤36,å“¥36,åº„36,è‘£36,è·¯35,æ¾35,é›¾35,æ³°35,ç”²35,è§’35,é¢œ35,å¤´34,å˜‰34,çŽ²34,éŸ³34,å²34,å“ˆ34,æº34,èµ«34,ç¬‘34,åŽŸ34,æ®·34,å´”34,æ±ª34,é‚“34,å¨33,ç«¥33,èš33,å¾—33,å™¬33,ç…ž33,ä¿Š33,å ‚33,å­—33,å…´33,å²©33,å»–33,æ›¼32,ä¼¦32,æš´32,å°š32,æ™®32,æ—‹32,çº¹32,æ­¥32,æ€€32,å¯32,æ®µ32,è¾›32,è½®31,è‚31,ç»31,é±¼31,è‹—31,åž30,æœº30,å·«30,ç»¿30,ç´30,è½©30,èŠ·30,éœž30,éœ²30,ä¹”30,é”¦30,åŠ29,å°˜29,å°¸29,èƒœ29,å¢ƒ29,åˆ29,åŽ29,èŠ™29,å¸•29,æ°29,å…„29,å€©29,æ¥29,è£´29,å§š29,è´¹29,è³ˆ29,å®ˆ28,ç¥28,æ®‹28,é˜µ28,å‡°28,é£˜28,æ¸¸28,è”28,å£«28,ç®¡28,åŸŽ28,ç´¢28,ç”³28,è¨28,è‰³28,æ¯›28,æ²28,ç³27,ç½¡27,å¦®27,æ ‘27,æ¡ƒ27,æ•£27,æ¸Š27,åŠŸ27,è›Ÿ27,è‰27,è™¹27,éš27,éœ„27,çˆ†27,é¡¹27,æœ27,éœœ27,æ¡‘27,å¿ 27,å±•27,é™¶27,å¿µ26,å…¨26,ä¹±26,å«£26,é¹26,è´¤26,æˆ´26,æ›²26,æ‹“26,å°¤25,å·§25,è¯­25,æŠ¤25,æ²‰25,é€†25,æ™º25,ç¢Ž25,å•¸25,å©·25,å™¨25,äº¦25,é›25,ä¼Ÿ24,è‰¾24,è¿½24,æ¹˜24,é›†24,æŠ˜24,é”24,é˜Ž24,éš†24,å‘½24,æ‹³24,æ’24,æ©24,é»›24,æ˜Š24,ç‰™24,ç24,è‡ª24,å°¾24,é³ž24,é¦¨24,è’™24,è£24,ä¼24,éŸ¦24,æ•™23,ç›˜23,æŽŒ23,è›®23,è¯¸23,é¼Ž23,åˆ†23,å¾®23,åˆš23,ç•Œ23,èº«23,æœ¬23,ç¬¬23,ç«¯23,æ˜Œ23,ä¿ž23,éº¦23,æŸ¯23,æ½˜23,è¡£22,ç‘¶22,ç”«22,èµ›22,å†²22,ä¸»22,åŠ«22,å…µ22,é­„22,è¨€22,è´µ22,ä»22,è±¡22,çŽ›22,æ¡‚22,å¦22,æ•¬22,ä¹‰22,å´‡22,æ™¨22,é¹¿22,æ–½22,é˜®22,å¦¹21,é–21,æžª21,ç¦21,é”‹21,é“œ21,è§£21,æ»¡21,å‡¡21,æ‰‹21,èŠ³21,ä½“21,å¹¿21,åŒ…21,è’‚21,æ²§21,éž21,è—¤21,æ˜­21,å®21,æ¯•21,æƒœ20,å20,æƒ…20,åŒ20,éƒ¨20,ç‰20,å¼º20,å¼¥20,çˆ·20,åœ†20,è§‚20,é—ª20,å¡ž20,æ³‰20,å½¢20,è•¾20,å¯Œ20,çœ¼20,èˆ’20,åº·20,è–‡20,å–œ20,é—»20,å¼µ20,å½­20,ä½©19,å€¾19,è°­19,æ± 19,æ€¡19,å¤19,åˆ«19,å¯†19,è¶…19,é€19,é™µ19,é›„19,åœ¨19,é…’19,çš“19,åˆ—19,é™€19,ç»§19,å†¬19,æŸ19,åºž19,ç‹±18,è¿·18,å¯»18,å°18,åŸŸ18,ç©¿18,é€ 18,æ€’18,ä¸º18,æŸ”18,èŸ’18,èŽ18,äº²18,ç“¦18,æ™´18,æ˜ 18,åº­18,ç¤¼18,ä¸´18,ç¾Š18,é‚µ18,é‡‡18,å½¦18,éºŸ18,é†‰18,æž«18,è’‹18,é‚¹18,æ¥¼17,å¤º17,æ‚ 17,æ•17,è¿˜17,ç¦…17,éª‘17,çŒŽ17,ç¼17,å­£17,æ¶17,æƒ 17,æ—­17,ç›ˆ17,å’17,åªš17,çŒ¿17,ç‰§17,å»·17,ç”˜17,æŸ¥17,ä¸˜17,è¶Š17,å«17,é›€17,å–„17,å…»17,å¥‰17,è¶17,æ‰¬17,è·‹17,éª†17,é‡Š16,é¡»16,é£Ÿ16,è¿16,å²š16,è€¶16,å‡€16,å®›16,é¢†16,è©16,å„¿16,éš16,éº’16,æ‰˜16,æ ¹16,å©†16,å¼—16,å…¶16,æ¶¯16,å…†16,å‡16,åŽ16,å¸­16,é¾Ÿ16,æ›¾16,æ¯15,è‰¯15,é“­15,æ®¿15,å¨˜15,åŸº15,ç•™15,æ¸¡15,çŽ¯15,ç››15,ç 15,ä¹˜15,å¼˜15,è™ž15,æ½œ15,åº“15,å¯¿15,äº¬15,è¡15,è‰²15,ç›¸15,èŒ‚15,å­˜15,å©´15,åŠ‰15,æ15,è†15,è¾•15,çº¯14,å›š14,å‚€14,æ€œ14,è‘«14,æ¯14,ä¸‹14,é‡Ž14,åŠ¨14,æžœ14,å¥”14,å¨œ14,èˆ14,é—´14,è„±14,å´©14,æ½‡14,çˆª14,å±…14,è¿›14,çš®14,é14,æŸ´14,ç»ƒ14,æ¨ª14,æµª14,æˆˆ14,ä»‡14,éº»14,å®£14,ç‘Ÿ14,åŸƒ14,éŸµ14,æ·³14,ç­14,ç‹„14,å‹14,å°¹14,æ»•14,æˆš13,çª13,åŸ13,ä¸°13,è½¬13,ç»Ÿ13,åº¦13,ç©¹13,æ€»13,å¿˜13,æ‰13,å³°13,ç–¾13,ç¿»13,ä¿¡13,æ‹œ13,äº¡13,çŠ€13,å°13,èŠŠ13,æ¬¢13,å§‹13,å¦ƒ13,é¡º13,å¼•13,æ¹–13,ç¿”13,èŠ¸13,å† 13,è·ƒ13,åˆ‘13,æ™‹13,æ¶›13,è§13,ç¥13,èŽ¹13,åŸ¹13,æ±¤13,å“12,å­12,æµ…12,è¯›12,ç’‡12,ç›–12,ç‰©12,å¼Ÿ12,èŠ’12,é™¨12,çŒ›12,å‡º12,æ´12,åŽš12,éš‹12,æŠ±12,å›º12,ç„¦12,çº¿12,åˆƒ12,é¢12,å€ª12,å®µ12,å·12,å•12,æ‰Ž12,é«“12,å¨‡12,è‹¦12,å¹•12,æ¶…12,ç®€12,æœ´12,çŠ12,æ¥Š12,ç”„12,é™³12,å¥•11,æƒŸ11,ç”œ11,å—œ11,é•–11,å¼‚11,ç¥­11,çŒ®11,ç›Ÿ11,è™«11,çŽ«11,æ—¶11,è‘¬11,æ¼«11,é•œ11,ç…§11,æ™š11,é²¨11,å¤–11,æ½®11,ç¥¥11,è¿Ÿ11,åˆº11,ç†11,ä»Ž11,å¥ˆ11,ä»˜11,é¢–11,æºª11,ä¼11,è¿¦11,æ¡11,æ –11,èž11,å¯‚11,ç°11,æ”¾11,é‡11,èµ–11,è½¯10,é¸Ÿ10,å†‰10,æš®10,å‡¶10,è››10,å®¢10,æ“Ž10,æ·±10,ç»“10,æœª10,ä¿10,æ²Œ10,æ›œ10,éº—10,çœ‰10,å¤­10,å¹´10,è¾¹10,ç†™10,å¸®10,éª·10,é™10,ä¾ 10,æœµ10,çŒª10,é»˜10,ç‘10,æ°‘10,ç§‰10,è“‰10,æ…ˆ10,è½¦10,å§†10,ä¼½10,å¹¼10,å®œ10,å¸10,åˆ‡10,è‡´10,å¿10,æ¨10,æ·®10,å»¶10,æ‚Ÿ10,å¥Ž10,çŒ´10,æž¯10,æ¾¹10,ç’ƒ10,ç¾¤10,è‚–10,é‚±10,é¾š10,å¤9,åŠ²9,ç­±9,æŒ‡9,ç„¡9,éª„9,çºµ9,é”9,å·ž9,é—9,è´¯9,å¯¼9,æ‹›9,å…¥9,æ±‚9,å†…9,æŽ§9,å“²9,åœ9,é›²9,ç§ƒ9,èœœ9,è§‰9,è¸9,å³9,è´9,ç–¯9,å‹’9,ç›¾9,æ´»9,åˆ¤9,èƒŽ9,å¤„9,å‰¯9,ä»£9,åˆ¹9,è‚²9,è„‰9,ç»9,é‚£9,é“¸9,é›³9,å²‘9,æ²9,å¦9,æ‰¶9,æ‹”9,ç‚«9,è¡¥9,è¤š9,è©¹9,é»ƒ9,éœ“8,ä½8,èœˆ8,å¥—8,å®¿8,èœ˜8,è¿‡8,æˆ‘8,ä¾8,å°„8,ç™»8,ä¼¤8,å‰²8,ç§»8,åŠˆ8,æ‚¦8,ç”»8,æ‚²8,é”»8,æ”¿8,èƒ½8,ä¸š8,ä¸¤8,é­…8,å·8,æ‰§8,å¼¦8,ä»ª8,å‰8,ç‹—8,å 8,æ¾œ8,éƒ8,åŠ³8,æ‚¬8,èŠ8,å¿…8,ç›Š8,èƒŒ8,é€Ÿ8,ç›®8,æµ‘8,æž­8,æ’’8,æ˜†8,å¯Ÿ8,å°‰8,å¿§8,æ‘„8,æ’¼8,æ•–8,æ±8,æ8,æ¨Š8,æ³¥8,æ·¬8,è’²8,é‚¢8,é¸¡8,éœ¹8,ä½‘7,åŒº7,ç‰¢7,é€7,èœƒ7,ç†”7,å€š7,èŒ¹7,èŽ½7,é­7,å¦7,å’’7,å¤•7,æƒ7,éž­7,æ²ƒ7,è£˜7,é˜7,çˆ¾7,å°–7,å ª7,ç¼ 7,å‹‡7,é¸ 7,è7,é”¡7,æ¬²7,å‘¼7,è¯š7,æ¢“7,è¶³7,ç»£7,ç¼˜7,å¤±7,å¤®7,å¥7,ç‚³7,èŒµ7,äº­7,å´–7,ç…Œ7,ä»¥7,ä¼—7,å†œ7,ç¿7,åˆ™7,é‡7,è‰7,è7,ç…7,å¯°7,è°¦7,ç„•7,çº¤7,é“ƒ7,å›°7,å®¾7,ç¦¹7,è‚ 7,ç‚½7,ç¦„7,å¥š7,å¯‡7,å½¼7,æœ¯7,å¼7,å¾‹7,ç¼š7,æ¢§7,æ´—7,æ»´7,èœ‚7,ç¿°7,ç”¦7,çž¬7,è¯7,éƒ7,é¡¶7,é©­7,é¦–6,ç‚¹6,å“­6,èŒ¶6,ä¼š6,å¢“6,åŒ»6,è€ƒ6,å„’6,å·¥6,è…°6,å”¯6,å§¥6,èŸ¾6,çº¦6,æ±6,ç‡Ž6,æ¢6,æŽ¨6,éƒŽ6,è¬6,å‡†6,è‚‰6,è¿”6,å 6,å¬6,éš¾6,è¾‰6,æŠ€6,éƒ¡6,å¹6,å£6,å¹¸6,å˜6,çª6,äº‹6,é¸¾6,å²­6,ä¹™6,å©§6,èŒ‰6,ä½6,è±¹6,é’°6,é­¯6,å²6,å‘³6,ç¿¡6,è±6,é½¿6,åŒ¡6,å®®6,å§6,åŽ„6,åŽ†6,ç§¯6,èƒ–6,ç“¶6,æ±6,å…·6,é¼ 6,æ­¢6,æ–§6,æ¢¨6,é²¸6,å¼„6,é†’6,ç„¶6,æ†6,æ‘˜6,ç š6,ç»­6,ç¿Ÿ6,çˆ6,æš–6,æœ‹6,é€¢6,æµ£6,æ¸º6,æ¶‚6,çƒ›6,çš„6,ç¥ˆ6,ç»œ6,ç»¯6,è€¿6,ç¿Ž6,é‰´6,é©±6,é¢¨5,å¼¹5,å¯¸5,çˆ¶5,ç„±5,æ¼”5,æ€ª5,å€Ÿ5,å†5,ç›¼5,è“¬5,æ¹®5,è¯€5,ç®—5,è½°5,ç¶­5,å†»5,ç£·5,æ³£5,åŠª5,ç»µ5,è¦5,æˆ·5,ç›´5,å£5,å¬5,æˆ®5,æ²»5,å®¡5,è±†5,å¯º5,ç”±5,å5,å·¢5,å¥‘5,å§—5,æ“’5,å£°5,å³¡5,ç›—5,è´¢5,å‡‰5,å…¹5,ä¸›5,æ‰€5,æ­Œ5,åºœ5,æˆ’5,é²²5,æµŽ5,å’†5,ç¾…5,æ——5,ç£5,çƒ­5,ç‡ƒ5,å5,çŸ®5,åŠ5,é€5,è 5,æž5,ä»ž5,æ—5,ç®­5,è£•5,æ²‚5,å¼‘5,ç¦½5,ä»€5,æ¡¥5,è®¡5,ä¼ 5,çº§5,ä½˜5,ä¿5,åš5,åª›5,å†¶5,ä¸«5,ç›5,èš•5,ç–¤5,å¿†5,ç„‰5,å¤·5,è´ž5,æ¯…5,ç¿…5,å5,é©¼5,å«5,æ¦­5,æ5,å²¸5,åš5,è‰º5,æ¥ž5,æ±—5,æŸ±5,èš€5,æ›¦5,è±ª5,å®Œ5,è•´5,é¾5,æ ‹5,è±5,æ¶¦5,å¿«5,è¦†5,å¾5,ç­‹5,ç ‚5,é—µ5,æµ¦5,èŒ5,èžº5,èŽŠ5,æ§5,æª€5,æ¿®5,é¸¯5,çž¿5,è”º5,ç£5,ç»†5,ä¹…5,ç®«5,ç¼©5,é®5,èŸ 5,è°ˆ5,éœ†5,è¿Ž5,é¿5,é¹ž5,å¡˜4,æˆª4,æ—º4,å²›4,é’§4,å¾½4,æˆ4,åŠ4,å½“4,æ˜™4,é’µ4,å§¨4,é³„4,è™4,å”¤4,å¢™4,ç–†4,æ•4,å·4,æ‹4,å®™4,èŽŽ4,é’“4,çº4,å¿’4,å¸4,æ”¯4,å§Š4,è¿«4,èŒœ4,ç–4,æ‹4,æ£4,é²4,æ²¼4,ç»«4,æ˜¾4,å¼ƒ4,çŒ4,åƒµ4,æŠ«4,å‡4,æ¶²4,èž³4,ç»„4,çž³4,æŽ¢4,ä¿„4,å‡›4,ç¼4,å·4,ä¸¾4,è®®4,æ´¥4,ä¸™4,æºŸ4,å‹ƒ4,é¸¦4,è£³4,é—²4,é˜”4,äº•4,æ–4,ä¼‘4,å‚¬4,æœ—4,å³¥4,ç½š4,å‹‹4,æ–Œ4,æŸ„4,é€‰4,è®º4,æ–4,é’ˆ4,æ³¡4,é™Œ4,è‹‘4,æ¦®4,æ´‹4,è–„4,éº“4,å‘‚4,å®ª4,æ›‰4,å¤¢4,å› 4,å¨„4,å 4,å£®4,å£¶4,äº®4,èª4,éˆ4,é³Œ4,è¯ƒ4,æ·4,å¥½4,æ²›4,é²¤4,è°›4,å°†4,é›¯4,å±4,å²4,è€Œ4,å·¡4,çµ²4,æ²«4,å»‰4,èœ€4,å¯¶4,å¾€4,èµ¢4,éº¥4,æ‰“4,æŽ’4,æŽ¥4,ç‚4,é¼“4,çŠ¶4,æ¼ª4,çž4,æ³ª4,åƒ4,å¼§4,æ½­4,éœ4,æ£‹4,æ©™4,æ°²4,é¹«4,è˜­4,è„š4,ç™¸4,é¹­4,è¯4,ç¨»4,ç²˜4,ç²±4,ç¿4,ç‘·4,è€4,è•­4,é¥®4,é„‚4,é™°4,é™¸4,é³4,é½Š4");
var ilchar=new Dictionary("ichar",1,"å±±796,çŽ‹692,å­669,å¤©661,å„¿636,åŸŽ588,äºº478,å‰‘478,å®—452,ä¸¹436,è¯€423,äº‘420,é¾™411,é—¨409,æ–¯403,å›½371,å³°335,é˜µ330,é£Ž322,æµ·313,æœˆ305,æœ¯287,æ˜Ž275,æ—271,æ³•270,å¢ƒ267,å›260,æ®¿253,å®«250,é“247,åŽ246,å¸ˆ243,é›ª242,å¾·223,çŸ³217,ç¥ž215,é˜214,ç”Ÿ211,ç•Œ209,é˜³206,å…°204,å°”202,ç»200,ç 200,å®¶199,ç«196,ä¸»195,çŽ‰195,å“¥189,æ˜Ÿ188,æž—186,è™Ž184,åˆ€184,åŠŸ183,ç‰¹179,å…„178,åŸŸ177,å…½176,è°·173,æ²³170,çµ169,ä»™166,å°165,é›¨164,é£ž164,å¸163,æ¥¼161,å²›159,èŠ±158,çš‡158,æ–‡156,é›·153,è€…153,æ‹³152,é’152,æ°´150,æ‰‹148,èŽ²146,å¨˜146,è‰145,ä¸œ143,å¨œ141,å·ž141,åºœ138,é›…136,ç½—136,å…ƒ134,æ°133,å ‚133,é™¢133,å°Š130,å›¾129,é™†127,å¸®126,æœŸ126,å¹³126,å†³125,ç¥–124,ç„¶124,æˆ123,å…‹123,æ¸…122,åŠ›122,å¡”121,å¿ƒ119,å†›119,ç¾½118,è½©115,å…‰113,æŽŒ112,çˆ·111,ç¬¦110,æ•™110,é­”109,å”109,å‡¤108,å¼Ÿ108,æ–©107,é›„107,è‹±106,ä¼š106,å¥³106,æ±Ÿ103,å¯’103,äºš103,å‡¡103,ç³101,æ‹‰101,æœ¨101,ç‚Ž101,å—100,æ°99,ä¸½99,å½±98,æ¶›98,åœ°97,è›‡96,ç‹¼96,æ°”95,å©·95,å®‡95,å·94,å£«93,æ´¾93,ç‘¶92,è¿œ92,å®91,æ­¥90,é­‚89,ä¹‰89,è„‰88,é¹87,åœ£86,ç©º86,é¦™86,è¾°86,è¾‰86,æ¾85,çº¢85,ä¾¯85,æžœ84,çŽ²84,å¼º84,æ™¶83,ç›Ÿ83,è¾¾83,æ­¦83,æŸ82,è¡Œ81,æ£®81,å¦¹81,è²81,åˆš80,å¥‡80,ä¹¦80,å†°80,èŠ³80,å¤«79,è£78,å…¬78,çœŸ77,æ ‘77,åŠ«77,ä½“77,åº„77,å®‰77,é€š76,æµ©76,é‡‘76,å°˜75,èŠ¸73,ç¿¼73,ç„°73,æ³¢73,é”‹73,ç‡•73,è–‡72,ä¸72,è“‰72,æž«72,ä»¤71,ç”²71,æº71,æŸ”71,çƒŸ71,é•‡71,é¸Ÿ70,é¹°70,æ´ž70,ä¼¯70,æ‰¬69,è±ª69,é¼Ž68,å§¬68,å®68,æ¢…68,ç§‹67,å‹67,å²©67,ä¼Ÿ66,çª66,çœ¼66,ç«¹65,å¿—65,æ¸Š65,è¶65,è€65,è¥¿65,è¨€64,çŽ„64,è¡£63,å›¢63,è¾ˆ63,å€©63,çƒˆ63,èˆž62,éœœ62,åˆ©62,é¸£62,å‡Œ61,æ©61,çŽ¯61,å¦61,å¨Ÿ61,ç§€60,å¶59,éŸ³59,æ™´59,æŒ‡59,é“59,æ³½59,ä¾ 59,å«59,å¿59,å²š59,å¯º58,ç´58,ç¿”58,æ˜¥58,é•œ57,éœž57,æ˜Œ57,çŒ¿56,ä¹‹55,æ•55,å…¸55,é¹¤55,æ€55,ä¹55,æµ54,èº«54,ä»54,é™µ54,å¼53,ä»ª53,å›­53,é¦¨53,ç‘ž53,ç™½52,æ—¥52,åŠ²52,ç‹±52,æ¢¦52,å…µ52,æ´›52,ç‰›52,æ…§52,æ¬£52,ç¥¥52,ä½›51,é›¯51,åŽŸ51,å°‘51,å¨51,æ€¡51,è±¹50,æ´‹50,è™¹50,å¦®50,è¯º50,æ€50,è“50,æ¶µ50,æ™¨50,ä¿Š49,èŽ¹49,ä¸€49,èŠ49,çº§49,æ‰49,æ­£49,å²­48,å´–48,å¦ƒ48,æ´²48,ä¸‰48,æ›¼48,èŽ‰48,é€¸48,è‰¯48,éƒ¡48,èŒ¹47,æ³‰47,æžª47,ç¾Ž47,å…´47,æ¯47,ç†Š47,å¿ 47,åº†47,è±47,å‹‡46,æž46,æ——46,é©¬46,æ¹–46,é±¼46,å¤´46,éƒŽ46,å¦‚46,åš46,äº®46,è™š45,åˆƒ45,è¿ª45,é™45,è®°44,æ± 44,å«£44,æ°‘44,æ¯…44,ç—•43,éŸµ43,æ²™43,èƒœ43,é¡¿43,è42,ç¦»42,æ„42,å‡°42,å¼“42,ç½¡42,éƒ½42,é‚ª42,æ³°42,é¸¿42,è¶…42,æ–Œ42,ç42,å¤š41,çˆª41,éœ²41,å¨‡41,æ´ª41,æ˜Š41,ä¿¡41,è´µ41,å¦–40,å˜40,å¤40,é‡Œ40,å°¼40,æ˜“40,é‡39,å¤œ39,æŸ±39,æƒ…39,å¨…39,ä¸š39,éœ„39,ç’‡39,å¹´38,å…³38,å™¨38,è›Ÿ38,åªš38,é¢–38,ç¦38,æ´38,åŒ38,å²³38,è´¤38,è‹¥38,èŸ’37,çƒ37,é²37,åŒ—37,æ–¹37,ä¾37,æ‘37,æ¥ 37,èŠ¬37,ç›¾36,è¡€36,æˆ˜36,å¸36,åŸº36,ä¸°36,è’™36,çŠ36,ä¼¦36,ç†™35,å¤§35,ä¸‹35,æ•£35,è½®35,æ€ª35,å°35,è’35,å…¨35,ä¸ƒ35,ç›ˆ35,é¢œ35,é“­35,å•¸34,è·¯34,è™«34,ç‹34,å’Œ34,æ™º34,éš†34,ç´ 34,ç”°34,ä½³34,è¿›33,é’Ÿ33,ä¸¸33,æµª33,åº­33,æ’33,äºŒ33,å“²33,åº·33,ç…ž32,åˆº32,éºŸ32,éœ¸32,è¯—32,é›32,é‡Ž32,æ ¹31,è¯­31,ç›˜31,å¸…31,åŽ31,è››31,å¡31,ç«‹31,è½31,ç»´31,å‰30,æºª30,å½•30,éª¨30,ç²¾30,æ¦œ30,ä¸­30,ä¹30,ç®­30,çž³30,è¨30,è—¤30,åŒ–30,å®¹30,æƒ 30,ç¼30,å¹½30,äº­30,å®30,è‰³30,ç¬‘29,ä¿®29,æ¥29,éž­29,é’ˆ29,ç”·29,ç´¢29,åœŸ29,å­¦29,é›€29,å ¡29,æ±‰29,æ¾œ29,äº¬29,å‡»28,æ¥š28,é•¿28,é½28,ç››28,å¥´28,ç‘œ28,è¯š28,å¤27,æ¶¯27,é¢†27,ç©¹27,è±¡27,èŽŽ27,å‹’27,å§†27,æ—­27,å§¨27,æ™“27,çœ‰27,å‡¯27,æ›¦27,å¢¨26,é¬¼26,åŒº26,é˜Ÿ26,æ ¼26,é­…26,è´¢26,å±…26,å»·26,å®¢26,ç§‘26,ç£Š26,æ–§25,èˆŸ25,å¹¡25,å››25,æ–‹25,å¸Œ25,å½¦25,è‹25,é“ƒ25,å½ª25,å½¤25,å¯Œ25,å©‰24,å’’24,æ—‹24,æŠ€24,çŒ«24,å“24,ç»24,å…­24,ç‰™24,æ¡¥24,ä¸24,æ¡24,ç¤¼24,å¤ª24,å¥¥24,å¸†24,æ¡‘24,å¤24,å†¥24,çŒ›24,å¨¥24,å˜‰24,éž24,ç ´23,å‘23,æ£23,é›•23,è§‚23,è§’23,ä¸–23,å23,è¶Š23,å°š23,ç«¥23,é—´23,å°23,å‚²23,å‡23,å½¬23,è€€23,ç­22,åˆ™22,ç½©22,å†²22,æ¶²22,æˆ’22,åš22,ç‘22,é™€22,å¯22,å£22,è•¾22,å¸¸22,äº”22,é’°22,çš“22,å¥Ž22,å¨´22,æ˜†21,ç« 21,ç‚‰21,å°º21,å·21,ç¿°21,æœº21,åƒ21,é»Ž21,éœ–21,å»º21,ç’21,å‡21,æœ—21,æ¨±21,é¡º21,èŒ21,ç‰Œ20,é‰´20,é”20,é”¤20,ç„±20,ç‹®20,åŽ‰20,ç¾¤20,é˜´20,å§‘20,å„’20,é‚¦20,å®š20,éƒ¨20,èŒµ20,æ­Œ20,é¼ 20,é’§20,é»˜20,èŠ™20,è´ž20,åª›20,æ–°20,æ•¬20,æ€»20,è‡£19,çŒª19,çŒ´19,èŠ’19,å±€19,è¥19,å·«19,çº³19,æ‰˜19,ç¾Š19,æ™®19,å¯19,è°¦19,å¯¿19,ç‚19,æ¬¢19,ç¦19,èŒœ19,å¥19,å…’18,å·18,åº§18,å‹‹18,ç¯18,ä¼ 18,ç™»18,æ¼ 18,çº¹18,ç³»18,ç’ƒ18,é¾Ÿ18,å©†18,ç‹—18,å©´18,éœ‡18,æ™¯18,å¾®18,ç…Œ18,è…¾18,æŸ³18,ç¦¹18,ä½‘18,ä¹¾18,ç¿ 18,åŠ 18,æ¨18,æ‰¿18,è±18,é–18,æƒœ17,ç´«17,æ‰‡17,é…’17,é­„17,ç¿Ž17,åŸ17,å°¸17,å€™17,äº‹17,é˜¶17,å…¹17,å†¬17,å®œ17,æŸ17,å®£17,å²—17,å·´17,å©µ17,å‘¨17,é«˜17,å´‡17,æŸ¯17,æ˜­17,å‰§17,é¦†16,ç­–16,åŠ¨16,æ¡ƒ16,ä¼ž16,æ½­16,çˆ¾16,è¡16,å¦ˆ16,æ®‡16,èˆª16,èŽ«16,å¿§16,å“16,é‘«16,åŒ16,èˆ’16,èŠ¦15,å¼¹15,æˆŸ15,çœ15,åœº15,æ¢15,å¸ƒ15,æ¸¸15,åº¦15,æ15,å®˜15,é›¶15,è‰º15,èŽ15,è‹‘15,å‰15,å–œ15,ç­15,èŠŠ15,æˆˆ15,æ¬§15,ç§¦15,æ”¿15,æ¹˜15,æƒ15,å¼˜15,æ‚¦15,é’±14,å¦™14,é¸¾14,æ•Œ14,å„¡14,é’»14,è°±14,é³„14,ç›®14,é’¢14,æ£’14,é“¾14,çŸ›14,æ¯’14,è 14,çŽ›14,ç¯‡14,é¢14,æ¯14,ç½‘14,è¿ž14,æ±—14,ç»«14,å”14,çƒ¨14,å¿Œ14,ä¿14,å¾’14,ç¿14,é“¶14,å¯¨14,ä¾„14,å°14,è´º14,è14,çŽ«14,å®¾14,æ„14,é­14,é¾„14,è›®14,ä½©13,è—13,æš´13,åƒ13,æ¢­13,è´13,æ›²13,æœ¬13,èƒŽ13,å®¤13,æ–13,çªŸ13,é«“13,æ‚”13,èŽ±13,å¾—13,é“œ13,ä¼¤13,ä¼Š13,æ€œ13,ç¼º13,åŒ»13,å§—13,èŠ13,è’‚13,å±13,æ—º13,è•™13,å»‰13,æ˜‚13,æœ›13,ç›´13,ç©†13,æ‘©13,æ‚ 13,æ°¸13,è¾›13,ç‚¼12,è£³12,ä¸´12,ç”µ12,è·ƒ12,åº™12,ä¹¡12,é”12,ç¬”12,äº†12,é©¹12,ä½12,æ£ 12,ç§12,èµ·12,è€¶12,å¨ƒ12,æ¯”12,è‰12,å± 12,é»„12,å¹»12,æ½®12,å°‰12,åŠ12,ç±³12,ç‹‚12,é—ª12,èª12,é—²12,æ ‹12,æ¡‚12,ç”œ12,ç¦„12,æ™‹12,å¸‚11,è§£11,èœ¥11,å§¿11,ç€š11,ç‘°11,èƒ½11,çºª11,å‘½11,èŸ¾11,åˆ¹11,å¤•11,ä¸Š11,éœ†11,ç†11,è¿11,çˆ¶11,ç…§11,ç»Ÿ11,æ½‡11,è•Š11,ç¿11,ä¸º11,éš11,å«‚11,æœ”11,å¥•11,å¾11,ç„•11,è¿¦11,å–„11,æ–11,éœ“11,ç‘¾11,è·11,è‹11,å´11,æ´¥11,èŽº11,å·§11,ç®¡11,æŒ¯11,çª11,é€11,æ˜±10,çº¯10,å¿µ10,èˆ¹10,çˆ†10,ç“¶10,çº±10,çŠ€10,ä¹Œ10,å† 10,è²‚10,å´©10,å³¡10,è¡«10,è¯10,è‘›10,é‡10,æ¨ª10,ç‹¸10,å›ž10,åˆ10,å§¥10,çœ¸10,èµ¤10,ç›–10,æ–—10,æŠ¤10,èŒ¶10,å› 10,è£‚10,è„š10,è¢–10,æ€€10,æ”¾10,å£°10,é¹¿10,å­™10,åœ†10,å°§10,çº¤10,å…¶10,æ‹“10,ç¨‹10,ä»”10,èƒ¤10,æ™–10,å…ˆ10,æ¿10,é­10,èŒ‚10,ä¸¥10,èœ‚10,ä½10,æ·³10,èž10,æ…ˆ10,ç¢§10,å©¶10,é€Š10,ä»²10,å‰10,æ²10,å‡10,è§10,ç‘›10,çˆ½10,èŠ¯9,è‡‚9,çŠ¬9,å²9,ç¢‘9,çš„9,çº¿9,åƒ§9,ç©´9,é•¯9,è£…9,è½¦9,å™¬9,é²¸9,æ ¸9,å²9,æ±€9,è›‹9,é³ž9,é©°9,é›²9,ä¹”9,è´¼9,çº¦9,å£9,é—®9,ç£9,å¼¦9,ä¸˜9,åŠ©9,ç¼˜9,æ¸¯9,çµ²9,å…š9,å†œ9,æœ‰9,é’¦9,ç»9,è˜­9,èµ9,ä¹™9,æ ‡9,å½’9,çŽŸ9,æ™”9,å­8,èµ‹8,ç®€8,èš£8,æ¶Ž8,åœˆ8,å‚8,å¼€8,å·¥8,é“ 8,å¤8,æ·‘8,é²¨8,èµ›8,ç›—8,é›†8,é‚£8,æ»¡8,å¦8,é¡¶8,çŽ‘8,é¥8,å¹•8,ç»„8,æ€’8,åº—8,å®™8,å¦8,å¢Ÿ8,å‰ª8,èš8,ç“¦8,ç ‚8,æ£‹8,æ­8,ç’‹8,å¡ž8,å¢“8,éŸ©8,ç–†8,æœ«8,å8,æ–‘8,ä»‡8,å‡‰8,å¥‰8,è8,é”¦8,ç›8,åº¸8,å¾8,é“Ž8,ä½™8,è¡¡8,ä¸‡8,æ¡“8,çº¬8,åºµ8,æµŽ8,åˆ—8,ç­ 8,é¸¦8,ä¼½8,æ²8,è‘£8,å§£8,ç”«8,å·8,èŠ·8,å¹¿8,å¾½8,ç‰§8,å©•8,ç‹„8,æ˜¾8,ç…œ7,ç‚®7,é7,åŠ¿7,ç¬›7,è½¬7,ç‰©7,è¸ª7,æ–­7,å°¾7,å›7,è‚ƒ7,åµ©7,åŸ7,ç’§7,ç¦½7,é¼“7,é’©7,å¨‘7,å£®7,å¤­7,æ®Š7,é£›7,ç­7,ç¬¼7,èŒƒ7,åº“7,å¯»7,å¥”7,å®ž7,çˆµ7,çš®7,é«…7,è‘µ7,å·¢7,æ¨7,çµ®7,è¯†7,æž­7,åŽš7,åˆ‘7,å®µ7,è¾…7,æ7,æ¸©7,å£¶7,è°¨7,å¡7,åŸ¹7,æ¶§7,å¸­7,ä»“7,ç°7,ä¼¶7,æˆ·7,æµ¦7,æ»¨7,æš„7,ç”³7,å”¯7,ä¸‘7,æ™ƒ7,åº”7,ç¦¾7,å²7,æ¡¦7,è™7,å©§7,æ­7,ç¿7,æ˜•7,ç‚«7,é™Œ7,é“®7,å®‹7,æš®7,é¾6,æ²›6,æ³ª6,æ¯›6,ç¥­6,åž6,æ±¤6,ä¹³6,è¡°6,éª‘6,è…¿6,å•†6,æ¶6,åˆ»6,è®º6,æž6,æ²ƒ6,å½¢6,é†‰6,è´¥6,ç‰¢6,åˆ6,æ ˆ6,å“ˆ6,å¤–6,å®ˆ6,æ‰Ž6,é˜¿6,å®›6,æœ6,å¸6,å³»6,æ£º6,è€³6,åº6,èµµ6,å¯Ÿ6,æ¼ª6,æ‰6,å±•6,å†‰6,æ·±6,é¸¡6,å 6,å¼±6,èƒ¶6,æ±6,ç›Š6,èŠ¹6,ç•™6,ç—…6,èŒ—6,å°¤6,å‚€6,ç ”6,é»‘6,å®¿6,æœ‹6,ä½•6,è¿6,èƒ–6,è‡´6,åŽ6,æ·®6,ç‘Ÿ6,èˆœ6,å‹¤6,ç¬6,è–°6,ä¼‘6,æ²»6,èƒ6,å¾6,é¸¢6,èŠ‚6,å¯†6,ä¸™6,é˜™6,é¹«6,æˆŽ6,å‡½6,å®½6,ç¡•6,è†6,ç”˜6,æ˜”5,å¿†5,èµ«5,ç²‰5,è¿‘5,å¥—5,æ‰€5,ç§»5,è¯5,æª€5,æ‰“5,ç š5,æ—¶5,èœœ5,ä»¬5,åˆ‡5,æ— 5,è¿Ÿ5,æ³Š5,æ‚²5,ç®“5,è¼5,äº•5,æ­»5,ç¿…5,é²²5,ä¼5,è¾•5,å„€5,é™¨5,ç­‰5,ç±5,ç¦5,é…¿5,ä»€5,å¼¼5,ç‹©5,çŸ¥5,èµ°5,æ¶5,é›¾5,èŽ½5,å§Š5,æ²‰5,ç¢Ž5,æ·¼5,ç«¯5,è”¡5,åœ‹5,å¥½5,åŽ„5,å²¸5,å…«5,å†¢5,ç…5,çº¶5,æ²Ÿ5,æŽ5,æ¬5,å¿5,æ²§5,è¯5,å¼—5,è¡—5,éŸ¬5,ç»£5,ç›5,ä¸¾5,é‡‡5,ç¬™5,é³³5,çŽº5,é—»5,å«5,è”“5,åŒ¡5,éº“5,å©­5,æ·‡5,è§‰5,é˜”5,åŽ†5,å·¦5,å½“5,é‚ˆ5,æºŸ5,å§œ5,è‹“5,è°‹5,æ—¦5,è‹¦5,è¯©5,å­Ÿ5,å®¸5,æ£‰5,éœ5,é£˜5,å¯¼5,è°¢5,å…†5,å‚…5,è½²5,é¹Š5,æ¼©5,å®ª5,æžš5,äº¨5,å¤·5,å¨‰5,äºŽ5,æµ®5,æ¸¡5,èªž5,ç¾²5,å†·5,éº’5,æ·5,é›5,å¨†4,ç›¼4,å­˜4,å†¯4,æš—4,å¤„4,ç‘š4,å¸–4,éš¼4,æµ†4,èˆ°4,çº²4,åž’4,é´4,å¼•4,å³’4,å†…4,å®´4,è†4,ç­‘4,é”™4,é’¥4,éª„4,éƒ4,ç«¿4,å£¤4,æ²Œ4,çŽ°4,ä¹˜4,äºž4,æ€§4,æˆ‘4,è§†4,ç»“4,ç¥€4,è¢4,èº¯4,ç…™4,è„Š4,å¢™4,å¼©4,å”¤4,å¸¦4,äº«4,èŒ«4,ä»£4,æœµ4,é”4,ç½•4,å¤™4,ç»’4,å£³4,ä»‹4,æ¶¡4,çº£4,åºž4,åŸƒ4,åŸ4,å°„4,å®…4,æ­¢4,èŠ®4,èˆ4,å¾µ4,å½©4,èœ4,è¾¹4,è€Œ4,èŠ½4,è“¬4,æŸ¥4,è£•4,éš¾4,ç”»4,å··4,èƒ¡4,æ¹¾4,ä¿ 4,å‰›4,é™‡4,æ„š4,çž4,å…®4,æ“Ž4,é 4,å“4,æ¥·4,ç®«4,é€‚4,ç€4,æ²¹4,åˆ«4,äºˆ4,æ²…4,ç£4,å¼4,çºµ4,è‡»4,è±†4,å…”4,åœ¨4,é©´4,é”®4,ç¤¾4,æ¤…4,é˜€4,å¦ž4,ç‘¤4,å¡˜4,ç¦…4,çœ 4,è‚¯4,æ²«4,å……4,çº4,å¦¤4,ç»®4,è‹¹4,ä»•4,æ»”4,è““4,ç¥¯4,ç³–4,å¤®4,å4,æ¼”4,è¡4,æ­†4,é¹ƒ4,ç4,é™¶4,æ¡¢4,ç„š4,çª4,çª4,å…4,ç¦§4,å«¦4,ç¿Œ4,æ¡©4,æ•¦4,æ¢§4,æ˜§4,åœ­4,è‹—4,å³¦4,å³4,é’—4,æ»Ÿ4,é’Š4,é€µ4,å‘4,èœ€4,æ¶…4,å­œ4,éŸ¦4,æŒº4,å†•4,å¿˜4,çŽ®4,ç¨4,ç»¿4,ç»ª4,æ‚Ÿ4,æ½œ4,é™ˆ4,æ¶¦4,è¾½4,æ”¸4,æž¢4,ä¿ª4,æ…•4,ç¬ 4,é—¯4,å›º4,è–™4");
function tokenizeName(t){
    if(! t[t.length-1] in ilchar){
        return t;
    }
    if(t.length == 3){
        var char2 = t.substring(0,2);
        if(ichar2.isPopular(char2)){
            return [char2 , t[2]];
        }
        if(ichar3.isPopular(t[0], 50) && ichar3.isPopular(t[1], 50)){
            return [t[0], t[1], t[2]];
        }
        if(ichar3.isPopular(t[0], 10) && ichar3.isPopular(t[1], 10) && ilchar.isPopular(t[2], 50)){
            return [t[0], t[1], t[2]];
        }
    }
    if(t.length == 4){
        var char2 = t.substring(0,2);
        if(ichar2.isPopular(char2) && ichar3.isPopular(t[2])){
            return [char2, t[2], t[3]];
        }
        if(ichar3.allIsPopular(t.substring(0,3), 50)){
            return [t[0], t[1], t[2], t[3]];
        }
        if(ichar3.allIsPopular(t.substring(0,3)) && ilchar.isPopular(t[3] , 50)){
            return [t[0], t[1], t[2], t[3]];
        }
    }
    if(t.length == 5){
        var char2 = t.substring(0,2);
        var char22 = t.substring(2,4);
        if(ichar2.isPopular(char2) && ichar2.isPopular(char22)){
            return [char2, char22, t[4]];
        }
        if(ichar2.isPopular(char2) && ichar3.allIsPopular(char22)){
            return [char2, ...char22.split(""), t[4]];
        }
        if(ichar2.isPopular(char22) && ichar3.allIsPopular(char2)){
            return [...char2.split(""), char2 , t[4]];
        }
        if(ichar3.allIsPopular(t.substring(0,4), 50)){
            return [t[0], t[1], t[2], t[3], t[4]];
        }
    }
    if(t.length > 5){
        var popularity = 0;
        for(var i = 0; i < t.length; i++){
            if(ichar3.isPopular(t[i],50)){
                popularity++;
            }
        }
        if(popularity > 4 && ichar3.isPopular(t[0])){ 
            return t.split("");
        }
        if(popularity > 3 && ichar2.isPopular(t.substring(0,2))){ 
            return t.split("");
        }
    }
    return t;
}
function parseNameRow(row){
	var row = e.split("=");
	if(row.length<2){}
	else{
		if(row[0]!=""){
			if(row[0].charAt(0)=="@"){
				row[0]=row[0].substring(1).split("|");
				if(row[1]!=null)
					row[1]=row[1].split("|");
				replaceByNode(row[0],row[1]);
			}else 
			if(row[0].charAt(0)=="#"){
				dictionary.set(row[0].substring(1),row[1]);
			}else 
			if(row[0].charAt(0)=="$"){

				var sear=row[0].substring(1);
				var rep=row.joinlast(1);
				if(sear.length==1){
					if(convertohanviets(sear)==rep.toLowerCase()){
						return;
					}
				}
				if(true){

					dictionary.set(sear,rep);
					nametree.setmean(sear,"="+rep);
				}else
				replaceOnline(sear,rep);
			}else 
			if(row[0].charAt(0)=="~"){
				meanengine(e.substr(1));
			}
			else{
				toeval2+="replaceByRegex(\""+eE(row[0])+"\",\""+eE(row[1])+"\");";
			}
		}
		
	}
}
function excuteContainer(){
	if(g(contentcontainer)==null)return;
	// if(getCookie("foreignlang") && getCookie("foreignlang") != "vi"){
	// 	return;
	// }
	// if(getCookie("transmode") == "chinese"){
	// 	return;
	// // }
	// if(dictionary.finished==false){
	// 	dictionary.readTextFile("//sangtacviet.com/wordNoChi.htm?update=1");
	// 	phrasetree.load();
	// 	tse.connect();
	// 	return;
	// }
	// if(tse.ws.readyState!=1){
	// 	tse.autoexcute=true;
	// 	tse.connect();
	// }
	var curl = document.getElementById("hiddenid").innerHTML.split(";");
	var book=curl[0];
	var chapter = curl[1];
	var host = curl[2];
	if(host=="sangtac")return;
	hideNb();
	//if(g("tmpcontentdiv")){
	//	pushFromView();
	//}
	
	if(host!="dich")
	fastNaming();
	prediction.enable=true;
	if(!window.appdb){
		return;
	}
	window.appdb.getName(host,book).then(function(namedata){
		if(namedata){
			for(var i = 0; i < namedata.length; i++){
				var e = namedata[i];
				parseNameRow(e);
			}
		}
		replaceVietphrase();
		if(window.setting&& window.setting.allownamev3){
			replaceName();
		}
		needbreak=false;
		meanengine.usedefault();
		if(!tse.connecting){
			if(invokeMeanSelector==null || invokeMeanSelector!==false){
				window.meanSelectorCheckpoint = 0;
				if(window.lazyProcessor){
					window.lazyProcessor.clear();
				}
				meanSelector();
			}
		}
		
		setTimeout(doeval,100);
		runned=true;
	});
}
function getEditSuggest(t,e,jn){
	var suggest = [];
	suggest.cleanDuplicate = function(){
		var newSuggest = [];
		for(var i = 0; i < suggest.length; i++){
			var e = suggest[i];
			if(!newSuggest.find(obj=>obj.text == e.text)){
				newSuggest.push(e);
			}
		}
		suggest.length = 0;
		newSuggest.sort(function(a,b){
			return b.priority - a.priority;
		});
		for(var i = 0; i < newSuggest.length; i++){
			suggest.push(newSuggest[i]);
		}
	}
	getTfcoreSuggest(t, function(sg){
		if(suggest.find(obj=>obj.text == sg)){
			var old = suggest.find(obj=>obj.text == sg);
			old.priority = 3;
			suggest.cleanDuplicate();
			suggest.onUpdate && suggest.onUpdate();
			return;
		}
		var isTitleCase = sg == titleCase(sg);
		suggest.push({ 
			text: sg,
			priority: 3,
			tag: isTitleCase ? "tf,name" : "tf,vp" 
		});
		suggest.cleanDuplicate();
		suggest.onUpdate && suggest.onUpdate();
	});
	if(phrasetree.getmean(t)!=""){
		var l = phrasetree.getmean(t).split('/');
		for(var i = 0; i < l.length; i++){
			suggest.push(
				{ 
					text: l[i],
					priority: 1,
					tag: "vp"
				});
		}
	}
	else{
		if(e && e.mean()){
			var l = e.mean().split('/');
			for(var i = 0; i < l.length; i++){
				suggest.push(
					{ 
						text: l[i],
						priority: 1,
						tag: "vp"
					});
			}
		}
	}
	ajax("sajax=getnamefromdb&name="+encodeURIComponent(t.trim()),function(down){
		var da=down.split("/");
		var sg = da[0];
		if(sg && !sg.match(/cáº©u|nháº­t/i)){
			suggest.push({ 
				text: sg,
				priority: 4,
				tag: "db" 
			});
			suggest.cleanDuplicate();
			suggest.onUpdate && suggest.onUpdate();
		}
	});
	getBingSuggest(t,function(d){
		var isTitleCase = d == titleCase(d);
		if(isTitleCase){
			suggest.push({ 
				text: d,
				priority: 2,
				tag: "bing" 
			});
			suggest.push({ 
				text: titleCase(convertohanviets(t)),
				priority: 2,
				tag: "name" 
			});
			suggest.cleanDuplicate();
			suggest.onUpdate && suggest.onUpdate();
		}else{
			suggest.push({ 
				text: d,
				priority: 1,
				tag: "bing" 
			});
			suggest.cleanDuplicate();
			suggest.onUpdate && suggest.onUpdate();
		}
	});
	suggest.push({ 
		text: titleCase(convertohanviets(t)),
		priority: 0,
		tag: "name" 
	});
	suggest.base = t;
	if(jn && t.length < 8){
		getTfcoreNameSuggest(t, function(sg){
			if(sg.JAP){
				sg = sg.JAP;
			}else{
				return;
			}
			suggest.push({ 
				text: sg,
				priority: 2,
				tag: "tf,jp"
			});
			suggest.cleanDuplicate();
			suggest.onUpdate && suggest.onUpdate();
		});
		googletranslateNocache(t,function(sg){
			suggest.push({ 
				text: sg,
				priority: 1,
				tag: "gg"
			});
			suggest.cleanDuplicate();
			suggest.onUpdate && suggest.onUpdate();
		});
	}
	return suggest;
}
function appSelectNode(e){
	if(e.currentTarget){
		e=e.currentTarget;
	}
	if(typeof setting !="undefined"){
		if(setting.allowtaptoedit!=null&&!setting.allowtaptoedit){
			return;
		}
	}
	if(selNode!=null && selNode.indexOf(e)!=-1){
		return;
	}
	unlock();
	selNode=[];
	e.style.color="red";
	basestr=e.innerHTML;
	// if(true){
	// 	var offset = getPos(e);
	// 	if(offset.x+257>windowWidth){
	// 		nb.style.left=(windowWidth-256)+"px";
	// 	}else{
	// 		nb.style.left=offset.x+"px";
	// 	}
	// 	nb.style.top=(e.offsetTop + offset.h) +"px";
	// }
	//showNb();
	selNode.push(e);
	return true;
}
function appExpandRight(e){
	var nextNode = nextNSibling(e);
	if(!nextNode){return;}
	var t1,t2,t3,t4;
	if(nextNode.nodeType==3){
		return appExpandRight(nextNode);
	}
	return nextNode.gT();
}
// function nextNSibling(e){
// 	var nod =selNode[selNode.length-1].nextSibling;
// 	if(nod.nodeType!=3)
// 	nod.style.color="red";
// 	selNode.push(nod);
// 	return selNode[selNode.length-1];
// }
function appExpandLeft(e){
	var nextNode = previousNSibling(e);var t1,t2,t3,t4;
	if(nextNode.nodeType==3){
		leftflag=true;
		return appExpandLeft(nextNode);
	}
	return nextNode.gT();
}
function getSelectedNodeChinese(){
	var s = "";
	for(var i = 0 ;i < selNode.length; i++){
		if(selNode[i].nodeType==3){
			continue;
		}
		s+=selNode[i].gT();
	}
	return s;
}
function tfTokenizer(text){
	var sentences = [];
	var sentence = "";
	var lastChar = "";
	var tokens = {
		"ã€‚": true,
		"ï¼Ÿ": true,
		"ï¼": true,
		"ï¼›": true,
		"â€": true,
		".": true,
		"?": true,
		"!": true,
		";": true,
	}
	for(var i = 0; i < text.length; i++){
		var char = text[i];
		if(char in tokens){
			if(lastChar in tokens){
				sentence += char;
			}else{
				sentence += char;
				if(sentence.length < 99){
					sentences.push(sentence);
				}
				sentence = "";
			}
		}else{
			sentence += char;
		}
		lastChar = char;
	}
	if(sentence && sentence.length < 99){
		sentences.push(sentence);
	}
	return sentences;
}
function tfDetname(){
	if(window.detnameLock){
		return;
	}
	var c = g(contentcontainer);
	var z = "";
	for(var i=0;i<c.childNodes.length;i++){
		if(c.childNodes[i].nodeType == 3){
			z+=c.childNodes[i].textContent;
		}else{
			z+=c.childNodes[i].gT();
		}
	}
	z = tfTokenizer(z).join("");
	var xhttp =  new XMLHttpRequest();
	xhttp.open("POST","/tfcore.php?detname=true");
	xhttp.onreadystatechange = function(){
		if(xhttp.readyState==4 && xhttp.status==200){
			var w=ui.win.create("Lá»c name");
			w.id = "detnamewin";
			window.detnameLock = false;
			var l = JSON.parse(xhttp.responseText);
			var lnames = l.lownames.join("\n");
			var names = l.names.join("\n");
			var r = w.body.row()
			r.addText("Name Ä‘Ã£ phÃ¡t hiá»‡n");
			var r = w.body.row();
			r.innerHTML = `<textarea id="detectedName" class="w-100" style="min-height: 250px">${names}</textarea>`;
			var r = w.body.row();
			r.addText("Tá»« ngá»¯ phá»• biáº¿n Ä‘Ã£ phÃ¡t hiá»‡n");
			if(lnames.length<2){
				r.style.display = "none";
			}
			var r = w.body.row();
			r.innerHTML = `<textarea id="detectedLowName" class="w-100" style="min-height: 90px">${lnames}</textarea>`;
			if(lnames.length<2){
				r.style.display = "none";
			}
			var r = w.body.row();

			var btn = r.addButton("Chá»‰ dÃ¹ng names", "useAllNameDetected()");
			if(lnames.length<2){
				btn.style.display = "none";
			}
			r.addButton("DÃ¹ng táº¥t cáº£", "useAllNameAndLowNameDetected()");
			w.show();
		}
	}
	xhttp.send(z.replace(/ +/g, "").replace(/\./g,"ã€‚").replace(/â€œ/g,"â€œ").replace(/â€/g,"â€"));
	window.detnameLock = true;
}
function useAllNameDetected(){
	var t = g("detectedName").value;
	namew.value = t+"\n"+namew.value;
	saveNS();
	excute();
	if(g("detnamewin")){
		g("detnamewin").hide();
	}
}
function useAllNameAndLowNameDetected(){
	var t = g("detectedName").value;
	var t2 = g("detectedLowName").value;
	namew.value =t2 +"\n" + t+"\n"+namew.value;
	saveNS();
	excute();
	if(g("detnamewin")){
		g("detnamewin").hide();
	}
}
var stvTts = {
	server: "wss://staticvn.sangtacvietcdn.xyz/audio/",
	ws: null,
	ready: false,
	voiceid:0,
	init: function(){
		this.ws = new WebSocket(this.server);
		this.ws.binaryType = "arraybuffer";
		this.ws.onmessage = this.decodeMessage.bind(this);
		this.ws.onopen = (function(){
			this.ready = true;
		}).bind(this);
	},
	getMessageId: function(){
		var text = "";
	    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
	    for (var i = 0; i < 20; i++)
			text += possible.charAt(Math.floor(Math.random() * possible.length));
	    return text;
	},
	base64ToArrayBuffer: function(base64) {
	    var binary_string =  window.atob(base64);
	    var len = binary_string.length;
	    var bytes = new Uint8Array( len );
	    for (var i = 0; i < len; i++)        {
	        bytes[i] = binary_string.charCodeAt(i);
	    }
	    return bytes.buffer;
	},
	decodeMessage: function(e){
	    var messageId = e.data.substring(0, 20);
	    var data = e.data.substring(20);
	    var arrayBuffer = this.base64ToArrayBuffer(data);
	    var blob = new Blob([arrayBuffer], {type: "audio/wav"});
	    var url = URL.createObjectURL(blob);
	    var audio = new Audio(url);
	    audio.play();
	},
	synth: function(text){
	    var voiceid = ("00" + this.voiceid).slice(-2);
	    var messageId = this.getMessageId();
	    var data = messageId + voiceid + text;
	    this.ws.send(data);
	},
	getVoices: function(){
		var vcs = [];
		for(var i=0;i<64;i++) vcs.push("Giá»ng "+(i+1));
		return vcs;
	},
	setVoice: function(voiceName){
		this.voiceid = parseInt(voiceName.substring(6)) - 1;
	}
}
Dịch