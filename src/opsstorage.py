import datetime
import sys

class OpsStorageException(Exception):
    pass

class OpsStorage(object):
    """Class responsible of keeping transactions to be stored in a graph.
    When a new transaction arrives, the storage is updated and the list of edges to be added/deleted is returned
    """

    def __init__(self):
        self.transactions = {}
        self.max_timestamp = 0

    def get_update(self, message):
        """From a json message updates the list of transactions
        and return a list of new messages and a list of obsolete messages.

        inputs
        --------
        message: json representing a single transaction
            eg:
                {"created_time": "2014-03-27T04:28:20Z", "target": "Jamie-Korn", "actor": "Jordan-Gruber"}

        returns
        --------
        list of new messages and list of obsolete messages
        eg:
            [
                [{"created_time": "2014-03-27T04:28:20Z", "target": "Jamie-Korn", "actor": "Jordan-Gruber"}],
                [{"created_time": "2014-03-27T04:26:00Z", "target": "Maryann-Berry", "actor": "Jamie-Korn"}, ...]
            ]
        """
        timestamp = self._seconds_since_epoch(message.get('created_time', ''))
        if not message.get('actor'):
            raise OpsStorageException('Actor in message is missing.')
        if not message.get('target'):
            raise OpsStorageException('Target in message is missing.')
        new_messages = self._get_new(message, timestamp)
        obsolete_messages = self._get_obsolete(timestamp)
        self.max_timestamp = max(timestamp, self.max_timestamp)
        return new_messages, obsolete_messages

    def _get_obsolete(self, timestamp):
        """gets all the messages older than 60 seconds from the current transaction timestamp"""
        obsolete_messages = []
        start = self.max_timestamp - 59
        end = min(timestamp - 59, self.max_timestamp + 1)
        for t in xrange(start, end):
            obsolete_messages += self.transactions.pop(t, [])
        return obsolete_messages

    def _get_new(self, message, timestamp):
        """gets the new messages from a single transatcion."""
        self.transactions[timestamp] = self.transactions.get(timestamp, [])
        self.transactions[timestamp].append(message)
        if timestamp < self.max_timestamp - 59:
            return []
        return [message]

    def _seconds_since_epoch(self, created_time):
        """converts timstamps to seconds since the epoch."""
        try:
            parsed_time = datetime.datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise OpsStorageException('created time is not valid: {}'.format(created_time))
        return int((parsed_time - datetime.datetime(1970, 1, 1)).total_seconds())
