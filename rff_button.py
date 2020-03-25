#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import subprocess

class Button():

	def __init__(self):
		self.dinput = 1

		# Set publisher
		self.pub = rospy.Publisher('buttonpress', String, queue_size = 5)
		rospy.init_node('Button', anonymous=False)
		self.rate = rospy.Rate(2)

	def checkPress(self):
		while not rospy.is_shutdown():
			try:
				self.dinput = subprocess.check_output(["ssh", "root@192.168.1.1", "gpio.sh get DIN1"], shell=False)
		
				if self.dinput == "0\n":
					self.pub.publish("Button has been pressed")
					rospy.loginfo("Button has been pressed")

				elif self.dinput == "1\n":
					self.pub.publish("Button not pressed")
					rospy.loginfo("Button not pressed")

				else:
					self.pub.publish("Invalid Digital Input")
					rospy.loginfo("Invalid Digital Input")

			except(subprocess.CalledProcessError):
				rospy.logwarn("SSH process into router terminated.")

			self.rate.sleep()

if __name__=='__main__':
	run = Button()
	run.checkPress()
