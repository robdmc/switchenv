#! /usr/bin/env python

import os
import sys
import time


env = os.environ
env.update(robsvar='lily')
prof = 'robs'
print(f'\n\nDropping into new bash shell with profile {prof}\n\n', file=sys.stderr)
time.sleep(1.5)


os.execvpe('bash', ['bash'], env)


"""
THOUGHTS ON THE API
switchenv -n rob -f rob.sh

switchenv -e [rob]

switchenv -d [rob]
"""

