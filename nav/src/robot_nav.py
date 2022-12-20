#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from time import sleep
msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""
moveBindings = {
        'i':(1,0,0,0),
        'u':(1,0,0,1),
        'l':(0,0,0,-1),
        'j':(0,0,0,1),
        'o':(1,0,0,-1),
        ',':(-1,0,0,0),'s':(-1,0,0,0),
        'm':(-1,0,0,-1),
        '.':(-1,0,0,1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }
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
			msg.angular.z = +0.27	
	if left<0.3 :
		msg.angular.z = -0.25
	elif right<0.3 :
		msg.angular.z = +0.25
	if not front:
		msg.angular.z = 0
		msg.linear.x = -0.5
	pub.publish(msg)


	
