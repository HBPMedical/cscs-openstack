#!/usr/bin/env python3

import os
import sys
import cscs_pollux_env

pollux = cscs_pollux_env.Pollux()
pollux.connect()
pollux.select_project()

servers = pollux.get_server_status_list()
for server in servers:
    print('Server <%s>%s: %s (OpenStack Status: %s)' %(server['name'], server['msg_spacer'], server['msg'], server['server'].status))

goahead = False
print('Press ENTER to review crashed servers, or any other key to skip this step')
key = pollux.wait_key()
if key == os.linesep:
    goahead = True

if goahead:
    other_servers = []
    for server in servers:
        if server['fail']:
            print('Reboot server <%s> [y/n]?' %(server['name']))
            key = pollux.wait_key()
            if key.lower() == 'y':
                print('Initiating HARD reboot on server <%s>...' %(server['name']))
                server['server'].reboot(reboot_type='HARD')
        else:
            other_servers.append(server)

goahead = False
print('Press ENTER to review not necessarily crashed servers, or any other key to skip this step')
key = pollux.wait_key()
if key == os.linesep:
    goahead = True

if goahead:
    for server in other_servers:
        print('Reboot server <%s> [y/n]?' %(server['name']))
        key = pollux.wait_key()
        if key.lower() == 'y':
            print('Initiating HARD reboot on server <%s>...' %(server['name']))
            server['server'].reboot(reboot_type='HARD')
