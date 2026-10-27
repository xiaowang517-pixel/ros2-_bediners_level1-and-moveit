import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from functools import partial
import random
import math


class TurtleSpawner(Node): 
    def __init__(self):
        super().__init__("turtle_spawner") 
        self.turtle_name_prefix = "turtle"
        self.turtle_count = 0
        self.spawn_client = self.create_client(Spawn, "/spawn")
        self.spawn_turtle_timer = self.create_timer(2.0, self.spawn_new_turtle)
    def spawn_new_turtle(self):
        self.turtle_count += 1
        turtle_name = self.turtle_name_prefix + str(self.turtle_count)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2 * math.pi)
        self.call_spawnservice(turtle_name, x, y, theta)
       

    def call_spawnservice(self,turtle_name, x, y, theta):
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for spawn service...")

        request = Spawn.Request()
        request.name = turtle_name
        request.x = x
        request.y = y
        request.theta = theta
        future = self.spawn_client.call_async(request)
        future.add_done_callback(
            partial(self.spawn_response_callback, request=request))
    def spawn_response_callback(self, future, request):
        response = future.result()
        if response.name != "":
            self.get_logger().info("new alive turtle: " + response.name)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
