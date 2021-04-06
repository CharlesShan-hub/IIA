//*********************************Creat Tamplate(Second Level)**********************************
#include "define.h"

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
    printf("\n Tamplates creating module\n");
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

