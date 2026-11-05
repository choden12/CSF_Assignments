"""Closest pair of planar points; ties use the smallest original index pair."""
from math import sqrt


def closest_pair_brute(points):
    """Return (distance, i, j), i < j, in Theta(n**2) time."""
    if len(points) < 2:
        raise ValueError("At least two points are required")
    best = (float("inf"), 0, 1)
    for i in range(len(points) - 1):
        x, y = points[i]
        for j in range(i + 1, len(points)):
            dx, dy = x - points[j][0], y - points[j][1]
            candidate = (dx * dx + dy * dy, i, j)
            if candidate < best:
                best = candidate
    return sqrt(best[0]), best[1], best[2]


def closest_pair(points):
    """Return (distance, i, j) in O(n log n) time and O(n) auxiliary space.

    Coordinates must be finite real numbers. Input order is never changed.
    Squared distances avoid square roots until the final result.
    """
    if len(points) < 2:
        raise ValueError("At least two points are required")
    px = sorted((x, y, i) for i, (x, y) in enumerate(points))

    # Handle coincidences first: a zero-width strip can contain arbitrarily
    # many duplicates, invalidating the usual constant-neighbour argument.
    duplicate = None
    for a, b in zip(px, px[1:]):
        if a[:2] == b[:2]:
            candidate = (0, min(a[2], b[2]), max(a[2], b[2]))
            if duplicate is None or candidate < duplicate:
                duplicate = candidate
    if duplicate is not None:
        return 0.0, duplicate[1], duplicate[2]

    py = sorted(px, key=lambda p: (p[1], p[0], p[2]))

    def candidate(a, b):
        dx, dy = a[0] - b[0], a[1] - b[1]
        return dx * dx + dy * dy, min(a[2], b[2]), max(a[2], b[2])

    def solve(xs, ys):
        if len(xs) <= 3:
            return min(candidate(xs[i], xs[j])
                       for i in range(len(xs)) for j in range(i + 1, len(xs)))
        middle = len(xs) // 2
        left, right = xs[:middle], xs[middle:]
        split_x = right[0][0]
        left_ids = {p[2] for p in left}
        ly, ry = [], []
        for p in ys:
            (ly if p[2] in left_ids else ry).append(p)
        best = min(solve(left, ly), solve(right, ry))
        strip = [p for p in ys if (p[0] - split_x) ** 2 <= best[0]]
        for i, a in enumerate(strip):
            # Packing bounds the number of points within delta in y by a
            # constant. Inclusive comparisons also examine equal-distance ties.
            for j in range(i + 1, len(strip)):
                b = strip[j]
                if (b[1] - a[1]) ** 2 > best[0]:
                    break
                best = min(best, candidate(a, b))
        return best

    best = solve(px, py)
    return sqrt(best[0]), best[1], best[2]
