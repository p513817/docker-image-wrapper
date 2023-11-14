import json
import argparse
import subprocess
import subprocess as sp
import os
import fcntl
import time
import sys
from typing import Tuple
import os
import logging

# Argument

def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, required=True,
                        help="path to config file")
    args = parser.parse_args()
    return args

# Error

class DisableServiceError(Exception):
    def __init__(self, message: str="The service is disabled."):
        self.message = message
        super().__init__(self.message)

# Utils

def clear_console():
    os.system('clear')

def timeit(func):
    def wrap(*args, **kwargs):
        ts = time.time()
        res = func(*args, **kwargs)
        te = time.time()
        return res, (round(te-ts, 2))
    return wrap 

def read_json(json_path: str) -> dict:
    with open(json_path, "r") as f:
        data = json.load(f)
    return data

def run_cmd(cmd: list):
    try:
        proc = sp.run(
            cmd,
            check=True,
            stdout=sp.PIPE, 
            stderr=sp.PIPE,
            text=True)
    except sp.CalledProcessError as e:
        raise RuntimeError(f"Command Error: \"{' '.join(cmd)}\"")

def get_buildx_cmd(src: str, trg:str, arch: str="linux/amd64") -> list:
    return [
        "docker", "buildx", "build", 
        "-f", "wrapper.dockerfile", 
        "--platform", arch, 
        "--build-arg",
        f"SRC={src}",
        "--push",
        "-t", trg, "." ]

def get_image_name(imagename: str, version: str, username: str = "") -> str:
    basic = f"{imagename}:{version}"
    return f"{username}/{basic}" if username else basic

@timeit
def wrap_service(source: str, target: str, arch: str):
    return run_cmd(get_buildx_cmd(source, target, arch))

# Test

@timeit
def wait_seconds(sec:int, skip:bool=False, interrupt:bool= False):
    if skip: raise DisableServiceError()
    if interrupt: raise InterruptedError('For test')
    return sp.run(f"sleep {sec}", shell=True)
    