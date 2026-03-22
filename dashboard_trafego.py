import cv2
import time
import math
import subprocess
import numpy as np
from collections import defaultdict, Counter

import streamlit as st
from ultralytics import YOLO

########################################
# 1. Função para extrair URL do YouTube
########################################

def extrair_stream_youtube(youtube_url: str) -> str | None:
    comando = ["yt-dlp", "-g", youtube_url]
    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode != 0:
        print("Erro ao extrair URL do YouTube:", resultado.stderr)
        return None

    urls = resultado.stdout.strip().split("\n")
    return urls[0] if urls else None

########################################
# 2. Classes expandidas (COCO)
########################################

CLASSES_INTERESSE = {
    0: "pessoa",
    1: "bicicleta",
    2: "carro",
    3: "moto",
    4: "avião",
    5: "ônibus",
    6: "trem",
    7: "caminhão",
    8: "barco",
    14: "gato",
    15: "cachorro",
    16: "cavalo",
    17: "ovelha",
    18: "vaca",
    19: "elefante",
    20: "urso",
    21: "zebra",
    22: "girafa"
}

########################################
# 3. Trajetórias, anomalias e contagem
########################################

def atualizar_trajetorias(tracked_boxes, trajectories, timestamps):
    agora = time.time()
    for box in tracked_boxes:
        x1, y1, x2, y2, track_id, cls = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        trajectories[track_id].append((cx, cy))
        timestamps[track_id].append(agora)
    return trajectories, timestamps


def detectar_anomalias(tracked_boxes, trajectories, timestamps):
    anomalies = []

    for box in tracked_boxes:
        x1, y1, x2, y2, track_id, cls = box
        traj = trajectories[track_id]
        times = timestamps[track_id]

        if len(traj) < 3:
            continue

        dx = traj[-1][0] - traj[-2][0]
        dy = traj[-1][1] - traj[-2][1]
        dt = times[-1] - times[-2] if times[-1] > times[-2] else 1e-3
        speed = math.sqrt(dx*dx + dy*dy) / dt

        dx1 = traj[-2][0] - traj[-3][0]
        dy1 = traj[-2][1] - traj[-3][1]
        v1 = np.array([dx1, dy1], dtype=float)
        v2 = np.array([dx, dy], dtype=float)

        if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
            cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            cosang = np.clip(cosang, -1, 1)
            angle = math.degrees(math.acos(cosang))
        else:
            angle = 0

        # --- ANOMALIAS EXPANDIDAS ---
        if cls == 0 and speed > 120:
            anomalies.append((track_id, "Pessoa correndo"))

        if cls in [2, 3, 5, 7] and angle > 90:
            anomalies.append((track_id, "Veículo com movimento errático"))

        if cls in [14, 15, 16, 17, 18, 19, 20, 21, 22] and speed > 150:
            anomalies.append((track_id, "Animal em movimento rápido"))

        if cls == 4 and dy > 50:
            anomalies.append((track_id, "Avião descendo rapidamente"))

        if cls == 6 and speed < 2 and len(traj) > 50:
            anomalies.append((track_id, "Trem parado por muito tempo"))

    return anomalies


def atualizar_contagem(tracked_boxes, seen_ids):
    for box in tracked_boxes:
        _, _, _, _, track_id, _ = box
        seen_ids.add(track_id)

    contagem_frame = Counter()
    for box in tracked_boxes:
        _, _, _, _, _, cls = box
        if cls in CLASSES_INTERESSE:
            contagem_frame[CLASSES_INTERESSE[cls]] += 1

    return contagem_frame, seen_ids

########################################
# 4. Desenho no frame + heatmap
########################################

