"""Tests for the MedianTracker operations.
For the different types of updates a significant range of cases has been tested.
"""
import tracker_util

def test_compute_median():
    """test correct computation of the median
    """
    tracker = tracker_util.generate_mediantracker([1, 2, 3])
    assert tracker.median() == 2, '{} != {}'.format(
        tracker.median(), 2
    )
    tracker = tracker_util.generate_mediantracker([1, 2, 3, 5])
    assert tracker.median() == 2.5, '{} != {}'.format(
        tracker.median(), 2.5
    )

def test_receive_new_initial():
    """test the reception of a new node from the initial state.
    """
    tracker = tracker_util.initial
    tracker.receive((0, 1))
    assert tracker.medians == ((1, 0),), '{} != {}'.format(
        tracker.medians, ((1, 0),)
    )

def test_receive_new():
    """test when a new node is added to the data structure (possible only with degree 1)
    """
    degree_configuration_list = [
        #initial state,      update, expected_medians
        ([1],                (0, 1), ((1, 0), (1, 1))), # configuration after init
        ([1, 1, 3, 5, 9],    (0, 1), ((1, 2), (3, 0))), # from single median element (3,)
        ([1, 2, 3, 5, 5, 9], (0, 1), ((3, 0),)) # two median elements (3, 5)
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_obsolete_single_median():
    """test deletion of a node from the data structure when there is a single
    median in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,      update, expected_medians
        ([1, 1, 3, 5, 9],    (5, 0), ((1, 1), (3, 0))),
        ([1, 1, 3, 5, 9],    (3, 0), ((1, 1), (5, 0))),
        ([1, 1, 3, 5, 9],    (1, 0), ((3, 0), (5, 0)))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_obsolete_two_medians_same_value():
    """test deletion of a node from the data structure when there are two
    median elements with the same value in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,         update, expected_medians
        ([1, 1, 3, 3, 5, 9],    (5, 0), ((3, 0),)),
        ([1, 1, 3, 3, 5, 9],    (3, 0), ((3, 0),)),
        ([1, 1, 3, 3, 5, 9],    (1, 0), ((3, 1),))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test


def test_receive_obsolete_two_medians():
    """test deletion of a node from the data structure when there are two
    median elements in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,         update, expected_medians
        ([1, 1, 3, 5, 7, 9],    (7, 0), ((3, 0),)),
        ([1, 1, 3, 5, 7, 9],    (5, 0), ((3, 0),)),
        ([1, 1, 3, 5, 7, 9],    (3, 0), ((5, 0),)),
        ([1, 1, 3, 5, 7, 9],    (1, 0), ((5, 0),))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_increase_two_medians_same_value():
    """test a degree increase of a node when there are two
    median elements with the same value in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,         update, expected_medians
        ([1, 1, 3, 3, 5, 9],    (5, 6), ((3, 0), (3, 1))),
        ([1, 1, 3, 3, 5, 9],    (3, 4), ((3, 0), (4, 0))),
        ([1, 2, 3, 3, 5, 9],    (2, 3), ((3, 1), (3, 2))),
        ([1, 2, 3, 3, 5, 9],    (1, 2), ((3, 0), (3, 1)))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_increase_single_median():
    """test a degree increase of a node when there is a single median
    in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,      update, expected_medians
        ([1, 1, 3, 5, 9],    (5, 6), ((3, 0),)),
        ([1, 1, 3, 5, 9],    (3, 4), ((4, 0),)),
        ([1, 1, 3, 3, 9],    (3, 4), ((3, 0),)),
        ([1, 2, 3, 5, 9],    (2, 3), ((3, 1),)),
        ([1, 2, 3, 5, 9],    (1, 2), ((3, 0),)),
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_increase_two_median():
    """test a degree increase of a node when there are two median elements
    in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,         update, expected_medians
        ([1, 1, 3, 4, 5, 9],    (5, 6), ((3, 0), (4, 0))),
        ([1, 1, 3, 4, 4, 9],    (4, 5), ((3, 0), (4, 0))),
        ([1, 1, 2, 3, 6, 9],    (3, 4), ((2, 0), (4, 0))),
        ([1, 3, 3, 4, 7, 9],    (3, 4), ((4, 0), (4, 1))),
        ([1, 3, 3, 5, 7, 9],    (3, 4), ((4, 0), (5, 0))),
        ([1, 2, 3, 4, 5, 9],    (2, 3), ((3, 1), (4, 0)))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_decrease_single_median():
    """test a degree decrease of a node when there is a single median
    in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,      update, expected_medians
        ([1, 1, 3, 5, 9],    (5, 4), ((3, 0),)),
        ([1, 1, 3, 5, 9],    (5, 3), ((3, 0),)),
        ([1, 1, 3, 7, 9],    (7, 2), ((2, 0),)),
        ([4, 4, 5, 7, 9],    (5, 1), ((4, 1),)),
        ([1, 2, 5, 5, 9],    (5, 3), ((3, 0),))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_decrease_two_medians_same_value():
    """test a degree decrease of a node when there are two
    median elements with the same value in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,         update, expected_medians
        ([1, 1, 3, 3, 5, 9],    (5, 4), ((3, 0), (3, 1))),
        ([1, 1, 3, 3, 5, 9],    (5, 3), ((3, 0), (3, 1))),
        ([1, 1, 3, 3, 7, 9],    (7, 2), ((2, 0), (3, 0))),
        ([4, 4, 5, 5, 7, 9],    (5, 1), ((4, 1), (5, 0))),
        ([1, 2, 5, 5, 7, 9],    (5, 3), ((3, 0), (5, 0)))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test

def test_receive_decrease_two_median():
    """test a degree decrease of a node when there are two median elements
    in the starting configuration.
    """
    degree_configuration_list = [
        #initial state,         update, expected_medians
        ([1, 1, 3, 5, 7, 9],    (9, 6), ((3, 0), (5, 0))),
        ([1, 1, 3, 5, 7, 9],    (9, 4), ((3, 0), (4, 0))),
        ([1, 1, 3, 5, 7, 9],    (9, 3), ((3, 0), (3, 1))),
        ([1, 1, 3, 5, 7, 9],    (9, 2), ((2, 0), (3, 0))),
        ([1, 1, 3, 5, 7, 9],    (5, 4), ((3, 0), (4, 0))),
        ([1, 1, 3, 5, 7, 9],    (5, 3), ((3, 0), (3, 1))),
        ([1, 1, 3, 5, 7, 9],    (5, 2), ((2, 0), (3, 0))),
        ([1, 1, 4, 5, 7, 9],    (4, 3), ((3, 0), (5, 0))),
        ([1, 3, 3, 5, 7, 9],    (3, 2), ((3, 0), (5, 0))),
        ([1, 3, 4, 5, 7, 9],    (3, 1), ((4, 0), (5, 0)))
    ]
    for test in degree_configuration_list:
        yield tracker_util.exec_simple_test, test
