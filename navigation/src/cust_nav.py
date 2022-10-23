#!/usr/bin/env python3

import rospy
from time import sleep
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from tf.transformations import euler_from_quaternion
from time import sleep


front = 0.0
left = 0.0
right = 0.0

roll = pitch = yaw = 0.0


def odom_callback(msg):
	global roll, pitch, yaw
	o = msg.pose.pose.orientation
	o_q = [o.x,o.y,o.z,o.w]

	(roll,pitch,yaw) = euler_from_quaternion(o_q)



x = 40
rospy.init_node('bot_contoller')
msg = Twist()
msg.linear.x = 0.0
msg.angular.z = 0.0
pub = rospy.Publisher('/cmd_vel',Twist, queue_size = 10)
rospy.Subscriber('/odom',Odometry,odom_callback)
t = 0.44
rate = rospy.Rate(10)
r = 0
while not rospy.is_shutdown():
	if r<=x:
		msg.angular.z = 0
		msg.linear.x = 0.5
	elif r>x and r<=2*x:
		msg.linear.x = 0
		msg.angular.z = t
	elif r>2*x and r<=3*x:
		msg.angular.z = 0
		msg.linear.x = 0.5
	elif r>3*x and r<=4*x:
		msg.angular.z = t
		msg.linear.x = 0
	elif r>4*x and r<=5*x:
		msg.angular.z = 0
		msg.linear.x = 0.5
	elif r>5*x and r<=6*x:
		msg.angular.z = t
		msg.linear.x = 0
	elif r>6*x and r<=7*x:
		msg.angular.z = 0
		msg.linear.x = 0.5
	elif r>7*x and r<=8*x:
		msg.angular.z = t
		msg.linear.x = 0
	else:
		r = 0
	r+=1
	pub.publish(msg)
	sleep(0.1)

