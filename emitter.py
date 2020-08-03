from bitarray import bitarray
from fletcher import FletcherChecksum
from hamming import Hamming
import socket
import random
import pickle

class Emitter:

    per_bit = 100
    hamming = Hamming()

    def __init__(self, ip: str, port: int):
        self.server_info = (ip, port)
    
    def _to_binary_str(self, st):
        return ''.join(format(ord(x), 'b') for x in st)
    
    def _add_noise(self, byte_array):
        noise = round(len(byte_array) / self.per_bit)
        for i in range(noise if noise else 1):
            pos = random.randint(0, len(byte_array) - 1)
            byte_array[pos] = not byte_array[pos] 
        return byte_array
    
    def _verify_message(self, message: str):
        bin_message = self._to_binary_str( message )
        r = self.hamming.calc_redundant_bits(len(bin_message))
        bin_message = self.hamming.placed_redundancy_bits(bin_message, r)
        bin_message = self.hamming.calc_parity_bits(bin_message, r)
        message = bitarray( bin_message )
        return message

    def _send_message(self, message, wait_response: bool = True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_info)
            sock.sendall(message)
            if wait_response:
                res = sock.recv(1024)
                return res

    def send_message(self, message):
        before_noise = self._verify_message(message)
        print(f'before noise {before_noise}')
        after_noise = self._add_noise(before_noise)
        print(f'after noise {after_noise}')
        pickle_message = pickle.dumps(after_noise)

        return self._send_message(pickle_message, False)
