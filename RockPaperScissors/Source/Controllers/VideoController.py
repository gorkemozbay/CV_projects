
import cv2
import mediapipe as mp
import Utils.ProjectSetings as ps


class VideoController():
    
    def __init__(self, cap, model):
        print("VideoController is created")
        self.cap = cap
        self.model = model
        
    
    def run(self):
        if not self.cap.isOpened():
            print("Failed to open source")
            exit()
        
        while True:
            finger_list = [None, None]
            success, frame = self.cap.read()
            if success:
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.model.process(frame_rgb)
                if results.multi_hand_landmarks:
                    for hand_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
                        for id, landmark in enumerate(hand_landmarks.landmark):
                            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                            if id == ps.INDEX_TIP and landmark.y < hand_landmarks.landmark[ps.INDEX_MIDDLE_JOUNT].y:
                                cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
                                finger_list[hand_id] = (x, y)
                
                    if len(results.multi_hand_landmarks) == 2:
                        cv2.line(frame, finger_list[0], finger_list[1], ps.BLUE, ps.LINE_THICKNESS)
                    cv2.imshow('Hand Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        self.cap.release()
        cv2.destroyAllWindows()