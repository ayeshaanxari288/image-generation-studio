# Multimodal Image Generation Studio

**DecodeLabs Industrial Training — Batch 2026**  
Project 3 — Generative AI Track

---

## Overview

A production-grade web application that converts natural language text prompts into high-quality digital images using the Stability AI REST API. Built with a complete engineering pipeline covering network resilience, memory-safe binary streaming, and automated quality verification.

## Features

- Text-to-image generation via Stability AI
- Multiple aspect ratios — 1:1, 16:9, 9:16, 4:3
- Style presets — photographic, cinematic, digital-art, neon-punk, anime, and more
- Exponential backoff retry logic
- Memory-safe chunked binary streaming
- Pixel-level image integrity verification
- Dual security gate handling
- One-click image download

## Tech Stack

- Python
- Streamlit
- Stability AI REST API
- Pillow

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to Deploy

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Deploy — your live link is ready

## Pipeline Architecture

| Layer | Description |
|-------|-------------|
| Payload Construction | Prompt + exact resolution mapping |
| Network Gateway | Split timeout — 3.05s connect, 90s read |
| Retry Logic | Exponential backoff with jitter |
| Binary Streaming | Memory-safe 64KB chunked download |
| Integrity Verification | Pixel-level decode via Pillow |
| Security Gates | Input and output content moderation handling |
