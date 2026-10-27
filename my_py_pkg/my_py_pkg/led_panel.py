#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedStateArray 
from my_robot_interfaces.srv import SetLed

class LedPanelNode(Node): 
    def __init__(self):
        super().__init__("led_panel_node")
        self.led_states_pub_ = self.create_publisher(
            LedStateArray, "led_states", 10)
        self.led_states = [0,0,0]  # Example LED states
        self.get_logger().info("LED Panel Node has been started.")
        self.set_led_service_ = self.create_service(
            SetLed, "set_led", self.callback_set_led)
        self.timer_ = self.create_timer(
            5.0, self.publish_led_states)
    def publish_led_states(self):
        msg = LedStateArray()
        msg.led_states = self.led_states
        self.led_states_pub_.publish(msg)
    def callback_set_led(self, request: SetLed.Request, response: SetLed.Response):
        led_number = request.led_number
        state = request.led_state
        if led_number < 0 or led_number >= len(self.led_states):
            response.success = False
            return response
        if state not in [0, 1]:
            response.success = False
            response.message = "Invalid state. Use 0 for OFF and 1 for ON."
            return response
        self.led_states[led_number] = state
        response.success = True
        self.publish_led_states()
        return response
def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
