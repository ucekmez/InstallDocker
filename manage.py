#!/usr/bin/python
import sys, os

DOCKER_REGISTRY = "repo.acip.io"

if len(sys.argv) > 1:
    # sys.argv[1] : command
    if sys.argv[1] == "login":
        username = sys.argv[2]
        password = sys.argv[3]
        os.system("docker login -u {} -p {} {}".format(username, password, DOCKER_REGISTRY))
    if sys.argv[1] == "pull":
        image_label = sys.argv[2]
        image_label = image_label if DOCKER_REGISTRY+"/" in image_label else "{}/{}".format(DOCKER_REGISTRY,image_label)
        os.system("docker pull {}".format(image_label))
        os.system("docker save -o {}.tar {}".format(image_label.split("/")[1], image_label))
    if sys.argv[1] == "push":
        image_label = sys.argv[2]
        image_label = image_label if DOCKER_REGISTRY+"/" in image_label else "{}/{}".format(DOCKER_REGISTRY,image_label)
        #os.system("docker manifest inspect {} > /dev/null ; echo $?".format(image_label))
        os.system("docker push {}".format(image_label))
