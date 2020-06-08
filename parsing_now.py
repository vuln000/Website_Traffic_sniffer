import sys
from parsing import read_packets,read_tls,read_cells
from utils import *
import os
import time 
config = read_config('config')

path_packets = str(config['path_packets'])
path_tls = str(config['path_tls'])
path_cells = str(config['path_cells'])

check_path(path_packets)
check_path(path_tls)
check_path(path_cells)
with open('websites.txt','r') as f:
    websites = f.readlines()
with open('websites_non_sensitive.txt','r') as f:
    websites_non_sensitive = f.readlines()
def get_name(pcap):
    for i,p in zip(websites,range(len(websites))):
        if i.split('\n')[0] in pcap:
            return str(p)
    for i,p in zip(websites_non_sensitive,range(len(websites_non_sensitive))):
        if i.split('\n')[0] in pcap:
            return str(p+len(websites))

pcaps = os.listdir('results/')
if len(pcaps)>2:
    for pcap in pcaps:
        try:
            pcap_path = 'results/'+pcap
            name = get_name(pcap)
            if 'packets' in sys.argv:
                read_packets(pcap,name,path_packets,flag=True)
            if 'tls' in sys.argv:
                read_tls(pcap,name,path_tls,flag=True)
            if 'cells' in sys.argv:
                read_cells(pcap,name,path_cells,flag=True)
            os.remove(pcap_path)
            print(str(pcap_path) + 'has been removed')
        except:
            print('writing ... jumped')
 



