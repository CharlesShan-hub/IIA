#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <string>
#include <windows.h>
#include <conio.h>

// 类型 1 网站信息 
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

//
int information_check();//信息查询 
	int infor_check_all();//查询所有信息 
	int infor_check_web();//查询网页信息  
int information_add();//信息增加 
	int infor_add_Website();//添加网页信息 

//工具函数 
int judge_num(char num[]);//判断用户输入是否为整数
int judge_kongge(char[]);//判断用户输入是否有空格
//*************************************主要函数**************************************
int main()
{
	char choice[16]={'\0'};//获得用户的选择 
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//清屏 
			printf("\n直接退出程序  请输入0\n");
			printf("进入信息输入  请输入1\n");
			printf("进入信息查询  请输入2\n");
			
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
			case 1: repeat = information_add();break;//管理员登陆
			case 2: repeat = information_check();break;//用户登陆
			case 0: repeat = 0;break;//直接退出程序		 
		}	
	}//repeat 循环结束 
	return 0;
}

int information_add()//信息添加 
{
	char choice[16]={'\0'};//获得用户的选择 
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//清屏 
			printf("\n直接退出程序  请输入0\n");
			printf("返回上级程序  请输入1\n");
			printf("添加网页信息  请输入2\n");
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
			case 2: repeat = infor_add_Website();break;//直接退出程序		 
		}	
	}//repeat 循环结束
}

int information_check()
{
	char choice[16]={'\0'};//获得用户的选择 
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//清屏 
			printf("\n直接退出程序  请输入0\n");
			printf("返回上级程序  请输入1\n");
			printf("查看所有信息  请输入2\n");
			printf("查看网页信息  请输入3\n");
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
			case 2: repeat = infor_check_all();break;//查看所有信息
		 	case 3: repeat = infor_check_web();break;//查看网页信息	 
		}	
	}//repeat 循环结束

}

//*************************************信息添加**************************************

int infor_add_Website()//添加网页信息
{
	struct Website website;
	char choice[16]={'\0'};//获得用户的选择 
	FILE* information;//所有场次的信息
	
	//收入信息 
		//网址 
	printf("信息添加-网页信息\n");
	printf("\n请输入网站的网址\n");
	fflush(stdin);
	scanf("%s",website.web);
		//描述
	printf("好的！现在输入对网站信息的描述\n");
	fflush(stdin);
 	scanf("%s",website.describe);
		//关键词
	printf("好的！现在输入四个可以检索除本信息的关键词\n");
	fflush(stdin);
	scanf("%s",website.find1);
	fflush(stdin);
	scanf("%s",website.find2);
	fflush(stdin);
	scanf("%s",website.find3);
	fflush(stdin);
	scanf("%s",website.find4);
	//核对信息
	printf("\n您本次添加的信息为：\n"
		 "网址：%s\n描述：%s\n关键词1：%s\n"
		 "关键词2：%s\n关键词3：%s\n关键词4：%s\n"
		 ,website.web,website.describe,website.find1,
		 website.find2,website.find3,website.find4);
	printf("\n您是否要输入本次信息？1-是，0-不是\n");
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
			printf("您已成功添加\n按任意键继续\n");
			fflush(stdin);
			getchar();
			return 1;
		case 0: 
			printf("您已取消添加\n按任意键继续\n");
			fflush(stdin);
			getchar();
			return 1;		 
	}	
}

//*************************************信息查询**************************************

int infor_check_all()//查询所有信息 
{
	struct Website website;
	FILE* information;//所有场次的信息
	char choice[16]={'\0'};
	char vacuum[16]={'\0'};
	
	printf("请输入检索词\n");
	fflush(stdin);
	scanf("%s",choice);
	information=fopen("information.txt","r");
	while(fscanf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&website.type,website.web,website.describe,website.find1,website.find2,
	website.find3,website.find4,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,
	vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum)!=EOF)
	{
		printf("\n描述：%s\n网址：%s\n",website.describe,website.web);	
	}
	printf("\n按任意键继续\n");
	fflush(stdin);
	getchar();
	return 1;
} 

int infor_check_web()//查询网页信息
{
	struct Website website;
	FILE* information;//所有场次的信息
	char choice[16]={'\0'};
	char vacuum[16]={'\0'};
	
	printf("请输入检索词\n");
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
			printf("\n描述：%s\n网址：%s\n",website.describe,website.web);
		}	
	}
	printf("\n按任意键继续\n");
	fflush(stdin);
	getchar();
	return 1;
}

//*************************************工具函数**************************************
int judge_num(char num[])//判断是否为数字 
{
	int valid = 0,i;
	for(i = 0;i<strlen(num);i++)
	{
		if(isdigit(num[i])) continue;
		else
		{
			printf("请输入数字！\n按任意键继续");
			fflush(stdin);
			getchar();
			valid = 1;
			break;
		}
	}
	return valid;//返回值为0，代表输入正确 
} 

int judge_kongge(char num[])//判断是否有空格 
{
	int valid = 0,i;
	for(i = 0;i<strlen(num);i++)
	{
		if(int(num[i]) == 32)
		{
			printf("请不要输入空格！\n");
			getchar();
			getchar();
			valid = 1;
			break;
		}
	}
	return valid;//返回值为0，代表输入正确 
}