def desenhar_overlay(frame, tracked_boxes, trajectories, anomalies, heatmap):
    anomaly_ids = {a[0] for a in anomalies}

    for box in tracked_boxes:
        x1, y1, x2, y2, track_id, cls = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        if 0 <= cy < heatmap.shape[0] and 0 <= cx < heatmap.shape[1]:
            heatmap[cy, cx] += 1

    for box in tracked_boxes:
        x1, y1, x2, y2, track_id, cls = box

        color = (0, 255, 0)
        if track_id in anomaly_ids:
            color = (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        nome = CLASSES_INTERESSE.get(cls, "objeto")
        label = f"ID {track_id} {nome}"

        cv2.putText(frame, label, (x1, max(0, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        if track_id in trajectories:
            pts = trajectories[track_id][-30:]
            for i in range(1, len(pts)):
                cv2.line(frame, pts[i-1], pts[i], color, 2)

    hm_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    hm_uint8 = hm_norm.astype(np.uint8)
    hm_color = cv2.applyColorMap(hm_uint8, cv2.COLORMAP_JET)
    hm_color = cv2.addWeighted(frame, 0.6, hm_color, 0.4, 0)

    return frame, hm_color

########################################
# 5. Loop principal com Streamlit
########################################

def main():
    st.set_page_config(page_title="Monitoramento Inteligente", layout="wide")

    st.title("🛰️ Monitoramento Inteligente de Tráfego e Fauna — YOLOv8 + ByteTrack")

    col1, col2 = st.columns([2, 1])

    with col2:
        youtube_url = st.text_input(
            "URL do YouTube (live ou vídeo)",
            "https://youtu.be/z1E5ciDe3a0"
        )
        conf_thres = st.slider("Confiança mínima YOLO", 0.1, 0.9, 0.4, 0.05)
        run_button = st.button("Iniciar monitoramento")

    frame_placeholder = col1.empty()
    heatmap_placeholder = col1.empty()
    info_placeholder = col2.empty()
    alert_placeholder = col2.empty()

    if not run_button:
        st.stop()

    stream_url = extrair_stream_youtube(youtube_url)
    if not stream_url:
        st.error("Não foi possível extrair o stream do YouTube.")
        st.stop()

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        st.error("Não foi possível abrir o vídeo/stream.")
        st.stop()

    model = YOLO("yolov8n.pt")
    tracker_cfg = "bytetrack.yaml"

    trajectories = defaultdict(list)
    timestamps = defaultdict(list)
    seen_ids = set()
    heatmap = None

    last_alert_time = 0
    alert_cooldown = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Stream encerrado ou travado.")
            break

        if heatmap is None:
            h, w, _ = frame.shape
            heatmap = np.zeros((h, w), dtype=np.float32)

        results = model.track(
            frame,
            tracker=tracker_cfg,
            persist=True,
            conf=conf_thres,
            verbose=False
        )

        tracked_boxes = []
        if results and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            clss = results[0].boxes.cls.cpu().numpy().astype(int)

            for (x1, y1, x2, y2), tid, cls in zip(boxes, ids, clss):
                if cls in CLASSES_INTERESSE:
                    tracked_boxes.append([
                        int(x1), int(y1), int(x2), int(y2),
                        int(tid), int(cls)
                    ])

        trajectories, timestamps = atualizar_trajetorias(
            tracked_boxes, trajectories, timestamps
        )
        anomalies = detectar_anomalias(tracked_boxes, trajectories, timestamps)
        contagem_frame, seen_ids = atualizar_contagem(tracked_boxes, seen_ids)

        frame_drawn, heatmap_img = desenhar_overlay(
            frame.copy(), tracked_boxes, trajectories, anomalies, heatmap
        )

        frame_rgb = cv2.cvtColor(frame_drawn, cv2.COLOR_BGR2RGB)
        heatmap_rgb = cv2.cvtColor(heatmap_img, cv2.COLOR_BGR2RGB)

        frame_placeholder.image(frame_rgb)
        heatmap_placeholder.image(heatmap_rgb)

        with info_placeholder.container():
            st.subheader("📊 Contagem atual no frame")
            for k, v in contagem_frame.items():
                st.write(f"- **{k}**: {v}")

            st.subheader("📈 Total de IDs únicos rastreados")
            st.write(len(seen_ids))

            st.subheader("⚠️ Anomalias detectadas")
            if anomalies:
                for aid, desc in anomalies:
                    st.write(f"- ID {aid}: {desc}")
            else:
                st.write("Nenhuma anomalia.")

        now = time.time()
        if anomalies and (now - last_alert_time > alert_cooldown):
            with alert_placeholder.container():
                st.error("⚠️ ALERTA: comportamento anômalo detectado!")
                for aid, desc in anomalies:
                    st.write(f"- ID {aid}: {desc}")
            last_alert_time = now

        time.sleep(0.03)

    cap.release()

if __name__ == "__main__":
    main()