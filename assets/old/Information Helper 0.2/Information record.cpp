#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <string>
#include <windows.h>
#include <conio.h>

//template for information
struct club
{
    int type;
    char class_name[32];
    char item[20][128];
    char name[20][32];
};

//Website template
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

//function
int information_check(void);//check information
int information_add(void);//add information
int information_copy(void);//main copy information function
int information_copy_copy(void);//copy information
int information_copy_cover(void);//cover information by copies
int information_copy_check(void);//check information copies
int club_control(void); //template
int club_control_creat(void);//creat new tempalte
int club_control_check(void);//cheak templates already have
int club_control_change(void);//alter templates or templates' items
int club_control_change_ClubValid(char[]);//input validation
int club_control_copy(void);//copy recent tempalte
int club_control_copy_check(void);//check copies

//tool
int judge_num(char num[]);//judge the input is interger or not
int judge_kongge(char[]);//jugdge the input has blank or not

//********************************Main Function(First Level)**************************************
int main()
{
    char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    
    while(repeat){
        //acquire user's choice
        while(1){
            system("cls");//clear screen
            printf("\n Leave Immidiately    Please Input 0\n");
            printf(" Add Information      Please Input 1\n");
            printf(" Check Information    Please Input 2\n");
            printf(" Copy  Information    Please Input 3\n");
            printf(" Related To Tempalte  Please Input 4\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)!=0&&atoi(choice)!=1
		&&atoi(choice)!=2&&atoi(choice)!=3&&atoi(choice)!=4)
                continue;
            break;
        }
        //provide function responses to choice
        switch(atoi(choice))
        {
            case 1: repeat = information_add();break;//add information
            case 2: repeat = information_check();break;//check information
            case 3: repeat = information_copy(); break;//copy information
            case 4: repeat = club_control();break;//template
            case 0: repeat = 0;break;//exit
        }
    }//repeat over
    return 0;
}

//*******************************Add Information(Second Level)**************************************

int information_add()//add information
{
    char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    struct club creat;
    FILE* Club;
    FILE* information;
    int i = 1;//Loop varibles
    
    Club=fopen("club.txt","r");
    //Get Users' choice (type of imformation)
    while(1)
    {
        system("cls");//clear screen
        printf("\n Input 0 : Back to last level\n");
        while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
                     "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
                     &creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
                     ,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
                     ,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
                     ,creat.name[11],creat.name[12],creat.name[13]
                     ,creat.name[14],creat.name[15],creat.name[16]
                     ,creat.name[17],creat.name[18],creat.name[19])!=EOF)
        {
            printf(" Input %-2d: Type of %s\n",creat.type,creat.class_name);
        }
        fflush(stdin);
        scanf("%s",choice);
        if(judge_num(choice)!=0)
            continue;
        if(atoi(choice)>creat.type)
            continue;
        break;
    }
    
    //Record responding structure of the tamplate
    if(atoi(choice) == 0) return 1;
    rewind(Club);
    while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
                 "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
                 &creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
                 ,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
                 ,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
                 ,creat.name[11],creat.name[12],creat.name[13]
                 ,creat.name[14],creat.name[15],creat.name[16]
                 ,creat.name[17],creat.name[18],creat.name[19])!=EOF)
    {
        if(atoi(choice) == creat.type) break;
    }
    fclose(Club);
    
    //Show the structure of tamplate
    printf(" The Structure of Tampale %s is\n",creat.class_name);
    for(i=0;i<20;i++)
    {
        if(strcmp(creat.name[i],"NOTHING") != 0)
            printf("  %-2d : %s\n",i+1,creat.name[i]);
    }
    printf("\n");
    
    //Get items in the tamplate
    for(i=0;i<20;i++)
    {
        if(strcmp(creat.name[i],"NOTHING") == 0)
        {
            strcpy(creat.item[i],creat.name[i]);
        }else{
            printf("  item %-2d  %-10s : ",i+1,creat.name[i]);
            while(1)
            {
                fflush(stdin);
                scanf("%s",creat.item[i]);//later! add! blank! solve!
                if(strcmp(creat.item[i],"NOTHING") == 0)
                {
                    printf(" Your input cannot be NOTHING, Please input again!\n");
                    continue;
                }
                break;
            }
        }
    }
    
    //Make sure to add
    printf("\n Your imformation is:\n");
    for(i=0;i<20;i++)
    {
        if(strcmp(creat.name[i],"NOTHING") == 0)
            break;
        printf("  item %-2d  %-10s : %s\n",i+1,creat.name[i],creat.item[i]);
    }
    printf(" Do you really want to add ?\n");
    printf(" Input YES to add, others to leave\n");
    fflush(stdin);
    scanf("%s",choice);
    
    //Add information
    if(strcmp(choice,"YES") == 0)
    {
        information=fopen("information.txt","a+");
        fprintf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
                "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n"
                ,creat.type,creat.class_name,creat.item[0],creat.item[1],creat.item[2]
                ,creat.item[3],creat.item[4],creat.item[5],creat.item[6]
                ,creat.item[7],creat.item[8],creat.item[9],creat.item[10]
                ,creat.item[11],creat.item[12],creat.item[13]
                ,creat.item[14],creat.item[15],creat.item[16]
                ,creat.item[17],creat.item[18],creat.item[19]);
        fclose(information);
        printf(" You have successfully added the information !\n");
    }else{
        printf(" You have cancles the adding !\n");
    }
    fflush(stdin);
    getchar();
    return 1;
}

