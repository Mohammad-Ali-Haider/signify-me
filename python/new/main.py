import cv2
import mediapipe as mp
import csv
import os
import numpy as np

OFFSET = 20
IMGSIZE = 150

datafolder = "./archive/asl_alphabet_train/asl_alphabet_train"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

num_cord = 21
landmarks = ["class"]
for val in range(1, num_cord+1):
    landmarks += [f'x{val}', f'y{val}', f'z{val}', f'v{val}']

with open("./new/gesture_detection.csv", mode="w", newline="") as f:
    csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(landmarks)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    for label in os.listdir(datafolder):
        counter = 0
        if label == ".DS_Store": continue
        for file in os.listdir(os.path.join(datafolder, label)):
            frame = cv2.imread(os.path.join(datafolder, label, file))

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if (label in ["G", "H", "P", "Q"]) : rgb_frame = cv2.flip(rgb_frame, 1)

            results = hands.process(rgb_frame)

            class_name = label

            
            try:
                hand_row = np.array([])
                if results.multi_hand_landmarks:
                    for landmarks in results.multi_hand_landmarks:
                        for point in landmarks.landmark:
                            x, y, z = point.x, point.y, point.z
                            hand_row = np.append(hand_row, [x, y, z])

                        mp.solutions.drawing_utils.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                    hand_row = list(hand_row)
                    if len(hand_row) > 84: continue

                    row = hand_row

                    row.insert(0, class_name)
                    counter += 1
                    print(counter)
                    if counter > 1000: break
                    with open("./model.csv", mode="a", newline="") as f:
                        csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(row)

            except:
                print("fail")

            cv2.imshow("Holistic Model Detection", frame)

            if cv2.waitKey(1) == ord("q"):
                break

cv2.destroyAllWindows()

