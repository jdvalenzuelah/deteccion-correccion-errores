from bitarray import bitarray
import socket
import random
import pickle

class Emitter:

    def __init__(self, ip: str, sock: int):
        self.per_bit = 20
        self.server_info = (ip, sock)
    
    def _to_binary_str(self, st):
        return ''.join(format(ord(x), 'b') for x in st)
    
    def _add_noise(self, byte_array):
        choices = [bytearray('1', encoding = "utf-8"), bytearray('0', encoding = "utf-8")]
        noise = round(len(byte_array) / self.per_bit)
        for i in range(noise):
            pos = random.randint(0, len(byte_array))
            byte_array = byte_array[0:pos] + random.choice(choices) + byte_array[pos:]
        return byte_array
    
    def _verify_message(self, message: str):
        return bytearray( self._to_binary_str( message ), encoding = "utf-8" )



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
        return self._send_message(pickle_message)


if __name__ == "__main__":
    emitter = Emitter('127.0.0.1', 65432)
    res = emitter.send_message('Hello World')
    print(res)
