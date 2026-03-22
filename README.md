![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Detection-green)
![License](https://img.shields.io/badge/License-MIT-yellow)


# 🛰️ Monitoramento Inteligente de Tráfego em tempo real.   
### YOLOv8 + ByteTrack + Streamlit — Versão 1.0

Este projeto implementa um sistema completo de **monitoramento inteligente em tempo real**, capaz de analisar fluxos urbanos, rodoviários e ambientais utilizando visão computacional avançada.

Ele combina:

- **YOLOv8** para detecção de objetos  
- **ByteTrack** para rastreamento multi‑objeto  
- **Streamlit** para dashboard interativa  
- **Heatmap de movimento**  
- **Trajetórias dos objetos**  
- **Detecção de anomalias comportamentais**  
- **Contagem automática de objetos**  
- **Streaming direto do YouTube (via yt‑dlp)**  

---

# 🎯 Objetivo do Projeto

Criar uma plataforma capaz de:

- Monitorar **tráfego urbano**  
- Detectar e rastrear **veículos, pessoas e animais**  
- Identificar **anomalias de comportamento**  
- Gerar **heatmaps de movimento**  
- Exibir tudo em uma **dashboard web em tempo real**  
- Permitir uso com **câmeras públicas, privadas ou vídeos do YouTube**  

Aplicações:

- Segurança pública  
- Mobilidade urbana  
- Monitoramento ambiental  
- Vigilância inteligente  
- Estudos de comportamento animal  
- Análise de tráfego em rodovias e ferrovias  

---

# 🔍 Visão Geral do Sistema

O sistema funciona em 5 etapas principais:

## 1. Entrada de Vídeo
- Link do YouTube (live ou gravado)  
- Webcam  
- Arquivo local (opcional)  

## 2. Detecção de Objetos (YOLOv8)
Detecta automaticamente:

### Pessoas
- pessoa

### Veículos
- bicicleta  
- carro  
- moto  
- ônibus  
- caminhão  
- trem  
- barco  
- avião  

### Animais
- gato  
- cachorro  
- cavalo  
- ovelha  
- vaca  
- elefante  
- urso  
- zebra  
- girafa  

## 3. Rastreamento Multi‑Objeto (ByteTrack)
Atribui um **ID único** para cada objeto e mantém esse ID ao longo do vídeo.

## 4. Análises Inteligentes
- Trajetórias  
- Velocidade aproximada  
- Mudança brusca de direção  
- Heatmap de movimento  
- Anomalias:
  - pessoa correndo  
  - veículo com movimento errático  
  - animal em fuga  
  - avião descendo rápido  
  - trem parado por muito tempo  

## 5. Dashboard Streamlit
Exibe:

- Vídeo com marcações  
- Heatmap  
- Contagem por classe  
- IDs rastreados  
- Lista de anomalias  
- Alertas em tempo real  

---

# 🧠 Tecnologias Utilizadas

| Tecnologia | Função |
|-----------|--------|
| **YOLOv8** | Detecção de objetos |
| **ByteTrack** | Rastreamento multi‑objeto |
| **OpenCV** | Processamento de vídeo |
| **NumPy** | Cálculos e matrizes |
| **Streamlit** | Dashboard web |
| **yt‑dlp** | Extração de stream do YouTube |

---

# 📦 Instalação

## 1. Criar ambiente virtual (opcional)

```bash
python -m venv venv
venv\Scripts\activate
