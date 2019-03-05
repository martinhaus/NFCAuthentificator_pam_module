import sys, getopt
from android_nfc_com.APDUCommunicator import APDUCommunicator
from android_nfc_com.APDUMessageConverter import MessageConverter
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode
from Crypto.Hash import SHA256
import hashlib


def pair_device():
    com = APDUCommunicator('asymmetric', False)
    pubkey = com.send_message([0x00, 0x15, 0x00, 0x00], '')
    keyDER = b64decode(pubkey)
    keyPub = RSA.importKey(keyDER)

    with open ("public.pem", "w") as pub_file:
        print("{}".format(keyPub.exportKey(format='PEM').decode('UTF-8')), file=pub_file)

def authenticate():
    with open('public.pem', mode='r') as public_file:
        key_data = public_file.read()
        public_key = RSA.import_key(key_data)

    com = APDUCommunicator('asymmetric', False)
    payload = com.send_message([0x00, 0x16, 0x00, 0x00], '')
    password = com.request_otp()

    h = SHA256.new(password.encode('UTF-8'))

    signer = PKCS1_v1_5.new(public_key)

    if signer.verify(h, b64decode(payload)):
        # Authentication successful
        sys.exit(0)
    else:
        # Authentication failure
        sys.exit(1)

def challange_recieved_payload(payload):
    return True

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hpwa")
    except getopt.GetoptError:
        print ('Usage: TODO - to be added')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Usage: TODO - to be added')
            sys.exit()
        elif opt in ("-p", "--pair"):
            print('pairing')
            pair_device()
        elif opt in ("-a", "--authenticate"):
            print('autenthicating')
            authenticate()
        elif opt in ("-w", "--wait"):
            print('-w')

if __name__ == "__main__":
    main(sys.argv[1:])