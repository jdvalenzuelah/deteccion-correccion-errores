from bitarray import bitarray

class FletcherChecksum:
    MOD = 255
    SHIFT = 8

    def generate_checksum(self, buffer: bytes):
        a, b = 0, 0
        for b in buffer:
            a = (a + b) % self.MOD
            b = (b + a) % self.MOD
        return (b << self.SHIFT) | a