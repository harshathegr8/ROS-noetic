#!/usr/bin/env python3
import rospy
from move_base_msgs.msg import MoveBaseActionGoal
import tf
from time import sleep
from geometry_msgs.msg import Quaternion
from actionlib_msgs.msg import GoalStatusArray
a = [(5,5,90),(5,-5,0),(-2,-5.5,180),(-2,4.5,60)]
class var:
    def __init__(self):
    	self.val = 0
i,c,j = var(),var(),var()
j.val = len(a)
def array_to_quaternion(nparr):
    quat = Quaternion()
    quat.x = nparr[0]
    quat.y = nparr[1]
    quat.z = nparr[2]
    quat.w = nparr[3]
    return quat
def callback(data):
    if c.val == 0:
    	talker(a[i.val])
    	c.val+=1
    if data.status_list[-1].text == "Goal reached.":
    	i.val+=1
    	if i.val==j.val:
    	   i.val=0
    	talker(a[i.val])
    	sleep(3)
    
def talker(goal):
    x,y,th = goal
    pub = rospy.Publisher("move_base/goal", MoveBaseActionGoal,queue_size=0)
    data = MoveBaseActionGoal()
    data.goal.target_pose.header.stamp = rospy.rostime.Time.now()
    data.header.stamp = rospy.rostime.Time.now()
    data.goal.target_pose.header.frame_id = 'map'
    data.goal.target_pose.pose.position.x,data.goal.target_pose.pose.position.y,data.goal.target_pose.pose.position.z = x,y,0
    quaternionArray = tf.transformations.quaternion_about_axis(th, (0,0,1))
    data.goal.target_pose.pose.orientation = array_to_quaternion(quaternionArray)
    rate = rospy.Rate(10) # 10hz
    c =0
    while not rospy.is_shutdown():
    	pub.publish(data)
    	rate.sleep()
    	c+=1
    	if c>10:break
def listener():
    global processing, new_msg, msg
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('moving', anonymous=True)
    rospy.Subscriber("move_base/status", GoalStatusArray, callback)
    # spin() simply keeps python from exiting until this node is stopped
    
    rospy.spin()

if __name__ == '__main__':
    listener()
