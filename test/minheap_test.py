import unittest
import random
from typing import (
    List,
)
from pygraph.minheap import (
    MinHeap,
)


N_RANDNUM = 0xFFFF

def extract_mq(heap: MinHeap) -> List[object]:
    extracted = list()
    while not heap.is_empty():
        extracted.append(heap.extract_min())
    return extracted

def int_less(a: int, b: int) -> bool:
    #print(f"Compare {a} and {b}")
    return a < b

def check_constraint(arr: List) -> bool:
    bound = (len(arr) >> 1) - 1
    for i in range(bound):
        i += 1
        i_l, i_r = i << 1, (i << 1) + 1
        i -= 1
        if i_l <= len(arr):
            if arr[i] > arr[i_l - 1]:
                print(f"[{i}]={arr[i]} > [{i_l}]={arr[i_l-1]} violated.")
                return False
        if i_r <= len(arr):
            if arr[i] > arr[i_r - 1]:
                print(f"[{i}]={arr[i]} > [{i_l}]={arr[i_r-1]} violated.")
                return False
    return True


class TestMinHeap(unittest.TestCase):
    def test_basic(self):
        ascend = [0, 1, 2, 3, 4, 5, 6, 7]
        descnd = [7, 6, 5, 4, 3, 2, 1, 0]
        ordered = ascend.copy()
        mq_a = MinHeap(int_less, arr=ascend)
        mq_b = MinHeap(int_less, arr=descnd)
        # test ascending and descending case.
        self.assertTrue(
            check_constraint(ascend)
        )
        extracted = extract_mq(mq_a)
        self.assertEqual(ordered, extracted)
        
        self.assertTrue(
            check_constraint(descnd)
        )
        extracted = extract_mq(mq_b)
        self.assertEqual(ordered, extracted)
        
        return
    
    def test_complex(self):
        # test randomly generated case.
        rng_arr = [random.randint(0, 0xFFFFFFFF) for _ in range(N_RANDNUM)]
        sorted_arr = sorted(rng_arr)
        mq = MinHeap(int_less, arr=rng_arr)

        extracted = extract_mq(mq)
        self.assertEqual(sorted_arr, extracted)
        
        return

