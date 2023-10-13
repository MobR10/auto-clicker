import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import customtkinter  as ctk




from configuration import SaveConfig
from control import Key,Mouse,Controller
    
class App(tk.Tk):
    
    def __init__(self,save:SaveConfig=None,controller:Controller=None,key_list:list[Key]=None,mouse_list:list[Mouse]=None):
        
        super().__init__()
        
        self.save=save
        self.controller=controller
        self.key_list=key_list
        self.mouse_list=mouse_list
        
        self.theme=ttk.Style()
        self.theme.theme_use('clam')

        self.style_window()
        self.styles=self.create_fonts_and_styles()
        
        self.full_menu=FullMenu(parent=self,controller=self.controller,key_list=self.key_list,mouse_list=self.mouse_list)
        
        self.keyboard_menu=self.full_menu.keyboard_menu
        self.mouse_menu=self.full_menu.mouse_menu
        
        
        self.top_level:Popup=None
        
        

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
    
    def create_fonts_and_styles(self):
        self.button_font=Font(family='Playfair',size=11,weight='bold')
        self.combobox_font=Font(family='Playfair',size=20,weight='bold')
        self.label_header_font=Font(family='Playfair',size=20,weight='bold')
        self.label_body_font=Font(family='Playfair',size=16,weight='normal')
    
        self.button_style=ttk.Style().configure("custom.TButton",font=self.button_font)
        self.optionmenu_style=ttk.Style().configure('combobox.TButton',font=self.combobox_font)
        self.label_header_style=ttk.Style().configure('header.TLabel',font=self.label_header_font)
        self.label_body_style=ttk.Style().configure('body.TLabel',font=self.label_body_font)
        
        return [self.button_style,self.optionmenu_style,self.label_header_style,self.label_body_style]
        
        
class Popup(tk.Toplevel):
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
        self.grab_set()
    
    def on_close_toplevel(self):
        self.controller.change_state=False
        self.destroy()

class FullMenu(ttk.Notebook):
    def __init__(self,parent:App,controller:Controller=None,key_list:list[Key]=None,mouse_list:list[Mouse]=None):
        super().__init__(master=parent,takefocus=0)
        self.parent=parent
        self.controller=controller
        self.key_list=key_list
        self.mouse_list=mouse_list
        
        self.enable_traversal()
        
        self.keyboard_menu=KeyboardMenu(parent=self,controller=self.controller)
        self.keyboard_menu.create_buttons()
        
        self.keyboard_menu.pack(expand=True,fill='both')
        
        self.mouse_menu=MouseMenu(parent=self,controller=self.controller)
        self.mouse_menu.create_buttons()
        
        self.mouse_menu.pack(expand=True,fill='both')
        
        self.add(self.keyboard_menu,text='Keyboard Functions')
        self.add(self.mouse_menu,text='Mouse Functions')
        

        self.pack(expand=True,fill='both')
        
