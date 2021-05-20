"""
@author: Kevin Costello
"""
from typing import List

some_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def factorial(n: int) -> int:
    """
    Recursively computes the value of n!

    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    """
    if n in (1, 0):
        return 1
    return n * factorial(n - 1)


def binomial(n: int, m: int) -> int:
    """
    Returns the binomial n choose m

    >>> binomial(4, 1)
    4
    >>> binomial(5, 2)
    10
    >>> binomial(11, 5)
    462
    """
    return int(factorial(n) / (factorial(n - m) * factorial(m)))


def totient(n: int) -> int:
    """
    Returns the euler totient function of an integer. This is the number of integers less or equal to n that are
    relatively prime to n, or equivalently the order of the multiplicative group (Z/nZ)^*

    >>> totient(5)
    4
    >>> totient(4)
    2
    >>> totient(11)
    10
    >>> totient(12)
    4
    """
    assert n < 102
    value = n
    for p in some_primes:
        if p > n:
            break
        if n % p == 0:
            value *= (1 - 1/p)
    return int(value)


def G(n: int, d: int, memo={}) -> List[List[int]]:
    """
    Given an integers n and d, returns the set of vectors G(n, d), which is defined to be the vectors of (Z/nZ)^d such
    that no collection of the entries sums to zero.

    >>> G(2, 1)
    [[1]]
    >>> G(4, 2)
    [[1, 1], [2, 1], [1, 2], [3, 2], [2, 3], [3, 3]]
    >>> G(5, 3)[:9]
    [[1, 1, 1], [2, 1, 1], [1, 2, 1], [3, 3, 1], [1, 1, 2], [2, 2, 2], [4, 2, 2], [2, 4, 2], [3, 1, 3]]
    >>> G(5, 3)[9:]
    [[1, 3, 3], [3, 3, 3], [4, 4, 3], [2, 2, 4], [4, 3, 4], [3, 4, 4], [4, 4, 4]]
    """
    if (n, d) in memo:
        return memo[(n, d)]
    if d == 1:
        return [[i] for i in range(1, n)]
    d_grams = []
    for i in range(1, n):
        # recursively look through past solutions for d - 1
        for solution in G(n, d - 1):
            is_solution = True
            sublists = [[i]]
            # check if all coordinate sums with new entry are nonzero
            for j in range(len(solution)):
                orig = sublists[:]
                new = solution[j]
                # if any sums of the sublists are divisible by n, stop checking
                for k in range(len(sublists)):
                    if sum(sublists[k] + [new]) % n == 0:
                        is_solution = False
                        break
                    sublists[k] = sublists[k] + [new]
                if not is_solution:
                    break
                sublists = orig + sublists
            # if is_solution is still True, then all of the coordinate sums are nonzero
            if is_solution:
                d_grams.append(solution + [i])
    memo[(n, d)] = d_grams
    return d_grams


def _g_2(n: int) -> int:
    """
    Returns |G(n, 2)|

    >>> _g_2(1)
    0
    >>> _g_2(4)
    6
    >>> all([_g_2(n) == len(G(n, 2)) for n in range(2, 25)])
    True
    """
    if n <= 1:
        return 0
    elif n > 1:
        return n**2 - 3*n + 2


def _g_3(n: int) -> int:
    """
    Returns |G(n, 3)|

    >>> [_g_3(n) for n in range(0, 4)]
    [0, 0, 0, 0]
    >>> all([_g_3(n) == len(G(n, 3)) for n in range(4, 21, 2)])
    True
    >>> all([_g_3(n) == len(G(n, 3)) for n in range(5, 22, 2)])
    True
    """
    if n <= 2:
        return 0
    elif n % 2 == 1:
        return n**3 - 7*n**2 + 15*n - 9
    elif n % 2 == 0:
        return n**3 - 7*n**2 + 15*n - 10


def _g_4(n: int) -> int:
    """
    Returns |G(n, 4)|

    >>> [_g_4(n) for n in range(0, 5)]
    [0, 0, 0, 0, 0]
    >>> all([_g_4(n) == len(G(n, 4)) for n in range(4, 17, 6)])
    True
    >>> all([_g_4(n) == len(G(n, 4)) for n in range(5, 18, 6)])
    True
    >>> all([_g_4(n) == len(G(n, 4)) for n in range(6, 19, 6)])
    True
    >>> all([_g_4(n) == len(G(n, 4)) for n in range(7, 20, 6)])
    True
    >>> all([_g_4(n) == len(G(n, 4)) for n in range(8, 21, 6)])
    True
    >>> all([_g_4(n) == len(G(n, 4)) for n in range(9, 22, 6)])
    True
    """
    if n <= 3:
        return 0
    elif n % 6 == 0:
        return n**4 - 15*n**3 + 80*n**2 - 180*n + 154
    elif n % 6 in (2, 4):
        return n**4 - 15*n**3 + 80*n**2 - 180*n + 144
    elif n % 6 == 3:
        return n**4 - 15*n**3 + 80*n**2 - 170*n + 114
    elif n % 6 in (1, 5):
        return n**4 - 15*n**3 + 80*n**2 - 170*n + 104


def order_of_G(n: int, d: int) -> int:
    if d == 2:
        return _g_2(n)
    if d == 3:
        return _g_3(n)
    elif d == 4:
        return _g_4(n)
    elif n > 1 and d == (n - 1):
        return totient(n)
    elif n >= 4 and d == (n - 2):
        return (n - 1) * totient(n)
    elif n >= 7 and d == (n - 3):
        return binomial(n - 1, 2) * totient(n)
    else:
        return len(G(n, d))


if __name__ == '__main__':
    import doctest
    doctest.testmod()