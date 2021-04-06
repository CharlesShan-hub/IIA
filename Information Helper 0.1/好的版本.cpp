#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <string>
#include <windows.h>
#include <conio.h>

//模板 
struct club
{
	int type;
	char class_name[32];
	char item[20][32];	
	char name[20][32];	
};

//信息查询  
struct Website
{
	int type;
	char find1[16];
	char find2[16];
	char find3[16];
	char find4[16];
	char web[64];
	char describe[64];
};
//功能函数 
int information_check();//信息查询 
	int infor_check_all();//查询所有信息  
	int infor_check_web();//查询网页信息  
int information_add();//信息增加
	int infor_add_Website();//添加网页信息 
int club_control(); //模板系统 
	int club_control_creat();//模板创建 
	int club_control_check();//模板查看 
	int club_control_change();//模板更改 
		int club_control_change_ClubValid(char[]);//用户输入的名称是否已创建 
	int club_control_copy();//模板备份 
	
//工具函数 
int judge_num(char num[]);//判断用户输入是否为整数
int judge_kongge(char[]);//判断用户输入是否有空格

//*************************************主函数（一级选择）**************************************
int main()
{
	char choice[16]={'\0'};//获得用户选择 
	int repeat = 1;//判断是否循环选择 
	
	/*一级功能选择*/ 
	while(repeat){
		while(1){//获得选择 
			system("cls");//清屏
			printf("\n直接离开程序  请输入0\n");
			printf("进行信息添加  请输入1\n");
			printf("进行信息查找  请输入2\n");
			printf("进入模板控制  请输入3\n");
			
			fflush(stdin);
			scanf("%s",choice);
			if(judge_num(choice)!=0)
				continue;//判断不是数字，再次输入 
			if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2&&atoi(choice)!=3)
				continue;//判断无效数字，再次输入 
		 	break;
		}
		switch(atoi(choice))//进入对应功能 
		{
			case 1: repeat = information_add();break;//信息添加函数 
			case 2: repeat = information_check();break;//信息查找函数 
			case 3: repeat = club_control();break;//模板控制函数 
			case 0: repeat = 0;break;//直接退出程序		 
		}	
	}//repeat 循环结束 
	return 0;
}

//*************************************信息添加（二级选择）**************************************

int information_add()//信息添加主函数 
{
	char choice[16]={'\0'};//
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//清屏 
			printf("\n直锟斤拷锟剿筹拷锟斤拷锟斤拷  请输入0\n");
			printf("锟斤拷锟斤拷锟较硷拷锟斤拷锟斤拷  请输入1\n");
			printf("锟斤拷锟斤拷锟揭筹拷锟较? 请输入2\n");
			fflush(stdin);
			scanf("%s",choice);
			if(judge_num(choice)!=0)
				continue;
			if(atoi(choice)!=1&&atoi(choice)!=2&&atoi(choice)!=0)
				continue;
		 	break;
		}
		switch(atoi(choice))
		{
			case 0: return 0;
			case 1: return 1;
			case 2: repeat = infor_add_Website();break;//直锟斤拷锟剿筹拷锟斤拷锟斤拷		 
		}	
	}//repeat 循锟斤拷锟斤拷锟斤拷
}

//*************************************网页信息添加*************************************

