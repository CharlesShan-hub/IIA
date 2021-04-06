# mian function

def main():
    choice = " "
    choice_num = 0
    repeat = 1 #repeat to choose
    
    while repeat == 1:
        # acquire user's choice
        while 1:
            print("\n     INFORMATION     SYSTEM")
            print("\n Leave Immidiately           Please Input 0")
            print(" Related to Information      Please Input 1")
            print(" Related to Tempalte         Please Input 2")
            print(" Setting                     Please Input 3")
            choice = input()
            if choice!='0' and choice!='1' and choice!='2' and choice!='3':
                continue
            break
        choice_num = eval(choice)
        # provide function responses to choice
        if choice_num == 0:
            repeat = 0;
        elif choice_num == 1:
            repeat = information_control()
        elif choice_num == 2:
            repeat = template_control()
        elif choice_num == 3:
            repeat = setting_control()
    return 0

def information_control():
    choice = " "
    choice_num = 0
    repeat = 1 #repeat to choose
    
    while repeat == 1:
        # acquire user's choice
        while 1:
            print("\n Imformation section")
            print("\n Leave Immidiately           Please Input 0")
            print(" Back to last level          Please Input 1")
            print(" Add    information          Please Input 2")
            print(" Check  information          Please Input 3")
            choice = input()
            if choice!='0' and choice!='1' and choice!='2' and choice!='3':
                continue
            break
        choice_num = eval(choice)
        # provide function responses to choice
        if choice_num == 0:
            return 0
        elif choice_num == 1:
            return 1
        elif choice_num == 2:
            print("2!")
        elif choice_num == 3:
            print("3!")
    return 1
    
def template_control():
    choice = " "
    choice_num = 0
    repeat = 1 #repeat to choose
    
    while repeat == 1:
        # acquire user's choice
        while 1:
            print("\n Template section")
            print("\n Leave Immidiately           Please Input 0")
            print(" Back to last level          Please Input 1")
            print(" Add    template             Please Input 2")
            print(" Check  template             Please Input 3")
            choice = input()
            if choice!='0' and choice!='1' and choice!='2' and choice!='3':
                continue
            break
        choice_num = eval(choice)
        # provide function responses to choice
        if choice_num == 0:
            return 0
        elif choice_num == 1:
            return 1
        elif choice_num == 2:
            print("2!")
        elif choice_num == 3:
            print("3!")
    return 1
    
def setting_control():
    choice = " "
    choice_num = 0
    repeat = 1 #repeat to choose
    
    while repeat == 1:
        # acquire user's choice
        while 1:
            print("\n Setting section")
            print("\n Leave Immidiately           Please Input 0")
            print(" Back to last level          Please Input 1")
            print(" Change colors               Please Input 2")
            choice = input()
            if choice!='0' and choice!='1' and choice!='2':
                continue
            break
        choice_num = eval(choice)
        # provide function responses to choice
        if choice_num == 0:
            return 0
        elif choice_num == 1:
            return 1
        elif choice_num == 2:
            print("2!")
    return 1




'''
from tkinter import *
mygui = Tk(className = '小肥川')
text = Text(width = 40,height = 4)
btn=Button()
btn['text']='确认'
btn.pack()
text.pack()
mainloop()
'''
main()