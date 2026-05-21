# CP3 - MediaPipe

Projeto com dois exercicios usando Python, OpenCV e MediaPipe.

## Exercicios

### 1. Contador de Polichinelo (`contador_polichinelo.py`)
Captura a webcam em tempo real, detecta os landmarks do corpo usando o
MediaPipe Pose e conta automaticamente quantos polichinelos a pessoa fez.

Funciona usando uma maquina de estados simples:
- **fechado**: bracos abaixados e pernas juntas
- **aberto**: bracos acima dos ombros e pernas afastadas
- Cada ciclo `fechado -> aberto -> fechado` conta 1 polichinelo

A borda da tela fica verde quando o sistema reconhece o estado "aberto",
e o contador aparece no canto superior esquerdo.

### 2. Detector de Sono do Motorista (`detector_sono.py`)
Captura a webcam, detecta o rosto com o MediaPipe Face Mesh e monitora
sinais de sonolencia:
- **EAR (Eye Aspect Ratio)**: se o olho fica fechado por muitos frames
  seguidos, mostra o alerta "MOTORISTA DORMINDO".
- **Inclinacao da cabeca**: se a cabeca fica muito inclinada por muitos
  frames seguidos, mostra o alerta "MOTORISTA DESATENTO".

## Requisitos

- Python **3.12** (o 3.13/3.14 ainda nao tem suporte completo do MediaPipe)
- Webcam funcionando
- Windows, Linux ou macOS

## Como rodar

### 1. Criar e ativar a venv

No Windows (cmd):
```cmd
py -3.12 -m venv venv
venv\Scripts\activate
```

No Linux/macOS:
```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias
```
pip install -r requirements.txt
```

### 3. Rodar
```
python contador_polichinelo.py
```
ou
```
python detector_sono.py
```

Em ambos, aperte a tecla **`c`** pra fechar a janela.

## Dicas de uso

### Contador de polichinelo
- Fique a uns 2 metros da webcam pra aparecer o corpo inteiro
  (ombros, maos e tornozelos precisam estar no quadro).
- Se o contador estiver muito sensivel, abra mais `fator_pernas_aberto`
  (ex: 1.4) no arquivo. Se nao contar, diminua os fatores.

### Detector de sono
- Mantenha o rosto enquadrado e iluminado.
- Pra testar o alerta de sono, feche os olhos por ~1 segundo.
- Pra testar o alerta de desatencao, incline a cabeca pro lado.
- Os limiares (`ear_limiar`, `inclinacao_limiar`) podem ser ajustados
  no comeco do arquivo se quiser deixar mais ou menos sensivel.

## Problemas comuns

**Erro `module 'mediapipe' has no attribute 'solutions'`**
Voce esta usando uma versao do Python que o MediaPipe nao suporta
direito (3.13 ou 3.14). Recrie a venv com Python 3.12.

**Webcam nao abre**
Mude `cv2.VideoCapture(0)` pra `cv2.VideoCapture(1)` nos arquivos
(testa outra camera do sistema).

**`py -3.12` nao encontrado**
Instala o Python 3.12 em https://www.python.org/downloads/release/python-3128/
e marca "Add python.exe to PATH" no instalador.