int infor_add_Website()//锟斤拷锟斤拷锟揭筹拷锟较?
{
	struct Website website;
	char choice[16]={'\0'};//锟斤拷锟斤拷没锟斤拷锟窖★拷锟?
	FILE* information;//锟斤拷锟叫筹拷锟轿碉拷锟斤拷息
	
	//锟斤拷锟斤拷锟斤拷息 
		//锟斤拷址 
	printf("锟斤拷息锟斤拷锟?锟斤拷页锟斤拷息\n");
	printf("\n锟斤拷锟斤拷锟斤拷锟斤拷站锟斤拷锟斤拷址\n");
	fflush(stdin);
	scanf("%s",website.web);
		//锟斤拷锟斤拷
	printf("锟矫的ｏ拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟秸撅拷锟较拷锟斤拷锟斤拷锟絓n");
	fflush(stdin);
 	scanf("%s",website.describe);
		//锟截硷拷锟斤拷
	printf("锟矫的ｏ拷锟斤拷锟斤拷锟斤拷锟斤拷锟侥革拷锟斤拷锟皆硷拷锟斤拷锟斤拷锟斤拷锟斤拷息锟侥关硷拷锟斤拷\n");
	fflush(stdin);
	scanf("%s",website.find1);
	fflush(stdin);
	scanf("%s",website.find2);
	fflush(stdin);
	scanf("%s",website.find3);
	fflush(stdin);
	scanf("%s",website.find4);
	//锟剿讹拷锟斤拷息
	printf("\n锟斤拷锟斤拷锟斤拷锟斤拷拥锟斤拷锟较⑽拷锟絓n"
		 "锟斤拷址锟斤拷%s\n锟斤拷锟斤拷锟斤拷%s\n锟截硷拷锟斤拷1锟斤拷%s\n"
		 "锟截硷拷锟斤拷2锟斤拷%s\n锟截硷拷锟斤拷3锟斤拷%s\n锟截硷拷锟斤拷4锟斤拷%s\n"
		 ,website.web,website.describe,website.find1,
		 website.find2,website.find3,website.find4);
	printf("\n锟斤拷锟角凤拷要锟斤拷锟诫本锟斤拷锟斤拷息锟斤拷1-锟角ｏ拷0-锟斤拷锟斤拷\n");
	while(1){
		fflush(stdin);
		scanf("%s",choice);
		if(judge_num(choice)!=0)
			continue;
		if(atoi(choice)!=1&&atoi(choice)!=0)
			continue;
	 	break;
	}
	switch(atoi(choice))
	{
		case 1: 
			information=fopen("information.txt","a+");
			fprintf(information,"1  %s  %s  %s  %s  %s  %s"
			"  -  -  -  -  -  -  -  -  -  -  -  -  -  -\n",
				website.web,website.describe,website.find1,website.find2,
				website.find3,website.find4);
			fclose(information);
			printf("锟斤拷锟窖成癸拷锟斤拷锟絓n锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟絓n");
			fflush(stdin);
			getchar();
			return 1;
		case 0: 
			printf("锟斤拷锟斤拷取锟斤拷锟斤拷锟絓n锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟絓n");
			fflush(stdin);
			getchar();
			return 1;		 
	}	
}


//*************************************信息查找（二级选择）**************************************

int information_check()
{
	char choice[16]={'\0'};//锟斤拷锟斤拷没锟斤拷锟窖★拷锟?
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//锟斤拷锟斤拷 
			printf("\n直锟斤拷锟剿筹拷锟斤拷锟斤拷  锟斤拷锟斤拷锟斤拷0\n");
			printf("锟斤拷锟斤拷锟较硷拷锟斤拷锟斤拷  锟斤拷锟斤拷锟斤拷1\n");
			printf("锟介看锟斤拷锟斤拷锟斤拷息  锟斤拷锟斤拷锟斤拷2\n");
			printf("锟介看锟斤拷页锟斤拷息  锟斤拷锟斤拷锟斤拷3\n");
			fflush(stdin);
			scanf("%s",choice);
			if(judge_num(choice)!=0)
				continue;
			if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2&&atoi(choice)!=3)
				continue;
		 	break;
		}
		switch(atoi(choice))
		{
			case 0: return 0;
			case 1: return 1;
			case 2: repeat = infor_check_all();break;//锟介看锟斤拷锟斤拷锟斤拷息
		 	case 3: repeat = infor_check_web();break;//锟介看锟斤拷页锟斤拷息	 
		}	
	}//repeat 循锟斤拷锟斤拷锟斤拷

}

//*************************************网页信息查找**************************************

