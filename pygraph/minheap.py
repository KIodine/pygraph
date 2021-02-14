from typing import (
    Callable,
    List,
)

class MinHeap():
    INIT_SIZE = 32
    def __init__(
            self, less_than: Callable[[object, object], bool], *,
            arr: List[object]=None
        ):
        self.less_than = less_than
        self.arr: List = None
        if arr is None:
            self.arr: List[object] = [None for _ in range(self.INIT_SIZE)]
            self.count = 0
        else:
            self.arr = arr
            self.count = len(self.arr)
            # Then do heapify
        self.cap = len(self.arr)
        return
    # TODO: heapify, sift_up, sift_down, extract_min, insert
    def is_empty(self) -> bool:
        return self.count == 0
    
    def sift_up(self, idx: int):
        arr = self.arr
        while idx > 0:
            parent = (idx + 1) >> 1
            if self.less_than(arr[idx], arr[parent - 1]):
                parent -= 1
                tmp         = arr[idx]
                arr[idx]    = arr[parent]
                arr[parent] = tmp
                parent += 1
            idx = parent - 1
        return
    
    def sift_down(self, idx: int):
        bound = self.count #len(self.arr)
        max_idx = (bound >> 1) - 1
        arr = self.arr
        while idx <= max_idx:
            idx += 1
            i_l, i_r = idx << 1, (idx << 1) + 1
            idx -= 1
            swp = idx
            if i_l <= bound and self.less_than(arr[i_l - 1], arr[idx]):
                swp = i_l
            if i_r <= bound and self.less_than(arr[i_r - 1], arr[idx]) \
                and self.less_than(arr[i_r], arr[i_l]):
                swp = i_r
            if swp == idx:
                break
            swp -= 1
            tmp      = arr[idx]
            arr[idx] = arr[swp]
            arr[swp] = tmp
            idx = swp
        return
    
    def min_heapify(self):
        #arr = self.arr
        max_idx = (self.count >> 1) - 1 #(len(arr) >> 1) - 1
        for i in range(max_idx, -1, -1):
            self.sift_down(i)
        return
    
    def extract_min(self) -> object:
        if self.count <= 0:
            return None
        arr = self.arr
        res = arr[0]
        arr[0] = arr[self.count - 1]
        self.count -= 1
        #print(self.count, self.arr)
        self.sift_down(0)
        return res
    
    def insert(self, obj: object):
        idx = self.count
        self.count += 1
        if self.count > self.cap:
            self.arr.extend((None for i in range(len(self.arr))))
            self.cap = len(self.arr)
        self.arr[idx] = obj
        self.sift_up(idx)
        return
    pass
