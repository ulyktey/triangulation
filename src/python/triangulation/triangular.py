"""Generate triangulars form random points (kdtree)."""
import logging
import sys
import optparse
import kdtree

from triangulation import point as pt


def get_triangular(kd_tree, point):
    """Get three point from kdtree object.

    Parameters:
        - kd_tree - Kdtree object with points
        - point - point.
    Return:
        List with three points(triangular) or []
    """
    points = kd_tree.search_knn(point, 3)
    return points if len(points) == 3 else []


def generate_triangulars(kd_tree, triangulars):
    """Generate triangulars.

    Parameters:
        - kd_tree - Kdtree object with points
        - children - Node of kdtree.
        - triangulars - List with triangulars
    """
    points = get_triangular(kd_tree, kd_tree.data)
    if points:
        triangulars.append(points)

    for children in kd_tree.children:
        generate_triangulars(children[0], triangulars)


def main():
    """ Do job. """
    parser = optparse.OptionParser('usage: %prog [options]')
    parser.add_option('-v', '--verbosity', action='store', dest='verbosity',
                      type=int, default=1, help='Verbosity level [0-3]')
    (options, _) = parser.parse_args()

    log_level = logging.ERROR
    if options.verbosity == 1:
        log_level = logging.INFO
    elif options.verbosity >= 2:
        log_level = logging.DEBUG

    _logger = logging.getLogger('generate_triangulars')
    _logger.setLevel(log_level)

    points = pt.generate_points(((0, 0), (10, 0), (0, 10), (10, 10)), 0, 10, 2)
    tree = kdtree.create(points)
    kdtree.visualize(tree)
    triangulars = []
    generate_triangulars(tree, triangulars)

    for point in triangulars:
        print point


if __name__ == '__main__':
    sys.exit(main())
