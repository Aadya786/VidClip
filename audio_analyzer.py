import numpy as np
from pydub import AudioSegment

def analyze_audio_energy(video_path, window_sec=2):
    """Calculates RMS audio energy in sliding time windows across the audio track."""
    print("[Audio Analyzer] Analyzing audio volume peaks...")
    
    try:
        audio = AudioSegment.from_file(video_path)
    except Exception as e:
        print(f"[Audio Analyzer] Error loading audio: {e}")
        return []

    audio = audio.set_channels(1)
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    sample_rate = audio.frame_rate
    
    window_samples = int(window_sec * sample_rate)
    energies = []
    
    for i in range(0, len(samples) - window_samples, window_samples):
        window = samples[i:i + window_samples]
        rms = np.sqrt(np.mean(window ** 2))
        start_time = i / sample_rate
        energies.append({
            'start': start_time,
            'end': start_time + window_sec,
            'rms': rms
        })
        
    if not energies:
        return []

    max_rms = max(e['rms'] for e in energies) or 1.0
    for e in energies:
        e['norm_energy'] = e['rms'] / max_rms
        
    return energies
