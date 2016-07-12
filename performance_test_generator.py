import sys
import json
import datetime

def generate_samples(start, end, timestamp):
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    transaction = {
        'actor': str(start),
        'created_time': timestamp.strftime(dateformat)
    }
    for i in xrange(start + 1, end):
        transaction['target'] = transaction['actor']
        transaction['actor'] = str(i)
        print json.dumps(transaction)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        size = int(sys.argv[1])
    else:
        size = 100
    now = datetime.datetime.now()
    start = 0
    end = size/2
    generate_samples(start, end, now)
    start = end
    end = size
    generate_samples(start, end, now + datetime.timedelta(seconds=90))
