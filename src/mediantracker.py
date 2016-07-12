class MedianTrackerException(Exception):
    pass

class MedianTracker(object):
    """Class that tracks the median of graph degrees.
    Each node has its unique representation as a tuple (degree, index) where index is an integer from 0 to #degree - 1.
    There are two fake nodes to have a consistent initial state (0, 1) and (float('inf'), 1)
    These nodes are included in a doubly linked list (the property "nodes_linked_list") in which (degree, index) points to (degree, index + 1) if there is such a node,
    if not it will be point to (degree_above, 0) where degree_above is the next degree above it.

    The degree counts and the median elements are stored respectively in the properties "degrees" and "medians".

    There is only one public instance method, receive, that handles updates to the data structure.
    """

    def __init__(self):
        self.nodes_linked_list = {}
        self.nodes_linked_list[(0, 0)] = {'above': (float('inf'), 0)}
        self.nodes_linked_list[(float('inf'), 0)] = {'below': (0, 0)}
        self.degrees = {
            0: 1,
            float('inf'): 1
        }
        self.medians = ((0, 0), (float('inf'), 0))

    def receive(self, update):
        """Receives and processes one degree update.

        input
        -------
        single degree update (<old_degree>, <new_degree>)

        if old_degree is 0 a new node in the data structure is created (only 1 is accepted as starting degree).
        if new_degree is 0 a node with degree old_degree is removed from the data structure.
        In all other cases one node in the data structure with degree old_degree is updated to a node with new_degree.
        Though, only degree one increases are allowed. There is no such limit on decreases.
        """
        if update[0] == 0:
            if update[1] != 1:
                raise MedianTrackerException('invalid operation {}'.format(update))
            self._receive_new()
        elif update[1] == 0:
            self._receive_obsolete(update[0])
        elif update[0] + 1 == update[1]:
            self._receive_increase(update)
        elif update[0] > update[1]:
            self._receive_decrease(update)
        else:
            raise MedianTrackerException('invalid operation {}'.format(update))

    def _insert_node(self, degree, degree_below, degree_above):
        """insert a new node with degree "degree" between two nodes with "degree_below" and "degree_above".
        Return the node created.
        """
        self.degrees[degree] = self.degrees.get(degree, 0) + 1
        if degree >= degree_above or degree < degree_below:
            message = """Operation not permitted.
            Cannot insert degreee {} between {} and {}""".format(
                degree, degree_below, degree_above
            )
            raise RuntimeError(message)
        elif degree == degree_below:
            position = self.degrees[degree] - 1
            self.nodes_linked_list[(degree, position)] = {
                'below': (degree, position - 1),
                'above': (degree_above, 0)
            }
            self.nodes_linked_list[(degree, position - 1)]['above'] = (degree, position)
            self.nodes_linked_list[(degree_above, 0)]['below'] = (degree, position)
            return (degree, position)
        else:
            count_below = self.degrees[degree_below]
            self.nodes_linked_list[(degree, 0)] = {
                'below': (degree_below, count_below - 1),
                'above': (degree_above, 0)
            }
            self.nodes_linked_list[(degree_below, count_below - 1)]['above'] = (degree, 0)
            self.nodes_linked_list[(degree_above, 0)]['below'] = (degree, 0)
            return (degree, 0)


    def _remove_node(self, degree):
        """removes a node from the linked list.
        Returns the node deleted and the two nodes that were before and after it.
        """
        count = self.degrees[degree]
        node_above = self.nodes_linked_list[(degree, count - 1)]['above']
        node_below = self.nodes_linked_list[(degree, count - 1)]['below']
        self.nodes_linked_list[node_above]['below'] = node_below
        self.nodes_linked_list[node_below]['above'] = node_above
        self.nodes_linked_list.pop(degree, count - 1)
        if count == 1:
            self.degrees.pop(degree)
        else:
            self.degrees[degree] = count - 1
        return (degree, count - 1), node_below, node_above

    def _update_median_on_insert(self, new_node):
        """updates the median element(s) after an insertion.
        """
        if len(self.medians) == 2:
            if new_node < self.medians[0]:
                self.medians = (self.medians[0],)
            elif new_node > self.medians[1]:
                self.medians = (self.medians[1],)
            elif self.medians[0] < new_node < self.medians[1]:
                self.medians = (new_node,)
            else:
                raise RuntimeError('Operation not valid. the new node already existed.')
        else:
            if new_node < self.medians[0]:
                below_median = self.nodes_linked_list[self.medians[0]]['below']
                self.medians = (below_median, self.medians[0])
            elif new_node > self.medians[0]:
                above_median = self.nodes_linked_list[self.medians[0]]['above']
                self.medians = (self.medians[0], above_median)
            else:
                raise RuntimeError('Operation not valid. the new node already existed.')

    def _update_median_on_remove(self, obsolete_node, node_below, node_above):
        """updates the median element(s) after a removal.
        """
        if len(self.medians) == 2:
            if obsolete_node >= self.medians[1]:
                self.medians = (self.medians[0],)
            elif obsolete_node <= self.medians[0]:
                self.medians = (self.medians[1],)
            else:
                raise RuntimeError('Invalid state. Medians are not contiguous')
        else:
            if obsolete_node > self.medians[0]:
                below_median = self.nodes_linked_list[self.medians[0]]['below']
                self.medians = (below_median, self.medians[0])
            elif obsolete_node < self.medians[0]:
                above_median = self.nodes_linked_list[self.medians[0]]['above']
                self.medians = (self.medians[0], above_median)
            else:
                self.medians = (node_below, node_above)

    def _receive_new(self):
        """receives a new element of the graph. The node will always start with degree 1.
        """
        count = self.degrees.get(1)
        if count:
            degree_below = 1
            degree_above = self.nodes_linked_list[(1, count - 1)]['above'][0]
        else:
            degree_below = 0
            degree_above = self.nodes_linked_list[(0, 0)]['above'][0]
        new_node = self._insert_node(1, degree_below, degree_above)
        self._update_median_on_insert(new_node)

    def _receive_obsolete(self, degree):
        """receives an obsolete element of the graph and deletes it from the linked_list.
        """
        obsolete_node, node_below, node_above = self._remove_node(degree)
        self._update_median_on_remove(obsolete_node, node_below, node_above)
        return obsolete_node, node_below, node_above

    def _receive_increase(self, update):
        """receives an increase in the degree.
        For each update we have that: degree_after - degree_before == 1
        """
        degree_before, degree_after = update
        _, node_below, node_above = self._receive_obsolete(degree_before)
        if node_above[0] > degree_after:
            degree_below = node_below[0]
            degree_above = node_above[0]
        elif node_above[0] == degree_after:
            degree_below = degree_after
            count = self.degrees[degree_after]
            degree_above = self.nodes_linked_list[(degree_after, count - 1)]['above'][0]
        else:
            raise RuntimeError("""Invalid state or operation.
            State: {} {}
            Operation: {} {}
            """.format(
                self.graph, self.nodes_linked_list,
                degree_before, degree_after
            ))
        new_node = self._insert_node(degree_after, degree_below, degree_above)
        self._update_median_on_insert(new_node)

    def _receive_decrease(self, update):
        """receives a decrease in the degree.
        To insert the node correctly we need to find the first degree below for which there is a node.
        """
        degree_before, degree_after = update
        _, _, node_above = self._receive_obsolete(degree_before)
        for degree_above in xrange(degree_after + 1, degree_before + 1):
            if self.degrees.get(degree_above):
                break
        else:
            degree_above = node_above[0]
        degree_below = self.nodes_linked_list[(degree_above, 0)]['below'][0]
        new_node = self._insert_node(degree_after, degree_below, degree_above)
        self._update_median_on_insert(new_node)

    def median(self):
        """method to compute the numeric median"""
        if len(self.medians) == 1:
            return self.medians[0][0]
        else:
            return (self.medians[0][0] + self.medians[1][0])/2.0
