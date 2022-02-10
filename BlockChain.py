
from time import time
from  hashlib import sha256 
from math import ceil
from tracemalloc import start


def updatehash (*args):
    hashing_txt ="";h=sha256()
    for arg in args : 
        hashing_txt += str (arg)
        
    h.update(hashing_txt.encode('utf-8'))
    return h.hexdigest()

#print (updatehash("hello world "))

class Block() :
    nonce = 0 
    
    def __init__ (self  ,no, data="" , prev= None ):
        
        self.data = data
        self.no = no 
        if prev is None:
            self.prev = "0" * 64
        else:
            self.prev = prev
      
    def hash (self):
        return updatehash(self.prev , self.no , self.data , self.nonce)
    
        
    def getprev (self,block): 
        return block.prev
     
    def __str__(self): 
        out= f"Block#: {self.no} \n hash: {self.hash()} \n prev:{self.prev} \n data: {self.data} \n nonce: {self.nonce} \n "
        return ("hello")
       

class BlockChain():
    
    equal = 0
    
    def __init__(self):
        self.chain = [] 
        self.num= 0
        self.wait = 0 
        
        
    
    def add(self,block):
        self.num +=1
      
          
        self.chain.append({
            'hash':block.hash(), 
            'prev':block.prev,
            'no':block.no,
            'data':block.data ,
            'nonce':block.nonce
            
            })

        if(self.wait == 1 ):
            self.wait = 0   
            globalchain.chain.append({
            'hash':block.hash(), 
            'prev':block.prev,
            'no':block.no,
            'data':block.data ,
            'nonce':block.nonce
            
            })
            
    
    def get_length (self  ):
        return self.num ;    
    
    
    def pop(self):
        self.chain.remove(self.chain[-1])
        
        
        
    def mine (self,block,speed):
        
        self.diffculty=1
        try:
            block.prev=self.chain[-1].get('hash')
        except IndexError:
            pass
        
        latestnonce=None
        rate =-1
        stime= time()
        found = 0
        while True: 
        
            if block.hash ()[: self.diffculty]== "0"* self.diffculty:
            #sol. Found
                # print (rate)
                found=1
                latestnonce=block.nonce
            else:
                block.nonce += 1
            rate = time()-stime
          
            if (rate> speed):
                self.diffculty -=1
                block.nonce=latestnonce
                self.add(block)
                break
                #take it as it's
            elif(rate < speed and found):
                self.diffculty += 1
                found=0
                # stime= time() #reset timer
                continue
            if (found):
                block.nonce=latestnonce
                self.add(block)
                break
            
    
    def max_chain (chain1, *args):
        mem =0 
        same = 0 
        # print("hiiiiiiiiiiiiiiiiiii")
        for arg in args :
            
            if len(chain1.chain)< len(arg.chain):
                chain1 = arg
                equal = 0
                mem =1
                # print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                #for block in chain1.chain:
                #    print (block)
                
            if len(chain1.chain)==len(arg.chain) and mem == 0 :
                equal =1 
                
                for i, j  in zip(chain1.chain,arg.chain):

                    if i == j :
                        same=1 
                    else :
                        same =0 
                        chain1.wait =1
                        arg.wait = 1  
                           
        
              
                
                
        if equal == 0 and mem == 1: 
            return chain1 
        elif same == 1:
            return chain1 
        else:
            return "no chain yet" 


def sim_51_attack(chain,percent=51):
    n=5
    
    networkspeed =1
    att_speed = (percent/(100-percent)*networkspeed)
    current_chain= chain.chain
    
    attacker=BlockChain()
    attacker.chain=current_chain[:-1]
    attacker_data="attacker"
    miner=BlockChain()
    miner.chain=current_chain
    miner_data="mine"
    attacker.mine(Block(current_chain[-1].get('no'),data=attacker_data),1/att_speed)


    if(len(current_chain)>=2):
        # j=1
        # threshold=ceil( (percent/100)*n )
        for i in range(1,n+1): # 1--->50
            starttime= time()   #start timer

            attacker.mine(Block(attacker.chain[-1].get('no')+1,data=attacker_data),1/att_speed)
            attacktime = time()-starttime
            starttime= time()   #reset timer

            miner.mine(Block((miner.chain[-1].get('no')+1),data=miner_data),networkspeed)
            networktime = time()-starttime

            if (attacktime<networktime):
                miner.pop()
            else :
                attacker.pop()
        chain= chain.max_chain (chain,attacker,miner)

        # print chain after attack :
        for block in chain.chain:
            print (f"Block#: {block['no']}, Data: {block['data']}, Hash:{block['hash'][:10]},prev:{block['prev'][:10]}, Nonce: {block['nonce']}\n")
        if(len(chain.chain) == len(attacker.chain)):
            print(f"Attack worked\nAttackSpeed={att_speed} Blockpersecond\n" )
        
        elif(len(chain.chain)>len(attacker.chain)):
            print(f"attack failed\nAttackSpeed={att_speed} Blockpersecond\n")

        

globalchain = BlockChain()

#for testing purposes
def main():
    # blockchain = BlockChain()
    database = ["12", "13", "17", "16","18"]

    num = 0
    for data in database:
        num += 1
        globalchain.mine(Block(num, data=data),0.5)


    sim_51_attack(globalchain,51)



if __name__ == '__main__':
    main()
