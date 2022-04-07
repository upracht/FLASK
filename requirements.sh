#!/bin/bash

yes | apt install python3-pip
yes | apt install  libatlas-base-dev

pip3 install numpy
pip3 install matplotlib
pip3 install scipy
pip3 install pi-ina219
pip3 install pyserial
pip3 install flask
pip3 install flask-restful
pip3 install pymodbus
pip3 install requests 
pip3 install adafruit-python-shell

wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
python3 raspi-blinka.py
pip3 install adafruit-circuitpython-max31865
pip3 install adafruit-circuitpython-fxas21002c
pip3 install adafruit-circuitpython-fxos8700
rm raspi-blinka.py


path=$(pwd)
cronjob="@reboot bash $path/app-init.sh"
(crontab -u supramotion -l; echo "$cronjob") | crontab -u supramotion -

cronjob="@reboot bash $path/log-init.sh"
(crontab -u supramotion -l; echo "$cronjob") | crontab -u supramotion -

cronjob="0 0 * * * bash $path/vacuum.sh"
(crontab -u supramotion -l; echo "$cronjob") | crontab -u supramotion -

curl -sL https://install.raspap.com > AP.sh
bash AP.sh -y
rm AP.sh

echo "___________"
echo "System preparation finished
echo "After reboot, connect to raspi-webgui netowrk (psw ChangeMe)"
echo "and access the cryostat at https://10.3.141.1:13378/user (this is the default)"
echo "You may change network settings at https://10.3.141.1 (Username: admin Password: secret)"
