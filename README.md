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
The value that you can see for docker0 is not relevant, as it seems that we can't change it.

To check the MTU value of your Docker default bridge link, you can run:

<pre>
docker network inspect --format '{{index .Options "com.docker.network.driver.mtu"}}' bridge
</pre>

You can fix the Docker daemon default bridge's MTU by creating a file /etc/docker/daemon.json and put '{"mtu": 1450}' (without single quotes) in it. Note that I've put 1450 here for the example. Set it to the value of your outgoing connection interface.

Once done, you have to restart the Docker daemon.

<pre>
systemctl restart docker
</pre>

Then, you can inspect the docker network once again with the previous command, and you should see the new value. But it doesn't affect what you run with docker-compose (I'm not sure what it really affects, BTW)! Actually, as docker0 MTU is still 1500, whenever you will run the docker-compose the first time, it will create a new network with the bridge driver, and then, this network won't have any Option in it, if not specifically defined in the networks section of the docker-compose file.

You can fix your docker-compose file the same way I did, by adding or completing the networks section:

<pre>
networks:
  default:
    driver: bridge
    driver_opts:
      com.docker.network.driver.mtu: 1450
</pre>

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

# Interactively working inside the container

## Connectivity and OpenStack CLI

By default, the docker-compose.yml has the command commented, which means that you will not have a "one shot" container, but an interactive bash session inside.
At this moment, when you arrive on the bash prompt, you can check in /etc/openstack to see the yaml clouds configuration files generated to use openstack command.
Just typing "openstack --os-cloud <YOUR_PROJECT_NAME>", you can use openstack CLI.

## Vagrant

Now, you also have the possibility of using Vagrant from within the container, thanks to the vagrant-openstack-provider plugin that I've patched to be used with CSCS (see https://github.com/crochat/vagrant-openstack-provider). A default template-like Vagrantfile is generated in /root.
You should copy it outside your container:

* Create a VM work directory

<pre>
mkdir /code/vm
</pre>

* Copy the Vagrantfile in your VM directory

<pre>
cp /root/Vagrantfile /code/vm/
</pre>

* Edit the Vagrantfile. At the top of the file, you will find some variables to set.
  * cloud: This should already contain your project name.
  * ssh_username: This must be set to the default cloud username used to reach the machine in OpenStack. Usually "ubuntu" for Ubuntu or "debian" for Debian.
  * ssh_keypair_name: This must be set to the SSH keypair configured in your OpenStack project.
  * ssh_private_key_file: In your /code folder (which is linked to the "code" folder outside of the container), you should put your SSH private key to be used to match the public key set in the SSH keypair.
* At the bottom of the file, you have the VM structure (see Vagrant to learn how to work with it).
  * You can assign floating IP by uncommenting the os.floating_ip_pool and make it match your external network name in OpenStack. Also comment out the os.floating_ip_pool_always_allocate and set it to true.
  * Alternatively, if you're running this container from within a VM already running in your OpenStack project, you can also decide not to use a floating IP, but to set a dynamic or fixed "local" IP, as defined in os.networks: "name" must match a network name defined in OpenStack, and "address" is used here as a fixed ip. If you want a DHCP IP, just comment the "address" variable.
  * As an example, I also prepared a boot volume, attached to the machine, using a specific image (which must obviously match an existing image in OpenStack), with a specific size (GB) and a "delete_on_destroy" parameter to tell OpenStack if we want this volume to be destroyed whenever we destroy the VM.

When you're done and want to create your VM, just make sure you're in the folder where you have your Vagrantfile. Vagrant works by context, and then, it's important to be in the folder where a Vagrantfile lives.

To create the VM:

<pre>
vagrant up
</pre>

To connect to the machine via ssh

<pre>
vagrant ssh
</pre>

To destroy the VM

<pre>
vagrant destroy
</pre>

Also, vagrant --help will give you more useful commands. "vagrant openstack" will give you a list of OpenStack-oriented Vagrant subcommands.
