#!/bin/sh

adduser --ingroup nogroup --shell /etc/false --disabled-password --gecos "" --no-create-home mongodb

mkdir /var/log/mongodb
chown mongodb:nogroup /var/log/mongodb

mkdir /var/lib/mongodb
chown mongodb:root /var/lib/mongodb
chmod 775 /var/lib/mongodb

git clone https://github.com/robertsLando/MongoDB-OrangePI.git

cd MongoDB-OrangePI
cp mongodb.conf /etc
cp mongodb.service /lib/systemd/system

cd bin
chown root:root mongo*
chmod 755 mongo*
cp -p mongo* /usr/bin

systemctl start mongodb
systemctl status mongodb

sudo systemctl enable mongodb

# Si besoin de réparer la base...
#sudo -u mongodb mongod --repair --dbpath /var/lib/mongodb/
#sudo service mongodb restart