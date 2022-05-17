import os
import signal
import subprocess

# cmd = "ffplay video.mov"
cmd = "ffplay -fflags nobuffer rtmp://192.168.55.1/rtmp/live"

pro = subprocess.Popen(cmd,  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                       shell=True, preexec_fn=os.setsid)

while True:
    mode = input("0: Original, 1: Face Detect, 2: Hand Detect, 3: Object Detect, e:Exit.")
    if mode.lower() == "e":
        break
    elif mode in ["0", "1", "2", "3"]:
        pass

os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

'''
sudo apt-get autoremove --purge
sudo apt-get install  
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base \
gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x \
gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 \
gstreamer1.0-pulseaudio
'''

'''
gst-launch-1.0 \
nvarguscamerasrc num-buffers=300 ! \
"video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1" ! \
queue ! \
nvv4l2h264enc bitrate=8000000 ! \
h264parse ! \
qtmux ! \
filesink location=video.mov
'''