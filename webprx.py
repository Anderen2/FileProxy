#Thanks to Luu Gia Thuy for the Python HTTP Proxy v1.0

import os,sys,thread,socket

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = True           # set to True to see the debug msgs

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
		print("Connection!")
		conn, client_addr = s.accept()
		thread.start_new_thread(proxy_thread, (conn, client_addr))
		
	s.close()

def proxy_thread(conn, client_addr):
	request = conn.recv(MAX_DATA_RECV) #Browser Request

	#Parse the first line
	first_line = request.split('\n')[0]
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
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
		s.connect((webserver, port))
		s.send(request)         # send request to webserver

		while True:

			### RECIEVE ( RX ) ###

			# receive data from web server
			data = s.recv(MAX_DATA_RECV)
			
			if (len(data) > 0):
				# send to browser
				conn.send(data)
			else:
				break
		s.close()
		conn.close()
	except socket.error, (value, message):
		if s:
			s.close()
		if conn:
			conn.close()
		print "Runtime Error:", message
		sys.exit(1)

if __name__ == '__main__':
	main()

