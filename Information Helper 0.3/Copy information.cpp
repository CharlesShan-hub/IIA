//******************************Copy Information (Second Level)*************************************
#include "define.h"
/* 
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

*/ 
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
        printf("\n Information Copy module\n\n");
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
        printf("\n Information Copies Cover module\n\n");
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
        printf("\n Information Copies Check module\n\n");
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
