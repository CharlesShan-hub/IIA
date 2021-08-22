// 用于建立与服务器的联系
var ip = setting.ip;
var port = setting.port;
var wsObj;  

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
        if(data.reply=='100'){
            window.location.href="./main.html?mail="+mail;
        }else{
            alert('禁止登陆！')
            wsObj.close();
        }
    }
}

function to_login(event){
	var event=window.event?window.event:event;   
	if(event.keyCode==13){
		login();
	}
}