//*********************************Check Information(Second Level)**********************************

int information_check()//Check Information
{
    
    char choice[16]={'\0'};//record user's choice
    int all = 0;//number to search all the information
    int truth = 0;//whether to printf
    int type = 0;
    struct club creat;
    FILE* Club;
    FILE* information;
    int i = 1;//Loop varibles
    char key[32]={'\0'};//record user's key word to search
    
    //Get Users' choice (type of imformation)
    Club=fopen("club.txt","r");
    while(1){
        system("cls");//clear screen
        printf("\n Input 0 : Back to last level\n");
        while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
                     "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
                     &creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
                     ,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
                     ,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
                     ,creat.name[11],creat.name[12],creat.name[13]
                     ,creat.name[14],creat.name[15],creat.name[16]
                     ,creat.name[17],creat.name[18],creat.name[19])!=EOF)
        {
            printf(" Input %-2d: Type of %s\n",creat.type,creat.class_name);
        }
        printf(" Input %-2d: In all information\n",creat.type+1);
        fflush(stdin);
        scanf("%s",choice);
        if(judge_num(choice)!=0){
            rewind(Club);
            continue;
        }
        if(atoi(choice)>(creat.type+1)){
            rewind(Club);
            continue;
        }
        break;
    }
    all = creat.type+1;
    if(atoi(choice) == 0) return 1;
    
    //Get key word
    printf(" Please input the key word to search:\n");
    fflush(stdin);
    scanf("%s",key);
    
    //Search
    information=fopen("information.txt","r");
    while(fscanf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
     "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
     &creat.type,creat.class_name,creat.item[0],creat.item[1],creat.item[2]
     ,creat.item[3],creat.item[4],creat.item[5],creat.item[6]
     ,creat.item[7],creat.item[8],creat.item[9],creat.item[10]
     ,creat.item[11],creat.item[12],creat.item[13]
     ,creat.item[14],creat.item[15],creat.item[16]
     ,creat.item[17],creat.item[18],creat.item[19])!=EOF)
    {
        truth = 0;
        if(atoi(choice) == creat.type || atoi(choice) == all)
        {
            for(i = 0;i<20;i++){
            	if(strcmp(creat.item[i],key) == 0){
                    truth = 1;break;
                }
            }
            if(strcmp(creat.class_name,key) == 0) truth = 1;
        }
        if(truth == 1)
        {
            printf(" type:%-8s\n",creat.class_name);
            rewind(Club);
		    while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
		    "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
		    &type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
		    ,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
			,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
		    ,creat.name[11],creat.name[12],creat.name[13]
		    ,creat.name[14],creat.name[15],creat.name[16]
		    ,creat.name[17],creat.name[18],creat.name[19])!=EOF)
		    {
		    	if(type==creat.type)  break;
		    }
            for(i=0;i<20;i++)
            {
                if(strcmp(creat.item[i],"NOTHING")!=0)
                {
					printf("  %-20s : %s\n",creat.name[i],creat.item[i]);
                } 
            }
            printf("\n");
        }
    }
    fflush(stdin);
    getchar();
    fclose(information);
    return 1;
}

//******************************Information Copy (Second Level)*************************************

