import numpy as np

# "R" - means random values in the table
# "S" - sorted values
# "A" - sorted values in reverse order 
# "T" - table of three sorted sequences(sorted by fragments)

class MonitoredTable:

    def __init__(self, start=0, to=1000, elem=100, mode="R"):
        np.random.seed(0)
        if mode=="R":
            self.table = np.linspace(start, to, elem, dtype=np.int64)
            np.random.shuffle(self.table)
        elif mode=="S":
            self.table = np.linspace(start, to, elem, dtype=np.int64)
        elif mode=="A":
            self.table = np.linspace(start, to, elem, dtype=np.int64)
        elif mode=="T":
            __table = np.linspace(start, (to-start)//3, elem//3, dtype=np.int64)
            self.table = np.concatenate((__table,__table,__table))
        self.reset()


    def reset(self):
        self.indexes = []
        self.values = []
        self.access_mode = []
        self.full_copy = []

    def tracking(self, key, access_mode):
        self.indexes.append(key)
        self.values.append(self.table[key])
        self.access_mode.append(access_mode)
        self.full_copy.append(np.copy(self.table))

    def activity(self, idx=None):
        if isinstance(idx, type(None)):
            return [(i, op) for (i, op) in zip(self.indexes, self.access_mode)]
        else:
            return (self.indexes[idx], self.access_mode[idx])

    def __getitem__(self, key):
        self.tracking(key, "get")
        return self.table.__getitem__(key)

    def __setitem__(self, key, value):
        self.table.__setitem__(key, value)
        self.tracking(key, "set")

    def __len__(self):
        return self.table.__len__()


