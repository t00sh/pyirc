Small IRC python module

-----------------------------

Example, echo messages on channel :

```python
from irc import IRC
import logging

def handler_privmsg(irc, msg):
    if msg['args'][0] == '#mychannel']:
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

  - __author__ : Tosh

  - __license__ : GPL
