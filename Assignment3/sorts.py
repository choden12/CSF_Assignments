"""In-place quicksort implementations. Both functions return None."""
import random


def quicksort_basic(a):
    """Lomuto partition with the last element as pivot."""
    def partition(lo, hi):
        pivot = a[hi]
        boundary = lo
        for j in range(lo, hi):
            if a[j] <= pivot:
                a[boundary], a[j] = a[j], a[boundary]
                boundary += 1
        a[boundary], a[hi] = a[hi], a[boundary]
        return boundary

    def sort(lo, hi):
        if lo < hi:
            pivot_index = partition(lo, hi)
            sort(lo, pivot_index - 1)
            sort(pivot_index + 1, hi)

    sort(0, len(a) - 1)


def quicksort_improved(a, cutoff=16):
    """Random pivot, insertion-sort cutoff, and O(log n) recursion depth.

    Three-way partitioning groups equal values so repeated amounts do not
    repeatedly enter recursive calls.
    """
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")

    def insertion_sort(lo, hi):
        for i in range(lo + 1, hi + 1):
            value = a[i]
            j = i - 1
            while j >= lo and a[j] > value:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = value

    def sort(lo, hi):
        while lo < hi:
            if hi - lo + 1 <= cutoff:
                insertion_sort(lo, hi)
                return

            pivot = a[random.randrange(lo, hi + 1)]
            # [lo, lt) < pivot; [lt, i) == pivot; (gt, hi] > pivot.
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1

            # Recurse on the smaller unequal part; loop over the larger.
            if lt - lo < hi - gt:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(a) - 1)
