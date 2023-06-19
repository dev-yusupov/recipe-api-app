from django.test import SimpleTestCase

from . import calc

class Calc_Test(SimpleTestCase):
    """Test the calc module"""

    def test_add_numbers(self):
        res = calc.add(4,5)

        self.assertEqual(res, 9)
    
    def test_subtract_numbers(self):
        res = calc.subtract(5, 4)

        self.assertEqual(res, 1)
    
    def test_multiply_numbers(self):
        res = calc.multiply(5, 2)

        self.assertEqual(res, 10)