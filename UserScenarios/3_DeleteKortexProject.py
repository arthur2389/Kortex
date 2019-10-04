import shutil
import os

root_dir = input("Set your kortex project root directory: ")

user_input = input("Are sure sure you want to erase all files in :" + root_dir + " ? [Yes for remove]\n")

if user_input == "Yes":
    for _dir in os.listdir(rootDir):
        shutil.rmtree(os.path.join(rootDir, _dir))
