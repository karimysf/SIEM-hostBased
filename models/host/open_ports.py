import psutil
from utils import is_sudo
def scan_ports():
    if not is_sudo():
        print("Scanning Ports requires sudo priviliges \n Scanning will be skipped!! ")
        return 
    

    print("----Scanning Open Ports ----")
    connections = psutil.net_connections(kind='inet')
    open_ports=0
    for conn in connections:
        if conn.status == psutil.CONN_LISTEN:
            open_ports=open_ports+1
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
        
            pid = conn.pid
            try:
                proc_name = psutil.Process(pid).name() if pid else "N/A"
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(e) 
            
            print(f"Process: {proc_name} (PID: {pid}), Listening on: {laddr}")
    print(f"You have {open_ports} open ports , Make sure to disable uncessary ports  ")
    
    print("------Port scan Finished---")


            