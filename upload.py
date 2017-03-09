import ftp_uploader

import json

with open("props.json") as data_file:
    settings = json.load(data_file)

config = ftp_uploader.ftp_config(host=settings["host"], username=settings["user"], password=settings["passwd"], key=settings["aes_key"], initial_dir=settings["initial_dir"])
ftp = ftp_uploader.ftp_uploader(ftp_config=config)
ftp.connect()
ftp.set_remote_initial_dir(config.initial_dir)
ftp.set_remote_initial_dir("upload/lib")
ftp.change_or_create_to_dir("paoo")
ftp.xfer(remote_file_name="XXXXXXXXXXXXXX.xxx", local_file_name="/home/paolinux/b.txt")
ftp.shutdown()
