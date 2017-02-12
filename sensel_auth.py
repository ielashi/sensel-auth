#!/usr/bin/env python

from __future__ import print_function
from keyboard_reader import *
import matplotlib.pyplot as plt
import sensel

from features import ContactStream, Gesture, get_features, similarity_vector

exit_requested = False;

def keypress_handler(ch):
  global exit_requested
  global new_gesture

  if ch == 0x51 or ch == 0x71: #'Q' or 'q'
    print("Exiting gesture capture...", end="\r\n");
    exit_requested = True;


def getGesture():
  global exit_requested
  exit_requested = False

  sensel_device = sensel.SenselDevice()

  if not sensel_device.openConnection():
    print("Unable to open Sensel sensor!", end="\r\n")
    exit()

  sensel_device.writeReg(0x51, 1, bytearray([0]))
  sensel_device.writeReg(0x52, 1, bytearray([0]))
  sensel_device.writeReg(0x53, 1, bytearray([0]))
  sensel_device.writeReg(0x54, 1, bytearray([0]))

  keyboardReadThreadStart(keypress_handler)

  #Enable contact sending
  sensel_device.setFrameContentControl(
      sensel.SENSEL_FRAME_PRESSURE_FLAG
      | sensel.SENSEL_FRAME_LABELS_FLAG
      | sensel.SENSEL_FRAME_CONTACTS_FLAG)
  
  decompressed_cols = sensel_device.getDecompressedCols()
  decompressed_rows = sensel_device.getDecompressedRows()

  #Enable scanning
  sensel_device.startScanning()

  print("\r\nTouch sensor! (press 'q' to quit)...", end="\r\n")


  contact_stream = ContactStream()
  current_streams = {}
  all_streams = []

  gestures = []

  while not exit_requested: 
    frame = sensel_device.readFrame()
    if frame:
      (lost_frame_count, forces, labels, contacts) = frame

      if len(contacts) == 0:
        continue

      for c in contacts:
        event = ""
        if c.type == sensel.SENSEL_EVENT_CONTACT_INVALID:
          event = "invalid"; 
        elif c.type == sensel.SENSEL_EVENT_CONTACT_START:
          sensel_device.setLEDBrightness(c.id, 100) #Turn on LED
          event = "start"
          current_streams[c.id] = ContactStream()
        elif c.type == sensel.SENSEL_EVENT_CONTACT_MOVE:
          event = "move";
          current_streams[c.id].append(c)
        elif c.type == sensel.SENSEL_EVENT_CONTACT_END:
          sensel_device.setLEDBrightness(c.id, 0) #Turn off LED
          event = "end";
          all_streams.append(current_streams[c.id])
          del current_streams[c.id]
        else:
          event = "error";

        contact_stream.append(c)
    
        """
        print("Contact ID %d, event=%s, mm coord: (%f, %f), force=%.3f, " 
            "major=%f, minor=%f, orientation=%f" % 
            (c.id, event, c.x_pos, c.y_pos, c.total_force, 
             c.major_axis, c.minor_axis, c.orientation), end="\r\n")
        """


  sensel_device.stopScanning();
  sensel_device.closeConnection();
  keyboardReadThreadStop()

  print("Total streams:", len(all_streams))
  print(all_streams)
  return Gesture(all_streams)


def get_hand():
  print("Place hand...")
  sig = getGesture()
  
  # Signature must have 5 contact streams.
  while len(sig.contact_streams) != 5:
    print("Didn't have 5 contact points. Repeat please...")
    sig = getGesture()

  return sig


def add_user():
  hands = [get_hand(), get_hand(), get_hand()]

  feature_vectors = [get_features(h) for h in hands]

  hands[0].plot()

  return feature_vectors


USERS = dict()

if __name__ == "__main__":

  while True:
    print("""
    Welcome to Sensel Auth.

    Choose one of the options below:

    1) Add user
    2) Verify user
    3) Show user features
    4) Exit
    """)

    option = input('Enter #: ')

    if option == 1:
      name = raw_input("What's your name? ")
      USERS[name] = add_user()
    elif option == 2:
      gesture = get_features(get_hand())

      for (name, fv) in USERS.iteritems():
        print('Testing against', name)
        similarities = [similarity_vector(i, gesture) for i in fv]
        print(similarities)
    elif option == 3:
      print(USERS)
    elif option == 4:
      break
