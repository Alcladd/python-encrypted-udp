Environment to run code in: Linux ubuntu pycryptodome
python version: Python 3.10.12

UDP protocol source: https://linuxhint.com/send_receive_udp_python/
AES encryption source: https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
hashing source: https://docs.python.org/3/library/hashlib.html

instructions to run code:

1. open virtual box and run ubuntu
2. open the terminal and navigate to the directory containing the files
3. open another terminal tab
4. execute the command "python3 alice.py" on the first tab and "python3 bob.py" on the second tab
5. when prompt to enter name of file, enter "alice.txt" for the first tab and "bob.txt" for the second
6. type message to send to bob from alice's end(tab 1) 
7. message will be decrypted on bob's side (tab 2)
8. type message to send to alice from bob's end(tab 2)
9. message will be decrypted on alice's side (tab 1)
10. repeat step 6 to 9 or press ctrl + c to exit the program
