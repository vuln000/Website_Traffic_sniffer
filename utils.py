import pathlib
import os
import subprocess
import time
import shutil

def read_config(config_path):
    dict_temp = {}
    with open(config_path,'r') as f:
        lines = f.readlines()
        for line in lines:
            if('#' in line):
                pass
            else:
                print(line)
                key = str(line.split('=')[0])
                value = str(line.split('=')[1])
                value = value.replace('\n','')
                dict_temp[key] = value
    return dict_temp
def check_path(save_path):
    if pathlib.Path(save_path).exists()==True:
        pass
    else:
        os.mkdir(save_path)
        cmd_chmod = 'sudo chmod o+w '+ save_path
        print(cmd_chmod)
        chmod = subprocess.Popen(cmd_chmod,stdout=subprocess.PIPE,shell=True)

config = read_config('config')
parsing_control = str(config['parsing_control'])

def logger(file_name,flag):
    localtime = time.asctime( time.localtime(time.time()) )
    fsize = os.path.getsize(file_name)
    f_kb = fsize/float(1024)
    if(flag==True):
        with open('logs/log_successed.txt','a') as f:
            f.write(str(localtime)+' '+str(f_kb)+'kb saved in '+ str(file_name)+'\n')
    else:
        with open('logs/log_failed.txt','a') as f:
            f.write(str(localtime)+' '+str(f_kb)+'kb saved in '+ str(file_name)+'\n')
    if parsing_control=='True':
        os.remove(file_name)

def cache_clean():
    caches = os.listdir('/tmp')
    for cache in caches:
        if 'rust' in str(cache):
            try: 
                shutil.rmtree('/tmp/'+str(cache))
            except:
                print("error in remove"+'/tmp/'+str(cache))
