//*********************************Copy Tamplate(Second Level)**********************************
#include "define.h"

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
        printf("\n Tamplates Copy module\n");
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
        printf("\n Tamplates Checking Copies module\n");
        printf("\n Please input the number of Copy Space\n");
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

