import fcntl,time 
class Locker:
    def __init__(self,fp,log=""):
        self.fp = fp
        self.log = log
    def __enter__ (self):
        # print("Accquiring Lock",self.log)
        fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX)

    def __exit__ (self, _type, value, tb):
        fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
        # print("Releasing Lock",self.log)
        self.fp.close()

# fp = open('lockfile.lck','r')
# print("waiting for lock")
# with Locker(fp):
#     print("obtained lock")
#     time.sleep(5.0)