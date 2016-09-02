"""Generate random poins."""
import collections
import logging
import random
import sys
import threading
import optparse


def generate_points(polygon, offset_y, number=10, dist_min=None):
    """Generate random points in specific polygon.

    Parameters:
        - polygon - List of tuple points ((x, y), ...).
        - offset_y - Offset by y-axis.
        - number - Count of needed point.
        - dist_min - Min distance value beetwen two points.

    Return:
        list of Points
    """
    log = logging.getLogger('generate_points')
    log.info('Start generating random points for polygon: %s, '
             'offset_y: %s, number of point: %s, dist_min: %s.',
             polygon, offset_y, number, dist_min)

    Point = collections.namedtuple('Point', 'x y z')
    points = []
    min_value = min([min(x) for x in polygon])
    max_value = max([max(x) for x in polygon])

    while len(points) < number:
        point = Point(random.uniform(min_value, max_value),
                      offset_y,
                      random.uniform(min_value, max_value))
        if is_point_inside_polygon(point, polygon) and point not in points:
            if dist_min and not is_right_distance(point, points, dist_min):
                continue
            points.append(point)

    log.info('Process of generating random points is finished successfully. '
             'polygon: %s, offset_y: %s, number of point: %s, dist_min: %s.',
             polygon, offset_y, number, dist_min)

    return points


def get_distance(point_a, point_b):
    """Calculate and return distance value beetwen two points."""
    return ((point_a.x - point_b.x)**2 + (point_a.z - point_b.z)**2)**.5


def process_point(points, result):
    """Worker for calculating distance beetwen two points.

    Parameters:
        - points - List of Points
        - result - Empty list. This list will be used
                   for collecting of distances.
    """
    while points:
        try:
            point_a, point_b = points.pop()
        except IndexError:
            break

        result.append(get_distance(point_a, point_b))


def is_right_distance(point, points, distance):
    """Check if point is created on the correct distance.

    Parameters:
        - point - Point object.
        - points - list of Point objects.
        - distance - Distance value beetwen two points.

    Return:
        boolien value
    """

    points = [(point, x) for x in points]
    result = []
    threads = []
    for i in range(5):
        thr = threading.Thread(target=process_point,
                               name='worker-%d' % i,
                               args=(points, result))
        threads.append(thr)
        thr.start()

    for thr in threads:
        thr.join()

    return bool([x for x in result if x >= distance]) if points else True


def is_point_inside_polygon(point, polygon):
    """Check if point inside polygon.

    Parameters:
        - point - Point object
        - polygon - list of tuple points

    Return:
        boolien value
    """
    inside = False
    p1x, p1y = polygon[0]
    for i in range(len(polygon) + 1):
        p2x, p2y = polygon[i % len(polygon)]
        if point.z > min(p1y, p2y):
            if point.z <= max(p1y, p2y):
                if point.x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = \
                            (point.z - p1y) * (p2x - p1x)/(p2y - p1y) + p1x
                    if p1x == p2x or point.x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def main():
    """ Do job. """
    parser = optparse.OptionParser('usage: %prog [options]')
    parser.add_option('-v', '--verbosity', action='store', dest='verbosity',
                      type=int, default=1, help='Verbosity level [0-3]')
    (options, args) = parser.parse_args()

    log_level = logging.ERROR
    if options.verbosity == 1:
        log_level = logging.INFO
    elif options.verbosity >= 2:
        log_level = logging.DEBUG

    _logger = logging.getLogger('generate_point')
    _logger.setLevel(log_level)
    points = generate_points(((0, 0), (10, 0), (0, 10), (10, 10)), 0, 10, 2)
    import kdtree
    import pdb; pdb.set_trace()
    tree = kdtree.create(points)
    kdtree.visualize(tree)


if __name__ == '__main__':
    sys.exit(main())
