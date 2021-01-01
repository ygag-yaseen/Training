import os
import shutil
from zipfile import ZipFile
from os import path
from shutil import make_archive

from os import listdir
from os.path import isfile, join
from zipfile import ZipFile

dir_name=input()
output_filename=dir_name+'/a'
onlyfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
shutil.make_archive(output_filename, 'zip', dir_name)


# /home/bassam10/path_test

