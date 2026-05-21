import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_desenho = mp.solutions.drawing_utils

pose = mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)

contador = 0
estado = "fechado"

# fator pra considerar pernas abertas/fechadas em relacao a largura dos ombros
fator_pernas_aberto = 1.2
fator_pernas_fechado = 0.9


def pegar_ponto(lm, indice):
    return lm[indice]


cap = cv2.VideoCapture(0)

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        continue

    frame = cv2.flip(frame, 1)
    altura, largura, _ = frame.shape

    saida_pose = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if saida_pose.pose_landmarks:
        mp_desenho.draw_landmarks(frame, saida_pose.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_desenho.DrawingSpec(color=(255, 102, 102), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_desenho.DrawingSpec(color=(102, 204, 0), thickness=2, circle_radius=2))

        lm = saida_pose.pose_landmarks.landmark

        ombro_esq = pegar_ponto(lm, mp_pose.PoseLandmark.LEFT_SHOULDER.value)
        ombro_dir = pegar_ponto(lm, mp_pose.PoseLandmark.RIGHT_SHOULDER.value)
        pulso_esq = pegar_ponto(lm, mp_pose.PoseLandmark.LEFT_WRIST.value)
        pulso_dir = pegar_ponto(lm, mp_pose.PoseLandmark.RIGHT_WRIST.value)
        tornozelo_esq = pegar_ponto(lm, mp_pose.PoseLandmark.LEFT_ANKLE.value)
        tornozelo_dir = pegar_ponto(lm, mp_pose.PoseLandmark.RIGHT_ANKLE.value)

        # no opencv o eixo Y cresce pra baixo, entao pulso "acima" do ombro tem Y menor
        bracos_para_cima = pulso_esq.y < ombro_esq.y and pulso_dir.y < ombro_dir.y
        bracos_para_baixo = pulso_esq.y > ombro_esq.y and pulso_dir.y > ombro_dir.y

        dist_tornozelos = abs(tornozelo_esq.x - tornozelo_dir.x)
        dist_ombros = abs(ombro_esq.x - ombro_dir.x)

        pernas_abertas = dist_tornozelos > dist_ombros * fator_pernas_aberto
        pernas_fechadas = dist_tornozelos < dist_ombros * fator_pernas_fechado

        # maquina de estados: fechado -> aberto -> fechado conta 1 polichinelo
        if bracos_para_cima and pernas_abertas:
            if estado == "fechado":
                estado = "aberto"

        if bracos_para_baixo and pernas_fechadas:
            if estado == "aberto":
                contador = contador + 1
                estado = "fechado"

        cv2.rectangle(frame, (0, 1), (320, 110), (58, 58, 55), -1)
        cv2.putText(frame, f"Polichinelos: {contador}", (10, 40),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Estado: {estado}", (10, 80),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

        # cor da borda muda quando ta no estado aberto (so pra dar um feedback visual)
        if estado == "aberto":
            cv2.rectangle(frame, (0, 0), (largura - 1, altura - 1), (0, 255, 0), 4)

    else:
        cv2.putText(frame, "Corpo nao detectado", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Contador de Polichinelo', frame)
    if cv2.waitKey(10) & 0xFF == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()
