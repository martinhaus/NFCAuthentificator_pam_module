import sys, getopt
from android_nfc_com.APDUCommunicator import APDUCommunicator
from android_nfc_com.APDUMessageConverter import MessageConverter
from smartcard.CardMonitoring import CardObserver, CardMonitor
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from Crypto.Hash import SHA256
import hashlib
from time import sleep
import os
import config

class PhoneObserver(CardObserver):
    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            try:
                algo, key_size = load_config()
                authenticate(algo, key_size)
            except Exception:
                print("Connection could not be established, please try again...")

def load_config():
    if hasattr(config, 'key_size'):
        key_size = config.key_size
    
    if hasattr(config, 'key_transfer_method'):
        algo = config.key_transfer_method

    return algo, key_size

def pair_device(algo = 'assymetric', key_size = 1024):
    com = APDUCommunicator(algo, key_size, False)
    pubkey = com.send_message([0x00, 0x15, 0x00, 0x00], '')
    keyDER = b64decode(pubkey)
    keyPub = RSA.importKey(keyDER)

    with open ("public.pem", "w") as pub_file:
        print("{}".format(keyPub.exportKey(format='PEM').decode('UTF-8')), file=pub_file)

def authenticate(algo = 'assymetric', key_size = 1024):
    with open('public.pem', mode='r') as public_file:
        key_data = public_file.read()
        public_key = RSA.import_key(key_data)
    
    com = APDUCommunicator(algo, key_size, False)
    payload = com.send_message([0x00, 0x16, 0x00, 0x00], "")
    password = com.request_otp()

    h = SHA256.new(password.encode('UTF-8'))

    signer = PKCS1_v1_5.new(public_key)

    if signer.verify(h, b64decode(payload)):
        # Authentication successful
        print('Verified!')
        os._exit(0)
    else:
        # Authentication failure
        os._exit(1)

def wait_for_device():
    cardmonitor = CardMonitor()
    cardobserver = PhoneObserver()
    cardmonitor.addObserver(cardobserver)
    print('Waiting for device...')
    sleep(10)

    cardmonitor.deleteObserver(cardobserver)
    os._exit(1)


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hpwa")
    except getopt.GetoptError:
        print ('Usage: python wrapper.py -a -p -w')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Usage:\n \
-p   Generates new RSA keys and recieves devices \
public key for signature verification\n\
 -a   Authentication - the device must be already attached to\
the reader when running this command.\n\
 -w    Wait for device - same as -a, but the reader waits 10 seconds for device.')
            sys.exit()
        elif opt in ("-p", "--pair"):
            print('pairing')
            pair_device()
        elif opt in ("-a", "--authenticate"):
            print('autenthicating')
            authenticate()
        elif opt in ("-w", "--wait"):
            wait_for_device()

if __name__ == "__main__":
    main(sys.argv[1:])