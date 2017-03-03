import ftp_uploader
import json

settings = json.loads("props.json")
ftp = ftp_uploader.ftp_uploader(host=settings["host"], username=settings["user"], password=settings["passwd"], key="this is my key12")
ftp.connect()
ftp.set_remote_initial_dir(settings["initial_dir"])
ftp.set_remote_initial_dir("upload")
ftp.xfer(remote_file_name="a8.xxx", local_file_name="/home/paolinux/b.txt")
ftp.shutdown()
