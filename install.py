#!/usr/bin/python
import os, subprocess, sys, getpass

def run_command(command):
    if sys.version_info[0] < 3: # python 2x
        return subprocess.check_output(command, shell=True).strip().decode()
    else: # python 3x
        return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode()

# get system information
# architecture
architecture = run_command("uname -m").replace("\n", "")
# OS name. # possible OSes : debian, ubuntu, centos
OS           = run_command("lsb_release -is").replace("\n", "").lower()
# OS version # cosmic, bionic, stretch, etc...
CODENAME     = run_command("lsb_release -cs").replace("\n", "")

print ("arch: {}\nOS: {}\ncodename: {}".format(architecture, OS, CODENAME))

print('previous installations are being removed...', end='\r')
run_command('sudo apt-get remove docker docker-engine docker.io containerd runc')

print('system is being updated...', end='\r')
run_command('sudo apt-get update')

print('dependencies are being installed...', end='\r')
if OS == 'debian':
    run_command('sudo apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common')
elif OS == 'ubuntu':
    run_command('sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common')

run_command('curl -fsSL https://download.docker.com/linux/{}/gpg | sudo apt-key add -'.format(OS))

print('repository is being added...', end='\r')
if architecture in ['x86_64', 'amd64']:
    run_command('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/{} {} stable"'.format(OS, CODENAME))
else:
    run_command('sudo add-apt-repository "deb [arch={}] https://download.docker.com/linux/{} {} stable"'.format(architecture, OS, CODENAME))


print('docker is finally being installed...', end='\r')
run_command('sudo apt-get update')
run_command('sudo apt-get install -y docker-ce docker-ce-cli containerd.io')
print('permissions are being updating...', end='\r')
run_command('sudo groupadd docker')
run_command('sudo usermod -aG docker {}'.format(getpass.getuser()))
run_command('docker run hello-world')
