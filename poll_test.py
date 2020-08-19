from select import *
from socket import *
f = open("test.log")

sockfd = socket()
sockfd.bind(('0.0.0.0',8888))
sockfd.listen(5)

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('0.0.0.0',9999))

map = {f.fileno():f,sock.fileno():sock}

p = poll()
p.register(f,POLLOUT|POLLERR)
p.register(sockfd,POLLIN|POLLERR)

events = p.poll()
print(events)