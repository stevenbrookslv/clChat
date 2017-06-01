#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random



inp = input("Enter string to encrypt: ")

print("\n\n\n")

random_generator = Random.new().read
key = RSA.generate(2048, random_generator) #generate pub and priv key

f = open("privKey.pem", 'w')
privKey = key.exportKey('PEM').decode("utf-8") + '\n'
f.write(privKey)
g = open("pubKey.pem", 'w')
pubKey = key.publickey().exportKey('PEM').decode("utf-8") + '\n'
g.write(pubKey)



f.close()
g.close()

f = open("pubKey.pem", 'r')
key = RSA.importKey(f.read())
dStr = str.encode(inp)
enc = PKCS1_OAEP.new(key.publickey())
encString = enc.encrypt(dStr)
pString = str(encString)[2:-1]
print("Encrypted String: \n" + pString + "\n\n")
f.close()

g = open("privKey.pem", 'r')
key = RSA.importKey(g.read())
enc = PKCS1_OAEP.new(key)
dString = enc.decrypt(encString)
decString = str(dString)[2:-1]
print("Decrypted String: \n" + decString + "\n\n")

