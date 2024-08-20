from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

predicted_class = ''
prob = ''
word = ''
translate = False

@app.route('/')
def index():
    global translate
    translate = False
    return render_template('index.html')

@app.route('/video')
def video():
    global translate
    translate = False
    return render_template('video.html')

@app.route('/livecam')
def livecam():
    global translate
    translate = False
    return render_template('livecam.html', predicted_class = predicted_class, probability = prob)

@app.route('/dictionary')
def dict():
    global translate
    translate = False
    return render_template('support.html')

@app.route('/support')
def support():
    global translate
    translate = False
    return render_template('support.html')

@app.route('/about-us1')
def about():
    global translate
    translate = False
    return render_template('about-us1.html')

@app.route('/start-stop-clicked', methods=['POST'])
def button_click():
    global translate, word
    if not translate: translate = True
    else: translate = False
    return jsonify({'success': True})

import pickle
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

OFFSET = 20
IMGSIZE = 150
isPotrait = False

with open('./python/model.pkl', 'rb') as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def generate_frames():
    global predicted_class, prob, translate
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
        
        if translate:
            try:
                hand_row = np.array([])
                if results.multi_hand_landmarks:
                    for landmarks in results.multi_hand_landmarks:
                        for point in landmarks.landmark:
                            x, y, z = point.x, point.y, point.z
                            hand_row = np.append(hand_row, [x, y, z])

                        mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                    hand_row = list(hand_row)

                    if len(hand_row) <= 84:
                        row = hand_row
                        X = pd.DataFrame([row])
                        body_language_class = model.predict(X)[0]
                        body_language_prob = model.predict_proba(X)[0]
                        probability = max(body_language_prob) * 100

                        # print(body_language_class, round(probability, 2), confirm)

                        predicted_class = body_language_class
                        prob = f"{probability}"

                        if (probability > 30 and previous == body_language_class):
                            confirm += 1
                        else:
                            confirm = 0
                        previous = body_language_class

                        if confirm == 5:
                            # print("Confirmed")
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
        else:
            word = ""
            confirmed_sequence = []

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
