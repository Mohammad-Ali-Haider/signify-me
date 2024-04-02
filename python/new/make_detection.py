import pickle
import cv2
import mediapipe as mp
import csv
import os
import numpy as np
import pandas as pd

OFFSET = 20
IMGSIZE = 150
isPotrait = False

def draw_asl_fingerspelling(image, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 3
    color = (0, 255, 0)

    image_height, image_width, _ = image.shape

    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = (image_width - text_size[0]) // 2
    text_y = (image_height + text_size[1]) // 2

    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)

with open('./python/model.pkl', 'rb') as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

confirmed_sequence = []
confirmation_mode = False
confirm = 0
previous = ""
word = ""

cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        if isPotrait:
            h, w, _ = frame.shape
            aspectRatio = w / h
            if aspectRatio > 1:
                frame = frame[:, int(w/2 - (h**2 / w)/2): int(w/2 + (h**2 / w)/2)]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img_white = np.ones((frame.shape[0], frame.shape[1], 3), np.uint8) * 255

        results = hands.process(rgb_frame)
        
        try:
            hand_row = np.array([])
            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    for point in landmarks.landmark:
                        x, y, z = point.x, point.y, point.z
                        hand_row = np.append(hand_row, [x, y, z])

                    mp.solutions.drawing_utils.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                hand_row = list(hand_row)

                if len(hand_row) <= 84:
                    row = hand_row
                    X = pd.DataFrame([row])
                    body_language_class = model.predict(X)[0]
                    body_language_prob = model.predict_proba(X)[0]
                    probability = max(body_language_prob) * 100

                    print(body_language_class, round(probability, 2), confirm)

                    if (probability > 30 and previous == body_language_class):
                        confirm += 1
                    else:
                        confirm = 0
                    previous = body_language_class

                    if confirm == 5:
                        print("Confirmed")
                        confirmation_mode = True

                    if confirmation_mode:
                        if (body_language_class == "space"):
                            confirmed_sequence.append(" ")
                        elif (body_language_class == "del"):
                            confirmed_sequence.pop()
                        else:
                            confirmed_sequence.append(body_language_class)
                        confirmation_mode = False

                    word = "".join(confirmed_sequence)

        except:
            print("fail")

        new_frame = cv2.flip(frame, flipCode=1)

        draw_asl_fingerspelling(new_frame, word)

        cv2.imshow("ASL Convertor", new_frame)

    key = cv2.waitKey(1)

    if key == ord("c"):
        confirmation_mode = True

    if key == ord("q"):
        cv2.destroyAllWindows()
        break
