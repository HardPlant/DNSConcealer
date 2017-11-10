import socket


wcount = 0
weapons = ['M16A4',  'K1', 'K2']
def weapon():
    global wcount, weapons
    wcount = wcount + 1 % len(weapons)
    return weapons[wcount]


class IFOF:
    server = 1
    client = 0
    def __init__(self, chall, resp):
        self.challenge = chall
        self.response = resp
        self.turn = 0
        self.count = 0

    def initProtocol(self):
        return bytes("정지, 정지, 정지! 움직이면 쏜다!")

    def challenge(self):
        return bytes(self.challenge)

    def resp(self):
        return bytes(self.response)

    def endProtocol(self, positive = False):
        if positive:
            return bytes("flag{aR3alSt0ry1nKCTC}")

        return bytes("당신은", weapon(),"에 의해 사망했습니다.")

def Server(pass_pair, role):
    protocol = IFOF(pass_pair[0], pass_pair[1])
    server_btlmsg = "당신은", weapon(),"에 의해 사망했습니다."
    client_respmsg = "고생하십니다."

    serverSock = socket.socket()
    serverSock.bind('')
    serverSock.listen(1)
    while True:
        try:
            connection_sock, client_addr = serverSock.accept()

            if role == IFOF.server :
                connection_sock.send(protocol.initProtocol())
                protocol.count = 0

                while protocol.count < 3 :
                    protocol.count = protocol.count + 1
                    connection_sock.send(protocol.challenge())
                    response = connection_sock.recv(1024)
                    if response == protocol.resp():
                        connection_sock.send(protocol.endProtocol(positive=True))
                        connection_sock.recv(1024)
                        break

                if protocol.count == 3: connection_sock.send(protocol.endProtocol())

            elif role == IFOF.client:
                resp = connection_sock.recv(1024)
                if resp == protocol.initProtocol():
                    resp = connection_sock.recv(1024)
                    if resp == protocol.challenge:
                        connection_sock.send(protocol.response())
                    else:
                        connection_sock.send(server_btlmsg)
                        raise Exception

                    connection_sock.recv(1024)
                    connection_sock.send(client_respmsg)

                else:
                    connection_sock.send(server_btlmsg)

        except Exception as e:
            pass
        finally:
            connection_sock.close()

if __name__ == '__main__':
    role = input("초소 : S, 서버 : C")
    pass_chall = input("문어: ")
    pass_resp = input("답어: ")
    pass_pair = [pass_chall,pass_resp]
    if role == 'S': role = IFOF.server
    elif role == 'C': role = IFOF.client

    Server(pass_pair, role)



