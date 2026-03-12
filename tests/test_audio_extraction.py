from modules.audio_extractor import extract_audio

video_file = "test_video.mp4"

audio_path = extract_audio(video_file)

print("Audio file created:", audio_path)