import os
from pathlib import Path
import wave
import numpy as np
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

output_dir = Path('output')
video_dir = Path('output/generated_images')
images = sorted(video_dir.glob('*.png'))
print('found images', len(images))
if not images:
    raise SystemExit('no images found')

duration_sec = 21*60
frame_rate = 16000
n_frames = duration_sec * frame_rate
audio_path = output_dir / 'narration_placeholder.wav'
if not audio_path.exists():
    with wave.open(str(audio_path), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(frame_rate)
        wf.writeframes(b'\x00\x00' * n_frames)
    print('created audio')
else:
    print('audio exists')

frames = []
target_size = (1920, 1080)
for p in images:
    img = Image.open(p).convert('RGB').resize(target_size)
    frames.append(np.array(img))

per_image = duration_sec / len(frames)
clip = ImageSequenceClip(frames, durations=[per_image]*len(frames))
clip = clip.with_audio(AudioFileClip(str(audio_path)))
final_path = output_dir / 'preview_21min.mp4'
clip.write_videofile(str(final_path), fps=24, codec='libx264', audio_codec='aac', bitrate='2000k')
print('done', final_path)
