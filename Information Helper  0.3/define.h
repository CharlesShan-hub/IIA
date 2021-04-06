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
int information_control(void);//information
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

int setting_control(void);//setting
int setting_display(void);//setting display
int setting_display_screen(void);//setting display of screen
int setting_display_letters(void);//setting display of letters
void setting_display_slcolor(int,int);//set color of screen and letters

//tool
int judge_num(char num[]);//judge the input is interger or not
int judge_kongge(char[]);//jugdge the input has blank or not

