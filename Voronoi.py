#!/usr/bin/python

import math
from DataTypes import *

class EndPoint(object) :
    def __init__(self, pt, line, left_sep=None, \
            right_sep=None, above=None, below=None) :
        self.pt = Site(pt=pt)
        self.line = Site(seg=line)
        self.left_sep = left_sep
        self.right_sep = right_sep
        self.above = above
        self.below = below

def avgx(ep1, ep2) :
    return (ep1.pt.pt.px + ep2.pt.pt.px) / 2.0

class Voronoi(object) :
    # lines is a list of line segments,
    # defined by start and end points

    # LINE = 0; LEFT_SEP=1; RIGHT_SEP=2; ABOVE=3; BELOW=4
    DELTA = 10.0

    def __init__(self, lines) :
        self.lines = lines
        self.nr_pt = 2 * len(self.lines) # number of point sites

        self.ep = [] # endpoints
        for line in self.lines :
            self.ep.append(EndPoint(pt=line.start, line=line))
            self.ep.append(EndPoint(pt=line.end, line=line))
        self.ep.sort(key = lambda x : x.pt.pt.px) # presort

        self.sep = [] # list of (nr_pt+1) seperators
        self.sep.append(VertLine(pt = Point(px = self.ep[0].pt.pt.px - Voronoi.DELTA)))
        for i in range(1, self.nr_pt) :
            self.ep[i-1].left_sep = self.sep[i-1]
            self.sep.append(VertLine(pt = avgx(self.ep[i-1], self.ep[i])))
            self.ep[i-1].right_sep = self.sep[i]
        self.ep[self.nr_pt-1].left_sep = self.sep[self.nr_pt-1]
        self.sep.append(VertLine(pt = Point(px = self.ep[self.nr_pt-1].pt.pt.px + Voronoi.DELTA)))
        self.ep[self.nr_pt-1].right_sep = self.sep[-1]

        self._vertical_ray_shoot() # to populate the above and below field

        self.output = [] # list of Vorornoi Edges

    def build(self) :
        print '[INFO] Building Voronoi Diagram...'
        m = self.nr_pt
        self._build(m, 0, self.nr_pt) # slab is [sep[0], sep[nr_pt]]

    # returns tuple tup where tup[0] is a list of quads
    # in the current slab, where each slab is marked
    # active/inactive along with their windows, tup[1] is
    # a list of Voronoi edges for these quads and tup[2]
    # is the Convex Hull of the sites in the current slab.
    # When the recursive call end in method @build, we have
    # the entire diagram in @output.
    def _build(self, m, l_id, r_id) :
        # Basic error checking
        if l_id < 0 :
            raise ValueError("Invalid left seperator index = {0}".format(l_id))
        if r_id > self.nr_pt :
            raise ValueError("Invalid right seperator index = {0}".format(r_id))
        if r_id < l_id :
            raise ValueError("right seperator({0}) is to the left of left seperator({1})"
                    .format(r_id,l_id))

        if m == 1:
            # base case
            return
        # Divide
        m_ceil = int(math.ceil(m / 2.0))
        m_floor = int(math.floor(m / 2.0))
        self._build(m_ceil, l_id, l_id + m_ceil)
        self._build(m_floor, l_id + m_ceil, r_id)

        #conquer

    # XXX not very efficient
    def _vertical_ray_shoot(self) :
        for end_point in self.ep :
            point = end_point.pt.pt
            candidate = []
            for line in self.lines :
                if line.start.px < point.px and line.end.px > point.px :
                    candidate.append(line)
            d_min_above = float('inf')
            d_min_below = float('inf')
            for cand in candidate :
                d = cand.dist(point)
                if cand.above(point) :
                    if d < d_min_above :
                        end_point.above = cand
                        d_min_above = d
                else :
                    if cand.dist(point) < d_min_below :
                        end_point.below = cand
                        d_min_below = d

# TEST
def main() :
    s1 = Segment(Point(6,5), Point(7,8))
    s2 = Segment(Point(8,4), Point(10,16))
    s3 = Segment(Point(2,8), Point(15,10))

    lines = [s1,s2,s3]

    vor = Voronoi(lines)
    vor.build()

if __name__ == '__main__' :
    main()


