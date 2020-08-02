from bitarray import bitarray
import socket
import random
import pickle

class Emitter:

    per_bit = 20

    def __init__(self, ip: str, port: int):
        self.server_info = (ip, port)
    
    def _to_binary_str(self, st):
        return ''.join(format(ord(x), 'b') for x in st)
    
    def _add_noise(self, byte_array):
        choices = [bitarray('1'), bitarray('0')]
        noise = round(len(byte_array) / self.per_bit)
        for i in range(noise):
            pos = random.randint(0, len(byte_array))
            byte_array = byte_array[0:pos] + random.choice(choices) + byte_array[pos:]
        return byte_array
    
    def _verify_message(self, message: str):
        return bitarray( self._to_binary_str( message ))

    def _send_message(self, message, wait_response: bool = True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_info)
            sock.sendall(message)
            if wait_response:
                res = sock.recv(1024)
                return res

    def send_message(self, message):
        before_noise = self._verify_message(message)
        after_noise = self._add_noise(before_noise)
        pickle_message = pickle.dumps(after_noise)

        return self._send_message(pickle_message, False)
