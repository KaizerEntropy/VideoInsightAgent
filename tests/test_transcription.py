from modules.transcriber import transcribe_audio

audio_file = "audio.wav"

transcript = transcribe_audio(audio_file)

print("\nTRANSCRIPT:")
print(transcript)