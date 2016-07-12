"""This module provides utilities for generating tracker unit tests"""
if __name__ == '__main__':
    import sys, os
    basepath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(basepath, '..', 'src')
    sys.path.append(path)
    from rolling_median import main

from mediantracker import MedianTracker

def generate_mediantracker(degree_list):
    """methods that returns a mediantracker from a list of degrees"""
    if len(degree_list)%2 == 0 :
        median_indexes = set([len(degree_list)/2, len(degree_list)/2 - 1])
    else:
        median_indexes = set([len(degree_list)/2])
    prev = (0, 0)
    linked_list = {
        prev: {}
    }
    degrees = {}
    medians = []
    for i, d in enumerate(degree_list):
        if prev[0] == d:
            new = (prev[0], prev[1] + 1)
        else:
            degrees[prev[0]] = prev[1] + 1
            new = (d, 0)
        linked_list[new] = {
            'below': prev
        }
        linked_list[prev]['above'] = new
        if i in median_indexes:
            medians.append(new)
        prev = new
    degrees[prev[0]] = prev[1] + 1
    last = (float('inf'), 0)
    linked_list[last] = {
        'below': prev
    }
    linked_list[prev]['above'] = last
    tracker = MedianTracker()
    tracker.degrees = degrees
    tracker.nodes_linked_list = linked_list
    tracker.medians = tuple(medians)
    return tracker

def exec_simple_test(test):
    degree_list = test[0]
    update = test[1]
    expected_medians = test[2]
    tracker = generate_mediantracker(degree_list)
    tracker.receive(update)
    assert expected_medians == tracker.medians, '{} != {}'.format(
        tracker.medians, expected_medians
    )

# initial tracker state
initial = MedianTracker()

# degree list has a odd number of elements, the median is the element in the middle.
_single_median_degrees_0 = [1, 1, 2, 3, 5, 7, 9]
_single_median_tracker_0 = generate_mediantracker(_single_median_degrees_0)
assert _single_median_tracker_0.medians == ((3,0), )

_single_median_degrees_1 = [2, 2, 2, 3, 5, 7, 7, 11, 11]
_single_median_tracker_1 = generate_mediantracker(_single_median_degrees_1)
assert _single_median_tracker_1.medians == ((5, 0), )
# degree list has an even number of elements, there are two median elements with the same value
_two_equal_medians_degrees_0 = [1, 1, 2, 3, 3, 5, 7, 9]
_two_equal_medians_tracker_0 = generate_mediantracker(_two_equal_medians_degrees_0)
assert _two_equal_medians_tracker_0.medians == ((3, 0), (3, 1))

_two_equal_medians_degrees_1 = [2, 2, 2, 3, 5, 5, 7, 7, 11, 11]
_two_equal_medians_tracker_1 = generate_mediantracker(_two_equal_medians_degrees_1)
assert _two_equal_medians_tracker_1.medians == ((5, 0), (5, 1))
# degree list has an even number of elements, there are two median elements with different values
_two_medians_degrees_0 = [1, 1, 2, 3, 5, 7, 7, 9]
_two_medians_tracker_0 = generate_mediantracker(_two_medians_degrees_0)
assert _two_medians_tracker_0.medians == ((3, 0), (5, 0))

_two_medians_degrees_1 = [2, 2, 2, 3, 5, 6, 7, 7, 11, 11]
_two_medians_tracker_1 = generate_mediantracker(_two_medians_degrees_1)
assert _two_medians_tracker_1.medians == ((5, 0), (6, 0))

class SimpleMedianTracker(MedianTracker):
    """This implementation of the median tracker stores the list of degrees
    in a list instead of the linked list in the original implementation.
    There is no need to track the median as it is computed from the middle
    element(s) in this list.
    """

    def __init__(self):
        self.degree_list = []
        self.degrees = {}
        self._receive_decrease = self._receive_increase

    def receive(self, update):
        # print self.degree_list, update
        super(SimpleMedianTracker, self).receive(update)

    def _receive_new(self):
        self.degree_list.insert(0, 1)
        self.degrees[1] = self.degrees.get(1, 0) + 1

    def _receive_obsolete(self, degree):
        self.degrees[degree] -= 1
        if self.degrees[degree] == 0:
            self.degrees.pop(degree)
        self.degree_list.remove(degree)

    def _receive_increase(self, update):
        degree_before, degree_after = update
        self.degrees[degree_before] -= 1
        if self.degrees[degree_before] == 0:
            self.degrees.pop(degree_before)
        self.degree_list.remove(degree_before)
        self.degrees[degree_after] = self.degrees.get(degree_after, 0) + 1
        for i, d in enumerate(self.degree_list):
            if d >= degree_after:
                self.degree_list.insert(i, degree_after)
                break
        else:
            self.degree_list.insert(i + 1, degree_after)

    def median(self):
        m = len(self.degree_list)/2
        if len(self.degree_list)%2 == 0:
            return (self.degree_list[m - 1] + self.degree_list[m])/2.0
        else:
            return self.degree_list[m]


if __name__ == '__main__':
    if len(sys.argv) == 2:
        debug = (sys.argv[1] == 'debug')
    else:
        debug = False
    main(sys.stdin, sys.stdout, debug, SimpleMedianTracker)
