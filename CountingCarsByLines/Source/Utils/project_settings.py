import cv2

# OpenCV Settings
# Color
BLUE   = (255, 0, 0)
GREEN  = (0, 255, 0)
RED    = (0, 0, 255)
YELLOW = (0, 255, 255)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

# Line Thickness
BBOX_THICKNESS     = 2
BBOX_CIRCLE_RADIUS = 3
LINE_THICKNESS     = 3
FILL               = -1

# Text
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_FONT_SCALE = 1
TEXT_THICKNESS  = 2
TEXT_POS = (50, 50)

# Background
UI_POS    = (40, 20)
UI_WIDTH  = UI_POS[0] + 260
UI_HEIGHT = UI_POS[1] + 80

# Point
POINT_RADIUS = 5

# YOLO Settings
SHOW_YOLO_SCREEN = False
YOLO_THRESHOLD   = 0.2
IMG_SIZE         = 320

# Algorithm Settings
COLLUSION_THRESHOLD  = 10
MOUSE_DIFF_THRESHOLD = 10

# FPS Settings
FPS_INTERVAL = 1
FPS_POS      = (50, 90)  