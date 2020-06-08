import sys
from parsing import read_packets,read_tls,read_cells
from util import *
import os

config = read_config('config')

path_packets = str(config['path_packets'])
path_tls = str(config['path_tls'])
path_cells = str(config['path_cells'])

check_path(path_packets)
check_path(path_tls)
check_path(path_cells)

if 'packets' in sys.argv:
    read_packets(sys.argv[-1],path_packets)
if 'tls' in sys.argv:
    read_tls(sys.argv[-1],path_tls)
if 'cells' in sys.argv:
    read_cells(sys.argv[-1],path_cells)

os.remove(sys.argv[-1])
print(sys.argv,'has been removed')
