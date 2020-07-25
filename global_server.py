#!/usr/bin/python3

import socket
import threading as thread

import time
import random

import sys

# CONSTANTS
IP = "0.0.0.0"
PORT = 56789
PEERS = [] # [ "external_address": <eAddr>, "external_port": <ePort>} ] -> EXAMPLE: [ {"external_address": "185.60.170.111", "extranl_port": 8080}]

def initiate_connection(peer_address, server_socket):
    # Retrive Random Peer
    list_without_peer_address = [peer for peer in PEERS if peer['external_address'] != peer_address[0] or peer['external_port'] != peer_address[1]] #?#

    random_peer_dict = random.choice(list_without_peer_address) #?#
    random_peer_conn_tuple = (random_peer_dict['external_address'], random_peer_dict['external_port'])

    try:
        # Send to the peer, the random peer details
        server_socket.sendto(str(random_peer_conn_tuple).encode(), peer_address)

        # Send to the random peer, the peer details
        server_socket.sendto(str(peer_address).encode(), random_peer_conn_tuple)

        # Connection initiation message
        print(str(peer_address) + " <----------> " + str(random_peer_conn_tuple) + "\n")
    except:
        print("An error has occured")

def is_new_peer(peer_address):
    # Checking if peer already registered to the server
    for peer in PEERS:
        if peer['external_address'] == peer_address[0] and peer['external_port'] == peer_address[1]:
            return 0
    
    return 1

def add_peer(peer_address):
    peer_global_ip = peer_address[0]
    peer_global_port = peer_address[1]

    PEERS.append( {"external_address": peer_global_ip, "external_port": peer_global_port} )
    print(str(peer_address) + " joined as a peer!")

def remove_peer(peer_address):
    for peer in PEERS:
        if peer['external_address'] == peer_address[0] and peer['external_port'] == peer_address[1]:
            PEERS.remove(peer)
            
            print(str(peer_address) + " left the network!")
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket
    server_socket.bind((IP, PORT))

    while (True):
        (peer_message, peer_address) = server_socket.recvfrom(1024)

        if 'CLOSE' in peer_message.decode():
            remove_peer(peer_address)
        elif is_new_peer(peer_address):   
            add_peer(peer_address)

        if (len(PEERS) > 1):
            initiate_connection(peer_address, server_socket)

    server_socket.close()

if __name__ == '__main__':
    main()
