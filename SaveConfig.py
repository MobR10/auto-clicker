import os
"""This class is responsible for handling the reading and writing the configuration for the buttons.
     
"""
class SaveConfig:
     
     def __init__(self,*buttons:tuple) -> None:
          self.buttons=buttons
          
     def read_config(self):
          if os.path.exists(os.getcwd()+'\\config.txt'):
               with open('config.txt','r') as file:
                    for button in self.buttons:
                         line=file.readline()
                         button.value=line[line.index('=')+1:].strip()
                         
    
     def write_config(self):
         with open('config.txt','w') as file:
              for button in self.buttons:
                   file.write(button.name+'='+button.value+'\n')