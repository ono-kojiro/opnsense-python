import pytest
from pprint import pprint
import subprocess
import shlex

import re

def check_message(proc, msg):
    ret = 1
    while True:
        line = proc.stdout.readline().rstrip()
        if not line:
            break
        print(line)

        exp = msg
        m = re.search(exp, str(line))
        if m :
            ret = 0
            break
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

