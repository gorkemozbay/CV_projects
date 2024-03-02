import numpy as np
import math

def calculate_bbox_center(xyxy):
    return (int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)) 


def check_line_collusion(center_point, point1, point2, threshold):
    line_start = np.array([point1.x, point1.y])
    line_end   = np.array([point2.x, point2.y])
    object_pos = np.array([center_point.x, center_point.y])
    
    distance = np.abs(np.cross(line_end - line_start, object_pos - line_start) / np.linalg.norm(line_end - line_start))
    distance_condition    = distance <= threshold
    
    left_point  = point1 if point1.x < point2.x  else point2
    right_point = point1 if left_point == point2 else point2
        
    left_point_condition  = center_point.x >= left_point.x
    right_point_condition = center_point.x <= right_point.x
    
    return distance_condition and left_point_condition and right_point_condition


def check_line_remove_collusion(center_point, point1, point2, threshold):
    line_start = np.array([point1.x, point1.y])
    line_end   = np.array([point2.x, point2.y])
    object_pos = np.array([center_point.x, center_point.y])
    distance = np.abs(np.cross(line_end - line_start, object_pos - line_start) / np.linalg.norm(line_end - line_start))
    distance_condition    = distance <= threshold
    return distance_condition


def check_two_point_collusion(point1, point2, threshold):
    x_distance = math.pow(abs(point1.x - point2.x), 2)
    y_distance = math.pow(abs(point1.y - point2.y), 2)
    total_diff = math.sqrt(x_distance + y_distance)
    return total_diff < threshold
        