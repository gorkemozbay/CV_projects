import threading
import cv2
import mediapipe as mp

from Controllers.VideoController import VideoController

def main():
    cap = cv2.VideoCapture(0)
    model = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
    
    video_controller = VideoController(cap, model)
    video_processor = threading.Thread(target=video_controller.run)
    video_processor.start()
    video_processor.join()

if __name__ == "__main__":
    main()