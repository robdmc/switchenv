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
# Add a profile name rob from the file named rob.sh
switchenv -n rob -f rob.sh

# Switch to the rob profile (fuzzypick profile when you want)
switchenv -e [rob]

# View the contents of a profile (fuzzypypick when needed)
switchenv -v [rob]
"""


