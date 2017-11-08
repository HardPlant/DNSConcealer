import socket
import traceback
from dnslib import DNSRecord


def httpResponse():
    string = 'HTTP/1.1 200 OK\n'
    string += '\n'
    string += '<html>'
    string += '<head><title>Hello Sockets!</title></head>'
    string += '<body>'
    string += '<img src="http://down.humoruniv.org//hwiparambbs/data/editor/thema2/e_2325584567_ecb7fcbe46c764d9c14d38939c3e7fab15daea71.png"/>'
    string += '<p>Wow, this works!</p> <br>'
    string += '<p>This site is made by python socket library! Dehehe!</p> <br> <p>Try Computer Network : Top-down Approach :)</p>'
    string += '<p>Teacher says DNS sends in UDP packet, but I don\'t know what it means.. who knows?</p>'
    string += '<p>Ah, I have a domain, named http://miraicute.org! :) You can get it with HTTP Via Request Header, see and back to this page!</p>'
    string += '<iframe width="560" height="315" src="https://www.youtube.com/watch?v=MmzpkZYPJ-c?&autoplay=1" frameborder="0" allowfullscreen></iframe>'
    string += '</body>'
    string += '</html>'
    return string


def httpError():
    string = 'HTTP/1.1 500 Internal Server Error\n'
    string += '\n'
    string += ' '
    return string

def successResponse():
    string = 'HTTP/1.1 200 OK\n'
    string += '\n'
    string += '<html>'
    string += '<head><title>flag{http_protocol}</title></head>'
    string += '<body>'
    string += '<img src="http://upload2.inven.co.kr/upload/2015/08/22/bbs/i11254207826.jpg"/>'
    string += '<p>Good job!</p>'
    string += '</body>'
    string += '</html>'
    return string

def sendDNS(sock, client_address):
    str = 'flag{DNS_Hides_Power}'
    print('DNS will sent to ' + client_address[0])
    for char in str:
        packet = DNSPacket(char)
        print(packet)
        sock.send(packet)

def DNSPacket(char):
    d = DNSRecord.question("miraicute.com")
    d.header.id = ord(char)
    return d.pack()

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (' ', 12741)
    sock.bind(server_address)
    sock.listen(5)
    print('Server running at' + str(server_address))

    while True:
        msg_sock, client_address = sock.accept()
        print('Socket Established' + str(msg_sock))
        try:
            data = msg_sock.recv(4096)
            print(data)
            req = data.decode().split()
            try:
                index = req.index('Via: ')
                if req[index+1] == 'http://miraicute.org':
                    msg_sock.send(bytes(successResponse(),'UTF-8'))
            except ValueError:
                msg_sock.send(bytes(httpResponse(),'UTF-8'))

        except Exception as e:
            print('Error Occured')
            traceback.print_exc(e)
            msg_sock.send(bytes(httpError(),'UTF-8'))

        finally:
            msg_sock.close()


if __name__ == '__main__':
    server()