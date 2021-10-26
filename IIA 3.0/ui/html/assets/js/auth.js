// 用于建立与服务器的联系
var ip = setting.ip;
var port = setting.port;


function load(){
	// 自动填充默认用户邮箱
	document.getElementById('mail').value = local_setting.default_mail;
}


function _login(mail,password){
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
		content = '{"type":"auth","operate":"login","password":"';
		content = content+password;
		content = content+'","mail":"';
		content = content+mail;
		content = content+'"}';
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        var data = JSON.parse(evt.data);
        if(data.reply=='100'){
            alert("Close!")
            wsObj.close();
            window.location.href="./index.html?mail="+mail;
        }else{
        	alert("Wrong password/mail or you are new to this computer!");
        }
        wsObj.close();
    }
}


function _regist(mail,password,username,code){
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
        var content = '{"type":"auth","operate":"regist","password":"';
        content = content+password;
        content = content+'","mail":"';
        content = content+mail;
        content = content+'","name":"';
        content = content+username;
        content = content+'","code":"';
        content = content+code;
        content = content+'"}';
        wsObj.send(content);
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        var data = JSON.parse(evt.data);
        if(data.reply=='100'){
            wsObj.close();
            window.location.href="./index.html?mail="+mail;
        }else if(data.reply=='200'){
            alert("Have send Code to your email!");
        }else{
            alert("Failed to Register.");
        }
        wsObj.close();
    }
}


function _find_password(mail,code){
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
        var content = '{"type":"auth","operate":"find password","code":"';
        content = content+code;
        content = content+'","mail":"';
        content = content+mail;
        content = content+'"}';
        wsObj.send(content);
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        var data = JSON.parse(evt.data);
        if(data.reply=='100'){
            alert("Close!")
            wsObj.close();
            window.location.href="./index.html?mail="+mail;
        }
    }
}


function login(){
	mail = document.getElementById('mail').value;
	password = document.getElementById('password').value;
	if(mail==""||password=="")
		return;
	_login(mail,password);
}


function regist(){
    mail = document.getElementById('mail').value;
    password = document.getElementById('password').value;
    username = document.getElementById('username').value;
    code = document.getElementById('code').value;
    if(mail==""||password==""||username=="")
        return;
    _regist(mail,password,username,code);
}

function request_regist(){
    mail = document.getElementById('mail').value;
    password = document.getElementById('password').value;
    username = document.getElementById('username').value;
    if(mail=="")
        return;
    _regist(mail,password,username,"request");
}


function find_password(){
	mail = document.getElementById('mail').value;
	code = document.getElementById('code').value;
	if(mail=="")
		return;
	if(code==""){
		_find_password(mail,"request");
	}else{
		_find_password(mail,code);
	}
}


/*
function do_auth(event){
	var event=window.event?window.event:event;   
		if(event.keyCode==13){
			auth();
	}
}*/

/*function do_find_password(event){
	var event=window.event?window.event:event;   
		if(event.keyCode==13){
			find_password();
	}
}*/