int infor_check_all()//锟斤拷询锟斤拷锟斤拷锟斤拷息 
{
	struct Website website;
	FILE* information;//锟斤拷锟叫筹拷锟轿碉拷锟斤拷息
	char choice[16]={'\0'};
	char vacuum[16]={'\0'};
	
	printf("锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟絓n");
	fflush(stdin);
	scanf("%s",choice);
	information=fopen("information.txt","r");
	while(fscanf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&website.type,website.web,website.describe,website.find1,website.find2,
	website.find3,website.find4,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,
	vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum)!=EOF)
	{
		printf("\n锟斤拷锟斤拷锟斤拷%s\n锟斤拷址锟斤拷%s\n",website.describe,website.web);	
	}
	printf("\n锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟絓n");
	fflush(stdin);
	getchar();
	return 1;
} 

int infor_check_web()//锟斤拷询锟斤拷页锟斤拷息
{
	struct Website website;
	FILE* information;//锟斤拷锟叫筹拷锟轿碉拷锟斤拷息
	char choice[16]={'\0'};
	char vacuum[16]={'\0'};
	
	printf("锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟絓n");
	fflush(stdin);
	scanf("%s",choice);
	information=fopen("information.txt","r");
	while(fscanf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&website.type,website.web,website.describe,website.find1,website.find2,
	website.find3,website.find4,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,
	vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum)!=EOF)
	{
		if(website.type == 1&&(strcmp(choice,website.find1)==0||strcmp(choice,website.find2)==0
		||strcmp(choice,website.find3)==0||strcmp(choice,website.find4)==0))
		{
			printf("\n锟斤拷锟斤拷锟斤拷%s\n锟斤拷址锟斤拷%s\n",website.describe,website.web);
		}	
	}
	printf("\n锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟絓n");
	fflush(stdin);
	getchar();
	return 1;
}

//*************************************模板管理（二级选择）**************************************

//.....................................模板管理主函数（第三层级）............................................ 

int club_control()
{
	char choice[16]={'\0'};//获得用户选择 
	int repeat = 1;
	
	while(repeat)
	{
		//获得正确用户输入
		while(1){ 
			system("cls");//清屏 
			printf("\n直接离开程序  请输入0\n");
			printf("返回上一界面  请输入1\n");
			printf("进行模板创建  请输入2\n");
			printf("进行模板查看  请输入3\n");
			printf("进行模板修改  请输入4\n"); 
			printf("进行模板备份  请输入5\n");
			fflush(stdin);
			scanf("%s",choice);
			if(judge_num(choice)!=0)
				continue;
			if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
			&&atoi(choice)!=3&&atoi(choice)!=4&&atoi(choice)!=5)
				continue;
		 	break;
		}
		//提供对应选择 
		switch(atoi(choice))
		{
			case 0: return 0;
			case 1: return 1;
			case 2: repeat = club_control_creat(); break;//进行模板创建 
		 	case 3: repeat = club_control_check(); 
				         fflush(stdin);getchar();break;//进行模板查看
			case 4: repeat = club_control_change();break;//进行模板修改
			case 5: repeat = club_control_copy();  break;//进行模板备份 
		}	
	}//repeat 循环结束
}

//.................................模板管理-创建模板（第三层级）............................................ 

