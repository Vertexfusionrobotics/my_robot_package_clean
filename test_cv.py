# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import cv2
import sys
import traceback

def global_exception_hook(exctype, value, tb):
    print("UNCAUGHT EXCEPTION:", exctype, value)
    traceback.print_tb(tb)
    sys.exit(1)

sys.excepthook = global_exception_hook

cap = cv2.VideoCapture("ari_videos/ari_talking_video_fixed.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("test", frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

