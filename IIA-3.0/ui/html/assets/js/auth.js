// 用于建立与服务器的联系
var ip = setting.ip;
var port = setting.port;


function load(){
	// 自动填充默认用户邮箱
	document.getElementById('mail').value = local_setting.default_mail;
}


function _login(mail,password,remember){
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
        content = '{"type":"auth","operate":"login","password":"';
        content = content+password;
        content = content+'","mail":"';
        content = content+mail;
        content = content+'"}';
        wsObj.send(content);
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        var data = JSON.parse(evt.data);
        if(data.reply=='100'){
            if(remember==true){
                content = '{"type":"auth","operate":"remember","mail":"';
                content = content+mail;
                content = content+'"}';
                wsObj.send(content);
            }
            wsObj.close();
            window.location.href="./index.html?mail="+mail;
            //alert("Successed to login!");
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
            alert("Don't Forget Your Password: xxxx")
            wsObj.close();
            window.location.href="./index.html?mail="+mail;
        }
        wsObj.close();
    }
}


function login(){
	mail = document.getElementById('mail').value;
	password = document.getElementById('password').value;
	if(mail==""||password=="")
		return;
    remember = document.getElementById('remember').checked;
	_login(mail,password,remember);
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
	if(mail==""){
        alert("Please Input Mail Address!");
        return;
    }
	if(code==""){
		_find_password(mail,"request");
	}else{
		_find_password(mail,code);
	}
}
