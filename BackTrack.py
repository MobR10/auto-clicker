
import time
class BackTrack:
    
    def combine(self, n:int,k:int,list:list)-> list[list[str]] :
        res=[]
        
        def backtrack(start:int,comb:list):
            if len(comb)==k:
                res.append(comb.copy())
                return
            
            for i in range(start,n):
                comb.append(list[i])
                backtrack(i+1,comb)
                comb.pop()
        backtrack(0,[])
        return res
    
    def key_list(self,list:list):
        time.sleep(1)
        for i in range(1,len(list)+1):
            print(self.combine(n=len(list),k=i,list=list))
            print('')