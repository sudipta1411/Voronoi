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
        if self.root is None :
            self.root = Node(key)
        else :
            self.root = self._insert(self.root, key)

    def _insert(self, node, key) :
        if node is None :
            print '2'
            node = Node(key)
        elif key < node.key :
            print '3'
            node.left = self._insert(node.left, key)
            node = self.left_rebalance(node)
        elif key > node.key :
            print '4'
            node.right = self._insert(node.right, key)
            node = self.right_rebalance(node)
        else :
            print "Key already exists"
        return node

    def right_rebalance(self, node) :
        l = node.left
        r = node.right
        h_l = self.get_height(l)
        h_r = self.get_height(r)
        if h_r > h_l+1 :
            if self.get_height(r.right) >= self.get_height(r.left) :
                node = self.rotate_left(node)
            else :
                node = self.rotate_right_left(node)
        else :
            node = self.fix_height(node)
        return node

    def left_rebalance(self, node) :
        l = node.left
        r = node.right
        h_l = self.get_height(l)
        h_r = self.get_height(r)
        if h_l > h_r+1 :
            if self.get_height(l.left) >= self.get_height(l.right) :
                node = self.rotate_right(node)
            else :
                node = self.rotate_left_right(node)
        #else :
        node = self.fix_height(node)
        return node

    def rotate_left(self, node) :
        t = node.right
        node.right = t.left
        t.left = node
        self.fix_height(t.right)
        self.fix_height(t)
        return t

    def rotate_right(self, node) :
        t = node.left
        node.left = t.right
        t.right = node
        self.fix_height(t.right)
        self.fix_height(t)
        return t

    def rotate_left_right(self, node) :
        t = node.left
        node.left = self.rotate_left(t)
        return self.rotate_right(node)

    def rotate_right_left(self, node) :
        t = node.right
        node.right = self.rotate_right(t)
        return self.rotate_left(node)

    def fix_height(self, node) :
        if node is not None :
            h_l = self.get_height(node.left)
            h_r = self.get_height(node.right)
            node.height = (h_l+1) if h_l > h_r else (h_r+1)
        return node

    def postorder(self) :
        self._postorder(self.root)

    def _postorder(self, node) :
        if node is not None :
            self._postorder(node.left)
            self._postorder(node.right)
            print node.key

    def get_height(self, node) :
        return 0 if node is None else node.height
