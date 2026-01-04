import os

from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

MUSIC_PATH = os.path.join(
    "services",
    "assets",
    "corporate-background-music-446651.mp3"
)


def create_video_from_image(image_path: str, duration: int = 6) -> str:
    """
    Takes a creative image path (e.g. 'static/creative_final.png'),
    combines it with a background music track, and exports an MP4.
    Returns the URL path: '/static/creative_final.mp4'.
    """

    if image_path.startswith("/"):
        image_path = image_path.lstrip("/")

    # 1) Still image → video clip (MoviePy v2: with_duration)
    clip = ImageClip(image_path).with_duration(duration)

    # 2) Optional background music (MoviePy v2: subclipped + with_audio)
    if os.path.exists(MUSIC_PATH):
        audio = AudioFileClip(MUSIC_PATH).subclipped(0, duration)
        clip = clip.with_audio(audio)

    out_path = os.path.join(STATIC_DIR, "creative_final.mp4")

    clip.write_videofile(
        out_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
    )

    return "/static/creative_final.mp4"
