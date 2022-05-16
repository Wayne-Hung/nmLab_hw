#!/bin/bash

# Install openssl
sudo apt-get install -y openssl libssl-dev

# Download Nginx
wget http://nginx.org/download/nginx-1.13.8.tar.gz
tar -xzvf nginx-1.13.8.tar.gz && rm nginx-1.13.8.tar.gz
mv nginx-1.13.8 nginx

# Download Nginx RTMP Module
git clone https://github.com/arut/nginx-rtmp-module.git

# Configure Nginx Compilation
NGINX_RTMP_DIR="$PWD/nginx-rtmp-module"
cd nginx
./configure --prefix=/var/www --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --pid-path=/var/run/nginx.pid --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --with-http_ssl_module --without-http_proxy_module --add-module=${NGINX_RTMP_DIR}

# Compile the NGINX
make -j`nproc`
sudo make install

# Modify the config file
cd ..
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo cp nginx.service /lib/systemd/system/nginx.service
sudo systemctl enable nginx
sudo systemctl start nginx
