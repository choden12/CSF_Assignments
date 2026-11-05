"""Run with: python -m unittest -v"""
import random
import unittest
from closest import closest_pair, closest_pair_brute


class ClosestPairTests(unittest.TestCase):
    def check_case(self, points, expected=None):
        actual = closest_pair(points)
        self.assertEqual(actual, closest_pair_brute(points))
        if expected is not None:
            self.assertEqual(actual, expected)

    def test_500_random_inputs(self):
        rng = random.Random(302)
        for case in range(500):
            with self.subTest(case=case):
                self.check_case([(rng.randint(-100, 100), rng.randint(-100, 100))
                                 for _ in range(rng.randint(2, 50))])

    def test_exactly_two(self):
        self.check_case([(0, 0), (3, 4)], (5.0, 0, 1))

    def test_duplicates(self):
        self.check_case([(8, 9), (2, 3), (8, 9), (2, 3), (8, 9)], (0.0, 0, 2))

    def test_vertical_line(self):
        self.check_case([(4, y) for y in [20, 0, 10, 11, 30, 50]], (1.0, 2, 3))

    def test_pair_across_split(self):
        self.check_case([(-20, 0), (-10, 10), (-1, 0), (1, 0), (10, 10), (20, 0)],
                        (2.0, 2, 3))


if __name__ == '__main__':
    unittest.main()
