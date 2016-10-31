#!/usr/bin/python

class Node(object) :
    def __init__(self, key) :
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVLTree(object) :
    def __init__(self) :
        self.root = None

     def insert(self, key) :
        self._insert(self.root, key)

    def _insert(self, key) :
        # if self.root is None :
        #    print '1'
        #    self.root = Node(key)
        # elif node is None :
        if node is None :
            print '2'
            node = Node(key)
        elif key < node.key :
            print '3'
            self.insert(key, node.left)
            node = self.left_rebalance(node)
        elif key > node.key :
            print '4'
            self.insert(key, node.right)
            node = self.right_rebalance(node)
        else :
            print "Key already exists"
        # return node

    def right_rebalance(self,node) :
        l = node.left, r = node.right
        h_l = l.height, h_r = r.height
        if h_r > h_l+1 :
            if r.right.height >= r.left.height :
                node = self.rotate_left(node)
            else :
                node = self.rotate_right_left(n)
        else :
            node = fix_height(node)
        return node

    def left_rebalance(node) :
        l = node.left, r = node.right
        h_l = l.height, h_r = r.height
        if h_l > h_r+1 :
            if l.left.height >= l.right.height :
                node = rotate_right(node)
            else :
                node = rotate_letf_right(node)
        #else :
        node = fix_height(node)
        return node

    def rotate_left(node) :
        t = node.right
        node.right = t.left
        t.left = node
        fix_height(t.right)
        fix_height(t)
        return t

    def rotate_right(node) :
        t = node.left
        node.left = t.right
        t.right = node
        fix_height(t.right)
        fix_height(t)
        return t

    def rotate_letf_right(node) :
        t = node.left
        node.left = rotate_left(t)
        return rotate_right(node)

    def rotate_right_left(node) :
        t = node.right
        node.right = rotate_right(t)
        return rotate_left(node)

    def fix_height(node) :
        if node is not None :
            h_l = node.letf.height
            h_r = node.right.height
            node.height = (l_h+1) if l_h > r_h else (r_h+1)
        return node

    def postorder(self) :
        self._postorder(self.root)

    def _postorder(self,node) :
        if node is not None :
            self._postorder(node.left)
            self._postorder(node.right)
            print node.key
