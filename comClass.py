import os
import getch
import sys

class comClass:
	def __init__(self, mode):
                self.tempFile = "tmp" + mode + ".txt"

	def removeTempFile(self):
		if(os.path.isfile(self.tempFile)):
			os.remove(self.tempFile)

	def sendStringGet(self, s, name):
		while True:
			sendString = ""
			c = ''
			sData = open(self.tempFile, 'w')
			sData.close()
			try:
				while c != '\n':
					c = getch.getch()
					sData = open(self.tempFile, 'w')
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
				self.removeTempFile()
				return
			except OverflowError:
				self.removeTempFile()
				return
			except BrokenPipeError:
				self.removeTempFile()
				return
			except Exception as e:
				self.removeTempFile()
				raise(e)

	def sentStringGet(self, s, pName):
		while True:
			try:
				sentString = str(s.recv(4096))[2:-1]
				if(len(sentString) == 0):
					print("\n\n\nPartner disconnected, press ctrl-c to exit")
					raise(KeyboardInterrupt)
				sys.stdout.flush()
				currTextFile = open(self.tempFile)
				currText = currTextFile.read()
				for char in range(len(currText)):
					sys.stdout.write('\b \b')
				print(pName + ": " + sentString + "\n")
				print(currText, end='')
				currTextFile.close()
				sys.stdout.flush()
			except KeyboardInterrupt as e:
				self.removeTempFile()
				return
			except Exception as e:
				raise(e)
