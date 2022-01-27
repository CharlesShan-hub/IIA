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

function charCodeAt(str){

    var length = str.length,
        num = 0,
        utf16Arr = [];

    for(num; num < length; num++){
        utf16Arr[num] = '0x'+str[num].charCodeAt().toString(16);
    }

    return utf16Arr;
}
//charCodeAt('𢈢');//['0xD848', '0xDE22']


function test_upload_small_file(){
    // 判断文件大小
    var MaxSize = 1024*64;
    var file    = document.getElementById("small_file").files[0];
    if((file.size / MaxSize)>1){
        alert("File size should smaller than 64KB");
        return;
    }
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    wsObj.onopen = function(){  

        var reader  = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = function loaded(evt) {
            var content = '{"type":"test","operate":"upload file","state":"start"}';
            wsObj.send(content);

            wsObj.send(this.result);

            content = '{"type":"test","operate":"upload file","state":"end","name":"'+file.name+'"}';
            wsObj.send(content);

            wsObj.close();
        }
    }
}

var ccc;
function test_upload_large_file(){
    // 判断文件大小
    var MaxSize = 1024*32;
    var file    = document.getElementById("large_file").files[0];
    //alert(file.size / MaxSize);
    ccc = file.name;
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    wsObj.onopen = function(){  
        alert(parseInt(file.size/MaxSize)+1)
        var content = '{"type":"test","operate":"upload file","state":"start","len":"'+(parseInt(file.size/MaxSize)+1).toString()+'"}';
        wsObj.send(content);

        var start;
        var count=0;
        var sequence=0;
        var reader_array = new Array();
        var reader_last  = new FileReader();

        //reader_last.onloadstart=function onloadstart_last(evt){
        //    this.id = sequence;
        //    sequence++;
        //}

        reader_last.onload = function loaded_last(evt) {
            //ccc=this.result;
            //console.log(this.result);
            //alert(this.result);
            wsObj.send(this.result);
            content = '{"type":"test","operate":"upload file","state":"end","name":"'+file.name+'"}';
            wsObj.send(charCodeAt(content));
            wsObj.close();
        }

        function loaded(evt) {
            //alert(1);
            wsObj.send(this.result);
        }

        for(start=0,count=0;start<file.size;start+=MaxSize,count++){
            if(start + MaxSize>file.size){
                //alert(start,file.size);
                reader_last.readAsDataURL(file.slice(start, file.size));
                //reader_last.readAsText(file.slice(start, file.size),'gb2312');
                //reader_last.readAsArrayBuffer(file.slice(start, file.size),"GB2312");
            }else{
                //alert(start,start+MaxSize);
                reader_array[count]=new FileReader();
                reader_array[count].onload = loaded;
                //reader_array[count].onloadstart=function onloadstart(evt){
                    //this.id = sequence;
                    //sequence++;
                //}
                reader_array[count].readAsDataURL(file.slice(start, start + MaxSize));
                //reader_array[count].readAsText(file.slice(start, start + MaxSize),'gb2312');
                //reader_array[count].readAsArrayBuffer(file.slice(start, start + MaxSize),"GB2312");
            }
        }
    }
}

function test_file(){
    // 判断文件大小
    var MaxSize = 10;
    var start;
    var count=0;
    var sequence=0;
    var reader_array = new Array();
    var reader_last  = new FileReader();

    reader_last.onload = function loaded_last(evt) {
        alert(this.result);
    }

    function loaded(evt) {
        alert(this.result);
    }

    var file    = document.getElementById("file").files[0];
    for(start=0,count=0;start<file.size;start+=MaxSize,count++){
        if(start + MaxSize>file.size){
            reader_last.readAsText(file.slice(start, file.size));
        }else{
            reader_array[count]=new FileReader();
            reader_array[count].onload = loaded;
            reader_array[count].readAsText(file.slice(start, start + MaxSize));
        }
    }
}

var ccc
function test_file2(){
    // 判断文件大小
    var MaxSize = 1024*64;
    var file    = document.getElementById("file2").files[0];
    // 建立连接
    var wsObj = new WebSocket("ws://"+ip+":"+port);

    wsObj.onopen = function(){  
        alert(parseInt(file.size/MaxSize)+1)
        var content = '{"type":"test","operate":"upload file","state":"start","name":"'+file.name+'","len":"'+(parseInt(file.size/MaxSize)+1).toString()+'"}';
        alert(content);
        wsObj.send(charCodeAt(content));

        var start;
        var count=0;
        var sequence=1;
        var reader_array = new Array();
        var reader_last  = new FileReader();

        reader_last.onload = function loaded_last(evt) {
            //ccc = this.result;
            var content = this.result.replace(/\+/g, "-")
            content = content.replace(/\//g, "_")
            wsObj.send('{"type":"test","operate":"upload file","state":"send","sequence":'+sequence.toString()+',"content":"'+content+'"}');
            content = '{"type":"test","operate":"upload file","state":"end","name":"'+file.name+'"}';
            wsObj.send(charCodeAt(content));
            wsObj.close();
        }

        function loaded(evt) {
            //alert(1);
            var content = this.result.replace(/\+/g, "-")
            content = content.replace(/\//g, "_")
            wsObj.send('{"type":"test","operate":"upload file","state":"send","sequence":'+sequence.toString()+',"content":"'+content+'"}');
            sequence++;
        }

        for(start=0,count=0;start<file.size;start+=MaxSize,count++){
            if(start + MaxSize>file.size){
                reader_last.readAsDataURL(file.slice(start, file.size));
                //reader_last.readAsText(file.slice(start, file.size),'gb2312');
                //reader_last.readAsArrayBuffer(file.slice(start, file.size),"GB2312");
            }else{
                //alert(start,start+MaxSize);
                reader_array[count]=new FileReader();
                reader_array[count].onload = loaded;
                //reader_array[count].onloadstart=function onloadstart(evt){
                    //this.id = sequence;
                    //sequence++;
                //}
                reader_array[count].readAsDataURL(file.slice(start, start + MaxSize));
                //reader_array[count].readAsText(file.slice(start, start + MaxSize),'gb2312');
                //reader_array[count].readAsArrayBuffer(file.slice(start, start + MaxSize),"GB2312");
            }
        }
    }
}

