import numpy as np
import math

def calculate_bbox_center(xyxy):
    return (int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)) 


def check_line_collusion(center_point, point1, point2, threshold):
    line_start = np.array([point1.x, point1.y])
    line_end   = np.array([point2.x, point2.y])
    object_pos = np.array([center_point.x, center_point.y])
    distance = np.abs(np.cross(line_end - line_start, object_pos - line_start) / np.linalg.norm(line_end - line_start))
    return distance <= threshold


def check_two_point_collusion(point1, point2, threshold):
    x_distance = math.pow(abs(point1.x - point2.x), 2)
    y_distance = math.pow(abs(point1.y - point2.y), 2)
    total_diff = math.sqrt(x_distance + y_distance)
    return total_diff < threshold
        