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

cronjob="@reboot bash /home/supramotion/app-init.sh"
(crontab -u supramotion -l; echo "$cronjob") | crontab -u supramotion -

cronjob="@reboot bash /home/supramotion/log-init.sh"
(crontab -u supramotion -l; echo "$cronjob") | crontab -u supramotion -

cronjob="0 0 * * * bash /home/supramotion/vacuum.sh"
(crontab -u supramotion -l; echo "$cronjob") | crontab -u supramotion -
