import yt_dlp
import os

def download_video_and_info(url, output_filename="sample.mp4"):
    """Downloads video and retrieves full metadata including heatmap data."""
    print(f"[Heatmap Extractor] Downloading metadata & video from {url}...")
    
    if os.path.exists(output_filename):
        try:
            os.remove(output_filename)
        except PermissionError:
            pass
          
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_filename,
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        
    heatmap_data = info.get('heatmap', [])
    print(f"[Heatmap Extractor] Extracted {len(heatmap_data) if heatmap_data else 0} heatmap data points.")
    return output_filename, heatmap_data, info.get('duration', 0)

def process_heatmap_peaks(heatmap_data, total_duration):
    """Parses heatMap intensity values and maps them to video timestamps."""
    if not heatmap_data:
        print("[Heatmap Extractor] Warning: No heatmap data available for this video.")
        return []

    processed_peaks = []
    for point in heatmap_data:
        start_time = point.get('start_time', 0)
        end_time = point.get('end_time', 0)
        value = point.get('value', 0.0)
        
        processed_peaks.append({
            'start': start_time,
            'end': end_time,
            'intensity': value
        })
        
    return processed_peaks
