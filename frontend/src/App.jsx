// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Read from './pages/Read';
import Watch from './pages/Watch';
import Review from './pages/Review';
import Guide from './pages/Guide';
import styles from './App.module.css'; // We'll create this next

function App() {
  return (
    <Router>
      <nav className={styles.navbar}>
        <div className={styles.logo}>🎌 Yomitan MVP</div>
        <div className={styles.links}>
          <Link to="/">Home</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/read">Read</Link>
          <Link to="/watch">Watch</Link>
          <Link to="/review">Review</Link>
          <Link to="/guide">Guide</Link>
        </div>
      </nav>

      <main className={styles.mainContent}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/read" element={<Read />} />
          <Route path="/watch" element={<Watch />} />
          <Route path="/review" element={<Review />} />
          <Route path="/guide" element={<Guide />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;