from bitarray import bitarray
from fletcher import FletcherChecksum
from hamming import Hamming
import socket
import random
import pickle

class Receiver:

    hamming = Hamming()

    def __init__(self, ip: str, port: int):
        self.server_info = (ip, port)
    
    # Codificacion
    def _load_req(self, req):
        return pickle.loads(req)
    
    def _to_binary_str(self, bit_array):
        return ''.join([ '1' if x else '0' for x in bit_array ])

    def _verify_message(self, bit_array):
        # last 16 bits checksum
        bin_message = self._to_binary_str(bit_array)
        r = self.hamming.calc_redundant_bits(len(bin_message))
        error = self.hamming.detect(bin_message, r)
        bin_message = self.hamming.correct(bin_message, error)
        return bin_message
        
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
