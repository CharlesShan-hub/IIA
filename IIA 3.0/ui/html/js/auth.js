function load(){
	// 自动填充默认用户邮箱
	document.getElementById('mail').value = local_setting.default_mail;
}

function auth(){
	mail = document.getElementById('mail').value;
	password = document.getElementById('password').value;
	if(mail==""||password=="")
		return;
	login(mail,password);
}

function do_auth(event){
	var event=window.event?window.event:event;   
		if(event.keyCode==13){
			auth();
	}
}