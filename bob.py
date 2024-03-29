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
sk_bob = int(f.readline())
pk_alice = int(f.readline())
f.close()

pk_bob = pow(g, sk_bob, p)

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (local_ip, local_port)
s.bind(server_address)
print("Do Ctrl+c to exit the program !!")
print()

while True:
		print("####### Bob is listening #######")
		print()
		data, address = s.recvfrom(4096)
		gr, C, MAC = data.decode('utf-8').split(',')
		gr = int(gr)
    
    # Compute TK
		TK = pow(gr, sk_bob, p)
		TK_bytes = long_to_bytes(TK, 16)
		
		# Compute LK
		LK = pow(pk_alice, sk_bob, p)
		hash_object = str(LK) + str(gr) + C + str(LK)
		MAC2 = hashlib.sha1(hash_object.encode('utf-8')).hexdigest()
		#print("C:", C)
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
    
    
		M = input("Type some text to send to Alice => ")
		M_byte = M.encode('utf-8')
		# Generate a random number r (nonce)
		r = randint(2, p - 1)
		
		gr = pow(g, r, p)
		TK = pow(pk_alice, r, p)
		TK_bytes = long_to_bytes(TK, 16)
		# Use TK to encrypt M denoted by C=E(TK, M) AES encryption
		iv = b'\x85\xf2\xf5\x84\xa0y!#t\xdf\xeb\xa2u\x9b\xabp'
		cipher = AES.new(TK_bytes, AES.MODE_CBC, iv)
		C_bytes = cipher.encrypt(pad(M_byte, AES.block_size))
		C = b64encode(C_bytes).decode('utf-8')
		
		# Compute LK
		LK = pow(pk_alice, sk_bob, p)
		hash_object = str(LK) + str(gr) + C + str(LK)
		MAC = hashlib.sha1(hash_object.encode('utf-8')).hexdigest()
		
		# send data to alice
		send_data = f"{gr},{C},{MAC}"
		s.sendto(send_data.encode('utf-8'), (remote_ip, remote_port))
		print()
		print("Bob Sent : ")
		print("M: ", M)
		print("g^r: ", gr)
		print("C: ", C)
		print("MAC: ", MAC)
		print()
