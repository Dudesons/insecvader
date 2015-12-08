from scapy.all import *
import socket
import re
import os
import json


class ArpScan:
    """

    """
    def __init__(self, mask, net_interface):
        """
        """
        self.net = []
        self.mask = mask
        self.gw = ''
        self.route = []
        self.net_interface = net_interface
        self.mac_constructor = (os.popen("grep -e \"base 16\" -R mac_constructor")).readlines()
        self.arp_pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=self.mask)

    def scan(self):
        """
        """
        n = list()
        cmd = list()
        ans, unans = srp(self.arp_pkt, iface=self.net_interface, timeout=2)
        ans.summary(lambda (s, r): cmd.append(r.sprintf("%Ether.src% %ARP.psrc%").split(" ")))
        [n.append({"mac": i[0],
                   "ip": i[1],
                   "device": self._get_device(i[0]),
                   "os": None,
                   "hostname": ArpScan._get_hostname(i[1])}) for i in cmd]
        self.net = n

    @staticmethod
    def _get_hostname(ip):
        """
        """
        return socket.getfqdn(ip)

    def _get_gw(self):
        """
        """
        self.gw = list(set(((os.popen('route -n | grep -e "0\.0\.0\.0 *[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\} *0\.0\.0\.0"')).read()).split(" ")))[1]

    def _get_device(self, mac):
        """
        """

        constructor_sign = str(''.join(mac.split(':', 3)[0:3])).upper()
        device = "computer"
        phones = ["nokia", "ericsson", "samsung"]
        mac_apple = "apple"
        virtual = "VMware"

        for line in self.mac_constructor:
            if constructor_sign in line:
                brand = line.split(" ", 8)
                i = 0

                if mac_apple in str(brand[8]).lower():
                    device = "apple"
                    break
                elif virtual in brand[8]:
                    device = "vm"
                    break
                elif str(brand[8]).lower() in phones[i]:
                    device = "phone"
                    break
                else:
                     i += 1
                break

        return device

    def _get_os(self, ip):
        """
        """
        #nmap -sV --version-all
        #i = (os.popen("nmap -O "+ip)).readlines()
        #to = i.readlines()
        i = 0
        system = "Unknown"
        while i < len(i):
            if re.search(".*Linux.*", i[i], re.IGNORECASE):
                system = "Linux"
                break
            if re.search(".*Windows.*", i[i], re.IGNORECASE):
                system = "Windows"
                break
            if re.search(".*Mac.*", i[i], re.IGNORECASE):
                system = "Mac"
                break
            i += 1
        return system

    def get_network(self, opt=0):
        """
        """
        n = {'gw':self.gw, 'route':self.route, 'net':self.net}
        if opt == 0:
            return n
        elif opt == 1:
            return json.dumps(n)
        else:
            print("[ERROR] GetNetwork(self, opt) : opt must equal 0 (dict) or 1 (json)")

if __name__ == "__main__":
    #s = ArpScan("10.8.97.1/20", "eth1")
    s = ArpScan("192.168.0.0/24", "eth0")
    #s = ArpScan("192.168.0.0/24")

    #print s.GetDevice("b8:ac:6f:43:39:cd")
    #print s.GetDevice("8c:89:a5:a3:ad:1f")
    #print s.GetDevice2("00:50:56:93:10:DC")
    s.scan()
    print s.get_network()
    """s = Scan("172.18.0.0/24")
    s.GetGW()
    s.GetIpMac()
    print s.GetNetwork(0)
    print "-"*20
    print s.GetNetwork(1)"""
