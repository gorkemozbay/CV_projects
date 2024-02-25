import numpy as np

import Utils.math_utils as math_ut
import Utils.project_settings as ps

class CollusionController():
    
    def __init__(self):
        print("CollusionController is created")
        self.number_of_collusions = 0
        self.line_list = []
        
        
    def check_for_collusions(self, results):
        for result in results:
            boxes = result.boxes.cpu().numpy()
            xyxys = boxes.xyxy
            for xyxy in xyxys:
                center_coordinates = (int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)) 
                for line in self.line_list:
                    success = self.check_line_collision(center_coordinates, line.point1, line.point2)
                    if success:
                        self.number_of_collusions += 1
                        print(f"Collusion happened {self.number_of_collusions} times")
                        
                
    def check_line_collision(self, center_pos, point1, point2):
        line_start = np.array([point1.x, point1.y])
        line_end   = np.array([point2.x, point2.y])
        object_pos = np.array([center_pos[0], center_pos[1]])
        distance = np.abs(np.cross(line_end - line_start, object_pos - line_start) / np.linalg.norm(line_end - line_start))
        #print(f"Distance: {distance}")
        return distance <= ps.COLLUSION_THRESHOLD
    