import argparse
import csv
import os
from pprint import pprint
import sys

import piazza_api

#TODO take roster file name
def initialize_class(class_id, emails_path):
    emails = []
    with open(emails_path)  as f:
        for email_address in f:
            emails.append(email_address)

    p = piazza_api.PiazzaAPI(class_id)
    p.user_auth() #TODO uncaught exception
    piazza_data = p.enroll_students(emails)

    with open('new_roster.csv', 'w') as roster:
        writer = csv.writer(roster)
        writer.writerow(['Canonical Email', 'Piazza ID'])
        for student in piazza_data:
            if student.get(u'role') == u'student':
                writer.writerow([student.get(u'email'),
                                 student.get(u'id')])

    print("roster written to new_roster.csv") #TODO fix

def sync(class_id, roster_path, nd_course_code):
    # build set of students enrolled in this ND
    enrolled_students = set()
    with open('coached_students.csv') as rainman_csv:
        reader = csv.reader(rainman_csv)
        for row in reader:
            if row[5] == nd_course_code: #row[5] is the course code
                enrolled_students.add(row[2]) # row[2] is the student's email

    ids_to_drop = [] #a list of student IDs to un-enroll from Piazza


    with open(roster_path, 'r') as roster_file:
        with open('.PiazzaPirhana.tmp', 'w') as temp_file:
            writer = csv.writer(temp_file)

            writer.writerow(['Canonical Email', 'Piazza ID'])

            for row in csv.reader(roster_file):
                student_email = row[0]
                student_id = row[1]
                if student_email in enrolled_students:
                    #if this student is still enrolled keep them on the roster
                    writer.writerow(row)
                else:
                    #otherwise mark them for removal from Piazza
                    assert student_id
                    ids_to_drop.append((student_email, student_id))

    print("Students to be unenrolled from Piazza and removed from {}".format(
        roster_path))
    pprint(ids_to_drop)#TODO print prettier
    print ("\nPress return to proceed, ^C to abort")
    while True:
        if sys.stdin.read(1):
            break

    #un-enroll students from Piazza
    p = piazza_api.PiazzaAPI(class_id)
    p.user_auth() #TODO uncaught exception
    p.remove_users([idno[1] for idno in ids_to_drop])

    #Overwrite old roster with updated roster
    os.remove(roster_path)
    os.rename('.PiazzaPirhana.tmp', roster_path)

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
    parser.add_argument("-nd", "--nanodegree-course-code",
                        help="The course code of the nanodegree to sync")

    args = parser.parse_args()

    if args.synchronize and not (args.class_id and args.nanodegree_course_code):
        print("Please provide and a Piazza class id to synchronize with")
        sys.exit()

    if args.new_roster and not args.class_id:
        print("Please provide a Piazza class id to enroll students in")
        sys.exit()

    if args.synchronize:
        sync(args.class_id, args.synchronize, args.nanodegree_course_code)
    elif args.new_roster:
        initialize_class(args.class_id, args.new_roster)

