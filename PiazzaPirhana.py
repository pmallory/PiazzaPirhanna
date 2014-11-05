import argparse
import sys

import piazza_api

def initialize_class(class_id, emails_path):
    pass

def sync(class_id, roster_path):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage Piazza enrollment')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--new-roster",
                        help="list of \\n separated email addresses")
    group.add_argument("-s", "--synchronize",
                        metavar='ROSTER_FILE',
                        help="Sync Piazza's roster to match ROSTER_FILE")
    parser.add_argument("-id", "--class-id",
                        help="The Piazza ID of the course to be updated")

    args = parser.parse_args()

    if args.synchronize and not args.class_id:
        print("Please provide a Piazza class id to synchronize with")
        sys.exit()

    if args.new_roster and not args.class_id:
        print("Please provide a Piazza class id to enroll students in")
        sys.exit()

    if args.synchronize:
        sync(args.class_id, args.synchronize)
    else:
        initialize_class(args.class_id, args.new_roster)

