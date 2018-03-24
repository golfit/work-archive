from MDSplus import *
import subprocess

#Run profile script so that environment variables are set.
subprocess.call(['/home/golfit/bin/sh/runProfileScript.sh'])

s=int(Data.compile('current_shot("cmod")').evaluate())

print(s)
