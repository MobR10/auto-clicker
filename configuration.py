import os

from control import Key
"""This class is responsible for handling the reading and writing the configuration for the buttons.
     
"""
class SaveConfig:
     
     def __init__(self,key_list:list[Key]=None) -> None:
          self.key_list=key_list
          
     def read_config(self):
          try:
               if os.path.exists(os.getcwd()+'\\config.txt'):
                    with open('config.txt','r') as file:
                         for key in self.key_list:
                              line=file.readline()
                              key.value_key=line[line.index('=')+1:].strip()
                              line=file.readline()
                              key.action_key=line[line.index('=')+1:].strip()
          except ValueError:
               print('Fisierul nu contine ce trebuie, mai bine il stergi, daca nu stii ce trebuie sa aiba inauntru!')
                         
    
     def write_config(self):
         with open('config.txt','w') as file:
              for key in self.key_list:
                   file.write(key.name+' Value Key='+key.value_key+'\n')
                   file.write(key.name+' Action Key='+key.action_key+'\n')