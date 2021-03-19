import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from go_to_specific_point_on_map import GoToPose

if __name__ == '__main__':
    try:
        navigator = GoToPose()

        position = {'x': 11.8, 'y' : -10.5}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, reached the desired pose")
        else:
            rospy.loginfo("The base failed to reach the desired pose")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")