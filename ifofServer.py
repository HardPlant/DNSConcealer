import socket
import traceback
import random

class IFOF:
    server = 1
    client = 0
    def __init__(self, chall, resp):
        self.chall = chall
        self.res = resp
        self.turn = 0
        self.count = 0

    def initProtocol(self):
        return bytes("Freeze!\n", 'utf-8')

    def challenge(self):
        return bytes(self.chall, 'utf-8')

    def response(self):
        return bytes(self.res, 'utf-8')

    def endProtocol(self, positive = False):
        if positive:
            return bytes("You've authenticated.\n flag{aR3alSt0ry1nKCTC}\n", 'utf-8')

        return bytes(("You have killed by M16A4.\n"), 'utf-8')

def firstInit(connection_sock, protocol):
    print("[Server] Protocol Init sended: ")
    connection_sock.send(protocol.initProtocol())
    protocol.count = 0
    try:
        while protocol.count < 3:
            protocol.count = protocol.count + 1
            print("[Server] Try ", protocol.count, ': ')
            connection_sock.send(protocol.challenge())
            response = connection_sock.recv(1024)
            print("[Server] Result :", response.decode().rstrip(), '/ ', protocol.response().decode())
            print("[Server] Result :", response.decode().rstrip() == protocol.response().decode())

            print("[Server] Received :", str(response.decode()))
            if response.decode().rstrip() == protocol.response().decode().rstrip():
                print("[Server] Try Successed")
                connection_sock.send(protocol.endProtocol(positive=True))
                print("[Server] Protocol Sent: ", protocol.endProtocol(positive=True))
                resp = connection_sock.recv(1024)
                print("[Server] Received :", resp.decode())
                connection_sock.close()
                return True

        print("Try Failed.")
        connection_sock.send(protocol.endProtocol())

    except Exception as e:
        print(e)

    return False

def lastInit(connection_sock, protocol):
    print("[Server] Client Init: ")

    resp = connection_sock.recv(1024)
    print("[Server] Server Says: ")
    print(resp.decode())

    if resp.decode().rstrip() == protocol.initProtocol().decode().rstrip():
        print("[Server] Client Protocol Started: ")
        resp = connection_sock.recv(1024)
        print("[Server] Client Respose: ", resp.decode())
        if resp.decode().rstrip() == protocol.challenge().decode().rstrip():
            connection_sock.send(protocol.response() + bytes('\r\n'))
            connection_sock.recv(1024)
            connection_sock.send(bytes("Bye!\n",'utf-8'))
        else:
            connection_sock.send(protocol.endProtocol() + bytes('\r\n'))
            return


    else:
        connection_sock.send(bytes("Enemy spotted!\n", 'utf-8'))

def Server(pass_pair, role, port):
    protocol = IFOF(pass_pair[0], pass_pair[1])

    serverSock = socket.socket()
    serverSock.bind(('',port))
    serverSock.listen(1)
    print("[Server] running at ", port)
    while True:
        try:
            connection_sock, client_addr = serverSock.accept()
            print("[Server] connected as ", role)

            if role == IFOF.server :
                firstInit(connection_sock, protocol)

            elif role == IFOF.client:
                rad = int(random.random()*10)
                print('[Server] ', rad)
                if rad % 2 == 0 :
                    print("[Server] Client Founds you.")
                    firstInit(connection_sock, protocol)
                if rad % 2 == 1 :
                    print("[Server] Client was Founded.")
                    lastInit(connection_sock, protocol)

        except Exception as e:
            print(e)

        finally:
            connection_sock.close()

if __name__ == '__main__':
    port = input("포트: ")
    role = input("초소 : S, 서버 : C : ")
    pass_chall = input("문어: ")
    pass_resp = input("답어: ")
    pass_pair = [pass_chall,pass_resp]
    if role == 'S': role = IFOF.server
    elif role == 'C': role = IFOF.client

    Server(pass_pair, role, int(port))



