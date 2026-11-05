"""Hall booking algorithms. Chosen indices refer to the original input.

Requests have start < finish and nonnegative fees. Events may be back-to-back.
"""
from bisect import bisect_right


def greedy_earliest_finish(requests):
    """Accept compatible requests in ascending finish-time order."""
    order = sorted(range(len(requests)), key=lambda i: (requests[i][1], i))
    chosen = []
    total = 0
    last_finish = float('-inf')
    for i in order:
        start, finish, fee = requests[i]
        if start >= last_finish:
            chosen.append(i)
            total += fee
            last_finish = finish
    return total, chosen


def greedy_highest_fee(requests):
    """Accept requests by descending fee if they fit all accepted events."""
    order = sorted(range(len(requests)), key=lambda i: (-requests[i][2], i))
    chosen = []
    total = 0
    for i in order:
        start, finish, fee = requests[i]
        if all(finish <= requests[j][0] or requests[j][1] <= start
               for j in chosen):
            chosen.append(i)
            total += fee
    chosen.sort(key=lambda i: (requests[i][0], requests[i][1], i))
    return total, chosen


def best_schedule(requests):
    """Weighted interval scheduling using DP and binary-search predecessors."""
    order = sorted(range(len(requests)), key=lambda i: (requests[i][1], i))
    finishes = [requests[i][1] for i in order]
    n = len(order)
    # p[j] is the last compatible position before position j, or -1.
    p = [bisect_right(finishes, requests[i][0], 0, j) - 1
         for j, i in enumerate(order)]
    # opt[k] is the best total using the first k finish-sorted requests.
    opt = [0] * (n + 1)
    for j, i in enumerate(order):
        include = requests[i][2] + opt[p[j] + 1]
        opt[j + 1] = max(opt[j], include)

    chosen = []
    k = n
    while k > 0:
        j = k - 1
        i = order[j]
        if requests[i][2] + opt[p[j] + 1] > opt[k - 1]:
            chosen.append(i)
            k = p[j] + 1
        else:
            k -= 1
    chosen.reverse()
    return opt[n], chosen


def brute_force(requests):
    """Try every subset; intended only for n <= 15."""
    n = len(requests)
    if n > 15:
        raise ValueError('Brute force is limited to 15 requests')
    order = sorted(range(n), key=lambda i: (requests[i][1], i))
    best_total, best_chosen = 0, []
    for mask in range(1 << n):
        chosen = []
        total = 0
        last_finish = float('-inf')
        for i in order:
            if mask & (1 << i):
                start, finish, fee = requests[i]
                if start < last_finish:
                    break
                chosen.append(i)
                total += fee
                last_finish = finish
        else:
            if total > best_total:
                best_total, best_chosen = total, chosen
    return best_total, best_chosen
