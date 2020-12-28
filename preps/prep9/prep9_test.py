from prep9 import *
import unittest


class TestMaximum(unittest.TestCase):
    def test_invlaid_case(self):
        expect = None
        tree = BinarySearchTree(None)
        actual = tree.maximum()
        self.assertEqual(expect, actual)

    def test_complete_tree(self):
        expect = 100
        tree = BinarySearchTree(50)
        left = BinarySearchTree(30)
        left._left = BinarySearchTree(20)
        left._right = BinarySearchTree(40)
        right = BinarySearchTree(70)
        right._left = BinarySearchTree(60)
        right._right = BinarySearchTree(100)
        tree._left = left
        tree._right = right
        actual = tree.maximum()
        self.assertEqual(expect, actual)

    def test_left_tree(self):
        expect = 50
        tree = BinarySearchTree(50)
        left = BinarySearchTree(30)
        left._left = BinarySearchTree(20)
        left._left._left = BinarySearchTree(10)
        tree._left = left
        actual = tree.maximum()
        self.assertEqual(expect, actual)

    def test_right_tree(self):
        expect = 99
        tree = BinarySearchTree(50)
        right = BinarySearchTree(60)
        right._right = BinarySearchTree(70)
        right._right._right = BinarySearchTree(99)
        tree._right = right
        actual = tree.maximum()
        self.assertEqual(expect, actual)


class TestCount(unittest.TestCase):
    def test_invlaid_case(self):
        expect = 0
        tree = BinarySearchTree(None)
        actual = tree.count(4)
        self.assertEqual(expect, actual)

    def test_count_0(self):
        expect = 0
        tree = BinarySearchTree(50)
        left = BinarySearchTree(40)
        left._left = BinarySearchTree(30)
        right = BinarySearchTree(90)
        right._left = BinarySearchTree(80)
        right._right = BinarySearchTree(100)
        tree._left = left
        tree._right = right
        actual = tree.count(1)
        self.assertEqual(expect, actual)

    def test_count_all(self):
        expect = 7
        tree = BinarySearchTree(50)
        left = BinarySearchTree(50)
        left._left = BinarySearchTree(50)
        left._right = BinarySearchTree(50)
        right = BinarySearchTree(50)
        right._left = BinarySearchTree(50)
        right._right = BinarySearchTree(50)
        tree._left = left
        tree._right = right
        actual = tree.count(50)
        self.assertEqual(expect, actual)

    def test_count_left_tail(self):
        expect = 1
        tree = BinarySearchTree(50)
        left = BinarySearchTree(40)
        left._left = BinarySearchTree(30)
        left._right = BinarySearchTree(41)
        left._left._left = BinarySearchTree(20)
        right = BinarySearchTree(58)
        right._left = BinarySearchTree(52)
        right._right = BinarySearchTree(70)
        tree._left = left
        tree._right = right
        actual = tree.count(20)
        self.assertEqual(expect, actual)

    def test_count_right_tail(self):
        expect = 1
        tree = BinarySearchTree(60)
        left = BinarySearchTree(50)
        left._left = BinarySearchTree(40)
        left._right = BinarySearchTree(45)
        right = BinarySearchTree(70)
        right._left = BinarySearchTree(65)
        right._right = BinarySearchTree(80)
        right._right._right = BinarySearchTree(99)
        tree._left = left
        tree._right = right
        actual = tree.count(99)
        self.assertEqual(expect, actual)

    def test_internal_2(self):
        expect = 2
        tree = BinarySearchTree(60)
        left = BinarySearchTree(50)
        left._left = BinarySearchTree(40)
        left._right = BinarySearchTree(45)
        right = BinarySearchTree(70)
        right._left = BinarySearchTree(65)
        right._right = BinarySearchTree(80)
        right._right._left = BinarySearchTree(80)
        right._right._right = BinarySearchTree(99)
        tree._left = left
        tree._right = right
        actual = tree.count(80)
        self.assertEqual(expect, actual)

    def test_internal_3(self):
        expect = 3
        tree = BinarySearchTree(60)
        left = BinarySearchTree(50)
        left._left = BinarySearchTree(40)
        left._right = BinarySearchTree(45)
        right = BinarySearchTree(70)
        right._left = BinarySearchTree(65)
        right._right = BinarySearchTree(80)
        right._right._left = BinarySearchTree(80)
        right._right._left._right = BinarySearchTree(80)
        right._right._right = BinarySearchTree(99)
        tree._left = left
        tree._right = right
        actual = tree.count(80)
        self.assertEqual(expect, actual)


