from typing import List
from sys import stderr

def debug(*args):
    """
    Use this function to print debug info
    without affecting the autograder
    """
    print(*args, file=stderr)
def split_by_x(points):
    """Partitions an array of points into two by x-coordinate. All points with
    the same x-coordinate should remain on the same side of the partition. All
    points in the right partition should have strictly greater x-coordinates
    than all points in the left partition.

    >>> split_by_x([(0, 0), (1, 0), (1, 1), (3, 1), (2, 1), (3, 2)])
    ([(0, 0), (1, 0), (1, 1)], [(2, 1), (3, 1), (3, 2)])
    >>> split_by_x([(0, 0), (0, 1), (0, -1), (0, -2)])
    ([(0, 0), (0, 1), (0, -1), (0, -2)], [])
    >>> split_by_x([(0, 0), (0, 1), (0, -1), (0, -2), (2, 1)])
    ([(0, 0), (0, 1), (0, -1), (0, -2)], [(2, 1)])
    >>> split_by_x([(0, 0),(1, 0),(1, 1),(1, 2),(1, 3)])
    ([(0, 0)], [(1, 0), (1, 1), (1, 2), (1, 3)])
    >>> split_by_x([(0, 0), (1, 1), (1, 2)])
    ([(0, 0)], [(1, 1), (1, 2)])
    """
    from collections import defaultdict

    assert len(points) > 0

    points_by_x = defaultdict(list)
    for p in points:
        points_by_x[p[0]].append(p)
    halfway = len(points) // 2
    xs = list(sorted(points_by_x))

    right_idx = 0
    right_num_points = 0
    for idx, x in enumerate(xs):
        ps = points_by_x[x]
        right_num_points += len(ps)
        if right_num_points > halfway:
            right_idx = idx + 1
            break

    left_idx = right_idx - 1
    left_num_points = right_num_points
    left_num_points -= len(points_by_x[xs[left_idx]])

    left_badness = abs(halfway - left_num_points)
    right_badness = abs(halfway - right_num_points)
    if left_badness < right_badness:
        cut_idx = left_idx
    elif left_badness >= right_badness:
        # If equally bad, cut at the right point. This means that if one of
        # the returned arrays is empty, it will always be the right array.
        cut_idx = right_idx

    def collect_points(points_by_x, xs):
        result = []
        for x in xs:
            result.extend(points_by_x[x])
        return result

    return (
        collect_points(points_by_x, xs[:cut_idx]),
        collect_points(points_by_x, xs[cut_idx:]),
    )


def solution(points: List[List[int]]) -> List[int]:
    ind = {}
    res = []
    for i in range(0, len(points)):
        ind[tuple(points[i])] = i+1
    s = dict(sorted(ind.items()))
    
    def finder(p):
        if len(p)==1:
            return p
        else:
            l, r = split_by_x(p)
            if r==[]:
                return l
            elif l==[]:
                return r
            else:
                l_p = finder(l)
                r_p = finder(r)
                y_current = float("-inf")
                for point in r_p:
                    if point[1]>y_current:
                        y_current = point[1]
                for point in l_p:
                    if point[1]>=y_current:
                        r_p.append(point)
                return r_p
    skey = list(s.keys())    
    optimal = finder(skey)
    for k in optimal:
        res.append(s[k])
    res.sort()
    return res


if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        points = []
        N = int(input())
        for _ in range(N):
            x, y = map(int, input().split())
            points.append([x, y])
        out = solution(points)
        print(" ".join(map(str, sorted(out))))
