# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import rclpy
from rclpy.node import Node
import os

class HelloNode(Node):
    def __init__(self):
        super().__init__('hello_node')
        self.i = 1
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        text = f"Counting: {self.i}"
        self.get_logger().info(text)
        os.system(f'espeak -v mb-us2 "{text}" --stdout | aplay')  # Better quality output
        self.i += 1
        if self.i > 5:  # Stops after 5 counts
            self.destroy_timer(self.timer)
            self.get_logger().info("Done counting.")

def get_greeting_response():
    return "Hello! I am ARI, your friendly robot assistant."

def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
