import time
import keyboard as kb
import threading

from tkinter import *
from Keys import Keys
from SaveConfig import SaveConfig

def repeat_function():
    if repeat_enable.state and repeat_button.value!='None':
        print('Repeat Enabled\n')
        while repeat_enable.state and not changing_state:
                kb.press_and_release(repeat_button.value)
                time.sleep(0.04)
        print("Repeat Disabled\n")
    
def press_function():
    if press_enable.state and press_button.value!='None':
        kb.press(press_button.value)
        print('Press Enabled\n')
    elif press_button.value!='None':
        kb.release(press_button.value)
        print('Stopped Pressing\n')    

# CHANGING BUTTONS
changing_state=False
changing_button=''
# PRESS AND RELEASE LOOP
repeat_enable=Keys(name='repeat_enable',description='Choose button to enable the repeated pressing',state=False,function=repeat_function)
repeat_button=Keys(name='repeat_button',description='Choose button to repeat pressing',state=None,function=None)

# ONE PRESS AND HOLD
press_enable=Keys(name='press_enable',description='Choose button to enable one time press and hold',state=False,function=press_function)
press_button=Keys(name='press_button',description='Choose button to press once and hold onto',state=None,function=None)

# ARRAY
enable_keys=[repeat_enable,press_enable]

def are_same_keys():
    if repeat_enable.value == press_enable.value and repeat_enable.value!='None':
        return True
    else:
        return False

# SAVE FILE
save=SaveConfig(repeat_enable,repeat_button,press_enable,press_button)

def  main(e):
    if not changing_state:
        if e.event_type=='down':
            for key in enable_keys:
                if e.name==key.value and not key.pressed:
                    key.pressed=True
                    key.state= not key.state
                    x=threading.Thread(target=lambda:key.function(),daemon=True,name=key.name)
                    x.start()
        elif e.event_type=='up':
            for key in enable_keys:
                if e.name==key.value and key.pressed:
                    key.pressed=False     

second_window=Toplevel()
created_window=False

def main_change(e):
    global changing_state,changing_button
    if changing_state:
        abort=False
        if(e.event_type=='down'):
            for key in enable_keys:
                if changing_button!=key and e.name==key.value and changing_button!=repeat_button and changing_button!= press_button:
                    print("You tried to attribute the same value to "+ changing_button.name+ " as "+ key.name+"'s value! REFUSED")
                    abort=True
            if not abort:
                changing_button.value=e.name
                print('Changed value for '+changing_button.name+' in '+e.name)
        changing_state=False
        second_window.quit()
        

def change_button(button):
    global changing_state,changing_button
    if changing_state==False:
        changing_state=True
        changing_button=button
        print('waiting for input...')
    else:
        print('MAI INTAI SELECTEAZA BUTONUL ANTERIOR, BIATCH!')

def new_window(key):
    global created_window,second_window,window
    if not created_window:
        second_window.master=window
        #second_window=Toplevel(window)
        second_window.geometry('200x50')
        second_window.resizable(False,False)
        second_window.title('')

        label=Label(second_window,text='Choose '+key.name)
        label.pack()
        button=Button(second_window,text='...',command=lambda: change_button(key))
        button.pack()
        window.wait_window(second_window)
    
if __name__=='__main__': 
    # WINDOW INIT
    window=Tk()
    window.geometry('400x400')
    window.resizable(False,False)
    window.title('RClicker')
    
    # HANDLING CLOSING WINDOW BEHAVIOUR   
    def on_closing():
        save.write_config()
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_closing) 
     
    #  CONFIGURATION
    
    save.read_config()
    if are_same_keys():
        print("Values for some keys who should not have the same value are the same. Changing to None")
        repeat_enable.value='None'
        press_enable.value='None'

    # INSTRUCTIONS

    if repeat_enable.value!='None' and repeat_button.value!='None':
        print(f"Press {repeat_enable.value.capitalize()} to keep pressing and releasing {repeat_button.value.capitalize()}!")  
    if press_enable.value!='None' and press_button.value!='None':    
        print(f"Press {press_enable.value.capitalize()} to keep pressing {press_button.value.capitalize()}!\n")

    kb.hook(main)
    kb.hook(main_change)
        
    window_repeat_enable=Button(window,text="Repeat Enable",fg='green',bg='black',font=('Arial',10,"bold"),command=lambda: new_window(repeat_enable))
    window_repeat_button=Button(window,text="Repeat Button",fg='green',bg='black',font=('Arial',10,"bold"),command=lambda: new_window(repeat_button))
        
    window_press_enable=Button(window,text="Press Enable",fg='green',bg='black',font=('Arial',10,"bold"),command=lambda: new_window(press_enable))
    window_press_button=Button(window,text="Press Button",fg='green',bg='black',font=('Arial',10,"bold"),command=lambda: new_window(press_button))
        
    window_repeat_enable.place(x=0,y=0)
    window_repeat_button.place(x=110,y=0)
        
    window_press_enable.place(x=0,y=100)
    window_press_button.place(x=100,y=100)
    window.mainloop()