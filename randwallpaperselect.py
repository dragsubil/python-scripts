import os
import random
from shutil import copy2

file_dir = str(input("Enter the wallpaper directory path: "))

dirlist = os.listdir(file_dir)
rand_file = random.randrange(len(dirlist))
file_name = dirlist[rand_file]
file_extension = dirlist[rand_file].split('.')[1]
new_file = 'background.{}'.format(file_extension)
file_path = os.path.join(file_dir, file_name)

copy2(file_path, new_file)