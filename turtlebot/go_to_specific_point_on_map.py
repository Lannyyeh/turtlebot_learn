#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
import green_patch_recognition as reco
import goincircles

class GoToPose():
    def __init__(self):

        self.goal_sent = False

	# What to do if shut down (e.g. Ctrl-C or failure)
	rospy.on_shutdown(self.shutdown)
	
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(180)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=False)
        navigator = GoToPose()
        # Customize the following values so they are appropriate for your location
        positions = ({'x': 1.04, 'y' : 0.28},{'x': 6.13, 'y' : -6.52},{'x': 8.43, 'y' : -5.25},{'x': 7.24, 'y' : -8.17},{'x': 10.33, 'y' : -11.9},{'x': 11.8, 'y' : -10.5})
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}
        for position in positions: #door to air-conditioner
            rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
            success = navigator.goto(position, quaternion)

            if success:
                rospy.loginfo("Hooray, reached the desired pose")
            else:
                rospy.loginfo("The base failed to reach the desired pose")

            #Sleep to give the last log messages time to be sent
            rospy.sleep(1)
        # rospy.init_node("vision_manager")
        rospy.loginfo("start")
        
        if reco.Image_converter().test_color=='R':
            print 'red'
            route_to_bed={'x':14.55,'y':-4.82}
            position=route_to_bed
            rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
            success = navigator.goto(position, quaternion)
            if success:
                rospy.loginfo("Hooray, reached the desired pose")
            else:
                rospy.loginfo("The base failed to reach the desired pose")
            # Sleep to give the last log messages time to be sent
            rospy.sleep(1)
            route_back=({'x': 10.33, 'y' : -11.9},{'x': 10.33, 'y' : -11.9},{'x': 11.8, 'y' : -10.5})
            for position in route_back: #fridge to air-conditioner
                rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
                success = navigator.goto(position, quaternion)
                if success:
                    rospy.loginfo("Hooray, reached the desired pose")
                else:
                    rospy.loginfo("The base failed to reach the desired pose")
                # Sleep to give the last log messages time to be sent
                rospy.sleep(1)
        elif reco.Image_converter().test_color=='G':
            print 'green'
            route_to_trash=({'x': 18.3, 'y' : -5.26},{'x': 18.3, 'y' : -5.26},{'x': 18.3, 'y' : -5.26},{'x': 18.41, 'y' : -5.17},{'x': 19.4536,'y':-5.02946})
            for position in route_to_trash: #fridge to air-conditioner
                rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
                success = navigator.goto(position, quaternion)
                if success:
                    rospy.loginfo("Hooray, reached the desired pose")
                else:
                    rospy.loginfo("The base failed to reach the desired pose")
                # Sleep to give the last log messages time to be sent
                rospy.sleep(1)
            goincircles.GoForward()
            route_back=({'x': 10.33, 'y' : -11.9},{'x': 10.33, 'y' : -11.9},{'x': 11.8, 'y' : -10.5})
            for position in route_back: #fridge to air-conditioner
                rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
                success = navigator.goto(position, quaternion)
                if success:
                    rospy.loginfo("Hooray, reached the desired pose")
                else:
                    rospy.loginfo("The base failed to reach the desired pose")
                # Sleep to give the last log messages time to be sent
                rospy.sleep(1)
        
        elif reco.Image_converter().test_color=='B':
            print 'blue'
            route_to_fridge=({'x':12.7,'y':4.56},{'x':12.7,'y':4.56},{'x':12.75,'y':4.6})
            for position in route_to_fridge: #air-conditioner to fridge
                rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
                success = navigator.goto(position, quaternion)
                if success:
                    rospy.loginfo("Hooray, reached the desired pose")
                else:
                    rospy.loginfo("The base failed to reach the desired pose")
                # Sleep to give the last log messages time to be sent
                rospy.sleep(1)
            rospy.sleep(4)
            route_back=({'x': 10.33, 'y' : -11.9},{'x': 10.33, 'y' : -11.9},{'x': 11.8, 'y' : -10.5})
            for position in route_back: #fridge to air-conditioner
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

