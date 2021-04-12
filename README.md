# Requirements

In order to use it, make sure you already have docker, docker-cli and docker-compose. Also, your user could be in **docker** group, or you can use sudo.

# docker-compose.yml
## network
You can notice that a networks section has been defined, with a MTU adjusted to 1450. This is the value we have on CSCS' Pollux's OpenStack environment.

Then, if you plan to run this container on a Pollux VM, you HAVE to adjust this value, because the default MTU is 1500, which means that the IP packets
will be fragmented, resulting, in some cases, in an impossibility to reach the outside world from within a container.

In the case of Docker, this is because Docker doesn't check the MTU of the outgoing connection at startup. Therefore, the value of the Docker MTU is set
to the default one, which is 1500.

To check the MTU value of your network outgoing connection, type "ip link" and check which value is set for your outgoing (i.e. ens3) network interface.

Then, you can also see which value is set on your default Docker interface: docker0.

You can face different situations and fix them (if needed) with different ways:

- Your docker0 MTU is less than or equal to the outgoing connection interface MTU. You don't need to do anything!
- Your docker0 MTU is greater than the outgoing connection interface MTU
  - You can fix the Docker daemon's MTU. You create a file /etc/docker/daemon.json and put '{"mtu": 1450}' (without single quotes) in it. Note that I've
  put 1450 here for the example. Set it to the value of your outgoing connection interface. Once done, you have to restart the Docker daemon.
  - You can fix your docker-compose files the same way it's done here, by adding or completing the networks section.

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

## Python API client doc

| Component | OpenStack component part | Client name | Doc URL |
| --------- | ------------------------ | ----------- | ------- |
|Nova|Compute|python-novaclient|https://docs.openstack.org/python-novaclient/latest|
|Glance|Image Service|python-glanceclient|https://docs.openstack.org/python-glanceclient/latest|
|Swift|Object Storage|python-swiftclient|https://docs.openstack.org/python-swiftclient/latest|
|Keystone|Identity Service|python-keystoneclient|https://docs.openstack.org/python-keystoneclient/latest|
|Neutron|Networking|python-neutronclient|https://docs.openstack.org/python-neutronclient/latest|
|Cinder|Block Storage|python-cinderclient|https://docs.openstack.org/python-cinderclient/latest|
|Ceilometer|Telemetry|python-ceilometerclient|https://docs.openstack.org/python-ceilometerclient/pike|
|Heat|Orchestration|python-heatclient|https://docs.openstack.org/python-heatclient/latest|

# Launching container

If you don't know how to use docker or docker-compose, you can simply run **./run.sh**
