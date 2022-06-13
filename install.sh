#!/bin/bash
echo "TI4 Installation"
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

if ! uname -a | grep -q Ubuntu; then
    echo 'This script are designed for ubuntu only'
    exit 1
fi


echo "Please input your hostname"
read -r tiHostname

echo "Installing Dependencies"
apt-get update
apt-get install python3-pip python3-dev nginx
pip3 install virtualenv
virtualenv venv

source venv/bin/activate
venv/bin/pip3 install -r requirements.txt

echo "Installing Services"

sed -e "s:<pwd>:$(pwd):g" -e "s:<user>:$USER:g" ./daemon/ti3-get.service | tee /etc/systemd/system/ti-3-get.service
sed -e "s:<pwd>:$(pwd):g" -e "s:<user>:$USER:g" ./daemon/ti3-update.service | tee /etc/systemd/system/ti-3-update.service

systemctl daemon-reload

systemctl start ti-3-get.service
systemctl enable ti-3-get.service

systemctl start ti-3-update.service
systemctl enable ti-3-update.service

mkdir nginx-cache

sed -e "s:<pwd>:$(pwd):g" -e "s/<host>/$tiHostname/g" ./nginx.conf | tee "/etc/nginx/sites-available/$tiHostname" > /dev/null
ln -s "/etc/nginx/sites-available/$tiHostname" "/etc/nginx/sites-enabled" > /dev/null
systemctl restart nginx