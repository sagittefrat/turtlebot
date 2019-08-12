'''imports'''
import os,sys
import speedtest
import yaml
import time

# ROS related
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, PointStamped, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

data_path='./data/'
data_name='data_lab.json'

#rospy.init_node('get_data', anonymous=False)
def sample_place(place):
	''' 
	this func sample the requested features of the place the robot at 
	'''
	
	s = speedtest.Speedtest()
	#s.get_servers()
	ping=s.results.ping
	download=s.download()
	upload=s.upload()
	print(upload)
	return (place.x, place.y, int(time.time()),ping)#,upload,download)
	#return (place, time.time(), upload, download)

def callback(msg):
	pos=msg.pose.pose.position
	print(sample_place(pos))
	
    

rospy.init_node('check_odometry')
odom_sub = rospy.Subscriber('/odom', Odometry, callback)

rospy.spin()
    



    
for i in range(1800):
	pass	
	
	




