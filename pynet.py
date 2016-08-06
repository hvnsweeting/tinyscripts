#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Python network discover tool
'''


import ipaddress
import itertools as itt
import json
import logging
import re
import sys
import subprocess as spr
import urllib.request

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


def list_to_dict(parts):
    return dict(
        zip(itt.islice(parts, 0, len(parts), 2),
            itt.islice(parts, 1, len(parts), 2)
            )
    )


class PyNet(object):
    def __init__(self, iface='en0'):
        self.interface = iface
        self._my_ip = None
        self.hosts = []
        self.gateway = None

    @property
    def my_ip(self):
        if self._my_ip:
            return self._my_ip

        output = spr.check_output(['ifconfig', self.interface])
        for line in output.splitlines():
            # inet 10.235.31.220 netmask 0xfffffc00 broadcast 10.235.31.255
            if b'inet ' in line:
                parts = line.decode().strip().split()
        data = list_to_dict(parts)
        # TODO get mask
        # netmarks = int(data['netmask'], 16)
        ipaddr = ipaddress.ip_address(data['inet'])
        self._my_ip = str(ipaddr)
        return self._my_ip

    def scan_network(self):
        cidr = self.my_ip + "/24"  # TODO get real netmask
        logger.info("Nmap scanning CIDR: %s", cidr)
        cmd = ["nmap", "-sP", cidr]
        output = spr.check_output(cmd)
        for line in output.splitlines():
            logger.debug("Nmap output: %s", line)
            line = line.decode().split()
            if self.my_ip in line:
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

    def default_route(self):
        cmd = ['netstat', '-nr']
        for line in cmdoutlines(cmd):
            if 'default' in line.split():
                self.gateway = line.split()[1]
                return self.gateway

    def show_gateway(self):
        cmd = ['nmap', '-A', '-T4', self.gateway]
        for line in cmdoutlines(cmd):
            print(line)

    def show_my_wan(self):
        with urllib.request.urlopen(
            urllib.request.Request(
                'http://ipinfo.io',
                # fake as python-requests since the site does not support
                # default python user-agent
                headers={'User-Agent': 'python-requests/2.10.0'})
        ) as f:
            waninfo = json.loads(f.read().decode())
        logger.info("Getting WAN data:")
        print(waninfo)


def cmdoutlines(cmd):
    for line in spr.check_output(cmd).splitlines():
        yield line.decode().strip()


def main():
    # TODO ping 3 different sources
    c = PyNet('en0')
    c.show_my_wan()
    c.scan_network()
    c.show_hosts()
    for host in c.hosts:
        #  PyNet.ping(host)
        PyNet.ping_sweep(host)
    c.show_gateway()

    # - save all data to db
    # tables
    # WanIP - LANIP, DefaultRroute,  ISP, hostname, location, timestamp, SSID
    # WanIP,LanIP foreign key - hosts
    # hosts table (MAP, ip, hostname, ping, port, device type, misc, time)

    # TODO get wifiname
    print(c.default_route())


if __name__ == "__main__":
    main()
