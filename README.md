# 🎥 Video Insight Agent

An AI-powered system that transforms videos into searchable, structured knowledge.

🔗 **Live Demo:**  
https://videoinsightagent.streamlit.app

---

# 🚀 Overview

Video Insight Agent enables users to upload videos or provide YouTube links, automatically transcribe the content, translate non-English videos, generate structured insights, and interact with videos using semantic search and conversational AI.

The system turns raw video content into an **interactive knowledge base**.

---

# ✨ Key Highlights

- 🎨 Modern, clean, and responsive UI for smooth interaction  
- 🌍 Supports Hindi & Bengali videos via automatic translation to English  
- ⚡ Faster and smoother processing pipeline  
- 🧠 Improved AI chatbot with better contextual understanding  
- 🔎 Semantic search across all videos  
- 💬 Conversational Q&A with timestamp citations  

---

# 🚀 Features

## 📹 Multi-Video Processing

Supports:
- Single uploaded video  
- Multiple uploaded videos  
- Single YouTube video  
- Multiple YouTube videos  

All videos are processed together into a unified semantic search system.

---

## 🌍 Multilingual Video Support

The system supports:
- Hindi videos  
- Bengali videos  

Pipeline:

```
Video → Transcription → Translation → English Processing
```

---

## 🎨 Enhanced UI/UX

- Clean and modern interface  
- Better layout and interaction flow  
- Improved responsiveness  

---

## 🎙 Automatic Transcription

Uploaded videos:

```
Video → Audio Extraction → Whisper Transcription
```

YouTube videos:

```
YouTube URL → Transcript API
```

Each transcript is broken into timestamped segments.

---

## 🧠 AI Video Understanding

The system generates:

- AI summaries  
- Study flashcards  
- Timestamped timelines  
- Semantic search results  
- Conversational answers  

---

## ⚡ Improved AI Chatbot

- Better understanding of transcript context  
- More accurate and relevant answers  
- Improved reasoning using retrieved segments  
- More efficient learning from video content  

---

## ⏱ Timeline Generation

Example:

```
0:00 — Introduction to the software
0:45 — Demonstration of typing transcript
1:20 — Keyboard shortcuts overview
2:10 — Timestamp insertion method
3:30 — Workflow explanation
```

---

## 🔎 Semantic Timestamp Search

Example:

```
keyboard shortcuts
```

Returns the most relevant timestamp and transcript segment.

---

## 💬 Conversational Video QA

Example:

```
What software is demonstrated in the video?
```

Output:

```
Answer:
The video demonstrates the transcription tool Inkscribe.

Sources:
YouTube Video 1 — 0:35
Uploaded Video 1 — 1:04
```

---

# 🧠 System Architecture

## 1️⃣ Input Layer

- Uploaded video files  
- YouTube URLs  

---

## 2️⃣ Transcription Layer

Uploaded videos:

```
Video → Audio Extraction → Whisper
```

YouTube videos:

```
YouTube → Transcript API
```

---

## 3️⃣ Translation Layer

```
Non-English Transcript → Translation → English
```

---

## 4️⃣ Transcript Segmentation

Each transcript becomes:

```
Video Label | Timestamp | Text
```

Example:

```
YouTube Video 1 | 1:24 | The software allows users to insert timestamps while typing.
```

---

## 5️⃣ Vector Search (FAISS)

- Transcripts are converted into embeddings  
- Stored in a vector database  

Enables:
- Semantic search  
- Context retrieval  

---

## 6️⃣ LLM Processing

Generates:
- Summary  
- Flashcards  
- Timelines  

---

## 7️⃣ Retrieval-Augmented Generation (RAG)

1. Query embedding is created  
2. Relevant segments are retrieved  
3. Context is passed to the LLM  
4. Answer is generated with timestamp citations  

---

# 📂 Project Structure

```
Video_Insight_Agent
│
├── app.py
├── README.md
├── requirements.txt
│
├── modules
│   ├── audio_extractor.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── flashcards.py
│   ├── timeline_generator.py
│   ├── vector_store.py
│   ├── qa_agent.py
│   ├── translator.py
│   └── youtube_transcript.py
│
├── services
├── ui
├── assets
├── downloads
└── tests
```

---

# ⚙️ Installation

```
git clone git@github.com:KaizerEntropy/VideoInsightAgent.git
```

```
cd VideoInsightAgent
```

```
python -m venv venv
```

Linux / macOS:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

```
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

```
GROQ_API_KEY=your_api_key_here
```

---

# ▶ Running the Application

```
streamlit run app.py
```

```
http://localhost:8501
```

---

# 📊 Example Workflow

1. Upload one or more videos  
2. Add optional YouTube URLs  
3. Click **Process Videos**  
4. AI generates transcripts, translations, summaries, flashcards, and timelines  
5. Use semantic search or chat  

---

# ⚠ Limitations

- Extremely long transcripts may exceed LLM token limits  
- Timeline quality depends on transcription accuracy  
- Real-time streaming not supported  

---

# 🧩 Technologies Used

- Python  
- Streamlit  
- Whisper  
- Sentence Transformers  
- FAISS  
- Groq API  
- MoviePy  
- yt-dlp  
- YouTube Transcript API  

---

# 👨‍💻 Author

Diptarko Bhattacharjee  
B.E. Computer Science and Engineering  
Jadavpur University (2024–2028)

---

# 📜 License

MIT License
