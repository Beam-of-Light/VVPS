import unittest

from lab import *


class TestLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        points = Point.read_points("test_points.txt")
        cls.indexed_points = init_points(points)
        cls.interval = Interval.make_interval(0, len(cls.indexed_points) - 1, cls.indexed_points)

        cls.region1 = [Point(2, 1), Point(8, 7)]  # region contains some points
        cls.region2 = [Point(2, 1), Point(4, 4)]  # region contains 1 point
        cls.region3 = [Point(2, 1), Point(4, 2)]  # empty result
        cls.region4 = [Point(2, 1), Point(2, 1)]  # empty result

    def test_tree_region_method(self):
        result = tree_region_method(self.indexed_points, self.region1)
        self.assertEqual(result, {Point(6, 2), Point(3, 3), Point(7, 5), Point(4, 6)})

        result = tree_region_method(self.indexed_points, self.region2)
        self.assertEqual(result, {Point(3, 3)})

        result = tree_region_method(self.indexed_points, self.region3)
        self.assertEqual(result, set())

        result = tree_region_method(self.indexed_points, self.region4)
        self.assertEqual(result, set())

    def test_find_interval(self):
        result = find_interval(self.indexed_points, self.region1[0].x, self.region1[1].x)
        self.assertEqual(result, [1, 5])

        result = find_interval(self.indexed_points, self.region2[0].x, self.region2[1].x)
        self.assertEqual(result, [1, 2])

        result = find_interval(self.indexed_points, self.region3[0].x, self.region3[1].x)
        self.assertEqual(result, [1, 2])

        result = find_interval(self.indexed_points, self.region4[0].x, self.region4[1].x)
        self.assertEqual(result, [-1, -1])

    def test_make_interval(self):
        self.assertEqual(self.interval, Interval(0, 8, self.indexed_points))
        self.assertEqual(self.interval.left.left.left, Interval(0, 1, [(3, 3), (1, 5)]))
        self.assertEqual(self.interval.left.left.left.left, None)


if __name__ == '__main__':
    unittest.main()
