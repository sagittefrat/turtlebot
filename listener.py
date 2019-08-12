  #!/usr/bin/env python

    import rospy
    from geometry_msgs.msg import Pose

    def callback(data):
        variable_x = data.position.x
        rospy.loginfo(rospy.get_caller_id() + 'I heard %f', variable_x)

    def listener():
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('chatter', Pose, callback)
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

    if __name__ == '__main__':
        listener()
