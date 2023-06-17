import matplotlib.pyplot as plt
import csv


class Point:
    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return (self.x, self.y) != (other.x, other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __le__(self, other):
        return (self.x, self.y) <= (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)

    def __ge__(self, other):
        return (self.x, self.y) >= (other.x, other.y)

    @staticmethod
    def print_points(points):
        print("Points:\t", end="")
        for p in points:
            print(p.name + " ", end="")
        print()

    @staticmethod
    def read_points(file_name):
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            result = []
            for row in reader:
                result.append(Point(int(row[0]), int(row[1])))
            return result

    @staticmethod
    def draw_points(points):
        x, y = [p.x for p in points], [p.y for p in points]
        plt.scatter(x, y, marker="o", s=240, fc="orange")
        for p in points:
            plt.annotate(text=p.name, xy=(p.x, p.y), xytext=(0, 0),
                         textcoords="offset points", ha="center", va="center",
                         color="white", weight="heavy")

    @staticmethod
    def draw_region(points_region):
        x, y = [p.x for p in points_region], [p.y for p in points_region]
        x = [x[0], x[0], x[1], x[1], x[0]]
        y = [y[0], y[1], y[1], y[0], y[0]]
        plt.plot(x, y, color="green")
        plt.fill(x, y, color="green", alpha=0.2)


class Interval:
    def __init__(self, begin, end, points=None):
        self.points = points
        self.begin = begin
        self.end = end
        self.left = None
        self.right = None

    def __eq__(self, other):
        return (self.begin, self.end, self.points) == (other.begin, other.end, self.points)

    def __ne__(self, other):
        return (self.begin, self.end, self.points) != (other.begin, other.end, self.points)

    def y_search(self, region_y):
        # Getting slice from points in interval
        result = []
        for i, p in enumerate(self.points):
            if region_y[0] <= p.y <= region_y[1]:
                result.append(p)
            elif p.y > region_y[1]:
                break

        return result

    def intervals_search(self, region_x):
        if self.begin >= region_x[0] and self.end <= region_x[1]:
            return [self]

        m = (self.begin + self.end) // 2
        intervals = []
        if region_x[1] > m:
            intervals += self.right.intervals_search(region_x)
        if region_x[0] < m:
            intervals += self.left.intervals_search(region_x)
        return intervals

    def region_search(self, region_x, region_y):
        # Search by x
        intervals = self.intervals_search(region_x)

        # Search by y
        result_points = set()
        for interval in intervals:
            result_points = result_points.union(set(interval.y_search(region_y)))
        return result_points

    @staticmethod
    def make_interval(begin, end, points):
        interval = Interval(begin, end)
        interval.points = [p for ps in points for p in ps]
        interval.points.sort(key=lambda point: point.y)

        if end - begin != 1:
            m = (begin + end) // 2
            interval.left = Interval.make_interval(begin, m, points[:(m + 1 - begin)])
            interval.right = Interval.make_interval(m, end, points[(m - begin):])

        return interval


def init_points(points):
    points.sort()  # Sort by (x, y)
    counter = -1
    indexed_points = []
    prev_x = None
    for i in range(len(points)):
        points[i].name = chr(65 + i)
        if prev_x != points[i].x:
            indexed_points.append(list())
            counter += 1
        indexed_points[counter].append(points[i])
        prev_x = points[i].x
    return indexed_points  # return list of lists


def find_interval(indexed_points, x1, x2):
    left_x, right_x = -1, -1
    for i, ps in enumerate(indexed_points):
        if left_x == -1 and x1 <= ps[0].x:
            left_x = i
        if x2 < ps[0].x:
            right_x = i - 1
            break
    if right_x == -1:
        right_x = len(indexed_points) - 1

    # Interval too small
    if left_x == -1 or left_x > right_x:
        return [-1, -1]

    return [left_x, right_x]


def tree_region_method(indexed_points, points_region, interval=None):
    if interval is None:
        interval = Interval.make_interval(0, len(indexed_points) - 1, indexed_points)
    x_indexed = find_interval(indexed_points, points_region[0].x, points_region[1].x)

    if x_indexed[0] == -1:
        return set()
    elif x_indexed[0] == x_indexed[1]:
        return {indexed_points[x_indexed[0]]}
    else:
        return interval.region_search(x_indexed, [points_region[0].y, points_region[1].y])


def main():
    # Read data from file
    points = Point.read_points("points.txt")
    indexed_points = init_points(points)
    points_region = Point.read_points("region.txt")

    # Algorithm
    interval = Interval.make_interval(0, len(indexed_points) - 1, indexed_points)
    x_indexed = find_interval(indexed_points, points_region[0].x, points_region[1].x)

    if x_indexed[0] == -1:
        print("Interval too small or out of range")
    elif x_indexed[0] == x_indexed[1]:
        Point.print_points(indexed_points[x_indexed[0]])
    else:
        result_points = interval.region_search(x_indexed, [points_region[0].y, points_region[1].y])

        # Print result
        Point.print_points(result_points)

    # Drawing
    Point.draw_region(points_region)
    Point.draw_points(points)
    plt.title("Lab4")
    plt.show()


if __name__ == '__main__':
    main()
