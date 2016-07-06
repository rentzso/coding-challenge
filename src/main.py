import sys
import json

from .mediantracker import MedianTracker
from .opsstorage import OpsStorage
from .venomgraph import VenomGraph

def main():
    ops = OpsStorage()
    graph = VenomGraph()
    tracker = MedianTracker()
    for line in sys.stdout:
        message = json.loads(line)
        additions, deletions = ops.get_update(message)
        updated_nodes = graph.update(additions, deletions)
        median = tracker.receive(updated_nodes)
        print median
