import os
import glob

# delete all files in the directory starting with "neat-checkpoint-"
files = glob.glob('neat-checkpoint-*')
for f in files:
    os.remove(f)