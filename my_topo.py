#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import Link, TCLink
import time
from threading import Thread

# Topology:
#  victim ---------+
#                [s0]----[s1]----- server
#  attacker -------+

def start_server(net):
    server = net.get('server')
    return server.popen([
        'python3', 'my_server.py'
    ])

def start_victim_one(net, victim_no):
    victim = net.get(victim_no)
    return victim.popen([
        'python3', 'my_client.py'
    ])

def start_victim_two(net, victim_no):
    victim = net.get(victim_no)
    return victim.popen([
        'python3', 'my_client.py'
    ])

def start_three(net, victim_no):
    victim = net.get(victim_no)
    return victim.popen([
        'python3', 'my_client.py'
    ])

def start_attacker_1(net, attacker_no):
    attacker = net.get(attacker_no)
    return attacker.popen([
        'python3', 'my_attacker.py'
    ])

def start_attacker_2(net, attacker_no):
    attacker = net.get(attacker_no)
    return attacker.popen([
        'python3', 'my_attacker.py'
    ])


def topology():

    net = Mininet()

    # add controller
    c0 = net.addController( 'c0', controller=lambda name: RemoteController(name,ip= '192.168.226.128', protocol= 'tcp', port= 6653))

    # add hosts
    server = net.addHost( 'server', ip = "10.10.10.1", mac = "00:00:00:00:00:01")
    victim_one = net.addHost( 'victim_one', ip = "10.10.10.2", mac = "00:00:00:00:00:02")
    #victim_two = net.addHost( 'victim_two', ip = "10.10.10.3", mac = "00:00:00:00:00:03")
    #three = net.addHost( 'three', ip = "10.10.10.4", mac = "00:00:00:00:00:04")
    attacker_1 = net.addHost( 'attacker_1', ip = "10.10.10.5", mac = "00:00:00:00:00:05")
    attacker_2 = net.addHost( 'attacker_2', ip = "10.10.10.6", mac = "00:00:00:00:00:06")

    # add switches
    s0 = net.addSwitch( 's0', dpid='0000000000000001')
    s1 = net.addSwitch( 's1', dpid='0000000000000002')
   
    # add links
    net.addLink(victim_one, s0)
    #net.addLink(victim_two, s0)
    #net.addLink(three, s0)
    net.addLink(attacker_1, s0)
    net.addLink(attacker_2, s0, cls=TCLink, delay='20ms')
    net.addLink(server, s1)
    net.addLink(s0, s1)
  
    net.build()

    print ("*** Starting network")

    net.start()

    victim_one.cmd('ping 10.10.10.1 -c 2')
    #victim_two.cmd('ping 10.10.10.1 -c 2')
    #three.cmd('ping 10.10.10.1 -c 2')
    attacker_1.cmd('ping 10.10.10.1 -c 2')
    attacker_2.cmd('ping 10.10.10.1 -c 2')
    time.sleep(2)

    # DDOS SYNC
    one = round(float(attacker_1.cmd('ping 10.10.10.1 -c 10').splitlines()[-1].split('/')[4]))
    two = round(float(attacker_2.cmd('ping 10.10.10.1 -c 10').splitlines()[-1].split('/')[4]))
    diff = int(two) - int(one)

    
    server = Thread(target=start_server, args=(net,))
    victim_one_thread = Thread(target=start_victim_one, args=(net, "victim_one",))
    #victim_two_thread = Thread(target=start_victim_two, args=(net, "victim_two",))
    #victim_three_thread = Thread(target=start_three, args=(net, "three",))
    attacker_1_thread = Thread(target=start_attacker_1, args=(net, "attacker_1",))
    attacker_2_thread = Thread(target=start_attacker_2, args=(net, "attacker_2",))

    server.start()
    victim_one_thread.start()
    #victim_two_thread.start()
    #victim_three_thread.start()
    attacker_2_thread.start()
    time.sleep(diff / 1000)
    attacker_1_thread.start()

    time.sleep(400)
    net.stop()

if __name__ == '__main__':
    topology()
