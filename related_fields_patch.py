# Django command helper to apply django related fields patch programattically
# Will cd into 1st argument and run patch
import os
import sys
from subprocess import Popen, PIPE

patch_file = os.path.join(
    os.path.abspath('.'), 'bin', 'django-related-fields.patch')

process = Popen(['patch', '-p1'], stdin=PIPE, shell=False, cwd=sys.argv[1])
process.communicate(open(patch_file).read())
