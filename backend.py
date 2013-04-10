#Internet Proxy/Adapter/Whatever backend v1.0

#Thanks to Luu Gia Thuy for the Python HTTP Proxy v1.0 layer

import os,sys,thread,socket
from random import randrange
from time import sleep

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = True           # set to True to see the debug msgs

DIRECTORY="/home/anderen2/Loggmtest/"
RXfile = DIRECTORY+"rx"
TXfile = DIRECTORY+"tx"

def main():

	print("\n")

	if (len(sys.argv)<1):
		print "usage: proxy <TXfile> <RXfile>"  
		return sys.stdout
	
	try:
		print("Opening TX")
		tx=open(TXfile, "r")

	except (value, message):
		if rx | tx:
			rx.close()
			tx.close()
		print "Could not open socket:", message
		sys.exit(1)
	
	old=""

	while True:
		sleep(0.1)
		tx.seek(0)
		request = tx.read(MAX_DATA_RECV)

		if len(request)>0 and request[len(request)-1]==chr(4):
			rx=None
			print("Clearing TX")
			tx.close()
			tx=open(TXfile, "w")
			tx.write("")
			tx.close()
			tx=open(TXfile, "r")
			print("Opening thread")
			request=request[:len(request)-2]
			thread.start_new_thread(proxy_thread, (rx, request))

	#s.close()

def proxy_thread(rx, req):
	request = req #Browser Request
	print("\n"+"#"*10+" REQUEST "+"#"*10)
	print(request)

	#Parse the first line
	try:
		first_line = request.split('\n')[0]
		url = first_line.split(' ')[1] #Get url
	except:
		print("Invalid request")
		sys.exit()

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
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((webserver, port))
		s.send(request+"\n\n")         # send request to webserver
		print("Connected to server, and sent request")
		rx = open(RXfile, "a")
		print("Opening RX as writeable")


		while True:
			### RECIEVE ( RX ) ###
			print("Waiting for server response...")
			data = s.recv(4096) #receive data from web server
			print("Got response, dumping data:")
			print data
			
			if (len(data) > 0):
				print("Got data! Sending to frontend through RX")
				rx.write(data)
				rx.flush()

			else:
				print("End of transmission")
				rx.write(chr(4))
				rx.flush()
				break

		s.close()
		rx.close()

	except socket.error, (value, message):
		# if s:
		# 	s.close()
		# if rx:
		# 	rx.write(chr(4))
		# 	rx.flush()
		# 	rx.close()
		# print "Runtime Error:", message
		# sys.exit(1)
		pass

if __name__ == '__main__':
	main()


