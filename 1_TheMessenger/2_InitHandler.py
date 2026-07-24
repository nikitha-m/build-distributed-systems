#!/usr/bin/env python3
import sys
import json

class Node:
    def __init__(self):
        self.node_id = None
        self.node_ids = []
        self.next_msg_id = 0
    
    def send(self, dest, body):
        body["msg_id"] = self.next_msg_id
        self.next_msg_id += 1
        response = {"src": dest, "dest": self.node_id, "body": body}
        print(json.dumps(response), flush=True)

    def reply(self, request, body):
        body["in_reply_to"] = request["body"]["msg_id"]
        self.send(request["dest"], body)

def main():
    node = Node()
    
    for line in sys.stdin:
        message = json.loads(line)
        body = message["body"]
        msg_type = body["type"]
        
        if msg_type == "init":
            node.node_id = message["src"]
            node.reply(message, {"type": "init_ok", "in_reply_to": body["msg_id"]})

if __name__ == "__main__":
    main()
