# About this repo

This repository has automation content to manage a lab with Junos devices.

# Repository structure 

- The ansible inventory file is [**hosts**](hosts)  
- The ansible configuration file is [**ansible.cfg**](ansible.cfg)
- The variables are yml files under the [**group_vars**](group_vars) directory.  
- The ansible playbooks are at the root of the repository. All playbooks are named **pb.*.yml**      
- The directory [**cli**](cli) has the output of the Junos show commands collected from the playbook [**pb.collect.cli.yml**](pb.collect.cli.yml)
- The directory [**configuration**](configuration) has the junos configuration files collected when we run the playbook [**pb.collect.configuration.yml**](pb.collect.configuration.yml) 
- The directory [**backup**](backup) has the junos configuration files automatically backed up by the playbooks: 
  - [**pb.configure.lines.yml**](pb.configure.lines.yml) 
  - [**pb.deploy.golden.yml**](pb.deploy.golden.yml)
- The directory [**golden_configuration**](golden_configuration) has the junos configuration files for various demo.
  - The playbook [**pb.collect.golden.configuration.yml**](pb.collect.golden.configuration.yml) collects the running configuration on the junos devices and updates the directory [**golden.configuration**](golden_configuration) with these files.
  - The playbook [**pb.deploy.golden.configuration.yml**](pb.deploy.golden.configuration.yml) overwrites the running configuration on the junos devices with the files in the directory [**golden_configuration**](golden_configuration)
- The directory [**python**](python) has the python scripts
   - The file [**inventory.py**](python/inventory.py) creates a python list of devices ip address based on the ansible inventory file [**hosts**](hosts)
   - The file [**credentials.py**](python/credentials.py) gets the devices username and password from the ansible variables file  [**credentials.yml**](/group_vars/JUNOS/credentials.yml)
   - The file [**locate.mac.address.py**](python/locate.mac.address.py) indicates where a given mac address in the network is located.

# Requirements to use this repository

### Clone the repository 


```
git clone https://github.com/ksator/junos_lab_management.git
cd junos_lab_management/
```
### Install requirements
```
sudo pip install requirements.txt -r 
sudo ansible-galaxy install Juniper.junos,2.1.0
```
### Verify
```
ansible --version
ansible-galaxy Juniper.junos list
pip list
```
# How to use this repository

### Locate a mac address

Execute this [**python script**](python/locate.mac.address.py) to locate a mac address in the network
```
python ./python/locate.mac.address.py ac:1f:6b:8d:c4:52
```

### check if some services are reachable on Junos devices

The playbook [**pb.check.reachability.yml**](pb.check.reachability.yml) checks if Ansible can connect on some ports on Junos devices (ssh, telnet, ftp, netconf)  
Run this command to execute this playbook for the whole network:
```
ansible-playbook pb.check.reachability.yml
```

### Collect the facts on junos devices and print them on the Ansible server

The playbook [**pb.print.facts.yml**](pb.print.facts.yml) collects the facts on junos devices and prints them on the Ansible server. 
Run this command to execute this playbook for the whole network:
```
ansible-playbook pb.print.facts.yml
```

### Collect junos show commands 

Edit the [**cli.yml**](group_vars/JUNOS/cli.yml) file to indicate the list of junos show commands you want to collect
```
vi group_vars/JUNOS/cli.yml
```

Run this command to execute the [**pb.collect.cli.yml**](pb.collect.cli.yml) playbook.  
It runs the junos show commands from the [**cli.yml**](group_vars/JUNOS/cli.yml) file and saves the output on the Ansible server in the [**cli**](cli) directory. 
```
ansible-playbook pb.collect.cli.yml
```

The junos show commands output is available in the [**cli**](cli) directory 
```
ls cli
```

### Collect the junos configuration files

The playbook [**pb.collect.configuration.yml**](pb.collect.configuration.yml) collects the Junos configuration in set, xml, json and text formats, and saves the configuration files in the directory [**configuration**](configuration)  

Run this command to collect the junos configuration files for a device/group.  
```
ansible-playbook pb.collect.configuration.yml --limit QFX10K2
```

Run this command to collect the junos configuration files for the whole network
```
ansible-playbook pb.collect.configuration.yml
```

The configuration files are available in the directory [**configuration**](configuration)
```
ls configuration
```

### Update the golden configuration files

The playbook [**pb.collect.golden.configuration.yml**](pb.collect.golden.configuration.yml) collects the running configuration on the junos devices and updates the directory [**golden_configuration**](golden_configuration) with these files.

Example 1: 
Run this command to collect the configuration running on the junos devices and updates the directory [**golden_configuration/bgp**](golden_configuration/bgp) with these files.
```
ansible-playbook pb.collect.golden.configuration.yml --extra-vars lab=bgp
```
The golden configuration files are available in the directory [**golden_configuration/bgp**](golden_configuration/bgp)
```
ls golden_configuration/bgp
```
Example 2: 
Run this command to collect the running configuration on the junos devices and updates the directory [**golden_configuration/ospf**](golden_configuration/ospf) with these files.
```
ansible-playbook pb.collect.golden.configuration.yml --extra-vars lab=ospf
```
The golden configuration files are available in the directory [**golden_configuration/ospf**](golden_configuration/ospf)
```
ls golden_configuration/ospf
```


