#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__("py_test")  # 节点名字 py_test
        self.counter_ = 0
        self.get_logger().info("Hello world")
        self.create_timer(1.0, self.timer_callback) # 1秒回调一次

    def timer_callback(self):
        self.get_logger().info("Hello " + str(self.counter_))
        self.counter_ += 1

def main(args=None):
    rclpy.init(args=args)       # 初始化ros2通信
    node = MyNode()
    rclpy.spin(node)            # 循环等待回调，阻塞
    rclpy.shutdown()            # 关闭ros2

if __name__ == "__main__":
    main()
