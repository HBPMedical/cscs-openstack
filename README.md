# docker-compose.yml
## environment

Just replace variables in docker-compose.yml. You can also set environment variables.

With these variables, you can directly use the container with your credentials and your project, and be immediately able to use it, without having to complete any further authentication.

- **OS_USERNAME**
- **OS_PASSWORD**
- **OS_PROJECT_NAME**

If you don't provide anything, you will have to answer corresponding questions inside the container.

You can also put a session token instead of the password, and override other default values if you want:

- OS_TOKEN
- OS_AUTH_URL
- OS_IDENTITY_API_VERSION
- OS_IDENTITY_PROVIDER
- OS_IDENTITY_PROVIDER_URL
- OS_PROTOCOL
- OS_INTERFACE
- OS_REGION_NAME
- OS_COMPUTE_API_VERSION

## command

If you don't put any command, you'll have a bash, where you can call your scripts directly. You can also call **openstack-cli**, to have a ready-to-use OpenStack shell to manage your project.

If you want your script to be called immediately, just put it in **command:** line.

# Scripts

You can put all your Python 3 scripts in the **code** folder, which is also a mounted volume from within the container. Then, once inside the container, you'll be by default in **/code**, and you'll be able to execute your scripts directly with "./script.py"

With simple lines on top of your script, you can directly use the provided environment:

<pre>
#!/usr/bin/env python3

import cscs_pollux_env

pollux = cscs_pollux_env.Pollux()
pollux.connect()
pollux.select_project()
</pre>
