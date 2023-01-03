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

To compile an `exe` for both pincher and firefoxDecrypt, run the `builder.py` script.
```bash
python3 builder.py
```

`pincher.exe` and `firefoxDecrypt.exe` files will be located in the `final` folder. You can copy these two files in the same folder in a USB.


#### Note that there will be no errors reported, since its meant to get the job done asap.

### I AM NOT RESPONSIBLE FOR ANY WRONG USE OF THIS SCRIPT, ANY TROUBLE YOU CAUSE WILL CONFINE TO YOU.

## License

[Pincher](https://github.com/0xcabrex/Pincher) is licensed under the MIT license as stated in the [LICENSE](https://github.com/0xcabrex/Pincher/blob/master/LICENSE) file
