"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False

        # You will change this in Task 5
        # if len(self._subtrees) > 0:
        #     self._expanded = True
        # else:
        #     self._expanded = False

        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.data_size = 0
        if self._subtrees == []:
            self.data_size = data_size
        else:
            for sub in self._subtrees:
                self.data_size += sub.data_size

        for a in self._subtrees:
            a._parent_tree = self


    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        self.update_data_sizes()
        if self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif self._subtrees == []:
            self.rect = rect
        else:
            x, y, width, height = rect
            self.rect = rect
            if width > height:
                sumw = 0
                for e in range(len(self._subtrees) - 1):
                    subwidth = self._subtrees[e].data_size * width // \
                               self.data_size
                    self._subtrees[e].update_rectangles((x, y, subwidth, \
                                                         height))
                    sumw += subwidth
                    x += subwidth
                self._subtrees[-1].update_rectangles((x, y, width - sumw, \
                                                      height))
            else:
                sumh = 0
                for f in range(len(self._subtrees) - 1):
                    subheight = self._subtrees[f].data_size * \
                                height // self.data_size
                    self._subtrees[f].update_rectangles((x, y, width, \
                                                         subheight))
                    y += subheight
                    sumh += subheight
                self._subtrees[-1].update_rectangles((x, y, width, \
                                                      height - sumh))


    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self._name is None:
            return []
        if not self._expanded:
            return [(self.rect, self._colour)]
        else:
            result = []
            for f in self._subtrees:
                result.extend(f.get_rectangles())
            return result


    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        if self.is_empty():
            return None
        x, y, width, height = self.rect
        a = x + width
        b = y + height
        xp, yp = pos
        if not self._expanded:
            if x == y == xp == yp == 0:
                return self
            elif x == xp == 0 and y < yp <= b:
                return self
            elif y == yp == 0 and x < xp <= a:
                return self
            elif xp <= x or yp <= y or xp > a or yp > b:
                return None
            else:# y < yp <= b and x < xp <= a:
                return self
        else:
            for g in self._subtrees:
                h = g.get_tree_at_position(pos)
                if h is not None:
                    return h
            return None


    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self._subtrees != []:
            self.data_size = 0
            for sub in self._subtrees:
                if sub._subtrees != []:
                    sub.update_data_sizes()
                self.data_size += sub.data_size
        return self.data_size


    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self._subtrees == [] and destination._subtrees != [] and \
                not self.is_empty() and not self.is_empty():
            destination._subtrees.append(self)
            self._parent_tree._subtrees.remove(self)
            self._parent_tree.data_size -= self.data_size
            self._parent_tree = destination
            self.update_data_sizes()
            self._update_parent_tree()

    def _update_parent_tree(self) -> None:
        """Update the data size of all the trees below this tree"""
        if self._parent_tree is not None:
            self._parent_tree.data_size = 0
            for o in self._parent_tree._subtrees:
                self._parent_tree.data_size += o.data_size
            self._parent_tree._update_parent_tree()

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self._subtrees == []:
            if factor >= 0:
                change = math.ceil(self.data_size * factor)
            else:
                change = math.floor(self.data_size * factor)
            self.data_size += change
            if self.data_size < 1:
                self.data_size = 1
            self._update_parent_tree()

    def expand(self) -> None:
        """Expand the select folder"""
        if self._subtrees != []:
            self._expanded = True

    def expand_all(self) -> None:
        """Expand all folders into file."""
        if self._subtrees != []:
            self._expanded = True
            for i in self._subtrees:
                i.expand_all()

    def collapse(self) -> None:
        """Unexpand the select file"""
        if self._parent_tree is not None:
            self._parent_tree._collapse_lower()

    def _collapse_lower(self) -> None:
        self._expanded = False
        if self._subtrees != []:
            for i in self._subtrees:
                i._collapse_lower()

    def collapse_all(self) -> None:
        """Unexpand all the file"""
        if self._parent_tree is not None:
            self._parent_tree._expanded = False
            self._parent_tree.collapse_all()
        self._collapse_lower()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.rect = (0, 0, 0, 0)
        self._name = os.path.basename(path)
        self._parent_tree = None
        self._expanded = False
        if os.path.isdir(path):
            self._subtrees = []
            lstdir = os.listdir(path)
            for b in lstdir:
                self._subtrees.append(FileSystemTree(os.path.join(path, b)))
            self.data_size = 0
            if self._subtrees != []:
                for c in self._subtrees:
                    self.data_size += c.data_size
            for d in self._subtrees:
                d._parent_tree = self
        else:
            self.data_size = os.path.getsize(path)
            self._subtrees = []

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
