import time
import threading
import keyboard as kb
import mouse as ms
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Key:
    def __init__(self,name:str=None,value_key:str='None',action_key:str='None',function:callable=None,app=None) -> None:
        self.name=name
        self.value_key=value_key
        self.action_key=action_key
        self.function=function
        self.app=app
        self.pressed=False
        self.state=False
        
class Mouse:
    button:str='None'
    interval:float=0.1
    def __init__(self,name:str=None,value_key:str='None',function:callable=None,app=None) -> None:
        self.name=name
        self.value_key=value_key
        self.function=function
        self.app=app
        
        self.pressed=False
        self.state=False
        
class Controller:
    def __init__(self,key_list:list[Key]=None,mouse_list:list[Mouse]=None,app:tk.Tk=None):
        from gui import Popup
        self.key_list=key_list
        self.mouse_list=mouse_list
        self.app=app
        
        self.top_level:Popup=None
        
        self.loop_keys:kb.KeyboardEvent=[]
        
        self.abort:bool=False
        self.error:bool=False
        self.keys_running:bool=False
        self.change_state:bool=False
        self.change_key:Key|Mouse=None
        self.change_order:int=None
        
        kb.hook(self.main)
        kb.hook(self.main_change)
        
        self.buttons = {
            'Left Button' : 'left',
            'Right Button' : 'right'
        }
    
    # INPUT LISTENER   
    def  main(self,e:kb.KeyboardEvent):
        if not self.change_state:
            if not self.error:
                if self.keys_running:
                    if e.event_type=='down':
                        for mouse in self.mouse_list:
                            if e.name==mouse.value_key and not mouse.pressed and mouse.state:
                                if mouse.function!=None:
                                    mouse.state=False
                                    thread=threading.Thread(target=lambda:mouse.function(),daemon=True,name=mouse.name)
                                    thread.start()
                                mouse.pressed=True
                if not self.keys_running:
                    if e.event_type=='down':
                        
                        for mouse in self.mouse_list:
                            if e.name==mouse.value_key and not mouse.pressed and not mouse.state:
                                if Mouse.button=='None':
                                    self.messagebox_thread(title='Button Not Selected',message='Please select a button',type='info')
                                elif mouse.function!=None:
                                    mouse.state=True
                                    thread=threading.Thread(target=lambda:mouse.function(),daemon=True,name=mouse.name)
                                    thread.start()
                                mouse.pressed=True
                if self.keys_running:
                    if e.event_type=='down':
                        for key in self.key_list:
                            if e.name==key.value_key and not key.pressed and key.state:
                                if key.function!=None:
                                    key.state=False
                                    thread=threading.Thread(target=lambda:key.function(),daemon=True,name=key.name)
                                    thread.start()
                                key.pressed=True                        
                if not self.keys_running:
                    if e.event_type=='down':
                        for key in self.key_list:
                            if e.name==key.value_key and not key.pressed and not key.state:
                                if key.function!=None:
                                    key.state=True
                                    thread=threading.Thread(target=lambda:key.function(),daemon=True,name=key.name)
                                    thread.start()
                                key.pressed=True
            if e.event_type=='up':
                for key in self.key_list:
                    if e.name==key.value_key and key.pressed:
                        key.pressed=False
                for mouse in self.mouse_list:
                    if e.name==mouse.value_key and mouse.pressed:
                        mouse.pressed=False
    
    # CHANGING BUTTONS FUNCTIONS
    
    def main_change(self,e:kb.KeyboardEvent):
        if self.change_state:
            if e.event_type=='down' and not self.change_key.pressed and not self.error:
                self.abort=False
                abort_key=None
                for key in self.key_list:
                    if self.change_key!=key and e.name==key.value_key and self.change_order==1:
                        abort_key=key
                        self.abort=True
                for mouse in self.mouse_list:
                    if self.change_key!=mouse and e.name==mouse.value_key and self.change_order==1:
                        abort_key=mouse
                        self.abort=True
                if self.abort:
                    self.change_key.pressed=True
                    self.messagebox_thread(title='Error',message="You tried to attribute the same value to "+ self.change_key.name+ " as "+ abort_key.name+"'s value!",type='error')
                elif not self.abort:
                    self.change_key.pressed=True
                    if self.change_order==1:
                        self.change_key.value_key=e.name
                        print('Changed value for '+self.change_key.name+' value in '+e.name)
                    elif self.change_order==2:
                        self.change_key.action_key=e.name
                        print('Changed value for '+self.change_key.name+' action in '+e.name)
                    self.app.keyboard_menu.update_vars()
                    self.app.mouse_menu.update_vars()
                    self.top_level.destroy()
            if e.event_type=='up' and self.change_key.pressed:
                self.change_key.pressed=False
                if not self.abort:
                    self.change_state=False
                        
    def change_init(self,key:Key|Mouse,value:str):
        if not self.keys_running:
            self.change_state=True
            self.change_key=key
            if value=='value':
                self.change_order=1
            elif value=='action':
                self.change_order=2
            else:
                print('Ma ce?')
            self.app.change_window()
        else:
            self.messagebox_thread(title='Running Function Detected',message='Turn off or wait for running function',type='info')
    
    def change_clear(self):
        if self.change_order==1:
            self.change_key.value_key='None'
        elif self.change_order==2: 
            self.change_key.action_key='None'
        else:
            print('HUH?')
        self.change_state=False
        self.app.mouse_menu.update_vars()
        self.app.keyboard_menu.update_vars()
        self.top_level.on_close_toplevel()
        

    def change_cancel(self):
        self.change_state=False
        self.top_level.on_close_toplevel()
        
    # KEYBOARD FUNCTIONS
    
    def repeat_function(self,key:Key):
        if key.action_key=='None': 
            key.state=False
            self.messagebox_thread(title='No Binded Key',message=f'Choose a key for {key.name.upper()} Function',type='info')
        elif key.state:
            self.keys_running=True
            print('Repeat Enabled\n')
            while key.state:
                    kb.press_and_release(key.action_key)
                    time.sleep(0.04)
            self.keys_running=False
            print("Repeat Disabled\n")
    
    def press_function(self,key:Key):
        if key.action_key=='None': 
            key.state=False
            self.messagebox_thread(title='No Binded Key',message=f'Choose a key for {key.name.upper()} Function',type='info')
        elif key.state:
            self.keys_running=True
            kb.press(key.action_key)
            print('Press Enabled\n')
        elif not key.state:
            self.keys_running=False
            kb.release(key.action_key)
            print('Stopped Pressing\n')
        
    def loop_record_init(self,key:Key):
        if key.value_key=='None':
            self.messagebox_thread(title='No Binded Key',message='Cannot proceed to record without having set the Stop Recording Key',type='error')
        elif not self.keys_running:
            thread=threading.Thread(target=self.loop_record,args=(key,),daemon=True)
            thread.start()
        else: 
            self.messagebox_thread(title='Running Function Detected',message='Turn off or wait for running function first',type='error')
            
    def loop_record(self,key:Key):
        self.keys_running=True
        self.loop_keys=kb.record(until=key.value_key)
        self.loop_keys.pop()
        self.keys_running=False
                    
    def loop_play(self,key:Key):
        if len(self.loop_keys)==0:
            key.state=False
            self.messagebox_thread(title='No recorded events',message='Can\'t play because no events have been recorded',type='info')
        elif key.state:
            print('started loop')
            self.keys_running=True
            while key.state:
                
                try:
                    kb.play(self.loop_keys)
                except Exception:
                    key.state=False
                    self.messagebox_thread(title='Weird input',message='There is something wrong with the recorded events. Cleared events!',type='error')
                    self.loop_keys:kb.KeyboardEvent=[]
            self.keys_running=False
            print('stopped loop')
            
    # MOUSE FUNCTIONS
    
    def autoclick(self,mouse:Mouse):
        if mouse.state and Mouse.button!='None':
            self.keys_running=True
            print(f'Clicking {Mouse.button}')
            thread=threading.Thread(target=self.autoclick_thread,args=(mouse,),daemon=True,name='autoclicker-process')
            thread.start()
            while mouse.state:
                time.sleep(0.1)
            print(f'Stopped clicking {Mouse.button}')
            self.keys_running=False
            
    def autoclick_thread(self,mouse:Mouse):
        while mouse.state:
                ms.click(self.buttons[Mouse.button])
                time.sleep(Mouse.interval)
    
    def mouse_press(self,mouse:Mouse):
        if mouse.state and Mouse.button!='None':
            self.keys_running=True
            print(f'Pressing {Mouse.button}')
            ms.press(self.buttons[Mouse.button])
        elif not mouse.state and Mouse.button!='None':
            ms.release(self.buttons[Mouse.button])
            print(f'Released {Mouse.button}')
            self.keys_running=False
        
    # MESSAGE BOX FACTORY
    
    def messagebox_thread(self,title:str,message:str,type:str):
        thread=threading.Thread(target=self.messagebox_create,args=(title,message,type),name=type,daemon=True)
        thread.start()
    
    def messagebox_create(self,title:str,message:str,type:str):
        self.error=True
        if type=='error':
            messagebox.showerror(title=title,message=message)
        elif type=='info':
            messagebox.showinfo(title=title,message=message)
        self.error=False
        
    # CHECKING REPEATED OCCURING VALUES AT READING CONFIGURATION FILE
    
    def are_identical_value_keys(self):
        for index in range(1,len(self.key_list)):
            if  self.key_list[0].value_key==self.key_list[index].value_key and self.key_list[0].value_key!='None':
                    return True
        for index in range(1,len(self.mouse_list)):
            if  self.mouse_list[0].value_key==self.mouse_list[index].value_key and self.mouse_list[0].value_key!='None':
                    return True
        for index_1 in range(len(self.mouse_list)):
            for index_2 in range(len(self.key_list)):
                if self.mouse_list[index_1].value_key == self.key_list[index_2].value_key and self.mouse_list[index_1].value_key!='None':
                    return True
        return False        