#!/bin/sh

APD_NAME="DOMGW"
HOST_NAME=$APD_NAME

set -e

apt-get update -y
apt-get upgrade -y

apt-get install dnsmasq -y
apt-get install hostapd -y
apt-get install vim -y

echo "$HOST_NAME" > /etc/hostname

echo "interface=wlan0" > /etc/hostapd/hostapd.conf
echo "ssid=$APD_NAME" >> /etc/hostapd/hostapd.conf
echo "hw_mode=g" >> /etc/hostapd/hostapd.conf
echo "channel=7" >> /etc/hostapd/hostapd.conf
echo "country_code=FR" >> /etc/hostapd/hostapd.conf
#echo "auth_algs=0" >> /etc/hostapd/hostapd.conf

# Reference hostapd script into default one
sed -i 's/#DAEMON_CONF=\"\"/DAEMON_CONF=\/etc\/hostapd\/hostapd.conf/' /etc/default/hostapd

echo "interface=wlan0" > /etc/dnsmasq.conf 
echo "dhcp-range=192.168.2.50, 192.168.2.200, 255.255.255.0, 24h" >> /etc/dnsmasq.conf 

echo "auto lo" > /etc/network/interfaces
echo "iface lo inet loopback" >> /etc/network/interfaces

echo "auto eth0" >> /etc/network/interfaces
echo "allow-hotplug eth0" >> /etc/network/interfaces
echo "iface eth0 inet dhcp" >> /etc/network/interfaces

echo "auto wlan0" >> /etc/network/interfaces
echo "allow-hotplug wlan0" >> /etc/network/interfaces
echo "iface wlan0 inet static" >> /etc/network/interfaces
echo "address 192.168.2.1/24" >> /etc/network/interfaces
echo "gateway 192.168.1.1/24" >> /etc/network/interfaces

systemctl unmask dnsmasq
systemctl enable dnsmasq

systemctl unmask hostapd
systemctl enable hostapd

# Enable IP forwarding
sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

apt-get install mysql-server -y

mysql -e "CREATE USER 'iscl'@'%' IDENTIFIED BY 'iscl';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'iscl'@'%';"
mysql -e "FLUSH PRIVILEGES;"

# Allow distant clients
#sed -i 's/bind-address.+/bind-address=0.0.0.1/p' /etc/mysql/mariadb.conf.d/50-server.cnf
# Dans /etc/mysql/mariadb.conf.d/50-server.cnf
# bind-address=0.0.0.0
#
# En cas de difficulte persistante de connexion, ajouter la ligne suivante:
# skip-name-resolve
#
#

echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list
apt-get update
apt-get install rabbitmq-server -y
rabbitmq-plugins enable rabbitmq_management
rabbitmq-plugins enable rabbitmq_mqtt

rabbitmqctl add_user admin domotique
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions admin ".*" ".*" ".*"


apt-get install python3 -y
apt-get install python3-pip -y
python3 -m pip install requests
python3 -m pip install pyserial
python3 -m pip install pymodbus
python3 -m pip install flask
python3 -m pip install mysql-connector-python
python3 -m pip install pymongo
python3 -m pip install python-dateutil



