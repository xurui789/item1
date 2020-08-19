from socket import *
from select import select
import re


class WebSever:
    def __init__(self, host='0.0.0.0', port=80, html=None):
        self.host = host
        self.port = port
        self.html = html  # 网页的更目录
        self.create_socket()
        self.bind()
        self.rlist = []
        self.wlist = []
        self.xlist = []

    # 启动服务，开始监听客户端的连接
    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind((self.address))

    #启动服务器
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        self.rlist.append(self.sock)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)

            for r in rs:
                if r is self.sock:
                    connfd, addr = r.accept()
                    print("Connect from", addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    try:
                        self.handel(r)
                    except:
                        r.close()
                        self.rlist.remove(r)

    #实现HTTP的功能
    def handel(self, connfd):
        #接收浏览器请求
        request = connfd.recv(1024*10).decode()
        #解析请求，获取请求内容
        pattern = "[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern,request)
        if result:
            info = result.group('info')
            print("请求内容：",info)
            self.send_html(connfd,info)
        else:
            connfd.close()
            self.rlist.remove(connfd)
            return
    #发根据请求发送响应数据
    def send_html(self, connfd, info):
        #info -->/ 请求 主页 否则 具体请求内容
        if info =='/':
            filename = self.html + "/index.html"
        else:
            filename = self.html+info

        try:
            f = open(filename,'rb')
        except:
            #文件不存在
            response = "HTTP/1.1 404 NOT Found\r\n"
            response += "Content - Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry...<\h1>"
            response = response.encode()
        else:
            data = f.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%s\r\n"%len(data)
            response += "\r\n"
            response = response.encode()+data
        finally:
            connfd.send(response)

if __name__ == '__main__':
    httpd = WebSever(host='0.0.0.0', port=8000, html="./static")
    httpd.start()
