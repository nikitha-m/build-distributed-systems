#!/usr/bin/env python3
import sys
import json

class Node:
    def __init__(self):
        self.node_id = None
        self.node_ids = []
        self.next_msg_id = 0
    
    def send(self, dest, body):
        body["body"]["msg_id"] = self.next_msg_id
        self.next_msg_id+=1 
        print(json.dumps(body), flush=True)
    
    def reply(self, request, body):
        ## This makes it very specific to init
        ## Thats bad coding style
        body["type"] = "init_ok"
        body["in_reply_to"] = request["body"]["msg_id"]
        ############################################
        response = {}
        response["src"] = request["dest"]
        response["dest"] = request["src"]
        response["body"] = body
        self.send(request["dest"], response)

def main():
    node = Node()
    
    for line in sys.stdin:
        message = json.loads(line)
        body = message["body"]
        msg_type = body["type"]
        
        if msg_type == "init":
            node.reply(message, {})

if __name__ == "__main__":
    main()
