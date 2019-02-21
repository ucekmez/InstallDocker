# InstallDocker

## usage:

sudo ./prepare -r [OPTIONS] 
sudo ./prepare help ( for a short documentation )

## notes

With this script, Docker engine bundle can be prepared for any kind of CPU architecture.
(possible architectures: aarch64 armel armhf ppc64le s390x x86_64)

After the bundle.tar.gz is prepared, you can send the bundle to the corresponding IoT/remote/offline device.
In the device, open the tar and type the following command:

$> sudo ./install

After everything is OK, then you will be able to load docker images as tar files.
For this purpose, use ./manage-docker script

## manage-docker
In your local machine:
 - run './manage-docker pull image_name' (saves your docker image as image.tar)
 - sen this tar file to your device

In your device:
 - (assuming that you have already installed bundle.tar.gz)
 - run 'manage-docker load PATH/TO/IMAGE/image.tar' (loads image.tar as a docker image)
 - then you are good to go
 - run 'docker run image_label --parameters'
