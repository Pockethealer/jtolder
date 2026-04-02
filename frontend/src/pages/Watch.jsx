// src/pages/Watch.jsx
export default function Watch() {
    return (
        <div>
            <h1>Immersion Hub: Watch</h1>
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
                <label>
                    Video: <input type="file" accept="video/mp4,video/webm" />
                </label>
                <label>
                    Subtitles: <input type="file" accept=".srt" />
                </label>
            </div>
            <div style={{ height: '300px', backgroundColor: '#000', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                Video Player Placeholder
            </div>
        </div>
    );
}