# 🎌 Backend Agile Backlog: Yomitan Platform

**Methodology:** Incremental delivery. No feature is considered "Done" until it can be manually tested via the FastAPI Swagger UI or a basic automated test.

---

## Epic 1: Infrastructure & Skeleton (The Foundation)
*Goal: Get the server running and talking to the database.*

- [*] **Task 1.1: Initialize FastAPI & Docker DB**
  - **Action:** Spin up `docker-compose.yml`, create the `main.py` entry point, and write a simple `GET /health` route.
  - **Testing:** Visit `http://localhost:8000/docs` and execute the `/health` endpoint. It should return `{"status": "ok"}`.
  - **Estimated Time:** 1 Hour

- [*] **Task 1.2: SQLAlchemy Setup & Alembic Migrations**
  - **Action:** Configure `core/database.py` using `.env` credentials. Install Alembic and initialize it to track database schema changes. Create a dummy test table.
  - **Testing:** Run `alembic upgrade head`. Check pgAdmin (`http://localhost:5050`) to verify the dummy table was created in your PostgreSQL container.
  - **Estimated Time:** 2 Hours

---

## Epic 2: The NLP Engine (Tokenization)
*Goal: Parse raw Japanese text into an array of words without touching the database.*

- [*] **Task 2.1: Integrate `fugashi` (MeCab)**
  - **Action:** Install `fugashi` and `unidic-lite`. Write a standalone Python function in `services/nlp_parser.py` that takes a Japanese string and returns a list of dictionaries (surface form, dictionary form, part of speech).
  - **Testing:** Write a simple `pytest` script: `test_parser.py` to assert that "食べた" correctly returns "食べる" as its base form.
  - **Estimated Time:** 2 Hours

- [*] **Task 2.2: Build the `/api/parse` Endpoint**
  - **Action:** Create the FastAPI router. It should accept a POST request with a JSON payload `{"text": "..."}` and return the tokenized array.
  - **Testing:** Open Swagger UI, paste a Japanese paragraph into the `/api/parse` request body, and verify the JSON response is correctly chunked.
  - **Estimated Time:** 1 Hour

---

## Epic 3: Dictionary Import & Storage (The Heavy Lifter)
*Goal: Successfully parse a Yomitan .zip file and store it in PostgreSQL.*

- [ ] **Task 3.1: Define the Dictionary Database Schema**
  - **Action:** Create SQLAlchemy models in `models/dictionary.py` for `Terms`, `TermTags`, and `Kanji`. Generate an Alembic migration and apply it.
  - **Testing:** Verify the tables and columns exist in pgAdmin.
  - **Estimated Time:** 1.5 Hours

- [ ] **Task 3.2: Build the ZIP Extraction Script**
  - **Action:** Write an offline Python script (not an API endpoint) that unzips a Yomitan dictionary, reads `index.json`, and iterates through the `term_bank_*.json` files.
  - **Testing:** `print()` the first 10 entries of the first term bank to the terminal to verify the JSON array mapping works.
  - **Estimated Time:** 2 Hours

- [ ] **Task 3.3: Implement Bulk Insert Logic**
  - **Action:** Connect the extraction script to SQLAlchemy. Use bulk inserts (e.g., `session.bulk_insert_mappings`) to push chunks of 10,000 words into PostgreSQL. Create indexes on the `term` and `reading` columns.
  - **Testing:** Run the script on the JMdict ZIP. Open pgAdmin and query `SELECT count(*) FROM terms;` to verify hundreds of thousands of rows were added successfully.
  - **Estimated Time:** 3 Hours

---

## Epic 4: Dictionary Lookup Logic (The Brains)
*Goal: Given a word from the frontend, return the Yomitan definition.*

- [ ] **Task 4.1: Basic Exact Match Query**
  - **Action:** Write a function in `services/yomitan_logic.py` that queries the database for an exact string match. Create the `GET /api/dictionary?word=...` endpoint.
  - **Testing:** Use Swagger UI to search for "猫" and verify the JSON definition is returned instantly.
  - **Estimated Time:** 1.5 Hours

- [ ] **Task 4.2: Implement De-inflection Logic**
  - **Action:** Add a de-inflection ruleset (JSON map) to the service. If "食べられませんでした" is queried, the code strips suffixes until it finds "食べる" in the database.
  - **Testing:** Write `pytest` cases for 5 different verb conjugations (passive, potential, past, negative) to ensure they all resolve to their dictionary forms.
  - **Estimated Time:** 3-4 Hours

---

## Epic 5: User State & SRS (The Memory)
*Goal: Track what words the user knows and schedule them for review.*

- [ ] **Task 5.1: User Vocab Schema & Batch Lookup**
  - **Action:** Create the `user_vocab` SQLAlchemy model (with the composite index). Update the `/api/parse` endpoint to accept an optional `user_id`. If provided, cross-reference the tokens against the user's saved words and attach a `status` (known/learning) to the output.
  - **Testing:** Manually insert a "known" word into the DB via pgAdmin. Send a paragraph containing that word to `/api/parse` via Swagger UI. Verify that specific token returns with `"status": "known"`.
  - **Estimated Time:** 2 Hours

- [ ] **Task 5.2: SRS CRUD Endpoints**
  - **Action:** Create `POST /api/srs/add` (to save a new word) and `GET /api/srs/queue` (to fetch today's due cards).
  - **Testing:** Use Swagger UI to add a word, then call the queue endpoint to ensure it appears in the list.
  - **Estimated Time:** 2 Hours