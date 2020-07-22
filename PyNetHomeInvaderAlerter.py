import datetime
import socketserver
import sqlite3

# HOST, PORT = 'x.x.x.x', 514
# HOST, PORT = 'localhost', 514
# my_branch test
HOST, PORT = '172.27.0.165', 514


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def __init__(self, db):
        self.db = db
        super().__init__(self)
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        today = datetime.datetime.today()
        name_syslog_file = 'sys.log'
        with open(name_syslog_file, 'a') as f:
           # if 'kernel: wlan0' in str(data):
           #     f.write('IP: ' + self.client_address[0] + '\t' + today.strftime('%Y-%m-%d %H:%M:%S') + '\t' + str(
           #             data[19:]) + '\n')
            f.write(str(data[19:]) + '\n')
           #  print(data)


if __name__ == '__main__':
    try:
        db = sqlite3.connect('destination.db')
        _handler = SyslogUDPHandler(db)
        server = socketserver.UDPServer((HOST, PORT), _handler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        db.close()
        print('Ctrl+C Pressed. Shutting down.')
