#!bin/bash
sleep 46
ip=$(hostname -I | cut -f1 -d ' ')
while : 
	do
		curl -s "$ip:13378/sample" &> /dev/null
		sleep 60
	done
