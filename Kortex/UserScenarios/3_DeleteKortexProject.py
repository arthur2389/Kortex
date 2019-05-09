import shutil
import os

rootDir = input("Set your kortex project root directory: ")

userInput = input("Are sure sure you want to erase all files in :" + rootDir + " ? [Yes for remove]\n")

if userInput == "Yes":
    for _dir in os.listdir(rootDir):
        shutil.rmtree(os.path.join(rootDir, _dir))