int club_control_creat()//创建模板 
{
	struct club creat;
	char choice[32];
	char club_name[32];
	int number = 0,i = 0,valid = 1;
	FILE* Club;
	
	printf("您已进入模板创建功能！\n");
	printf("任意地方输入 EOF 可以终止此次添加行为\n");	
	while(valid){
		number = 0;
		printf("\n请您输入添加模板的名称：");
		fflush(stdin);
		scanf("%s",choice);
		if(strcmp(choice,"NOTHING") == 0) 
		{
			printf("名称不可以是NOTHING！请您重新输入\n");
			continue;
		}
		if(strcmp(choice,"EOF") == 0) return 1; 
		Club=fopen("club.txt","r");
		while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
		"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
		&creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
		,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
		,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
		,creat.name[11],creat.name[12],creat.name[13]
		,creat.name[14],creat.name[15],creat.name[16]
		,creat.name[17],creat.name[18],creat.name[19])!=EOF)
		{
			if(strcmp(choice,creat.class_name)==0){
				printf("该名字已经存在，请您再次输入\n");
				valid = 1;
				break;
			}	
			if(number <= creat.type){
				number = creat.type + 1;	
			}	
				valid = 0;
		}
	}
	fclose(Club);
	strcpy(club_name,choice);//模板名为 club_name!
	
	printf("新模板的名称是 %s\n",club_name);
	printf("请您依次输入该模板的每一个项的名称（不超过20个）\n输入STOP停止继续添加\n");
	//锟斤拷锟斤拷锟斤拷锟斤拷值锟斤拷锟斤拷锟?
	for(i=0;i<20;i++)
	{
		while(1)
		{
			printf("请输入 %s 中的第 %d 项：",club_name,i+1);
			fflush(stdin);
			scanf("%s",creat.name[i]);
			if(strcmp(creat.name[i],"NOTHING") == 0)
			{
				printf("名称不可以是NOTHING！请您重新输入\n");
				continue;
			}
			break;
		}
			//锟斤拷锟斤拷崭锟阶拷锟斤拷锟斤拷锟?
		if(strcmp(creat.name[i],"EOF") == 0) return 1;
		if(strcmp(creat.name[i],"STOP") == 0) break;
	}
	for(i;i<20;i++)
	{
		strcpy(creat.name[i],"NOTHING");
	}
	
	//询锟斤拷锟角凤拷锟斤拷锟?
	printf("\n下面是您本次添加的模板\n");
	for(i=0;i<20;i++)
	{
		if(strcmp(creat.name[i],"NOTHING")!=0)
		printf(" 第 %d 项：%s\n",i+1,creat.name[i]);
	}
	printf("您是否要添加？\n是 输入 1,不是 输入 其他任意字符\n");
	fflush(stdin);
	scanf("%s",choice);
	if(strcmp(choice,"1")==0){
		Club=fopen("club.txt","a+");
		fprintf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
		"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n",
		number,club_name,creat.name[0],creat.name[1],creat.name[2]
		,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
		,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
		,creat.name[11],creat.name[12],creat.name[13]
		,creat.name[14],creat.name[15],creat.name[16]
		,creat.name[17],creat.name[18],creat.name[19]
		,creat.name[20]);
		fclose(Club);
		printf("已成功添加新模板（按任意键继续）\n");
	}else{
		printf("已成功取消添加（按任意键继续）\n");
	}
	fflush(stdin);
	getchar();
	return 1;
}

//.................................模板管理-查看模板（第三层级）............................................ 

int club_control_check()//查看模板
{
	FILE * Club;
	struct club creat;
	int i = 0;
	
	Club=fopen("club.txt","a+");
	while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
	,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
	,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
	,creat.name[11],creat.name[12],creat.name[13]
	,creat.name[14],creat.name[15],creat.name[16]
	,creat.name[17],creat.name[18],creat.name[19])!=EOF)
	{
		printf("模板名称：%s\n",creat.class_name);
		for(i=0;i<20;i++)
		{
			if(strcmp(creat.name[i],"NOTHING")!=0)
			printf("  第 %d 项：%s\n",i+1,creat.name[i]);
		}
		printf("\n");
	}
	fclose(Club);
	return 1;
}

//.................................模板管理-更改模板（第三层级）............................................ 

int club_control_change()//模板更改 
{
	char change_club[32];
	FILE * Club;
	FILE * draft;
	int success = 0;
	
	printf("下面是已有模板\n");
	club_control_check();
	while(1)
	{
		printf("请输入需要更改的模板(输入BACK返回):");
		fflush(stdin);
		scanf("%s",change_club);
		if(strcmp(change_club,"BACK") == 0) 
			return 1;
		if(club_control_change_ClubValid(change_club))
			continue;
		break;
	}
	printf("现在还不支持修改模板 谢谢理解！\n");
	fflush(stdin);
	getchar();
	//printf("下面请选择更改类型/n");
	//scanf("%s");
	//锟斤拷锟斤拷 
	/* 
	Club=fopen("club.txt","r");
	while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
	,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
	,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
	,creat.name[11],creat.name[12],creat.name[13]
	,creat.name[14],creat.name[15],creat.name[16]
	,creat.name[17],creat.name[18],creat.name[19])!=EOF)
	{
		printf("锟斤拷目锟斤拷锟斤拷%s\n",creat.class_name);
		for(i=0;i<20;i++)
		{
			if(strcmp(creat.name[i],"NOTHING")!=0)
			printf("  锟斤拷 %d 锟筋：%s\n",i+1,creat.name[i]);
		}
		printf("\n");
	}
	fclose(Club);
	*/	
	return 1;
}

