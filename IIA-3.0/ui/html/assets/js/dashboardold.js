var row_element = new Array();

function init_all_element_position(){
	for(var index_y=0;index_y<row_element.length;index_y++){
		for(var index_x=0;index_x<row_element[index_y][2].length;index_x++){
			var element = document.getElementById("dashboard_list").childNodes.item(index_y).childNodes.item(index_x);
			var box = document.getElementById("dashboard_list");
			row_element[index_y][2][index_x]["x"]=element.offsetLeft-box.offsetLeft;
			row_element[index_y][2][index_x]["y"]=element.offsetTop-box.offsetTop;
			row_element[index_y][2][index_x]["width_px"]=element.offsetWidth;
			row_element[index_y][2][index_x]["height_px"]=element.offsetHeight;
		}
	}
}

function init_element_position(row,index){
	// 第row行的第index下标元素
	var element = document.getElementById("dashboard_list").childNodes.item(row).childNodes.item(index);
	//alert(element.className);
	//alert(element.offsetLeft);
	//alert(element.offsetTop)
	//alert(row_element[row][2]["width"]);
	var box = document.getElementById("dashboard_list");
	row_element[row][2][index]["x"]=element.offsetLeft-box.offsetLeft;
	row_element[row][2][index]["y"]=element.offsetTop-box.offsetTop;
	row_element[row][2][index]["width_px"]=element.offsetWidth;
	row_element[row][2][index]["height_px"]=element.offsetHeight;
}

function init_list_add_element(){
	var row = document.createElement("div");
	row.className="row";
	var dlist = document.getElementById('dashboard_list');
	dlist.appendChild(row);
	var element_content = new Array();
	element_content.push(4);
	element_content.push(row);
	element_content.push(new Array());

	return element_content;
}

function init_list(){
	// 空界面
	if(row_element.length==0){
		row_element.push(init_list_add_element());
	}
	// 最后一行满
	if(row_element[row_element.length-1][0]==0){
		row_element.push(init_list_add_element());
	}
	// 最后一行不满 - 成功
	return row_element.length-1;
}


function init_display_setting(){
	var div_ = document.createElement("div");
	div_.className="btn-group mr-1 mt-2 display_setting";
	div_.innerHTML="<button class=\"btn btn-secondary btn-sm dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">Small button <i class=\"mdi mdi-chevron-down\"></i></button><div class=\"dropdown-menu\"><a class=\"dropdown-item\" href=\"#\">Action</a><a class=\"dropdown-item\" href=\"#\">Another action</a><a class=\"dropdown-item\" href=\"#\">Something else here</a><div class=\"dropdown-divider\"></div><a class=\"dropdown-item\" href=\"#\">Separated link</a></div>"
	//div.style.display="none";
	return div_;
}

function init_display_box(){
	var div = document.createElement("div");
	div.className="col-xl-3 col-md-6";
	var div2 = document.createElement("div");
	div2.className="card mini-stat bg-primary text-white";
	//div.appendChild(init_display_setting());
	div.appendChild(div2);
	var div3 = document.createElement("div");
	div3.className="card-body";
	div2.appendChild(div3);
	var div4 = document.createElement("div");
	div4.className="mb-4";
	div3.appendChild(div4);
	var div5 = document.createElement("div");
	div5.className="float-left mini-stat-img mr-4";
	div4.appendChild(div5);
	var img = document.createElement("img");
	img.src="assets/images/services-icon/01.png";
	div5.appendChild(img);
	var h5 = document.createElement("h5");
	h5.className="font-size-16 text-uppercase mt-0 text-white-50";
	h5.innerHTML="Orders";
	div4.appendChild(h5);
	var h4 = document.createElement("h4");
	h4.className="font-weight-medium font-size-24";
	h4.innerHTML="1,685";
	div4.appendChild(h4);
	var h4i = document.createElement("i");
	h4i.className="mdi mdi-arrow-up text-success ml-2";
	h4.appendChild(h4i);
	var div6 = document.createElement("div");
	div6.className="mini-stat-label bg-success";
	div4.appendChild(div6);
	var p = document.createElement("p");
	p.className="mb-0";
	p.innerHTML="+ 12%";
	div6.appendChild(p);

	var div7 = document.createElement("div");
	div7.className="pt-2";
	div3.appendChild(div7);
	var div8 = document.createElement("div");
	div8.className="float-right";
	div7.appendChild(div8);
	var a = document.createElement("a");
	a.className="text-white-50";
	div8.appendChild(a);
	var ai = document.createElement("i");
	ai.className="mdi mdi-arrow-right h5";
	a.appendChild(ai);
	var p2 = document.createElement("p");
	p2.className="text-white-50 mb-0 mt-1";
	p2.innerHTML="Since last month";
	div7.appendChild(p2);

	return div;
}

function add_display_element(element_id){
	current = init_list();
	
	element_id = 1;
	switch(element_id){
		case 1://卡片box
			var element_width=1;
			row_element[current][0]-=element_width;
			row_element[current][1].appendChild(init_display_box());
			row_element[current][2].push({width:1});
			break;
		default:
			alert("Wrong Type of Element");
	}
}

function to_adjust_mode(){
	for(var index_y=0;index_y<row_element.length;index_y++){
		for(var index_x=0;index_x<row_element[index_y][2].length;index_x++){
			var element = document.getElementById("dashboard_list").childNodes.item(index_y+1).childNodes.item(index_x);
			alert(element.offsetWidth);
		}
	}
}

function to_save_mode(){
	for(var index_y=0;index_y<row_element.length;index_y++){
		for(var index_x=0;index_x<row_element[index_y][2].length;index_x++){
			var element = document.getElementById("dashboard_list").childNodes.item(index_y+1).childNodes.item(index_x);
			alert(element.childNodes.item(1));
		}
	}
}

function adjust_or_save(){
	var button_ad_sa = document.getElementById("adjust_or_save_button");
	if(button_ad_sa.innerHTML[0]=="A"){
		button_ad_sa.innerHTML="Save   UI";
		to_adjust_mode();
	}else{
		button_ad_sa.innerHTML="Adjust UI";
		to_save_mode();
	}
	
}
