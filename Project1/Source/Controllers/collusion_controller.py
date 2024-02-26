import numpy as np

import Utils.math_utils as math_ut
import Utils.project_settings as ps
from   Utils.data_classes import Point

class CollusionController():
    
    def __init__(self):
        print("CollusionController is created")
        self.number_of_collusions = 0
        self.line_list = []
        self.passed_id_list = []


    def check_for_collusions(self, results):
        for result in results:
            boxes  = result.boxes.cpu().numpy()
            xyxys  = boxes.xyxy
            ids    = boxes.id
            for xyxy, box_id in zip(xyxys, ids):
                center_coordinates = Point(int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)) 
                for line in self.line_list:
                    success = math_ut.check_line_collusion(center_coordinates, line.point1, line.point2, ps.COLLUSION_THRESHOLD)
                    if success and (box_id not in self.passed_id_list):
                        self.passed_id_list.append(box_id)
                        self.number_of_collusions += 1
                        print(f"Collusion happened with id {box_id}")
                        print(f"Total collusion: {self.number_of_collusions}")
                        
                
    def check_for_line_remove(self, mouse_pos):
        for line in self.line_list:
            success = math_ut.check_line_remove_collusion(mouse_pos, line.point1, line.point2, ps.MOUSE_DIFF_THRESHOLD)
            if success:
                self.line_list.remove(line)
                break
            