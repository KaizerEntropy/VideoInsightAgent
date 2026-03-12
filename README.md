## 🌐 Live Demo

Try the application here:

https://videoinsightagent.streamlit.app

# 🎥 Video Insight Agent

An AI-powered system that transforms videos into searchable knowledge.

Video Insight Agent allows users to upload videos or provide YouTube links, automatically transcribe the content, generate structured insights, and interact with the video using semantic search and AI question answering.

---

# 🚀 Features

### 📹 Multi-Video Processing

Supports:

* Single uploaded video
* Multiple uploaded videos
* Single YouTube video
* Multiple YouTube videos

All videos are processed together and indexed into a unified semantic search system.

---

### 🎙 Automatic Transcription

Two transcription pipelines are used:

**Uploaded videos**

```
Video → Audio Extraction → Whisper Transcription
```

**YouTube videos**

```
YouTube URL → Transcript API
```

Each transcript is broken into timestamped segments.

---

### 🧠 AI Video Understanding

The system generates:

* AI summaries
* Study flashcards
* Timestamped timelines
* Semantic search results
* Conversational answers

---

### ⏱ Timeline Generation

Each processed video receives a structured timeline of important moments.

Example:

```
0:00 — Introduction to the software
0:45 — Demonstration of typing transcript
1:20 — Keyboard shortcuts overview
2:10 — Timestamp insertion method
3:30 — Workflow explanation
```

---

### 🔎 Semantic Timestamp Search

Users can search for concepts inside videos.

Example:

```
keyboard shortcuts
```

The system returns the most relevant timestamp and transcript segment.

---

### 💬 Conversational Video QA

Users can ask questions like:

```
What software is demonstrated in the video?
```

The AI answers using retrieved transcript segments and provides timestamp citations.

Example:

```
Answer:
The video demonstrates the transcription tool Inkscribe.

Sources:
YouTube Video 1 — 0:35
Uploaded Video 1 — 1:04
```

---

# 🧠 System Architecture

The system consists of several stages.

### 1️⃣ Input Layer

The system accepts:

* Uploaded video files
* YouTube URLs

---

### 2️⃣ Transcription Layer

Uploaded videos:

```
Video → Audio Extraction → Whisper
```

YouTube videos:

```
YouTube → Transcript API
```

Both produce timestamped segments.

---

### 3️⃣ Transcript Segmentation

Each transcript becomes segments like:

```
Video Label | Timestamp | Text
```

Example:

```
YouTube Video 1 | 1:24 | The software allows users to insert timestamps while typing.
```

---

### 4️⃣ Vector Search

All segments are embedded and stored in a vector index.

This enables:

* semantic search
* retrieval-augmented question answering

---

### 5️⃣ LLM Processing

The transcript is processed by an LLM to generate:

* summary
* flashcards
* timelines

---

### 6️⃣ Retrieval-Augmented Generation

When a user asks a question:

1. Query embedding is created
2. Relevant transcript segments are retrieved
3. The LLM receives those segments as context
4. The answer is generated with timestamp citations

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
│   └── youtube_transcript.py
│
├── downloads
└── tests
```

---

# ⚙️ Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/video-insight-agent.git
```

Move into the project directory:

```
cd video-insight-agent
```

Create a virtual environment:

```
python -m venv venv
```

Activate it.

Linux / macOS

```
source venv/bin/activate
```

Windows

```
venv\\Scripts\\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

# ▶ Running the Application

Start the Streamlit server:

```
streamlit run app.py
```

The interface will open at:

```
http://localhost:8501
```

---

# 📊 Example Workflow

1️⃣ Upload one or more videos
2️⃣ Add optional YouTube URLs
3️⃣ Click **Process Videos**
4️⃣ AI generates transcripts, summaries, flashcards, and timelines
5️⃣ Use **Semantic Search** or **Chat** to interact with the videos

---

# ⚠ Limitations

* Extremely long transcripts may exceed LLM token limits.
* Timeline quality depends on transcript accuracy.
* Real-time streaming video is not currently supported.

---

# 🧩 Technologies Used

* Python
* Streamlit
* Whisper
* Sentence Transformers
* FAISS
* Groq LLM API
* MoviePy
* yt-dlp
* YouTube Transcript API

---

# 👨‍💻 Author

Diptarko Bhattacharjee
B.E. Computer Science and Engineering
Jadavpur University, 2024-2028

---

# 📜 License

MIT License
