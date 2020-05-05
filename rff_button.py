#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import String
import subprocess

class Button():

	def __init__(self):
		self.dinput = 1
		self.status = False
		self.timedown = 0
		self.timeup = 0
		self.hold = 0
		# Set publisher
		self.pub = rospy.Publisher('buttonpress', String, queue_size = 5)
		rospy.init_node('Button', anonymous=False)
		self.rate = rospy.Rate(5)
		
	def checkPress(self):
		while not rospy.is_shutdown():
			try:
				self.dinput = subprocess.check_output(["ssh", "root@192.168.1.1", "gpio.sh get DIN1"], shell=False)
				self.ainput = subprocess.check_output(["ssh", "root@192.168.1.1", "analog_calc"], shell=False)
				self.analog = float(str(self.ainput).strip("V\n"))
				if self.analog <= 4:
					rospy.loginfo("Fuel level below 50%")

				else:
					rospy.loginfo("Fuel level above 50%")
		
				if self.dinput == "0\n":
					if self.status == False:
						self.timedown = time.time()
						rospy.loginfo("pressed: %f", self.timedown)
					self.status = True
					self.pub.publish(str(self.status))
					
				elif self.dinput == "1\n":
					if self.status == True:
						self.timeup = time.time()
						rospy.loginfo("released: %f", self.timeup)
					self.status = False
					self.pub.publish(str(self.status))
					
				else:
					rospy.loginfo("Invalid Digital Input")

				if self.timedown > self.timeup:
					if (time.time() - self.timedown) > 1.2:
						rospy.loginfo("Long press")
					else:
						pass

				else:
					if self.hold == self.timeup - self.timedown:
						pass
					else:
						self.hold = self.timeup - self.timedown
						rospy.loginfo("Time held: %f", self.hold)

			except(subprocess.CalledProcessError):
				rospy.logwarn("SSH process into router terminated.")

			self.rate.sleep()

if __name__=='__main__':
	run = Button()
	run.checkPress()