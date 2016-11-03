#!/usr/bin/python

class Point(object) :
    def __init__(self, px=0.0, py=0.0) :
        self.px = float(px)
        self.py = float(py)

    def __str__(self) :
        return '({0},{1})'.format(self.px, self.py)

class Segment(object) :
    # start Point, end Point
    def __init__(self, start=None, end=None, m=None, c=None) :
        self.start = start
        self.end = end
        self.m = m
        self.c = c

        if self.start and self.end :
            self.m = (self.end.py - self.start.py) / (self.end.px - self.start.px)
            self.c = (self.start.px * self.end.py - self.start.py * self.end.px) / (self.start.px - self.end.px)

    @property
    def m(self) : return self.m

    @property.setter
    def m(self, m) : self.m = m

    @property
    def c(self) : return self.c

    @property.setter
    def c(self, c) : self.c = c

    @property
    def start(self) : return self.start

    @property.setter
    def start(self, start) :
        self.start = start
        if self.start and self.end :
            self.m = (self.end.py - self.start.py) / (self.end.px - self.start.px)
            self.c = (self.start.px * self.end.py - self.start.py * self.end.px) / (self.start.px - self.end.px)

    @property
    def end(self) : return self.end

    @property.setter
    def end(self, end) :
        self.end = end
        if self.start and self.end :
            self.m = (self.end.py - self.start.py) / (self.end.px - self.start.px)
            self.c = (self.start.px * self.end.py - self.start.py * self.end.px) / (self.start.px - self.end.px)

    def isOnLine(self, point) :
        if not self.start or not self.end : return False
        return point.py == self.m * point.px + self.c

    def isOnSegment(self, point) :
        if not self.isOnLine(point) : return False
        return (self.start.px<=point.px<=self.end.px) \
                and (self.start.py<=point.py<=self.end.py)

class Parabola(object) :
    # A parabola is determined by a focal point and directrix
    def __init__(self, foci, direc, start=None, end=None) :
        self.foci = foci
        self.direc = direc
        self.start = start
        self.end = end

    @property foci(self) : return self.foci

    @property.setter
    def foci(self, foci) : self.foci = foci

    @property
    def direc(self) : return self.direc

    @property.setter
    def direc(self, direc) : self.direc = direc

    @property
    def start(self) : return self.start

    @property.setter
    def start(self, start) : self.start = start

    @property
    def end(self) : return self.end

    @property.setter
    def end(self, end) : self.end = end

class VertLine(object) :
    # represent a vertical line through a given point to a given line
    # if no line is specified, then the line is vertical to x-axis
    def __init__(self, pt, line=None) :
        self.pt = pt
        self.vert = Segment()
        if line is not None :
            self.vert.m = -1.0 / line.m
            self.vert.c = self.pt.py - self.vert.m * pt.px

    @property
    def pt(self) : return self.pt

    @property
    def vert(self) : return self.vert
