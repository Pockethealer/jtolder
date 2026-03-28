# 🎌 Frontend Agile Backlog: React SPA (Lean Architecture)

**Methodology:** Component-driven development using native Web APIs (`fetch`), native React state (`Context`), and scoped CSS Modules. 

**Allowed External Dependencies:** * `react` & `react-dom`
* `react-router-dom` (Essential for SPA routing)
* `epub.js` (Mandatory for EPUB parsing)

---

## Epic 1: Scaffolding & Routing (The Skeleton)
*Goal: Get the React app running with CSS Modules and page navigation.*

- [ ] **Task 1.1: Vite & CSS Variables Initialization**
  - **Action:** Run `npm create vite@latest` (select React/JS). Clear out the default CSS. Set up `index.css` with a robust set of CSS variables (`--color-bg`, `--color-primary`, `--font-main`) to act as your design system.
  - **Testing:** Run `npm run dev`. Create a basic `div` using your CSS variables and ensure it renders correctly.
  - **Estimated Time:** 1 Hour

- [ ] **Task 1.2: App Routing & Layouts**
  - **Action:** Install `react-router-dom`. Create placeholder components for the 5 main routes (`/dashboard`, `/read`, `/watch`, `/review`, `/guide`). Build a Top Navigation bar using a `.module.css` file for styling.
  - **Testing:** Click through the navigation bar and verify the URL and screen content changes without a full page reload.
  - **Estimated Time:** 1.5 Hours

---

## Epic 2: The Core API Client & State
*Goal: Connect React to the Python backend natively.*

- [ ] **Task 2.1: Native Fetch Wrapper**
  - **Action:** Create `api/fetchClient.js`. Write a custom function that wraps the native `fetch()` API, automatically prepends `http://localhost:8000`, adds standard headers (`Content-Type: application/json`), and handles error throwing for non-2xx responses.
  - **Testing:** On the Dashboard mount, fetch the FastAPI `/health` endpoint and `console.log` the result.
  - **Estimated Time:** 1 Hour

- [ ] **Task 2.2: Global State (React Context)**
  - **Action:** Create `context/UserContext.jsx`. Use `createContext` and `useState` to hold dummy user settings (e.g., target daily review count). Wrap your `<App />` in this provider.
  - **Testing:** Consume the context in the Dashboard and display the daily review count. Update the state via a test button and watch the UI react.
  - **Estimated Time:** 1 Hour

---

## Epic 3: The Dictionary UI (The Pop-up)
*Goal: Build the interactive dictionary UI using vanilla CSS.*

- [ ] **Task 3.1: Tokenized Text Component**
  - **Action:** Build a `TokenizedText` component taking a dummy array of words. Use CSS Modules to create classes for `.known`, `.learning`, and `.new`, applying colors via your CSS variables.
  - **Testing:** Render this on the `/labs` page and ensure the text color-codes correctly based on the dummy JSON.
  - **Estimated Time:** 1.5 Hours

- [ ] **Task 3.2: The Dictionary Bottom Sheet**
  - **Action:** Create a Bottom Sheet component using CSS `position: fixed; bottom: 0;` and a simple CSS transition for sliding up. 
  - **Testing:** Hardcode a dummy Yomitan JSON definition. Click a word in the `TokenizedText` component to trigger the CSS transition and show the definition.
  - **Estimated Time:** 2 Hours

- [ ] **Task 3.3: Wire Dictionary to Backend**
  - **Action:** Swap the dummy definition with a real call using your `fetchClient` to the `/api/dictionary` endpoint.
  - **Testing:** Click a word and watch the real database definition load into the UI.
  - **Estimated Time:** 1 Hour

---

## Epic 4: The EPUB Reader
*Goal: Load a local book and inject our clickable dictionary tokens.*

- [ ] **Task 4.1: Local File Loader & `epub.js`**
  - **Action:** Install `epub.js`. Build a native `<input type="file" accept=".epub" />`. Pass the file to `epub.js` and render the canvas.
  - **Testing:** Successfully read a local Japanese EPUB in the browser and page through it.
  - **Estimated Time:** 2 Hours

- [ ] **Task 4.2: Text Interception & Tokenization**
  - **Action:** Grab the raw text from the `epub.js` view, send it to the `/api/parse` endpoint via `fetch`, and replace the view with our `TokenizedText` component.
  - **Testing:** Open the book, wait for the fetch request to resolve, and watch the text become clickable.
  - **Estimated Time:** 3 Hours

---

## Epic 5: The SRS Flashcard Interface
*Goal: Manage SRS state using native React APIs.*

- [ ] **Task 5.1: The Flashcard UI**
  - **Action:** Build the visual card and the 4 grading buttons. Style them cleanly with CSS Modules.
  - **Testing:** Render the card with dummy data and test the button hover states.
  - **Estimated Time:** 1.5 Hours

- [ ] **Task 5.2: SRS Context & API Integration**
  - **Action:** Create `context/SrsContext.jsx`. Fetch the daily queue on mount. As the user grades cards, update the local context state immediately, and send a background `fetch` request to `POST /api/srs/grade`.
  - **Testing:** Complete a review session, refresh the page, and ensure the queue is empty.
  - **Estimated Time:** 2.5 Hours

---

## Epic 6: The Video Player
*Goal: Play local video and sync parsed subtitles without external video libraries.*

- [ ] **Task 6.1: HTML5 Video & Native SRT Parsing**
  - **Action:** Use the native `<video>` tag. Allow the user to upload a local `.mp4` and `.srt`. Write a pure JavaScript function (no external libraries) to parse the `.srt` timestamps into an array of objects.
  - **Testing:** Use the video's `onTimeUpdate` event to display the correct subtitle text below the video.
  - **Estimated Time:** 2.5 Hours

- [ ] **Task 6.2: Subtitle Tokenization Integration**
  - **Action:** Pass the active subtitle string through `/api/parse` and render it using the `TokenizedText` component.
  - **Testing:** Pause the video, click a subtitle word, and watch the Dictionary pop-up appear.
  - **Estimated Time:** 1.5 Hours