#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

from tf.transformations import euler_from_quaternion
from time import sleep


front = 0.0
left = 0.0
right = 0.0

roll = pitch = yaw = 0.0

def laser_callback(msg):
	global front,right,left
	right = min(min(msg.ranges[0:36]),10)		#0-36degrees
	front = min(min(msg.ranges[72:108]),10)  	#72-108 deg
	left = min(min(msg.ranges[144:180]),10)		#144-180 deg

def odom_callback(msg):
	global roll, pitch, yaw
	o = msg.pose.pose.orientation
	o_q = [o.x,o.y,o.z,o.w]

	(roll,pitch,yaw) = euler_from_quaternion(o_q)




rospy.init_node('bot_contoller')
msg = Twist()
msg.linear.x = 0.0
msg.angular.z = 0.0
pub = rospy.Publisher('/cmd_vel',Twist, queue_size = 10)
rospy.Subscriber('/scan_filtered',LaserScan,laser_callback)
rospy.Subscriber('/odom',Odometry,odom_callback)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
	if(front>0.5):
		msg.angular.z = 0
		msg.linear.x = 0.5
	
	
	else:
		msg.linear.x = 0
		if(right > left):
			msg.angular.z = -0.25
		else:
			msg.angular.z = +0.25	
	if left<0.3 and left>0.1:
		msg.angular.z = -0.25
	elif right<0.3 and right>0.1:
		msg.angular.z = 0.25
	if not front:
		msg.angular.z = 0
		msg.linear.x = -0.5
	pub.publish(msg)


	
