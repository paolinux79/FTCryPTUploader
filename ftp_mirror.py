import os
from ftp_uploader import ftp_uploader
from ftp_uploader import ftp_config


class ftp_mirror:

    start_local_path = None
    start_remote_path = None
    depth = None
    ftp_config = None

    def __init__(self, start_local_path, start_remote_path, depth, ftp_config):
        self.start_local_path = start_local_path
        self.start_remote_path = start_remote_path
        self.depth = depth
        self.ftp_config = ftp_config

    def crawl(self):
        for root, dirs, files in os.walk(self.start_local_path):
            index = len(self.start_local_path)
            current_root = root[index+1:]
            trailing_dirs = None
            if len(current_root) > 1:
                trailing_dirs = current_root.split(os.sep)
            ftp = ftp_uploader(ftp_config=self.ftp_config)
            ftp.connect()
            ftp.set_remote_initial_dir(self.ftp_config.initial_dir)
            init_dirs = self.start_remote_path.split(os.sep)
            for init_dir in init_dirs:
                ftp.change_or_create_to_dir(init_dir)
            if trailing_dirs is not None:
                for current_dir in trailing_dirs:
                    print("current dir " + current_dir)
                    ftp.change_or_create_to_dir(current_dir)
            for infile in files:
                filepath = os.path.join(root, infile)
                print("filename is " + infile + " with filepath " + filepath)
                ftp.xfer(infile,local_file_name=filepath)
            ftp.shutdown()


import json

with open("props.json") as data_file:
    settings = json.load(data_file)

config = ftp_config(host=settings["host"], username=settings["user"], password=settings["passwd"], key=settings["aes_key"], initial_dir=settings["initial_dir"])
x = ftp_mirror("/home/paolinux/SoapUI-5.2.1","upload/SoapUI-5.2.1",None,config)
x.crawl()