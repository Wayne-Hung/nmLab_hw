#!/bin/bash

RTMP_SRC="rtmp://localhost/rtmp/live"

# OpenCV pipeline on Jetson Nano
gst-launch-1.0 -e \
    rtmpsrc location=${RTMP_SRC} ! \
    flvdemux name=demux demux.video ! \
    queue ! \
    decodebin ! \
    nvvidconv ! \
        "video/x-raw, format=(string)BGRx" ! \
    videoconvert ! \
        "video/x-raw, format=(string)BGR" ! \
    appsink

# Record RTMP video on Jetson Nano with NVENC & NVDEC
gst-launch-1.0 -e \
    rtmpsrc location=${RTMP_SRC} ! \
    flvdemux name=demux demux.video ! \
    queue ! \
    decodebin ! \
    nvvidconv ! \
    "video/x-raw(memory:NVMM), format=(string)NV12" ! \
    queue ! \
    nvv4l2h264enc bitrate=8000000 ! \
    h264parse ! \
    qtmux ! \
    filesink location=rtmp.mov

# Record RTMP video on Normal PC
gst-launch-1.0 -e \
    rtmpsrc location=${RTMP_SRC} ! \
    flvdemux name=demux demux.video ! \
    queue ! \
    decodebin ! \
    videoconvert ! \
        "video/x-raw, format=I420" ! \
    x264enc speed-preset=superfast tune=zerolatency psy-tune=grain sync-lookahead=5 bitrate=480 key-int-max=50 ref=2 ! \
    qtmux ! \
    filesink location=rtmp.mov
