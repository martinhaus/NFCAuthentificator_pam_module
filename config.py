# Encryption method that is used to secure communication between Android device and this module
# asymmetric - RSA to transfer AES key to device
# diffie - Diffie-Hellman key exchange to create AES key on both devices
# key_transfer_method = 'asymmetric'
key_transfer_method = 'diffie-hellman'

key_size = 2048

# AID used to determine which application handles the communication at Android device.
# AID is part of introductory message sent to device after device is connected
# Default value [0xF2, 0x22, 0x22, 0x22, 0x22]
AID = [0xF2, 0x22, 0x22, 0x22, 0x22]
