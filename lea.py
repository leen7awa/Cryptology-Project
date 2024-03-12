# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 09:49:33 2024

@author: ?
"""
import numpy as np
import math
import random

#import Crypto.Random

def get_bin(number: int, n: int)-> str:
    '''Returns binary representation of number filled with 0's to length n'''
    return bin(number)[2:].zfill(n)

def get_random_bits(n: int) -> str:
    '''Returns sequence of random bits of length n'''
    i = random.randint(0,pow(2,n)-1)
    bin_key = get_bin(i,n)
    return bin_key

def ADD(x: str,y: str) -> str:
    '''ADD mod 2^32'''
    return get_bin(((int(x,2) + int(y,2)) % 4294967296), 32) #pow(2,32)

ADD('11111111111111111111111111111111','10')

def SUB(x: str,y: str) -> str:
    '''SUB mod 2^32'''
    return get_bin(((int(x,2) - int(y,2)) % 4294967296),32)

SUB('1','10')


def XOR(bits1: str, bits2: str) -> str:
    """XOR operation"""
    xor_result = ""
    for index in range(len(bits1)):
        if bits1[index] == bits2[index]: 
            xor_result += '0'
        else:
            xor_result += '1'
    return xor_result 

XOR('010','110')


def ROL(x: str,i: str) -> str:
    '''i-bit's left rotation'''
    shiftedbits = x[i:] + x[:i]
    return shiftedbits

def ROR(x: str,i: str) -> str:
    '''i-bit's right rotation'''
    shiftedbits = x[-i:] + x[:-i] 
    return shiftedbits


#The table is longer than we need, because we use all values for longer keys
d = [0xc3efe9db, 0x44626b02, 0x79e27c8a, 0x78df30ec, 0x715ea49e, 0xc785da0a, 0xe04ef22a, 0xe5c40957]

get_bin(d[0],32)

from textwrap import wrap

def get_round_keys(key: str) -> list:
    '''
    Takes:
    - 128-bit key (string)
    Returns:
    - 24 192-bit round keys (array)
    '''
    # round key table
    RK = []
    
    # 1.
    T0, T1, T2, T3 = wrap(key, 32)

    # 2.
    for i in range(0,24):
        delta = get_bin(d[i%4], 32)
        
        T0 = ROL(ADD(T0, ROL(delta,i)), 1)
        T1 = ROL(ADD(T1, ROL(delta,i+1)), 3)
        T2 = ROL(ADD(T2, ROL(delta,i+2)), 6)
        T3 = ROL(ADD(T3, ROL(delta,i+3)), 11)
        
        RK.append([T0, T1, T2, T1, T3, T1])
    return RK
    
test_key = get_random_bits(128)
test_RK = get_round_keys(test_key)
# print(len(test_RK))

def lea_encrypt(block: str, key: str) -> str:
    '''
    Takes:
    - 128-bit blok (string w postaci binarnej)
    - 128-bit klucz (string w postaci binarnej)
    Returns:
    - 128-bit zaszyfrowany blok (string w postaci binarnej)
    '''
    # wygenerowanie kluczy rundowych
    RK = get_round_keys(key)
    
    # 1.
    X00, X01, X02, X03 = wrap(block, 32)
    
    
    # 2.
    for i in range(0,24):
        X10 = ROL(ADD(XOR(X00, RK[i][0]), XOR(X01, RK[i][1])), 9)
        X11 = ROR(ADD(XOR(X01, RK[i][2]), XOR(X02, RK[i][3])), 5)
        X12 = ROR(ADD(XOR(X02, RK[i][4]), XOR(X03, RK[i][5])), 3)
        X13 = X00
        
        X00, X01, X02, X03 = X10, X11, X12, X13
        
    # 3.
    return X10+X11+X12+X13

def lea_decrypt(ciphered_block: str, key: str) -> str:
    '''
    Takes:
    - 128-bit ciphertext 
    - 128-bit key 
    Returns:
    - 128-bit deciphered text 
    '''
    # generating round keys
    RK = get_round_keys(key)
    
    # 1.
    X10, X11, X12, X13 = wrap(ciphered_block, 32)
    
    # 2.
    for i in range(23,-1,-1):
        X00 = X13
        X01 = XOR(SUB(ROR(X10, 9), XOR(X00, RK[i][0])), RK[i][1])
        X02 = XOR(SUB(ROL(X11, 5), XOR(X01, RK[i][2])), RK[i][3])
        X03 = XOR(SUB(ROL(X12, 3), XOR(X02, RK[i][4])), RK[i][5])
        
        X10, X11, X12, X13 = X00, X01, X02, X03 
        
    # 3.
    return X00+X01+X02+X03
plaintext = get_random_bits(128)
'''
key = get_random_bits(128)

print('Plaintext: '+ hex(int(plaintext,2)))
ciphertext = lea_encrypt(plaintext, key)
print('Ciphered: '+hex(int(ciphertext,2)))
decrypted = lea_decrypt(ciphertext, key)
print('Decrypted: '+hex(int(decrypted,2)))
print('if plain==decrypted:'+ str(plaintext==decrypted))

'''
'''
LEA-128
# Key: 0f 1e 2d 3c 4b 5a 69 78 87 96 a5 b4 c3 d2 e1 f0
# Plaintext: 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f
# Ciphertext: 9f c8 4e 35 28 c6 c6 18 55 32 c7 a7 04 64 8b fd
'''
'''
key = get_bin(0x0f1e2d3c4b5a69788796a5b4c3d2e1f0, 128) 
plaintext = get_bin(0x101112131415161718191a1b1c1d1e1f, 128)

print('Plaintext: '+ hex(int(plaintext,2)))
ciphertext = lea_encrypt(plaintext, key)
print('Ciphertext: '+hex(int(ciphertext,2)))
print('if ciphertext==0x9fc84e3528c6c6185532c7a704648bfd:'+ str(int(ciphertext,2)==0x9fc84e3528c6c6185532c7a704648bfd))
decrypted = lea_decrypt(ciphertext, key)
print('Decrypted: '+hex(int(decrypted,2)))
'''