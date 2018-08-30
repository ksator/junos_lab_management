# About this repo

This repository has automation content to manage a lab with Junos devices.

# Repository structure 

### Ansible inventory file
The ansible inventory file is [**hosts**](hosts) file at the root of the repository.    

### Ansible configuration file
The ansible configuration file is [**ansible.cfg**](ansible.cfg) at the root of the repository.   

### variables 
The variables are yml files under the [**group_vars**](group_vars) directory.  

### Ansible Playbooks
The ansible playbooks are at the root of the repository.  
All playbooks are named **pb.*.yml**      

### cli directory 
The directory [**cli**](cli) has the output of the Junos show commands from the playbook [**pb.collect.cli.yml**](pb.collect.cli.yml)

### configuration directory
The directory [**configuration**](configuration) has the junos configuration files backed up when we ran the playbook [**pb.collect.configuration.yml**](pb.collect.configuration.yml) 

### backup directory
The directory [**backup**](backup) has the junos configuration files automatically backed up by the playbooks: 
  - [**pb.configure.lines.yml**](pb.configure.lines.yml) 
  - [**pb.configure.golden.yml**](pb.configure.golden.yml)

### golden.configuration directory
The directory [**golden_configuration**](golden_configuration) has the junos configuration files for various demo.
- The playbook [**pb.collect.golden.configuration.yml**](pb.collect.golden.configuration.yml) collects the running configuration on the junos devices and updates the directory [**golden.configuration**](golden_configuration) with these files.
- The playbook [**pb.deploy.golden.yml**](pb.deploy.golden.yml) overwrites the running configuration on the junos devices with the files in the directory [**golden_configuration**](golden_configuration)

### python directory
The directory [**python**](python) has the python scripts
- The file [**inventory.py**](python/inventory.py) creates a python list of devices ip address based on the ansible inventory file [**hosts**](hosts)
- The file [**credentials.py**](python/credentials.py) gets the devices username and password from the ansible variables file  [**credentials.yml**](/group_vars/JUNOS/credentials.yml)
- The file [**locate.mac.address.py**](python/locate.mac.address.py) indicates where a given mac address in the network is located.

# Usage

### How to locate a mac address

Execute this [**python script**](python/locate.mac.address.py) to locate a mac address in the network
```
python ./python/locate.mac.address.py ac:1f:6b:8d:c4:52
```

### How to collect junos show commands 

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

### How to collect the junos configuration files

The playbook [**pb.collect.configuration.yml**](pb.collect.configuration.yml) collects the Junos configuration in set, xml, json and text formats, and saves the configuration files in the [**directory configuration**](configuration)  

Run this command to collect the junos configuration files for a device/group.  
```
ansible-playbook pb.collect.configuration.yml --limit QFX5100
```

Run this command to collect the junos configuration files for the whole network
```
ansible-playbook pb.collect.configuration.yml
```

The configuration files are available in the directory [**configuration**](configuration)
```
ls configuration/
```

### How to collect the running configuration on the junos devices and update the golden configuration files

The golden configuration files are the configuration files that will be loaded at the beginning of each demo. 

The playbook [**pb.collect.golden.yml**](pb.collect.golden.yml) collects the running configuration on the junos devices and updates the directory [**golden_configuration**](golden_configuration) with these files.

Run this command to do it for a device/group
```
ansible-playbook pb.collect.golden.yml --limit QFX5110
```

Run this command to do it for the whole network
```
ansible-playbook pb.collect.golden.yml 
```

The golden configuration files are available in the directory [**golden_configuration**](golden_configuration)
```
ls golden_configuration
```


### Looking for more Junos automation examples:

https://github.com/ksator?tab=repositories  
https://gitlab.com/users/ksator/projects  
https://gist.github.com/ksator/  












### Clone the repository:
```
git clone https://github.com/ksator/xxxxxx.git
cd xxxxx/
pip install -r requirements.txt
```
###


### Install requirements: 

From ubuntu 16.04

```
sudo apt-get update
sudo apt-get upgrade
sudo pip install requirements.txt -r 
ansible-galaxy install Juniper.junos,2.1.0
```
Verify:
```
ansible --version
ansible-galaxy Juniper.junos list
pip list
```