### Overwrite the running configuration on junos devices with a golden configuration

The playbook [**pb.deploy.golden.configuration.yml**](pb.deploy.golden.configuration.yml) overwrites the running configuration on the junos devices with the files in the directory [**golden_configuration**](golden_configuration).  

Example 1: 
Run this command to overwrite the running configuration on the junos devices with the files in the directory [**golden_configuration/bgp**](golden_configuration/bgp).  
```
ansible-playbook pb.deploy.golden.configuration.yml --extra-vars lab=bgp
```

Example 2: 
Run this command to overwrite the running configuration on the junos devices with the files in the directory [**golden_configuration/ospf**](golden_configuration/ospf).  
```
ansible-playbook pb.deploy.golden.configuration.yml --extra-vars lab=ospf
```

The playbook [**pb.deploy.golden.configuration.yml**](pb.deploy.golden.configuration.yml) backs-up the current running configuration from the remote devices in the directory [**backup**](backup) before applying the golden configuration. 
``` 
ls backup/
```

### Check which devices are not running their golden configuration

In order to know which junos devices will have a configuration change if you load the golden configuration files, execute the playbook [pb.deploy.golden.configuration.yml](pb.deploy.golden.configuration.yml) in dry run mode.
This won’t load the golden configuration.

```
ansible-playbook pb.deploy.golden.configuration.yml --extra-vars lab=ospf --check
```
Run this command to do it for one device/group. 
This won’t load the golden configuration.

```
ansible-playbook pb.deploy.golden.configuration.yml --extra-vars lab=ospf -check --limit demo-qfx10k2-11
```

### Get the difference between the configuration running on devices and their golden configuration

In order to know if a junos device will have a configuration change if you load its golden configuration file, and also to know the difference between its running configuration and its golden configuration, run this command.
This won’t change the junos configuration.
```
ansible-playbook pb.deploy.golden.configuration.yml --extra-vars lab=bgp --check --diff --limit demo-qfx10k2-11
```
Run this command to do it for the whole network.
This won’t load the golden configuration.
```
ansible-playbook pb.deploy.golden.configuration.yml --extra-vars lab=bgp --check --diff 
```

### Configure junos devices with set/delete commands

The playbook [**pb.configure.lines.yml**](pb.configure.lines.yml) configures the junos devices with set/delete commands. 

Edit the playbook [**pb.configure.lines.yml**](pb.configure.lines.yml) to indicate the list of set and delete commands you want to use:
```
vi pb.configure.lines.yml
```

In order to know which junos devices would have a configuration change if you execute the playbook [**pb.configure.lines.yml**](pb.configure.lines.yml), execute it in dry run mode.  
This won’t change the junos configuration.  
```
ansible-playbook pb.configure.lines.yml --check
```

In order to know if a junos device will have a configuration change if you execute the playbook [**pb.configure.lines.yml**](pb.configure.lines.yml), and also to know the difference between the desired state described in the playbook [**pb.configure.lines.yml**](pb.configure.lines.yml) and the device actual state, run this command.  
This won’t change the junos configuration.  
```
ansible-playbook pb.configure.lines.yml --check --diff --limit demo-qfx10k2-11
```

Run this command to execute the playbook [**pb.configure.lines.yml**](pb.configure.lines.yml) for one device/group.  
This will configure the device/group with the list of set/delete commands. 
```
ansible-playbook pb.configure.lines.yml --limit QFX10K2
```

Run this command to execute the playbook [**pb.configure.lines.yml**](pb.configure.lines.yml).  
This will configure the whole network with the list of set/delete commands. 
```
ansible-playbook pb.configure.lines.yml
```

The playbook [**pb.configure.lines.yml**](pb.configure.lines.yml) backs-up the current running configuration from the remote devices in the directory [**backup**](backup) before applying the configuration change. 
```
ls backup/
```

### rollback the running configuration to a previous version

The playbook [**pb.rollback.yml**](pb.rollback.yml) performs a configuration rollback on junos devices.

Run this command to rollback 1 the whole network 
```
ansible-playbook pb.rollback.yml --extra-vars rbid=1
```

Run this command to rollback 3 the group MX80 
```
ansible-playbook pb.rollback.yml --extra-vars rbid=3 --limit MX80
```

### Zeroize your network

The playbook [**pb.zeroize.yml**](pb.zeroize.yml) zeroizes the network. 

Run this command to zeroize a device or a group
```
ansible-playbook pb.zeroize.yml --limit demo-qfx10k2-11
```

Run this command to zeroize the whole network 
```
ansible-playbook pb.zeroize.yml 
```

### Reboot Junos devices 

The playbook [**pb.reboot.junos.yml**](pb.reboot.junos.yml) reboots Junos devices.  
This is the equivalent of the ```request system reboot``` CLI command.

Run this command to reboot a device
```
ansible-playbook pb.reboot.junos.yml --extra-vars target=demo-qfx5100-8
```

Run this command to reboot a group of devices
```
ansible-playbook pb.reboot.junos.yml --extra-vars target=QFX
```

Run this command to reboot all Junos devices
```
ansible-playbook pb.reboot.junos.yml --extra-vars target=JUNOS
```



### Looking for more Junos automation examples:

https://github.com/ksator?tab=repositories  
https://gitlab.com/users/ksator/projects  
https://gist.github.com/ksator/  
