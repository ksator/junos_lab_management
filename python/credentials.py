
'''
get the devices credentials from ansible variables
import this function into your python scripts in order to get the devices credentials
'''

def ansible_credentials_to_python_credentials(): 
	import yaml
	from pprint import pprint as pp
	credentials_file = open('group_vars/JUNOS/credentials.yml', "r")
        credentials_file_content = credentials_file.read()
	credentials_file.close()
        credentials_file_content_in_yaml = yaml.load(credentials_file_content)
	user = credentials_file_content_in_yaml['credentials']['username']
	password = credentials_file_content_in_yaml['credentials']['password']
	credentials = {'user': user, 'password': password} 
        return credentials
