#!/usr/bin/env python

import rospy
import math 
import sys
import time
from numpy import sign

from geometry_msgs.msg import PoseWithCovarianceStamped 
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist



def tb0_get_rotation(msg): 
    global roll, pitch, yaw, tb0_X, tb0_Y, tb0_yaw
    orientation_q = msg.pose.pose.orientation 
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w] 
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    tb0_X = msg.pose.pose.position.x
    tb0_Y = msg.pose.pose.position.y
    tb0_yaw = math.degrees(yaw)
    return tb0_X, tb0_Y, tb0_yaw

def tb1_get_rotation(msg): 
    global tb1roll, tb1pitch, tb1yaw, tb1_X, tb1_Y, tb1_yaw
    orientation_q = msg.pose.pose.orientation 
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w] 
    (tb1_roll, tb1_pitch, tb1_yaw) = euler_from_quaternion(orientation_list)
    tb1_X = msg.pose.pose.position.x
    tb1_Y = msg.pose.pose.position.y
    #tb1_yaw = math.radians(tb1_yaw)
    return tb1_X, tb1_Y, tb1_yaw



if __name__ == "__main__":
    global roll, pitch, yaw, tb0_X, tb0_Y, tb0_yaw,tb1roll, tb1pitch, tb1yaw, tb1_X, tb1_Y, tb1_yaw
    roll = pitch = yaw = 0.0
    tb1_roll = tb1_pitch = tb1_yaw = 0.0
    tb1_X = tb0_X = tb1_Y = tb0_Y = 0.0
    maxlv = 0.22
    rospy.init_node('leader_follower')
    r = rospy.Rate(10) 
    tb0_sub = rospy.Subscriber('/tb3_0/amcl_pose', PoseWithCovarianceStamped, tb0_get_rotation) # geometry_msgs/PoseWithCovariance pose
    tb1_sub = rospy.Subscriber('/tb3_1/amcl_pose', PoseWithCovarianceStamped, tb1_get_rotation)
    velocity_publisher = rospy.Publisher('/tb3_1/cmd_vel', Twist, queue_size=10)
    while not rospy.is_shutdown(): 
        #tb0_quat = quaternion_from_euler(roll, pitch,yaw) #print(quat)     
        #tb1_quat = quaternion_from_euler(tb1roll, tb1pitch, tb1yaw)
        dist = math.sqrt((tb1_X-tb0_X)**2+(tb1_Y-tb0_Y)**2)
        course = math.atan2(tb0_Y-tb1_Y,tb0_X-tb1_X)
        dhdg = course-tb1_yaw
        print("dist: ", dist)
        print("course: ", course)
        print("tb1_yaw: ", tb1_yaw)
        #if dhdg < -(math.pi):
        #    dhdg = dhdg + (2*(math.pi))
        #elif dhdg > math.pi:
        #    dhdg = dhdg - (2*(math.pi))
        print("dhdg: ", dhdg)
        KpVel = 0.5
        KpAng = 0.5
        linvel = KpVel*(dist-0.5)
        angvel = KpAng*dhdg;
        if abs(dhdg) > (20.0*(math.pi)/180):
            linvel =0.0
        if abs(linvel) > maxlv:
            linvel = sign(linvel) * maxlv
        print("angvel: ", angvel)
        vel_msg = Twist()
        vel_msg.linear.x = linvel
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = angvel
        velocity_publisher.publish(vel_msg)
        r.sleep()
    rospy.spin()




             
