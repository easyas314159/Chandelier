#!/bin/bash
pushd /root/

base="/usr/share/chandelier/"
config=$base"config"

echo "$base"
echo "$config"

if [ -e Chandelier ]; then
    pushd Chandelier
    git pull
    popd
else
    git clone git@github.com:easyas314159/Chandelier.git
fi

if [ ! -e "$base" ]; then
    echo "Linking $base"
    ln -s /root/Chandelier/ "$base"
fi

if [ ! -e /var/log/chandelier ]; then
    mkdir /var/log/chandelier
fi

if [ ! -e /etc/chandelier ]; then
    cp /root/Chandelier/default.config /etc/chandelier
    ln -s /etc/chandelier "$config"
fi

echo "Copying daemon script"
cp -f /root/Chandelier/chandelier.sh /etc/init.d/chandelier
chmod a+x /etc/init.d/chandelier

apt-get install python-daemon
apt-get -y purge libx11-6 libgtk-3-common xkb-data lxde-icon-theme raspberrypi-artwork penguinspuzzle

update-rc.d -f chandelier enable

popd