from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

predicted_class = ''
prob = ''
word = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/livecam')
def livecam():
    return render_template('livecam.html', predicted_class = predicted_class, probability = prob)

@app.route('/dictionary')
def dict():
    return render_template('support.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/about-us1')
def about():
    return render_template('about-us1.html')

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

def generate_frames():
    global predicted_class, prob
    cap = cv2.VideoCapture(0)
    confirmed_sequence = []
    confirmation_mode = False
    previous = ""
    word = ""
    confirm = 0

    while cap.isOpened():
        ret, frame = cap.read()
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

                    predicted_class = body_language_class
                    prob = f"{probability}"

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

                    socketio.emit('update_data', {'predicted_class': predicted_class, 'probability': probability, 'words': word})

        except Exception as e:
            print(e)

        new_frame = cv2.flip(frame, flipCode=1)

        _, buffer = cv2.imencode('.jpg', new_frame)
        new_frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + new_frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def handle_connect():
    emit('update_data', {'predicted_class': predicted_class, 'probability': prob, 'words': word})


if __name__ == '__main__':
    socketio.run(app, debug=True) 