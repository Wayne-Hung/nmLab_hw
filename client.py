import os
import os.path as osp
import sys

import signal
import subprocess

BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
import fib_pb2
import fib_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default="localhost")
parser.add_argument("--port", type=int, default=8080)
args = vars(parser.parse_args())
host = f"{args['ip']}:{args['port']}"
print(host)

cmd = f"ffplay -fflags nobuffer rtmp://{args['ip']}/rtmp/live"

pro = subprocess.Popen(cmd,  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
                    shell=True, preexec_fn=os.setsid)

try:
    with grpc.insecure_channel(host) as channel:
        stub = fib_pb2_grpc.FibCalculatorStub(channel)
        request = fib_pb2.FibRequest()

        while True:
            mode = input("0: Original, 1: Face Detect, 2: Hand Detect, 3: Object Detect, 4: Pose Detect, e:Exit.")
            if mode.lower() == "e":
                break
            elif mode in ["0", "1", "2", "3", "4"]:
                request.order = int(mode)
                response = stub.Compute(request)
                print(response.value)
except KeyboardInterrupt as e:
    pass

os.killpg(os.getpgid(pro.pid), signal.SIGTERM)