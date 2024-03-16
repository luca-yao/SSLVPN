# Editer : Luca_yao
# E-mail : stelliva42@gmail.com
# Date : 2024/02/06

import os, re
from netmiko import ConnectHandler
from mac_list import main

def connect_to_fortigate(device_info):
    try:
        log_file_path = f"netmiko.log"
        net_connect = ConnectHandler(**device_info, session_log=log_file_path)
        print("Connected to FortiGate device")
        return net_connect
    except Exception as e:
        print(f"Error connecting to FortiGate: {e}")
        return None

def configure_sslvpn_portal(net_connect, portal_name, mac_addr_list):
    try:
        commands = [
            'config vpn ssl web portal',
            f'edit {portal_name}',
            'config mac-addr-check-rule',
            f'edit "VPN_{file_name}"',
            f'set mac-addr-list {mac_addr_list}',
            'show',
            'next',  
            'end',  
        ]
        for command in commands:
            output = net_connect.send_command_timing(command)
        print(output)

    except Exception as e:
        print(f"Error configuring SSL VPN Portal: {e}")

    finally:
        if net_connect:
            net_connect.disconnect()
            print("Disconnected from FortiGate device")

fortigate_device = {
    'device_type': 'fortinet',
    'ip': 'xxx.xxx.xxx.xxx',
    'username': 'username',
    'password': 'password',
    'port': 22, 
}

file_name = input()
file_path = os.path.join("List", file_name)

net_connection = connect_to_fortigate(fortigate_device)

if net_connection:
    sslvpn_portal_name = f'SSLVPN_{file_name}_Portal'
    mac_addr_list = main(file_path)
    configure_sslvpn_portal(net_connection, sslvpn_portal_name, mac_addr_list)