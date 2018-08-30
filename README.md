## About this repo
This repository has automation content to manage a lab with Junos devices.

## Repository structure
- [ansible inventory file](hosts)
- [group specific variables](group_vars)

## Usage 

### Install requirements: 

From ubuntu 16.04

```
sudo apt-get update
sudo apt-get upgrade
sudo pip install ansible==2.5.2.0 junos-eznc jxmlease jsnapy
ansible-galaxy install Juniper.junos,2.1.0
```
Verify:
```
ansible --version
ansible-galaxy Juniper.junos list
pip list
```
### Clone the repository: 
```
git clone https://github.com/ksator/xxxxxx.git
cd xxxxx/
pip install -r requirements.txt
```
### 




