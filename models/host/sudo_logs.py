from datetime import datetime
import json

def format_sudo_command(line:str):
    user=''
    command=''
    dir=''
    data={}
    time=''
    i=0
    while (line[i]!=' '):
        time=time+line[i]
        i=i+1
    data['timestamps']=time

    i=line.index('sudo:')+5
    while( line[i]!=':' ):
        if (line[i]!=' '):
            user=user+line[i]
        i=i+1
    i=line.index('PWD=')+4
    while( line[i]!=';' ):
        if (line[i]!=' '):
            dir=dir+line[i]
        i=i+1
    i=line.index('COMMAND')+8
    while( i<len(line)-1 ):
       
        command=command+line[i]
        i=i+1
    data['event_type']='sudo command'
    data['user']=user
    data['command']=command
    data['directory']=dir
    print(json.dumps(data))
    
            
    
    
     
        
            


