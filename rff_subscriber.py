#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import subprocess

class ButtonSubscriber():

	def __init__(self):
		self.status = ""
		rospy.init_node('ButtonSubscriber', anonymous=False)
		# Set subscriber
		rospy.Subscriber('buttonpress', String, self.get_press)
		self.rate = rospy.Rate(2)

	def get_press(self, msg):
		self.status = msg.data

	def main(self):
		while not rospy.is_shutdown():
			rospy.loginfo(self.status)
			self.rate.sleep()

if __name__=='__main__':
	run = ButtonSubscriber()
	run.main()
