#import tkinter as tk
#from tkinter import ttk
import customtkinter as ctk
from configuration import SaveConfig
from control import Key,Controller


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')        
class App(ctk.CTk):
    
    def __init__(self,save:SaveConfig=None,controller:Controller=None,key_list:list[Key]=None):
        
        super().__init__()
        
        self.save=save
        self.controller=controller
        self.key_list=key_list
    
        self.menu=MainMenu(parent=self,controller=self.controller)
        self.top_level:Popup=None
        
        self.style_window()
        self.menu.app_create_buttons()
        self.protocol("WM_DELETE_WINDOW",  self.on_close_main)
        
    def style_window(self):
        self.title('RClicker')
        self.width=500
        self.height=500
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        self.geometry(f'{self.width}x{self.height}+{(screen_width-self.width)//2}+{(screen_height-self.height)//2}')
        self.resizable(False,False)
    
    def change_window(self):
            current_x=self.winfo_x()
            current_y=self.winfo_y()
            self.top_level=Popup(main_window=self,title="Choose value",controller=self.controller,width=300,height=40,main_x=current_x,main_y=current_y)
            self.controller.top_level=self.top_level
            
    def on_close_main(self): 
        self.save.write_config()
        self.destroy()
        
class Popup(ctk.CTkToplevel):
    def __init__(self,main_window:App=None,title:str=None,controller:Controller=None,width=None,height=None,main_x=None,main_y=None):
        super().__init__()
        self.main_window=main_window
        self.title(title)
        self.controller=controller
        self.width=width
        self.height=height
        main_x=main_x
        main_y=main_y
        self.menu=TopLevelMenu(parent=self,controller=self.controller)
    
        # STYLING
        xpos=main_x+(main_window.width-self.width)//2
        ypos=main_y+(main_window.height-self.height)//2
        self.style_window(width=width,height=height,x=xpos,y=ypos)
        self.menu.toplevel_create_button()
        self.protocol("WM_DELETE_WINDOW",  self.on_close_toplevel)        
        
    def  style_window(self,width,height,x,y):
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False,False)
        self.positionfrom('program')
        self.grab_set()
    
    def on_close_toplevel(self):
        self.controller.change_state=False
        self.destroy()

class MainMenu(ctk.CTkFrame):
    def __init__(self,parent:App,controller:Controller=None):
        super().__init__(master=parent)
        self.parent=parent
        self.controller=controller
        
        self.pack(expand=True,fill='both')
              
    def app_create_buttons(self):
            self.repeat_value_var=ctk.StringVar(value=self.parent.key_list[0].value_key)
            self.repeat_action_var=ctk.StringVar(value=self.parent.key_list[0].action_key)
            self.press_value_var=ctk.StringVar(value=self.parent.key_list[1].value_key)
            self.press_action_var=ctk.StringVar(value=self.parent.key_list[1].action_key)
            
            self.columnconfigure((0,1,2,3,4,5,6,7,8),weight=2,uniform='a')
            self.rowconfigure((0,1,2,3,4,5,6,7,8),weight=1,uniform='a')

            self.header_font=ctk.CTkFont(family='Calibri',size=30,weight='bold')
            self.normal_font=ctk.CTkFont(family='Calibri',size=25,weight='normal')
            self.value_font=ctk.CTkFont(family='Calibri',size=25,weight='bold')
            #  REPEAT FUNCTION LABELS
            
            self.repeat_function_label=ctk.CTkLabel(master=self,text='Repeat Function',font=self.header_font).grid(row=0,column=0,columnspan=5,sticky='we')
            self.repeat_label_1=ctk.CTkLabel(master=self,text='Value',font=self.normal_font).grid(row=1,column=0,columnspan=2,sticky='we')
            self.repeat_label_2=ctk.CTkLabel(master=self,text='Action',font=self.normal_font).grid(row=1,column=4,columnspan=2,sticky='we')
            
            # PRESS FUNCTION LABELS
            self.press_function_label=ctk.CTkLabel(master=self,text='Press Function',font=self.header_font).grid(row=2,column=0,columnspan=5,sticky='we')
            self.press_label_1=ctk.CTkLabel(master=self,text='Value',font=self.normal_font).grid(row=3,column=0,columnspan=2,sticky='we')
            self.press_label_2=ctk.CTkLabel(master=self,text='Action',font=self.normal_font).grid(row=3,column=4,columnspan=2,sticky='we')
            
            # REPEAT FUNCTION BUTTONS
            self.repeat_value=ctk.CTkButton(master=self,
                                            font=self.value_font,
                                            textvariable=self.repeat_value_var, 
                                            command=lambda: self.controller.change_init(key=self.parent.key_list[0],value='value')).grid(row=1,column=2,columnspan=2,sticky='w')
            
            self.repeat_action=ctk.CTkButton(master=self,
                                             font=self.value_font,
                                             textvariable=self.repeat_action_var,
                                             command=lambda: self.controller.change_init(key=self.parent.key_list[0],value='action')).grid(row=1,column=6,columnspan=2,sticky='w')
            
            # PRESS FUNCTION BUTTONS
            self.press_value=ctk.CTkButton(master=self,
                                           font=self.value_font,
                                           textvariable=self.press_value_var,
                                           command=lambda: self.controller.change_init(key=self.parent.key_list[1],value='value')).grid(row=3,column=2,columnspan=2,sticky='w')
            
            self.press_action=ctk.CTkButton(master=self,
                                            font=self.value_font,
                                            textvariable=self.press_action_var,
                                            command=lambda: self.controller.change_init(key=self.parent.key_list[1],value='action')).grid(row=3,column=6,columnspan=2,sticky='w')
        
    def update_vars(self):
        self.repeat_value_var.set(value=self.parent.key_list[0].value_key)
        self.repeat_action_var.set(value=self.parent.key_list[0].action_key)
        self.press_value_var.set(value=self.parent.key_list[1].value_key)
        self.press_action_var.set(value=self.parent.key_list[1].action_key)

class TopLevelMenu(ctk.CTkFrame):
    def __init__(self,parent:Popup,controller:Controller=None):
        super().__init__(master=parent)
        self.parent=parent
        self.controller=controller
        self.pack()
    
    def toplevel_create_button(self):
        self.header_font=ctk.CTkFont(family='Calibri',size=20,weight='bold')
        self.normal_font=ctk.CTkFont(family='Calibri',size=20,weight='normal')
        
        self.clear=ctk.CTkButton(master=self,text='Clear',
                                 font=self.header_font,
                                 command=lambda: self.controller.change_clear()).grid(row=0,column=0,padx=5,pady=5)
        self.cancel=ctk.CTkButton(master=self,
                                  text='Cancel',
                                  font=self.header_font,
                                  command=lambda: self.controller.change_cancel()).grid(row=0,column=1,padx=5,pady=5)