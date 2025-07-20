import os
def is_sudo()-> bool:
    if os.geteuid() != 0:
        return False
    return True
        
       
    