#!/usr/bin/python3

import socket
import random

# CONSTANTS
PORT = 56789
PEERS = [] # [ {"external_address": <eAddr>, "external_port": <ePort>} ] -> EXAMPLE: [ {"external_address": "185.60.170.111", "extranl_port": 8080} ]

def initiate_connection(peer_address, server_socket, peer_code):
    # Retrive Random Peer
    list_without_peer_address = # generate a list without the current peer_address in it

    random_peer_dict = # get a random peer from the generated list above, HINT: random
    random_peer_conn_tuple = # create a tuple from the random_peer_dict as follows: (ip, port)

    try:
        # Send to the peer, the random peer details
        # CODE HERE...

        # Send to the random peer, the peer details
        # CODE HERE...

        # Connection initiation message
        print(str(peer_address) + " <----------> " + str(random_peer_conn_tuple) + "\n")
    except:
        print("An error has occured")

def is_new_peer(peer_address):
    # Checking if peer already registered to the server
    
    # HINT: Iteration is the key
    # NOTE: Don't forget to check the port number! 

def add_peer(peer_address):
    print(str(peer_address) + " joined the server!")

    # Adding a peer in the following manner: { "external_address": <peer_global_ip>, "external_port": <peer_global_port> }

    # NOTE: peer_address is a tuple: (ip, port)
    
    # PEERS.append( ? ) -> UCOMMENT THIS LINE

def remove_peer(peer_address):
    print(str(peer_address) + " left the server!")

    # Removing a peer from the PEERS list

    # HINT: iteration is good!
    # NOTE: .remove() function will remove an element from the list

def main():
    # Creating a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket

    # Binding the socket to a specific port number
    server_socket.bind(("0.0.0.0", PORT))

    while (True):
        # Waiting to recieve peers that want to connect to other peers
        (peer_message, peer_address) = server_socket.recvfrom(1024)

        # if a peer is sending a CLOSE message, remove the peer from the PEERS list
        if 'CLOSE' in peer_message.decode():
            remove_peer(peer_address)

        # if a new peer is connection to the server, add him to the PEERS list
        elif is_new_peer(peer_address):   
            add_peer(peer_address)

        # If there is more than 1 peer connected to the server, try to initiate a direct connection between them
        if (len(PEERS) > 1):
            initiate_connection(peer_address, server_socket, peer_message.decode())

    server_socket.close()

if __name__ == '__main__':
    main()