int club_control_change_ClubValid(char change_club[])////用户输入的名称是否已创建
{
	FILE* Club;
	struct club creat;
	int success = 0;
	int i = 0;
	
	Club=fopen("club.txt","r");
	while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
	,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
	,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
	,creat.name[11],creat.name[12],creat.name[13]
	,creat.name[14],creat.name[15],creat.name[16]
	,creat.name[17],creat.name[18],creat.name[19])!=EOF)
	{
		if(strcmp(creat.class_name,change_club) == 0)
		{
			success += 1;
		}
	}
	if(success == 0)
	{
		printf(" 请您输入已有的模板名称！\n");
		return 1;
	}
	return 0;
}

//.................................模板管理-拷贝模板（第三层级）............................................ 

int club_control_copy()//拷贝模板 
{
	FILE * Club;
	FILE * Copy;
	struct club creat; 
	char choice[32];
	char choice2[32];

	//获得正确用户输入
	while(1){ 
		system("cls");//清屏
		printf("\n这里是备份文件模块\n"); 
		printf("返回至上一界面  请输入0\n");
		printf("备份到一号文件  请输入1\n");
		printf("备份到二号文件  请输入2\n");
		printf("备份到三号文件  请输入3\n"); 
		printf("备份到四号文件  请输入4\n");
		fflush(stdin);
		scanf("%s",choice);
		if(judge_num(choice)!=0)
			continue;
		if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
		&&atoi(choice)!=3&&atoi(choice)!=4)
			continue;
	 	break;
	}
	if(atoi(choice) == 0)
		return 1;
	//再次确认是否备份
	printf("备份会清空对应文件上次的信息！\n"); 
	printf("您 确 认 要 备 份 吗 ？\n");
	printf("是 输入 'YES',不是 输入其他字符 \n");
	fflush(stdin);
	scanf("%s",choice2);
	if(strcmp(choice2,"YES") != 0)
		return 1;
	//提供对应选择 
	switch(atoi(choice))
	{
		case 1: Copy = fopen("club_copy1.txt","w");
		case 2: Copy = fopen("club_copy2.txt","w");
		case 3: Copy = fopen("club_copy3.txt","w");
		case 4: Copy = fopen("club_copy4.txt","w");
	}	
	Club = fopen("club.txt","r");
	while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
	,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
	,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
	,creat.name[11],creat.name[12],creat.name[13]
	,creat.name[14],creat.name[15],creat.name[16]
	,creat.name[17],creat.name[18],creat.name[19])!=EOF)
	{
		fprintf(Copy,"%d  %s  %s  %s  %s  %s  %s  %s"
		"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n",
		creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
		,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
		,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
		,creat.name[11],creat.name[12],creat.name[13]
		,creat.name[14],creat.name[15],creat.name[16]
		,creat.name[17],creat.name[18],creat.name[19]);
	}
	fclose(Club);
	fclose(Copy);
	printf("您已备份成功！(按任意键继续)\n");
	fflush(stdin);
	getchar();
	return 1;
}
 
//*************************************工具函数**************************************

int judge_num(char num[])//判断用户输入是否为整数 
{
	int valid = 0,i;
	for(i = 0;i<strlen(num);i++)
	{
		if(isdigit(num[i])) continue;
		else
		{
			printf("请您输入整数\n按任意键继续");
			fflush(stdin);
			getchar();
			valid = 1;
			break;
		}
	}
	return valid; 
} 

int judge_kongge(char num[])//判断用户输入是否有空格
{
	int valid = 0,i;
	for(i = 0;i<strlen(num);i++)
	{
		if(int(num[i]) == 32)
		{
			printf("请您不要输入空格\n按任意键继续");
			fflush(stdin);
			getchar();
			valid = 1;
			break;
		}
	}
	return valid;
}
 