from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
from collections import deque
import os

# --- Global Variables & Constants ---
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 20
YAWN_THRESH = 25
YAWN_CONSEC_FRAMES = 10

# EAR Smoothing
EAR_SMOOTHING_WINDOW = 5
ear_history = deque(maxlen=EAR_SMOOTHING_WINDOW)

# Counters and Status Flags
eye_counter = 0
yawn_counter = 0
alert_active_drowsy = False
alert_active_yawn = False

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    if C == 0: return 0.3
    ear = (A + B) / (2.0 * C)
    return ear

def final_ear(shape):
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0
    return (ear, leftEye, rightEye)

def lip_distance(shape):
    top_lip_pts = shape[50:53]
    top_lip_pts = np.concatenate((top_lip_pts, shape[61:64]))
    low_lip_pts = shape[56:59]
    low_lip_pts = np.concatenate((low_lip_pts, shape[65:68]))
    top_mean = np.mean(top_lip_pts, axis=0)
    low_mean = np.mean(low_lip_pts, axis=0)
    distance = abs(top_mean[1] - low_mean[1])
    return distance

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--webcam", type=int, default=0,
                   help="index of webcam on system")
    ap.add_argument("-p", "--shape-predictor",
                   default="shape_predictor_68_face_landmarks.dat",
                   help="path to facial landmark predictor")
    args = vars(ap.parse_args())

    print("[INFO] Loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    print("[INFO] Starting video stream...")
    vs = cv2.VideoCapture(args["webcam"])
    time.sleep(1.0)  # Allow camera to warm up

    while True:
        ret, frame = vs.read()
        if not ret:
            print("[INFO] Failed to grab frame or end of stream. Exiting...")
            break

        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)
        face_detected_this_frame = len(rects) > 0
        ear = 0.3
        lip_dist = 0
        smoothed_ear = ear

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            ear_data = final_ear(shape)
            ear = ear_data[0]
            leftEye = ear_data[1]
            rightEye = ear_data[2]

            ear_history.append(ear)
            if len(ear_history) == EAR_SMOOTHING_WINDOW:
                smoothed_ear = np.mean(ear_history)
            else:
                smoothed_ear = ear

            lip_dist = lip_distance(shape)

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            lipHull = cv2.convexHull(shape[48:60]) # Assuming landmarks 48-59 are the outer lip contour
            cv2.drawContours(frame, [lipHull], -1, (0, 255, 0), 1)


        # Drowsiness detection (Eyes)
        if face_detected_this_frame and smoothed_ear < EYE_AR_THRESH:
            eye_counter += 1
            if eye_counter >= EYE_AR_CONSEC_FRAMES and not alert_active_drowsy:
                current_alert_message = "DROWSINESS ALERT!"
                alert_active_drowsy = True
                os.system("sudo python3 alert_sys_v1.py") # Consider non-blocking alternatives
        else:
            if face_detected_this_frame and smoothed_ear >= EYE_AR_THRESH and alert_active_drowsy:
                alert_active_drowsy = False
            eye_counter = 0

        # Yawn detection
        if face_detected_this_frame and lip_dist > YAWN_THRESH:
            yawn_counter += 1
            if yawn_counter >= YAWN_CONSEC_FRAMES and not alert_active_yawn:
                current_alert_message = "YAWN DETECTED!"
                alert_active_yawn = True
                os.system("sudo python3 alert_sys_v1.py") # Consider non-blocking alternatives
        else:
            if face_detected_this_frame and lip_dist <= YAWN_THRESH and alert_active_yawn:
                alert_active_yawn = False
            yawn_counter = 0

        # Display information
        if not face_detected_this_frame:
            current_alert_message = "No Face Detected"
            eye_counter = 0
            yawn_counter = 0
            alert_active_drowsy = False
            alert_active_yawn = False
            ear_history.clear()
        elif alert_active_drowsy:
            current_alert_message = "DROWSINESS ALERT!"
        elif alert_active_yawn:
            current_alert_message = "YAWN DETECTED!"
        else:
            current_alert_message = ""

        # Display EAR and Lip Distance
        if face_detected_this_frame:
            cv2.putText(frame, f"EAR: {ear:.2f} (S:{smoothed_ear:.2f})",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, f"LIP: {lip_dist:.2f}",
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Display counters
        text_y_pos = frame.shape[0] - 10
        cv2.putText(frame, f"Yawn: {yawn_counter}/{YAWN_CONSEC_FRAMES}",
                   (10, text_y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 0), 1)
        text_y_pos -= 20
        cv2.putText(frame, f"Eyes Closed: {eye_counter}/{EYE_AR_CONSEC_FRAMES}",
                   (10, text_y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 0), 1)

        # Display alert message
        if current_alert_message:
            text_size, _ = cv2.getTextSize(current_alert_message, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            text_x = frame.shape[1] - text_size[0] - 10
            text_y = 30

            if "ALERT" in current_alert_message or "DETECTED" in current_alert_message:
                cv2.rectangle(frame, (text_x - 5, text_y - text_size[1] - 5),
                            (text_x + text_size[0] + 5, text_y + 5), (0, 0, 0), -1)
                cv2.putText(frame, current_alert_message, (text_x, text_y),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Drowsiness Detector", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:  # 'q' or ESC
            break

    print("[INFO] Cleaning up...")
    cv2.destroyAllWindows()
    vs.release()
