import config
from heatmap_extractor import download_video_and_info, process_heatmap_peaks
from audio_analyzer import analyze_audio_energy
from transcriber import transcribe_and_chunk
from llm_scorer import score_chunk_with_llm
from video_renderer import render_vertical_clip

def calculate_multimodal_score(chunk, heatmap_peaks, audio_energies):
    """Calculates composite Viral Potential Score using weights from config."""
    c_start, c_end = chunk['start'], chunk['end']

    h_scores = [p['intensity'] for p in heatmap_peaks if c_start <= p['start'] <= c_end]
    avg_heatmap = (sum(h_scores) / len(h_scores)) if h_scores else 0.3

    a_scores = [a['norm_energy'] for a in audio_energies if c_start <= a['start'] <= c_end]
    avg_audio = (sum(a_scores) / len(a_scores)) if a_scores else 0.3

    llm_score_10, reasoning = score_chunk_with_llm(chunk['text'])
    norm_llm = llm_score_10 / 10.0

    final_score = (
        (config.WEIGHT_HEATMAP * avg_heatmap) +
        (config.WEIGHT_AUDIO_ENERGY * avg_audio) +
        (config.WEIGHT_LLM_SCORE * norm_llm)
    )

    return final_score, reasoning

def run_pipeline(youtube_url):
    video_file = "sample.mp4"

    video_path, heatmap_raw, duration = download_video_and_info(youtube_url, video_file)
    heatmap_peaks = process_heatmap_peaks(heatmap_raw, duration)

    audio_energies = analyze_audio_energy(video_path)

    chunks = transcribe_and_chunk(video_path)

    scored_candidates = []
    print("\n[Pipeline] Scoring candidate clips using Multimodal Engine...")
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

    top_clips = scored_candidates[:config.MAX_OUTPUT_CLIPS]
    print(f"\n[Pipeline] Rendering Top {len(top_clips)} High-V value Clip(s):\n")

    for i, clip in enumerate(top_clips):
        print(f"--- Clip #{i+1} (Score: {clip['score']:.2f}) ---")
        print(f"Time: {clip['start']:.1f}s to {clip['end']:.1f}s")
        print(f"Text Preview: \"{clip['text'][:80]}...\"")
        print(f"Analysis: {clip['reasoning']}")

        output_file = f"viral_highlight_{i+1}.mp4"
        render_vertical_clip(video_path, clip['start'], clip['end'], output_file)

if __name__ == "__main__":
    TEST_URL = "https://www.youtube.com/watch?v=Y6bbMQXQ180"
    run_pipeline(TEST_URL)
