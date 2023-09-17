class Keys:
    
    def __init__(self,name:str,description:str,state:bool,function) -> None:
        self.name=name
        self.description=description
        self.state=state
        self.function=function
        
        self.value='None'
        self.pressed=False