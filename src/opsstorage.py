class OpsStorage(object):
    def get_update(self, message):
        """From a json message updates the list of transactions
        and return a list of edges added and deleted.

        inputs
        --------
        message: json representing a single transaction
            eg:
                {"created_time": "2014-03-27T04:28:20Z", "target": "Jamie-Korn", "actor": "Jordan-Gruber"}

        returns
        --------
        list of edges to be added and list of edges to be deleted
        eg:
            [('Jamie-Korn', 'Jordan-Gruber'), ...], [('Maryann-Berry', 'Jamie-Korn'), ...]
        """
        return [], []
