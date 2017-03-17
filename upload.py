import json

from FTCryPTUploader import FtpUploader


def main():
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


if __name__ == '__main__':
    main()


