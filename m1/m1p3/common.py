#!/usr/bin/python3
# -*- coding: utf-8 -*-

r"""EITN41 http common.

There are many types of HTTP requests. The most frequently used are
- GET,  if the client uses 'requests.get', OR send by browser
- POST: if the client uses 'requests.post'

I will show their format in both binary and plain text, b.c. there are some
special characters in the binary format and we should be careful about that when
constructing the send page.

###############################################################################
#                            HTTP GET from browser                            #
###############################################################################

We use links, like
- http://igor.eit.lth.se:6001/M1P3/generate?seed=YOUR_SEED
- http://igor.eit.lth.se:6001/M1P3/submit?seed=YOUR_SEED&chain=YOUR_CHAIN
to query from browser.

# Firefox sends this request to server ########################################

b'GET /M1P3/generate?seed=0a72 HTTP/1.1\r\nHost: localhost:6001\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: de,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: none\r\nSec-Fetch-User: ?1\r\nPriority: u=0, i\r\n\r\n'

# Below: HTTP GET (from Firefox) #######
GET /M1P3/generate?seed=0a72 HTTP/1.1
Host: localhost:6001
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: de,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i


# Above: HTTP GET (from Firefox) #######

# Google Chrome sends this request to server ##################################

b'GET /M1P3/generate?seed=0a72 HTTP/1.1\r\nHost: localhost:6001\r\nConnection: keep-alive\r\nsec-ch-ua: "Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Linux"\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: de-SE,de;q=0.9,en-SE;q=0.8,en;q=0.7,zh-DE;q=0.6,zh;q=0.5,de-DE;q=0.4,en-US;q=0.3\r\n\r\n'

# Below: HTTP GET (from Chrome) ########
GET /M1P3/generate?seed=0a72 HTTP/1.1
Host: localhost:6001
Connection: keep-alive
sec-ch-ua: "Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Linux"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: de-SE,de;q=0.9,en-SE;q=0.8,en;q=0.7,zh-DE;q=0.6,zh;q=0.5,de-DE;q=0.4,en-US;q=0.3


# Above: HTTP GET (from Chrome) ########

"""

from socketserver import BaseRequestHandler
import socket
from datetime import datetime  # for our block timestamp
import re


class EITN41Server(BaseRequestHandler):
    """EITN41 server."""

    def receive(self):
        """From the received HTTP request, parse important information."""
        http_request = self.request.recv(8192).decode('utf8')
        self.method = re.match(r'\b(GET|POST)\s[^\n]*', http_request).group(1)
        http_header, http_body = http_request.split('\r\n\r\n', 1)
        url = re.sub(r'^(GET|POST)\s+|\s+HTTP/1\.1$', '',
                     http_header.split('\r\n', 1)[0])
        if self.method == 'POST':
            self.path = url
            self.body = http_body
        if self.method == 'GET':
            self.path = '/' + url.split('/')[1]
            self.body = url.replace(self.path+'/', '')
        return self.body

    def http_response_construct(self, content_type, content):
        """HTTP response template."""
        return f"""HTTP/1.1 200 OK\r
Content-Type: {content_type}; charset=utf-8\r
Content-Length: {len(content)}\r\n\r
{content}"""

    def send(self, text):
        """Server constructs HTTP response."""
        if self.method == 'GET':
            content = f"""<html>
<head><title>EITN41 Advanced Web Security</title></head>
<body>[{datetime.now()}] $ {self.path}</br>{text}</body>
</html>"""
            http_response = self.http_response_construct("text/html", content)
        if self.method == 'POST':
            content = f"""[{datetime.now()}] $ {self.path}\n{text}"""
            http_response = self.http_response_construct("text/plain", content)
        self.request.sendall(http_response.encode('utf-8'))


class EITN41Client(socket.socket):
    """EITN41 client shared by three assignments."""

    def __init__(self, host, port, method, path):
        """Client init."""
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.host = host
        self.port = port
        self.method = method
        self.path = path

    def http_request_construct(self, url, content):
        """HTTP request template."""
        return f"""{self.method} {url} HTTP/1.1\r
Host: {self.host}:{self.port}
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(content)}\r\n\r
{content}"""

    def send(self, text):
        """Client constructs HTTP request."""
        if self.method == 'GET':
            url = f"""{self.path}/{text}"""
            content = ""
            http_request = self.http_request_construct(url, content)
        if self.method == 'POST':
            url = self.path
            content = f"""{text}"""
            http_request = self.http_request_construct(url, content)
        self.sendall(http_request.encode('utf-8'))

    def receive(self):
        """Receive HTTP response and extract the body."""
        http_response = self.recv(8192)
        http_response = http_response.decode('utf8')
        http_header, http_body = http_response.split('\r\n\r\n', 1)
        if self.method == 'GET':
            return re.search(r'<body>(.*?)</body>', http_body,
                             re.DOTALL).group(1).split('</br>')[1]
        if self.method == 'POST':
            return http_body.splitlines()[1]
