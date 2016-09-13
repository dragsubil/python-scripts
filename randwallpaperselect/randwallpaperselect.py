#!/usr/bin/env python3
# Selects and copies a random wallpaper from your wallpaper directory
# If you have Unity or Gnome Shell, this will change the wallpaper directly 

# to your current directory.
# You must first set an environment variable pointing to your wallpaper directory
# and name it 'WALLPAPER'


import os
import sys
import subprocess   
import random
from shutil import copy2

file_dir = os.environ.get('WALLPAPER')

dirlist = os.listdir(file_dir)
rand_file = random.randrange(len(dirlist))
file_name = dirlist[rand_file]
file_path = os.path.join(file_dir, file_name)

if sys.platform == 'linux':
    # As far as I know, this command only applies to Unity and the Gnome Shell
	subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://{}".format(file_path)])


else:
    # In case you don't have Unity or Gnome shell
    file_extension = dirlist[rand_file].split('.')[-1]
    new_file = 'background.{}'.format(file_extension)
    copy2(file_path, new_file)
