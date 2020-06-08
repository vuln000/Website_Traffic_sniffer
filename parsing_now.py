import sys
from parsing import read_packets,read_tls,read_cells
from utils import *
import os

config = read_config('config')

path_packets = str(config['path_packets'])
path_tls = str(config['path_tls'])
path_cells = str(config['path_cells'])

check_path(path_packets)
check_path(path_tls)
check_path(path_cells)

name = sys.argv[1]

if 'packets' in sys.argv:
    read_packets(sys.argv[-1],name,path_packets,flag=True)
if 'tls' in sys.argv:
    read_tls(sys.argv[-1],name,path_tls,flag=True)
if 'cells' in sys.argv:
    read_cells(sys.argv[-1],name,path_cells,flag=True)

print(sys.argv,'has been removed')
