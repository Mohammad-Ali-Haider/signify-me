import pickle
import cv2
import mediapipe as mp
import csv
import os
import numpy as np
import pandas as pd

with open('./new/gesture_detection.pkl', 'rb') as f:
    model = pickle.load(f)

def rescale(frame, percentage = 75):
    scale_percent = percentage
    width = int(frame.shape[1] * scale_percent/100)
    height = int(frame.shape[0] * scale_percent/100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = rescale(frame,60)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = holistic.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)

        class_name = "Victory"
        
        try:
            pose = results.pose_landmarks.landmark
            pose_row = np.array([])
            
            for landmark in pose:
                pose_row = np.append(pose_row, [landmark.x, landmark.y, landmark.z, landmark.visibility])
            pose_row = list(pose_row)

            face = results.face_landmarks.landmark
            face_row = np.array([])
            
            for landmark in face:
                face_row = np.append(face_row, [landmark.x, landmark.y, landmark.z, landmark.visibility])
            face_row = list(face_row)

            row = pose_row+face_row

            X = pd.DataFrame([row])
            body_language_class = model.predict(X)[0]
            body_language_prob = model.predict_proba(X)[0]
            print(body_language_class, body_language_prob)

            # Grab ear coords
            # coords = tuple(np.multiply(
            #                 np.array(
            #                     (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x, 
            #                      results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
            #             , [640,480]).astype(int))
            
            # cv2.rectangle(image, 
            #               (coords[0], coords[1]+5), 
            #               (coords[0]+len(body_language_class)*20, coords[1]-30), 
            #               (245, 117, 16), -1)
            # cv2.putText(image, body_language_class, coords, 
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # # Get status box
            # cv2.rectangle(image, (0,0), (250, 60), (245, 117, 16), -1)
            
            # # Display Class
            # cv2.putText(image, 'CLASS'
            #             , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(image, body_language_class.split(' ')[0]
            #             , (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # # Display Probability
            # cv2.putText(image, 'PROB'
            #             , (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)],2))
            #             , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # row.insert(0, class_name)

            # with open("C://Users//alimh//OneDrive//Desktop//Python Projects//Body Tracking//coords.csv", mode="a", newline="") as f:
            #     csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #     csv_writer.writerow(row)

        except:
            pass

        cv2.imshow("Holistic Model Detection", image)

        if cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()

