#!bin/bash

ip=$(hostname -I | cut -f1 -d ' ')
curl -s "$ip:13378/vacuum_performance_test" & > /dev/null
