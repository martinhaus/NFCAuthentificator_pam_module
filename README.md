# NFCAuthentificator_pam_module

PAM module using [Python NFC authenticator](https://github.com/martinhaus/NFCAuthentificator_python_client) [1] and [Android NFC authenticator](https://github.com/martinhaus/NFCAuthentificator_android_client) [2] for NFC communication and authentication with Android device


## Compiling PAM module 

```
gcc -fPIC -fno-stack-protector -c pam.c
```

## Installing PAM module (Arch Linux)

```
sudo ld -x --shared -o /lib/security/pam_nfc.so pam.o
```

## PAM Configuration 

```
#This file must be put in /etc/pam.h/

auth        required       pam_nfc.so
account     required       pam_nfc.so
password    required       pam_nfc.so

```

# Usage

To use this module you need NFC enabled Android device with Android client [2] (or its modification) installed. You'll also need Python module [2] to be running at the host with connected NFC reader.


File `simple.c` contains simple usage of this module for the purpose of user authentication. The C application runs Python wrapper by running `wrapper.py`.

### `Wrapper.py`

```
Usage:
 -p   Generates new RSA keys and recieves devices public key for signature verification
 -a   Authentication - the device must be already attached tothe reader when running this command.
 -w   Wait for device - same as -a, but the reader waits 10 seconds for device.

```



# Reference

This repository is part of my diploma thesis - Authentication using smartphone.

[1] Python backend module - https://github.com/martinhaus/NFCAuthentificator_python_client
 
[2] Android communication module - https://github.com/martinhaus/NFCAuthentificator_android_client