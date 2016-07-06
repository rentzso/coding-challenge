class VenomGraph(object):

    def update(self, additions, deletions):
        """Updates the graph and return the list of degree updates (one for each modified node) 

        inputs
        ---------
        additions: list of edges to be added (eg [('foo', 'bar'), ('barfoo', 'foo'), ...] )
        deletions: list of edges to be deleted (eg [('foofoo', 'barfoo'), ...] )

        returns
        ---------
        list of degree updates [{<old_degree>: <new_degree>}, ...]
        eg:
            [
                {2: 0}, # all the edges for this node have been deleted (the node has been deleted)
                {0: 1}, # new node with one neighbour
                {3: 2}, # one neighbour less (an edge has been removed)
                {4: 5}, # one new neighbour (new edge)
                ...
            ]

        Possible operations are defined in the class property OPERATIONS
        """
        return []
