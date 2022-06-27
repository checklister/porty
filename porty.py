#!/usr/bin/env python3
from queue import Queue
import socket
from threading import Thread,Lock
from colorama import Fore,init
import argparse

init()
#shortcuts for colours
Y = Fore.YELLOW
G = Fore.LIGHTBLACK_EX
R = Fore.RESET

n_t = 200
q = Queue()
p_l = Lock()


parser = argparse.ArgumentParser(description = "Just test tool to scan port.")
parser.add_argument("host",help = "Our target, Master.")
parser.add_argument("-p","--port",dest = "port_range",default = "1-65535",help = "Range of our interests, Master. Defaul 1 - 65535.")
args = parser.parse_args()
host, port_range = args.host, args.port_range
start_port, end_port = port_range.split("-")
start_port, end_port = int(start_port), int(end_port)

for port in range(start_port,end_port):
	q.put(port)

def scan(port):
	s = socket.socket()
	try:
		s.connect((host,port))
	except:
		with p_l:
			print(f"{G}{host}:{port} is closed.{R}", end = '\r')
	else:
		with p_l:
			print(f"{Y}{host}:{port} is open.   {R}\n")
	finally:
		s.close()

def thread():
	global q
	while True:
		now = q.get()
		scan(now)
		q.task_done()

def main(host):
	global q
	for i in range(n_t):
		t = Thread(target=thread)
		t.daemon = True
		t.start()
	q.join()
main(host)