int information_copy()//main copy information function
{
	char choice[16]={'\0'};//record user's choice
	int repeat = 1;//repeat to choose
	
	while(repeat){
	//acquire user's choice
	while(1)
	{
		system("cls");//clear screen
		printf("\n You have entered Imformation Copy function\n");
		printf("\n Leave Immidiately    Please Input 0\n");
		printf(" Back to last level   Please Input 1\n");
		printf(" Copy  Information    Please Input 2\n");
		printf(" Cover Information    Please Input 3\n");
		printf(" Check   Copies       Please Input 4\n");
		fflush(stdin);
		scanf("%s",choice);
		if(judge_num(choice)!=0)
		    continue;
		if(atoi(choice)!=0&&atoi(choice)!=1
		&&atoi(choice)!=2&&atoi(choice)!=3&&atoi(choice)!=4)
		    continue;
		break;
	}
	//provide function responses to choice
	switch(atoi(choice))
	{
		case 1: return 1;//Back to last level
		case 2: repeat = information_copy_copy();break;//copy information
		case 3: repeat = information_copy_cover();break;//cover information
		case 4: repeat = information_copy_check();break;//check copies
		case 0: return 0;//exit
	}
	}//repeat over
	return 0;
}

int information_copy_copy()//copy information
{
    FILE * information;
    FILE * Copy;
    struct club creat;
    char choice[32];
    char choice2[32];
    
    //Get valued inputing
    while(1){
        system("cls");//Clear Screen
        printf("\n This is Copy Information function\n\n");
        printf(" Back to last    level   Please Input 0\n");
        printf(" Copy to first   space   Please Input 1\n");
        printf(" Copy to Second  space   Please Input 2\n");
        printf(" Copy to Third   space   Please Input 3\n");
        printf(" Copy to Forth   space   Please Input 4\n");
        printf(" Copy to Fifth   space   Please Input 5\n");
        printf(" Copy to Sixth   space   Please Input 6\n");
        printf(" Copy to Seventh space   Please Input 7\n");
	    printf(" Copy to Eighth  space   Please Input 8\n");
	    printf(" Copy to Ninth   space   Please Input 9\n");
	    printf(" Copy to Tenth   space   Please Input10\n");
        
        fflush(stdin);
        scanf("%s",choice);
        if(judge_num(choice)!=0)
            continue;
        if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
           &&atoi(choice)!=3&&atoi(choice)!=4&&atoi(choice)!=5
	     &&atoi(choice)!=6&&atoi(choice)!=7&&atoi(choice)!=8
		&&atoi(choice)!=9&&atoi(choice)!=10)
            continue;
        break;
    }
    if(atoi(choice) == 0)
        return 1;
    
    //Check whether to Copy
    printf(" Your operation would clear last copy!\n");
    printf(" Do you realy want to copy?\n");
    printf(" Input 'YES' to copy, others to leave.\n");
    fflush(stdin);
    scanf("%s",choice2);
    if(strcmp(choice2,"YES") != 0)
        return 1;
    
    //Supply responding functions
    switch(atoi(choice))
    {
        case 1 : Copy = fopen("information_copy1.txt","w"); break;
        case 2 : Copy = fopen("information_copy2.txt","w"); break;
        case 3 : Copy = fopen("information_copy3.txt","w"); break;
        case 4 : Copy = fopen("information_copy4.txt","w"); break;
        case 5 : Copy = fopen("information_copy5.txt","w"); break;
        case 6 : Copy = fopen("information_copy6.txt","w"); break;
        case 7 : Copy = fopen("information_copy7.txt","w"); break;
        case 8 : Copy = fopen("information_copy8.txt","w"); break;
        case 9 : Copy = fopen("information_copy9.txt","w"); break;
        case 10: Copy = fopen("information_copy10.txt","w");break;
    }
    information = fopen("information.txt","r");
    while(fscanf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
                 "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
                 &creat.type,creat.class_name,creat.item[0],creat.item[1],creat.item[2]
                 ,creat.item[3],creat.item[4],creat.item[5],creat.item[6]
                 ,creat.item[7],creat.item[8],creat.item[9],creat.item[10]
                 ,creat.item[11],creat.item[12],creat.item[13]
                 ,creat.item[14],creat.item[15],creat.item[16]
                 ,creat.item[17],creat.item[18],creat.item[19])!=EOF)
    {
        fprintf(Copy,"%d  %s  %s  %s  %s  %s  %s  %s"
                "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n",
                creat.type,creat.class_name,creat.item[0],creat.item[1],creat.item[2]
                ,creat.item[3],creat.item[4],creat.item[5],creat.item[6]
                ,creat.item[7],creat.item[8],creat.item[9],creat.item[10]
                ,creat.item[11],creat.item[12],creat.item[13]
                ,creat.item[14],creat.item[15],creat.item[16]
                ,creat.item[17],creat.item[18],creat.item[19]);
    }
    fclose(information);
    fclose(Copy);
    printf(" Copied Successfully! (Input anything to continue)\n");
    fflush(stdin);
    getchar();
    return 1;
}

