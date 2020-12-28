from prep8 import *
import unittest
class TestNumPositives(unittest.TestCase):
    def test_none(self):
        temp = Tree(None, [])
        expect = 0
        actual = temp.num_positives()
        self.assertEqual(expect, actual)

    def test_leaft(self):
        temp = Tree(1, [])
        expect = 1
        actual = temp.num_positives()
        self.assertEqual(expect, actual)

    def test_leaf2(self):
        temp = Tree(0, [])
        expect = 0
        actual = temp.num_positives()
        self.assertEqual(expect, actual) 

    def test_leaf3(self):
        temp = Tree(-1, [])
        expect = 0
        actual = temp.num_positives()
        self.assertEqual(expect, actual)

    def test_random_tree(self):
        temp = Tree(-1,[Tree(1,[Tree(2,[Tree(-3,[Tree(-4,[])])])])])
        expect = 2
        actual = temp.num_positives()
        self.assertEqual(expect, actual)

    def test_all_positive(self):
        temp = Tree(1,[Tree(2,[Tree(3,[Tree(4,[])])])])
        expect = 4
        actual = temp.num_positives()
        self.assertEqual(expect, actual)

    def test_all_negative(self):
        temp = Tree(0,[Tree(-1,[Tree(-2, [])])])
        expect = 0
        actual = temp.num_positives()
        self.assertEqual(expect, actual)


class TestMaximum(unittest.TestCase):
    def test_none(self):
        temp = Tree(None, [])
        expect = 0
        actual = temp.maximum()
        self.assertEqual(expect, actual)
    
    def test_leaf(self):
        temp = Tree(10, [])
        expect = 10
        actual = temp.maximum()
        self.assertEqual(expect, actual)
    
    def test_all_positive(self):
        temp = Tree(10, [Tree(100,[Tree(30,[])])])
        expect = 100
        actual = temp.maximum()
        self.assertEqual(expect, actual)
    
    def test_all_positive_2(self):
        temp = Tree(1000,[Tree(10,[Tree(20,[])])])
        expect = 1000
        actual = temp.maximum()
        self.assertEqual(expect, actual)
    
    def test_allpositive_3(self):
        temp = Tree(1000,[Tree(400,[Tree(4000,[])])])
        expect = 4000
        actual = temp.maximum()
        self.assertEqual(expect, actual)
    
    def test_all_negative(self):
        temp = Tree(-10,[Tree(-1, [Tree(-3,[Tree(-2,[])])])])
        expect = -1
        actual = temp.maximum()
        self.assertEqual(expect, actual)
    
    def test_all_negiative_2(self):
        temp = Tree(-10,[Tree(-5, [Tree(0,[])])])
        expect = 0
        actual = temp.maximum()
        self.assertEqual(expect, actual)


class TestHeight(unittest.TestCase):
    def test_none(self):
        temp = Tree(None, [])
        expect = 0
        actual = temp.height()
        self.assertEqual(expect, actual)
    
    def test_leaf(self):
        temp = Tree(1, [])
        expect = 1
        actual = temp.height()
        self.assertEqual(expect, actual)

    def test_signle_tree(self):
        temp = Tree(1,[Tree(2,[Tree(3,[Tree(4,[])])])])
        expect = 4
        actual = temp.height()
        self.assertEqual(expect, actual)
    
    def test_one_line(self):
        temp = Tree(1, [Tree(3,[])])
        expect = 2
        actual = temp.height()
        self.assertEqual(expect, actual)

    def test_equal_height(self):
        temp = Tree(1, [Tree(3,[]), Tree(2,[])])
        expect = 2
        actual = temp.height()
        self.assertEqual(expect, actual)
    
    def test_right_tree(self):
        temp = Tree(1,[Tree(2,[Tree(3,[])]),Tree(4,[Tree(5,[Tree(6,[])])])])
        expect = 4
        actual = temp.height()
        self.assertEqual(expect, actual)

    def test_left_tree(self):
        temp = Tree(1,[Tree(2,[Tree(3,[Tree(4,[])])]), Tree(5,[Tree(6,[])])])
        expect = 4
        actual = temp.height()
        self.assertEqual(expect, actual)

    def test_right_most_tree(self):
        temp = Tree(1,[Tree(2,[]),Tree(3,[]),Tree(4,[Tree(5,[])])])
        expect = 3
        actual = temp.height()
        self.assertEqual(expect, actual)
        
        
class TestContains(unittest.TestCase):
    def test_none(self):
        temp = Tree(None, [])
        expect = False
        actual = temp.__contains__(5)
        self.assertEqual(expect, actual)
    
    def test_leaf(self):
        temp = Tree(3,[])
        expect = True
        actual = temp.__contains__(3)
        self.assertEqual(expect, actual)
    
    def test_leaf2(self):
        temp = Tree(5,[])
        expect = False
        actual = temp.__contains__(3)
        self.assertEqual(expect, actual)  
    
    def test_false(self):
        temp = Tree(5,[Tree(3,[Tree(4,[])])])
        expect = False
        actual = temp.__contains__(7)
        self.assertEqual(expect, actual)
    
    def test_true(self):
        temp = Tree(5,[Tree(3,[Tree(7,[])]), Tree(2,[Tree(7,[])])])
        expect = True
        actual = temp.__contains__(7)
        self.assertEqual(expect, actual)
    
    def test_one_line(self):
        temp = Tree(1,[Tree(2,[Tree(3,[Tree(4,[])])])])
        expect = True
        actual = temp.__contains__(4)
        self.assertEqual(expect, actual)
    
    def test_one_line2(self):
        temp = Tree(1,[Tree(3,[Tree(5,[])])])
        expect = False
        actual = temp.__contains__(7)
        self.assertEqual(expect, actual)
    
    def test_one_line3(self):
        temp = Tree(1,[Tree(3,[Tree(5,[Tree(7,[])])])])
        expect = True
        actual = temp.__contains__(1)
        self.assertEqual(expect, actual)        

if __name__ == "__main__":
    unittest.main(exit = False)