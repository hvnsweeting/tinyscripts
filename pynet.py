#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Python network discover tool
'''


import json
import logging
import re
import sys
import subprocess as spr
import urllib.request

import netifaces


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PERCENT = re.compile('\d+\.*\d*%')


def ping(ip):
    logger.info("Pinging %s", ip)
    cmd = ['ping', '-c3', ip]
    for line in cmdoutlines(cmd):
        if 'packet loss' in line:
            loss = PERCENT.findall(line)[0]
            continue
        if line.startswith('round-trip'):
            min_, avg, max_, stddev = line.split(
                ' = '
            )[1].strip(' ms').split('/')
            print(loss, avg)


class PyNet(object):
    def __init__(self):
        self.interface = None
        self.gateway = None
        self.lan_ipv4 = None

        self.load_interfaces()
        self.hosts = []

    def __str__(self):
        return "interface: {0} - IPv4: {1} - mask: {2}".format(
                self.interface,
                self.lan_ipv4,
                self.netmask
        )

    def load_interfaces(self):
        logger.info("Getting default interface")
        iface = netifaces.gateways()['default'][netifaces.AF_INET]
        self.gateway, self.interface = iface

        iface = netifaces.ifaddresses(self.interface)[netifaces.AF_INET][0]
        self.lan_ipv4 = iface['addr']
        self.broadcast = iface['broadcast']
        self.netmask = iface['netmask']

    def scan_network(self):
        cidr = self.lan_ipv4 + "/" + get_net_size(self.netmask)
        logger.info("Nmap ping scaning CIDR: %s", cidr)
        ping_scan = ["nmap", "-sn", cidr]
        output = spr.check_output(ping_scan)
        for line in output.splitlines():
            logger.debug("Nmap output: %s", line)
            line = line.decode().split()
            if self.lan_ipv4 in line:
                continue
            # Nmap scan report for 10.235.51.221
            if "for" in line:
                self.hosts.append(line[-1])
        if len(self.hosts) == 1:
            sys.exit("Found only myself")

    def show_hosts(self):
        logger.info("Showing found hosts:")
        for host in self.hosts:
            print("FOUND %s" % host)

    @classmethod
    def get_mac(ip):
        '''convert IP to MAC by using arp'''
        pass

    @staticmethod
    def ping_sweep(ip):
        cmd = ["nmap", "-sn", ip]
        logger.info("nmap ping sweep: %s", cmd)
        for line in cmdoutlines(cmd):
            logger.debug(line)

    def full_scan(self, ip):
        cmd = ["nmap", "-A", "-T4", ip]
        logger.info("nmap fullscan: %s", cmd)
        for line in cmdoutlines(cmd):
            logger.debug(line)

    def show_gateway(self):
        self.full_scan(self.gateway)

    def show_my_wan(self):
        logger.info("Getting WAN data:")

        waninfo = None
        with urllib.request.urlopen(
            urllib.request.Request(
                'http://ipinfo.io',
                # fake as python-requests since the site does not support
                # default python user-agent
                headers={'User-Agent': 'python-requests/2.10.0'})
        ) as f:
            data = f.read()
            logger.debug("Got wan info: %s", data[:100])
            try:
                waninfo = json.loads(f.read().decode())
            except json.decoder.JSONDecodeError:
                # TODO use dig when cannot get by ipinfo
                pass
        print(waninfo)


def get_net_size(netmask):
    binary_str = ''
    for octet in netmask.split('.'):
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))


def cmdoutlines(cmd):
    for line in spr.check_output(cmd).splitlines():
        yield line.decode().strip()


def main():
    # TODO ping 3 different sources
    c = PyNet()
    print(c)
    c.show_my_wan()
    c.scan_network()
    c.show_hosts()
    for host_ip in c.hosts:
        ping(host_ip)
        c.full_scan(host_ip)

    # - save all data to db
    # tables
    # WanIP - LANIP, DefaultRroute,  ISP, hostname, location, timestamp, SSID
    # WanIP,LanIP foreign key - hosts
    # hosts table (MAP, ip, hostname, ping, port, device type, misc, time)

    # TODO get wifiname


if __name__ == "__main__":
    main()
