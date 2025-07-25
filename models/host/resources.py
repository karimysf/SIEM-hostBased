import psutil

import subprocess

import time

def monitor_cpu_utilisation():
    pc_mem =psutil.virtual_memory().total
    cpu_percent=psutil.cpu_percent(interval=1)
    mem_percent=psutil.virtual_memory().used
   

    for process in psutil.process_iter(['pid','name','cpu_percent','memory_info']): 
        try :
            process_cpu_percent=process.cpu_percent(interval=1)
            process_mem=process.memory_percent()
            if (process_cpu_percent>80  ):
                if (mem_percent/pc_mem >50 ):
                    print("Memory and CPU Usage is high !!")
                    get_processes_by_usage()
                    continue
                else : 
                    print("CPU is High !!")
                    print("please check this list of over consuming processes")
                    get_processes_by_usage()
                    continue
            if (mem_percent/pc_mem >50 ):

                    print("Mem  is High !!")
                    print("please check this list of over consuming processes")
                    get_processes_by_usage()
                    continue
            name=process.name()
            pid=process.pid
            print(f"the process {name} of pid {pid} is using {process_mem} % mem,{cpu_percent} % of CPU")

            



        except (psutil.NoSuchProcess, psutil.AccessDenied) as e :
           print(e)


def get_processes_by_usage():

    cmd = ['ps', '-eo', 'pid,%cpu,%mem', '--sort=-%cpu', '--no-headers']
    result = subprocess.run(cmd, capture_output=True, text=True)

    for line in result.stdout.strip().split('\n'):
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue  
        pid, cpu, mem = parts

        try:
            process = psutil.Process(int(pid))
            name = process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            name = "N/A"
        
        time.sleep(0.4)
        print(f"PID: {pid}, Name: {name}, CPU%: {cpu}, MEM%: {mem}")



monitor_cpu_utilisation()
