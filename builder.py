# This script is to build the exe file for pincher.py

import subprocess
import os
import shutil




def pincher_builder(build_directory, wd):
    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    try:
        data = subprocess.check_output(['pyinstaller','--help'], shell=True, stderr=open(os.devnull, 'wb')).decode('utf-8', errors='backslashreplace')

    except subprocess.CalledProcessError as e:
        print(e)
        print("Pyinstaller not installed, installing")
        output = subprocess.check_output(['pip', 'install', 'pyinstaller'], shell=True).decode('utf-8', errors='backslashreplace')

        print("Installed successfully")

    print("Building script...")
    os.chdir(build_directory)

    # subprocess.check_output(['echo', 'hello world', '>', 'test.txt'],  shell=True)

    subprocess.check_output(['pyinstaller', '--onefile', f'{wd}/pincher.py'], shell=True)

    print("Build completed successfully")

    if not os.path.exists(f"{wd}/final/"):
        os.mkdir(f"{wd}/final")

    shutil.copyfile("./dist/pincher.exe", f"{wd}\\final\\pincher.exe")

    print(f"\npincher.exe file located in {wd}\\final")

    os.chdir(wd)

def firefoxDecrypt_builder(build_directory, wd):
    if not os.path.exists(build_directory):
        os.mkdir(build_directory)

    try:
        data = subprocess.check_output(['pyinstaller','--help'], shell=True, stderr=open(os.devnull, 'wb')).decode('utf-8', errors='backslashreplace')

    except subprocess.CalledProcessError as e:
        print(e)
        print("Pyinstaller not installed, installing")
        output = subprocess.check_output(['pip', 'install', 'pyinstaller'], shell=True).decode('utf-8', errors='backslashreplace')

        print("Installed successfully")

    print("Building script...")
    os.chdir(build_directory)

    # subprocess.check_output(['echo', 'hello world', '>', 'test.txt'],  shell=True)

    subprocess.check_output(['pyinstaller', '--onefile', f'{wd}/modules/firefoxDecrypt.py'], shell=True)

    print("Build completed successfully")

    if not os.path.exists(f"{wd}/final/"):
        os.mkdir(f"{wd}/final")

    shutil.copyfile("./dist/firefoxDecrypt.exe", f"{wd}\\final\\firefoxDecrypt.exe")

    print(f"\nfirefoxDecrypt.exe file located in {wd}\\final")

    os.chdir(wd)


if __name__ == "__main__":

    print("Script to build pincher and firefoxDecrypt.\n\n")

    wd = os.getcwd()                                            # Original working directory
    pincher_build_directory = "build/pincher/"
    firefoxDecrypt_build_directory = "build/firefoxDecrypt/"

    if not os.path.isdir("build"):
        os.mkdir("build")

    print("Building firefoxDecrypt.exe...")
    firefoxDecrypt_builder(firefoxDecrypt_build_directory, wd)

    print("\nBuilding pincher.exe...")
    pincher_builder(pincher_build_directory, wd)

    print("\nBuild Complete. Removing build directory")
    shutil.rmtree("build/")
    
