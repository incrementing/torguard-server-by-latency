import os
import re
import time
import platform
import subprocess
from beautifultable import BeautifulTable

servers = dict(
    Brazil_Sau_Paulo = "br.torguardvpnaccess.com",
    Chile = "chil.torguardvpnaccess.com",
    Canada_Toronto = "ca.torguardvpnaccess.com",
    Canada_Vancouver = "vanc.ca.west.torguardvpnaccess.com",
    Costa_Rica = "cr.torguardvpnaccess.com",
    Mexico = "mx.torguardvpnaccess.com",
    USA_Atlanta = "atl.east.usa.torguardvpnaccess.com",
    USA_LA = "la.west.usa.torguardvpnaccess.com",
    USA_Miami = "fl.east.usa.torguardvpnaccess.com",
    USA_Dallas = "dal.central.usa.torguardvpnaccess.com",
    USA_New_Jersey = "nj.east.usa.torguardvpnaccess.com",
    USA_New_York = "ny.east.usa.torguardvpnaccess.com",
    USA_Chicago = "chi.central.usa.torguardvpnaccess.com",
    USA_Las_Vegas = "lv.west.usa.torguardvpnaccess.com",
    USA_San_Francisco = "sf.west.usa.torguardvpnaccess.com",
    USA_Seattle = "sa.west.usa.torguardvpnaccess.com",
    Austria = "aus.torguardvpnaccess.com",
    Belgium = "bg.torguardvpnaccess.com",
    Bulgaria = "bul.torguardvpnaccess.com",
    Cyprus = "cp.torguardvpnaccess.com",
    Czech_Republic = "czech.torguardvpnaccess.com",
    Denmark = "den.torguardvpnaccess.com",
    Finland = "fin.torguardvpnaccess.com",
    France = "fr.torguardvpnaccess.com",
    Germany = "gr.torguardvpnaccess.com",
    Greece = "gre.torguardvpnaccess.com",
    Hungary = "hg.torguardvpnaccess.com",
    Iceland = "ice.torguardvpnaccess.com",
    Ireland = "ire.torguardvpnaccess.com",
    Isle_of_Man = "iom.torguardvpnaccess.com",
    Italy = "it.torguardvpnaccess.com",
    Latvia = "lv.torguardvpnaccess.com",
    Luxembourg = "lux.torguardvpnaccess.com",
    Netherlands = "nl.torguardvpnaccess.com",
    Norway = "no.torguardvpnaccess.com",
    Poland = "pl.torguardvpnaccess.com",
    Portugal = "por.torguardvpnaccess.com",
    Romania = "ro.torguardvpnaccess.com",
    Russia_Moscow = "mos.ru.torguardvpnaccess.com",
    Russia_St_Petersburg = "ru.torguardvpnaccess.com",
    Slovakia = "slk.torguardvpnaccess.com",
    Spain = "sp.torguardvpnaccess.com",
    Sweden = "swe.torguardvpnaccess.com",
    Switzerland = "swiss.torguardvpnaccess.com",
    Turkey = "turk.torguardvpnaccess.com",
    Ukraine = "ukr.torguardvpnaccess.com",
    United_Kingdom = "uk.torguardvpnaccess.com",
    Australia_Sydney = "au.torguardvpnaccess.com",
    Australia_Melbourne = "melb.au.torguardvpnaccess.com",
    Hong_Kong = "hk.torguardvpnaccess.com",
    Japan_Tokyo_1 = "jp.torguardvpnaccess.com",
    #Japan_Tokyo_2 = "loc2.jp.torguardvpnaccess.com", Dead?
    South_Korea = "sk.torguardvpnaccess.com",
    Malaysia = "my.torguardvpnaccess.com",
    New_Zealand = "nz.torguardvpnaccess.com",
    Singapore_1 = "singp.torguardvpnaccess.com",
    Singapore_2 = "loc2.singp.torguardvpnaccess.com",
    Taiwan = "tw.torguardvpnaccess.com",
    Thailand = "thai.torguardvpnaccess.com",
    Vietnam = "vn.torguardvpnaccess.com",
    Egypt = "egy.torguardvpnaccess.com",
    India_Chennai = "loc2.in.torguardvpnaccess.com",
    India_Bangalore = "in.torguardvpnaccess.com",
    Israel = "isr.torguardvpnaccess.com",
    South_Africa = "za.torguardvpnaccess.com",
    Saudi_Arabia = "saudi.torguardvpnaccess.com",
    Tunisia = "tun.torguardvpnaccess.com",
    Dubai = "uae.torguardvpnaccess.com"
)

def ping(hostname):
    if (platform.system()=="Windows"):
        ping = os.popen("ping "+hostname+" -n 1")
        result = ping.readlines()
        msLine = result[-1].strip()
        return str(msLine.split(' = ')[-1]).replace("ms", "") + ".0"
    else:
        ping = subprocess.Popen(['ping', '-c', '1', '-W', '2', hostname],
                               shell=False,
                               stdout=subprocess.PIPE)
        ping_out = ping.communicate()[0]

        if (ping.wait() == 0):
            search = re.search(r'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms',
                         str(ping_out), re.M|re.I)
            ping_rtt = search.group(2)
            return ping_rtt

def clear():
    if (platform.system()=="Windows"):
        os.system("cls")
    else:
        os.system("clear")

print("Collecting response times...")
time.sleep(1)

pings = dict()
for key, value in servers.items():
    print("Pinging " + key.replace("_", " ") + " ("+value+")...")
    response = ping(value)
    intPing = 1000
    try:
        if (str(response)!="None"):
            intPing = int(str(response).split(".")[0])
    except:
        intPing = 1000
    pings[key.replace("_", " ") + "|"+value] = intPing
    clear()

clear()
print("Ordering by response times...")

table = BeautifulTable()
table.column_headers = ["Location", "Hostname", "Response Time"]
sortedPings = sorted(pings, key=pings.__getitem__)
for k in sortedPings:
    table.append_row([k.split("|")[0], k.split("|")[1], str(pings[k])+"ms"])
clear()
print(table)