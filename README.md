# 🎵 AI Stem Extractor

[![Live Demo](https://img.shields.io/badge/Live_Demo-Play_Now-success?style=for-the-badge)](https://mitsuha16-stem-extractor.hf.space)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)]()

A full-stack AI web application that uses deep learning to isolate and extract specific audio elements (Vocals, Drums, Bass, and Other Instruments) directly from video and audio files. 

## 🚀 Live Demo
Test the live application here: **[AI Stem Extractor on Hugging Face](https://mitsuha16-stem-extractor.hf.space)**

## ✨ Features
* **Multi-Format Support:** Upload both standard audio (`.mp3`, `.wav`) and video files (`.mp4`, `.mov`).
* **AI Source Separation:** Leverages Meta's state-of-the-art Hybrid Transformer Demucs model.
* **Custom Stem Mixing:** Selectively combine extracted vocals, drums, bass, or melody into a custom track.
* **Automated Video Recombination:** Automatically strips audio from a video, processes the AI extraction, and stitches the newly isolated audio back onto the original video file.
* **Session Security:** Utilizes secure, temporary system directories to ensure user files are isolated and automatically purged after processing.

## 🛠️ Technical Stack
* **Frontend:** Streamlit
* **AI/ML Model:** PyTorch & Demucs (htdemucs)
* **Media Processing:** MoviePy (FFmpeg) & PyDub
* **Deployment:** Dockerized environment hosted via Hugging Face Spaces.

## 💻 How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/srijonchakma13/ai-stem-extractor.git](https://github.com/srijonchakma13/ai-stem-extractor.git)
   cd ai-stem-extractor