class MouseMenu(ttk.Frame):
    def __init__(self,parent:FullMenu,controller:Controller=None):
        super().__init__(master=parent)
        self.parent=parent
        self.controller=controller
        
        self.pack(expand=True,fill='both')
    
    def choose_button(self,e):
        key=self.button_combobox.get()
        self.button_var.set(value=key)
        Mouse.button=key
        self.parent.parent.focus_set()
        
    def set_interval(self):
        interval=self.interval_entry.get()
        try:
            Mouse.interval=float(interval)
            self.interval_var.set(value=interval)
        except ValueError:
            print('Nu ai introdus un numar')
            self.interval_var.set(value=Mouse.interval)
        
        self.parent.parent.focus_set()
        
    def update_vars(self):
        self.autoclick_value_var.set(value=self.parent.mouse_list[0].value_key)
        self.hold_value_var.set(value=self.parent.mouse_list[1].value_key)
        
    def  create_buttons(self):
        
        self.autoclick_value_var=tk.StringVar(value=self.parent.mouse_list[0].value_key)
        self.hold_value_var=tk.StringVar(value=self.parent.key_list[1].value_key)
        self.button_var=tk.StringVar(value=Mouse.button)
        self.interval_var=tk.StringVar(value=Mouse.interval)

        # self.columnconfigure((0,1,2,3,4,5,6,7,8),weight=1,uniform='a')
        # self.rowconfigure((0,1,2,3,4,5,6,7,8),weight=1,uniform='a')
        
        self.autoclick_function_label=ttk.Label(master=self,text='Mouse Autoclick Function',style='header.TLabel').grid(row=0,column=0,columnspan=5,sticky='we')
        self.autoclick_label_1=ttk.Label(master=self,text='Enable/Disable',style='body.TLabel').grid(row=1,column=0,columnspan=2,sticky='we')
        
        self.autoclick_label_2=ttk.Label(master=self,text='Interval (sec)',style='body.TLabel').grid(row=2,column=0,sticky='we')
        
        self.interval_entry=ttk.Entry(master=self,textvariable=self.interval_var,justify='center',takefocus=False)
        
        self.interval_entry.grid(row=2,column=2)
        
        self.b=ttk.Button(master=self,text='Submit Interval',takefocus=False,style='custom.TButton',command=self.set_interval).grid(row=2,column=3,padx=5)
        
        
        
        
        self.autoclick_button=ttk.Button(master=self,
                                         takefocus=0,
                                         style='custom.TButton',
                                         textvariable=self.autoclick_value_var, 
                                         command=lambda:self.controller.change_init(key=self.parent.mouse_list[0],value='value')).grid(row=1,column=2)
        
        self.press_function_label=ttk.Label(master=self,text='Mouse Hold Function',style='header.TLabel').grid(row=3,column=0,columnspan=5,sticky='we')
        self.press_label_1=ttk.Label(master=self,text='Enable/Disable',style='body.TLabel').grid(row=4,column=0,columnspan=2,sticky='we')
        
        self.autoclick_button=ttk.Button(master=self,
                                         takefocus=0,
                                         style='custom.TButton',
                                         textvariable=self.hold_value_var,
                                         command=lambda:self.controller.change_init(key=self.parent.mouse_list[1],value='value')).grid(row=4,column=2)
        
        self.choose_button_label=ttk.Label(master=self,text='Choose button',style='header.TLabel').grid(row=5,column=0,columnspan=2)
        self.button_combobox=ttk.Combobox(master=self,state='readonly',takefocus=0,textvariable=self.button_var,values=['Left Button','Right Button'],justify='center',style='custom.TCombobox')
        self.button_combobox.bind("<<ComboboxSelected>>",self.choose_button)
        self.button_combobox.grid(row=6,column=0,columnspan=2,sticky='we')
            
        
    
