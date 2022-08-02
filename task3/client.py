#!/usr/bin/env python
import socket

import lorem
import random
import json
import re

from token_generator import token_gen
from info import ClientInfo

CLIENTS_NUM = 50

HOST = "127.0.0.1"      # The server's hostname or IP address.
PORT_KEYS = 8000        # The port used by the server for tokens exchange.
PORT_MSG = 8001         # The port used by the server for messages.

c_info = ClientInfo()   # Client side client class.


client = 0
while client < CLIENTS_NUM:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        identifier_token = token_gen(8)

        s.connect((HOST, PORT_KEYS))
        s.sendall(identifier_token.encode('utf8'))

        recived_token = s.recv(1024).decode('utf8')

        if recived_token:
            c_info.add_token_pair(identifier_token, recived_token)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
                # Random message generator:
                text = re.sub('\n', '', lorem.text())
                textList = text.split(' ')

                words_random = random.choices(textList, k = 4)
                random_text = ''
                for item in words_random:
                    random_text += f'{item.strip()} '

                msgObj = c_info.save_msg(identifier_token, recived_token, random_text)
                msgObj_encoded = json.dumps(msgObj).encode('utf-8')

                s1.connect((HOST, PORT_MSG))
                s1.sendall(msgObj_encoded)

                recived_respond = s1.recv(1024).decode('utf8')
        else:
            print('ERROR: respond Token not recived')

        # print(c_info.users)
        print(f'Client token --- {identifier_token}')
        print(f'Server token --- {recived_token!r}')
        print(f'Message: {random_text}')
        print(f'{recived_respond}')


        print('')
        client += 1
