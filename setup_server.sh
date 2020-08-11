#!/bin/bash

# Running this script will setup the server with all the dependencies.

# download redis
cd
wget http://download.redis.io/releases/redis-5.0.7.tar.gz
tar -xvf redis-5.0.7.tar.gz

# install compilation dependencies
sudo apt install make gcc g++

# compile redis
cd redis-5.0.7/deps/
make hiredis jemalloc linenoise lua geohash-int
cd ..
make

# delete redis file and make logs folder
cd ..
rm redis-5.0.7.tar.gz
mkdir logs
cd logs
mkdir pothole


# install python dependencies
sudo apt install python3-pip
cd ~/validator_backend/
pip3 install -r requirements.txt

# create systemd services
sudo cp systemctl_services/* /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/redis.service
sudo chmod 644 /etc/systemd/system/rq.service
sudo chmod 644 /etc/systemd/system/pothole.service
sudo systemctl daemon-reload

# install nginx
sudo apt install nginx

# redirect port 80 to port 3000 via nginx
sudo cp nginx/plothole /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/plothole /etc/nginx/sites-enabled/plothole
sudo service nginx restart


echo "Start the services redis rq and pothole manually"