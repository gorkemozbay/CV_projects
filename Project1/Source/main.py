import os
import cv2
import threading
from   ultralytics import YOLO 

import Utils.project_settings as ps
from   Controllers.UI_controller import UIController 


TEST_VIDEO = r'Videos\cars.mp4'
MODEL      = r'Models\yolov8n.pt'

def process_video(cap, model):
    while True:
        success, frame = cap.read()
        if success:
            results = get_YOLO_results(model, frame)
            annotated_frame = annotate_frame(results, frame)
            cv2.imshow('out', annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            pass


def annotate_frame(results, frame):
    for result in results:
        boxes = result.boxes.cpu().numpy()
        xyxys = boxes.xyxy
        for xyxy in xyxys:
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), ps.GREEN, ps.BBOX_THICKNESS)
    return frame


def get_YOLO_results(model, frame):
    results = model(frame, classes=[1,2,3,7], show=False)
    return results


def main():
    model_path = os.path.join(os.getcwd(), MODEL)
    model = YOLO(model_path)
    
    source_path = os.path.join(os.getcwd(), TEST_VIDEO)
    cap = cv2.VideoCapture(source_path)
    
    UI_controller = UIController()
    
    if not cap.isOpened():
        print("Failed to open source")
        exit()
    
    video_processor = threading.Thread(target=process_video, args=(cap, model,))
    video_processor.start()
    
    video_processor.join()
    
if __name__ == "__main__":
    main()