from control import Key,Mouse,Controller

from gui import App

from configuration import SaveConfig
 
if __name__=='__main__':
    
    controller=Controller()
    
    repeat=Key(name='repeat',function=lambda:controller.repeat_function(key=repeat))
    press=Key(name='press',function=lambda: controller.press_function(key=press))
    loop=Key(name='loop',function=lambda:controller.loop_play(key=loop))
    stop_record=Key(name='stop_record')
    autoclick=Mouse(name='autoclick',function=lambda: controller.autoclick(mouse=autoclick))
    mouse_hold=Mouse(name='mouse hold',function=lambda: controller.mouse_press(mouse=mouse_hold))
    key_list=[repeat,press,loop,stop_record]
    mouse_list=[autoclick,mouse_hold]
    
    #  CONFIGURATION
    save=SaveConfig(key_list=key_list,mouse_list=mouse_list)
    save.read_config()
    
    if Mouse.interval <0.001:
        Mouse.interval=0.1
    
    
    frame=App(save=save,controller=controller,key_list=key_list,mouse_list=mouse_list)
    
    controller.key_list=key_list
    controller.mouse_list=mouse_list
    controller.app=frame
    
    if controller.are_identical_value_keys():
        print("Enable value keys for different keys should not be the same. Changing all to to None")
        for key in key_list: 
            key.value_key='None'
        for mouse in mouse_list:
            mouse.value_key='None'
            
    
    # INSTRUCTIONS
    if repeat.value_key!='None' and repeat.action_key!='None':
        print(f"Press {repeat.value_key.upper()} to keep pressing and releasing {repeat.action_key.upper()}!")  
    if press.value_key!='None' and press.action_key!='None':    
        print(f"Press {press.value_key.upper()} to keep pressing {press.action_key.upper()}!\n")
    
    frame.mainloop()