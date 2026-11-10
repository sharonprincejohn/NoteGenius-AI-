# 🧠 NoteGenius AI – Intelligent Study Assistant

> **"Upload. Understand. Learn Smarter."**  
> An intelligent, AI-powered study companion that helps students understand complex academic materials using Google Gemini Generative AI and lightweight Retrieval-Augmented Generation (RAG).

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/AI-Google%20Gemini%20API-8E75C4.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Free Tier Friendly](https://img.shields.io/badge/Cost-100%25%20Free%20Tier-success.svg)](#)

---

## 📖 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Technology Stack](#-technology-stack)
4. [System Architecture](#-system-architecture)
5. [Lightweight RAG Pipeline](#-lightweight-rag-pipeline)
6. [Installation & Setup](#-installation--setup)
7. [Environment Variables](#-environment-variables)
8. [How to Run](#-how-to-run)
9. [Project Directory Structure](#-project-directory-structure)
10. [Application Preview & Screenshots](#-application-preview--screenshots)
11. [Testing](#-testing)
12. [Security & Reliability](#-security--reliability)
13. [Future Enhancements](#-future-enhancements)
14. [Contributing & License](#-contributing--license)

---

## 🌟 Project Overview

**NoteGenius AI** is an intelligent academic study assistant built to eliminate the struggle of dense textbooks, lengthy lecture slides, and unorganized notes. Designed for laptops with standard hardware (e.g., 8 GB RAM, no GPU required), NoteGenius AI enables students to upload multiple PDFs and instantly transform them into:
- Structured, student-friendly **summaries** and **cheat sheets**.
- Grounded **chat with documents** powered by TF-IDF Retrieval-Augmented Generation (RAG).
- Interactive **multiple-choice quizzes** with instant scoring and explanations.
- Active recall **flashcards** with interactive flip-to-reveal answers.
- **Deep-dive Study Mode** lessons using intuitive analogies, examples, and practice questions.

Built strictly using **100% free libraries** and Google Gemini's **free API tier quota**, the app never requires paid subscriptions or GPU servers.

---

## ✨ Key Features

### 📤 1. Multi-PDF Document Ingestion & Reader
- Upload single or multiple PDF documents simultaneously (lecture slides, notes, syllabus).
- Extracts clean text from all pages while preserving page numbers and document names.
- Automatic detection of empty or scanned image PDFs with clear user warnings.
- Robust handling of password-protected, corrupted, or malformed files.
- Document preview modal to inspect extracted text page-by-page.

### 📝 2. AI Notes Summarizer
- Three versatile summary formats:
  - **Quick Overview (Exam Crunch):** High-yield 3–5 minute read highlighting top takeaways and memory hooks.
  - **Comprehensive Study Guide:** Detailed section-by-section breakdown with definitions and applications.
  - **Definitions & Formula Cheat Sheet:** Quick-reference glossary of core principles, laws, and equations.
- Optional custom focus field to direct the summary to specific chapters or concepts.
- Strict anti-hallucination prompt engineering: only summarizes what is present in the uploaded material.
- One-click Markdown export (`.md`) to save summaries locally.

### 💬 3. Chat with PDF (Grounded RAG Assistant)
- Ask natural language questions about your uploaded study notes.
- Uses a lightweight TF-IDF and Cosine Similarity retriever (instant CPU execution, zero GPU memory).
- Retrieved chunks are injected into Gemini's context window with document and page citations.
- **Zero-Hallucination Guardrail:** If an answer is not present in the notes, the assistant clearly states: *"This information is not found in your uploaded study notes."*
- Real-time response streaming for conversational responsiveness.
- Collapsible source references panel displaying exact document names, page numbers, and relevance match scores.

### 🎯 4. AI Quiz Generator
- Generates interactive multiple-choice quizzes (3, 5, 8, or 10 questions) at Easy, Medium, or Hard difficulty.
- 4 options per question with strict grounding in uploaded notes.
- Interactive submission with instant evaluation and achievement badges (*Master Genius*, *Great Progress*, etc.).
- Detailed explanations for every question explaining why an answer is correct based on the source text.

### 🗂️ 5. AI Flashcard Generator
- Generates active recall flashcards with question/prompt on the front and explanation on the back.
- Interactive card player with clean flip animation to reveal answers.
- Sequential card navigation (`Previous`, `Flip`, `Next`), progress bar, and category tags.
- Full deck preview drawer to browse all cards at once.

### 💡 6. Deep-Dive Study Mode
- Automated discovery of core topics and chapters directly from the notes.
- Explains difficult concepts using:
  - **The Intuition (ELI5):** Jargon-free mental model.
  - **Formal Definition:** Academic definitions strictly from notes.
  - **Real-World Analogy:** Tangible, everyday comparisons.
  - **Worked Example:** Practical step-by-step application.
  - **Common Exam Pitfalls:** Mistakes students frequently make on tests.
  - **Self-Check Questions:** Immediate practice questions with collapsible answers.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ | Core programming language |
| **Frontend UI** | Streamlit | Responsive, interactive single-page web application |
| **Generative AI** | Google Gemini API & Groq Cloud API | Text synthesis, summarization, quiz, and flashcards |
| **AI SDKs** | Google GenAI SDK & Groq Python SDK | Official SDKs with dynamic runtime provider switching |
| **PDF Extraction** | PyMuPDF (`fitz`) + `pypdf` | High-speed PDF text and page extraction with pure-Python fallback |
| **Document Retrieval** | Scikit-learn (`TfidfVectorizer` + `cosine_similarity`) | In-memory, CPU-friendly lightweight RAG pipeline |
| **Environment Config** | Python-dotenv | Secure `.env` variable management |
| **Styling** | Custom CSS / Theme Tokens | Soft lavender and purple modern study theme |
| **Version Control** | Git | Clean source code versioning |

---

## 🏗️ System Architecture

```
NoteGenius-AI/
│
├── app.py                      # Main Streamlit application and view router
├── config.py                   # Central constants, UI tokens, models & prompts
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment variables
├── .env                        # Local API key storage (git-ignored)
├── .gitignore                  # Git ignore rules
├── test_core.py                # Automated unit and integration test suite
├── README.md                   # Project documentation
│
├── modules/
│   ├── pdf_reader.py           # Multi-engine PDF extractor (PyMuPDF / pypdf)
│   ├── text_chunker.py         # Context-preserving overlapping text chunker
│   ├── retriever.py            # Scikit-learn TF-IDF & cosine similarity RAG
│   ├── ai_service.py           # Gemini SDK service with error handling & streaming
│   ├── summarizer.py           # Quick, Detailed, & Cheat Sheet summarizer
│   ├── quiz_generator.py       # JSON MCQ quiz maker with scoring engine
│   ├── flashcards.py           # Active recall flashcard deck generator
│   └── study_mode.py           # Pedagogical deep-dive tutor & topic analyzer
│
├── components/
│   ├── sidebar.py              # Branding, navigation, and API key manager
│   ├── dashboard.py            # Welcome hero, metrics, and multi-file uploader
│   └── document_cards.py       # Document management cards & text previewer
│
└── assets/
    └── logo.png                # Modern NoteGenius AI branding logo
```

---

## 🔍 Lightweight RAG Pipeline

For students running on everyday laptops (e.g., 8 GB RAM without an expensive dedicated GPU), standard heavy vector databases and multi-gigabyte embedding models can cause sluggish performance or memory crashes.

NoteGenius AI solves this with an ultra-lightweight, high-speed in-memory pipeline:

1. **PDF Ingestion:** Text is extracted page-by-page, recording exact page numbers and document titles.
2. **Context-Aware Chunking:** Paragraphs and sentences are grouped into ~750-character chunks with a 150-character sliding overlap.
3. **TF-IDF Vectorization:** Scikit-learn indexes unigram and bigram tokens with sublinear term-frequency scaling. Fits in milliseconds and uses < 10 MB RAM.
4. **Cosine Similarity Matching:** User queries are vectorized and compared against all chunk vectors in parallel.
5. **Context Assembly & Grounding:** The top 3–4 chunks above the relevance threshold are formatted with source citations and sent to Google Gemini with strict zero-hallucination instructions.

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your machine.
- A free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/NoteGenius-AI.git
cd NoteGenius-AI
```

### 3. Create and Activate a Virtual Environment
**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

1. Copy `.env.example` to create your local `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in any text editor and add your free Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_gemini_api_key_here
   GEMINI_MODEL=gemini-3.8-flash
   ```

*(Alternatively, you can also paste your API key directly into the secure API input field in the NoteGenius AI sidebar at runtime!)*

---

## 🖥️ How to Run

Launch the Streamlit application by running:

```bash
streamlit run app.py
```

The application will start immediately and open in your default browser at:
```
http://localhost:8501
```

---

## 🧪 Testing

Run the included automated test suite to verify all core components:

```bash
python test_core.py
```

**What the test suite validates:**
- [x] Text chunking logic with sentence boundary and overlap verification.
- [x] TF-IDF RAG indexing and cosine similarity query retrieval.
- [x] Document citation formatting and page tracking.
- [x] Quiz scoring engine, percentage calculation, and badge assignment.
- [x] Flashcard JSON parser and sanitization.
- [x] Graceful error handling when API key is missing.
- [x] Empty, scanned, and password-protected PDF detection.

---

## 🛡️ Security & Reliability

- **Key Privacy:** API keys are read securely from `.env` or session memory. Keys are never logged, committed to Git, or exposed in the UI.
- **Strict Grounding:** Prompts include explicit anti-hallucination guardrails instructing Gemini never to fabricate facts outside the uploaded notes.
- **Quota & Rate-Limit Resilience:** Built-in error handling catches HTTP 429 and Resource Exhausted responses, advising students with friendly countdown guidance.
- **Input Validation:** Restricts uploads strictly to `.pdf` files, limits file size to 25 MB, and handles corrupted or unreadable files gracefully.

---

## 🔮 Future Enhancements

- [ ] **Handwritten Notes OCR:** Integration of free Tesseract OCR for scanned handwritten notes.
- [ ] **Voice Q&A:** Voice-to-text queries and audio read-aloud for flashcards.
- [ ] **Anki Deck Export (.apkg):** One-click export of generated flashcards directly to Anki.
- [ ] **Study Schedule Planner:** Automated calendar scheduling based on syllabus topics.
- [ ] **Mind Map Visualizer:** Interactive concept graphs generated using Mermaid.js.

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute for academic and personal projects.

