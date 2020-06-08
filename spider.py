import subprocess
import sys
import os
import time
import numpy
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tbselenium.tbdriver import TorBrowserDriver
import numpy as np
import threading
import signal
import psutil
import pathlib
from utils import *


config = read_config('config')
Timeout = int(config['Timeout'])
instances = int(config['instances'])
TimegapMin = int(config['TimegapMin'])
TimegapMax = int(config['TimegapMax'])
socks_port= int(config['socks_port'])
control_port= int(config['control_port'])
sniff_port_http = int(config['sniff_port_http'])
sniff_port_tor = int(config['sniff_port_tor'])
screensnap_control = str(config['screensnap_control'])
refreshlog = str(config['refreshlog'])
parsing_control = str(config['parsing_control'])
parsing_type = str(config['parsing_type']).split(',')

print(sys.argv)

y_split = []
pid_TBB_list = []
def protect_tbb():
    pid_TBB_list.append(int(subprocess.check_output(["pidof", 'tor'])))
    for i in subprocess.check_output(["pidof", 'firefox.real']).split(): 
        pid_TBB_list.append(int(i)) 
    print('pid of TBB servises is ',pid_TBB_list)


def firfox_proxy(webdriver):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', '::1')
    profile.set_preference('network.proxy.http_port', 8899)
    profile.set_preference('network.proxy.ssl', '::1')
    profile.set_preference('network.proxy.ssl_port', 8899)
    profile.update_preferences()
    return profile
def get_pid(name):
    pids = subprocess.check_output(["pidof",name]).split()
    pids_1 = []
    [pids_1.append(int(pid)) for pid in pids]
    return pids_1
def screensnap(website,epoch):
    os.system("import -window root "+ figpath + website+str(epoch)+'.png')
    print('Get screenshot in',figpath + website+str(epoch)+'.png')
    time.sleep(10)
def kill(process):
    pids = get_pid('tshark')
    for pid in pids:
        cmd1 = "sudo kill -9 %s" % pid# . # -9 to kill force fully
        os.system(cmd1)
    if (process.wait())==-9 : # this will print -9 if killed force fully, else -15.
       print('tshark killed force fully')
def kill2(proc_pid):
    try:
        pids = get_pid('firefox.real')
    except:
        print("error when kill2")
    #print(pids)
    for pid in pid_TBB_list:
        if pid in pids:
            pids.remove(pid)
    #print(pids)
    for pid in pids:
        cmd1 = "sudo kill -9 %s" % pid# . # -9 to kill force fully
        os.system(cmd1)
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        try:
            proc.kill()
        except:
            pass
    process.kill()
def kill_firefox():
    pids = get_pid('firefox')
    for pid in pids:
        cmd1 = "sudo kill -9 %s" % pid# . # -9 to kill force fully
        os.system(cmd1)
