PiazzaPirhanna
==============

There's two ways to run PiazzaPirhanna:

1. Add new students mode
2. Synchronize Piazza with the Rainman roster mode

Add new students mode
---------------------
1. To add new students you need a file with a list of student email addresses (one per line)
2. Run something like this: `python PiazzaPirhana.py -n email_list.txt -id i0ifo49m8204pq`
i0ifo49m8204pq a Piazza class ID, you can get this from the url of a class if you're on the Q&A page.
3. That will add each of those email address to the Piazza course, students will get emails to join!
4. It will also spit out new_roster.csv Rename that file and don't lose it.

Synchronize Piazza with the Rainman roster mode
-----------------------------------------------
1. Don't panic! PiazzaPirhanna will give you a list of the students it wants to remove from Piazza/the roster.
It won't actually remove them until you tell it to.
Hit control-c to abort the sync
2. Run something like this: `python PiazzaPirhana.py -s new_roster.csv -id i0ifo49m8204pq -nd nd001`
3. PiazzaPirhanna will tell you the students it thinks have dropped. Press return if the list looks correct.
4. The students will be removed from Piazza and from the roster csv.
