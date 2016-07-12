import random
import os
import sys
import shutil
import copy

def generate_shuffle(lines):
    max_size = len(lines)
    min_size = min(15, max_size/2)
    size = random.randint(min_size, max_size)
    shuffled = copy.deepcopy(lines[:size])
    random.shuffle(shuffled)
    return shuffled

def save_shuffle(shuffled, i):

    base = os.path.join('tests', 'test-data-gen-shuffled-' + str(i))
    input_dir = os.path.join(base, 'venmo_input')
    output_dir = os.path.join(base, 'venmo_output')
    file_path = os.path.join(input_dir, 'venmo-trans.txt')
    try:
        shutil.rmtree(base)
    except:
        pass
    os.makedirs(input_dir)
    os.makedirs(output_dir)
    with open(file_path, 'w') as f:
        for line in shuffled:
            f.write(line)

def main():
    n = int(sys.argv[1]) if len(sys.argv) == 2 else 3
    with open('../data-gen/venmo-trans.txt') as f:
        lines = f.readlines()
    for i in xrange(n):
        shuffled = generate_shuffle(lines)
        save_shuffle(shuffled, i)

if __name__ == '__main__':
    main()
