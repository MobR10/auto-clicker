import os
from control import Key,Mouse
"""This class is responsible for handling the reading and writing the configuration for the buttons.
     
"""
class SaveConfig:
     
     def __init__(self,key_list:list[Key]=None,mouse_list:list[Mouse]=None) -> None:
          self.key_list=key_list
          self.mouse_list=mouse_list
          
     def read_config(self):
          try:
               if os.path.exists(os.getcwd()+'\\config.txt'):
                    with open('config.txt','r') as file:
                         for key in self.key_list:
                              line=file.readline()
                              key.value_key=line.split('=')[1].strip()
                              if not key==self.key_list[2] and not key==self.key_list[3]:
                                   line=file.readline()
                                   key.action_key=line.split('=')[1].strip()
                         for mouse in self.mouse_list:
                              line=file.readline()
                              mouse.value_key=line.split('=')[1].strip()
                         line=file.readline()
                         Mouse.button=line.split('=')[1].strip()
                         line=file.readline()
                         Mouse.interval=float(line.split('=')[1].strip())
          except ValueError:
               print('Fisierul nu contine ce trebuie, mai bine il stergi, daca nu stii ce trebuie sa aiba inauntru!')
          except Exception:
               print('Ceva nu e bine cu fisierul')
                         
    
     def write_config(self):
         with open('config.txt','w') as file:
               for key in self.key_list:
                    file.write(f'[{key.name}] value key={key.value_key}\n')
                    if not key==self.key_list[2] and not key==self.key_list[3]:
                         file.write(f'[{key.name}] action key={key.action_key}\n')
               for mouse in self.mouse_list:
                    file.write(f'[{mouse.name}] value key={mouse.value_key}\n')
               file.write(f'[mouse button]={Mouse.button}')
               file.write('\n')
               file.write(f'[mouse interval]={Mouse.interval}')