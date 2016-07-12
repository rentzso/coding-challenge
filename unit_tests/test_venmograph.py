"""Tests for VenmoGraph operations.
"""
from nose import with_setup
from nose.tools import assert_equals
import copy
import venmograph

_globals = {
    'single_edge_graph': {
        'Amber-Sauer': {
            'Raffi-Antilian': 1
        },
        'Raffi-Antilian': {
            'Amber-Sauer': 1
        }
    }
}

def test_first_message():
    """Tests the graph when the first message (edge) arrives."""
    graph = venmograph.VenmoGraph()
    updates = graph.update(
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}],
        []
    )
    assert_equals(graph.graph, _globals['single_edge_graph'])
    assert_equals(
        set(updates), set([(0, 1), (0, 1)])
    )

def setup_single_edge_graph():
    graph = venmograph.VenmoGraph()
    # single edge graph
    graph.graph = copy.deepcopy(_globals['single_edge_graph'])
    _globals['graph'] = graph

def test_updates_on_single_edge_graph():
    @with_setup(setup_single_edge_graph)
    def exec_test(new_messages, obsolete_messages, expected_graph, expected_updates):
        graph = _globals['graph']
        updates = graph.update(new_messages, obsolete_messages)

        assert_equals(graph.graph, expected_graph)
        assert_equals(set(updates), expected_updates)
    # add a new edge
    yield (
        exec_test,
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Caroline-Kaiser-2'}],
        [],
        {
            'Amber-Sauer': {
                'Raffi-Antilian': 1,
                'Caroline-Kaiser-2': 1
            },
            'Raffi-Antilian': {
                'Amber-Sauer': 1
            },
            'Caroline-Kaiser-2': {
                'Amber-Sauer': 1
            }
        },
        set([(0, 1), (1, 2)])
    )
    # receive one message that deletes an edge and another that recreates it
    # the graph stays the same
    # no update is returned
    yield (
        exec_test,
        [{'created_time': '2016-03-28T23:28:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}],
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}],
        _globals['single_edge_graph'],
        set()
    )
    # delete an edge
    yield (
        exec_test,
        [],
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}],
        {},
        set([(1, 0), (1, 0)])
    )
    # a new transaction for the same edge is received
    # no updates is sent
    # the neighbor counts get updated
    yield (
        exec_test,
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}],
        [],
        {
            'Amber-Sauer': {
                'Raffi-Antilian': 2
            },
            'Raffi-Antilian': {
                'Amber-Sauer': 2
            }
        },
        set()
    )

def test_updates_on_generic_graph():
    def exec_test(new_messages, obsolete_messages, expected_graph, expected_updates):
        graph = venmograph.VenmoGraph()
        graph.graph = {
            'Amber-Sauer': {
                'Caroline-Kaiser-2': 2,
                'Raffi-Antilian': 1
            },
            'Raffi-Antilian': {
                'Amber-Sauer': 1,
                'charlotte-macfarlane': 1
            },
            'Caroline-Kaiser-2': {
                'Amber-Sauer': 2
            },
            'charlotte-macfarlane': {
                'Raffi-Antilian': 1
            }
        }
        updates = graph.update(new_messages, obsolete_messages)
        assert_equals(expected_graph, graph.graph)
        assert_equals(set(updates), expected_updates)
    # add a new edge
    yield (
        exec_test,
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'charlotte-macfarlane'}],
        [],
        {
            'Amber-Sauer': {
                'Caroline-Kaiser-2': 2,
                'Raffi-Antilian': 1,
                'charlotte-macfarlane': 1
            },
            'Raffi-Antilian': {
                'Amber-Sauer': 1,
                'charlotte-macfarlane': 1
            },
            'Caroline-Kaiser-2': {
                'Amber-Sauer': 2
            },
            'charlotte-macfarlane': {
                'Amber-Sauer': 1,
                'Raffi-Antilian': 1
            }
        },
        set([(1, 2), (2, 3)])
    )
    # delete a redundant edge
    # no update is returned
    # the neighbor counts are updated
    yield (
        exec_test,
        [],
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Caroline-Kaiser-2'}],
        {
            'Amber-Sauer': {
                'Caroline-Kaiser-2': 1,
                'Raffi-Antilian': 1
            },
            'Raffi-Antilian': {
                'Amber-Sauer': 1,
                'charlotte-macfarlane': 1
            },
            'Caroline-Kaiser-2': {
                'Amber-Sauer': 1
            },
            'charlotte-macfarlane': {
                'Raffi-Antilian': 1
            }
        },
        set()
    )
    # delete a non redundant edge
    yield (
        exec_test,
        [],
        [{'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}],
        {
            'Amber-Sauer': {
                'Caroline-Kaiser-2': 2
            },
            'Raffi-Antilian': {
                'charlotte-macfarlane': 1
            },
            'Caroline-Kaiser-2': {
                'Amber-Sauer': 2
            },
            'charlotte-macfarlane': {
                'Raffi-Antilian': 1
            }
        },
        set([(2, 1), (2, 1)])
    )
    # delete every edge having "Raffi-Antilian" as vertex
    # delete the node "Raffi-Antilian"
    # send the correct degree updates
    yield (
        exec_test,
        [],
        [
            {'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'},
            {'created_time': '2016-03-28T23:23:12Z', 'target': 'charlotte-macfarlane', 'actor': 'Raffi-Antilian'},
        ],
        {
            'Amber-Sauer': {
                'Caroline-Kaiser-2': 2
            },
            'Caroline-Kaiser-2': {
                'Amber-Sauer': 2
            }
        },
        set([(2, 0), (2, 1), (1, 0)])
    )
