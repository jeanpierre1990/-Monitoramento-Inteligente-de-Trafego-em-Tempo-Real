# 🧩 Arquitetura do Sistema — Monitoramento Inteligente de Tráfego em tempo real.

Este documento descreve a arquitetura interna do sistema, seus componentes, fluxo de dados, decisões técnicas e como cada módulo interage para entregar monitoramento inteligente em tempo real.

---

# 🏗️ 1. Visão Geral da Arquitetura

O sistema é composto por cinco camadas principais:

1. **Entrada de vídeo**
2. **Processamento de detecção (YOLOv8)**
3. **Rastreamento multiobjeto (ByteTrack)**
4. **Módulos de análise inteligente**
5. **Dashboard interativa (Streamlit)**

Fluxo simplificado:


---

# 🎥 2. Camada de Entrada de Vídeo

### Fontes suportadas:
- URL do YouTube (via `yt-dlp`)
- Webcam local
- Arquivo de vídeo

### Responsabilidades:
- Capturar frames em tempo real
- Garantir taxa de FPS estável
- Converter frames para o formato esperado pelo YOLO

### Tecnologias:
- OpenCV
- yt-dlp

---

# 🧠 3. Detecção de Objetos (YOLOv8)

YOLOv8 é responsável por:

- Detectar objetos em cada frame
- Classificar cada objeto (pessoa, carro, animal, etc.)
- Retornar bounding boxes, confiança e classe

### Saída típica:

```json
{
  "bbox": [x1, y1, x2, y2],
  "confidence": 0.87,
  "class": "car"
}
