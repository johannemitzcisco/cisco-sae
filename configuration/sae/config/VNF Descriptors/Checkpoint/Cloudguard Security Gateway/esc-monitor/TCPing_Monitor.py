#!/usr/bin/python

import sys
from subprocess import call

def get_value(key):
    i = 0
    for arg in sys.argv:
        i = i + 1
        if arg == key:
            return sys.argv[i]

    return None

def get_ip_addr():
    device_ip = get_value("vm_ip_address")
    return device_ip

def get_tcp_port():
    tcp_port = get_value("tcp_port")
    return tcp_port

def get_timeout():
    timeout = get_value("timeout_sec")
    return timeout 

def tcping(ip, port, timeout):
    status = call(["tcping", "-t", timeout, ip, port])
    return status

vm_ip=get_ip_addr()
if vm_ip == None:
    print >>sys.stdout, "Missing argument: vm_ip_address"
    sys.exit(1)

tcp_port=get_tcp_port()
if tcp_port == None:
    print >>sys.stdout, "Missing argument: tcp_port"
    sys.exit(1)

timeout=get_timeout()
if timeout == None:
    print >>sys.stdout, "Missing argument: timeout_sec"
    sys.exit(1)

status = tcping(vm_ip, tcp_port, timeout)
sys.exit(status)

