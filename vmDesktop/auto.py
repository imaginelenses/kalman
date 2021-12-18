import subprocess
import signal
from time import sleep 

# command = 'http-server'
command = 'flask run -h 0.0.0.0 -p 8084'

with subprocess.Popen([command], stdout=subprocess.PIPE, shell=True) as p:
    readOut = iter(p.stdout.readline, b'')
    
    # sleep(5)
    # for line in readOut:
    #     print('out', line)

    for i in range(4):
        print('out', next(readOut, 'Error'))
    
    print('End')
    out = iter(p.stdout.readlines, b'')
    print('out', next(out, 'Error'))
    print('out', next(out, 'Error'))
    print('out', next(out, 'Error'))


    
    # print(next(readOut, 'Hello'))
    # # for i in range(6):
    #     # continue



# def run_command(command):
#     p = subprocess.Popen(command,
#                          stdout=subprocess.PIPE,
#                          stderr=subprocess.PIPE,
#                          shell=True)
    
#     # Read stdout from subprocess until the buffer is empty !
#     for line in iter(p.stdout.readline, b''):
#         if line: # Don't print blank lines
#             yield line
    
#     # This ensures the process has completed, AND sets the 'returncode' attr
#     while p.poll() is None:                                                                                                                                        
#         sleep(.1) #Don't waste CPU-cycles
#     # Empty STDERR buffer
#     err = p.stderr.read()
#     if p.returncode != 0:
#        # The run_command() function is responsible for logging STDERR 
#        print("Error: " + str(err))

# cmd="flask run -h 0.0.0.0 -p 8080"

# for line in run_command(cmd):
#     # x = str(line)
#     # print("val : ",x)
#     print(line)
