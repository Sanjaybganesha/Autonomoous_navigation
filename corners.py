import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point 

class map_navigation():
	def __init__(msg): 
		msg.xCorner4 =  -1.424
		msg.yCorner4 = 3.252
		msg.xCorner3 = -5.86
		msg.yCorner3 = 0.9027
		msg.xCorner2 = -4.79
		msg.yCorner2 = -2.89
		msg.xCorner5 = -6.09
		msg.yCorner5 = -6.98
		msg.xCorner6 = -9.248
		msg.yCorner6 = -0.759

		msg.goalReached = False
		
        	rospy.init_node('map', anonymous=False)
		choice = 0
		
		if (choice == 0):
			while(not msg.goalReached):
				msg.goalReached = msg.moveToGoal(msg.xCorner4, msg.yCorner4)
				if (msg.goalReached):
					rospy.loginfo("Reached End of lab!")
			msg.goalReached = False
			while(not msg.goalReached):
				msg.goalReached = msg.moveToGoal(msg.xCorner5, msg.yCorner5)	
				if (msg.goalReached):
					rospy.loginfo("Reached outside the door to the left!")
			msg.goalReached = False
			while(not msg.goalReached):	
				msg.goalReached = msg.moveToGoal(msg.xCorner6, msg.yCorner6)
				if (msg.goalReached):
					rospy.loginfo("Reached outside the door to the right!")
			msg.goalReached = False
			while(not msg.goalReached):
				msg.goalReached = msg.moveToGoal(msg.xCorner2, msg.yCorner2)	
				if (msg.goalReached):
					rospy.loginfo("Reached at the corner in front of lab! ")
		
		


	def shutdown(self):
        	rospy.loginfo("Quit program")
        	rospy.sleep()

	def moveToGoal(self,xGoal,yGoal):

		move = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		while(not move.wait_for_server(rospy.Duration.from_sec(5.0))):
			rospy.loginfo("Waiting for the move_base action server to come up")
		simplegoal = MoveBaseGoal()
		simplegoal.target_pose.header.frame_id = "map"
		simplegoal.target_pose.header.stamp = rospy.Time.now()

		simplegoal.target_pose.pose.position =  Point(xGoal,yGoal,0)
		simplegoal.target_pose.pose.orientation.x = 0.0
		simplegoal.target_pose.pose.orientation.y = 0.0
		simplegoal.target_pose.pose.orientation.z = 0.0
		simplegoal.target_pose.pose.orientation.w = 1.0

		rospy.loginfo("Sending Next goal location ")
		move.send_goal(simplegoal)
		move.wait_for_result(rospy.Duration(60))

		if(move.get_state() ==  GoalStatus.SUCCEEDED):
			rospy.loginfo("This is the end of navigation")	
			return True
	
		else:
			rospy.loginfo("The robot failed to reach the destination")
			return False

if __name__ == '__main__':
    try:
	
	rospy.loginfo("Reached")
        map_navigation()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("map_navigation node terminated.")