int information_copy_cover()// information copis covering
{
	FILE * information;
    FILE * Copy;
    struct club creat;
    char choice[32];
    char choice2[32];
    
    //Get valued inputing
    while(1){
        system("cls");//Clear Screen
        printf("\n This is Cover Information function\n\n");
        printf(" Back  to last    level   Please Input 0\n");
        printf(" Cover by first   space   Please Input 1\n");
        printf(" Cover by Second  space   Please Input 2\n");
        printf(" Cover by Third   space   Please Input 3\n");
        printf(" Cover by Forth   space   Please Input 4\n");
        printf(" Cover by Fifth   space   Please Input 5\n");
        printf(" Cover by Sixth   space   Please Input 6\n");
        printf(" Cover by Seventh space   Please Input 7\n");
	    printf(" Cover by Eighth  space   Please Input 8\n");
	    printf(" Cover by Ninth   space   Please Input 9\n");
	    printf(" Cover by Tenth   space   Please Input10\n");
        
        fflush(stdin);
        scanf("%s",choice);
        if(judge_num(choice)!=0)
            continue;
        if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
           &&atoi(choice)!=3&&atoi(choice)!=4&&atoi(choice)!=5
	     &&atoi(choice)!=6&&atoi(choice)!=7&&atoi(choice)!=8
		&&atoi(choice)!=9&&atoi(choice)!=10)
            continue;
        break;
    }
    if(atoi(choice) == 0)
        return 1;
    
    //Check whether to Cover
    printf(" Your operation would clear your latest information!!\n");
    printf(" Do you realy want to cover?\n");
    printf(" Input 'YES' to copy, others to leave.\n");
    fflush(stdin);
    scanf("%s",choice2);
    if(strcmp(choice2,"YES") != 0)
        return 1;
    
    //Supply responding functions
    switch(atoi(choice))
    {
        case 1 : Copy = fopen("information_copy1.txt","r"); break;
        case 2 : Copy = fopen("information_copy2.txt","r"); break;
        case 3 : Copy = fopen("information_copy3.txt","r"); break;
        case 4 : Copy = fopen("information_copy4.txt","r"); break;
        case 5 : Copy = fopen("information_copy5.txt","r"); break;
        case 6 : Copy = fopen("information_copy6.txt","r"); break;
        case 7 : Copy = fopen("information_copy7.txt","r"); break;
        case 8 : Copy = fopen("information_copy8.txt","r"); break;
        case 9 : Copy = fopen("information_copy9.txt","r"); break;
        case 10: Copy = fopen("information_copy10.txt","r");break;
    }
    information = fopen("information.txt","w");
    while(fscanf(Copy,"%d  %s  %s  %s  %s  %s  %s  %s"
                 "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
                 &creat.type,creat.class_name,creat.item[0],creat.item[1],creat.item[2]
                 ,creat.item[3],creat.item[4],creat.item[5],creat.item[6]
                 ,creat.item[7],creat.item[8],creat.item[9],creat.item[10]
                 ,creat.item[11],creat.item[12],creat.item[13]
                 ,creat.item[14],creat.item[15],creat.item[16]
                 ,creat.item[17],creat.item[18],creat.item[19])!=EOF)
    {
        fprintf(information,"%d  %s  %s  %s  %s  %s  %s  %s"
                "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n",
                creat.type,creat.class_name,creat.item[0],creat.item[1],creat.item[2]
                ,creat.item[3],creat.item[4],creat.item[5],creat.item[6]
                ,creat.item[7],creat.item[8],creat.item[9],creat.item[10]
                ,creat.item[11],creat.item[12],creat.item[13]
                ,creat.item[14],creat.item[15],creat.item[16]
                ,creat.item[17],creat.item[18],creat.item[19]);
    }
    fclose(information);
    fclose(Copy);
    printf(" Covered Successfully! (Input anything to continue)\n");
    fflush(stdin);
    getchar();
    return 1;
}