class TestItems(unittest.TestCase):
    def test_invalid_case(self):
        expect = []
        tree = BinarySearchTree(None)
        actual = tree.items()
        self.assertListEqual(expect, actual)

    def test_complete_tree(self):
        expect = [1, 2, 3, 4, 5, 6, 7]
        tree = BinarySearchTree(4)
        left = BinarySearchTree(2)
        left._left = BinarySearchTree(1)
        left._right = BinarySearchTree(3)
        right = BinarySearchTree(6)
        right._left = BinarySearchTree(5)
        right._right = BinarySearchTree(7)
        tree._left = left
        tree._right = right
        actual = tree.items()
        self.assertListEqual(expect, actual)

    def test_left_line(self):
        expect = [1, 2, 3, 4, 5]
        tree = BinarySearchTree(5)
        left = BinarySearchTree(4)
        left._left = BinarySearchTree(3)
        left._left._left = BinarySearchTree(2)
        left._left._left._left = BinarySearchTree(1)
        tree._left = left
        actual = tree.items()
        self.assertListEqual(expect, actual)

    def test_right_line(self):
        expect = [10, 20, 30, 40, 50]
        tree = BinarySearchTree(10)
        right = BinarySearchTree(20)
        right._right = BinarySearchTree(30)
        right._right._right = BinarySearchTree(40)
        right._right._right._right = BinarySearchTree(50)
        tree._right = right
        actual = tree.items()
        self.assertListEqual(expect, actual)

    def test_unpack_tree(self):
        expect = [10, 20, 30]
        tree = BinarySearchTree(20)
        left = BinarySearchTree(10)
        right = BinarySearchTree(30)
        tree._left = left
        tree._right = right
        actual = tree.items()
        self.assertListEqual(expect, actual)

    def test_unpack_tree_2(self):
        expect = [10, 20, 30, 40, 50]
        tree = BinarySearchTree(20)
        left = BinarySearchTree(10)
        right = BinarySearchTree(30)
        right._right = BinarySearchTree(50)
        right._right._left = BinarySearchTree(40)
        tree._left = left
        tree._right = right
        actual = tree.items()
        self.assertListEqual(expect, actual)


class TestSmaller(unittest.TestCase):
    def test_invalid_case(self):
        expect = []
        tree = BinarySearchTree(None)
        actual = tree.smaller(10)
        self.assertListEqual(expect, actual)

    def test_empty_list(self):
        expect = []
        tree = BinarySearchTree(3)
        tree._left = BinarySearchTree(2)
        tree._right = BinarySearchTree(4)
        actual = tree.smaller(2)
        self.assertListEqual(expect, actual)

    def test_whole_tree(self):
        expect = [1, 2, 3, 4, 5, 6, 7]
        tree = BinarySearchTree(4)
        left = BinarySearchTree(2)
        left._left = BinarySearchTree(1)
        left._right = BinarySearchTree(3)
        right = BinarySearchTree(6)
        right._left = BinarySearchTree(5)
        right._right = BinarySearchTree(7)
        tree._left = left
        tree._right = right
        actual = tree.smaller(8)
        self.assertListEqual(expect, actual)

    def test_left_line_1(self):
        expect = [1, 2]
        tree = BinarySearchTree(5)
        left = BinarySearchTree(4)
        left._left = BinarySearchTree(3)
        left._left._left = BinarySearchTree(2)
        left._left._left._left = BinarySearchTree(1)
        tree._left = left
        actual = tree.smaller(3)
        self.assertListEqual(expect, actual)

    def test_left_line_2(self):
        expect = [1, 2, 3, 4, 5]
        tree = BinarySearchTree(5)
        left = BinarySearchTree(4)
        left._left = BinarySearchTree(3)
        left._left._left = BinarySearchTree(2)
        left._left._left._left = BinarySearchTree(1)
        tree._left = left
        actual = tree.smaller(6)
        self.assertListEqual(expect, actual)

    def test_right_line_1(self):
        expect = [10, 20, 30]
        tree = BinarySearchTree(10)
        right = BinarySearchTree(20)
        right._right = BinarySearchTree(30)
        right._right._right = BinarySearchTree(40)
        right._right._right._right = BinarySearchTree(50)
        tree._right = right
        actual = tree.smaller(40)
        self.assertListEqual(expect, actual)

    def test_right_line_2(self):
        expect = [10, 20, 30, 40, 50]
        tree = BinarySearchTree(10)
        right = BinarySearchTree(20)
        right._right = BinarySearchTree(30)
        right._right._right = BinarySearchTree(40)
        right._right._right._right = BinarySearchTree(50)
        tree._right = right
        actual = tree.smaller(100)
        self.assertListEqual(expect, actual)

    def test_partial_tree(self):
        expect = [1, 2, 3, 4]
        tree = BinarySearchTree(4)
        left = BinarySearchTree(2)
        left._left = BinarySearchTree(1)
        left._right = BinarySearchTree(3)
        right = BinarySearchTree(6)
        right._left = BinarySearchTree(5)
        right._right = BinarySearchTree(7)
        tree._left = left
        tree._right = right
        actual = tree.smaller(5)
        self.assertListEqual(expect, actual)

    def test_partial_tree_2(self):
        expect = [1, 2, 3, 4, 5, 6]
        tree = BinarySearchTree(4)
        left = BinarySearchTree(2)
        left._left = BinarySearchTree(1)
        left._right = BinarySearchTree(3)
        right = BinarySearchTree(6)
        right._left = BinarySearchTree(5)
        right._right = BinarySearchTree(7)
        tree._left = left
        tree._right = right
        actual = tree.smaller(7)
        self.assertListEqual(expect, actual)

    def test_partial_tree_3(self):
        expect = [10, 20, 30, 40]
        tree = BinarySearchTree(20)
        left = BinarySearchTree(10)
        right = BinarySearchTree(30)
        right._right = BinarySearchTree(50)
        right._right._left = BinarySearchTree(40)
        tree._left = left
        tree._right = right
        actual = tree.smaller(50)
        self.assertListEqual(expect, actual)

    def test_partial_tree_4(self):
        expect = [10]
        tree = BinarySearchTree(30)
        left = BinarySearchTree(20)
        left._left = BinarySearchTree(10)
        left._right = BinarySearchTree(25)
        right = BinarySearchTree(30)
        right._right = BinarySearchTree(50)
        right._right._left = BinarySearchTree(40)
        tree._left = left
        tree._right = right
        actual = tree.smaller(20)
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    unittest.main(exit=False)
