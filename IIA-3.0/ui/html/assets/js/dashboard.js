// ************************************************
// 这些是添加页面元素的内容
// ************************************************

var row_element = new Array();

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

function init_display_box_set_color(element){
	// 找到元素
	element = element.parentNode.parentNode.parentNode;
}

function init_display_box_setting(){
	var div = document.createElement("div");
	div.className="btn-group mr-1 mt-2 display_setting";
	//div.innerHTML="<button class=\"btn btn-secondary btn-sm dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">Setting<i class=\"mdi mdi-chevron-down\"></i></button><div class=\"dropdown-menu\"><a class=\"dropdown-item\" href=\"#\">Action</a><a class=\"dropdown-item\" href=\"#\">Another action</a><a class=\"dropdown-item\" href=\"#\">Something else here</a><div class=\"dropdown-divider\"></div><a class=\"dropdown-item\" href=\"#\">Separated link</a></div>"
	div.innerHTML="<button class=\"btn btn-secondary btn-sm dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">Setting<i class=\"mdi mdi-chevron-down\"></i></button><div class=\"dropdown-menu\"><a class=\"dropdown-item\" href=\"#\" onclick=\"init_display_box_set_color(this)\">Color</a><div class=\"dropdown-divider\"></div><a class=\"dropdown-item\" href=\"#\" onclick=\"delete_element(this)\">Delete</a></div>"
	div.style.display="none";
	return div;
}

function init_display_box(){
	var div2 = document.createElement("div");
	div2.className="card mini-stat bg-primary text-white";
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

	return div2;
}

function init_display_box1(){
	var div = document.createElement("div");
	div.className="col-xl-3 col-md-6";
	div.appendChild(init_display_box_setting());
	div.appendChild(init_display_box());
	return div;
}

function init_display_box2(){
	var div = document.createElement("div");
	div.className="col-xl-3";
	var row = document.createElement("div");
	row.className = "row";

	var div1 = document.createElement("div");
	div1.className="col-md-12";
	div1.appendChild(init_display_box());
	var div_block = document.createElement("div");
	div_block.innerHTML="&nbsp<br>&nbsp";
	var div2 = document.createElement("div");
	div2.className="col-md-12";
	div2.appendChild(init_display_box());

	row.appendChild(div1);
	row.appendChild(div_block);
	row.appendChild(div2);
	div.appendChild(init_display_box_setting());
	div.appendChild(row);

	return div;
}

function init_display_video_set_url(){

}

function init_display_video_setting(){
	var div = document.createElement("div");
	div.className="btn-group mr-1 mt-2 display_setting";
	//div.innerHTML="<button class=\"btn btn-secondary btn-sm dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">Setting<i class=\"mdi mdi-chevron-down\"></i></button><div class=\"dropdown-menu\"><a class=\"dropdown-item\" href=\"#\">Action</a><a class=\"dropdown-item\" href=\"#\">Another action</a><a class=\"dropdown-item\" href=\"#\">Something else here</a><div class=\"dropdown-divider\"></div><a class=\"dropdown-item\" href=\"#\">Separated link</a></div>"
	div.innerHTML="<button class=\"btn btn-secondary btn-sm dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">Setting<i class=\"mdi mdi-chevron-down\"></i></button><div class=\"dropdown-menu\"><a class=\"dropdown-item\" href=\"#\" onclick=\"init_display_video_set_url(this)\">Color</a><div class=\"dropdown-divider\"></div><a class=\"dropdown-item\" href=\"#\" onclick=\"delete_element(this)\">Delete</a></div>"
	div.style.display="none";
	return div;
}

function add_display_video(){
	var div = document.createElement("div");
	div.className="col-lg-6";
	var div_content = document.createElement("div");
	div_content.className="card";
	content="<div class=\"card-body\">";
	content+="<h4 class=\"card-title\">Responsive embed video 4:3</h4>";
	content+="<p class=\"card-title-desc\">Aspect ratios can be customized with modifier classes.</p>";
	content+="<div class=\"embed-responsive embed-responsive-4by3\">";
	content+="<iframe class=\"embed-responsive-item\" src=\"https://www.youtube.com/embed/1y_kfWUCFDQ\"></iframe>";
	content+="</div>";
	content+="</div>";
	div_content.innerHTML=content;
	div.appendChild(init_display_video_setting());
	div.appendChild(div_content);
	
	return div;
}

