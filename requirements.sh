#!/bin/bash


echo "This routine prepares your System to run the SupraMotion Cryostat Software Suite"
echo "It is highly automated and does not require user input."
echo "Checking, if the system needs to reboot first ..."
if [ -f /var/run/reboot-required ]; then
  echo '... reboot required'
  sleep 2
  reboot
fi

version=$(uname -srm | cut -f2 -d ' ' )
if ! [[ -d /lib/modules/$version ]]; then
   echo '... reboot required'
   sleep 2
   reboot
fi


yes | apt install python3-pip
yes | apt install  libatlas-base-dev
yes | apt install  libjpeg-dev

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
user=$(whoami)

cronjob="@reboot python3 $path/app.py"
(crontab -u $user -l; echo "$cronjob") | crontab -u $user -

cronjob="@reboot bash $path/log.sh"
(crontab -u $user -l; echo "$cronjob") | crontab -u $user -

cronjob="0 0 * * * bash $path/vacuum.sh"
(crontab -u $user -l; echo "$cronjob") | crontab -u $user -


curl -sL https://install.raspap.com > AP.sh
bash AP.sh -y
rm AP.sh

mkdir log


echo "___________"
echo "System preparation finished"
echo "After reboot, connect to raspi-webgui netowrk (psw ChangeMe)"
echo "and access the cryostat at https://10.3.141.1:13378/user (this is the default)"
echo "You may change network settings at https://10.3.141.1 (Username: admin Password: secret)"
