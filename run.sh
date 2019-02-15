#!/bin/sh

# install pip
if command -v python3 &>/dev/null; then
  echo "python3 found"
  sudo apt install -y python3-pip
  pip3 install -r requirements.txt --user
  sudo python3 install.py
else
  sudo apt install -y python-pip
  pip install -r requirements.txt  --user
  sudo python install.py
fi
