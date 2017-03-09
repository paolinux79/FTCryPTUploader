import ftp_uploader

import json

with open("props.json") as data_file:
    settings = json.load(data_file)

config = ftp_uploader.ftp_config(host=settings["host"], username=settings["user"], password=settings["passwd"], key=settings["aes_key"], initial_dir=settings["initial_dir"])
ftp = ftp_uploader.ftp_uploader(ftp_config=config)
ftp.connect()
ftp.set_remote_initial_dir(config.initial_dir)
ftp.set_remote_initial_dir("upload")

ftp.xfer(remote_file_name="1.xxx", local_file_name="/home/paolinux/SoapUI-5.2.1/LICENSE.txt")
ftp.shutdown()
