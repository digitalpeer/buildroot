#!/usr/bin/python

#
# Robot Arm Wii Remote Controller
# Joshua Henderson <digitalpeer@digitalpeer.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#

import cwiid
import time
import string
import os

# default/current duty cycles
duty_cycles = [150,
               180,
               80,
               150,
               130,
               150]

# maximum positions
maxes = [230,
         226,
         142,
         230,
         230,
         230]

# minimum positions
mins = [50,
        50,
        80,
        50,
        130,
        50]

# fastest time an update to a servo can occur
min_updates = [0.05,
               0.05,
               0.05,
               0.05,
               0.05,
               0.03]

# how much to increment each update
increments = [1,
              2,
              2,
              5,
              10,
              5]

def connect_remote(): 
   global wm
   print 'Press buttons 1 & 2 or the red button next to the battery...'
   time.sleep(1)

   while True:
      try:
         wm = cwiid.Wiimote()
         break
      except RuntimeError:
         print 'Error opening wiimote connection. Trying again...'
         time.sleep(1)

   wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_NUNCHUK | cwiid.RPT_STATUS
   print 'Wiimote connected .. Press HOME button to quit'

def rumble(): 
   wm.rumble = True
   time.sleep(.2)
   wm.rumble = False

dev_base = "/dev/rpio-pwm"

def servo_set(i, duty_cycle): 
   command = "%d=%d\n" % (i, duty_cycle)
   with open(dev_base, "w") as f:
      f.write(command)
   print command,
   time.sleep(min_updates[i])

def servo_init(i, duty_cycle):
   move_abs(i, duty_cycle)
   print "Initialized PWM %d" % i

def move_abs(i, val):
   global duty_cycles
   duty_cycles[i] = val;
   if duty_cycles[i] < mins[i]:
      duty_cycles[i] = mins[i]
      rumble()
   elif duty_cycles[i] > maxes[i]:
      duty_cycles[i] = maxes[i]
      rumble()
   servo_set(i, duty_cycles[i])

def move(i, inc):
   global duty_cycles
   duty_cycles[i] += inc;
   move_abs(i, duty_cycles[i])
   if recording == True:
      record(i, duty_cycles[i])

recording = False
record_base = "/tmp/record.dat"

def play():
   try:
      lines = [line.strip() for line in open(record_base)]
   except:
      print "No record file found."
      return

   prev = 0
   for line in lines:
      if wm.state['buttons'] & cwiid.BTN_HOME:
         break
      tokens = [int(x) for x in string.split(line, " ")]
      if prev == 0:
         prev = tokens[0]
      time.sleep(float(tokens[0] - prev) / 1000.0)   
      move_abs(tokens[1], tokens[2])
      prev = tokens[0]

def record_start():
   os.remove(record_base)
   # save off current servo position at start of record
   for i in range(len(duty_cycles)):
      record(i, duty_cycles[i])

def record(i, duty_cycle): 
   with open(record_base, "a+") as f:
      f.write("%d %d %d\n" % (time.time() * 1000, i, duty_cycle))

def handle_button(i, inc_btn, dec_btn):
   if wm.state['buttons'] & inc_btn:
      move(i, increments[i])
   elif wm.state['buttons'] & dec_btn:   
      move(i, -increments[i])

def robot(): 
   global recording

   SERVO_BASE = 0
   SERVO_SHOULDER = 1
   SERVO_ELBOW = 2
   SERVO_GRIPPER = 4
   SERVO_GRIPPER_ROTATE = 5

   connect_remote()

   print 'Battery:', int(100.0 * wm.state['battery'] / cwiid.BATTERY_MAX)

   for i in range(len(duty_cycles)):
      servo_init(i, duty_cycles[i])

   wm.led = cwiid.LED1_ON

   state = 0

   while True:

      if 'nunchuk' in wm.state.keys():
         if wm.state['nunchuk']['buttons'] & cwiid.NUNCHUK_BTN_C:
            if state == 0:
               state = 1
               wm.led = cwiid.LED2_ON
               print 'start new recording'
               recording = True
               record_start()
            elif state == 1:
               print 'recording stopped'
               wm.led = cwiid.LED1_ON
               state = 0
               recording = False
            time.sleep(0.5)
 
         if wm.state['nunchuk']['buttons'] & cwiid.NUNCHUK_BTN_Z:
            if state == 0:
               state = 2
               wm.led = cwiid.LED3_ON
               print 'playing'
               play()
               wm.led = cwiid.LED1_ON
               state = 0
            time.sleep(0.5)

      if wm.state['buttons'] & cwiid.BTN_HOME:
         print 'closing wiimote connection..'
         exit(wm)

      handle_button(SERVO_BASE, cwiid.BTN_LEFT, cwiid.BTN_RIGHT) 
      handle_button(SERVO_ELBOW, cwiid.BTN_DOWN, cwiid.BTN_UP) 
      handle_button(SERVO_SHOULDER, cwiid.BTN_2, cwiid.BTN_1) 
      handle_button(SERVO_GRIPPER_ROTATE, cwiid.BTN_PLUS, cwiid.BTN_MINUS) 
      handle_button(SERVO_GRIPPER, cwiid.BTN_B, cwiid.BTN_A) 

if __name__ == "__main__":
    robot()
