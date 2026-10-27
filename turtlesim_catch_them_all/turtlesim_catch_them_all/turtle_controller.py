#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.pose_: Pose = None
        self.target_x_ = 8.0
        self.target_y_ = 4.0
        self.pose_subscriber_ = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10)
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "/turtle1/cmd_vel", 10)
        self.control_timer_ = self.create_timer(0.1, self.control_loop)
    def pose_callback(self, pose: Pose):
        self.pose_ = pose
    def control_loop(self):
        if self.pose_ is None:
           return
        dist_x = self.target_x_ - self.pose_.x
        dist_y = self.target_y_ - self.pose_.y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        cmd = Twist()

        if distance > 0.1:
           cmd.linear.x = 2 * distance
           goal_theta = math.atan2(dist_y, dist_x)
           diff_theta = goal_theta - self.pose_.theta
           if diff_theta > math.pi:
               diff_theta -= 2 * math.pi
           elif diff_theta < -math.pi:
               diff_theta += 2 * math.pi
           cmd.angular.z = 6 * diff_theta

            
        else:
           cmd.linear.x = 0.0
           cmd.angular.z = 0.0
        self.cmd_vel_publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleController() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
