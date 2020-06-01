import sys
from selenium import webdriver
from tbselenium.tbdriver import TorBrowserDriver
import numpy as np
import time
from utils import *

config = read_config('config')
TBB_dir = config['TBB_dir']
firefox_dir = config['firefox_dir']

proxy_type = int(config['proxy_type'])
proxy_http = str(config['proxy_http'])
proxy_http_port = int(config['proxy_http_port'])
proxy_ssl = str(config['proxy_ssl'])
proxy_ssl_port = int(config['proxy_ssl_port'])

def firfox_proxy(webdriver):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', proxy_type)
    profile.set_preference('network.proxy.http', proxy_http)
    profile.set_preference('network.proxy.http_port', proxy_http_port)
    profile.set_preference('network.proxy.ssl', proxy_ssl)
    profile.set_preference('network.proxy.ssl_port', proxy_ssl_port)
    profile.update_preferences()
    return profile


def capture(website,epoch):
    if 'tor' in sys.argv:
        browser = TorBrowserDriver(TBB_dir,socks_port=socks_port,control_port=control_port)
    else:
        profile = firfox_proxy(webdriver)
        browser = webdriver.Firefox(firefox_profile=profile,firefox_binary = firefox_dir)
    browser.delete_all_cookies()
    browser.get('http://' + website)

website = sys.argv[1]
epoch = sys.argv[2]

try:
    capture(website,epoch)
except:
    print('###############################Error#####################################')
    print('website,epoch',website,epoch)
    print('###############################Error#####################################')
