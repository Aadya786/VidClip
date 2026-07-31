# VidClip

VidClip Pro is an automated Python pipeline and Streamlit dashboard that converts long-form YouTube videos (1–5 minutes) into engaging, vertical (9:16) short-form highlight clips. Instead of relying solely on basic keyword searches, VidClip Pro utilizes a **multimodal scoring engine** that analyzes viewer engagement graphs, audio volume spikes, and speech context to isolate the most high-value moments.

---

## Key Features

- **YouTube Engagement Heatmaps:** Extracts "Most Replayed" data using `yt-dlp` to pinpoint exact timestamps where viewers rewatch content.
- **Audio Energy Peak Detection:** Analyzes RMS audio volume using `pydub` to detect laughter, shouts, cheering, or vocal intensity.
- **Speech Transcription & Context Chunking:** Uses OpenAI's Whisper model to transcribe dialogue and group sentences into coherent 30–45 second ideas.
- **Multimodal Scoring Engine:** Combines retention, audio spikes, and semantic evaluation into a unified performance score.
- **Dynamic Keywords:** Allows users to input custom priority keywords via the Streamlit interface, with automatic fallback to high-engagement defaults.
- **Automated Vertical Re-framing:** Automatically center-crops landscape videos into 9:16 vertical shorts using MoviePy.
- **Interactive UI:** Built with Streamlit for previewing scores, viewing generated video clips, reading transcript summaries, and downloading output files.

 ## Stack
 
Frontend Interface: Streamlit
Video Extraction: yt-dlp
Speech Recognition: openai-whisper
Audio Processing: pydub, numpy
Video Processing & Editing: moviepy

