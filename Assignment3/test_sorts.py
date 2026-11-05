"""Run from Assignment3 with: python -B -m unittest -v"""
import random
import unittest
from itertools import permutations

from sorts import quicksort_basic, quicksort_improved


class SortTests(unittest.TestCase):
    def check_sorts(self, values):
        expected = sorted(values)
        for function in (quicksort_basic, quicksort_improved):
            with self.subTest(function=function.__name__, values=values):
                a = values.copy()
                self.assertIsNone(function(a))
                self.assertEqual(a, expected)

    def test_500_random_lists(self):
        rng = random.Random(302)
        random.seed(303)
        for _ in range(500):
            self.check_sorts([rng.randint(-1000, 1000)
                              for _ in range(rng.randint(0, 200))])

    def test_empty(self):
        self.check_sorts([])

    def test_500_brute_force_checks(self):
        rng = random.Random(307)
        for case in range(500):
            values = [rng.randint(-5, 5) for _ in range(rng.randint(0, 7))]
            # Exhaustively search permutations for an ascending arrangement.
            expected = next(list(p) for p in permutations(values)
                            if all(p[i] <= p[i + 1] for i in range(len(p) - 1)))
            for function in (quicksort_basic, quicksort_improved):
                with self.subTest(case=case, function=function.__name__):
                    actual = values.copy()
                    function(actual)
                    self.assertEqual(actual, expected)

    def test_one_element(self):
        self.check_sorts([7])

    def test_all_equal(self):
        self.check_sorts([100] * 100)

    def test_already_sorted(self):
        self.check_sorts(list(range(100)))

    def test_reverse_sorted(self):
        self.check_sorts(list(range(100, 0, -1)))

    def test_negative_numbers(self):
        self.check_sorts([-9, -1, -20, -1, 0, -5])


if __name__ == '__main__':
    unittest.main()
