import socketserver
import time

HOST = '127.0.0.1'
PORT = 12366


class MyHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            data = self.rfile.readline().strip()
            print(data)
            print(self.client_address)
            self.wfile.write(' %s %s ' % (data, time.ctime()))
            if data == 'exit':
                break


s = socketserver.ThreadingTCPServer((HOST, PORT), MyHandler)
s.serve_forever()

# python -m SimpleHTTPServer 8000
