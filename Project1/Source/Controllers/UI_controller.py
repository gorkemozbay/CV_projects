import cv2

import Utils.math_utils as math_ut
from   Utils.data_classes     import Point, Line
import Utils.project_settings as ps

class UIController():
    
    def __init__(self):
        self.point_couple = [None, None]
        self.point_count = 0
        self.line_list = []
        print("UIController is created")
    

    def save_points(self, mouse_pos):
        self.point_count += 1
        if self.point_count %2 == 1:
            self.point_couple[0] = Point(mouse_pos.x, mouse_pos.y)
        else:
            self.point_couple[1] = Point(mouse_pos.x, mouse_pos.y)
            line = Line(self.point_couple[0], self.point_couple[1],
                        ps.RED, ps.LINE_THICKNESS)
            self.point_couple = [None, None]
            self.line_list.append(line)
    
    
    def show_ongoing_line(self, frame, mouse_pos):
        if self.point_count %2 == 0:
            return frame
        point1 = self.point_couple[0]
        point2 = mouse_pos
        self.draw_point(frame, point1)
        cv2.line(frame, (point1.x, point1.y), (point2.x, point2.y), 
                 ps.BLACK, ps.LINE_THICKNESS)
        return frame
    
    
    def show_lines(self, frame):
        for line in self.line_list:
            self.draw_point(frame, line.point1, line.color)
            self.draw_point(frame, line.point2, line.color)
            self.draw_line(frame, line)
        return frame
    
    
    def draw_line(self, frame, line):
        cv2.line(frame, (line.point1.x, line.point1.y), (line.point2.x, line.point2.y), 
                 line.color, line.thickness)
        return frame
    
    
    def check_for_line_remove(self, mouse_pos):
        if self.point_count %2 == 1:
            self.point_count += 1
            return
        for line in self.line_list:
            success = math_ut.check_line_remove_collusion(mouse_pos, line.point1, line.point2, ps.MOUSE_DIFF_THRESHOLD)
            if success:
                self.line_list.remove(line)
                break
    
    
    def draw_point(self, frame, point, color = ps.BLACK):
        cv2.circle(frame, (point.x, point.y), ps.BBOX_CIRCLE_RADIUS, color, ps.POINT_RADIUS)
        return frame
    
    
    def show_count(self, frame, number_of_collusions):
        count_txt = f"Car Count:{number_of_collusions}"
        cv2.putText(frame, count_txt, ps.TEXT_POS, ps.TEXT_FONT, 
                    ps.TEXT_FONT_SCALE, ps.WHITE, ps.TEXT_THICKNESS)
        return frame
    
    
    def draw_background(self, frame):
        cv2.rectangle(frame, (ps.UI_POS[0], ps.UI_POS[1]), (ps.UI_WIDTH, ps.UI_HEIGHT), ps.BLACK, ps.FILL)
        return frame
    
    
    def show_fps(self, frame, fps):
        fps_txt = f"FPS:{fps}"
        cv2.putText(frame, str(fps_txt), ps.FPS_POS, ps.TEXT_FONT, 
                    ps.TEXT_FONT_SCALE, ps.WHITE, ps.TEXT_THICKNESS)
        return frame
    
    
    def change_line_color(self, frame, collided_lines):
        for line in collided_lines:
            cv2.line(frame, (line.point1.x, line.point1.y), (line.point2.x, line.point2.y), 
                 ps.YELLOW, line.thickness)
        return frame
