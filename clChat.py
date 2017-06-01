#!/usr/bin/env python3
import socket
import sys
import os
import ast
import comClass


if __name__ == "__main__":
    
    #
    #   BEGIN INIT SETUP
    #

    posArgs = ["-s", "-c", "-lc", "-ls"]

    if(len(sys.argv) != 2):
        print("Usage: ./edchat.py <-s|-c|-lc|-ls>")
        print("Args:")
        print("\t-s : Start a chat server that is internet facing, will require a router with uPnP enabled. Will tell you your ip/port for others to connect")
        print("\t-c : Connect to a chat server that is internet facing. Will be asked to specify ip/hostname of server to connect to")
        print("\t-ls : Start a chat server that is visible from your local network. Will have to specify your ip")
        print("\t-lc : Connect to a chat server that is visible from your local network. Will be asked to specify ip/hostname of server to connect to")
        sys.exit()
    else:
        args = sys.argv
    if(args[1] not in posArgs):
        print("Usage: ./edchat.py <-s|-c>")
    
    if(args[1] == "-c" or args[1] == "-lc"):
        sucFoundPort = False
        ip = input("Enter ip to connect to: ")
        s = socket.socket()         # Create a socket object
        if(args[1] != "-lc"):
            port = 49152
            while(not sucFoundPort):
                try:
                    s.connect((ip, int(port)))
                    sucFoundPort = True
                except:
                    port += 1
        else:
            port = input("Enter port to connect on: ")
            s.connect((ip, int(port)))

        comInit = comClass.comClass("C")
    elif(args[1] == "-s"):
        import miniupnpc
        sucInPort = False
        mu = miniupnpc.UPnP()
        mu.discover()
        mu.selectigd()
        ip = mu.lanaddr
        externalIp = mu.externalipaddress()
        port = 49152
        s = socket.socket()         # Create a socket object
        while(not sucInPort):
            try:
                s.bind((ip, int(port)))        # Bind to the port
                sucInPort = True
            except:
                port += 1
        mapPort = port
        mapPortTrigger = mu.getspecificportmapping(mapPort, "TCP")  #start with this
        while(mapPortTrigger != None and port < 65536):
            mapPort += 1
            mapPortTrigger = mu.getspecificportmapping(mapPort, "TCP")  #start with this
        mapping = mu.addportmapping(mapPort, "TCP", ip, port, "EDChat port %u" %(port), '')
        if(mapping):
            print("Starting chat server on %s:%s" %(externalIp, mapPort))
    
        try:
            s.listen(5)                 # Now wait for client connection.
            s, addr = s.accept()     # Establish connection with client.
        except KeyboardInterrupt as e:
            delMap = mu.deleteportmapping(port, "TCP")
            if(delMap):
                print("Successful exit, goodbye")
            else:
                print("Error on exit")
            print("Goodbye!")
            sys.exit()
        
        comInit = comClass.comClass("S")
    elif(args[1] == "-ls"):
        ip = input("Enter your local ip address: ")
        port = input("Enter port to listen for connections on: ")
        s = socket.socket()         # Create a socket object
        s.bind((ip, int(port)))        # Bind to the port
        try:
            s.listen(5)                 # Now wait for client connection.
            s, addr = s.accept()     # Establish connection with client.
        except KeyboardInterrupt as e:
            print("Goodbye!")
            sys.exit()
        comInit = comClass.comClass("S")
        

    name = input("Enter name: ")

    #
    #   END INIT SETUP
    #
    
    inputProc = os.fork()
    try:
        if inputProc != 0:
            conArgs = str(s.recv(4096))[2:-1]
            conArgs = ast.literal_eval(conArgs)
            print("You are now connected to " + conArgs[0])
            comInit.sentStringGet(s, conArgs[0])
        else:
            conArr = "['%s']" %(name,)
            s.send(conArr.encode())
            comInit.sendStringGet(s, name)
        os.waitpid(inputProc, 0)
    except KeyboardInterrupt as e:
        if inputProc == 0:
            if(args[1] == "-s"):
                delMap = mu.deleteportmapping(port, "TCP")
                if(delMap):
                    print("Successful exit, goodbye")
                else:
                    print("Error on exit")
        else:
            comInit.removeTempFile()
            print("Goodbye!")
        
        sys.exit()
    except ChildProcessError as e:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        raise(e)
