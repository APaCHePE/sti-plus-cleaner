import unittest

class TestSum(unittest.TestCase):
    print("TestSum")
    def test_empty_list(self):
        self.assertEqual(sum([]), 0)

    def test_one_element_list(self):
        self.assertEqual(sum([1]), 1)

    def test_multiple_element_list(self):
        self.assertEqual(sum([1, 2, 3]), 6)

if __name__ == "__main__":
    unittest.main()