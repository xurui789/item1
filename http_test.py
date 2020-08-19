from socket import *


sock = socket()
sock.bind(('0.0.0.0',8888))
sock.listen(5)

connfd,addr = sock.accept()
data = connfd.recv(1024*10)
print(data.decode())

html = "HTTP/1.1 200 OK\r\n"
html +="Content-Type:text/html\r\n"
html +="\r\n"
with open("python.html") as f:
    html +=f.read()

connfd.send(html.encode())

connfd.close()
sock.close()
