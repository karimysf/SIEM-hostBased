from ssh_monitor import read_logs_from_now
import psutil
data={}

def log_audit():
      print("----Monitoring  audit logs -----")
      for line in read_logs_from_now('/var/log/audit/audit.log'):
          type=''
          index=5
          while (line[index]!=' '):
               type=type+line[index]
               index=index+1
          print(type)

          if type=='SYSCALL':
               format_sysCall(line)




def format_sysCall(line:str):
    i=line.index('success')
    ppid=''
    pid=''
    if line[i+8]=='y':
        data['success']='yes'
    else:
        data['success']='no'
    #ppid
    i=line.index('ppid=')+5
    while line[i]!=' ':
        ppid=ppid+line[i]
        i=i+1
    i=i+5
    while line[i]!=' ':
        pid=pid+line[i]
        i=i+1
    try:
       parent_process = psutil.Process(int(ppid)).name() if pid else "N/A"
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(e) 
    try:
        process_name = psutil.Process(int(pid)).name() if pid else "N/A"
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(e) 
    data['parent-process']=parent_process
    data['process']=process_name

    

    #commande 
    i = line.index('comm=')+5
    while (line[i]!=' '):
        data['command']=data['command']+line[i] 
        i=i+1
    print(data)



log_audit()