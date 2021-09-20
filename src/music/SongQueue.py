import asyncio
import itertools
from random import shuffle


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        
        return self._queue[item]
    
    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def pop(self, index: int = 0):
        removed = self._queue[index]
        del self._queue[index]
        return removed
    
    def shuffle(self):
        shuffle(self._queue)