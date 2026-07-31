import whisper

def transcribe_and_chunk(video_path, target_chunk_duration=35):
    """Transcribes video and aggregates short Whisper segments into contextual chunks."""
    print("[Transcriber] Loading Whisper model...")
    model = whisper.load_model("base")
    
    print(f"[Transcriber] Transcribing '{video_path}'...")
    result = model.transcribe(video_path, verbose=False)
    raw_segments = result.get('segments', [])
    
    chunks = []
    current_text = []
    current_start = None
    current_end = 0

    for seg in raw_segments:
        if current_start is None:
            current_start = seg['start']
            
        current_text.append(seg['text'].strip())
        current_end = seg['end']
        
        if (current_end - current_start) >= target_chunk_duration:
            chunks.append({
                'start': current_start,
                'end': current_end,
                'text': " ".join(current_text)
            })
            current_text = []
            current_start = None

    if current_text and current_start is not None:
        chunks.append({
            'start': current_start,
            'end': current_end,
            'text': " ".join(current_text)
        })

    print(f"[Transcriber] Created {len(chunks)} contextual speech chunks.")
    return chunks
