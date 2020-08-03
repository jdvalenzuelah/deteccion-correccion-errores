from bitarray import bitarray
from fletcher import FletcherChecksum
import socket
import random
import pickle

class Receiver:

    checksum = FletcherChecksum()

    def __init__(self, ip: str, port: int):
        self.server_info = (ip, port)
    
    # Codificacion
    def _load_req(self, req):
        return pickle.loads(req)
    
    def _to_binary_str(self, bit_array):
        return ''.join([ '1' if x else '0' for x in bit_array ])

    def _verify_message(self, bit_array):
        # last 16 bits checksum
        msg_checksum = self.checksum.generate_checksum(bit_array[0:-16])
        incoming_checksum = int(self._to_binary_str(bit_array[-16:]), 2)
        if msg_checksum == incoming_checksum:
            return self._to_binary_str(bit_array)
        else:
            pass # need to correct errors
    
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
                    req_str = self._verify_message(self._load_req(req))
                    if send_response:
                        conn.sendall(req)
        return req_str
