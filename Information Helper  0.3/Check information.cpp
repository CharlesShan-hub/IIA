//*********************************Check Information(Second Level)**********************************
#include "define.h"

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
        printf("\n Information Checking module\n");
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
