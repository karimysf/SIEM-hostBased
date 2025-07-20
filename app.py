from flask import Flask

from models.host.ssh_monitor import monitor_auth_logs
from models.host.open_ports import scan_ports
app=Flask(__name__)





if __name__=='__main__':
    scan_ports()
    
    try :
     
     monitor_auth_logs()

    except KeyboardInterrupt:
     print("User cancelled operation , stopping monitoring ....")

    
    
    app.run(debug=True)
    