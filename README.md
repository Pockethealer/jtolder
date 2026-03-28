# 🎌 Yomitan-Powered Japanese Learning Platform (MVP)

An open-source, full-stack Japanese language learning platform designed for seamless immersion and retention. It combines a local-first media consumption experience (EPUBs and Video) with a highly scalable, server-side Yomitan dictionary and native Spaced Repetition System (SRS).

## 🏗 Tech Stack

* **Backend:** Python 3.11+, FastAPI
* **Frontend:** React (Vite / Next.js)
* **Database:** PostgreSQL (Containerized)
* **NLP Processing:** `fugashi` (MeCab)
* **Media Parsing:** `epub.js`, HTML5 Video

## ✨ MVP Features

* 📖 **Local EPUB Reader:** Read Japanese text with instant, on-click tokenization and Yomitan dictionary lookups.
* 🎬 **Local Video Player:** Sync `.srt` files to local video files (`.mp4`, `.webm`) for interactive, clickable subtitles.
* 🧠 **Native SRS Dashboard:** FSRS-powered flashcard system to review saved vocabulary.
* ⚡ **Lazy-Loaded Architecture:** Dictionary definitions and SRS metadata are fetched on-demand to keep initial page loads instantaneous.

## 📂 Project Structure

```text
├── backend/            # FastAPI server, Python NLP tools, and database models
├── frontend/           # React SPA, UI components, and state management
├── docker-compose.yml  # Local PostgreSQL database and (optional) PgAdmin/Redis
├── ADR.md # Detailed system design and architecture decisions
└── README.md