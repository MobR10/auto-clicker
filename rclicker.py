from control import Key,Controller

from gui import App

from configuration import SaveConfig
 
if __name__=='__main__':
    
    controller=Controller()
    
    repeat=Key(name='repeat',function=lambda:controller.repeat_function(key=repeat))
    press=Key(name='press',function=lambda: controller.press_function(key=press))
    enable_keys=[repeat,press]
    
    
    #  CONFIGURATION
    save=SaveConfig(enable_keys)
    save.read_config()
    
    frame=App(save=save,controller=controller,key_list=enable_keys)
    
    controller.key_list=enable_keys
    controller.app=frame
    
    if controller.are_identical_value_keys():
        print("Enable value keys for different keys should not be the same. Changing all to to None")
        for Key in enable_keys:
            Key.value_key='None'
    
    # INSTRUCTIONS
    if repeat.value_key!='None' and repeat.action_key!='None':
        print(f"Press {repeat.value_key.upper()} to keep pressing and releasing {repeat.action_key.upper()}!")  
    if press.value_key!='None' and press.action_key!='None':    
        print(f"Press {press.value_key.upper()} to keep pressing {press.action_key.upper()}!\n")
    
    frame.mainloop()
   
