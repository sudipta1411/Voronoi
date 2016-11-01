#!/usr/bin/python

from priority_queue import PrioQueue
from avl import AVLTree

S = 'site'
I = 'intersection'

class Voronoi(object) :
    '''
    @data is a list of points(sites)
    '''
    def __init__(self, data) :
        self.sites = data
        self.result = []
        # event points can be either sites or intersection points
        self.events  = PrioQueue()
        self.nr_sites = len(self.sites)
        # binary tree to store the regions and boundary
        self.bt = AVLTree()

        for x,y in self.sites :
            self.events.push((x,y,S))

    def build(self) :
        while not self.events.empty() :
            p = self.events.pop()
            if p[2] == S :
                selft.process_site(p)
            else :
                self.process_intersection(p)

    def process_site(self, point) :

