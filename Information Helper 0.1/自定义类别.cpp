# include <stdio.h>

int creat_club();
struct club
{
	int type;
	char class_name[32];
	char item[20][32];	
	char name[20][32];
	
};

int main()
{
	
	creat_club();
	
	
	
	
	return 0;
}

int creat_club()
{
	struct club creat;
	
	printf("您已进入添加自定义类别界面\n");
	
	printf("请输入该类别的名称：");
	scanf("%s",creat.class_name);
		//加入查重判断 
		//自动生成该类别的序号 
	printf("请输入该 %s 中的第一项：",creat.class_name);
	scanf("%s",item1);
	
	
	
	return 0;
}
