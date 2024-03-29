from Crypto.Random import get_random_bytes
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.number import long_to_bytes
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from random import randint
import hashlib
import socket
import sys

g = 5 # Generator 
p = 10061 # Prime number

filename = input("Enter name of textfile: ")
f = open(filename, "r")
local_ip = f.readline().strip('\n')
local_port = int(f.readline())
remote_ip = f.readline().strip('\n')
remote_port = int(f.readline())
sk_alice = int(f.readline())
pk_bob = int(f.readline())
f.close()

pk_alice = pow(g, sk_alice, p)


# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind((local_ip, local_port))
print("Do Ctrl+c to exit the program !!")
print()

# Let's send data through UDP protocol
while True:
		M = input("Type some text to send to Bob => ");
		M_byte = M.encode('utf-8')
		# Generate a random number r (nonce)
		r = randint(2, p - 1)
		
		# Compute gr and TK
		gr = pow(g, r, p)
		TK = pow(pk_bob, r, p)
		TK_bytes = long_to_bytes(TK, 16) 
		
		# Use TK to encrypt M denoted by C=E(TK, M) AES encryption
		iv = b'\x85\xf2\xf5\x84\xa0y!#t\xdf\xeb\xa2u\x9b\xabp'
		cipher = AES.new(TK_bytes, AES.MODE_CBC, iv)
		C_bytes = cipher.encrypt(pad(M_byte, AES.block_size))
		C = b64encode(C_bytes).decode('utf-8')
		
		# Compute LK
		LK = pow(pk_bob, sk_alice, p)
		hash_object = str(LK) + str(gr) + C + str(LK)
		MAC = hashlib.sha1(hash_object.encode('utf-8')).hexdigest()
		
		send_data = f"{gr},{C},{MAC}"
		s.sendto(send_data.encode('utf-8'), (remote_ip, remote_port))
		print()
		print("Alice Sent : ")
		print("M: ", M)
		print("g^r: ", gr)
		print("C: ", C)
		print("MAC: ", MAC)
		print()
		
		
		data, address = s.recvfrom(4096)
		gr, C, MAC = data.decode('utf-8').split(',')
		gr = int(gr)
		#print("address", address)
		
		# Compute TK
		TK = pow(gr, sk_alice, p)
		TK_bytes = long_to_bytes(TK, 16)
		
		# Compute LK
		LK = pow(pk_bob, sk_alice, p)
		hash_object = str(LK) + str(gr) + C + str(LK)
		MAC2 = hashlib.sha1(hash_object.encode('utf-8')).hexdigest()
		#print("MAC1: ", MAC)
		#print("MAC2: ", MAC2)
		if MAC == MAC2:
			ciphertext = b64decode(C)
			iv = b'\x85\xf2\xf5\x84\xa0y!#t\xdf\xeb\xa2u\x9b\xabp'
			cipher = AES.new(TK_bytes, AES.MODE_CBC, iv)
			Mprime_byte = unpad(cipher.decrypt(ciphertext), AES.block_size)
			Mprime = Mprime_byte.decode('utf-8') 
			print("**The decryption on**")
			print(f"({gr},{C},{MAC})")
			print("**is**")
			print(Mprime)
			print()
		else:
			print("**The decryption on**")
			print(f"({gr},{C},{MAC})")
			print("**is**")			
			print("ERROR")
			print()
# close the socket
s.close()
