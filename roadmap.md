# 🎌 Implementation Roadmap: Yomitan-Powered MVP

This roadmap outlines the vertical slice development plan, integrating both frontend (Vanilla React) and backend (FastAPI/PostgreSQL) at each phase to ensure a testable product increment.

## Phase 1: Foundation & Scaffolding
*Goal: Establish communicating client/server skeletons.*
* **Database:** Spin up `postgres:16-alpine` & `pgadmin` via `docker-compose.yml` (mapped to port 5433).
* **Backend:** Scaffold FastAPI (`api/`, `core/`, `models/`, `services/`). Configure SQLAlchemy & Alembic. Expose `GET /health`.
* **Frontend:** Initialize Vite. Set up CSS variables (`index.css`) and `react-router-dom` skeleton routes. Create native `api/fetchClient.js`.
* **Integration:** Dashboard fetches and displays the `/health` status from the backend.

## Phase 2: NLP Pipeline
*Goal: Parse text server-side and render interactive UI client-side.*
* **Backend:** Implement `fugashi` tokenization in `services/nlp_parser.py`. Expose `POST /api/parse` returning arrays of `[surface, base_form, pos]`.
* **Frontend:** Build `TokenizedText.jsx` using CSS modules to render clickable `<span>` elements, applying styling based on token status.
* **Integration:** Send test strings from React to `/api/parse` and render the output dynamically.

## Phase 3: Yomitan Dictionary Engine
*Goal: Import dictionary data and build the lookup popup.*
* **Backend:** Define SQLAlchemy models (`terms`, `kanji`, `tags`). Write an offline Python script to batch-insert Yomitan ZIP JSONs.
* **Backend:** Implement de-inflection/prefix-matching logic. Expose `GET /api/dictionary`.
* **Frontend:** Build the CSS-animated Bottom Sheet component for definition display.
* **Integration:** Bind an `onClick` event in `TokenizedText.jsx` to fetch and display definitions in the Bottom Sheet.

## Phase 4: Media Immersion
*Goal: Parse user-provided EPUBs and Videos through the NLP pipeline.*
* **Reader (`/read`):** Integrate `epub.js`. Intercept text from the active viewport, send to `/api/parse`, and swap raw text with `TokenizedText.jsx`.
* **Player (`/watch`):** Build HTML5 `<video>` UI. Write a vanilla JS `.srt` parser. Use `onTimeUpdate` to sync subtitles, sending the active subtitle line to `/api/parse` for rendering.

## Phase 5: Spaced Repetition System (SRS)
*Goal: Track user vocabulary and schedule reviews.*
* **Backend:** Create `user_vocab` table with a composite index (`user_id`, `word`). Modify `/api/parse` to batch-check and append known/learning status.
* **Backend:** Implement FSRS algorithm. Expose endpoints: `/api/srs/add`, `/api/srs/queue`, `/api/srs/grade`.
* **Frontend:** Create `SrsContext.jsx` for native global state. Build Flashcard UI (`/review`) with 4 grading buttons.
* **Integration:** Fetch daily queue, process grades locally in React Context, and batch-sync back to the backend transparently.

## Phase 6: Polish & The Hub
*Goal: Finalize the user loop and documentation.*
* **Hub (`/guide`):** Write static Markdown guides (e.g., Handbrake `.mkv` to `.mp4` tutorial, EPUB sourcing) and render them client-side.
* **Dashboard:** Aggregate `SrsContext` data to show live stats (e.g., "Cards due today").
* **UX Guardrails:** Add `HTMLMediaElement.canPlayType()` check to the video player to gracefully reject unsupported codecs before playback fails.