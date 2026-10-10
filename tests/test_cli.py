import pytest
from pprint import pprint
import subprocess
import shlex

import re

def test_cli():
    cmd = 'opncli'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    ret = 1
    while True:
        line = proc.stdout.readline().rstrip()
        if not line:
            break
        print(line)

        exp = 'Available Modules:'
        m = re.search(exp, str(line))
        if m :
            ret = 0
            break

    assert ret == 0
