#!/usr/bin/env python3

import sys
import socket
import os
import getch
import ast

def removeTempFile():
	if(os.path.isfile("tmpS.txt")):
		os.remove("tmpS.txt")

def sendStringGet(m, name):
	while True:
		sendString = ""
		c = ''
		sData = open("tmpS.txt", 'w')
		sData.close()
		try:
			while c != '\n':
				c = getch.getch()
				sData = open("tmpS.txt", 'w')
				if(ord(c) >= 32 and ord(c) <= 125):
					sendString += c
					print(c, end='')
				elif(str(ord(c)) == str(0x7f)):
					sys.stdout.write('\b \b')
					sendString = sendString[:-1]
				sys.stdout.flush()
				sData.write(sendString)
				sData.close()
			if(sendString != ""):
				m.send(sendString.encode())
			for char in range(len(sendString)):
				sys.stdout.write('\b \b')
			
			print("You: " + sendString + "\n")
		except KeyboardInterrupt as e:
			removeTempFile()
			return
		except OverflowError:
			removeTempFile()
			return
		except BrokenPipeError:
			removeTempFile()
			return
		except Exception as e:
			removeTempFile()
			raise(e)

def sentStringGet(c, pName):
	while True:
		try:
			sentString = str(c.recv(4096))[2:-1]
			if(len(sentString) == 0):
				print("\n\n\nPartner disconnected, press ctrl-c to exit")
				raise(KeyboardInterrupt)
			sys.stdout.flush()
			currTextFile = open("tmpS.txt")
			currText = currTextFile.read()
			for char in range(len(currText)):
				sys.stdout.write('\b \b')
			print(pName + ": " + sentString + "\n")
			print(currText, end='')
			currTextFile.close()
			sys.stdout.flush()
		except KeyboardInterrupt as e:
			removeTempFile()
			return
		except Exception as e:
			raise(e)

ip = input("Enter ip address: ")
port = input("Enter port to connect to: ")
name = input("Enter name: ")

s = socket.socket()         # Create a socket object
s.bind((ip, int(port)))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
c, addr = s.accept()     # Establish connection with client.


inputProc = os.fork()

try:
	if inputProc != 0:
		conArgs = str(c.recv(4096))[2:-1]
		conArgs = ast.literal_eval(conArgs)
		print("You are now connected to " + conArgs[0])
		sentStringGet(c, conArgs[0])
	else:
		conArr = "['%s']" %(name,)
		c.send(conArr.encode())
		sendStringGet(c, name)
	os.waitpid(inputProc, 0)
except KeyboardInterrupt as e:
	if inputProc == 0:
		print("\n\nGoodbye!")
	else:
		removeTempFile()
	sys.exit(0)
except ChildProcessError as e:
	print("\n\nGoodbye!")
	sys.exit(0)
except Exception as e:
	raise(e)
