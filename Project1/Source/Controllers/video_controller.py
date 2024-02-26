import cv2
import Utils.project_settings as ps
import Utils.math_utils       as math_ut
from   Utils.data_classes import Line, Point
from   Controllers.collusion_controller import CollusionController

class VideoController():
    
    def __init__(self, source, model):
        print("VideoController is created")
        self.collusion_controller = CollusionController()
        self.cap = cv2.VideoCapture(source)
        self.model = model
        self.point_couple = [None, None]
        self.point_count = 0


    def check_mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point_count += 1
            if self.point_count %2 == 1:
                self.point_couple[0] = Point(x, y)
            else:
                self.point_couple[1] = Point(x, y)
                line = Line(self.point_couple[0], self.point_couple[1], ps.RED, ps.LINE_THICKNESS)
                self.collusion_controller.line_list.append(line)
        elif event == cv2.EVENT_RBUTTONDOWN:
            mouse_pos = Point(x, y)
            self.collusion_controller.check_for_line_remove(mouse_pos)


    def draw_line(self, frame, line):
        cv2.line(frame, (line.point1.x, line.point1.y), (line.point2.x, line.point2.y), 
                 line.color, line.thickness)
        return frame


    def get_YOLO_results(self, frame):
        results = self.model.track(frame, classes=[1,2,3,7], 
                             show=ps.SHOW_YOLO_SCREEN, conf=ps.YOLO_THRESHOLD ,verbose=False)
        return results


    def get_YOLO_track_results(self, frame):
        results = self.model.track(frame, classes=[1,2,3,7], 
                             show=ps.SHOW_YOLO_SCREEN, conf=ps.YOLO_THRESHOLD ,verbose=False,
                             tracker = "botsort.yaml", persist = True)
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
            xyxys = boxes.xyxy
            ids   = boxes.id
            for xyxy, box_id in zip(xyxys, ids):
                center_coordinates = (int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2))
                id_coordiantes     = (center_coordinates[0] + 3, center_coordinates[1] + 3)  
                cv2.circle( frame, center_coordinates, ps.BBOX_CIRCLE_RADIUS, ps.GREEN, ps.BBOX_THICKNESS)
                cv2.putText(frame, str(int(box_id)), id_coordiantes, ps.TEXT_FONT, 
                    ps.TEXT_FONT_SCALE, ps.BLUE, ps.TEXT_THICKNESS)
        return frame


    def add_lines(self, frame):
        for line in self.collusion_controller.line_list:
            self.draw_line(frame, line)
        return frame


    def show_count(self, frame):
        car_count = f"Car Count: {self.collusion_controller.number_of_collusions}"
        cv2.putText(frame, car_count, ps.TEXT_POS, ps.TEXT_FONT, 
                    ps.TEXT_FONT_SCALE, ps.BLUE, ps.TEXT_THICKNESS)
        return frame    
    
    
    def run(self):
    
        if not self.cap.isOpened():
            print("Failed to open source")
            exit()
        
        cv2.namedWindow("out")
        cv2.setMouseCallback("out", self.check_mouse_event)
        while True:
            success, frame = self.cap.read()
            if success:
                results = self.get_YOLO_track_results(frame)
                self.collusion_controller.check_for_collusions(results)
                #annotated_frame = self.annotate_frame_by_box(results, frame)
                annotated_frame = self.annotate_frame_by_center(results, frame)
                annotated_frame = self.add_lines(annotated_frame)
                annotated_frame = self.show_count(annotated_frame)
                cv2.imshow("out", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass