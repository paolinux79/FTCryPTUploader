class crypt_file:

    opened_file = None
    cipherer = None
    cipherer_block_size = None

    def __init__(self, cipherer, cipherer_block_size):
        self.cipherer = cipherer
        self.cipherer_block_size = cipherer_block_size
        if self.cipherer is None:
            print("no cipherer")
        else:
            print("cipherer provided")


    def open(self, filename):
        self.opened_file = open(filename,'rb')
        return self.opened_file

    def read(self, size):
        if self.cipherer is not None:
            print("ciphering")
            return self.cipher(self.opened_file.read(size))
        return self.opened_file.read(size)

    def seek(self,offset):
        self.opened_file.seek(offset)

    def close(self):
        self.opened_file.close()

    def cipher(self, plaintext):
        remainder = len(plaintext) % self.cipherer_block_size
        if remainder == 0:
            return self.cipherer.encrypt(plaintext)
        else:
            encoded_remainder = "{0:c}".format(remainder)
            last_block = ('{:'+str(self.cipherer_block_size-1)+'}').format(plaintext) + encoded_remainder
            return self.cipherer(last_block)
