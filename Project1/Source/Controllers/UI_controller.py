import cv2
import Utils.project_settings as ps

class UIController():
    
    def __init__(self):
        print("UIController is created")
    
        
    def draw_line(self, frame, line):
        cv2.line(frame, (line.point1.x, line.point1.y), (line.point2.x, line.point2.y), 
                 line.color, line.thickness)
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
    
    def show_lines(self, frame, line_list):
        for line in line_list:
            self.draw_line(frame, line)
        return frame
    
    def change_line_color(self, frame, line_list):
        for line in line_list:
            cv2.line(frame, (line.point1.x, line.point1.y), (line.point2.x, line.point2.y), 
                 ps.YELLOW, line.thickness)
        return frame
