# clChat

## Overview

clChat is a small (for now POC) program that allows for instant messaging via a command line on Linux or Mac computers, with no need for a central server or relay point. It allows for communication on local area networks OR across the internet as a whole. The local area network communication is fairly simple in that the only requirement is that users be on the same net. For communication across the internet however, a router that is compatible with the Universal Plug and Play protocols (UPNP) is necessary. On most regular home internet connections, this is a non issue. Places where enterprise networking is in place (think universities) will most likely not be able to use this program however.

## Usage

clChat works in one of two ways. LAN mode and WAN mode.

### Lan Mode

For LAN mode, the person starting the server needs to run from their terminal

```
./clChat.py -ls
```

After this, they will be prompted to put in the IP and port they would like to listen on. If for whatever reason the runner of the program would like all communication to happen on the same machine, they could make this `localhost` or `127.0.0.1`. If someone would like to communicate with someone else on the same net, they would enter either `0.0.0.0` or whatever IP they were assigned during the DHCP process. After the person starting the server is done, the person acting as client and connecting to the server user will run from their terminal

```
./clChat.py -lc
```

Following this, the client will enter the IP and port the server user provides them. After this, a tunnel is started and communication can begin.

### Wan Mode

For WAN mode, the person starting the server needs to run from their terminal

```
./clChat.py -s
```

After this, the program handles acquisition of the public IP address the client should connect to, and picks a port after communication with the router finds a usable mapping from external to internal network. The client then only needs the server users public IP address. With this in hand, the client user runs

```
./clChat.py -c
```

and enters the IP of  the server user. 

## More info
This little program began as a project stemming from my desire to figure out how to somehow automate the opening of a port on a router to a user on the network behind the router. I then learned that UPNP implemented this exactly already. Before I would consider this program really usable for any stealthy communication however, some encryption of the tunnel the communication happens through must be implemented. That is on the to-do. For now, communication relating to non sensitive or private issues is perfectly fine using it. 