function init_display_card_set_url(){

}

function init_display_card_setting(){
	var div = document.createElement("div");
	div.className="btn-group mr-1 mt-2 display_setting";
	//div.innerHTML="<button class=\"btn btn-secondary btn-sm dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">Setting<i class=\"mdi mdi-chevron-down\"></i></button><div class=\"dropdown-menu\"><a class=\"dropdown-item\" href=\"#\">Action</a><a class=\"dropdown-item\" href=\"#\">Another action</a><a class=\"dropdown-item\" href=\"#\">Something else here</a><div class=\"dropdown-divider\"></div><a class=\"dropdown-item\" href=\"#\">Separated link</a></div>"
	div.innerHTML="<button class=\"btn btn-secondary btn-sm dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">Setting<i class=\"mdi mdi-chevron-down\"></i></button><div class=\"dropdown-menu\"><a class=\"dropdown-item\" href=\"#\" onclick=\"init_display_card_set_url(this)\">Color</a><div class=\"dropdown-divider\"></div><a class=\"dropdown-item\" href=\"#\" onclick=\"delete_element(this)\">Delete</a></div>"
	div.style.display="none";
	return div;
}

function add_display_card(){
	var div = document.createElement("div");
	div.className="col-lg-6";
	var div_content = document.createElement("div");
	div_content.className="card";

	content="<div class=\"card-body\">";
	content+="<h4 class=\"card-title\">With controls</h4>";
	content+="<p class=\"card-title-desc\">Adding in the previous and next controls:</p>";
	content+="<div id=\"carouselExampleControls\" class=\"carousel slide\" data-ride=\"carousel\">";
	content+="<div class=\"carousel-inner\" role=\"listbox\">";
	content+="<div class=\"carousel-item active\">";
	content+="<img class=\"d-block img-fluid\" src=\"assets/images/small/img-4.jpg\" alt=\"First slide\">";
	content+="</div>";
	content+="<div class=\"carousel-item\">";
	content+="<img class=\"d-block img-fluid\" src=\"assets/images/small/img-5.jpg\" alt=\"Second slide\">";
	content+="</div>";
	content+="<div class=\"carousel-item\">";
	content+="<img class=\"d-block img-fluid\" src=\"assets/images/small/img-6.jpg\" alt=\"Third slide\">";
	content+="</div>";
	content+="</div>";
	content+="<a class=\"carousel-control-prev\" href=\"#carouselExampleControls\" role=\"button\" data-slide=\"prev\">";
	content+="<span class=\"carousel-control-prev-icon\" aria-hidden=\"true\"></span>";
	content+="<span class=\"sr-only\">Previous</span>";
	content+="</a>";
	content+="<a class=\"carousel-control-next\" href=\"#carouselExampleControls\" role=\"button\" data-slide=\"next\">";
	content+="<span class=\"carousel-control-next-icon\" aria-hidden=\"true\"></span>";
	content+="<span class=\"sr-only\">Next</span>";
	content+="</a>";
	content+="</div>";
	content+="</div>";
	content+="</div>";

	div_content.innerHTML=content;
	div.appendChild(init_display_card_setting());
	div.appendChild(div_content);

	return div;
}

