import cv2
import Utils.project_settings as ps
from Utils.data_classes import Point

class UIController():
    
    def __init__(self):
        print("UI Controller is created")
        
    def draw_line(frame, point_1, point_2, color, thickness):
        cv2.line(frame, (point_1.x, point_1.y), (point_2.x, point_2.y), ps.RED, ps.LINE_THICKNESS)
        return frame