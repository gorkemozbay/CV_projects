import cv2
import Utils.project_settings as ps

class VideoController():
    
    def __init__(self, source, model):
        print("VideoController is created")
        self.cap = cv2.VideoCapture(source)
        self.model = model
        self.current_frame = None
        self.line_list = []
        
                
    def draw_line(frame, point_1, point_2, color, thickness):
        cv2.line(frame, (point_1.x, point_1.y), (point_2.x, point_2.y), color, thickness)
        return frame
    
    
    def get_YOLO_results(self, frame):
        results = self.model(frame, classes=[1,2,3,7], show=False)
        return results


    def annotate_frame(self, results, frame):
        for result in results:
            boxes = result.boxes.cpu().numpy()
            xyxys = boxes.xyxy
            for xyxy in xyxys:
                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), ps.GREEN, ps.BBOX_THICKNESS)
        return frame
    
    
    def add_lines(self):
        for line in self.line_list:
            pass
    
    
    def run(self):
        
        if not self.cap.isOpened():
            print("Failed to open source")
            exit()
        
        while True:
            success, frame = self.cap.read()
            if success:
                results = self.get_YOLO_results(frame)
                annotated_frame = self.annotate_frame(results, frame)
                cv2.imshow('out', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass