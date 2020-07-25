#!/usr/bin/python3

import socket

import time
import random
import threading

# CONSTANTS
SERVER_IP = '185.60.170.111'
SERVER_PORT = 56789
KEEP_ALIVE_TIME = 5

def punch_hole(peer_socket, remote_peer_tuple, stop_event):
    while not stop_event.wait(1):
        peer_socket.sendto("Punch Hole".encode(), remote_peer_tuple)

        time.sleep(1)

def keep_alive(peer_socket, remote_peer_tuple, stop_event):
    while not stop_event.wait(1):
        peer_socket.sendto("keep_alive".encode(), remote_peer_tuple)
        time.sleep(KEEP_ALIVE_TIME)

def connect_to_peer(peer_socket, remote_peer_tuple):
    # Initiate hole punching packet sending
    hole_punched = threading.Event()
    punch_hole_thread = threading.Thread(target=punch_hole, args=(peer_socket, remote_peer_tuple, hole_punched))
    punch_hole_thread.start()

    # Recieve the hole punching packet and send an Acknowledgment packet in return
    message, addr = peer_socket.recvfrom(1024)
    peer_socket.sendto('ACK'.encode(), remote_peer_tuple)

    # Stop the hole punching packets
    hole_punched.set()

def get_peer():
    # Creating a UDP socket that will serve the peer
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # Bind the UDP socket to an arbitrary port
    # If your router supports hairpin and you want to check the code on your own computer without a friend assist,
    # comment the .bind line or change the port number between peers :)   
    # peer_socket.bind(("0.0.0.0", 45678)) 

    # Sending the server a packet and thereby adding us to the PEERS list
    peer_socket.sendto("Connecting_To_Server".encode(), (SERVER_IP, SERVER_PORT))

    # Wait to get remote peer connection details
    remote_peer_tuple, server_address = peer_socket.recvfrom(1024)
    remote_peer_tuple = eval(remote_peer_tuple.decode()) # remote peer (ip, port) tuple

    # Remove yourself from PEERS list in the server
    peer_socket.sendto("CLOSE".encode(), (SERVER_IP, SERVER_PORT))

    # Try to connect to remote peer
    connect_to_peer(peer_socket, remote_peer_tuple)

    print("Initiated Connection to peer at " + str(remote_peer_tuple))
    return remote_peer_tuple, peer_socket

if __name__ == '__main__':
    remote_peer_tuple, peer_socket = get_peer()

    # UNCOMMENT the following lines if you want to send keep-alive packets to the remote peer
    # Initiate keep alive packet sending in order to keep the "hole" open
    # pill2kill = threading.Event()
    # keep_alive_thread = threading.Thread(target=keep_alive, args=(peer_socket, remote_peer_tuple, pill2kill))
    # keep_alive_thread.start()

    print("Bye Bye")
 