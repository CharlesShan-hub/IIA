// 用于建立与服务器的联系
var ip = setting.ip;
var port = setting.port;

//-------------------------------------------------------------

function _test_ping(){
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
		content = '{"type":"test","operate":"ping","param":"0"}';
        wsObj.send(content);
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        alert("Success!");
        wsObj.close();
    }
}


function _test_ping_get_number(){
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    //发送请求
    wsObj.onopen = function(){  
        content = '{"type":"test","operate":"ping","param":"1"}';
        wsObj.send(content);
    }

    // 验证是否登陆
    wsObj.onmessage = function(evt){ 
        var data = JSON.parse(evt.data);
        alert("Get number "+data.reply.toString());
        wsObj.close();
    }
}

function _test_upload_file(){

}


//-------------------------------------------------------------

function load(){
    // 自动填充默认用户邮箱
    document.getElementById('mail').value = local_setting.default_mail;
}

function test_ping(mode){
    if(mode=='0'){
        _test_ping();
    }else if(mode=='1'){
        _test_ping_get_number();
    }else{
        _test_ping();
    }
}

function _test_login(mail,password){
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


function test_login(){
    mail = document.getElementById('mail').value;
    password = document.getElementById('password').value;
    if(mail==""||password=="")
        return;
    _test_login(mail,password);
}

function test_upload_file(){
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    wsObj.onopen = function(){  
        var file    = document.getElementById("file").files[0];
        var reader  = new FileReader();
        reader.readAsDataURL(file);
        //reader.readAsBinaryString(file,"gb2312");

        reader.onload = function loaded(evt) {
            //var binaryString = evt.target.result;

            var content = '{"type":"test","operate":"upload file","state":"start"}';
            wsObj.send(content);

            wsObj.send(this.result);

            content = '{"type":"test","operate":"upload file","state":"end","name":"'+file.name+'"}';
            wsObj.send(content);
        }






        //var inputElement = document.getElementById("file");
        //name=document.getElementById('file').files[0].name;
        //var reader = new FileReader();
        //以二进制形式读取文件
        //reader.readAsArrayBuffer(inputElement.files[0]);
        //reader.readAsBinaryString(inputElement.files[0]);
        //文件读取完毕后该函数响应
        //reader.onload = function loaded(evt) {
        //    var binaryString = evt.target.result;
            //alert(binaryString);
            //发送文件 
            //var content = '{"type":"test","operate":"upload file","state":"start"}';
            //wsObj.send(content);
            //if
            //wsObj.send(binaryString);
            //content = '{"type":"test","operate":"upload file","state":"end","name":"'+name+'"}';
            //wsObj.send(content);
        //}
    }
}