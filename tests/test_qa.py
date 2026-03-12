from modules.chunker import split_transcript
from modules.vector_store import create_vector_store, retrieve
from modules.qa_agent import answer_question


chunks = split_transcript()

index, chunks = create_vector_store(chunks)

question = input("Ask a question about the video: ")

relevant_chunks = retrieve(question, index, chunks)

answer = answer_question(question, relevant_chunks)

print("\nANSWER:\n")
print(answer)