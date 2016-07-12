"""Tests for OpsStorage operations.
"""
import opsstorage
from nose import with_setup
from nose.tools import assert_raises

def test_invalids():
    """tests invalid messages"""
    storage = opsstorage.OpsStorage()
    invalid_messages = [
        {'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': ''},
        {'created_time': '2016-03-28T23:23:12Z', 'target': '', 'actor': 'Amber-Sauer'},
        {'created_time': 'not valid', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}
    ]
    for m in invalid_messages:
        yield assert_raises, opsstorage.OpsStorageException, storage.get_update, m

def test_one():
    """"tests a single valid message"""
    msg = {'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}
    storage = opsstorage.OpsStorage()
    new_messages, obsolete_messages = storage.get_update(msg)
    assert new_messages == [msg]
    assert obsolete_messages == []

def test_two():
    """tests two valid messages with the same timing"""
    msg_1 = {'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}
    msg_2 = {'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Caroline-Kaiser-2'}
    storage = opsstorage.OpsStorage()
    storage.get_update(msg_1)
    new_messages, obsolete_messages = storage.get_update(msg_2)
    assert new_messages == [msg_2]
    assert obsolete_messages == []

_globals = {}

def setup_timing():
    msg_1 = {'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Raffi-Antilian'}
    msg_2 = {'created_time': '2016-03-28T23:23:12Z', 'target': 'Amber-Sauer', 'actor': 'Caroline-Kaiser-2'}
    storage = opsstorage.OpsStorage()
    storage.get_update(msg_1)
    storage.get_update(msg_2)
    _globals['storage'] = storage
    _globals['messages'] = [msg_1, msg_2]

def test_message_timing():
    """tests how the OpsStorage responds to different message timing"""
    @with_setup(setup_timing)
    def exec_test(msg, expected_new, expected_obsolete, timestamp=None):
        storage = _globals['storage']
        if timestamp is None:
            timestamp = storage.max_timestamp
        new_messages, obsolete_messages = storage.get_update(msg)
        assert storage.max_timestamp == timestamp, (
            '{} != {}'.format(storage.max_timestamp, timestamp)
        )
        assert new_messages == expected_new, (
            '{} != {}'.format(new_messages, expected_new)
        )
        assert obsolete_messages == expected_obsolete, (
            '{} != {}'.format(obsolete_messages, expected_obsolete)
        )
    messages = [
        {'created_time': '2016-03-28T23:22:12Z', 'target': 'More-than-60-before', 'actor': 'Raffi-Antilian'},
        {'created_time': '2016-03-28T23:22:13Z', 'target': 'Less-than-60-before', 'actor': 'Raffi-Antilian'},
        {'created_time': '2016-03-28T23:24:12Z', 'target': 'More-than-60-after', 'actor': 'Raffi-Antilian'},
        {'created_time': '2016-03-28T23:24:11Z', 'target': 'Less-than-60-after', 'actor': 'Raffi-Antilian'}
    ]
    yield exec_test, messages[0], [], []
    yield (
        exec_test, messages[1], [messages[1]], []
    )
    timestamp = 1459207452 # '2016-03-28T23:24:12Z'
    yield (
        exec_test, messages[2], [messages[2]], _globals['messages'], timestamp
    )
    timestamp = 1459207451 # '2016-03-28T23:24:11Z'
    yield (
        exec_test, messages[3], [messages[3]], [], timestamp
    )
