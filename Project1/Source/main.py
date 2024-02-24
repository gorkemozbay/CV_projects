import os
import threading
from   ultralytics import YOLO 

from   Controllers.video_controller import VideoController

TEST_VIDEO = r'Videos\cars.mp4'
MODEL      = r'Models\yolov8n.pt'


def main():
    model_path = os.path.join(os.getcwd(), MODEL)
    model = YOLO(model_path)
    
    source_path = os.path.join(os.getcwd(), TEST_VIDEO)
    
    video_controller = VideoController(source_path, model)
    video_processor  = threading.Thread(target=video_controller.run)
    video_processor.start()
    
    video_processor.join()
    
if __name__ == "__main__":
    main()