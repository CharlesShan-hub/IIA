// 用于建立与服务器的联系
var ip = setting.ip;
var port = setting.port;


//-------------------------------------------------------------
function _test_dash(){
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
            wsObj.close();
            //window.location.href="./index.html?mail="+mail;
            alert("Successed to login!");
        }else{
            alert("Wrong password/mail or you are new to this computer!");
        }
        wsObj.close();
    }
}