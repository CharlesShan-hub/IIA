//*******************************Add Information(Second Level)**************************************
#include "define.h"

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
        printf("\n Information adding module\n");
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