int information_copy_check()//check information copies
{
    FILE * Copy;
    FILE * Club;
    struct club creat;
    char choice[32];
    char choice2[32];
    int i = 0;
    int type = 0;
    
    //Get valued inputing
    while(1)
	{
        system("cls");//Clear Screen
        printf("\n This is Check Information function\n\n");
        printf(" Back  to last    level   Please Input 0\n");
        printf(" Check   first    space   Please Input 1\n");
        printf(" Check   Second   space   Please Input 2\n");
        printf(" Check   Third    space   Please Input 3\n");
        printf(" Check   Forth    space   Please Input 4\n");
        printf(" Check   Fifth    space   Please Input 5\n");
        printf(" Check   Sixth    space   Please Input 6\n");
        printf(" Check   Seventh  space   Please Input 7\n");
	    printf(" Check   Eighth   space   Please Input 8\n");
	    printf(" Check   Ninth    space   Please Input 9\n");
	    printf(" Check   Tenth    space   Please Input10\n");
        
        fflush(stdin);
        scanf("%s",choice);
        if(judge_num(choice)!=0)
            continue;
        if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
           &&atoi(choice)!=3&&atoi(choice)!=4&&atoi(choice)!=5
	     &&atoi(choice)!=6&&atoi(choice)!=7&&atoi(choice)!=8
		&&atoi(choice)!=9&&atoi(choice)!=10)
            continue;
        break;
    }
    if(atoi(choice) == 0)
        return 1;
    
    //Supply responding functions
    switch(atoi(choice))
    {
        case 1 : Copy = fopen("information_copy1.txt","r"); break;
        case 2 : Copy = fopen("information_copy2.txt","r"); break;
        case 3 : Copy = fopen("information_copy3.txt","r"); break;
        case 4 : Copy = fopen("information_copy4.txt","r"); break;
        case 5 : Copy = fopen("information_copy5.txt","r"); break;
        case 6 : Copy = fopen("information_copy6.txt","r"); break;
        case 7 : Copy = fopen("information_copy7.txt","r"); break;
        case 8 : Copy = fopen("information_copy8.txt","r"); break;
        case 9 : Copy = fopen("information_copy9.txt","r"); break;
        case 10: Copy = fopen("information_copy10.txt","r");break;
    }
    Club=fopen("club.txt","r");
    while(fscanf(Copy,"%d  %s  %s  %s  %s  %s  %s  %s"
                 "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
                 &creat.type,creat.class_name,creat.item[0],creat.item[1],creat.item[2]
                 ,creat.item[3],creat.item[4],creat.item[5],creat.item[6]
                 ,creat.item[7],creat.item[8],creat.item[9],creat.item[10]
                 ,creat.item[11],creat.item[12],creat.item[13]
                 ,creat.item[14],creat.item[15],creat.item[16]
                 ,creat.item[17],creat.item[18],creat.item[19])!=EOF)
    {
    	printf(" type:%-8s\n",creat.class_name);
    	rewind(Club);
	    while(fscanf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
	    "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
	    &type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
	    ,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
		,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
	    ,creat.name[11],creat.name[12],creat.name[13]
	    ,creat.name[14],creat.name[15],creat.name[16]
	    ,creat.name[17],creat.name[18],creat.name[19])!=EOF)
	    {
	    	if(type==creat.type)  break;
	    }
		for(i=0;i<20;i++)
        {
            if(strcmp(creat.item[i],"NOTHING")!=0)
				printf("  %-20s : %s\n",creat.name[i],creat.item[i]);
        }
        printf("\n");
    }
    fclose(Copy);
    printf("(Input anything to continue)\n");
    fflush(stdin);
    getchar();
	return 1;
}

//******************************Tamplate Function(Second Level)*************************************

//.............................Tamplate Main Function(Third Level)..................................