class KeyboardMenu(ttk.Frame):
    def __init__(self,parent:FullMenu,controller:Controller=None):
        super().__init__(master=parent)
        self.parent=parent
        self.controller=controller
        
        
        
        self.pack(expand=True,fill='both')      
              
    def create_buttons(self):
            self.repeat_value_var=tk.StringVar(value=self.parent.key_list[0].value_key)
            self.repeat_action_var=tk.StringVar(value=self.parent.key_list[0].action_key)
            self.press_value_var=tk.StringVar(value=self.parent.key_list[1].value_key)
            self.press_action_var=tk.StringVar(value=self.parent.key_list[1].action_key)
            self.loop_start_stop_var=tk.StringVar(value=self.parent.key_list[2].value_key)
            self.loop_stop_record_var=tk.StringVar(value=self.parent.key_list[3].value_key)
            
            self.columnconfigure((0,1,2,3),weight=1,uniform='a')
            self.rowconfigure((0,1,2,3,4,5,6,7,8),weight=1,uniform='a')
        
            #  REPEAT FUNCTION LABELS
            
            self.repeat_function_label=ttk.Label(master=self,text='Repeat Function',style='header.TLabel').grid(row=0,column=0,columnspan=5,sticky='we')
            self.repeat_label_1=ttk.Label(master=self,text='Enable/Disable',style='body.TLabel').grid(row=1,column=0,columnspan=2,sticky='we')
            self.repeat_label_2=ttk.Label(master=self,text='Key to Press',style='body.TLabel').grid(row=1,column=4,columnspan=2,sticky='we')
            
            # PRESS FUNCTION LABELS
            self.press_function_label=ttk.Label(master=self,text='Press Function',style='header.TLabel').grid(row=2,column=0,columnspan=5,sticky='we')
            self.press_label_1=ttk.Label(master=self,text='Enable/Disable',style='body.TLabel').grid(row=3,column=0,columnspan=2,sticky='we')
            self.press_label_2=ttk.Label(master=self,text='Key to Press',style='body.TLabel').grid(row=3,column=4,columnspan=2,sticky='we')
            
            # REPEAT FUNCTION BUTTONS
            self.repeat_value=ttk.Button(master=self, 
                                        style='custom.TButton',
                                        takefocus=0,
                                        textvariable=self.repeat_value_var, 
                                        command=lambda: self.controller.change_init(key=self.parent.key_list[0],value='value')).grid(row=1,column=2,columnspan=2)
            
            self.repeat_action=ttk.Button(master=self,
                                        style='custom.TButton',
                                        takefocus=0,
                                        textvariable=self.repeat_action_var,
                                        command=lambda: self.controller.change_init(key=self.parent.key_list[0],value='action')).grid(row=1,column=6,columnspan=2)
            
            # PRESS FUNCTION BUTTONS
            self.press_value=ttk.Button(master=self,
                                        style='custom.TButton',
                                        takefocus=0,
                                        textvariable=self.press_value_var,
                                        command=lambda: self.controller.change_init(key=self.parent.key_list[1],value='value')).grid(row=3,column=2,columnspan=2)
            
            self.press_action=ttk.Button(master=self,
                                        style='custom.TButton',
                                        takefocus=0,
                                        textvariable=self.press_action_var,
                                        command=lambda: self.controller.change_init(key=self.parent.key_list[1],value='action')).grid(row=3,column=6,columnspan=2)
            
            self.loop_function_label=ttk.Label(master=self,style='header.TLabel',text='Loop Function').grid(row=4,column=0,columnspan=5,sticky='we')
            self.loop_label_1=ttk.Label(master=self,style='body.TLabel',text='Play/Stop').grid(row=5,column=0,columnspan=3,sticky='we')
            self.loop_label_2=ttk.Label(master=self,style='body.TLabel',text='Stop Recording').grid(row=6,column=0,columnspan=3,sticky='we')
            
            self.loop_value=ttk.Button(master=self,
                                        style='custom.TButton',
                                        takefocus=0,
                                        textvariable=self.loop_start_stop_var,
                                        command=lambda:self.controller.change_init(key=self.parent.key_list[2],value='value')).grid(row=5,column=3,columnspan=2,padx=25)
            self.stop_record_value=ttk.Button(master=self,
                                            style='custom.TButton',
                                            takefocus=0,
                                            textvariable=self.loop_stop_record_var,
                                            command=lambda:self.controller.change_init(key=self.parent.key_list[3],value='value')).grid(row=6,column=3,columnspan=2,padx=25)
            self.loop_record=ttk.Button(master=self,
                                        style='custom.TButton',
                                        takefocus=0,
                                        text='Record',
                                        command=lambda:self.controller.loop_record_init(key=self.parent.key_list[3])).grid(row=7,column=0,columnspan=9,sticky='we',padx=5)
        
    def update_vars(self):
        self.repeat_value_var.set(value=self.parent.key_list[0].value_key)
        self.repeat_action_var.set(value=self.parent.key_list[0].action_key)
        self.press_value_var.set(value=self.parent.key_list[1].value_key)
        self.press_action_var.set(value=self.parent.key_list[1].action_key)
        self.loop_start_stop_var.set(value=self.parent.key_list[2].value_key)
        self.loop_stop_record_var.set(value=self.parent.key_list[3].value_key)

class TopLevelMenu(ttk.Frame):
    def __init__(self,parent:Popup,controller:Controller=None):
        super().__init__(master=parent)
        self.parent=parent
        self.controller=controller
        self.pack()
    
    def toplevel_create_button(self):
        self.clear=ttk.Button(master=self,
                                takefocus=0,
                                style='custom.TButton',
                                text='Clear',
                                command=lambda: self.controller.change_clear()).grid(row=0,column=0,padx=5,pady=5)
        self.cancel=ttk.Button(master=self,
                                takefocus=0,
                                style='custom.TButton',
                                text='Cancel',
                                command=lambda: self.controller.change_cancel()).grid(row=0,column=1,padx=5,pady=5)