#!/usr/bin/env python
import socket
import string
import json
import os

from threading import Thread

from token_generator import token_gen
from info import ClientInfo


HOST = "127.0.0.1"       # Standard loopback interface address (localhost)

c_info = ClientInfo()    # Server side client class.


def serve_on_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen(50)
        if port == 8000:
            try:
                while True:
                    clientsocket, address = s.accept()
                    with clientsocket:
                        print(f"Connected by {address}")

                        recived_token = clientsocket.recv(1024).decode('utf8')

                        if len(recived_token) == 8:
                            respond_token = token_gen(size=8, chars=string.digits)

                            c_info.add_token_pair(recived_token, respond_token)

                            clientsocket.sendall(respond_token.encode('utf8'))
                        else:
                            send_data = 'ERROR: Wrong identifier format! Must be 8 charters.'
                            clientsocket.sendall(send_data.encode('utf8'))

            except KeyboardInterrupt as err:
                print(err)
                print('Stoped: get KeyboardInterrupt signal')
            finally:
                clientsocket.close()
                print('Clientsocket on server side closed.')

        if port == 8001:
            try:
                while True:
                    clientsocket, address = s.accept()
                    with clientsocket:
                        print(f"Connected by {address}")

                        recivedObj = json.loads(clientsocket.recv(1024).decode('utf8'))
                        identifier = list(recivedObj.keys())[0]
                        recived_token = recivedObj[identifier]['respond']
                        recived_message = recivedObj[identifier]['message']
                        formated_message = f'{identifier}: {recived_message}\n'

                        if c_info.check_token_pair(identifier, recived_token):
                            response = 'SUCCES: msg recived. keys accepted'
                            clientsocket.sendall(response.encode('utf8'))

                            try:
                                #  Create logs if not exist:
                                if not os.path.exists('logs'):
                                    os.mkdir('logs')
                                    print(f'---> logs just created!')

                                with open(f'logs/messages.log', "a") as file_object:
                                    # Append at the end of file:
                                    file_object.write(formated_message)
                            # If there is any permission issue:
                            except PermissionError:
                                e = 'ERROR: Permission denied.'
                                print(e)

                        else:
                            response = 'ERROR: msg recived. keys denied'
                            clientsocket.sendall(response.encode('utf8'))


            except KeyboardInterrupt as err:
                print(err)
                print('Stoped: get KeyboardInterrupt signal')
            finally:
                clientsocket.close()
                print('Clientsocket on server side closed.')

Thread(target=serve_on_port, args=[8000]).start()
Thread(target=serve_on_port, args=[8001]).start()
