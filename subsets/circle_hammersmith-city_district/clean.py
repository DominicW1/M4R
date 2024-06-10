import os
import glob

# delete all files in the directory starting with "neat-checkpoint-"
files = glob.glob('neat-checkpoint-*')
for f in files:
    os.remove(f)

# delete all .svg files
files = glob.glob('*.svg')
for f in files:
    os.remove(f)

# delete all .png files
files = glob.glob('*.png')
for f in files:
    os.remove(f)

# delete "Digraph.gv" file
files = glob.glob('Digraph.gv')
for f in files:
    os.remove(f)