from Function import Function
from Constant import Constant
from Variable import Variable
from SimplePower import Power
from Exponential import Exponential
from SimplePower import SimplePower
from Multiply import Multiply
import unittest


class MultiplyTest(unittest.TestCase):
    def test_combine_constants(self):
        product = Multiply([1, 3, 1, Constant(2), Constant(-1.5), 0.1])
        product.combine_constants()
        # test that product is length 1
        self.assertEqual(len(product.factors), 1)
        # test that product is correct
        self.assertEqual(product.factors[0], Constant(-0.9))

    def test_remove_nested_multiply(self):
        product = Multiply([8, Multiply([Multiply([3, Constant(0.5)]), Constant(-2)])])
        product.remove_nested_multiply()
        # test that product is length 4
        self.assertEqual(len(product.factors), 4)
        # test that product is correct
        self.assertEqual(product.factors, [8, 3, 0.5, -2])

    def test_combine_powers(self):
        product = Multiply([5, SimplePower("x", 2), SimplePower("x", 3), SimplePower("x", 0.5),
                            SimplePower("y", -2), SimplePower("x", 3), SimplePower("y", 10)])
        product.combine_powers()
        # test the length is correct
        self.assertEqual(len(product.factors), 3)
        # test that product is correct
        # self.assertTrue(product.factors == [5, SimplePower("x", 8.5), SimplePower("y", 8)] or
        # product.factors == [5, SimplePower("y", 8), SimplePower("x", 8.5)])
        self.assertEqual(product.factors[0], 5)
        if product.factors[1].base == "x":
            self.assertEqual(product.factors[1].power, 8.5)
            self.assertEqual(product.factors[2].base, "y")
            self.assertEqual(product.factors[2].power, 8)
        elif product.factors[1].base == "y":
            self.assertEqual(product.factors[1].power, 8)
            self.assertEqual(product.factors[2].base, "x")
            self.assertEqual(product.factors[2].power, 8.5)
        else:
            self.assertEqual(0, 1)

    def test_simplify(self):
        product = Multiply([8, Multiply([Multiply([3, Constant(0.5)]), Constant(-2)])])
        product.simplify()
        # test that product is length 1
        self.assertEqual(len(product.factors), 1)
        # test that product is correct
        self.assertEqual(product.factors, [-24])
