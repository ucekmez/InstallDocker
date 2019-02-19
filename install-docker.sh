#!/bin/sh

# docker version to be installed
DOCKER_VERSION="18.06.2"
ARCH="$(uname -m)"

# check if docker sources available
if [ ! -f src/docker.tgz ]; then
    # doker download can not be found. then download it
    sudo apt install -y curl
    url='https://download.docker.com/linux/static/stable/'"$ARCH"'/docker-'"$DOCKER_VERSION"'-ce.tgz'
    echo "docker is being downloaded"
    if [ ! -d src ]; then
      mkdir src
    fi
    wget -O src/docker.tgz $url
else
    echo "src/docker.tgz has been found!"
fi

# check if docker-compose file available
if [ ! -f src/docker-compose ]; then
    # doker download can not be found. then download it
    sudo apt install -y curl
    url='https://github.com/docker/compose/releases/download/1.23.1/docker-compose-Linux-'"$ARCH"
    echo "docker-compose is being downloaded"
    wget -O src/docker-compose $url
  else
      echo "src/docker-compose has been found!"
  fi

# we assume that now we have src/docker.tgz and docker-compose files

# open archieves to docker directory
sudo apt install -y tar
mkdir docker
tar xzvf src/docker.tgz
cp src/docker-compose docker/docker-compose

# install by copying them to /usr/bin
sudo cp docker/* /usr/bin/
sudo groupadd docker

# add docker usage rights to the $USER
sudo usermod -aG docker $USER
rm -rf docker

clear
echo "docker system has been installed successfully"




# clear the screen
#clear
