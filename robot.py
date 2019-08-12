#!/usr/bin/env python

# ROS related

'''imports'''
import os,sys
import rospy
import pyspeedtest
import yaml


from go_to_specific_point_on_map import GoToPose 
import util
from db import DB

#TODO - all
#TODO - decide how to relate each time to a time in the db

class InitializeRobot:
	''' 
	this class initialize the turtlebot for the first time
	'''
	def __init__(self,DB):
	
		# no need
		#self.create_map()
		
		'''list of the important places:'''
		self.locations=self.initialize_locations()

		self.full_data_directory=self.make_directory()


		'''hard coded initialization'''
		if self.locations==[]:
			#demo locations!!! need to ba change when there is a map'''
			'''read info from yaml file:'''
			with open(self.full_data_directory+"/../data/places.yaml",'r') as stream:
				total_route=yaml.load(stream)
				for loc in total_route:
					self.locations.append(loc)
					#print self.full_data_directory+"/../data/places.yaml"
			######################################################
		
		self.dock=self.initialize_dock
		self.DB=DB
		self.robot=Robot(self)

	def make_directory(self):
		script_dirname=os.path.dirname(os.path.abspath(__file__))

		'''default directory is same directory as script'''
		if len(sys.argv)<2:
			return script_dirname

		data_directory=sys.argv[1]
		return os.path.join(script_dirname+"/../"+data_directory)


	#TODO
	def initialize_locations(self):
		''' 
		this func define the locations by name 
		'''
		
		return []
		
	#TODO
	def initialize_dock(self):
		''' 
		this func define the dock 
		'''
		pass
	
class Robot:
	''' 
	this class maintain the reguler actions of the robot
	'''
	def __init__(self,rob):
		
		self.features=['place','time','day'].append(list(util.FEATURES))
		self.places_names_list=rob.locations
		self.rob=rob
		self.full_data_directory=rob.full_data_directory

		#this flag make sure that when a request is sent to robot, no other request will start process
		self.working_flag=False

		#initialize rob:
		#rospy.init_node('robot',anonymous=False)
		print 'create robot'
		print self

	#TODO
	def in_dock(self):
		'''
		this func checks if turty in his ducking station
		'''
		return True
		
	#no need
	def update_locations(self,location_name,method='update',location_coordinate=None):
		''' 
		this func update locations. recieves location and create or delete it
		'''
		loc=self.find_location(location_name)
		
		if method==delete:
			if loc==None:
				return 'no_loc'
			self.places_names_list.delete(loc)
		else:
			if loc==None:
				#TODO-create_new_loc:location_name,location_coordinate
				pass
			else:
				#TODO-update_exist_loc:location_name,location_coordinate
				pass	
		
			
	#no need
	#Sagitt - maybe will be hard coded and no need of this func
	def update_dock(self, location):
		''' 
		this func define a new place. recieves x,y returns name into places_names_list
		'''
		pass
	
	
	#no need
	def update_temp_db(self,sample_features):
		'''
		this func updates the db with the list of samples_features
		'''
		pass
	
	
	def sample_places_list(self, places_names=None):
		'''
		this func recieves a tuple of places names, find route and sends the robot to sample according to route
		'''
		if places_names is None:
			places_names=self.places_names_list

		self.working_flag=True
		total_route=self.find_route(places_names)


		#demo route!!! need to be changed when there is a map:
		'''read info from yaml file:'''
		with open(self.full_data_directory+"/route.yaml",'r') as stream:
			total_route=yaml.load(stream)
		###############################################

		self.send_robot_to_sample_according_to_route(total_route)
		#self.update_db()
		self.return_to_dock()
		self.rob.DB.update_db()
		self.working_flag=False
	
	#TODO - Sagitt
	def send_robot_to_sample_according_to_route(self,total_route):
		'''
		this func recieves a route and moves the robot accordingly, sample the location and updates the db 
		'''
		places_feature=[]
		for place in total_route:
			while(self.move_robot_to_place(place)==False):continue
			places_feature.append(self.sample_place(place))
			
		self.update_temp_db(places_feature)
		print places_feature
					

	#TODO - find a func online, try github
	def find_route(self, places_names):
		''' 
		this func recieves a tuple of places names, returns a route 
		'''
		return None
	
	
	def sample_place(self,place,features=util.FEATURES):
		''' 
		this func sample the requested features of the place the robot at 
		'''
		today=util.get_today()
		
		speed_test = pyspeedtest.SpeedTest()
		ping=speed_test.ping()
		upload=speed_test.upload()
		download=speed_test.download()

		return (place,util.timeConvert(today['time']),today['day'],ping,upload,download)
	
	#TODO - Sagitt
	def move_robot_to_place(self,position):
		''' 
		this func move the robot into place. check the place coordinate and the make him walk there 
		'''
		#TODO - while (robot not in place)
		'''taken from: https://github.com/markwsilliman/turtlebot/blob/master/follow_the_route.py'''
		try:
			# Initialize
			#rospy.init_node('follow_route', anonymous=False)
			navigator = GoToPose()


			# Navigation
			rospy.loginfo("Go to %s pose", name[:-4])
			success = navigator.goto(place['position'], place['quaternion'])
			if success==False:
				rospy.loginfo("Failed to reach %s pose", name[:-4])
				return False
			rospy.loginfo("Reached %s pose", position['x'], position['y'])
			return True

			#rospy.sleep(1)

		except rospy.ROSInterruptException:
			rospy.loginfo("Ctrl-C caught. Quitting")
			return True
		
	#TODO 
	def return_to_dock(self):
		''' 
		this func move the robot to its dock and updates the cloud db
		'''
		pass
'''		
db=DB()		
rob=InitializeRobot(db).robot
print rob.sample_place('nili')
'''
