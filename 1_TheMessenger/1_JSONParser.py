#!/usr/bin/env python3
import sys
import json

def main():
    # TODO: Read JSON messages from stdin
    # Each line is a complete JSON message
    # Parse and print: PARSED: src|dest|body_type
    # Log details to stderr for debugging

    for line in sys.stdin:
        try:
            data = json.loads(line)
            src = data.get("src","unknown")
            dest = data.get("dest","unknown")
            body_type = data.get("body",{}).get("type", "unknown")
            print(f"PARSED: {src}|{dest}|{body_type}")
        except Exception as e:
            print(e, file= sys.stderr)
if __name__ == "__main__":
    main()