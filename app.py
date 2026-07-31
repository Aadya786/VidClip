import streamlit as st
import os
import config
from heatmap_extractor import download_video_and_info, process_heatmap_peaks
from audio_analyzer import analyze_audio_energy
from transcriber import transcribe_and_chunk
from main import calculate_multimodal_score
from video_renderer import render_vertical_clip

st.set_page_config(
    page_title="VidClip Pro",
    layout="wide"
)

st.title("VidClip Pro: AI Short-Form Video Generator")
st.markdown("Paste a YouTube video link (1–5 minutes) to automatically extract top viral moments in vertical 9:16 format.")

st.sidebar.header("Pipeline Settings")

num_clips = st.sidebar.slider(
    "Number of clips to generate", 
    min_value=1, 
    max_value=5, 
    value=3
)
config.MAX_OUTPUT_CLIPS = num_clips

st.sidebar.subheader("Focus Keywords")
custom_keywords_input = st.sidebar.text_area(
    "Custom Keywords (Optional)",
    placeholder="e.g., secret, mistake, crazy, goal, hilarious",
    help="Enter comma-separated words. If left empty, default high-engagement keywords will be used."
)

if custom_keywords_input.strip():
    user_words = [w.strip().lower() for w in custom_keywords_input.split(",") if w.strip()]
    if user_words:
        config.FALLBACK_KEYWORDS = user_words

st.subheader("YouTube Input")
youtube_url = st.text_input(
    "YouTube Video URL", 
    placeholder="https://www.youtube.com/watch?v=..."
)

if st.button("Process and Create Clips", type="primary", use_container_width=True):
    if not youtube_url.strip():
        st.error("Please enter a valid YouTube URL.")
    else:
        video_file = "sample.mp4"
        
        with st.status("Running VidClip Engine...", expanded=True) as status:

            st.write("Downloading YouTube video and metadata...")
            video_path, heatmap_raw, duration = download_video_and_info(youtube_url, video_file)
            
            st.write("Extracting YouTube 'Most Replayed' engagement graph...")
            heatmap_peaks = process_heatmap_peaks(heatmap_raw, duration)

            st.write("Analyzing audio energy peaks and volume spikes...")
            audio_energies = analyze_audio_energy(video_path)

            st.write("Transcribing audio with OpenAI Whisper...")
            chunks = transcribe_and_chunk(video_path)

            st.write("Aggregating multimodal signals and scoring moments...")
            scored_candidates = []
            for chunk in chunks:
                score, reasoning = calculate_multimodal_score(chunk, heatmap_peaks, audio_energies)
                scored_candidates.append({
                    'start': chunk['start'],
                    'end': chunk['end'],
                    'text': chunk['text'],
                    'score': score,
                    'reasoning': reasoning
                })

            scored_candidates.sort(key=lambda x: x['score'], reverse=True)
            top_clips = scored_candidates[:num_clips]

            st.write("Cropping to 9:16 vertical shorts and rendering output files...")
            generated_clips = []
            for i, clip in enumerate(top_clips):
                output_file = f"viral_highlight_{i+1}.mp4"
                render_vertical_clip(video_path, clip['start'], clip['end'], output_file)
                generated_clips.append((output_file, clip))

            status.update(label="Processing Complete!", state="complete", expanded=False)

        st.divider()
        st.subheader("Top Highlight Clips")
        
        cols = st.columns(len(generated_clips))
        for idx, (file_path, clip_data) in enumerate(generated_clips):
            with cols[idx]:
                st.markdown(f"### Clip #{idx+1}")
                st.caption(
                    f"Score: **{clip_data['score']:.2f}** | "
                    f"Time: **{clip_data['start']:.1f}s - {clip_data['end']:.1f}s**"
                )
                
                if os.path.exists(file_path):
                    st.video(file_path)
                    
                    with open(file_path, "rb") as video_bytes:
                        st.download_button(
                            label=f"Download Clip #{idx+1}",
                            data=video_bytes,
                            file_name=file_path,
                            mime="video/mp4",
                            key=f"dl_{idx}",
                            use_container_width=True
                        )
                
                with st.expander("Transcript and Analysis"):
                    st.write(f"**Transcript:** \"{clip_data['text']}\"")
                    st.write(f"**Evaluation:** {clip_data['reasoning']}")
