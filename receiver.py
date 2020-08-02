from bitarray import bitarray
import socket
import random
import pickle

class Receiver:

    def __init__(self, ip: str, port: int):
        self.server_info = (ip, port)
    
    def _load_req(self, req):
        return pickle.loads(req)
    
    def _bit_array_string(self, bit_array):
        return ''.join([ '1' if x else '0' for x in bit_array ])
    
    def listen(self, send_response: bool = False):
        req_str = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.server_info)
            sock.listen()
            conn, addr = sock.accept()
            with conn:
                while True:
                    req = conn.recv(2048)
                    if not req:
                        break
                    req_str = self._bit_array_string(self._load_req(req))
                    if send_response:
                        conn.sendall(req)
        return req_str
