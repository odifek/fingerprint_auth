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
    dev = devs[0] # Select the first device detected
    dev.open()

    # Connect to the database database
    fdb = sqlite3.connect(DB_FILE)
    users = []
    gallery = []

    print("To gain access, we have to verify you are authorized using the biometric system\n")

    with fdb:
        cur = fdb.cursor()

        # Check that the table is already created. if not, it means no enrolment has been made so far
        # The function will return immediately
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='biometric'")
        if not cur.fetchone():
            print("No data in database yet. Please enroll first")
            return

        # Query the database for all entries, storing them in a vector list (users and gallery)
        cur.execute("SELECT username, finger_p FROM biometric")
        for row in cur.fetchall():
            fp_str = row[1].decode('utf8', 'surrogateescape') # Decode binary data from db
            data = pyfprint.pyf.fp_print_data_from_data(fp_str)
            gallery.append(pyfprint.Fprint(data_ptr=data))
            users.append(row[0])

        # After querying the database, proceed to ask for users finger swipe
        print("To proceed, please swipe your RIGHT INDEX finger on the sensor...\n")

        # Verification is done here
        # Checks to see if the users fingerprint match any of those retrieved from database
        n, fprint, img = dev.identify_finger(gallery)
        print("Authenticating...")

    if fprint:
        print("Authenticated! {0}".format(users[n])) # User is authenticated
        result = True
    else:
        print("Authentication Failed")  # User not authenticated
        result = False

    # verified, img = dev.verify_finger(fprint)
    # if verified:
    #     print("Welcome, {0}".format(username))
    # else:
    #     print("Sorry! You are not allowed here!")

    # if img is not None:
    dev.close()
    pyfprint.fp_exit()
    return result

def authenticate_from_disk():
    """
    Authenticate single user from data stored in his home directory
    :return: Boolean
    """

    # Initialize things
    pyfprint.fp_init()
    devs = pyfprint.discover_devices()
    dev = devs[0]
    dev.open()
    fprint = dev.load_print_from_disk(pyfprint.Fingers['RIGHT_INDEX'])

    print("Verifying...\nSwipe your finger across the sensor to proceed")
    verified, img = dev.verify_finger(fprint)

    if verified:
        print("Authenticated!")
    else:
        print("Authentication failed")
    if img is not None:
        img.save_to_file('verify.pgm')
        print("Wrote scanned image to verify.pgm")

    # Closing formalities
    dev.close()
    pyfprint.fp_exit()


# authenticate() # Run the authentication function for database authentication


authenticate_from_disk() # Authenticate from disk. Uncomment to run this function.  ***Delete the trailing space also
