class FtpCoord:

    shutdown = None
    stats = {}

    def __init__(self):
        self.shutdown = False

    def kill(self):
        print("raising shutdown")
        self.shutdown = True

    def need_to_stop(self):
        return self.shutdown

    def update_stats(self, filepath, size, status, elapsed):
        self.stats[filepath] = {'size':size, 'status' : status, 'elapsed' :elapsed}

    def show_stats(self):
        xferred = 0
        resumed = 0
        failed = 0
        already = 0
        elapsed = 0
        size = 0
        for k, v in self.stats.items():
            if v['status'] == 'xferred':
                xferred += 1
            elif v['status'] == 'resumed':
                resumed += 1
            elif v['status'] == 'failed':
                print(k)
                failed += 1
            elif v['status'] == 'already':
                already += 1
            elapsed += v['elapsed']
            size += v['size']
        print("xferred: " + str(xferred))
        print("resumed: " + str(resumed))
        print("failed: " + str(failed))
        print("already: " + str(already))
        print("elapsed: " + str(elapsed))
        print("size: " + str(size))
        if size > 0 and elapsed > 0:
            print("bandwith: " + str((size/elapsed)/1024) + " KiB/s")