# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 09:06:58 2024

@author: Leen
"""
import lea
import ElgamalEllipticCurve as gm
import rsa
import numpy as np
import math
import random
from tinyec import registry
from tinyec import ec
import secrets 


def main():
    
   # Generate keys
   k = lea.get_random_bits(128) # symmetric key
   # do the following to remove zeroes if they are found in the beginning of the string k
   intK = int(k)
   k = str(intK)

   plaintext = lea.get_random_bits(128)
   # encrypt plaintext
   ciphertext = lea.lea_encrypt(plaintext, k)
   # now encrypt the symmetric key with Bob's public key
   symmetricKey = int(k,2)
   y1x,y2x = gm.encrypt(symmetricKey) # EC ElGamal
   
   ################## RSA ################
   rsa.primefiller()
   rsa.setkeys()
   
   coded = rsa.encoder(ciphertext)
   print('Digital signature added')
   
   ################## Send Email ################
   print('-------------------------------------')
   print('Email is now sent from Alice to Bob')
   print('Of course it is encrypted')
   print('All Bob has to do is decrypt')
   print('-------------------------------------')
    
   ################## Decryption ################
   uncoded = rsa.decoder(coded) #decrypting digital signature
   decrypted_symmetricKey = gm.decrypt(y1x, y2x)
   decrypted = lea.lea_decrypt(ciphertext, (bin(decrypted_symmetricKey))[2:])

   print('Original message: ', plaintext)
   print('-------------------------------------')
   print('Decrypted: ', decrypted)
   print('-------------------------------------')
   print('Same message? ', plaintext == decrypted)
   # print('decrypted message: ')


if __name__ == "__main__":
    main()
