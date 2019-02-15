#!/usr/bin/python
import os, shutil, sys, urllib.request, subprocess, getpass
from tqdm import tqdm

def initialize_tmp():
    os.system("clear")
    try:
        os.mkdir("tmp")
    except:
        shutil.rmtree("tmp")
        os.mkdir("tmp")
    finally:
        sys.stdout.write("\rtmp directory initialized")

def run_command(command):
    if sys.version_info[0] < 3: # python 2x
        return subprocess.check_output(command, shell=True).strip().decode()
    else: # python 3x
        return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode()

def download_url(url, file_name):
    sys.stdout.write('\r')
    print('\rdocker is being downloaded...\n')

    class DownloadProgressBar(tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)


    def download(url, output_path):
        with DownloadProgressBar(unit='B', unit_scale=True,
                                 miniters=1, desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


#######################  docker version to be installed
DOCKER_VERSION = "18.06.2"

################## 1st step: install docker into local machine #################
################################################################################
#######################  get local system information
LOCAL_ARCH = run_command("uname -m").replace("\n", "")

####################### create tmp directory and download given version
initialize_tmp()

####################### download docker
url = 'https://download.docker.com/linux/static/stable/{}/docker-{}-ce.tgz'.format(LOCAL_ARCH, DOCKER_VERSION)
target_name = "docker-{}-ce.tgz".format(DOCKER_VERSION)

download_url(url, "tmp/"+target_name)

####################### open tar and add docker-compose inside
os.system("tar xzvf tmp/docker-{}-ce.tgz --directory tmp/".format(DOCKER_VERSION))
os.system("clear")
print('\rdocker-compose is being downloaded...\n')
download_url("https://github.com/docker/compose/releases/download/1.23.1/docker-compose-Linux-{}".format(LOCAL_ARCH), "tmp/docker/docker-compose")
os.system("chmod +x tmp/docker/docker-compose")
sys.stdout.write('\rmaking a new package...')
os.system("rm tmp/docker-{}-ce.tgz".format(DOCKER_VERSION))
os.system("tar -zcvf tmp/docker-{}-ce.tar.gz -C tmp/ docker".format(DOCKER_VERSION))
os.system("clear")

####################### install docker inside local machine
os.system("sudo cp tmp/docker/* /usr/bin/")
os.system("sudo groupadd docker")
os.system("sudo usermod -aG docker $USER")
os.system("rm -rf tmp/docker")


############ 2nd step: prepare docker installation for remote machine ##########
################################################################################


# possible architectures: aarch64 armel armhf ppc64le s390x x86_64
REMOTE_ARCH    = sys.argv[1] if len(sys.argv) > 1 else  "x86_64"

####################### create tmp directory and download given version
initialize_tmp()

####################### download docker
url = 'https://download.docker.com/linux/static/stable/{}/docker-{}-ce.tgz'.format(REMOTE_ARCH, DOCKER_VERSION)
target_name = "docker-{}-ce.tgz".format(DOCKER_VERSION)

download_url(url, "tmp/"+target_name)

####################### open tar and add docker-compose inside
os.system("tar xzvf tmp/docker-{}-ce.tgz --directory tmp/".format(DOCKER_VERSION))
os.system("clear")
print('\rdocker-compose is being downloaded...\n')
download_url("https://github.com/docker/compose/releases/download/1.23.1/docker-compose-Linux-{}".format(REMOTE_ARCH), "tmp/docker/docker-compose")
os.system("chmod +x tmp/docker/docker-compose")
sys.stdout.write('\rmaking a new package...')
os.system("rm tmp/docker-{}-ce.tgz".format(DOCKER_VERSION))
os.system("tar -zcvf tmp/docker-{}-ce.tar.gz -C tmp/ docker".format(DOCKER_VERSION))
os.system("rm -rf tmp/docker")
os.system("clear")




####################### send files to remote machine and extract them

CMD_extract = "sudo tar xzvf docker-{}-ce.tgz".format(DOCKER_VERSION)
CMD_move    = "sudo cp docker/* /usr/bin/"
CMD_group   = "sudo groupadd docker"
CMD_perm    = "sudo usermod -aG docker $USER"

CMD_all     = "{} && {} && {} && {}".format(CMD_extract, CMD_move, CMD_group, CMD_perm)

print("""
    You have to process the following steps:
        - send tmp/docker-{}-ce.tgz file to your remote server
        - run the following command pipeline:
            {}
        - copy docker.service => /etc/systemd/system/docker.service
        - run the following command pipeline
            sudo systemctl enable docker && sudo systemctl start docker
""".format(DOCKER_VERSION, CMD_all))
