import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from functools import partial
import random
import math
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.srv import CatchTurtle
from turtlesim.srv import Kill


class TurtleSpawner(Node): 
    def __init__(self):
        super().__init__("turtle_spawner") 
        self.declare_parameter("turtle_name_prefix", "turtle")
        self.declare_parameter("spawn_frequency", 0.8)


        self.turtle_name_prefix = self.get_parameter("turtle_name_prefix").value
        self.spawn_frequency = self.get_parameter("spawn_frequency").value
        self.turtle_count = 0
        self.alive_turtles_ = []
        self.spawn_client = self.create_client(Spawn, "/spawn")
        self.kill_client = self.create_client(Kill, "/kill")
        self.alive_turtles_publisher = self.create_publisher(
            TurtleArray, "/alive_turtles", 10)
        self.catch_turtle_service = self.create_service(
            CatchTurtle, "/catch_turtle", self.catch_turtle_callback)
        self.spawn_turtle_timer = self.create_timer(1.0/self.spawn_frequency, self.spawn_new_turtle)


    def catch_turtle_callback(
            self, request: CatchTurtle.Request, response : CatchTurtle.Response):
        self.call_killservice(request.name)


        response.success = True
        return response

    
    def publish_alive_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.alive_turtles_publisher.publish(msg)
    
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
            new_turtle = Turtle()
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta
            self.alive_turtles_.append(new_turtle)
            self.publish_alive_turtles()


    def call_killservice(self,turtle_name):
        while not self.kill_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for kill service...")

        request = Kill.Request()
        request.name = turtle_name
       
        future = self.kill_client.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_killservice, turtle_name=turtle_name))

    def callback_call_killservice(self, future, turtle_name):
        for (i, turtle) in enumerate(self.alive_turtles_):
            if turtle.name == turtle_name:
                del self.alive_turtles_[i]
                self.publish_alive_turtles()
                break
               
        

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