int club_control()//Tamplate Main Function
{
    char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    
    while(repeat)
    {
        //acquire user's choice
        while(1){
            system("cls");//clear screen
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

//.............................Tamplate Creat (Third Level).........................................

int club_control_creat()//creat new templates
{
    struct club creat;
    FILE* Club;
    creat.type = 0;     //if there is no record in club.txt,creat.type = 0
    char choice[32];    //record user's choice and input
    char club_name[32]; //record new tamplate's name
    int number = 0;     //record the type number of new tamplate
    int i = 0;          //loop variable
    int valid = 1;      //validation of new tamplate's name
    
    //reminding
    system("cls");//clear screen
    printf("\n Your have entered Tamplate Creating section!\n");
    printf(" Input EOF at anywhere to stop adding\n\n");
    
    
    //achieve name of new tamplate
    while(valid)
    {
        number = 0;
        printf(" Please input the name of new tamplate:");
        fflush(stdin);
        scanf("%s",choice);
        if(strcmp(choice,"NOTHING") == 0)
        {
            printf(" Name cannot be NOTHING. Please input again\n");
            continue;
        }
        if(strcmp(choice,"EOF") == 0)
            return 1;
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
            if(strcmp(choice,creat.class_name)==0)
            {
                printf(" This name has already existed, please input again\n");
                valid = 1;//input again
                break;
            }
            if(number <= creat.type)
            {
                number = creat.type + 1;
                valid = 0;//do not need to input again
            }
        }
        if(creat.type == 0)//there is no record in club.txt
        {
            valid = 0;//do not need to input again
            number = 1;
        }
    }
    fclose(Club);
    strcpy(club_name,choice);
    
    //Add items' names in the new tamplate
    printf("\n The name of the new tamplate is %s\n",club_name);
    printf(" Please input items' name in the new tamplate (NO more than 20)\n");
    printf(" Input STOP to stop adding\n");
    for(i=0;i<20;i++)
    {
        while(1)
        {
            printf("  Input %2d item is %s:",i+1,club_name);
            fflush(stdin);
            scanf("%s",creat.name[i]);
            if(strcmp(creat.name[i],"NOTHING") == 0)
            {
                printf("  Name cannot be NOTHING. Please input again\n");
                continue;
            }
            break;
        }
        if(strcmp(creat.name[i],"EOF") == 0) return 1;
        if(strcmp(creat.name[i],"STOP") == 0) break;
    }
    for(i;i<20;i++)
    {
        strcpy(creat.name[i],"NOTHING");
    }
    
    //Make sure to add the new tamplate
    printf("\n Your adding tamplate is:\n");
    printf(" Tamplate name : %s\n",club_name);
    for(i=0;i<20;i++)
    {
        if(strcmp(creat.name[i],"NOTHING")!=0)
            printf("  %-2d:%s\n",i+1,creat.name[i]);
    }
    printf("\n Do you realy want to add it?\n Yes input 1,No input any others\n");
    fflush(stdin);
    scanf("%s",choice);
    if(strcmp(choice,"1") == 0)
    {
        Club=fopen("club.txt","a+");
        fprintf(Club,"%d  %s  %s  %s  %s  %s  %s  %s"
                "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n",
                number,club_name,creat.name[0],creat.name[1],creat.name[2]
                ,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
                ,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
                ,creat.name[11],creat.name[12],creat.name[13]
                ,creat.name[14],creat.name[15],creat.name[16]
                ,creat.name[17],creat.name[18],creat.name[19]);
        fclose(Club);
        printf(" You have succeed to add new tamplate %s!\n",club_name);
    }
    else
    {
        printf(" You have canceled the command\n");
    }
    fflush(stdin);
    getchar();
    return 1;
}

//...............................Tamplate Check (Third Level)............................................

int club_control_check()//Check Tamplate
{
    FILE * Club;
    struct club creat;
    int i = 0;//loop variable
    
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
        printf(" Tamplate:%s\n",creat.class_name);
        for(i=0;i<20;i++)
        {
            if(strcmp(creat.name[i],"NOTHING")!=0)
                printf("  %-2d : %s\n",i+1,creat.name[i]);
        }
        printf("\n");
    }
    fclose(Club);
    return 1;
}

//................................Tamplate Change (Third Level)...........................................

int club_control_change()//Change Tamplate
{
    char change_club[32];
    FILE * Club;
    FILE * draft;
    
    printf(" These are your Tamplates:\n\n");
    club_control_check();
    while(1)
    {
        printf("Please input changing tamplate's name"
               "(input BACK to return last level):");
        fflush(stdin);
        scanf("%s",change_club);
        if(strcmp(change_club,"BACK") == 0)
            return 1;
        if(club_control_change_ClubValid(change_club))
            continue;
        break;
    }
    printf(" Sorry! The programe cannot change Tamplates now!\n");
    fflush(stdin);
    getchar();
    //printf("????????????????/n");
    //scanf("%s");
    //????
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
     printf("???????%s\n",creat.class_name);
     for(i=0;i<20;i++)
     {
     if(strcmp(creat.name[i],"NOTHING")!=0)
     printf("  ?? %d ??%s\n",i+1,creat.name[i]);
     }
     printf("\n");
     }
     fclose(Club);
     */
    return 1;
}

