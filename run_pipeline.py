from modules.audio_extractor import extract_audio
from modules.transcriber import transcribe_audio
from modules.summarizer import summarize_transcript
from modules.chunker import split_transcript
from modules.vector_store import create_vector_store, retrieve
from modules.qa_agent import answer_question


video_path = input("Enter video path: ")

# Step 1: Extract audio
audio_path = extract_audio(video_path)

# Step 2: Transcribe
transcript = transcribe_audio(audio_path)

# Step 3: Summarize
summary = summarize_transcript()

print("\nVIDEO SUMMARY:\n")
print(summary)

# Step 4: Prepare QA system
chunks = split_transcript()
index, chunks = create_vector_store(chunks)

print("\nYou can now ask questions about the video.")
print("Type 'exit' to quit.\n")

while True:

    question = input("Question: ")

    if question.lower() == "exit":
        break

    relevant_chunks = retrieve(question, index, chunks)

    answer = answer_question(question, relevant_chunks)

    print("\nAnswer:\n")
    print(answer)
    print()