import numpy as np

import Utils.math_utils as math_ut
import Utils.project_settings as ps
from   Utils.data_classes import Point

class CollusionController():
    
    def __init__(self):
        print("CollusionController is created")
        self.number_of_collusions = 0
        self.passed_id_list = []


    def check_for_collusions(self, results, line_list):
        collided_lines = []
        for result in results:
            boxes  = result.boxes.cpu().numpy()
            if not boxes:
                return collided_lines, self.number_of_collusions
            xyxys  = boxes.xyxy
            ids    = boxes.id
            if not isinstance(ids, np.ndarray):
                return collided_lines, self.number_of_collusions
            for xyxy, box_id in zip(xyxys, ids):
                center_coordinates = Point(int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)) 
                for line in line_list:
                    success = math_ut.check_line_collusion(center_coordinates, line.point1, line.point2, ps.COLLUSION_THRESHOLD)
                    if success and (box_id not in self.passed_id_list):
                        self.passed_id_list.append(box_id)
                        self.number_of_collusions += 1
                        collided_lines.append(line)
        return collided_lines, self.number_of_collusions
