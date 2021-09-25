// 用于建立与服务器的联系
var ip = setting.ip;
var port = setting.port;
var wsObj; 

function regist(mail,password){
    // 建立连接
    wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
        var content = '{"type":"regist","password":"';
        content = content+document.getElementById('password').value;
        content = content+'","mail":"';
        content = content+document.getElementById('mail').value;
        content = content+'"}';
        wsObj.send(content);
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        var data = JSON.parse(evt.data);
        if(data.reply=='100'){
            window.location.href="./temp_main/index.html?mail="+mail;
        }
    }
}

function login(mail,password){
    // 建立连接
    wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
		content = '{"type":"login","password":"';
		content = content+password;
		content = content+'","mail":"';
		content = content+mail;
		content = content+'"}';
        wsObj.send(content);
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        var data = JSON.parse(evt.data);
        wsObj.close();
        if(data.reply=='100'){
            window.location.href="./temp_main/index.html?mail="+mail;
        }else{
            regist(mail,password);
        }
    }
}

function to_login(event){
	var event=window.event?window.event:event;   
	if(event.keyCode==13){
		login();
	}
}
