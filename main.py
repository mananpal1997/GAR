import argparse
import sys

dot, underscore = False, False
fnames, lnames, numbers = [], [], []


def print_help():
    print "#####\nUSAGE\n#####\n\n\
python mail_extractor.py --filters [.,_,(1997)]\
 --fname_path /path/to/fnames.txt --lname_path /path/to/lnames.txt\n\n\
Filters (combination of filters can be used):\n\
1. '.' => firstname.lastname@gmail.com\n\
2. '_' => firstname_lastname@gmail.com\n\
3. (0-9), numbers inside '()' will be used as permutations,\
 eg- (27) => xyz2@gmail.com, xyz7@gmail.com, xyz27@gmail.com, xyz72@gmail.com"
    return


def load_name_files(fname_path, lname_path):
    with open(fname_path, "r") as f:
        fnames = f.read().strip().split('\n')
    with open(lname_path, "r") as f:
        lnames = f.read().strip().split('\n')
    return


def retrieve():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--filters', dest='filters', type=str)
    parser.add_argument('--fname_path', dest='fname_path', type=str)
    parser.add_argument('--lname_path', dest='lname_path', type=str)

    args = parser.parse_args()

    if len(sys.argv) < 2:
        print_help()
        sys.exit()

    filters = args.filters[1:-1].split(',')
    if '.' in filters:
        filters.remove('.')
        dot = True
    if '_' in filters:
        filters.remove('_')
        underscore = True
    if len(filters) > 0:
        numbers = list(filters[0][1:-1])

    retrieve()
