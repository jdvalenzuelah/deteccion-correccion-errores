#!/usr/bin/python

import sys
import threading
from receiver import Receiver
from emitter import Emitter

def start_receiver(ip, port):
    receiver = Receiver(ip, int(port))
    req = receiver.listen()
    print(f'Received message: {req}')

def send_message(ip, port, message):
    emitter = Emitter(ip, int(port))
    emitter.send_message(message)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Not enough args passed!')
        sys.exit(1)
    
    if not sys.argv[2].isdigit():
        print("Invalid port passed!")
        sys.exit(1)
    
    _, ip, port, message = sys.argv
    print('Starting receiver thread')
    r = threading.Thread(target=start_receiver, args=(ip, port))
    r.start()

    print('Sending message')
    send_message(ip, port, message)

    
