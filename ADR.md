# Project Context & Architecture Blueprint
**App Type:** Full-Stack Japanese Language Learning Platform (SPA)
**Core Loop:** Read/Watch (Immersion) -> Look up words -> Save to SRS -> Review (Retention).

## 1. Tech Stack
* **Backend:** Python (FastAPI) - Chosen for its speed and mature Japanese NLP ecosystem.
* **Frontend:** React (SPA) - For building a highly interactive, state-driven client.
* **Database:** PostgreSQL - Essential for managing complex relational SRS data and fast composite-index lookups. Hosted in a dedicated Docker container for resource isolation.
* **NLP/Parsing:** `fugashi` (MeCab wrapper) for high-speed server-side tokenization.

## 2. Core Architectural Decisions
To ensure scalability, low server costs, and cross-platform mobile support, the app adheres to the following constraints:
* **"Lazy-Loaded" Dictionary:** The server does *not* send full dictionary definitions on page load. Definitions are fetched from the database strictly on-demand (when a user clicks/taps a word).
* **Batch SRS Tagging:** On page/subtitle load, the backend tokenizes the text, deduplicates the words, and runs a single batch query against the `user_vocab` table (using a `user_id, word` composite index) to return known/learning/new statuses for UI color-coding.
* **Local-Only Media:** To avoid legal liability and storage costs, users do not upload `.epub` or video files to the server. The React frontend reads files locally via the File API and browser memory.
* **State Syncing, Not File Syncing:** Cross-device synchronization is achieved by saving reading progress (EPUB CFIs) and video timestamps to PostgreSQL, requiring the user to load the local file on the new device to resume.
* **No Server-Side Transcoding:** The app does not transcode video. The frontend performs a "pre-flight" check on local video files. If the codec (e.g., 10-bit MKV) is unsupported by the browser, it gracefully prompts the user to convert it to MP4 (H.264) locally.

## 3. Frontend Routing (The 5-Pillar Structure)
The React SPA is structured flatly by user intent:

1.  **`/` (Landing Page):** Marketing, feature overview, and Login/Signup.
2.  **`/dashboard`:** The logged-in home base. Shows daily SRS review counts and "continue reading/watching" shortcuts.
3.  **`/read` (Immersion Hub):** The document reader. Uses `epub.js`. Renders text as clickable tokens. On mobile, dictionary lookups appear in a Bottom Sheet UI.
4.  **`/watch` (Immersion Hub):** The video player. 
    * *Local:* Uses HTML5 `<video>` and parses local `.srt` files into React state to render clickable subtitles.
    * *YouTube:* Uses the IFrame API. The backend filters for manually verified transcripts (rejecting auto-generated ones) using `youtube-transcript-api`.
5.  **`/review` (Retention Hub):** The native Spaced Repetition System (SRS) using the FSRS algorithm. Fetches a batch of cards, handles reviews entirely client-side for speed, and batch-syncs the results back to the database.
6.  **`/guide` (Support):** Markdown-rendered static pages for tutorials (e.g., "How to use Handbrake") and a link to the community Discord (no custom forum).
7.  **`/labs` (Sandbox):** A space for experimental features (e.g., bulk Anki export, text difficulty analyzers).

## 4. Dictionary Search Logic (Yomitan Style)
When a user clicks a word or phrase, the backend applies:
1.  **De-inflection:** Reversing verb/adjective conjugations using a defined ruleset to find the dictionary form (e.g., 食べられませんでした -> 食べる).
2.  **Longest Prefix Matching:** Scanning ahead in the string to match multi-word idioms rather than isolating single tokens.