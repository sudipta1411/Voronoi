#!/usr/bin/pythnon

class Point(object) :
    def __init__(self, px=0.0, py=0.0) :
        self.px = px
        self.py = py

    def get_point(self) :
        return self.px, self.py

    def __str__(self) :
        return '({0},{1})'.format(self.px, self.py)

class Site(Point) :
    def __init__(self, px=0.0, py=0.0) :
        self.site_id = 0
        super(Site, self).__init__(px, py)

    def get_id(self) : return self.site_id

    def bisect(self, site) :
        edge = Edge()
        dx = float(site.px) - float(self.px)
        dy = float(site.py) - float(self.py)
        print 'dx {0}, dy {1}'.format(dx,dy)
        if dy == 0.0 :
            # line is perpendicular x=c
            edge.m = float('inf')
            edge.c = (self.px + site.px) * 0.5
            if self.px < edge.c :
                edge.l_site = self
                edge.r_site = site
            else :
                edge.l_site = site
                edge.r_site = self
        else :
            edge.m = -float(dx) / dy
            edge.c = (self.py + site.py - edge.m * (self.px + site.px)) * 0.5
            if self.py > edge.m * self.px + edge.c :
                edge.l_site = self
                edge.r_site = site
            else :
                edge.l_site = site
                edge.r_site = self
        return edge

class Vertex(Point) :
    def __init__(self, px=0.0, py=0.0) :
        self.vert_id = 0
        super(Vertex, self).__init__(px, py)

    def get_id(self) : return self.vert_id

class Edge(object) :
    def __init__(self, start=None, end=None, r_site=None, l_site = None):
        # start and end are Vertices, l_site and r_site are Sites
        self.start = start
        self.end = end
        self.l_site = l_site
        self.r_site = r_site
        self.edge_id = 0
        # y=m*x+c
        self.m = None
        self.c = None
