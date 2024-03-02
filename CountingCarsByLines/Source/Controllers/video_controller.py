import cv2
import time
import numpy                  as np
import Utils.project_settings as ps
from   Utils.data_classes               import Point
from   Controllers.collusion_controller import CollusionController
from   Controllers.UI_controller        import UIController 

class VideoController():
    
    def __init__(self, source, model):
        print("VideoController is created")
        self.collusion_controller = CollusionController()
        self.UI_controller = UIController()
        self.cap = cv2.VideoCapture(source)
        self.model = model
        self.mouse_pos = Point(0, 0)
        self.fps_start_time = None
        self.fps_number_of_frames = 0
        self.fps = 0


    def check_mouse_event(self, event, x, y, flags, param):
        self.mouse_pos = Point(x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.UI_controller.save_points(self.mouse_pos)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.UI_controller.check_for_line_remove(self.mouse_pos)


    def get_YOLO_results(self, frame):
        results = self.model.track(frame, classes=[1,2,3,7], 
                             show=ps.SHOW_YOLO_SCREEN, conf=ps.YOLO_THRESHOLD ,verbose=False)
        return results


    def get_YOLO_track_results(self, frame):
        results = self.model.track(frame, classes=[1,2,3,7], 
                             show=ps.SHOW_YOLO_SCREEN, conf=ps.YOLO_THRESHOLD ,verbose=False,
                             tracker = "botsort.yaml", persist = True, imgsz = ps.IMG_SIZE, half=True)
        return results


    def annotate_frame_by_box(self, results, frame):
        for result in results:
            boxes = result.boxes.cpu().numpy()
            xyxys = boxes.xyxy
            for xyxy in xyxys:
                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), ps.GREEN, ps.BBOX_THICKNESS)
        return frame

    
    def annotate_frame_by_center(self, results, frame):
        for result in results:
            boxes = result.boxes.cpu().numpy()
            if not boxes:
                return frame
            xyxys = boxes.xyxy
            ids   = boxes.id
            if not isinstance(ids, np.ndarray):
                return frame
            for xyxy, box_id in zip(xyxys, ids):
                center_coordinates = (int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2))
                id_coordiantes     = (center_coordinates[0] + 3, center_coordinates[1] + 3)  
                cv2.circle(frame, center_coordinates, ps.BBOX_CIRCLE_RADIUS, ps.GREEN, ps.BBOX_THICKNESS)
                cv2.putText(frame, str(int(box_id)), id_coordiantes, ps.TEXT_FONT, 
                    ps.TEXT_FONT_SCALE, ps.BLUE, ps.TEXT_THICKNESS)
        return frame

    
    def check_fps(self):
        self.fps_number_of_frames += 1
        time_passed = time.time() - self.fps_start_time
        if time_passed >= ps.FPS_INTERVAL:
            self.fps = int(self.fps_number_of_frames / time_passed)
            self.fps_start_time = time.time()
            self.fps_number_of_frames = 0   
        return self.fps

    
    def run(self):
    
        if not self.cap.isOpened():
            print("Failed to open source")
            exit()
        
        cv2.namedWindow("out")
        cv2.setMouseCallback("out", self.check_mouse_event)
        self.fps_start_time = time.time()
        while True:
            success, frame = self.cap.read()
            if success:
                
                results = self.get_YOLO_track_results(frame)
                line_list = self.UI_controller.line_list
                collided_lines, number_of_collusions = self.collusion_controller.check_for_collusions(results, line_list)
                fps = self.check_fps()
                
                annotated_frame = self.UI_controller.draw_background(frame)
                annotated_frame = self.annotate_frame_by_center(results, annotated_frame)
                annotated_frame = self.UI_controller.show_ongoing_line(annotated_frame, self.mouse_pos)
                annotated_frame = self.UI_controller.show_lines(annotated_frame)
                annotated_frame = self.UI_controller.change_line_color(annotated_frame, collided_lines)
                annotated_frame = self.UI_controller.show_count(annotated_frame, number_of_collusions)
                annotated_frame = self.UI_controller.show_fps(annotated_frame, fps)
                
                cv2.imshow("out", annotated_frame) 
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass
            