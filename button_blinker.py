#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import String
import paramiko


def callback(msg):
	global Button_State, ssh

	Button_State = msg.data
	if Button_State == "True":
		for i in range(20):
			stdin, stdout, stderr = ssh.exec_command('gpio.sh invert DOUT1')
			time.sleep(0.5)

def main():
	global ssh
	
	rospy.init_node('Blinker', anonymous=False, disable_signals=True)
	rospy.Subscriber('buttonpress', String, callback)
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.connect('192.168.1.1', username='root')
	print("Connected.")
	rospy.spin()

if __name__=='__main__':
	main()