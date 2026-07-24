#!/usr/bin/env python3
import sys
import json
import threading
from queue import Queue

class Node:
    def __init__(self):
        self.node_id = None
        self.node_ids = []
        self.next_msg_id = 0
        self.lock = threading.Lock()
    
    def send(self, dest, body):
        with self.lock:
            body["msg_id"] = self.next_msg_id
            self.next_msg_id += 1
            message = {"src": self.node_id, "dest": dest, "body": body}
            print(json.dumps(message), flush=True)
    
    def reply(self, request, body):
        body["in_reply_to"] = request["body"]["msg_id"]
        self.send(request["src"], body)
    
    def handle_message(self, message):
        msg_type = message["body"]["type"]
        if msg_type == "init": 
            with self.lock:
                self.node_id = message["body"]["node_id"]
            self.reply(message, {"type": "init_ok"})
        elif msg_type == "echo":
            self.reply(message, {"type": "echo_ok", "echo": message["body"]["echo"]})

def main():
    node = Node()
     
    for line in sys.stdin:
        message = json.loads(line)
        
        result = {}
        t = threading.Thread(target=node.handle_message, args=(message,))
        t.start()

if __name__ == "__main__":
    main()
