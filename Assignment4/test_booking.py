"""Run from Assignment4: python -B -m unittest -v"""
import random
import unittest

from booking import (best_schedule, brute_force, greedy_earliest_finish,
                     greedy_highest_fee)


class BookingTests(unittest.TestCase):
    def check_result(self, requests, result):
        total, chosen = result
        self.assertEqual(len(chosen), len(set(chosen)))
        self.assertTrue(all(0 <= i < len(requests) for i in chosen))
        self.assertEqual(total, sum(requests[i][2] for i in chosen))
        for position, i in enumerate(chosen):
            for j in chosen[position + 1:]:
                self.assertTrue(requests[i][1] <= requests[j][0]
                                or requests[j][1] <= requests[i][0])

    def check_case(self, requests, expected):
        for function in (greedy_earliest_finish, greedy_highest_fee,
                         best_schedule, brute_force):
            with self.subTest(function=function.__name__):
                result = function(requests)
                self.check_result(requests, result)
                self.assertEqual(result[0], expected)

    def test_500_random_inputs(self):
        rng = random.Random(304)
        for case in range(500):
            requests = []
            for _ in range(rng.randint(0, 10)):
                start = rng.randint(0, 20)
                requests.append((start, start + rng.randint(1, 10), rng.randint(1, 100)))
            with self.subTest(case=case):
                dp, brute = best_schedule(requests), brute_force(requests)
                self.check_result(requests, dp)
                self.check_result(requests, brute)
                self.assertEqual(dp[0], brute[0])
                for function in (greedy_earliest_finish, greedy_highest_fee):
                    result = function(requests)
                    self.check_result(requests, result)
                    self.assertLessEqual(result[0], brute[0])

    def test_no_requests(self):
        self.check_case([], 0)

    def test_one_request(self):
        self.check_case([(9, 12, 3000)], 3000)

    def test_all_overlapping(self):
        self.check_case([(9, 12, 3000), (10, 14, 2000), (11, 15, 1000)], 3000)

    def test_none_overlapping(self):
        self.check_case([(15, 16, 300), (9, 10, 100), (12, 13, 200)], 600)

    def test_back_to_back(self):
        self.check_case([(9, 12, 3000), (12, 14, 2500), (14, 16, 2000)], 7500)

    def test_equal_fees(self):
        rng = random.Random(305)
        for case in range(500):
            requests = []
            fee = rng.randint(1, 100)
            for _ in range(rng.randint(0, 10)):
                start = rng.randint(0, 20)
                requests.append((start, start + rng.randint(1, 10), fee))
            with self.subTest(case=case):
                greedy = greedy_earliest_finish(requests)
                self.check_result(requests, greedy)
                self.assertEqual(greedy[0], brute_force(requests)[0])


if __name__ == '__main__':
    unittest.main()
