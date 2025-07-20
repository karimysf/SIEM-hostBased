from loguru import logger
from datetime import datetime
import time
import json
from models.host.sudo_logs import format_sudo_command
import subprocess


#table for keeping track of already failed attemprs users
failed_hosts = {}

#monitoring all logs after service started
def read_logs_from_now(filepath:str):
    with open(filepath) as log:
        log.seek(0,2)
        while True:
            line = log.readline()
            if not line:
                time.sleep(0.2)
            else : 
                yield line 
                
#reads ssh aut.log and formats lines for later use   

def monitor_auth_logs():
 
    print(f"Starting [SSH-LOGIN] monitoring :{datetime.now()}")
    for line in read_logs_from_now("/var/log/auth.log"):
        print(line)
        if line.__contains__('session') and (line.__contains__('opened') or (line.__contains__('closed') )):
            monitor_sessions(line)
        elif (line.__contains__('sshd') and (line.__contains__('Accepted') or line.__contains__('Failed') )):
         get_info_from_ssh_auth(line)
        elif (line.__contains__('sudo')):
            format_sudo_command(line)

        
    
        
    


#handling ssh key exchange 
def get_info_from_ssh_auth(line:str):
    line =line.split(' ')
    n =len(line )-1
    data={}
    data['timestamp']=line[0]   

    for i in range(1,n) :
        
        if line[i]=='Accepted' or line[i]=='Failed':

            if i<n-2 and (line[i+1]=='password' or line[i+1]=='publickey'):
               j=i
               auth_method=line[i+1]
               result=line[i]
               while j<n:
                   if line[j]=='for' :
                       if line[j+1]=='user':
                           host=line[j+2]
                       else :
                           host=line[j+1]
                       
                       break
                   j=j+1
               while j<n:
                   if line[j]=='from':
                       ip=line[j+1]
                       break
                   j=j+1
               
                   
                  
               
                    
               data['event_type'] ='ssh-autentification-attempt'
               if result=='Failed':
                   failed_hosts[host]=failed_hosts.get(host,0) +1
                   data['Attempts:']=failed_hosts[host]
                
               data['auth_method']=auth_method
               data['ip_source']=ip
               data['host']=host
               data['result']=result
            
               #in case of multiple failed attempts
               if failed_hosts[host]>=3:
                   print("the user "+data['host'] +" had 3 failed Attempts ")
                   answer=''
                   while answer!='Y' or answer!='N':
                     answer=input("do you want to block the user from ssh (Y/N)")
                     if (answer=='Y'):
                       try:
                           subprocess.run([ "sudo", "iptables", "-A", "INPUT",
            "-p", "tcp", "--dport", "22",
            "-s", ip, "-j", "DROP"],check=True)
                           print(f"The ip {data['host']} has been blocked from ssh")
                       except subprocess.CalledProcessError as e :
                           print(f"Failed ",e)
                     elif answer=='N':
                         break
                     else:
                         print("please Select Y or N ")
                         
               print(json.dumps(data,indent=2))
#handles closing and opening sessions     
def monitor_sessions(line:str):
    line =line.split(' ')
    data={}
    data['timestamp']=line[0]
    for i in range(1,len(line)):
        if line[i]=='session':
            status=line[i+1]
            user=line[i+3]

            if (status=='opened'):
                by=line[len(line)-1]
            else :
                by=""
            data['event_type']='session change'
            data['status']=status
            

            data['user']=user
            data['by']=by 

            print(json.dumps(data))




