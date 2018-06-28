Small IRC python module

-----------------------------

Example, echo messages on channel :

```python
from irc import IRC
import logging

def handler_privmsg(irc, msg):
    if msg['args'][0] == '#mychannel':
        irc.privmsg('#mychannel', msg['content'])

if __name__ == '__main__':
    irc = IRC(user='t0x0shBot',
              nick='t0x0shBot',
              host='irc.root-me.org',
              port=6667,
              channels=['#mychannel'],
              log_level=logging.INFO)

    irc.set_handler('PRIVMSG', handler_privmsg)
    irc.loop()
```

-----------------------------

# API

`class IRC`

- __`__init__(self, user, nick, host, port, channels, log_level)`__ : Constructor

    - __user__ : IRC user (type str)

    - __nick__ : IRC nick (type str)

    - __host__ : server host (type str)

    - __port__ : server port (type int)

    - __channels__ : list of channels to join (type str list)

    - __log_level__ : level of logging (constants logging.DEBUG, logging.WARNING, etc...)

    - __`send(self, msg)`__ : Send an IRC msg

         - __msg__ : message to send without "\\r\\n" (type str)

    - __`privmsg(self, to, msg)`__ : Send a PRIVMSG to channel or nick

         - __to__ : channel or nick to send (type str)

         - __msg__ : message to send (type str)

    - __`set_handler(self, cmd, handler)`__ : Add event handler when handling IRC command

         - __cmd__ : the command triggering the handler (type str)

         - __handler__ : the function handler (type function(IRC, dict))

         The second parameter is the parsed IRC message, viewed as a dictionnary. It has the following fields :

         - __full__ : the raw message (type str)

         - __host__ : the host from where the message come from (type str)

         - __cmd__ : the IRC command (PRIVMSG, MODE, JOIN, etc) (type str)

         - __args__ : arguments of the command (type str)

         - __content__ : content of the message (type str)

    - __`set_timer(self, handler, seconds)`__ : Add function to be executed every X seconds

         - __handler__ : the function to be called (type function(IRC))

         - __seconds__ : number of seconds between each call (type int)


    - __`loop(self)`__ : Infinite loop, handling commands and timers.

-----------------------------

  - __author__ : Tosh

  - __license__ : GPL
