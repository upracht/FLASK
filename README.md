Software bundle for Le-Tehnika cryostats

This is tested on Linux Raspberry Pi zero w+
Raspberry Pi OS lite
Debian Version 11 (bullseye)
Kernel Version 5.15.32+

Note: due to explicit path varables the root of the repository should be /home/pi should 

prepare your system:
(Assuming you are logged in as user pi and are located in /home/pi/FLASK)

1. sudo apt upgrade && sudo apt upgrade
2. sudo bash requirements.sh

-- reboot --

3. Access cryostat via 
IP address: 10.3.141.1
Username: admin
Password: secret
DHCP range: 10.3.141.50 — 10.3.141.255
SSID: raspi-webgui
Password: ChangeMe


