import time
import keyboard as kb
import threading
import os

from pynput.keyboard import *
from tkinter import *


button_choosing=False
# PRESS AND RELEASE LOOP
press_release_hold=False
press_release_hold_enable_button= 'None'
press_release_hold_toggle_button='None'

# ONE PRESS AND HOLD
one_press_hold=False
one_press_hold_enable_button='None'
one_press_hold_toggle_button='None'

# EXIT BUTTON
exit_button='+'

#  HANDLING CONFIG FILE
def read_config(line,index):
    global press_release_hold_enable_button,press_release_hold_toggle_button,one_press_hold_enable_button,one_press_hold_toggle_button
    if index==1:
        press_release_hold_enable_button=line[line.index('=')+1:].strip()
    elif index==2:
        press_release_hold_toggle_button=line[line.index('=')+1:].strip()
    elif index==3:
        one_press_hold_enable_button=line[line.index('=')+1:].strip()
    elif index==4:
        one_press_hold_toggle_button=line[line.index('=')+1:].strip()

def write_config():
    global press_release_hold_enable_button,press_release_hold_toggle_button,one_press_hold_enable_button,one_press_hold_toggle_button
    text="press_release_hold_enable_button={}\n\
press_release_hold_toggle_button={}\n\
one_press_hold_enable_button={}\n\
one_press_hold_toggle_button={}".format(press_release_hold_enable_button,
                                                                press_release_hold_toggle_button,
                                                                one_press_hold_enable_button,
                                                                one_press_hold_toggle_button)
    with open('config.txt','w') as file:
        file.write(text)

# READING CONFIG        
if os.path.exists(os.getcwd()+'\\config.txt'):
     with open('config.txt','r') as file:
         for index in range(1,4+1):
             read_config(file.readline(),index)
# END OF HANDLING CONFIG FILE

# INSTRUCTIONS
if press_release_hold_enable_button!='None' and press_release_hold_toggle_button!='None':
    print(f"Press {press_release_hold_enable_button.capitalize()} to keep pressing and releasing {press_release_hold_toggle_button.capitalize()}!")  
if one_press_hold_enable_button!='None' and one_press_hold_toggle_button!='None':    
    print(f"Press {one_press_hold_enable_button.capitalize()} to keep pressing {one_press_hold_toggle_button.capitalize()}!\n")
print(f"Press {exit_button.capitalize()} to exit the program!\n")

# WINDOW INIT
window=Tk()

# CLICKER FUNCTIONS
def clicker():
    global press_release_hold,button_choosing
    while press_release_hold and not button_choosing:
            kb.press_and_release(press_release_hold_toggle_button)
            time.sleep(0.03)
    kb.release(press_release_hold_toggle_button)
    print("PRESS RELEASE HOLD OFF\n")

def main_listener(key):
    global one_press_hold,press_release_hold,\
        press_release_hold_enable_button,\
        press_release_hold_toggle_button,\
        one_press_hold_enable_button,\
        one_press_hold_toggle_button,\
        button_choosing
    try:
        if not button_choosing:
            # PRESS RELEASE HOLD
            if key.char==press_release_hold_enable_button:
                press_release_hold= not press_release_hold
                if press_release_hold:
                    x=threading.Thread(target=clicker,args=())   
                    x.start()
                    print("PRESS RELEASE HOLD ON\n")
            # ONE PRESS HOLD
            if key.char==one_press_hold_enable_button:
                    one_press_hold=not one_press_hold
                    if one_press_hold:
                        kb.press(one_press_hold_toggle_button)
                        print("ONE PRESS HOLD ON\n")
                    if not one_press_hold:
                        kb.release(one_press_hold_toggle_button)
                        print("ONE PRESS HOLD OFF\n")
            # EXITING PROGRAM
            if key.char==exit_button:
                one_press_hold=False
                press_release_hold=False
                print("EXIT")
                write_config()
                window.quit()
                window.destroy()
                return False
    except AttributeError:
        pass


    
# END OF CLICKER FUNCTIONS
button=None
def intermediate(button_name,button_value):
    global one_press_hold_enable_button,\
        one_press_hold_toggle_button,\
        press_release_hold_enable_button,\
        press_release_hold_toggle_button
        
def change_button():
    global button_choosing,\
        one_press_hold_enable_button,\
        one_press_hold_toggle_button,\
        press_release_hold_enable_button,\
        press_release_hold_toggle_button
    if button=='one_press_hold_enable_button':
        kb.remove_hotkey(one_press_hold_enable_button)
        print('Choose one press hold enable button')
        one_press_hold_enable_button=kb.read_hotkey()
        kb.add_hotkey(one_press_hold_enable_button,suppress=True)
    elif button=='one_press_hold_toggle_button':
        kb.remove_hotkey(one_press_hold_toggle_button)
        print('Choose a new one press hold toggle button')
        one_press_hold_toggle_button=kb.read_hotkey()
        kb.add_hotkey(one_press_hold_toggle_button,suppress=True)
    elif button=='press_release_hold_enable_button':
        kb.remove_hotkey(press_release_hold_enable_button)
        print('Choose press release hold enable button')
        press_release_hold_enable_button=kb.read_hotkey()
        kb.add_hotkey(press_release_hold_enable_button,suppress=True)
    elif button=='press_release_hold_toggle_button':
        kb.remove_hotkey(press_release_hold_toggle_button)
        print('Choose press release hold toggle button')
        press_release_hold_toggle_button=kb.read_hotkey()
        kb.add_hotkey(press_release_hold_toggle_button,suppress=True)
    button_choosing=False        
    
def change_button_init(new_button):
    global button,button_choosing,one_press_hold,one_press_hold_enable_button,press_release_hold
    # HANDLING CURRENT PROCCESSES
    if one_press_hold:
        one_press_hold=not one_press_hold
        kb.release(one_press_hold_toggle_button)
        print("ONE PRESS HOLD OFF\n")
    if press_release_hold:
        press_release_hold=not press_release_hold
    # HANDLING ATTRIBUTION    
    button_choosing=True
    button=new_button
    x=threading.Thread(target=change_button)
    x.daemon=True
    x.start()
    

if __name__=='__main__': 
    listener_main=Listener(on_press=main_listener)
    listener_main.name='listenerul pe care l am facut acus'
    listener_main.start()
    
    
    window.geometry('400x400')
    window.resizable(False,False)
    
    button1=Button(window,text="Change button",fg='green',bg='black',font=('Arial',10,"bold"),command=lambda: change_button_init('one_press_hold_buttons'))
    button1.place(x=0,y=0)
    
    window.mainloop()



