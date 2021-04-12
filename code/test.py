#!/usr/bin/env python3

import os
import sys
import cscs_pollux_env

pollux = cscs_pollux_env.Pollux()
print('Connecting...')
pollux.connect()
print('Scoped token?: %s' %(pollux.is_scoped()))

print("\nUser: %s (ID %s)" %(pollux.get_env()['OS_USERNAME'], pollux.get_user_id()))
projects = pollux.get_project_list()
projects_names = []
for project in projects:
    projects_names.append(project.name)
print("\nProject list:")
print(', '.join(projects_names))
pollux.select_project()
print('Scoped token?: %s' %(pollux.is_scoped()))

print("\nProject ID: %s" %(pollux.get_project_id()))
servers = pollux.get_server_status_list()
for details in servers:
    server = details['server']
    print('Server %s:' %(details['name']))
    print('     Status (as seen by OpenStack): %s' %(server.status))
    if details['fail']:
        print('     Real status <FAILED>: %s' %(details['err']['error']))
    security_groups = server.list_security_group()
    security_groups_list = []
    for security_group in security_groups:
        security_groups_list.append(security_group.name)
    print('     Security groups:')
    print('         '+', '.join(security_groups_list))
    print('     Networks:')
    print('         ', server.networks)
