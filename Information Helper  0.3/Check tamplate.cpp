//*********************************Check Tamplate(Second Level)**********************************
#include "define.h"

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
