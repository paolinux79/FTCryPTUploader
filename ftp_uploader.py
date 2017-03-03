import ftplib
from Crypto.Cipher import AES
import os.path
import crypt_file

FILE_BLOCK_SIZE = 8192

class ftp_uploader:
    """a simple ftp uploader"""
    host = None
    username = None
    password = None
    initialized_ftp = None
    current_file_dict = {}
    cipherer = None

    def __init__(self, host, username, password, key):
        print("initilializing")
        self.host = host
        self.password = password
        self.username = username
        if key is not None:
            # iv = Random.new().read(CAST.block_size)
            print("preparing cipherer")
            self.cipherer = AES.new(key, AES.MODE_ECB)

    def connect(self):
        ftp = ftplib.FTP_TLS(self.host)
        ftp.login(user=self.username, passwd=self.password)
        self.initialized_ftp = ftp

    def set_remote_initial_dir(self, dirname):
        self.initialized_ftp.cwd(dirname=dirname)
        self.get_file_list_size()

    def get_file_list_size(self):
        gen_list = self.initialized_ftp.mlsd(facts=["size"])
        self.current_file_dict.clear()
        for item in gen_list:
            current_file_name = item[0]
            try:
                current_file_size = item[1]['size']
            except KeyError:
                current_file_size = None
            self.current_file_dict[current_file_name] = current_file_size
        print(self.current_file_dict)

    def get_file_size(self, filename):
        print("filename " + filename)
        try:
            size = self.current_file_dict[filename]
        except KeyError:
            size = None
        return size

    def xfer(self, remote_file_name, local_file_name):
        remote_file_size = self.get_file_size(remote_file_name)
        local_file_size = os.path.getsize(local_file_name)
        print("remote file size " + str(remote_file_size))
        if remote_file_size is None:
            print("this is a new file")
            cf = crypt_file.crypt_file(cipherer=self.cipherer, cipherer_block_size=AES.block_size)
            cf.open(local_file_name)
            self.initialized_ftp.storbinary(cmd="STOR " + remote_file_name, fp=cf, blocksize=FILE_BLOCK_SIZE)
            cf.close()
        elif int(remote_file_size) < local_file_size:
            print("this is a file to be resumed")
            remote_file_size = int(remote_file_size)
            transferred_blocks = int(remote_file_size / FILE_BLOCK_SIZE)
            transferred_size = transferred_blocks * FILE_BLOCK_SIZE
            print("transferred_blocks " + str(transferred_blocks))
            print("transferred_size " + str(transferred_size))
            cf = crypt_file.crypt_file(cipherer=self.cipherer, cipherer_block_size=AES.block_size)
            cf.open(local_file_name)
            cf.seek(transferred_size)
            print("shifted")
            self.initialized_ftp.storbinary(cmd="STOR " + remote_file_name, fp=cf, rest=transferred_size, blocksize=FILE_BLOCK_SIZE)
            cf.close()
        else:
            print("file already completed")

    def shutdown(self):
        self.initialized_ftp.quit()


