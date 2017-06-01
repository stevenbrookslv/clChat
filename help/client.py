#!/usr/bin/env python3

import socket
import sys
import os
import getch
import ast
import miniupnpc

def removeTempFile():
	if(os.path.isfile("tmpC.txt")):
		os.remove("tmpC.txt")

def sendStringGet(s, name):
	while True:
		sendString = ""
		c = ''
		sData = open("tmpC.txt", 'w')
		sData.close()
		try:
			while c != '\n':
				c = getch.getch()
				sData = open("tmpC.txt", 'w')
				if(ord(c) >= 32 and ord(c) <= 125):
					sendString += c
					print(c, end='')
				elif(str(ord(c)) == str(0x7f)):
					sys.stdout.write('\b \b')
					sendString = sendString[:-1]
				sys.stdout.flush()
				sData.write(sendString)
				sData.close()
			
			for char in range(len(sendString)):
				sys.stdout.write('\b \b')
			
			print("You: " + sendString + "\n")
			if(sendString != ""):
				s.send(sendString.encode())
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

def sentStringGet(s, pName):
	while True:
		try:
			sentString = str(s.recv(4096))[2:-1]
			if(len(sentString) == 0):
				print("\n\n\nPartner disconnected, press ctrl-c to exit")
				raise(KeyboardInterrupt)
			sys.stdout.flush()
			currTextFile = open("tmpC.txt")
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

ip = input("Enter ip to connect to: ")
port = input("Enter port to connect to: ")
name = input("Enter name: ")

s = socket.socket()         # Create a socket object

s.connect((ip, int(port)))

inputProc = os.fork()
try:
	if inputProc != 0:
		conArgs = str(s.recv(4096))[2:-1]
		conArgs = ast.literal_eval(conArgs)
		print("You are now connected to " + conArgs[0])
		sentStringGet(s, conArgs[0])
	else:
		conArr = "['%s']" %(name,)
		s.send(conArr.encode())
		sendStringGet(s, name)
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
	
