from Crypto.Cipher import AES
import os.path
CHUNK_SIZE = 8192


def decypt(filename):
    key = "this is my key12"
    cipherer = AES.new(key, AES.MODE_ECB)
    filesize = os.path.getsize(filename)
    opened_file = open(filename,'rb')
    decoded_data_file = []
    while True:
        current_position = opened_file.tell()
        data = opened_file.read(CHUNK_SIZE)
        decoded_data = cipherer.decrypt(data)
        if current_position + CHUNK_SIZE >= filesize:
            decoded_data_file.append(unpad(decoded_data))
            break
        else:
            decoded_data_file.append(decoded_data)
    return b"".join(decoded_data_file)


def unpad(block):
    pad = block[-1]
    return block[:-pad]


def decypt_to_file(infile, outfile):
    with open(outfile,'wb') as out_file:
        output = decypt(infile)
        out_file.write(output)

decypt_to_file("/home/paolinux/a19.xxx","/home/paolinux/a19.dec")
