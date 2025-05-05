#include "define.h"
//********************************Main Function(First Level)**************************************
int main()
{
    char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    
    //Setting of display
	int screen_color;
	int letter_color; 
	FILE* setting;
	setting=fopen("setting.txt","r"); 
	fscanf(setting,"%d  %d",&screen_color,&letter_color);
	setting_display_slcolor(letter_color,screen_color);
    
    while(repeat){
        //acquire user's choice
        while(1){
            system("cls");//clear screen
            printf("\n INFORMATION ADMINISTRATION SYSTEM\n");
			printf("\n Leave Immidiately           Please Input 0\n");
            printf(" Related To Information      Please Input 1\n");
            printf(" Related To Tempalte         Please Input 2\n");
            printf(" Setting                     Please Input 3\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)!=0&&atoi(choice)!=1
			&&atoi(choice)!=2&&atoi(choice)!=3)
                continue;
            break;
        }
        //provide function responses to choice
        switch(atoi(choice))
        {
            case 1: repeat = information_control();break;//add information
            case 2: repeat = club_control();break;//template
            case 3: repeat = setting_control(); break;//setting
            case 0: repeat = 0;break;//exit
        }
    }//repeat over
    return 0;
}

int information_control()//information Main Function
{
	char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
	while(repeat)
    {
        //acquire user's choice
        while(1){
            system("cls");//clear screen
            printf("\n Information module\n");
            printf("\n Leave  Immidiately    Please Input 0\n");
            printf(" Back To Last Level    Please Input 1\n");
            printf(" Add    Information    Please Input 2\n");
            printf(" Check  Information    Please Input 3\n");
            printf(" Cover  Information    Please Input 4\n");
            printf(" Copy   Information    Please Input 5\n");
            printf(" Check    Copies       Please Input 6\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
               &&atoi(choice)!=3&&atoi(choice)!=4&&atoi(choice)!=5&&atoi(choice)!=6)
                continue;
            break;
        }
        //provide function responses to choice
        switch(atoi(choice))
        {
            case 0: return 0;
            case 1: return 1;
            case 2: repeat = information_add();        break;
            case 3: repeat = information_check();      break;
            case 4: repeat = information_copy_cover(); break;
            case 5: repeat = information_copy_copy();  break;
            case 6: repeat = information_copy_check(); break;
        }
    }//repeat over
}

int club_control()//Tamplate Main Function
{
    char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    
    while(repeat)
    {
        //acquire user's choice
        while(1){
            system("cls");//clear screen
            printf("\n Tempaltes module\n");
            printf("\n Leave  Immidiately    Please Input 0\n");
            printf(" Back To Last Level    Please Input 1\n");
            printf(" Creat    Tempaltes    Please Input 2\n");
            printf(" Check    Templates    Please Input 3\n");
            printf(" Change   Templates    Please Input 4\n");
            printf(" Copy     Templates    Please Input 5\n");
            printf(" Check    Copies       Please Input 6\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
               &&atoi(choice)!=3&&atoi(choice)!=4&&atoi(choice)!=5&&atoi(choice)!=6)
                continue;
            break;
        }
        //provide function responses to choice
        switch(atoi(choice))
        {
            case 0: return 0;
            case 1: return 1;
            case 2: repeat = club_control_creat();     break;
            case 3: repeat = club_control_check();
                fflush(stdin);getchar();    break;
            case 4: repeat = club_control_change();    break;
            case 5: repeat = club_control_copy();      break;
            case 6: repeat = club_control_copy_check();break;
        }
    }//repeat over
}

int setting_control()//Setting Main Function
{
	char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    
    while(repeat)
    {
        //acquire user's choice
        while(1){
            system("cls");//clear screen
            printf("\n Setting module\n");
            printf("\n Leave  Immidiately    Please Input 0\n");
            printf(" Back To Last Level    Please Input 1\n");
            printf(" Display               Please Input 2\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2)
                continue;
            break;
        }
        //provide function responses to choice
        switch(atoi(choice))
        {
            case 0: return 0;
            case 1: return 1;
            case 2: repeat = setting_display();     break;//这个当个模板吧 
        }
    }//repeat over
} 

//*************************************Tools**************************************

int judge_num(char num[])//judge the input is interger or not
{
    int valid = 0,i;
    for(i = 0;i < strlen(num);i++)
    {
        if(isdigit(num[i])) continue;
        else
        {
            printf(" Please input an integer!\n (Input anything to continue)");
            fflush(stdin);
            getchar();
            valid = 1;
            break;
        }
    }
    return valid;
}

int judge_kongge(char num[])//jugdge the input has blank or not
{
    int valid = 0,i;
    for(i = 0;i<strlen(num);i++)
    {
        if(int(num[i])==32)
        {
            printf(" Don't input blank!\n (Input anything to continue)");
            fflush(stdin);
            getchar();
            valid = 1;
            break;
        }
    }
    return valid;
}

