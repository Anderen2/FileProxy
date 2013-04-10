#Internet Proxy/Adapter/Whatever frontend v1.0

#Thanks to Luu Gia Thuy for the Python HTTP Proxy v1.0 layer

import os,sys,thread,socket
from random import randrange
from time import sleep

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = False           # set to True to see the debug msgs

DIRECTORY="/home/anderen2/Loggmtest/"

def main():
	if (len(sys.argv)<2):
		print "usage: proxy <port>"  
		return sys.stdout    

	host = 'localhost'
	port = int(sys.argv[1])
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(BACKLOG)

	except socket.error, (value, message):
		if s:
			s.close()
		print "Could not open socket:", message
		sys.exit(1)

	while True:
		conn, client_addr = s.accept()
		thread.start_new_thread(proxy_thread, (conn, client_addr))
		
	s.close()

def proxy_thread(conn, client_addr):
	request = conn.recv(MAX_DATA_RECV) #Browser Request
	r2=request

	#Parse the first line
	first_line = r2.split('\n')[0]
	url = first_line.split(' ')[1] #Get url

	if (DEBUG):
		print first_line
		print
		print "URL:",url
		print
	
	#Find the webserver and port
	http_pos = url.find("://")          # find pos of ://
	if (http_pos==-1):
		temp = url
	else:
		temp = url[(http_pos+3):]       # get the rest of url
	
	port_pos = temp.find(":")           # find the port pos (if any)

	#Find end of web server
	webserver_pos = temp.find("/")
	if webserver_pos == -1:
		webserver_pos = len(temp)

	webserver = ""
	port = -1
	if (port_pos==-1 or webserver_pos < port_pos):      # default port
		port = 80
		webserver = temp[:webserver_pos]
	else:       # specific port
		port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
		webserver = temp[:port_pos]

	print "Connecting to:", webserver, port

	try:

		### TRANSMITT ( TX ) ###

		# create a socket to connect to the web server
		# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
		# s.connect((webserver, port))
		# s.send(request)         # send request to webserver
		
		tx = open(DIRECTORY+"tx", "w+")
		rx = open(DIRECTORY+"rx", "r")

		doit=True
		if len(request)>1:
			tx.write(request+chr(4))
			tx.flush()
		else:
			doit=False

		while doit:

			### RECIEVE ( RX ) ###

			# receive data from web server
			sleep(0.1)
			rx.seek(0)
			data = rx.read()
			
			if (len(data) > 0):
				if data[len(data)-1]==chr(4):
					print("Got response, sending to browser")
					data=data[:len(data)-2]
					conn.send(data)
					print("Clearing RX")
					rx.close()
					rx = open(DIRECTORY+"rx", "w")
					rx.write("")
					rx.close
					rx = open(DIRECTORY+"rx", "r")
					tx.close()
					conn.close()

		#If timeout
		# tx.close()
		# conn.close()
	except socket.error, (value, message):
		# if rx:
		# 	rx.close()
		# if conn:
		# 	conn.close()
		print "Runtime Error:", message
		# sys.exit(1)
		pass

if __name__ == '__main__':
	main()


