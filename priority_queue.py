#!/usr/bin/python

import heapq

class PrioQueue(object) :
    '''A custom min heap where p<q means
    y(p)<y(q) or y(p)=y(q) and x(p) < x(q).
    This is the lexicographic ordering.
    '''
    class Wrapper(object) :
        def __init__(self, val) :
            self.val = val

        def __cmp__(self, other) :
            if self.val[1] < other[1] or self.val[1] == other[1] and self.val[0] < other[0] :
                    return -1
            if self.val[0] == other[0] and self.val[1] == other[0] :
                return 0
            return 1

        def __setitem__(self,index,value) :
            self.val[index] = value

        def __getitem__(self,index) :
            return self.val[index]

        def __str__(self) :
            return str(self.val)

    def __init__(self,data = None) :
        self.hq = []
        self.data = data
        if data :
            self.__make_queue()

    def __make_queue(self) :
        for val in self.data :
            heapq.heappush(self.hq,PrioQueue.Wrapper(val))

    def push(self,val) :
        heapq.heappush(self.hq,PrioQueue.Wrapper(val))

    def pop(self) :
        try :
            return heapq.heappop(self.hq)
        except IndexError :
            print '[ERROR] Index out of range'
