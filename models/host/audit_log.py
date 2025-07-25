from ssh_monitor import read_logs_from_now
import psutil
import re
import datetime
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
          if type in ['USER_LOGIN','USER_LOGOUT']:
               user_login_logout(line,type)




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


def user_login_logout(line: str,type:str):
    # Check event type in line
    
    # Extract timestamp (assume it's at start like "2025-07-19T10:55:01.794829+01:00")
    timestamp_str = line.split(' ')[0]
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
    except Exception:
        timestamp = datetime.now()  # fallback
    
    # Extract key=value pairs
    kv_pairs = re.findall(r'(\w+)=(".*?"|\S+)', line)
    info = {k: v.strip('"') for k, v in kv_pairs}
    
    # Prepare result dictionary
    result = {
        'event_type': type,
        'timestamp': timestamp.isoformat(),
        'user': info.get('user', 'N/A'),
        'uid': info.get('uid', 'N/A'),
        'tty': info.get('tty', 'N/A'),
        'ip': info.get('addr', 'N/A'),  
    }
    print(result)

log_audit()