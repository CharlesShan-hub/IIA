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
	
	printf("���ѽ�������Զ���������\n");
	
	printf("��������������ƣ�");
	scanf("%s",creat.class_name);
		//��������ж� 
		//�Զ����ɸ�������� 
	printf("������� %s �еĵ�һ�",creat.class_name);
	scanf("%s",item1);
	
	
	
	return 0;
}
