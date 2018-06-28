import socket
import select
import logging
import time

def handler_ping(irc, msg):
    irc.send('PONG :%s' % msg['content'])

def handler_376(irc, msg):
    irc.join(irc.channels)

class IRC:
    def __init__(self, user, nick, host, port=6667,
                 channels=[], log_level=logging.INFO):
        self.host = host
        self.port = port
        self.user = user
        self.nick = nick
        self.handlers = dict()
        self.timers = []
        self.channels = channels
        self.recv_buffer = ''

        logging.basicConfig(format='[%(levelname)s] %(message)s',
                            level=log_level)

        self.set_handler('PING', handler_ping)
        self.set_handler('376', handler_376)

    def __connect(self):
        logging.info("connect to %s:%d..." % (self.host, self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, msg):
        logging.info(">>> %s" % (msg))
        self.sock.send(msg.encode('utf-8') + b"\r\n")

    def set_handler(self, cmd, handler):
        if cmd in self.handlers:
            self.handlers[cmd].append(handler)
        else:
            self.handlers[cmd] = [handler]

    def set_timer(self, handler, seconds=1):
        self.timers.append({'handler': handler,
                            'seconds': seconds,
                            'next': int(time.time()) + seconds})

    def __parse_irc_msg(self, data):
        msg = {'full': data[:]}

        if data[0] == ':':
            i = data.index(' ')
            msg['host'] = data[1:i]
            data = data[i+1:]

        i = data.index(' ')
        msg['cmd'] = data[:i]
        data = data[i+1:]

        i = data.find(':')
        if i >= 0:
            msg['args'] = list(filter(lambda x: len(x), data[:i].split(" ")))
            msg['content'] = data[i+1:]
        else:
            msg['args'] = list(filter(lambda x: len(x), data.split(" ")))

        return msg


    def __parse_data(self, data):
        msgs = []
        data = data.decode('utf-8', 'backslashreplace')
        data = self.recv_buffer + data
        self.recv_buffer = ''

        while len(data) > 0:
            i = data.find("\r\n")
            if i >= 0:
                msgs.append(self.__parse_irc_msg(data[:i]))
                data = data[i+2:]
            else:
                self.recv_buffer = data
                data = ''
        return msgs

    def __execute_handlers(self, msgs):
        for msg in msgs:
            cmd = msg['cmd']
            full = msg['full']
            logging.info("<<< %s" % full)
            if cmd in self.handlers:
                for handler in self.handlers[cmd]:
                    handler(self, msg)

    def __execute_timers(self):
        for timer in self.timers:
            if timer['next'] <= int(time.time()):
                timer['handler'](self)
                timer['next'] = int(time.time()) + timer['seconds']

    def __handle_msg(self):
        data = self.sock.recv(0xFFFF)

        if len(data) == 0:
            return False

        msgs = self.__parse_data(data)
        self.__execute_handlers(msgs)
        return True

    def __login(self):
        self.send('NICK %s' % self.nick)
        self.send('USER %s %s %s :%s' % (self.user, self.user,
                                         self.user, self.user))
    def join(self, chans):
        if isinstance(chans, list):
            self.send('JOIN %s' % (",".join(chans)))
        else:
            self.send('JOIN %s' % (chans))

    def privmsg(self, to, msg):
        self.send('PRIVMSG %s :%s' % (to, msg))

    def loop(self):
        self.__connect()
        self.__login()

        run = True
        while run:
            (reads, _, _) = select.select([self.sock], [], [], 0.5)

            for s in reads:
                run = self.__handle_msg()
            self.__execute_timers()
