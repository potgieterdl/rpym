#!/bin/sh

# set up rpym
unit=rpimonitor.service
unit_path="`pwd`/${unit}"

echo checking /etc/hosts for a valid statsd entry
grep statsd /etc/hosts
if [ $? -eq 0 ] 
then
	echo looks good.
else
	echo looks bad.
	exit 1
fi


#sudo apt-get -y install python-pip python-dev
#sudo pip install statsd
#sudo pip install psutil
#sudo pip install requests
#sudo pip install apscheduler

if [ -f rpimonitor.service ]
then
  echo "Installing systemd unit ${unit_path}"
  mkdir -p /opt/rpimonitor
  cp * /opt/rpimonitor
  cd /opt/rpimonitor
  systemctl link ${unit_path}
  systemctl enable ${unit}
  systemctl start ${unit}
  systemctl status ${unit}
fi
