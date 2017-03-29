import json
import time
from FTCryPTUploader import FtpUploader
from FTCryPTUploader import FtpMirror
from FTCryPTUploader.FtpCoord import FtpCoord
import signal
import sys


ftpCoord = None

def single():
    with open("props.json") as data_file:
        settings = json.load(data_file)

    config = FtpUploader.FtpConfig(host=settings["host"], username=settings["user"], password=settings["passwd"],
                                   key=settings["aes_key"], initial_dir=settings["initial_dir"])
    ftp = FtpUploader.FtpUploader(ftp_config=config)
    ftp.connect()
    ftp.set_remote_initial_dir(config.initial_dir)
    ftp.set_remote_initial_dir("upload")

    status = ftp.xfer(remote_file_name="1.xxx", local_file_name="/home/paolinux/SoapUI-5.2.1/LICENSE.txt")
    ftp.shutdown()


def mirror(start_local_path,start_remote_path):
    signal.signal(signal.SIGINT, signal_handler)

    global ftpCoord
    ftpCoord = FtpCoord()

    with open("myprops.json", "r") as data_file:
        settings = json.load(data_file)

    config = FtpUploader.FtpConfig(host=settings["host"], username=settings["user"], password=settings["passwd"],
                                   key=settings["aes_key"], initial_dir=settings["initial_dir"])

    ftpMirror = FtpMirror.FtpMirror(start_local_path=start_local_path, start_remote_path=start_remote_path,
                                    depth=None, ftp_config=config, max_workers=10, ftpCoord=ftpCoord)
    start = time.time()
    ftpMirror.crawl()
    print("Total elapsed crawling time is: " + str(time.time() - start))


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    global ftpCoord
    ftpCoord.kill()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("2 parameters are needed: start_local_path and start_remote_path")
        print("e.g.,")
        print("/home/myhome/Backup upload/Backup")
        exit()
    # mirror(start_local_path="/home/paolinux/Dropbox", start_remote_path="upload/Dropbox")
    mirror(start_local_path=sys.argv[1], start_remote_path=sys.argv[2])