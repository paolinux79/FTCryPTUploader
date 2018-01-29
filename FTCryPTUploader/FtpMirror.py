import os
import time
from concurrent.futures import ThreadPoolExecutor

from FTCryPTUploader.FtpUploader import FtpConfig
from FTCryPTUploader.FtpUploader import FtpUploader
from FTCryPTUploader.FtpCoord import FtpCoord
import threading



class FtpMirror:
    """a class written to perform a full mirror copy from local to ftp server"""
    start_local_path = None
    start_remote_path = None
    depth = None
    ftp_config = None
    executor = None
    futures_pit = None
    ftpCoord = None
    lock = None

    def __init__(self, start_local_path, start_remote_path, depth, ftp_config, max_workers, ftpCoord):
        self.start_local_path = start_local_path
        self.start_remote_path = start_remote_path
        self.depth = depth
        self.ftp_config = ftp_config
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.ftpCoord = ftpCoord
        self.lock = threading.Lock()

    def process_current_directory(self, root, files):
        start = time.time()
        if self.ftpCoord.need_to_stop():
            print("need to stop")
            stop = time.time()
            return stop - start
        index = len(self.start_local_path)
        current_root = root[index + 1:]
        trailing_dirs = None
        if len(current_root) > 1:
            trailing_dirs = current_root.split(os.sep)
        ftp = FtpUploader(ftp_config=self.ftp_config)
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
            print("Filepath is " + filepath + " and size is " + str(os.path.getsize(filepath)))
            if self.ftpCoord.need_to_stop():
                print("need to stop")
                stop = time.time()
                return stop - start
            try:
                filestart = time.time()
                status = ftp.xfer(remote_file_name=infile, local_file_name=filepath)
            except:
                import traceback
                traceback.print_exc()
                status = 'failed'
            finally:
                filestop = time.time()
                file_elapsed = filestop - filestart
            xferred_size = 0
            if status == 'resumed' or status == 'xferred':
                xferred_size = os.path.getsize(filepath)
            self.ftpCoord.update_stats(filepath=filepath, status=status, size=xferred_size, elapsed=file_elapsed)

        ftp.shutdown()
        stop = time.time()
        return stop - start

    def crawl(self):
        self.futures_pit = {}
        for root, dirs, files in os.walk(self.start_local_path):
            # self.process_current_directory(root=root, files=files)
            future = self.executor.submit(self.process_current_directory, root, files)
            with self.lock:
                self.futures_pit[future] = None
        self.status_updater()

    def status_updater(self):
        running = len(self.futures_pit)
        while True:
            print("====> there are " + str(running) + " enqueued threads")
            self.ftpCoord.show_stats()
            if running == 0:
                print("====> there are NO enqueued threads")
                break
            with self.lock:
                for k, v in self.futures_pit.items():
                    # print("anayzing " + str(k))
                    if k.done():
                        elapsed = self.futures_pit[k]
                        if elapsed is None:
                            self.futures_pit[k] = k.result()
                            print("====> thread finished in  " + str(self.futures_pit[k]) + " ms")
                            running -= 1
            time.sleep(1)



def test():
    import json

    with open("myprops.json", "r") as data_file:
        settings = json.loads(data_file.read())

    config = FtpConfig(host=settings["host"], username=settings["user"], password=settings["passwd"],
                       key=settings["aes_key"], initial_dir=settings["initial_dir"])
    ftpCoord = FtpCoord()
    ftpMirror = FtpMirror("/home/paolinux/EAP-6.4.8", "upload/EAP-6.4.8", None, config, 10, ftpCoord)
    start = time.time()
    ftpMirror.crawl()
    print(str(time.time() - start))

if __name__ == '__main__':
    test()

