#!/usr/bin/python

from numpy import *
from DataTypes import *
from scipy import optimize

def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2

def _seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom.astype(float))*db + b1

def seg_intersect(seg1, seg2) :
    # seg2 is vertical line

    p1 = array([seg1.start.px, seg1.start.py])
    p2 = array([seg1.end.px, seg1.end.py])

    p3 = array([seg2.pt.px, 0.0])
    p4 = array([seg2.pt.px, 10.0])
    res = _seg_intersect(p1, p2, p3, p4)
    return Point(res[0], res[1])

def seg_par_intersect(seg, par) :
    c = par.direc.c
    m = par.direc.m
    delta = 1.0 / (m**2 + 1)
    x0 = par.foci.px; y0 = par.foci.py
    f = lambda x,y : (x - x0)**2 + (y - y0)**2 - delta*(m*x - y + c)**2
    g = lambda x : seg.m*x + seg.c
    h = lambda x,y : f(x,y) - g(x)
    x_int = optimize.fsolve(h, 0.001, 0.001)
    y_int = g(x_int)
    print x_int
    return Point(x_int, y_int)

