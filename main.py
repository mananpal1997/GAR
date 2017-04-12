import argparse
import sys
from itertools import permutations, product
import urllib2
import pickle

dot, underscore = False, False
fnames, lnames, numbers = [], [], []
target_url = "https://mail.google.com/mail/gxlu?email="


def print_help():
    print "#####\nUSAGE\n#####\n\n\
python mail_extractor.py --filters [.,_,(1997)]\
 --fname_path /path/to/fnames.txt --lname_path /path/to/lnames.txt\n\n\
Filters (combination of filters can be used):\n\
1. '.' => firstname.lastname@gmail.com\n\
2. '_' => firstname_lastname@gmail.com\n\
3. (0-9), numbers inside '()' will be used as permutations,\
 eg- (27;1) => xyz2@gmail.com, xyz7@gmail.com,\
  xyz27@gmail.com, xyz72@gmail.com, xyz1@gmail.com"
    return


def load_name_files(fname_path, lname_path):
    global fnames
    global lnames
    with open(fname_path, "r") as f:
        fnames = f.read().strip().split('\n')
    with open(lname_path, "r") as f:
        lnames = f.read().strip().split('\n')
    return


def generate():
    # a => firstname, b => lastname
    email_basenames = []
    perm_list = []

    if numbers:
        perm_list = []
        for num in numbers:
            perm_list.extend([''.join(digits) for digits in permutations(num)])

        # Generate all [a,b,1] combinations
        arr = [fnames, lnames, perm_list]
        normalised_list = list(product(*arr))  # [(a, b, 1), (a, c, 1) ...]
        # Now break [(a,b,1),(a,c,1) ...] in [a,a...] [b,c...] [1,1...]
        first_names, last_names, number = map(list, zip(*normalised_list))

        if dot and underscore:
            # Dummy Cases=> a.b_1, a_b.1
            for f, l, n in zip(first_names, last_names, number):
                email_basenames.append(f + "." + l + "_" + n)
                email_basenames.append(f + "_" + l + "." + n)
            return email_basenames

        elif dot:
            # Dummy Cases=> a.b1, ab.1, a.b.1
            for f, l, n in zip(first_names, last_names, number):
                email_basenames.append(f + "." + l + n)
                email_basenames.append(f + l + "." + n)
                email_basenames.append(f + "." + l + "." + n)
            return email_basenames

        elif underscore:
            # Dummy Cases=> a_b1, ab_1, a_b_1
            for f, l, n in zip(first_names, last_names, number):
                email_basenames.append(f + "_" + l + n)
                email_basenames.append(f + l + "_" + n)
                email_basenames.append(f + "_" + l + "_" + n)
            return email_basenames

        else:
            # Dummy Case=> ab1
            for f, l, n in zip(first_names, last_names, number):
                email_basenames.append(f + l + n)
            return email_basenames

    else:
        # Generate all [a,b] combinations
        arr = [fnames, lnames]
        normalised_list = list(product(*arr))  # [(a, b), (a, c) ...]
        # Now break [(a,b),(a,c) ...] in [a,a...] [b,c...]
        first_names, last_names = map(list, zip(*normalised_list))

    if dot:
        # Dummy Case=> a.b
        for f, l in zip(first_names, last_names):
            email_basenames.append(f + "." + l)
        return email_basenames

    elif underscore:
        # Dummy Case=> a_b
        for f, l in zip(first_names, last_names):
            email_basenames.append(f + "_" + l)
        return email_basenames

    else:
        # No filters or some error with filters
        for f, l in zip(first_names, last_names):
            email_basenames.append(f + l)
        return email_basenames


def retrieve():
    email_basenames = generate()
    valid_emails = []
    for email_basename in email_basenames:
        url = target_url + email_basename + "@gmail.com"
        print "validating " + email_basename + "@gmail.com ..."
        try:
            connection = urllib2.urlopen(url)
            if 'set-cookie' in connection.headers.keys():
                print "VALID !"
                valid_emails.append(email_basename + "@gmail.com")
            else:
                print "NOT VALID !"
            connection.close()
        except (KeyboardInterrupt, SystemExit):
            break
        except:
            pass
    return valid_emails


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--filters',
        dest='filters',
        type=str
    )
    parser.add_argument(
        '--fname_path',
        dest='fname_path',
        type=str,
        required=True
    )
    parser.add_argument(
        '--lname_path',
        dest='lname_path',
        type=str,
        required=True
    )

    args = parser.parse_args()

    if len(sys.argv) < 2:
        print_help()
        sys.exit()

    try:
        filters = args.filters[1:-1].split(',')
    except:
        filters = []
    if '.' in filters:
        filters.remove('.')
        dot = True
    if '_' in filters:
        filters.remove('_')
        underscore = True
    if len(filters) > 0:
        numbers = filters[0].strip()[1:-1].split(";")

    try:
        load_name_files(args.fname_path, args.lname_path)
    except:
        print "Error in reading from files."
        print "Check if path is valid, or files are not corrupted"
        print "exiting..."
        sys.exit()

    data = retrieve()
    # print data
    with open("data.pickle", "wb") as file:
        pickle.dump(data, file)
