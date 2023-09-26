import time
import threading
import keyboard as kb
import mouse as ms
# import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
import customtkinter as ctk

class Key:
    def __init__(self,name:str=None,value_key:str='None',action_key:str='None',function:callable=None,app=None) -> None:
        self.name=name
        self.value_key=value_key
        self.action_key=action_key
        self.function=function
        self.app=app
        self.pressed=False
        self.state=False
    
class Controller:
    
    def __init__(self,key_list:list[Key]=None,app:ctk.CTk=None):
        from gui import Popup
        self.key_list=key_list
        self.app=app
        
        self.top_level:Popup=None
    
        self.change_state:bool=False
        self.change_key:Key=None
        self.change_order:int=None
        kb.hook(self.main)
        kb.hook(self.main_change)
        
    def are_identical_value_keys(self):
        for index in range(1,len(self.key_list)):
            if  self.key_list[0].value_key==self.key_list[index].value_key and self.key_list[0].value_key!='None':
                    return True
        return False
    
    def  main(self,e:kb.KeyboardEvent):
        if not self.change_state:
            if e.event_type=='down':
                for key in self.key_list:
                    if e.name==key.value_key and not key.pressed:
                        key.pressed=True
                        key.state= not key.state
                        x=threading.Thread(target=lambda:key.function(),daemon=True,name=key.name)
                        x.start()
            elif e.event_type=='up':
                for key in self.key_list:
                    if e.name==key.value_key and key.pressed:
                        key.pressed=False     

    def main_change(self,e:kb.KeyboardEvent):
        if self.change_state:
            abort=False
            if(e.event_type=='down'):
                for key in self.key_list:
                    if self.change_key!=key and e.name==key.value_key and self.change_order==1:
                        print("You tried to attribute the same value to "+ self.change_key.name+ " as "+ key.name+"'s value! REFUSED")
                        messagebox.showerror('Error',"You tried to attribute the same value to "+ self.change_key.name+ " as "+ key.name+"'s value!")
                        abort=True
                if not abort:
                    if self.change_order==1:
                        self.change_key.value_key=e.name
                        print('Changed value for '+self.change_key.name+' value in '+e.name)
                    elif self.change_order==2:
                        self.change_key.action_key=e.name
                        print('Changed value for '+self.change_key.name+' action in '+e.name)
                    self.change_state=False
                    self.app.menu.update_vars()
                    self.top_level.on_close_toplevel()

            
    
    def change_init(self,key:Key,value:str):
        self.change_key=key
        if value=='value':
            self.change_order=1
        elif value=='action':
            self.change_order=2
        else:
            print('Ma ce?')
        self.change_state=True
        self.app.change_window()
    
    def change_clear(self):
        if self.change_order==1:
            self.change_key.value_key='None'
        elif self.change_order==2: 
            self.change_key.action_key='None'
        else:
            print('HUH?')
        self.top_level.on_close_toplevel()
        self.app.menu.update_vars()

    def change_cancel(self):
        self.top_level.on_close_toplevel()
        
        
            
    def repeat_function(self,key:Key):
        if key.state and key.action_key!='None':
            print('Repeat Enabled\n')
            while key.state and not self.change_state:
                    kb.press_and_release(key.action_key)
                    time.sleep(0.04)
            print("Repeat Disabled\n")
    
    def press_function(self,key:Key):
        if key.state and key.action_key!='None':
            kb.press(key.action_key)
            print('Press Enabled\n')
        elif key.action_key!='None':
            kb.release(key.action_key)
            print('Stopped Pressing\n')
            
    