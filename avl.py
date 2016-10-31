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
        #if self.root is None :
        #    self.root = Node(key)
        #else :
        self.root = self._insert(self.root, key)

    def remove(self, key) :
        ret, self.root = self._remove(self.root, key)
        return ret

    def _insert(self, node, key) :
        if node is None :
            node = Node(key)
        elif key < node.key :
            node.left = self._insert(node.left, key)
            node = self.left_rebalance(node)
        elif key > node.key :
            node.right = self._insert(node.right, key)
            node = self.right_rebalance(node)
        else :
            print "Key already exists"
        return node

    # @returns a tuple(bool,node)
    def _remove(self, node, key) :
        ret = True
        if node is None :
            ret = False
        elif key < node.key :
            ret, node.left = self._remove(node.left, key)
        elif key > node.key :
            ret, node.right = self._remove(node.right, key)
        else :
            ret = True
            if node.left is None :
                node = node.right
            elif node.right is None :
                node = node.left
            else :
                min_node = self.find_min(node.right)
                node.key = min_node.key
                ret, node.right = self._remove(node.right,min_node.key)
        if ret == True and node is not None:
            h_l = self.get_height(node.left)
            h_r = self.get_height(node.right)
            if h_l > h_r+1 :
                # print 'left_rebalance {0},{1}'.format(h_l,h_r)
                node = self.left_rebalance(node)
            elif h_r > h_l+1 :
                # print 'right_rebalance {0},{1}'.format(h_l,h_r)
                node = self.right_rebalance(node)
            else :
                node = self.fix_height(node)
        return (ret, node)

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
        t.left = self.fix_height(t.left)
        t = self.fix_height(t)
        return t

    def rotate_right(self, node) :
        t = node.left
        node.left = t.right
        t.right = node
        t.right = self.fix_height(t.right)
        t = self.fix_height(t)
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

    def find_min(self, node) :
        if node.left is not None :
            return self.find_min(node.left)
        return node

    def find_max(self, node) :
        if node.right is not None :
            return self.find_max(node.right)
        return node

    @property
    def height(self) :
        return self.get_height(self.root)

    def __str__(self):
        if self.root is None: return '<empty tree>'
        def recurse(parent, node):
            if node is None: return [], 0, 0
            label = str(node.key)
            left_lines, left_pos, left_width = recurse(node, node.left)
            right_lines, right_pos, right_width = recurse(node, node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and parent is not None and \
               node is parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle-2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
              [left_line + ' ' * (width - left_width - right_width) +
               right_line
               for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(None, self.root) [0])