def mult_capture(url_1,url_2,id_website,epoch):
    if 'tor' in sys.argv:
        sniff_port = sniff_port_tor
        cmd_page_1 = 'python browser.py ' + str(url_1) + ' '+ str(epoch) + ' tor mult'
        cmd_page_2 = 'python browser.py ' + str(url_2) + ' '+ str(epoch) + ' tor' + ' second mult'
    else:
        sniff_port = sniff_port_http
        cmd_page_1 = 'python browser.py ' + str(url_1) + ' '+ str(epoch)
        cmd_page_2 = 'python browser.py ' + str(url_2) + ' '+ str(epoch) + ' second'
    cmd = 'sudo tshark -w '+ path+url_1+'-'+str(epoch)+'.cap -i any -f "port '+ str(sniff_port)+ '"'
    print(cmd)
    tshark = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    process_page_1 = subprocess.Popen(cmd_page_1,stdout=subprocess.PIPE,shell=True) 
    Timegap = np.random.randint(TimegapMin,TimegapMax)
    y_split.append(Timegap)
    print('Opening the second tab after ' + str(Timegap) +' seconds')
    print('Watting for Timegap ',Timegap)
    time.sleep(Timegap)
    process_page_2 = subprocess.Popen(cmd_page_2,stdout=subprocess.PIPE,shell=True)
    print('Watting for Timeout ',Timeout)
    time.sleep(Timeout//2)
    if screensnap_control=='True':
        screensnap(url_1,epoch)
    time.sleep(Timeout//2)
   # kill2(process_page_1.pid)
    #kill2(process_page_2.pid)
    kill(tshark)
    if 'tor' not in sys.argv:
        kill_firefox()
    else:
        kill2(process_page_1.pid)
        kill2(process_page_2.pid)
    cmd_chmod = 'sudo chmod 777 '+ path+url_1+'-'+str(epoch)+'.cap'
    print(cmd_chmod)
    chmod = subprocess.Popen(cmd_chmod,stdout=subprocess.PIPE,shell=True)
    if parsing_control=='True':
        print('Trying to parsing...')
        cmd_parsing = 'python parsing_now.py ' + str(id_website) + ' ' +str(temp_parsing_type) + website+'-'+str(epoch)+'.cap'
        print(cmd_parsing)
        p = subprocess.Popen(cmd_parsing,stdout=subprocess.PIPE,shell=True)
        p.wait()
    np.save('y_split',y_split)
    cache_clean()
    print('exit')
def capture(website,id_website,epoch):
    if 'tor' in sys.argv:
        sniff_port = sniff_port_tor
        cmd_page_1 = 'python browser.py ' + str(website) + ' '+ str(epoch) + ' tor'
    else:
        sniff_port = sniff_port_http
        cmd_page_1 = 'python browser.py ' + str(website) + ' '+ str(epoch)
    cmd = 'sudo tshark -w '+ path+website+'-'+str(epoch)+'.cap -i any -f "port '+ str(sniff_port)+ '"'
    print(cmd)
    tshark = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    print(cmd_page_1)
    process_page_1 = subprocess.Popen(cmd_page_1,stdout=subprocess.PIPE,shell=True)
    print('Watting for Timeout ',Timeout)
    time.sleep(Timeout//2)
    if screensnap_control=='True':
        screensnap(website,epoch)
    time.sleep(Timeout//2)
    #kill2(process_page_1.pid)
    kill(tshark)
    if 'tor' not in sys.argv:
        kill_firefox()
    else:
        kill2(process_page_1.pid)
    cmd_chmod = 'sudo chmod 777 '+ path+website+'-'+str(epoch)+'.cap'
    print(cmd_chmod)
    chmod = subprocess.Popen(cmd_chmod,stdout=subprocess.PIPE,shell=True)
    if parsing_control=='True':
        print('Trying to parsing...')
        cmd_parsing = 'python parsing_now.py ' + str(id_website) + ' ' +str(temp_parsing_type) + website+'-'+str(epoch)+'.cap'
        print(cmd_parsing)
        p = subprocess.Popen(cmd_parsing,stdout=subprocess.PIPE,shell=True)
        p.wait()
    cache_clean()
    print('exit')




with open('websites.txt','r') as f:
    websites = f.readlines()
with open('websites_non_sensitive.txt','r') as f:
    websites_non_sensitive = f.readlines()

if refreshlog=='True':
    with open('logs/log_successed.txt','w') as f:
        print("log_successed.txt refreshed")
    with open('logs/log_failed.txt','w') as f:
        print("log_failed.txt refreshed")

#check parsing_type
temp_parsing_type=''
if ('cells' in parsing_type) and 'tor' not in sys.argv:
    print('cells could only be extracted from tor traffic')
    parsing_type.remove('cells')
for i in parsing_type:
    temp_parsing_type=temp_parsing_type + str(i) +' '

if 'tor' in sys.argv:
    Timeout = 100
    try:
        protect_tbb()
    except:
        print('No TBB servises detected')
if 'mult' in sys.argv:
    Timeout = Timeout*2
    path = os.getcwd()+'/mult_tab_results/'
    figpath = 'mult_tab_screenshots/'
    check_path(path)
    check_path(figpath)
    num_websites=len(websites)
    for i,id_website in zip(websites,range(num_websites)):
        url_1 = i.split('\n')[0]
        print('Dealing with sesitive '+str(url_1))
        for epoch in tqdm(range(instances)):
            pos = np.random.randint(0,len(websites))
            url_2 = websites[pos].split('\n')[0]
            print("The second website is "+url_2)
            file_name = path+url_1+'-'+str(epoch)+'.cap'
            try:
                mult_capture(url_1,url_2,id_website,epoch)
                logger(file_name,True)
            except:
                logger(file_name,False)  
elif 'single' in sys.argv:
    path = os.getcwd()+'/results/'
    figpath = 'screenshots/'
    check_path(path)
    check_path(figpath)
    num_websites=len(websites)
    for i,id_website in zip(websites,range(num_websites)):
        url = i.split('\n')[0]
        print('Dealing with sesitive '+str(url))
        for epoch in tqdm(range(instances)):
            file_name = path+url+'-'+str(epoch)+'.cap'
            try:
                capture(url,id_website,epoch)
                logger(file_name,True)
            except:
                logger(file_name,False)
    for i,id_website in zip(websites_non_sensitive,range(len(websites_non_sensitive))):
        url = i.split('\n')[0]
        print('Dealing with non-sesitive '+str(url))
        file_name = path+url+'-'+str(999)+'.cap'
        try:
            capture(url,id_website,999)
            logger(file_name,True)
        except:
            logger(file_name,False)
