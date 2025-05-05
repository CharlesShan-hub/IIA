//*********************************Display Setting(Second Level)**********************************
#include "define.h"
//Setting of display
int screen_color;
int letter_color;

int setting_display()//Display Setting
{
	char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    FILE* setting;
	
	setting=fopen("setting.txt","r"); 
	fscanf(setting,"%d  %d",&screen_color,&letter_color);
	
	fclose(setting);
    
    while(repeat)
    {
        //acquire user's choice
        while(1){
            printf("\n Setting Display module\n");
			system("cls");//clear screen
			printf("\n Leave  Immidiately    Please Input 0\n");
			printf(" Back To Last Level    Please Input 1\n");
            printf(" Color of screen       Please Input 2\n");
            printf(" Color of letters      Please Input 3\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)!=0&&atoi(choice)!=1&&atoi(choice)!=2&&atoi(choice)!=3)
                continue;
            break;
        }
        //provide function responses to choice
        switch(atoi(choice))
        {
            case 0: return 0;
            case 1: return 1;
            case 2: repeat = setting_display_screen();  break;
            case 3: repeat = setting_display_letters(); break;
        }
    }//repeat over
}

int setting_display_screen()
{
	char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    FILE* setting;
    
    while(repeat)
    {
        //acquire user's choice
        while(1){
            system("cls");//clear screen
            printf("\n Setting Screen Color module\n");
            printf("\n Back To Last Level    Please Input  0\n");
            printf(" Black                 Please Input  1\n");
            printf(" Blue                  Please Input  2\n");
            printf(" Green                 Please Input  3\n");
            printf(" Light Green           Please Input  4\n");
            printf(" Red                   Please Input  5\n");
            printf(" Purple                Please Input  6\n");
            printf(" Yellow                Please Input  7\n");
            printf(" White                 Please Input  8\n");
            printf(" Gray                  Please Input  9\n");
            printf(" Light Blue            Please Input 10\n");
            printf(" Light Green           Please Input 11\n");
            printf(" A pale light Green    Please Input 12\n");
            printf(" Light Red             Please Input 13\n");
            printf(" Light Purple          Please Input 14\n");
            printf(" Light Yellow          Please Input 15\n");
            printf(" Bright White          Please Input 16\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)<0||atoi(choice)>16)
                continue;
            if(atoi(choice) == letter_color)
            	continue;
            if(atoi(choice) == 0)
            	return 1;
            break;
        }
        //provide function responses to choice
        screen_color = atoi(choice);
        setting=fopen("setting.txt","w"); 
		fprintf(setting,"%d  %d",screen_color,letter_color);
		fclose(setting);
		setting_display_slcolor(letter_color,screen_color);
    }//repeat over
}

int setting_display_letters()
{
	char choice[16]={'\0'};//record user's choice
    int repeat = 1;//repeat to choose
    FILE* setting;
    
    while(repeat)
    {
        //acquire user's choice
        while(1){
            system("cls");//clear screen
            printf("\n Setting Letters color module\n");
            printf("\n Back To Last Level    Please Input  0\n");
            printf(" Black                 Please Input  1\n");
            printf(" Blue                  Please Input  2\n");
            printf(" Green                 Please Input  3\n");
            printf(" Light Green           Please Input  4\n");
            printf(" Red                   Please Input  5\n");
            printf(" Purple                Please Input  6\n");
            printf(" Yellow                Please Input  7\n");
            printf(" White                 Please Input  8\n");
            printf(" Gray                  Please Input  9\n");
            printf(" Light Blue            Please Input 10\n");
            printf(" Light Green           Please Input 11\n");
            printf(" A pale light Green    Please Input 12\n");
            printf(" Light Red             Please Input 13\n");
            printf(" Light Purple          Please Input 14\n");
            printf(" Light Yellow          Please Input 15\n");
            printf(" Bright White          Please Input 16\n");
            fflush(stdin);
            scanf("%s",choice);
            if(judge_num(choice)!=0)
                continue;
            if(atoi(choice)<0||atoi(choice)>16)
                continue;
            if(atoi(choice) == screen_color)
            	continue;
            if(atoi(choice) == 0)
            	return 1;
            break;
        }
        //provide function responses to choice
        letter_color = atoi(choice);
        setting=fopen("setting.txt","w"); 
		fprintf(setting,"%d  %d",screen_color,letter_color);
		fclose(setting);
        setting_display_slcolor(letter_color,screen_color);
    }//repeat over
}

void setting_display_slcolor(int letter_color,int screen_color)
{
	switch(letter_color)
        {
        	case 1: switch(screen_color){
        		case 2: system("color 10");break;
				case 3: system("color 20");break;
				case 4: system("color 30");break;
				case 5: system("color 40");break;
				case 6: system("color 50");break;
				case 7: system("color 60");break;
				case 8: system("color 70");break;
				case 9: system("color 80");break;
				case 10:system("color 90");break;
				case 11:system("color A0");break;
				case 12:system("color B0");break;
				case 13:system("color C0");break;
				case 14:system("color D0");break;
				case 15:system("color E0");break;
				case 16:system("color F0");break;
        	}break;
        	case 2: switch(screen_color){
        		case 1:  system("color 01");break;
        		case 3:  system("color 21");break;
        		case 4:  system("color 31");break;
        		case 5:  system("color 41");break;
        		case 6:  system("color 51");break;
        		case 7:  system("color 61");break;
        		case 8:  system("color 71");break;
        		case 9:  system("color 81");break;
        		case 10: system("color 91");break;
        		case 11: system("color A1");break;
        		case 12: system("color B1");break;
        		case 13: system("color C1");break;
        		case 14: system("color D1");break;
        		case 15: system("color E1");break;
        		case 16: system("color F1");break;
        	}break;
        	case 3: switch(screen_color){
        		case 1:  system("color 02");break;
        		case 2:  system("color 12");break;
        		case 4:  system("color 32");break;
        		case 5:  system("color 42");break;
        		case 6:  system("color 52");break;
        		case 7:  system("color 62");break;
        		case 8:  system("color 72");break;
        		case 9:  system("color 82");break;
        		case 10: system("color 92");break;
        		case 11: system("color A2");break;
        		case 12: system("color B2");break;
        		case 13: system("color C2");break;
        		case 14: system("color D2");break;
        		case 15: system("color E2");break;
        		case 16: system("color F2");break;
        	}break;
        	case 4: switch(screen_color){
        		case 1:  system("color 03");break;
        		case 2:  system("color 13");break;
        		case 3:  system("color 23");break;
        		case 5:  system("color 43");break;
        		case 6:  system("color 53");break;
        		case 7:  system("color 63");break;
        		case 8:  system("color 73");break;
        		case 9:  system("color 83");break;
        		case 10: system("color 93");break;
        		case 11: system("color A3");break;
        		case 12: system("color B3");break;
        		case 13: system("color C3");break;
        		case 14: system("color D3");break;
        		case 15: system("color E3");break;
        		case 16: system("color F3");break;
        	}break;
        	case 5: switch(screen_color){
        		case 1:  system("color 04");break;
        		case 2:  system("color 14");break;
        		case 3:  system("color 24");break;
        		case 4:  system("color 34");break;
        		case 6:  system("color 54");break;
        		case 7:  system("color 64");break;
        		case 8:  system("color 74");break;
        		case 9:  system("color 84");break;
        		case 10: system("color 94");break;
        		case 11: system("color A4");break;
        		case 12: system("color B4");break;
        		case 13: system("color C4");break;
        		case 14: system("color D4");break;
        		case 15: system("color E4");break;
        		case 16: system("color F4");break;
        	}break;
        	case 6: switch(screen_color){
        		case 1:   system("color 05");break;
        		case 2:   system("color 15");break;
        		case 3:   system("color 25");break;
        		case 4:   system("color 35");break;
        		case 5:   system("color 45");break;
        		case 7:   system("color 65");break;
        		case 8:   system("color 75");break;
        		case 9:   system("color 85");break;
        		case 10:  system("color 95");break;
        		case 11:  system("color A5");break;
        		case 12:  system("color B5");break;
        		case 13:  system("color C5");break;
        		case 14:  system("color D5");break;
        		case 15:  system("color E5");break;
        		case 16:  system("color F5");break;
        	}break;
        	case 7: switch(screen_color){
        		case 1:   system("color 06");break;
        		case 2:   system("color 16");break;
        		case 3:   system("color 26");break;
        		case 4:   system("color 36");break;
        		case 5:   system("color 46");break;
        		case 6:   system("color 56");break;
        		case 8:   system("color 76");break;
        		case 9:   system("color 86");break;
        		case 10:  system("color 96");break;
        		case 11:  system("color A6");break;
        		case 12:  system("color B6");break;
        		case 13:  system("color C6");break;
        		case 14:  system("color D6");break;
        		case 15:  system("color E6");break;
        		case 16:  system("color F6");break;
        	}break;
        	case 8: switch(screen_color){
        		case 1:   system("color 07");break;
        		case 2:   system("color 17");break;
        		case 3:   system("color 27");break;
        		case 4:   system("color 37");break;
        		case 5:   system("color 47");break;
        		case 6:   system("color 57");break;
        		case 7:   system("color 67");break;
        		case 9:   system("color 87");break;
        		case 10:  system("color 97");break;
        		case 11:  system("color A7");break;
        		case 12:  system("color B7");break;
        		case 13:  system("color C7");break;
        		case 14:  system("color D7");break;
        		case 15:  system("color E7");break;
        		case 16:  system("color F7");break;
        	}break;
        	case 9: switch(screen_color){
        		case 1:   system("color 08");break;
        		case 2:   system("color 18");break;
        		case 3:   system("color 28");break;
        		case 4:   system("color 38");break;
        		case 5:   system("color 48");break;
        		case 6:   system("color 58");break;
        		case 7:   system("color 68");break;
        		case 8:   system("color 78");break;
        		case 10:  system("color 98");break;
        		case 11:  system("color A8");break;
        		case 12:  system("color B8");break;
        		case 13:  system("color C8");break;
        		case 14:  system("color D8");break;
        		case 15:  system("color E8");break;
        		case 16:  system("color F8");break;
        	}break;
        	case 10:switch(screen_color){
        		case 1:   system("color 09");break;
        		case 2:   system("color 19");break;
        		case 3:   system("color 29");break;
        		case 4:   system("color 39");break;
        		case 5:   system("color 49");break;
        		case 6:   system("color 59");break;
        		case 7:   system("color 69");break;
        		case 8:   system("color 79");break;
        		case 9:   system("color 89");break;
        		case 11:  system("color A9");break;
        		case 12:  system("color B9");break;
        		case 13:  system("color C9");break;
        		case 14:  system("color D9");break;
        		case 15:  system("color E9");break;
        		case 16:  system("color F9");break;
        	}break;
        	case 11:switch(screen_color){
        		case 1:   system("color 0A");break;
        		case 2:   system("color 1A");break;
        		case 3:   system("color 2A");break;
        		case 4:   system("color 3A");break;
        		case 5:   system("color 4A");break;
        		case 6:   system("color 5A");break;
        		case 7:   system("color 6A");break;
        		case 8:   system("color 7A");break;
        		case 9:   system("color 8A");break;
        		case 10:  system("color 9A");break;
        		case 12:  system("color BA");break;
        		case 13:  system("color CA");break;
        		case 14:  system("color DA");break;
        		case 15:  system("color EA");break;
        		case 16:  system("color FA");break;
        	}break;
        	case 12:switch(screen_color){
        		case 1:   system("color 0B");break;
        		case 2:   system("color 1B");break;
        		case 3:   system("color 2B");break;
        		case 4:   system("color 3B");break;
        		case 5:   system("color 4B");break;
        		case 6:   system("color 5B");break;
        		case 7:   system("color 6B");break;
        		case 8:   system("color 7B");break;
        		case 9:   system("color 8B");break;
        		case 10:  system("color 9B");break;
        		case 11:  system("color AB");break;
        		case 13:  system("color CB");break;
        		case 14:  system("color DB");break;
        		case 15:  system("color EB");break;
        		case 16:  system("color FB");break;
        	}break;
        	case 13:switch(screen_color){
        		case 1:   system("color 0C");break;
        		case 2:   system("color 1C");break;
        		case 3:   system("color 2C");break;
        		case 4:   system("color 3C");break;
        		case 5:   system("color 4C");break;
        		case 6:   system("color 5C");break;
        		case 7:   system("color 6C");break;
        		case 8:   system("color 7C");break;
        		case 9:   system("color 8C");break;
        		case 10:  system("color 9C");break;
        		case 11:  system("color AC");break;
        		case 12:  system("color BC");break;
        		case 14:  system("color DC");break;
        		case 15:  system("color EC");break;
        		case 16:  system("color FC");break;
        	}break;
        	case 14:switch(screen_color){
        		case 1:   system("color 0D");break;
        		case 2:   system("color 1D");break;
        		case 3:   system("color 2D");break;
        		case 4:   system("color 3D");break;
        		case 5:   system("color 4D");break;
        		case 6:   system("color 5D");break;
        		case 7:   system("color 6D");break;
        		case 8:   system("color 7D");break;
        		case 9:   system("color 8D");break;
        		case 10:  system("color 9D");break;
        		case 11:  system("color AD");break;
        		case 12:  system("color BD");break;
        		case 13:  system("color CD");break;
        		case 15:  system("color ED");break;
        		case 16:  system("color FD");break;
        	}break;
        	case 15:switch(screen_color){
        		case 1:   system("color 0E");break;
        		case 2:   system("color 1E");break;
        		case 3:   system("color 2E");break;
        		case 4:   system("color 3E");break;
        		case 5:   system("color 4E");break;
        		case 6:   system("color 5E");break;
        		case 7:   system("color 6E");break;
        		case 8:   system("color 7E");break;
        		case 9:   system("color 8E");break;
        		case 10:  system("color 9E");break;
        		case 11:  system("color AE");break;
        		case 12:  system("color BE");break;
        		case 13:  system("color CE");break;
        		case 14:  system("color DE");break;
        		case 16:  system("color FE");break;
        	}break;
        	case 16:switch(screen_color){
        		case 1:   system("color 0F");break;
        		case 2:   system("color 1F");break;
        		case 3:   system("color 2F");break;
        		case 4:   system("color 3F");break;
        		case 5:   system("color 4F");break;
        		case 6:   system("color 5F");break;
        		case 7:   system("color 6F");break;
        		case 8:   system("color 7F");break;
        		case 9:   system("color 8F");break;
        		case 10:  system("color 9F");break;
        		case 11:  system("color AF");break;
        		case 12:  system("color BF");break;
        		case 13:  system("color CF");break;
        		case 14:  system("color EF");break;
        		case 15:  system("color DF");break;
        	}break;
        }
}
