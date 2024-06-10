import os
import glob
import shutil
import sys

# path to this file
path = os.path.dirname(__file__)
# create a folder called "checkpoints" in the folder where this script is located
checkpoint_folder_path = os.path.join(path, "checkpoints")
os.makedirs(os.path.join(path, "checkpoints"), exist_ok=True)
stats_folder_path = os.path.join(path, "stats")
os.makedirs(os.path.join(path, "stats"), exist_ok=True)
# move all files starting with "neat-checkpoint-" to a folder
files = glob.glob('neat-checkpoint-*')
for f in files:
    destination = os.path.join(checkpoint_folder_path, f)
    shutil.move(f, destination)

# move all .svg files to stats folder
files = glob.glob('*.svg')
for f in files:
    destination = os.path.join(stats_folder_path, f)
    shutil.move(f, destination)

files = glob.glob('*.png')
for f in files:
    destination = os.path.join(stats_folder_path, f)
    shutil.move(f, destination)

# delete "Digraph.gv" file
files = glob.glob('Digraph.gv')
for f in files:
    os.remove(f)