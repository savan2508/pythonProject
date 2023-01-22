#!/usr/bin/env python
"""
This program lets you change your mac address for your desired device to
your desire MAC address
"""
import subprocess

subprocess.call("ifconfig", shell=True)
interface = input('Please include the device: ')
mac_address = input('Please enter desired mac Address: ')

subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether " + mac_address, shell=True)
subprocess.call("ifconfig " + interface + " up", shell=True)

print(f"Your {interface} macaddress change to {mac_address}")
subprocess.call("ifconfig", shell=True)
