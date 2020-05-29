import pathlib
import os
import subprocess
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

