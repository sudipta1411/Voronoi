#!/usr/bin/python

# An linear space data structure to store
# the faces of voronoi diagram.

class VVertex(object) :
    def __init__(self, px=0.0, py=0.0) :
        self.px = px
        self.py = py
        self.incident = []
        self.sites = [] # Nearest site from this vertex(at least 3)

class VEdge(object) :
    def __init__(self, start=VVertex(), end=VVertex()) :
        self.startV = start
        self.endV = end
        # Note : the edge is oriented from startV to endV.
        # And also cw/ccw is w.r.t startV
        self.left_face = None
        self.right_face = None
        self.cw_next = None
        self.ccw_next = None
        self.cw_prev = None
        self.ccw_prev = None
        self.sites = [] # Nearest site from this edge(at least 2)

class VRegion(object) :
    def __init__(self) :
        self.edges = []
        self.site = None

