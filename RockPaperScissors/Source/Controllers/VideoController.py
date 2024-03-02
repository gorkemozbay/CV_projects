
import cv2
import mediapipe as mp


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
            success, frame = self.cap.read()
            if success:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.model.process(frame_rgb)
    
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for id, landmark in enumerate(hand_landmarks.landmark):
                            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                            if id in [4, 8, 12, 16, 20]:
                                pass
                                #cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
                
                cv2.imshow('Hand Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        self.cap.release()
        cv2.destroyAllWindows()