import cv2
import Utils.project_settings as ps
from   Utils.data_classes import Line, Point

class VideoController():
    
    def __init__(self, source, model):
        print("VideoController is created")
        self.cap = cv2.VideoCapture(source)
        self.model = model
        # Move the fields below somewhere else
        self.line_list = []
        self.point1 = None
        self.point2 = None
        self.point_count = 0


    def get_mouse_position(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point_count += 1
            if self.point_count %2 == 1:
                self.point1 = Point(x, y)
            else:
                self.point2 = Point(x, y)
                line = Line(self.point1, self.point2, ps.RED, ps.LINE_THICKNESS)
                self.line_list.append(line)


    def draw_line(self, frame, line):
        cv2.line(frame, (line.point1.x, line.point1.y), (line.point2.x, line.point2.y), 
                 line.color, line.thickness)
        return frame


    def get_YOLO_results(self, frame):
        results = self.model(frame, classes=[1,2,3,7], show=False, verbose=False)
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
            for xyxy in xyxys:
                center_coordinates = (int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)) 
                cv2.circle(frame, center_coordinates, ps.BBOX_CIRCLE_RADIUS, ps.GREEN, ps.BBOX_THICKNESS)
        return frame


    def add_lines(self, frame):
        for line in self.line_list:
            self.draw_line(frame, line)
        return frame


    def run(self):
        
        if not self.cap.isOpened():
            print("Failed to open source")
            exit()
        
        cv2.namedWindow("out")
        cv2.setMouseCallback("out", self.get_mouse_position)
        while True:
            success, frame = self.cap.read()
            if success:
                results = self.get_YOLO_results(frame)
                #annotated_frame = self.annotate_frame_by_box(results, frame)
                annotated_frame = self.annotate_frame_by_center(results, frame)
                annotated_frame = self.add_lines(annotated_frame)
                cv2.imshow("out", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass