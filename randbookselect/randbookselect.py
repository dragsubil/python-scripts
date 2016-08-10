# Copies a random book from your book folder into your current folder



import os
import random
import re
from shutil import copy2

book_dir = 'F:/books'
booklist = []
bookpath = []


def getbooks(directory):
    dir_list = os.listdir(directory)
    for i in dir_list:
        path1 = os.path.join(directory, i)
        if os.path.isfile(path1):
            # This ignores any other file formats except the ebook file formats
            if re.search(r'.*(.pdf|.epub|.mobi)', i):
                booklist.append(i)
                bookpath.append(path1)
        else:
            getbooks(path1)

getbooks(book_dir)

rand_number = random.randrange(len(booklist))
rand_book_path = bookpath[rand_number]
rand_book_name = booklist[rand_number]

# Copies the selected book from book folder to current directory
copy2(rand_book_path, rand_book_name)
