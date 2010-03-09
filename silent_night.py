""" Silences the phone between set hours

Meant for use on Android phones with the ASE application
"""

# Created by Christian Blades (christian.blades@docblades.com) - Mon Mar 08, 2010

import android
import datetime
from time import sleep

# MIN_HOUR and MAX_HOUR take an integer value between 0 and 23
# 12am == 0 and 1pm == 13
MIN_HOUR = 23
MAX_HOUR = 6

if MIN_HOUR > 23 or MIN_HOUR < 0 or MAX_HOUR > 23 or MAX_HOUR < 0:
    # If the min and max values are out of range, raise an error
    raise ValueError("0 <= (MIN_HOUR|MAX_HOUR) <= 23")

d_now = datetime.datetime.now

d_min = d_now().replace(hour=MIN_HOUR, minute=0, second=0)
d_max = d_now().replace(hour=MAX_HOUR, minute=0, second=0)

a_day = datetime.timedelta(days=1)

droid = android.Android()

def td_to_seconds(td):
    """ Convert a timedelta to seconds """
    return td.seconds + (td.days * 24 * 60 * 60)

def advance_times():
    """ Advance for the following day """
    d_min = d_min + a_day
    d_max = d_max + a_day
    return

def wait_for(dt):
    """ Wait until dt """
    sleep(td_to_seconds(dt - d_now()))

def main_loop():
    """
    Infinite loop that silences and unsilences the phone on schedule
    
    1. Wait for silent time
    2. Silence the phone
    3. Wait for awake time
    4. Turn on the ringer
    5. Advance the min and max to the following day
    6. Repeat
    
    NOTE: Must start during a loud period
    """
    while True:
        wait_for(d_min)
        droid.makeToast("Goodnight")
        droid.setRingerSilent(True)
        wait_for(d_max)
        droid.makeToast("Good morning")
        droid.setRingerSilent(False)
        advance_times()

t_now = d_now()

if MAX_HOUR < MIN_HOUR:
    # Do a little extra processing if we're going from
    # a larger hour to a smaller (ie: 2300 to 0600)
    if t_now.hour <= d_min.hour and t_now.hour < d_max.hour:
        # If it's, say, 0200 currently and we're going from 2300 to 0600
        # Make the 2300 minimum for the previous night      
        d_min = d_min - a_day
    elif t_now.hour >= d_min.hour and t_now.hour > d_max.hour:
        # In this case, it's 0900 and we're going from 2300 to 0600
        # Make the maximum for the next morning
        d_max = d_max + a_day

print "Now: " + t_now.ctime()
print "Min: " + d_min.ctime()
print "Max: " + d_max.ctime()

if t_now >= d_min and t_now < d_max:
    # Is it silent time now?
    # If so, do the silent stuff, then enter the loop
    droid.makeToast("Goodnight")
    droid.setRingerSilent(True)
    wait_for(d_max)
    droid.setRingerSilent(False)
    advance_times()

main_loop()
