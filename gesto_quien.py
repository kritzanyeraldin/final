import cv2
import mediapipe as mp
import math

video = cv2.VideoCapture(0)
# face
pose_face = mp.solutions.face_detection
Face = pose_face.FaceDetection(min_detection_confidence=0.5)
draw_face = mp.solutions.drawing_utils
# hands
pose_hands = mp.solutions.hands
Pose_hands = pose_hands.Hands(min_tracking_confidence=0.5, min_detection_confidence=0.5)
draw_hands = mp.solutions.drawing_utils

contador = 0
check = True



while True:
    success, img = video.read()

    if not success:
        break
    # Convertir la imagen a RGB para procesarla con Mediapipe
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width,  _ = img.shape


    results_face = Face.process(img_rgb)
    points_face= results_face.detections

    results_hands = Pose_hands.process(img_rgb)
    points_hands= results_hands.multi_hand_landmarks
    mx = 0
    my = 0
    dx = 0
    dy = 0
    if points_face and points_hands:

        for face_landmark in points_face:
            draw_face.draw_detection(img, face_landmark)

            # punto central de la boca
            mouth_center_x = (pose_face.get_key_point(face_landmark, pose_face.FaceKeyPoint.MOUTH_CENTER).x )
            mouth_center_y = (pose_face.get_key_point(face_landmark, pose_face.FaceKeyPoint.MOUTH_CENTER).y )

            #print(mouth_center_x, mouth_center_y)

            mx = int (mouth_center_x  * width)
            my = int (mouth_center_y * height)

            #print (mx, my)
            #cv2.circle(img, (mx, my), 8, (0,255, 0), 2)


            # cv2.rectangle(img, top_left, bottom_right, (255,0, 0), 2)

        for hand_landmarks in points_hands:
            draw_hands.draw_landmarks(img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            # primer punto del dedo medio
            p12x = (hand_landmarks.landmark[pose_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
            p12y = (hand_landmarks.landmark[pose_hands.HandLandmark.MIDDLE_FINGER_TIP].y)

            dx = int(p12x * width)
            dy = int(p12y * height)

            # rectangulo que cubre la boca a partir del punto central
            rect_top_left = (mx + 30, my - 15)
            rect_bottom_right = (mx - 30, my + 17)
            cv2.rectangle(img, rect_top_left, rect_bottom_right, (255, 0, 0), 2)

            # circulo que cubre el punto del dedo medio
            circle_center = 4
            cv2.circle(img, (dx, dy), circle_center, (0,255, 0), 2)
            #print(mx, my)
            # coordenadas para el borde superior del circulo
            circle_y=(dy-circle_center,dy+circle_center)


            # si el eje y del borde superior del circulo  esta contenido en el rectangulo se imprime quien
            if (
                    rect_top_left[1] < circle_y[0] <= rect_bottom_right[1]
            ):
                print("¿Quien?")
                texto = "Quien?"
                cv2.rectangle(img, (20, 20), (340, 120), (255, 0, 0), -1)
                cv2.putText(img, texto, (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

            else:
                print("No hay ningun gesto")

    cv2.imshow('Resultado', img)
    cv2.waitKey(50)