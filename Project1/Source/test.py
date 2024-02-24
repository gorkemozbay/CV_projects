import os
import cv2
from   ultralytics import YOLO 

TEST_IMAGE = r'Images\bus.jpg'
MODEL      = r'Models\yolov8n.pt'


def get_yolo_results(model, source_path):

    results = model(source_path, save=False, classes=[5])
    for result in results:
        boxes = result.boxes.cpu().numpy()
        xyxy = boxes.xyxy
        print(xyxy)


def cv2_test(source_path):
    while True:
        img = cv2.imread(source_path)
        cv2.imshow('before', img)
        img = cv2.rectangle(img, (17, 230), (801, 768), (0, 255, 0), 2)
        cv2.imshow('after', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    
    model_path = os.path.join(os.getcwd(), MODEL)
    model = YOLO(model_path)
    source_path = os.path.join(os.getcwd(), TEST_IMAGE)
    
    
    get_yolo_results(model, source_path)
    cv2_test(source_path)

    
        
if __name__ == "__main__":
    main()