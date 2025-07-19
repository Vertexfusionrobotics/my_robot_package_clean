# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import speech_recognition as sr

class AriListener(Node):
    def __init__(self):
        super().__init__('ari_listen_node')
        self.publisher_ = self.create_publisher(String, 'ari/input', 10)
        self.get_logger().info('🎤 ARI is now listening... Say something!')

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Call main loop once per second
        self.timer = self.create_timer(1.0, self.listen_and_publish)

    def listen_and_publish(self):
        with self.microphone as source:
            self.get_logger().info("🎙️ Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            self.get_logger().info(f"🗣️ Heard: {text}")
            msg = String()
            msg.data = text
            self.publisher_.publish(msg)
        except sr.UnknownValueError:
            self.get_logger().warn("❌ Could not understand audio.")
        except sr.RequestError as e:
            self.get_logger().error(f"⚠️ Could not request results; {e}")

def main(args=None):
    rclpy.init(args=args)
    node = AriListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
