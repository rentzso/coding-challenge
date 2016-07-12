import sys
import json

from mediantracker import MedianTracker
from opsstorage import OpsStorage, OpsStorageException
from venmograph import VenmoGraph

def main(input_stream, output_stream, debug=False, MedianTrackerClass=MedianTracker):
    """This methods executes the following steps:
    1) for each line from the input_stream, uses the OpsStorage instance to process the transaction
    2) gets from it a batch of new and obsolete messages
    3) uses the VenmoGraph Instance to process this batch
    4) the results is a list of degree updates
    5) they are all processed by the MedianTracker that returns the rolling median
    6) the median is written to the output_stream"""
    ops = OpsStorage()
    graph = VenmoGraph()
    tracker = MedianTrackerClass()
    for line in input_stream:
        try:
            message = json.loads(line)
        except ValueError:
            # skip message
            continue
        try:
            new_messages, obsolete_messages = ops.get_update(message)
        except OpsStorageException:
            # skip message
            continue
        degree_updates = graph.update(new_messages, obsolete_messages)
        for update in degree_updates:
            tracker.receive(update)
        if debug:
            output_stream.write('{} {} '.format(line.strip(), tracker.degrees))
        output_stream.write('{:.2f}\n'.format(tracker.median()))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        debug = (sys.argv[1] == 'debug')
    else:
        debug = False
    main(sys.stdin, sys.stdout, debug)
