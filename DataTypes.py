#!/usr/bin/python

# from collections import namedtuple
import math

class Point(object) :
    def __init__(self, px=0.0, py=0.0) :
        self._px = float(px)
        self._py = float(py)

    @property
    def px(self) : return self._px

    @property
    def py(self) : return self._py

    def dist(self,pt) : return math.sqrt((pt.px - self._px)**2 \
            + (pt.py - self._py)**2)

    def __str__(self) :
        return '({0},{1})'.format(self._px, self._py)

class Segment(object) :
    # start Point, end Point. This is to
    # represent line, halfline, line segment
    def __init__(self, start=None, end=None, m=None, c=None, hl=False) :
        self._start = start
        self._end = end
        self._m = m
        self._c = c
        self._hl = hl

        if self._start and self._end :
            if self._end.px == self._start.px :
                self._m = self._c = float('inf')
            else:
                self._m = (self._end.py - self._start.py) / (self._end.px - self._start.px)
                self._c = (self._start.px * self._end.py - self._start.py * self._end.px) \
                        / (self._start.px - self._end.px)

    @property
    def hl(self) : return self._hl

    @hl.setter
    def hl(self, val) : self._hl = val

    @property
    def m(self) : return self._m

    @m.setter
    def m(self, val) : self._m = val

    @property
    def c(self) : return self._c

    @c.setter
    def c(self, val) : self._c = val

    @property
    def start(self) : return self._start

    @start.setter
    def start(self, val) :
        self._start = val
        if self._start and self._end :
            if self._end.px == self._start.px :
                self._m = self._c = float('inf')
            else:
                self._m = (self._end.py - self._start.py) / (self._end.px - self._start.px)
                self._c = (self._start.px * self._end.py - self._start.py * self._end.px) \
                        / (self._start.px - self._end.px)

    @property
    def end(self) : return self._end

    @end.setter
    def end(self, val) :
        self._end = val
        if self._start and self._end :
            if self._end.px == self._start.px :
                self._m = self._c = float('inf')
            else:
                self._m = (self._end.py - self._start.py) / (self._end.px - self._start.px)
                self._c = (self._start.px * self._end.py - self._start.py * self._end.px) \
                        / (self._start.px - self._end.px)

    def isOnLine(self, point) :
        if not self._start or not self._end : return False
        return point._py == self._m * point._px + self._c

    def isOnSegment(self, point) :
        if not self.isOnLine(point) : return False
        return (self._start.px<=point.px<=self._end.px) \
                and (self._start.py<=point.py<=self._end.py)

    def dist(self, pt) :
        # if self.isOnSegment(pt) :
        return abs(self._m * pt.px - pt.py + self._c) \
                / math.sqrt(1 + self._m**2)
        # return min(pt.dist(self._start), pt.dist(self._end))

    # XXX line is above the point
    def above(self, pt) :
        return pt.py < self._m * pt.px + self._c

    # XXX line is below the point
    def below(self, pt) :
        return pt.py > self._m * pt.px + self._c

    def __str__(self) : return '[{0},{1}]'.format(self._start, self._end)

class Parabola(object) :
    # A parabola is determined by a focal point and directrix
    # if p=(px,py) is the focus and L:y=mx+c is the directrix the the parabola is
    # x^2 + y^2 -2(x*px+y*py) = -delta*px^2 - m^2*delta*py^2 
    # + delta*(c^2-2m*px*py-2c*py+2mc*px) where delta = 1/(1+m^2)
    def __init__(self, foci, direc, start=None, end=None) :
        self._foci = foci
        self._direc = direc
        self._start = start
        self._end = end

    @property
    def foci(self) : return self._foci

    @foci.setter
    def foci(self, val) : self._foci = val

    @property
    def direc(self) : return self._direc

    @direc.setter
    def direc(self, val) : self._direc = val

    @property
    def start(self) : return self._start

    @start.setter
    def start(self, val) : self._start = val

    @property
    def end(self) : return self._end

    @end.setter
    def end(self, val) : self._end = val

class VertLine(object) :
    # represent a vertical line through a given point to a given line
    # if no line is specified, then the line is vertical to x-axis
    # pt in most cases is the endpoint of the line
    def __init__(self, pt, line=None) :
        self._pt = pt
        self._vert = Segment()
        if line is not None :
            self._vert.m = -1.0 / line.m
            self._vert.c = self._pt.py - self._vert.m * pt.px

    @property
    def pt(self) : return self._pt

    @property
    def vert(self) : return self._vert

class Site(object) :
    # a site can be either a point or a line segment
    def __init__(self, pt=None, seg=None) :
        self._pt = pt
        self._seg = seg

    @property
    def pt(self) : return self._pt

    @property
    def seg(self) : return self._seg

    def isPointSite(self) : return self._pt is not None

    def isLineSite(self) : return self._seg is not None

class Vertex(object) :
    # A vertex is always a point
    def __init__(self, pt) :
        self._pt = pt

    @property
    def pt(self) : return self._pt

class Edge(object) :
    # An edge can be either a line segment,
    # halfline or a section of parabola
    def __init__(self, seg=None, prb=None) :
        self._seg = seg
        self._prb = prb

    @property
    def seg(self) : return self._seg

    @seg.setter
    def seg(self, val) : self._seg = val

    @property
    def prb(self) : return self._prb

    @prb.setter
    def prb(self, val) : self._prb = val

class Quad(object) :
    # left and right are vertical lines upper
    # and lower are long walls. Left and right
    # seperators are annotated with the windows
    # created by the crossing. Each window is a
    # vertical line segment or half line.
    def __init__(self, upper=None, lower=None, left=None, right=None) :
        self._upper = upper
        self._lower = lower
        self._left = left
        self._right = right
        self._active = False
        self.r_windows = []
        self.l_windows = []

    @property
    def upper(self) : return self._upper

    @upper.setter
    def upper(self, val) : self._upper = val

    @property
    def lower(self) : return self._lower

    @lower.setter
    def lower(self, val) : self._lower = val

    @property
    def left(self) : return self._left

    @left.setter
    def left(self, val) : self._left = val

    @property
    def right(self) : return self._right

    @right.setter
    def right(self, val) : self._right = val

    @property
    def active(self) : return self._active

    @active.setter
    def active(self, val) : self._active = val

    def getCorners(self) : pass