int club_control_change_ClubValid(char change_club[])//vertify tamplate's name that user inputed
{
    FILE* Club;
    struct club creat;
    int success = 0;
    
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
        printf(" %s not found! Please input again!\n",change_club);
        return 1;
    }
    return 0;
}

//................................Tamplate Copy (Third Level).............................................

int club_control_copy()//Copy Tamplate
{
    FILE * Club;
    FILE * Copy;
    struct club creat;
    char choice[32];
    char choice2[32];
    
    //Get valued inputing
    while(1){
        system("cls");//Clear Screen
        printf("\n This is Copy Tamplate function\n");
        printf(" Back to last   level   Please Input 0\n");
        printf(" Copy to first  space   Please Input 1\n");
        printf(" Copy to Second space   Please Input 2\n");
        printf(" Copy to Third  space   Please Input 3\n");
        printf(" Copy to Forth  space   Please Input 4\n");
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
    
    //Check whether to Copy
    printf(" Your operation would clear last copy!\n");
    printf(" Do you realy want to copy?\n");
    printf(" Input 'YES' to copy, others to leave.\n");
    fflush(stdin);
    scanf("%s",choice2);
    if(strcmp(choice2,"YES") != 0)
        return 1;
    
    //Supply responding functions
    switch(atoi(choice))
    {
        case 1: Copy = fopen("club_copy1.txt","w");break;
        case 2: Copy = fopen("club_copy2.txt","w");break;
        case 3: Copy = fopen("club_copy3.txt","w");break;
        case 4: Copy = fopen("club_copy4.txt","w");break;
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
    printf(" Copied Successfully! (Input anything to continue)\n");
    fflush(stdin);
    getchar();
    return 1;
}

int club_control_copy_check()//check copies
{
    char choice[16]={'\0'};//record user's choice
    int i;//Loop varibles
    FILE * Copy;
    struct club creat;
    
    //Get valued inputing
    while(1)
    {
        system("cls");//Clear Screen
        printf("\n This is Copy checking function\n");
        printf(" Please input the number of Copy Space\n");
        printf(" Back to last level   Input 0\n");
        printf(" First  copy  space   Input 1\n");
        printf(" Second copy  space   Input 2\n");
        printf(" Third  copy  space   Input 3\n");
        printf(" Forth  copy  space   Input 4\n");
        fflush(stdin);
        scanf("%s",choice);
        if(judge_num(choice)!=0)
            continue;
        if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2
           &&atoi(choice)!=3&&atoi(choice)!=4)
            continue;
        break;
    }
    
    //Supply responding functions
    switch(atoi(choice))
    {
        case 0: return 1;
        case 1: Copy = fopen("club_copy1.txt","r");break;
        case 2: Copy = fopen("club_copy2.txt","r");break;
        case 3: Copy = fopen("club_copy3.txt","r");break;
        case 4: Copy = fopen("club_copy4.txt","r");break;
    }
    while(fscanf(Copy,"%d  %s  %s  %s  %s  %s  %s  %s"
                 "  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s  %s",
                 &creat.type,creat.class_name,creat.name[0],creat.name[1],creat.name[2]
                 ,creat.name[3],creat.name[4],creat.name[5],creat.name[6]
                 ,creat.name[7],creat.name[8],creat.name[9],creat.name[10]
                 ,creat.name[11],creat.name[12],creat.name[13]
                 ,creat.name[14],creat.name[15],creat.name[16]
                 ,creat.name[17],creat.name[18],creat.name[19])!=EOF)
    {
        printf(" Tamplate:%s\n",creat.class_name);
        for(i=0;i<20;i++)
        {
            if(strcmp(creat.name[i],"NOTHING")!=0)
                printf("  %-2d : %s\n",i+1,creat.name[i]);
        }
        printf("\n");
    }
    fclose(Copy);
    printf(" (Input anything to continue)\n");
    fflush(stdin);
    getchar();
    return 1;
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
            printf(" Please input an integer!\n");
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
            printf(" Don't input blank!\n");
            fflush(stdin);
            getchar();
            valid = 1;
            break;
        }
    }
    return valid;
}

