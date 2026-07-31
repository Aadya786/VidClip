from moviepy import VideoFileClip

def render_vertical_clip(video_path, start, end, output_filename):
    """Cuts segment and crops center to 9:16 vertical short format."""
    print(f"[Video Renderer] Processing vertical clip ({start:.1f}s - {end:.1f}s) -> {output_filename}")
    
    with VideoFileClip(video_path) as video:
        if hasattr(video, 'subclipped'):
            clip = video.subclipped(start, end)
        else:
            clip = video.subclip(start, end)
        w, h = clip.size
        target_w = int(h * (9 / 16))
        
        if target_w < w:
            x_center = w / 2
            x1 = x_center - (target_w / 2)
            if hasattr(clip, 'cropped'):
                clip = clip.cropped(x1=x1, width=target_w)
            else:
                clip = clip.crop(x1=x1, width=target_w)

        clip.write_videofile(
            output_filename,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )
    print(f"[Video Renderer] Successfully created {output_filename}\n")
