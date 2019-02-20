# InstallDocker

## usage:

sudo ./prepare -r [OPTIONS]
sudo ./prepare help ( for a short documentation )

## notes

With this script, Docker engine bundle can be prepared for any kind of cpu architecture.

After the bundle.tar.gz is prepared, you can send the bundle to the corresponding IoT device.
In the device, open the tar and type the following command:

$> sudo ./install
