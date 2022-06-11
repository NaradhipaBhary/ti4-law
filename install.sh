echo "TI4 Installation"
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Please input your hostname"
read -r tiHostname

echo "Installing Dependencies"
apt-get install python3-pip python3-dev nginx
pip3 install --upgrade pip
pip3 install virtualenv
virtualenv venv

source venv/bin/activate
venv/bin/pip3 install -r requirements.txt

echo "Installing Services"

sed -e "s:<pwd>:$(pwd):g" -e "s:<user>:$USER:g" ./daemon/ti3-get.service | tee /etc/systemd/system/ti-3-get.service
sed -e "s:<pwd>:$(pwd):g" -e "s:<user>:$USER:g" ./daemon/ti3-update.service | tee /etc/systemd/system/ti-3-update.service

systemctl start ti-3-get.service
systemctl enable ti-3-get.service

systemctl start ti-3-update.service
systemctl enable ti-3-update.service

sed -e "s:<pwd>:$(pwd):g" -e "s/<host>/$tiHostname/g" ./nginx.conf | tee "/etc/nginx/sites-available/$tiHostname"
ln -s "/etc/nginx/sites-available/$tiHostname" "/etc/nginx/sites-enabled"
systemctl restart nginx