#!/usr/bin/env python3

import os
import sys
import cscs_pollux_env

pollux = cscs_pollux_env.Pollux()
pollux.connect()
pollux.select_project()

servers = pollux.get_server_status_list()
for server in servers:
    print('Server <%s>%s: %s' %(server['name'], server['msg_spacer'], server['msg']))

print('Press ENTER to initiate reboot on crashed servers, or CTRL-C to cancel')
key = pollux.wait_key()
if key != os.linesep:
    sys.exit()

for server in servers:
    if server['fail']:
        print('Initiating HARD reboot on server <%s>...' %(server['name']))
        #server['server'].reboot(reboot_type='HARD')
