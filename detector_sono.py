import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_desenho = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                   min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5)

p_olho_esq = [385, 380, 387, 373, 362, 263]
p_olho_dir = [160, 144, 158, 153, 33, 133]

ear_limiar = 0.25
limite_frames_olho = 30
contador_olho = 0

inclinacao_limiar = 18
limite_frames_cabeca = 30
contador_cabeca = 0


def calculo_ear(face, p_olho_dir, p_olho_esq):
    face = np.array([[coord.x, coord.y] for coord in face])
    face_esq = face[p_olho_esq, :]
    face_dir = face[p_olho_dir, :]

    ear_esq = (np.linalg.norm(face_esq[0] - face_esq[1]) + np.linalg.norm(face_esq[2] - face_esq[3])) / (2 * np.linalg.norm(face_esq[4] - face_esq[5]))
    ear_dir = (np.linalg.norm(face_dir[0] - face_dir[1]) + np.linalg.norm(face_dir[2] - face_dir[3])) / (2 * np.linalg.norm(face_dir[4] - face_dir[5]))

    media_ear = (ear_esq + ear_dir) / 2
    return media_ear


def calculo_inclinacao(face, largura, altura):
    olho_e = face[33]
    olho_d = face[263]

    x1 = olho_e.x * largura
    y1 = olho_e.y * altura
    x2 = olho_d.x * largura
    y2 = olho_d.y * altura

    angulo = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    return angulo


cap = cv2.VideoCapture(0)

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        continue

    frame = cv2.flip(frame, 1)
    altura, largura, _ = frame.shape

    saida_facemesh = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if saida_facemesh.multi_face_landmarks:
        for face_landmarks in saida_facemesh.multi_face_landmarks:
            mp_desenho.draw_landmarks(frame, face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=mp_desenho.DrawingSpec(color=(255, 102, 102), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_desenho.DrawingSpec(color=(102, 204, 0), thickness=1, circle_radius=1))

            face = face_landmarks.landmark

            ear = calculo_ear(face, p_olho_dir, p_olho_esq)
            inclinacao = calculo_inclinacao(face, largura, altura)

            cv2.rectangle(frame, (0, 1), (290, 80), (58, 58, 55), -1)
            cv2.putText(frame, f"EAR: {round(ear, 2)}", (1, 30),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f"Inclinacao: {round(inclinacao, 1)}", (1, 65),
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

            if ear < ear_limiar:
                contador_olho = contador_olho + 1
                if contador_olho >= limite_frames_olho:
                    cv2.rectangle(frame, (30, 400), (610, 450), (0, 0, 255), -1)
                    cv2.putText(frame, "ALERTA: MOTORISTA DORMINDO!", (50, 435),
                                cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
            else:
                contador_olho = 0

            if abs(inclinacao) > inclinacao_limiar:
                contador_cabeca = contador_cabeca + 1
                if contador_cabeca >= limite_frames_cabeca:
                    cv2.rectangle(frame, (30, 340), (610, 390), (0, 140, 255), -1)
                    cv2.putText(frame, "ALERTA: MOTORISTA DESATENTO!", (50, 375),
                                cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
            else:
                contador_cabeca = 0
    else:
        contador_olho = 0
        contador_cabeca = 0
        cv2.putText(frame, "Rosto nao detectado", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Detector de Sono', frame)
    if cv2.waitKey(10) & 0xFF == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()
