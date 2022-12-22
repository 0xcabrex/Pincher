# Pincher

Pincher is a Python script that can extract confidential information stored in the user's system.

This script is capable of:
* Decrypting saved Firefox passwords
* Decrypting saved Edge (Chromium based) passwords
* Decrypting saved Brave passwords
* Extracting saved wifi SSIDs and passwords
* Extracting the environment variables of the system

##### This script works only on Windows systems.

## Usage

Install the required modules
``` bash
pip install -r requirements.txt
```

Once the required modules are installed, run the script
``` bash
python3 pincher.py
```


## Points to note

This script can be compiled to an `.exe` file and ported onto a USB. To compile to an exe file, we need to install [pyinstaller](https://pypi.org/project/pyinstaller/) first. Then run the following:

```bash
pyinstaller --onefile pincher.py
```

The python script (and the compiled `.exe`) requires the [firefoxDecrypt.py](https://github.com/unode/firefox_decrypt) tool to be compiled into an executable, without which it would not be able to decrypt the firefox passwords.

To compile the file, simply run:
```bash
cd modules/
pyinstaller --onefile firefoxDecrypt.py
```

The compiled `firefoxDecrypt.exe` file (present in the `dist/` folder) needs to be in the same directory as `pincher.py`/`pincher.exe` for it to run.

Code and the compiled file for `firefoxDecrypt` are both present in this repository.

#### Note that there will be no errors reported, since its meant to get the job done asap.

### I AM NOT RESPONSIBLE FOR ANY WRONG USE OF THIS SCRIPT, ANY TROUBLE YOU CAUSE WILL CONFINE TO YOU.

## License

[Pincher](https://github.com/0xcabrex/Pincher) is licensed under the MIT license as stated in the [LICENSE](https://github.com/0xcabrex/Pincher/blob/master/LICENSE) file
