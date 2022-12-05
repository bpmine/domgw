#!/bin/sh

## Installation de npm, nodejs et pm2

curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -

apt-get install -y nodejs
apt-get install gcc g++ make
npm install -g pm2

pm2 startup


#pm2 start --name <Nom du service pm2> --interpreter <interpreteur> <Script a executer> 
#Exemple:
#pm2 start --name demo --interpreter python3 /root/iscl/demo_ws.py
