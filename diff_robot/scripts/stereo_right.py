#!/usr/bin/env python3
import rospy
from  sensor_msgs.msg import CameraInfo
def callback(data):
    talker(data)
def talker(data):
    
    pub = rospy.Publisher('camera/rgb/camera_info22', CameraInfo, queue_size=0)
    rate = rospy.Rate(10) # 10hz
    l = list(data.P)
    
    l[3] = -0.12*l[0]
    data.P = tuple(l)
    pub.publish(data)
    rate.sleep()
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('fil', anonymous=True)

    rospy.Subscriber("camera/rgb/camera_info2", CameraInfo, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
