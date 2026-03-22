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
