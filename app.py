from flask import Flask

from models.host.ssh_monitor import monitor_auth_logs
app=Flask(__name__)





if __name__=='__main__':
  
    try :
     monitor_auth_logs()

    except KeyboardInterrupt:
     print("User cancelled operation , stopping monitoring ....")

    
    
    app.run(debug=True)
    