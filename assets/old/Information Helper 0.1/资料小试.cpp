#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <string>
#include <windows.h>
#include <conio.h>

// ���� 1 ��վ��Ϣ 
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
int information_check();//��Ϣ��ѯ 
	int infor_check_all();//��ѯ������Ϣ 
	int infor_check_web();//��ѯ��ҳ��Ϣ  
int information_add();//��Ϣ���� 
	int infor_add_Website();//�����ҳ��Ϣ 

//���ߺ��� 
int judge_num(char num[]);//�ж��û������Ƿ�Ϊ����
int judge_kongge(char[]);//�ж��û������Ƿ��пո�
//*************************************��Ҫ����**************************************
int main()
{
	char choice[16]={'\0'};//����û���ѡ�� 
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//���� 
			printf("\nֱ���˳�����  ������0\n");
			printf("������Ϣ����  ������1\n");
			printf("������Ϣ��ѯ  ������2\n");
			
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
			case 1: repeat = information_add();break;//����Ա��½
			case 2: repeat = information_check();break;//�û���½
			case 0: repeat = 0;break;//ֱ���˳�����		 
		}	
	}//repeat ѭ������ 
	return 0;
}

int information_add()//��Ϣ��� 
{
	char choice[16]={'\0'};//����û���ѡ�� 
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//���� 
			printf("\nֱ���˳�����  ������0\n");
			printf("�����ϼ�����  ������1\n");
			printf("�����ҳ��Ϣ  ������2\n");
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
			case 2: repeat = infor_add_Website();break;//ֱ���˳�����		 
		}	
	}//repeat ѭ������
}

int information_check()
{
	char choice[16]={'\0'};//����û���ѡ�� 
	int repeat = 1;
	while(repeat){
		while(1){
			system("cls");//���� 
			printf("\nֱ���˳�����  ������0\n");
			printf("�����ϼ�����  ������1\n");
			printf("�鿴������Ϣ  ������2\n");
			printf("�鿴��ҳ��Ϣ  ������3\n");
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
			case 2: repeat = infor_check_all();break;//�鿴������Ϣ
		 	case 3: repeat = infor_check_web();break;//�鿴��ҳ��Ϣ	 
		}	
	}//repeat ѭ������

}

//*************************************��Ϣ���**************************************

int infor_add_Website()//�����ҳ��Ϣ
{
	struct Website website;
	char choice[16]={'\0'};//����û���ѡ�� 
	FILE* information;//���г��ε���Ϣ
	
	//������Ϣ 
		//��ַ 
	printf("��Ϣ���-��ҳ��Ϣ\n");
	printf("\n��������վ����ַ\n");
	fflush(stdin);
	scanf("%s",website.web);
		//����
	printf("�õģ������������վ��Ϣ������\n");
	fflush(stdin);
 	scanf("%s",website.describe);
		//�ؼ���
	printf("�õģ����������ĸ����Լ���������Ϣ�Ĺؼ���\n");
	fflush(stdin);
	scanf("%s",website.find1);
	fflush(stdin);
	scanf("%s",website.find2);
	fflush(stdin);
	scanf("%s",website.find3);
	fflush(stdin);
	scanf("%s",website.find4);
	//�˶���Ϣ
	printf("\n��������ӵ���ϢΪ��\n"
		 "��ַ��%s\n������%s\n�ؼ���1��%s\n"
		 "�ؼ���2��%s\n�ؼ���3��%s\n�ؼ���4��%s\n"
		 ,website.web,website.describe,website.find1,
		 website.find2,website.find3,website.find4);
	printf("\n���Ƿ�Ҫ���뱾����Ϣ��1-�ǣ�0-����\n");
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
			printf("���ѳɹ����\n�����������\n");
			fflush(stdin);
			getchar();
			return 1;
		case 0: 
			printf("����ȡ�����\n�����������\n");
			fflush(stdin);
			getchar();
			return 1;		 
	}	
}

//*************************************��Ϣ��ѯ**************************************

int infor_check_all()//��ѯ������Ϣ 
{
	struct Website website;
	FILE* information;//���г��ε���Ϣ
	char choice[16]={'\0'};
	char vacuum[16]={'\0'};
	
	printf("�����������\n");
	fflush(stdin);
	scanf("%s",choice);
	information=fopen("information.txt","r");
	while(fscanf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
	"  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	&website.type,website.web,website.describe,website.find1,website.find2,
	website.find3,website.find4,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,
	vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum,vacuum)!=EOF)
	{
		printf("\n������%s\n��ַ��%s\n",website.describe,website.web);	
	}
	printf("\n�����������\n");
	fflush(stdin);
	getchar();
	return 1;
} 

int infor_check_web()//��ѯ��ҳ��Ϣ
{
	struct Website website;
	FILE* information;//���г��ε���Ϣ
	char choice[16]={'\0'};
	char vacuum[16]={'\0'};
	
	printf("�����������\n");
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
			printf("\n������%s\n��ַ��%s\n",website.describe,website.web);
		}	
	}
	printf("\n�����������\n");
	fflush(stdin);
	getchar();
	return 1;
}

//*************************************���ߺ���**************************************
int judge_num(char num[])//�ж��Ƿ�Ϊ���� 
{
	int valid = 0,i;
	for(i = 0;i<strlen(num);i++)
	{
		if(isdigit(num[i])) continue;
		else
		{
			printf("���������֣�\n�����������");
			fflush(stdin);
			getchar();
			valid = 1;
			break;
		}
	}
	return valid;//����ֵΪ0������������ȷ 
} 

int judge_kongge(char num[])//�ж��Ƿ��пո� 
{
	int valid = 0,i;
	for(i = 0;i<strlen(num);i++)
	{
		if(int(num[i]) == 32)
		{
			printf("�벻Ҫ����ո�\n");
			getchar();
			getchar();
			valid = 1;
			break;
		}
	}
	return valid;//����ֵΪ0������������ȷ 
}
