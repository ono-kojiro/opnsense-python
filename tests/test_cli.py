import os
import sys

import pytest
from pprint import pprint
import subprocess
import shlex

import re

def check_message(proc, msg):
    ret = 1
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        
        line = str(line.rstrip())

        print(line, file=sys.stderr)

        exp = msg
        m = re.search(exp, str(line))
        if m :
            ret = 0
    return ret

def test_cli():
    cmd = 'opncli'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             text=True,
           )

    msg = 'Available Modules:'
    ret = check_message(proc, msg)
    assert ret == 1

def test_cli_core():
    cmd = 'opncli core --help'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    msg = 'Available Controller for core'
    ret = check_message(proc, msg)
    assert ret == 1

def test_cli_core_system_status():
    print('\ntest_cli_core_system_status\n', file=sys.stderr)
    key = os.getenv("key")
    secret = os.getenv("secret")
    base_url = os.getenv("base_url")
    ip = re.sub(r'.*//', '', base_url)

    cmd = 'opncli {0} core system status'.format(ip)
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    msg = '"dialogTitle": "System Status"'
    ret = check_message(proc, msg)
    assert ret == 0


