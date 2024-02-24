import os
import cv2
from   ultralytics import YOLO 

TEST_IMAGE = r'Images\bus.jpg'
MODEL      = r'Models\yolov8n.pt'

def process_video(model):
    test_image_path = os.path.join(os.getcwd(), TEST_IMAGE)
    results = model(test_image_path, save = True)

def main():
    model_path = os.path.join(os.getcwd(), MODEL)
    model = YOLO(model_path)
    process_video(model)


if __name__ == "__main__":
    main()