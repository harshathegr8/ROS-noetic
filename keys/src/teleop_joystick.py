#!/usr/bin/env python3

from __future__ import print_function
import threading
import rospy
import roslib; roslib.load_manifest('teleop_twist_keyboard')
from geometry_msgs.msg import Twist
import sys, select, termios, tty
import pygame as pg
from time import sleep
import pygame.joystick as js
import pygame.event as ev

msg ="""
Left joy - forward/reverse
------------------------
LT - left
RT - right
------------------------
"""
def direc(l,r,f):
	
    if l>0:
    	if f>0:
    	   return [1,0,0,-1]
    	elif f<0:
    	   return [-1,0,0,1]
    	return [0,0,0,-1]
    elif r>0:
    	if f>0:
    	   return [1,0,0,1]
    	elif f<0:
    	   return [-1,0,0,-1]
    	return [0,0,0,1]
    elif f>0:
    	return [1,0,0,0]
    elif f<0:
    	return [-1,0,0,0]
    return [0,0,0,0]
def con(speed,turn,w,v):
    if v==-1:
    	a,b = [1,0.9]
    elif w==1:
    	a,b =[1.1,1]
    elif v ==1:
    	a,b = [1,1.1]
    elif w==-1:
    	a,b = [0.9,1]
    else:
    	a,b= [1,1]
    speed,turn = speed*a,turn*b
    if (a+b)!=2:
    	print(vels(speed,turn))
    return [speed,turn]
class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def run(self):
        twist = Twist()
        while not self.done:
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twist)

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist)

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)
settings = termios.tcgetattr(sys.stdin)
rospy.init_node('teleop_twist_joystick')
speed = rospy.get_param("~speed", 0.5)
turn = rospy.get_param("~turn", 1.0)
repeat = rospy.get_param("~repeat_rate", 0.0)
key_timeout = rospy.get_param("~key_timeout", 0.0)
if key_timeout == 0.0:
        key_timeout = None
pub_thread = PublishThread(repeat)

a,run = 1,True
pg.init()
joys = [js.Joystick(i) for i in range(js.get_count())]
screen = pg.display.set_mode((100, 100))
clock = pg.time.Clock()
x = 0
y = 0
z = 0
th = 0
status = 0
try:
    pub_thread.wait_for_subscribers()
    pub_thread.update(x, y, z, th, speed, turn)
    print(msg)
    print(vels(speed,turn))
    while run:
        a,b=0,0
        if js.get_count()>0 and a==0:
            pg.init()
            joys = [js.Joystick(i) for i in range(js.get_count())]
            for joy in joys:
                joy.init()
            a = 1
        elif js.get_count()==0 and a==1:
            a = 0
        for event in ev.get():
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 6:
                	run =False
                	pg.quit()
                	pub_thread.stop()
                	break
        
        for joy in joys:
            l,r = round(joy.get_axis(2),1),round(joy.get_axis(5),1)
            f = -round(joy.get_axis(1),1)
            #print(l,r,f)
            v,w = joy.get_hat(0)
            
            #print(v,w)
        x, y, z, th = direc(l,r,f)
        speed,turn = con(speed,turn,w,v)
        
        #print(x,y,z,th)
        sleep(0.1)
        pub_thread.update(x, y, z, th, speed, turn)
except Exception as e:
    print(e)
finally:
    pub_thread.stop()
pg.quit()
        
    

