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
os.system('sudo apt remove docker docker-engine docker.io containerd runc')

print('system is being updated...', end='\r')
os.system('sudo apt update')

print('dependencies are being installed...', end='\r')
if OS == 'debian':
    os.system('sudo apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common')
elif OS == 'ubuntu':
    os.system('sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common')

os.system('curl -fsSL https://download.docker.com/linux/{}/gpg | sudo apt-key add -'.format(OS))

print('repository is being added...', end='\r')
if architecture in ['x86_64', 'amd64']:
    os.system('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/{} {} stable"'.format(OS, CODENAME))
else:
    os.system('sudo add-apt-repository "deb [arch={}] https://download.docker.com/linux/{} {} stable"'.format(architecture, OS, CODENAME))


print('docker is finally being installed...', end='\r')
os.system('sudo apt update')
os.system('sudo apt install -y docker-ce docker-ce-cli containerd.io')
print('permissions are being updating...', end='\r')
os.system('sudo groupadd docker')
os.system('sudo usermod -aG docker {}'.format(getpass.getuser()))
os.system('docker run hello-world')
