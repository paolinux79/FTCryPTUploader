import json
import time
from FTCryPTUploader import FtpUploader
from FTCryPTUploader import FtpMirror


def single():
    with open("props.json") as data_file:
        settings = json.load(data_file)

    config = FtpUploader.FtpConfig(host=settings["host"], username=settings["user"], password=settings["passwd"],
                                   key=settings["aes_key"], initial_dir=settings["initial_dir"])
    ftp = FtpUploader.FtpUploader(ftp_config=config)
    ftp.connect()
    ftp.set_remote_initial_dir(config.initial_dir)
    ftp.set_remote_initial_dir("upload")

    ftp.xfer(remote_file_name="1.xxx", local_file_name="/home/paolinux/SoapUI-5.2.1/LICENSE.txt")
    ftp.shutdown()


def mirror():
    import json

    with open("props.json", "r") as data_file:
        settings = json.load(data_file)

    config = FtpUploader.FtpConfig(host=settings["host"], username=settings["user"], password=settings["passwd"],
                                   key=settings["aes_key"], initial_dir=settings["initial_dir"])
    ftpMirror = FtpMirror.FtpMirror(start_local_path="/home/paolinux/Dropbox", start_remote_path="upload/Dropbox",
                                    depth=None, ftp_config=config, max_workers=10)
    start = time.time()
    ftpMirror.crawl()
    print(str(time.time() - start))


if __name__ == '__main__':
    mirror()
