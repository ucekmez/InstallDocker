#!/usr/bin/python
import os, shutil, requests, sys, urllib.request
from tqdm import tqdm

# possible architectures: aarch64 armel armhf ppc64le s390x x86_64
ARCH           = "x86_64"
DOCKER_VERSION = "18.06.2"


####################### create tmp directory and download given version
#######################
try:
    os.mkdir("tmp")
except:
    shutil.rmtree("tmp")
    os.mkdir("tmp")
finally:
    sys.stdout.write("\rtmp directory initialized")

url = 'https://download.docker.com/linux/static/stable/{}/docker-{}-ce.tgz'.format(ARCH, DOCKER_VERSION)
file_name = "docker-{}-ce.tgz".format(DOCKER_VERSION)

sys.stdout.write('\r')
print('\rDocker version {}-ce is being downloaded...\n'.format(DOCKER_VERSION))

####################### download functions
#######################

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

download_url(url, "tmp/"+file_name)
sys.stdout.write('\r')

####################### send files to remote machine and extract them
#######################


CMD_extract = "tar xzvf docker-{}-ce.tgz".format(DOCKER_VERSION)
CMD_move    = "sudo cp docker/* /usr/bin/"
CMD_start   = "sudo dockerd &"
CMD_test    = "sudo docker run hello-world"

CMD_all     = "{} && {} && {} {}".format(CMD_extract, CMD_move, CMD_start, CMD_test)

print("""
    You have to process the following steps:
        - send tmp/docker-{}-ce.tgz file to your remote server
        - run the following command pipeline:
            {}
""".format(DOCKER_VERSION, CMD_all))
