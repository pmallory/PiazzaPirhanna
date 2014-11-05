import argparse
import csv
import sys

import piazza_api

#TODO take roster file name
def initialize_class(class_id, emails_path):
    emails = []
    with open(emails_path)  as f:
        for email_address in f:
            emails.append(email_address)

    p = piazza_api.PiazzaAPI(class_id)
    p.user_auth()
    piazza_data = p.enroll_students(emails)

    with open('new_roster.csv', 'w') as roster:
        writer = csv.writer(roster)
        writer.writerow(['Canonical Email', 'Piazza ID', 'Is Enrolled', 'Name' ])
        for student in piazza_data:
            if student.get(u'role') == u'student':
                writer.writerow([student.get(u'email'),
                                 student.get(u'id'),
                                 True,
                                 student.get(u'name')])

    print("roster written to new_roster.csv") #TODO fix

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