function add_display_element(element_type){
	document.getElementById("place_holder").style.display="none";
	current = init_list();
	// element_id可以推算出元素位置与大小,比如占一个格的第一个元素: ele_0_0_1(坐标是数组下标,从零开始)
	
	switch(parseInt(element_type)){
		case 1://卡片box
			// 元素宽度(单位:格)
			var element_width=1;
			row_element[current][0]-=element_width;
			// 元素信息
			row_element[current][2].push({width:1});
			// 获取元素
			element = init_display_box1();
			// 生成元素id
			element_id = "ele_"+current.toString()+"_"+(row_element[current][2].length-1).toString();
			//alert(element_id+"_"+element_width.toString());
			element.setAttribute("id", element_id+"_"+element_width.toString());
			row_element[current][1].appendChild(element);
			break;
		case 2://卡片box
			// 元素宽度(单位:格)
			var element_width=1;
			row_element[current][0]-=element_width;
			// 元素信息
			row_element[current][2].push({width:1});
			// 获取元素
			element = init_display_box2();
			// 生成元素id
			element_id = "ele_"+current.toString()+"_"+(row_element[current][2].length-1).toString();
			//alert(element_id+"_"+element_width.toString());
			element.setAttribute("id", element_id+"_"+element_width.toString());
			row_element[current][1].appendChild(element);
			break;
		case 3://视频
			// 元素宽度(单位:格)
			var element_width=2;
			row_element[current][0]-=element_width;
			// 元素信息
			row_element[current][2].push({width:1});
			// 获取元素
			element = add_display_video();
			// 生成元素id
			element_id = "ele_"+current.toString()+"_"+(row_element[current][2].length-1).toString();
			//alert(element_id+"_"+element_width.toString());
			element.setAttribute("id", element_id+"_"+element_width.toString());
			row_element[current][1].appendChild(element);
			break;
		case 4://图
			// 元素宽度(单位:格)
			var element_width=2;
			row_element[current][0]-=element_width;
			// 元素信息
			row_element[current][2].push({width:1});
			// 获取元素
			element = add_display_card();
			// 生成元素id
			element_id = "ele_"+current.toString()+"_"+(row_element[current][2].length-1).toString();
			//alert(element_id+"_"+element_width.toString());
			element.setAttribute("id", element_id+"_"+element_width.toString());
			row_element[current][1].appendChild(element);
			break;
		default:
			alert("Wrong Type of Element");
	}
}

//var aaa;
function delete_element(element){
	// 找到元素
	element = element.parentNode.parentNode.parentNode;
	row = element.parentNode;
	// 删除元素信息
	index_y = parseInt(element.id.split('_')[1]);
	index_x = parseInt(element.id.split('_')[2]);
	index_length = parseInt(element.id.split('_')[3]);

	row_element[index_y][0]+=index_length;
	for(var count=index_x;count<row_element[index_y][2].length-2;count++){
		row_element[index_y][2][count]=row_element[index_y][2][count+1];
	}
	row_element[index_y][2].pop();
	row_element[index_y][1].childNodes.forEach(delete_element_change_id);
	function delete_element_change_id(item) {
		item_y = item.id.split('_')[1];
		item_x = parseInt(item.id.split('_')[2])-1;
		item_length = item.id.split('_')[3];
		item.id = "ele_"+item_y+"_"+item_x.toString()+"_"+item_length;
	}

	// 删除元素
	element.remove();

	// 删除空行
	if(row.childNodes.length==0){
		row.style.display="none";
	}

	// 重新初始化
	init_all_element_position();
}

// ************************************************
// 这些是进行位置调整的内容（包括是否可见按钮）
// ************************************************

function init_all_element_position(){
	for(var index_y=0;index_y<row_element.length;index_y++){
		for(var index_x=0;index_x<row_element[index_y][2].length;index_x++){
			var element = document.getElementById("dashboard_list").childNodes.item(index_y+1).childNodes.item(index_x);
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
	var element = document.getElementById("dashboard_list").childNodes.item(row+1).childNodes.item(index);
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

//var aaa;
//var bbb;
function to_adjust_mode(){
	//alert(row_element.length);
	//alert(row_element[0][2].length);
	for(var index_y=0;index_y<row_element.length;index_y++){
		for(var index_x=0;index_x<row_element[index_y][2].length;index_x++){
			var element = document.getElementById("dashboard_list").childNodes.item(index_y+1).childNodes.item(index_x);
			element.childNodes.item(0).style.display="inline";
		}
	}
}

function to_save_mode(){
	//alert(row_element.length);
	//alert(row_element[0][2].length);
	for(var index_y=0;index_y<row_element.length;index_y++){
		for(var index_x=0;index_x<row_element[index_y][2].length;index_x++){
			var element = document.getElementById("dashboard_list").childNodes.item(index_y+1).childNodes.item(index_x);
			element.childNodes.item(0).style.display="none";
		}
	}
}

function adjust_or_save(){
	var button_ad_sa = document.getElementById("adjust_or_save_button");
	if(button_ad_sa.innerText=="Adjust UI"){
		button_ad_sa.innerText="Lock   UI";
		to_adjust_mode();
		init_all_element_position();
	}else{
		button_ad_sa.innerText="Adjust UI";
		to_save_mode();
	}
}

var bbb;
//var element;
function test_alert(){
	init_all_element_position();
	//element = document.getElementById("dashboard_list").childNodes;
	//var element = document.getElementById("dashboard_list").childNodes.item(index_y+1).childNodes.item(index_x+1);
	//alert(element.offsetWidth);
}