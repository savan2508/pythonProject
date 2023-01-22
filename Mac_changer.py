#!/usr/bin/env python
"""
This program lets you change your mac address for your desired device to
your desire MAC address
"""
import subprocess
import optparse

parser = optparse.OptionParser()

parser.add_option("-i","--interface", dest='interface', help="Interface to change its mac address")
parser.add_option("-m","--mac", dest='mac_address', help="Please enter desired MAC address for to change for the "
                                                         "interface")

(options, arguments) = parser.parse_args()
if options.interface and options.mac_address:
    interface = options.interface
    mac_address = options.mac_address

else:
    subprocess.call("ifconfig", shell=True)
    interface = input('Please include the device: ')
    mac_address = input('Please enter desired mac Address: ')

subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether " + mac_address, shell=True)
subprocess.call("ifconfig " + interface + " up", shell=True)

print(f"Your {interface} macaddress change to {mac_address}")
subprocess.call("ifconfig", shell=True)
