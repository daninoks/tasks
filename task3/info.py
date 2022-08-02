#!/usr/bin/env python

class ClientInfo:
    def __init__(self):
        self.users = []
        self.messages = []

    def add_token_pair(self, identifier, respond):
        pair = {identifier: respond}
        self.users.append(pair)

    def check_token_pair(self, identifier, respond):
        authorised = False
        for pair in self.users:
            if identifier in pair:
                if respond == pair[identifier]:
                    authorised = True
        return authorised

    def save_msg(self, identifier, respond, message):
        msg = {identifier: {
                'respond': respond,
                'message': message
            }
        }
        self.messages.append(msg)
        return msg
