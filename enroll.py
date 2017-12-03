# Create table and insert fingerprint data into database
from __future__ import print_function
import pyfprint
import sqlite3

DB_FILE = "bio_fp.db"
def capture():
    print("To proceed with your fingerprint enrolment\n")
    username = input("Please enter your username: ")

    pyfprint.fp_init()
    devs = pyfprint.discover_devices()
    dev = devs[0]
    dev.open()

    print("Enrolling...\n\n")
    print("Please swipe your RIGHT INDEX finger on the sensor 5 times")
    fprint, img = dev.enroll_finger()

    fdb = sqlite3.connect(DB_FILE)

    with fdb:
        cur = fdb.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS biometric (username, finger_p BLOB)")
        if fprint is not None:
            b_fp = fprint.data().encode('utf8', 'surrogateescape') # Convert to binary data for onward storage in db
            cur.execute("INSERT INTO biometric(username, finger_p) VALUES(?, ?)", (username, sqlite3.Binary(b_fp),))
            print("Fingerprint Successfully enrolled! Thank you!")
        else:
            print("finger print not properly captured!")

    dev.close()
    pyfprint.fp_exit()


capture()