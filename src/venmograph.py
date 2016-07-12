class VenmoException(Exception):
    pass

class VenmoGraph(object):
    """Class that stores the graph status.
    For each node in the graph, it saves the number of transaction to its neighbors.
    Example:
    {
      "Amber-Sauer": {
        "Caroline-Kaiser-2": 2,
        "Raffi-Antilian": 1,
        "charlotte-macfarlane": 1
      },
      "Raffi-Antilian": {
        "Amber-Sauer": 1,
        "charlotte-macfarlane": 1,
        "Caroline-Kaiser-2": 1
      },
      "charlotte-macfarlane": {
        "Amber-Sauer": 1,
        "Raffi-Antilian": 1,
        "Caroline-Kaiser-2": 1
      },
      "Caroline-Kaiser-2": {
        "Amber-Sauer": 2,
        "Raffi-Antilian": 1,
        "charlotte-macfarlane": 1
      }
    }
    This graph is fully connected as each node had at least one transaction with
    every other node.
    There were 2 transactions between "Caroline-Kaiser-2" and "Amber-Sauer".
    """

    def __init__(self):
        self.graph = {}

    def update(self, new_messages, obsolete_messages):
        """Updates the graph and return the list of degree updates (one for each modified node)

        inputs
        ---------
        additions: list of new messages (eg [{"created_time": "2014-03-27T04:28:20Z", "target": "Jamie-Korn", "actor": "Jordan-Gruber"}] )
        deletions: list of obsolete_messages (eg [{"created_time": "2014-03-27T04:26:00Z", "target": "Maryann-Berry", "actor": "Jamie-Korn"}, ...] )

        returns
        ---------
        list of degree updates [{<old_degree>: <new_degree>}, ...]
        eg:
            [
                (2, 0), # all the edges for this node have been deleted (the node has been deleted)
                (0, 1), # new node with one neighbor
                (3, 2), # one neighbor less (an edge has been removed)
                (4, 5), # one new neighbor (new edge)
                ...
            ]
        """
        degrees_before = {}
        for m in obsolete_messages:
            try:
                degree_before = len(self.graph[m['target']])
                degrees_before[m['target']] = degree_before
                degree_before = len(self.graph[m['actor']])
                degrees_before[m['actor']] = degree_before
            except KeyError as e:
                raise VenmoException('{} does not exist in the graph'.format(e.args[0]))
        for m in obsolete_messages:
            self._handle_obsolete(m['target'], m['actor'])
            self._handle_obsolete(m['actor'], m['target'])
        for  m in new_messages:
            degrees_before[m['target']] = degrees_before.get(
                m['target'],
                len(self.graph.get(m['target'], []))
            )
            self._handle_new(m['target'], m['actor'])
            degrees_before[m['actor']] =  degrees_before.get(
                m['actor'],
                len(self.graph.get(m['actor'], []))
            )
            self._handle_new(m['actor'], m['target'])

        # now that the operations have been performed we can compute all the degree updates
        degree_updates = []
        for node, degree_before in degrees_before.iteritems():
            degree_after = len(self.graph.get(node, []))
            if degree_after != degree_before:
                degree_updates.append((degree_before, degree_after))
        return degree_updates

    def _handle_obsolete(self, node, neighbor):
        """handle an obsolete message by updating/deleting the node neighbor.
        """
        neighbors = self.graph[node]
        try:
            count = neighbors[neighbor]
        except KeyError:
            raise VenmoException('{} does not have {} as neighbor'.format(node, neighbor))
        if count == 1:
            neighbors.pop(neighbor)
            if len(neighbors) == 0:
                self.graph.pop(node)
        else:
            # we don't delete the neighbor here as there
            # was at least one recent transaction.
            neighbors[neighbor] = count - 1

    def _handle_new(self, node, neighbor):
        """add/update a node neighbor.
        """
        self.graph[node] = self.graph.get(node, {})
        neighbors = self.graph[node]
        neighbors[neighbor] = neighbors.get(neighbor, 0) + 1
