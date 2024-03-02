import cv2
import numpy as np

# Function to check collision between a circle and a line
def check_collision(circle_center, circle_radius, line_start, line_end):
    # Calculate the distance between the center of the circle and the line
    distance = np.abs(np.cross(line_end - line_start, circle_center - line_start) / np.linalg.norm(line_end - line_start))
    # Check if the distance is less than the radius of the circle
    print(distance)
    return distance <= 0.1, distance

# Create a blank image
image = np.zeros((400, 400, 3), dtype=np.uint8)

# Define the line parameters
line_start = np.array([100, 200])
line_end = np.array([500, 200])

# Initialize circle parameters
circle_center = np.array([50, 50])
circle_radius = 10
circle_velocity = np.array([2, 1])

# Main loop
while True:
    # Clear the image
    image.fill(0)

    # Update circle position
    circle_center += circle_velocity

    # Check collision
    success, dist = check_collision(circle_center, circle_radius, line_start, line_end)
    if success:
        print(f"Collision detected! Distance: {dist}")

    # Draw the line
    cv2.line(image, tuple(line_start), tuple(line_end), (255, 255, 255), 2)

    # Draw the circle
    cv2.circle(image, tuple(circle_center), circle_radius, (0, 0, 255), -1)

    # Show the image
    cv2.imshow('Collision Detection', image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()