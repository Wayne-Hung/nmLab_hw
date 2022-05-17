# nmLab_hw
Server (Jetson Nano) send streaming video to client (laptop), and user can send control signal to the server through gRPC.

## Install Dependencies
### Install gRPC Dependencies
Both server and client side:
```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install grpc packages
$ pip3 install -r requirements.txt
```

### Install Gstreamer
Server side:
```bash 
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base \
gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x \
gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 \
gstreamer1.0-pulseaudio
$ 
```
### Install openCV
Install on server side. Skip.

## How to Run
Start server:
``` bash
$ python3 server.py --ip [your ip] --port [your port]
```
For example:
``` bash
$ python3 server.py --ip 0.0.0.0 --port 8888
```


Start client:
``` bash
$ python3 client.py --ip [server ip] --port [server port]
```
For example:
``` bash
$ python3 client.py --ip 192.168.55.1 --port 8888
```

## Display mode
- 0: Do not apply any visual algorithm.
- 1: Face detection.
- 2: Hand detection.
- 3: Object detection.

## Demo video
[Youtube link](TODO)
