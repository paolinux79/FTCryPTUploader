import os.path
import time
class crypt_file:

    opened_file = None
    cipherer = None
    cipherer_block_size = None
    file_size = None

    def __init__(self, cipherer, cipherer_block_size):
        self.cipherer = cipherer
        self.cipherer_block_size = cipherer_block_size
        # if self.cipherer is None:
        #     print("no cipherer")
        # else:
        #     print("cipherer provided")


    def open(self, filename):
        self.opened_file = open(filename, 'rb')
        self.file_size = os.path.getsize(filename=filename)
        return self.opened_file

    def read(self, size):
        time.sleep(1)
        if self.cipherer is not None:
            # print("ciphering")
            current_position = self.opened_file.tell()
            # print("current_position " + str(current_position))
            # print("requesting " + str(size))
            padme = False
            if current_position + size >= self.file_size:
                # print("PADDING REQUESTED")
                padme = True
            plaintext = self.opened_file.read(size)
            # print("got " + str(len(plaintext)))
            if not plaintext:
                return plaintext
            return self.cipher(plaintext=plaintext, padme=padme)
        return self.opened_file.read(size)

    def seek(self, offset):
        self.opened_file.seek(offset)

    def close(self):
        self.opened_file.close()

    def cipher(self, plaintext, padme):
        if padme:
            return self.cipherer.encrypt(self.pad(block=plaintext))
        else:
            return self.cipherer.encrypt(plaintext)


    # PKCS7
    def pad(self, block):
        # print("incoming block size " + str(len(block)))
        block_size = len(block)
        amount_to_pad = self.cipherer_block_size - (block_size % self.cipherer_block_size)
        # print("amount to pad " + str(amount_to_pad))
        if amount_to_pad == 0:
            amount_to_pad = self.cipherer_block_size
        pad = bytes([amount_to_pad])
        pad_block = pad * amount_to_pad
        padded_block = block + pad_block
        # print("padded block size " + str(len(padded_block)))
        return padded_block

