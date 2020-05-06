#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import String
import paramiko


def main():
	rospy.init_node('RFF', anonymous=False, disable_signals=True)
	pub = rospy.Publisher('buttonpress', String, queue_size = 5)
	Button_State = False
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.connect('192.168.1.1', username='root')
	print("Connected.")

	while True:
		digin, digout, digerr = ssh.exec_command('gpio.sh get DIN1')
		digital_input = int(str(digout.readlines())[3])

		anain, anaout, anaerr = ssh.exec_command('analog_calc')
		# print(len(str(anaout.readlines())))
		analog_input = float(str(anaout.readlines())[3:-6])

		if digital_input == 0:
			if Button_State == False:
				timedown = time.time()
				rospy.loginfo("Button pressed.")
			Button_State = True
			pub.publish(str(Button_State))
			
		elif digital_input == 1:
			if Button_State == True:
				timeup = time.time()
				timeheld = timeup - timedown
				rospy.loginfo("Button released. Time held: %.2f", timeheld)
			Button_State = False
			pub.publish(str(Button_State))

		if 4.5 <= analog_input <= 5.5:
			rospy.loginfo("Fuel level normal.")

		elif 0 <= analog_input <= 3:
			rospy.loginfo("Fuel level low.")

		time.sleep(0.5)

	ssh.close()

if __name__=='__main__':
	main()