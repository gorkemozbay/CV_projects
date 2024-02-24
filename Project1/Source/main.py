import os
import cv2
from   ultralytics import YOLO 

TEST_IMAGE = r'Images\bus.jpg'
TEST_VIDEO = r'Videos\cars.mp4'
MODEL      = r'Models\yolov8n.pt'

def process_video(model):
    source_path = os.path.join(os.getcwd(), TEST_VIDEO)
    results = model(source_path, classes=[1,2,3,7] ,show=True)


def main():
    model_path = os.path.join(os.getcwd(), MODEL)    
    print(model_path)
    model = YOLO(model_path)
    
    process_video(model)
    
    
if __name__ == "__main__":
    main()