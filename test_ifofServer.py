import unittest
import threading
import socket
import time
import traceback

from ifofServer import Server, IFOF

class testServer(unittest.TestCase):
    def setUp(self):
        self.port = 3233
        self.role = IFOF.server
        self.pass_pair = ['고라니','자기장']
        self.t1 = threading.Thread(target=self.server)
        self.t1.start()
        time.sleep(1)

    def tearDown(self):
        self.t1.join()

    def server(self):
        Server(self.pass_pair, self.role, self.port)

    def test_server_fails(self):
        sock = socket.socket()
        addr = ('localhost', self.port)
        sock.connect(addr)
        res = sock.recv(1024)
        print('[TEST Received] : ', end='')
        print(str(res, 'utf-8'))

        sock.send(bytes("돼지\n",'utf-8'))
        res = sock.recv(1024)
        time.sleep(0.1)
        sock.send(bytes("소\n", 'utf-8'))
        res = sock.recv(1024)
        time.sleep(0.1)
        sock.send(bytes("닭\n",'utf-8'))
        res = sock.recv(1024)
        time.sleep(0.1)

        res = sock.recv(1024)
        print('[TEST] Receviced : ', end='')
        print(str(res, 'utf-8'))
        self.assertTrue("killed" in res.decode(), msg="Not dead")

    def test_server_success(self):
        try:
            sock = socket.socket()
            addr = ('localhost', self.port)
            sock.connect(addr)
            res = sock.recv(1024)
            self.assertTrue("Freeze" in res.decode())

            sock.send(bytes("자기장\n",'utf-8'))
            res = sock.recv(1024)
            self.assertTrue("고라니" in res.decode())
            time.sleep(0.1)

            res = sock.recv(1024)
            print('[TEST] Receviced : ', end='')
            print(str(res, 'utf-8'))
            sock.send(bytes("수고하십니다\n", 'UTF-8'))

        except Exception as e:
            traceback.print_exc(e)


class testServeronClient(unittest.TestCase):
    def setUp(self):
        self.port = 3233
        self.role = IFOF.client
        self.pass_pair = ['고라니','자기장']
        self.t1 = threading.Thread(target=self.client)
        self.t1.start()
        time.sleep(1)

    def tearDown(self):
        self.t1.join()

    def client(self):
        Server(self.pass_pair, self.role, self.port)

    def test_server_success(self):
        protocol = IFOF(self.pass_pair[0], self.pass_pair[1])
        sock = socket.socket()
        addr = ('localhost', self.port)
        sock.connect(addr)

        sock.send(protocol.initProtocol())
        time.sleep(0.1)
        sock.send(bytes(self.pass_pair[0] + '\n','utf-8'))
        res = sock.recv(1024)
        print('[TEST] Receviced : ', end='')
        print(str(res, 'utf-8'))

        self.assertTrue(self.pass_pair[1] in res.decode())

        sock.send(bytes("고생하십니다.\n",'utf-8'))
        res = sock.recv(1024)
        print('[TEST] Receviced : ', end='')
        print(str(res, 'utf-8'))

    def test_server_fails(self):
        protocol = IFOF(self.pass_pair[0], self.pass_pair[1])
        sock = socket.socket()
        addr = ('localhost', self.port)
        sock.connect(addr)

        sock.send(bytes("Hi!\n",'utf-8'))
        res = sock.recv(1024)
        print('[TEST] Receviced : ', end='')
        print(str(res, 'utf-8'))
        self.assertFalse(self.pass_pair[0] in res.decode())

if __name__ == '__main__':
    unittest.main()