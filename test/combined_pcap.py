import os 
import sys
import shutil

from_path = str(sys.argv[1])
from_list = os.listdir(sys.argv[1])

to_path = str(sys.argv[2])
to_list = os.listdir(sys.argv[2])

def get_id(pcap_name):
    return pcap_name.split('-')[-1].split('.')[0]
def changed_id(pcap_name,new_id):
    head,remain = pcap_name.split('-')
    old_id,tail = remain.split('.')
    return str(head) + '-' + str(new_id) + '.' + str(tail)
for pcap in from_list:
    #update to_list  
    to_list = os.listdir(sys.argv[2])
    pcap_from_path = from_path + str(pcap)
    pcap_to_path = to_path + str(pcap)
    temp_pcap_name = pcap
    #Let's get a new name
    while(temp_pcap_name in to_list):
        if(get_id(temp_pcap_name)=='999'):
            print('###detected non-sensitived website',temp_pcap_name,'jumped')
            break
        new_id = int(get_id(temp_pcap_name)) + 1
        temp_pcap_name = changed_id(temp_pcap_name,new_id)
    old = from_path+'/'+str(pcap)
    new = to_path+'/'+str(temp_pcap_name)
    shutil.copyfile(old,new)
    print(old,'----->>>>',new)
    
