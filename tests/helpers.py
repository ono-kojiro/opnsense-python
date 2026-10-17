import sys
import json
import re

import shlex
import subprocess

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

def proc2json(proc):
    lines = ''

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        
        line = str(line.rstrip())
        lines = lines + '\n' + line

    return json.loads(lines)

def run_shell(cmd):
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, text=True)

    lines = ''
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        
        line = str(line.rstrip())
        lines = lines + '\n' + line

    return lines

