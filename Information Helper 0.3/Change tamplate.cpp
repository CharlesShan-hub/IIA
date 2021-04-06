//*********************************Change Tamplate(Second Level)**********************************
#include "define.h"

int club_control_change()//Change Tamplate
{
    char change_club[32];
    FILE * Club;
    FILE * draft;
    system("cls");//clear screen
    printf("\n Tamplates Changing module\n");
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
