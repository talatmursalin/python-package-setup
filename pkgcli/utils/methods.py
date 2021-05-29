import os
import random
import string
import shutil
from distutils.dir_util import copy_tree


def make_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError as e:
        print('File already exist {}'.format(path))


def input_binary_choice(message, default=False):
    choice = input(message)
    choice = choice.lower()
    if len(choice) == 0:
        choice = default
    elif choice == 'yes' or 'Y':
        choice = True
    else:
        choice = False
    return choice


def touch(path):
    open(path, 'a').close()


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)


def copy_file(src, des):
    shutil.copy(src, des)


def copy_everything(src, des):
    copy_tree(src, des)


def random_dir_name():
    return 'tmp_' + ''.join(random.choice(string.ascii_letters+string.digits) for i in range(4))


def clear_everything(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
