from socket import *
from select import *

sockfd = socket()
sockfd.bind(('0.0.0.0', 8888))
sockfd.listen(5)

# 防止传输过程阻塞
sockfd.setblocking(False)

p = poll()
map = {sockfd.fileno(): sockfd}
p.register(sockfd,POLLIN)

while True:

    events = p.poll()

    for fd, event in events:
        if fd == sockfd.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            connfd.setblocking(False)
            p.register(connfd, POLLIN)
            map[connfd.fileno()] = connfd
        elif event==POLLIN:
            data = map[fd].recv(1024)
            # 客户端退出
            if not data:
                p.unregister(fd)
                map[fd].close()
                del map[fd]  # 移除监控

                continue
            print(data.decode())
            map[fd].send(b"OK")
