#Socket testing
import socket

request="""GET http://en.wikipedia.org/wiki/County_of_London HTTP/1.1
Host: en.wikipedia.org
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Cookie: mediaWiki.user.id=w3ESkQzVdmnxFLZLIFZVzB6NTdQ9EcCj; centralnotice_bannercount_fr12=5; centralnotice_bucket=0-4.2; mediaWiki.user.bucket%3Aext.articleFeedbackv5%4011-tracking=11%3Aignore; mediaWiki.user.bucket%3Aext.articleFeedbackv5%406-form=6%3A6; mediaWiki.user.bucket%3Aext.articleFeedbackv5%405-links=5%3AX; edittoolscharsubset=0
Connection: keep-alive

"""

print("Creating Socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting")
s.connect(("en.wikipedia.org", 80))

print("Sending request")
s.send(request)

while True:
	print("Waiting for server...")
	data=s.recv(4096)

	print ("Got data:")
	print data
	if len(data)<1:
		break