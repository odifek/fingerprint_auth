#! python3
"""
Requests user to swipe his/her finger on the finger print sensor
Compares fingerprint data with those stored in the database.
Grants access if match found
"""

from __future__ import print_function
import pyfprint
import sqlite3

DB_FILE = "bio_fp.db"


def authenticate():
    pyfprint.fp_init()  # Initialize the fingerprint library
    devs = pyfprint.discover_devices()
    dev = devs[0]
    dev.open()

    # Connect to the database database
    fdb = sqlite3.connect(DB_FILE)
    users = []
    gallery = []

    print("To gain access, we have to verify you are authorized using the biometric system\n")
    with fdb:
        cur = fdb.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='biometric'")
        if not cur.fetchone():
            print("No data in database yet. Please enroll first")
            return

        cur.execute("SELECT username, finger_p FROM biometric")
        for row in cur.fetchall():
            fp_str = row[1].decode('utf8', 'surrogateescape') # Decode binary data from db
            data = pyfprint.pyf.fp_print_data_from_data(fp_str)
            gallery.append(pyfprint.Fprint(data_ptr=data))
            users.append(row[0])
        print("To proceed, please swipe your RIGHT INDEX finger on the sensor...\n")
        n, fprint, img = dev.identify_finger(gallery)
        print("Verifying...")

    if fprint:
        print("Verified! {0}".format(users[n]))
    else:
        print("Verification Failed")

    # verified, img = dev.verify_finger(fprint)
    # if verified:
    #     print("Welcome, {0}".format(username))
    # else:
    #     print("Sorry! You are not allowed here!")

    # if img is not None:
    dev.close()
    pyfprint.fp_exit()

authenticate() # Run the authentication function