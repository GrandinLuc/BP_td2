from ecpy.curves import Curve
from ecpy.keys import ECPrivateKey
from ecpy.ecdsa import ECDSA
import hashlib
import binascii
import hmac

bip_0039 = open("english.txt",'r')
words = bip_0039.read()
words = words.split('\n')

example_seed = ['open', 'curious', 'climb', 'dog', 'strong', 'ridge', 'brush', 'capable', 'music', 'noodle', 'degree', 'jungle']
print("\nExemple de seed : ", example_seed)

def import_seed(list_words):
    res = []
    for word in list_words:
        res.append(bin(words.index(word))[2:])
    return res

print()     
print("Seed recuperee depuis l'example : ", import_seed(example_seed))


### Master private key et Chaincode ###


#il faut utiliser haslib sha512 pour hasher notre seed
#il faut calculer la public key de notre private key, soit avec une librairie externe soit en utilisant le schema de dérivation des clés enfants renforcée

root_seed_list = import_seed(example_seed)

# PB : tout les éléments de la seed ne font pas tous 11 bits de long
# solution : on ajoute des 0 en debut de chaine pour que tout éléments de la seed fassent 11 bit de long
root_seed = ''
for elem in root_seed_list:
    if len(elem) != 11:
        while len(elem) < 11:
            elem = ('0'+elem) # Tout les éléments font 11 bit de long
    root_seed += elem
    
# la root seed fait 132 bit de long, il faut y soustraire la checksum ( 4 dernier bit de la str )
root_seed = root_seed[:-4]

print("\n--------------------\n")  
print("Root seed en binaire : ", root_seed)
print()  
print("La longueur de la root seed est de : ", len(root_seed)) 

# transformation de la seed binaire en hexadecimal 
hexstr = "{0:0>4X}".format(int(root_seed,2)) 
data = binascii.a2b_hex(hexstr) 
print(type(data))

# Utilisation de haslib sur l'hexadecimal
extended_private_key_bytes = hashlib.sha512(data).hexdigest()
extended_private_key_bytes = extended_private_key_bytes.encode('utf-8')

print("\n--------------------\n") 
print("Hash de la root seed : ", extended_private_key_bytes)
print(type(extended_private_key_bytes))

extended_private_key = bin(int(extended_private_key_bytes, 16))[2:].zfill(512)
print("\n--------------------\n") 
print("Hash de la root seed sous forme string binaire : ", extended_private_key)
print(len(extended_private_key))

master_private_key = extended_private_key[:256]
master_chain_code = extended_private_key[256:]

print("\n--------------------\n") 
print("MASTER PRIVATE KEY : ", master_private_key)
print(len(master_private_key))
print("\nMASTER CHAIN CODE : ", master_chain_code)
print(len(master_chain_code))


### Master public key ###

# cv   = Curve.get_curve('secp256k1')
# master_public_key = ECPrivateKey(int(master_private_key, 2), cv)
# print(master_public_key)
# print(type(master_public_key))


### Child keys ###

print("\n--------------------\n") 

key = int("0", 2).to_bytes(2, 'big') # index 0
# msg = int("110110010110", base=2).to_bytes(2, 'big') # extended_private_key

child_keys = hmac.new(key=key, msg=extended_private_key_bytes, digestmod=hashlib.sha512).hexdigest()
child_keys = child_keys.encode('utf-8')
child_keys = bin(int(child_keys, 16))[2:].zfill(512)

print("Child Keys : ", child_keys)
print(len(child_keys))

child_private_key = child_keys[:256]
child_chain_code = child_keys[256:]

print("\nCHILD PRIVATE KEY : ", child_private_key)
print(len(child_private_key))
print("\nCHILD CHAIN CODE : ", child_chain_code)
print(len(child_chain_code))