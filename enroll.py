#! python3


from __future__ import print_function
import pyfprint
import sqlite3

DB_FILE = "bio_fp.db"


def capture():
    """
    Takes care of enrolment of individual fingerprints. The right index finger is used here.
    The biometrics data is stored in the database along with the username of the person
    """

    print("To proceed with your fingerprint enrolment\n")
    username = input("Please enter your username: ") # Request username at the command line

    # Initialization and selection of fingerprint module
    pyfprint.fp_init()
    devs = pyfprint.discover_devices()
    dev = devs[0]
    dev.open()

    print("Enrolling...\n\n")
    print("Please swipe your RIGHT INDEX finger on the sensor 5 times")
    fprint, img = dev.enroll_finger() # Fingerprint data is retried along with the image which can be used to update a GUI

    fprint.save_to_disk(pyfprint.Fingers['RIGHT_INDEX'])
    if img is not None:
        img.save_to_file('enrolled.pgm')
        print("Wrote scanned image to enrolled.pgm")

    # Connect database
    fdb = sqlite3.connect(DB_FILE)

    # Work on the database object
    with fdb:
        cur = fdb.cursor() # The cursor is used by python to address a table in the database
        cur.execute("CREATE TABLE IF NOT EXISTS biometric (username, finger_p BLOB)")
        if fprint is not None:
            b_fp = fprint.data().encode('utf8', 'surrogateescape') # Convert to binary data for onward storage in db
            cur.execute("INSERT INTO biometric(username, finger_p) VALUES(?, ?)", (username, sqlite3.Binary(b_fp),))
            print("Fingerprint Successfully enrolled! Thank you!")
        else:
            print("finger print not properly captured!")

    # Closing formalities
    dev.close()
    pyfprint.fp_exit()

def capture_to_disk():
    """
    Enrolls a single user and saves his data in his home directory
    :return: None
    """
    # Intialize things
    pyfprint.fp_init()
    devs = pyfprint.discover_devices()
    dev = devs[0] # Select the first device found
    dev.open()
    print("Enrolling...\n")
    print("Please swipe your RIGHT INDEX finger 5 times on the sensor\n")
    fprint, img = dev.enroll_finger()
    if fprint is not None:
        fprint.save_to_disk(pyfprint.Fingers['RIGHT_INDEX'])
        print("Successfully enrolled!")
    if img is not None:
        img.save_to_file('enrolled.pgm')
        print("Wrote scanned image to enrolled.pgm")
    dev.close()
    pyfprint.fp_exit()

# capture()   # The function is executed here. (Nothing will happen with the above
# except the function is called in this form!) # Comment to disable

capture_to_disk(); # uncomment to use this function
